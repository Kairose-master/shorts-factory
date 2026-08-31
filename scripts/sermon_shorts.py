#!/usr/bin/env python3
"""Tier 0 sermon-to-Shorts pipeline — 방배동 예심교회.

Four stages, each runnable on its own so a failure never costs you the
stages that already succeeded:

  fetch       yt-dlp the sermon into office/production/<id>/source/
  transcribe  Korean transcript with timecodes (whisper.cpp or Gemini)
  clips       print the transcript for reading, then validate clips.json
  render      cut → 9:16 crop → Korean subtitle burn-in → MP4

Clip selection is deliberately NOT automated. Stage `clips` prints a
timecoded transcript and stops; a human (or Claude) reads it and writes
clips.json with a stated reason per clip. A keyword heuristic cannot tell
the difference between a pastor's throwaway aside and the line the whole
sermon turns on, and guessing badly here is worse than not guessing.

Nothing in this file uploads anything. Rendering is the last step; publishing
is a human decision, every time.

Usage:
  python3 scripts/sermon_shorts.py fetch      SUN-2026-08-30 --url <youtube-url>
  python3 scripts/sermon_shorts.py transcribe SUN-2026-08-30 [--backend auto]
  python3 scripts/sermon_shorts.py clips      SUN-2026-08-30 [--window 12]
  python3 scripts/sermon_shorts.py render     SUN-2026-08-30 [--only clip-01]
  python3 scripts/sermon_shorts.py doctor
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROD = REPO / "office" / "production"
FONT_DIR = os.environ.get("FONT_DIR", "/usr/local/share/fonts")
FONT_NAME = "Noto Sans KR"

# 9:16 at the resolution YouTube Shorts actually wants.
OUT_W, OUT_H = 1080, 1920


# --------------------------------------------------------------- helpers ---
def die(msg: str, code: int = 1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, **kw)


def idea_dir(idea_id: str) -> Path:
    return PROD / idea_id


def need(idea_id: str) -> Path:
    d = idea_dir(idea_id)
    if not d.exists():
        die(f"{d.relative_to(REPO)} does not exist — run `fetch` first")
    return d


def ts(seconds: float) -> str:
    """Seconds → SRT timestamp."""
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def hhmmss(seconds: float) -> str:
    s = int(seconds)
    return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}"


def parse_time(v) -> float:
    """Accept 90, '90', '1:30' or '00:01:30.5'."""
    if isinstance(v, (int, float)):
        return float(v)
    parts = str(v).strip().split(":")
    return sum(float(p) * 60**i for i, p in enumerate(reversed(parts)))


# ----------------------------------------------------------------- fetch ---
def cmd_fetch(args):
    d = idea_dir(args.idea_id)
    src = d / "source"
    src.mkdir(parents=True, exist_ok=True)

    if not shutil.which("yt-dlp"):
        die("yt-dlp not installed — run: bash scripts/setup_render_env.sh")

    print(f"==> fetching {args.url}")
    try:
        run([
            "yt-dlp",
            "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
            "--merge-output-format", "mp4",
            "--write-info-json", "--no-playlist",
            "-o", str(src / "sermon.%(ext)s"),
            args.url,
        ])
    except subprocess.CalledProcessError:
        die(
            "yt-dlp failed.\n"
            "  If the error mentions 'Tunnel connection failed: 403', YouTube is\n"
            "  blocked by this environment's egress policy, not by yt-dlp.\n"
            "  See docs/environment-constraints.md for the two ways around it."
        )

    (d / "meta.json").write_text(
        json.dumps({"idea_id": args.idea_id, "source_url": args.url}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"==> source in {src.relative_to(REPO)}")


# ------------------------------------------------------------ transcribe ---
def find_source(d: Path) -> Path:
    for p in sorted((d / "source").glob("sermon.*")):
        if p.suffix.lower() in (".mp4", ".mkv", ".webm", ".m4a", ".mp3", ".wav"):
            return p
    die(f"no source media in {(d / 'source').relative_to(REPO)} — run `fetch` first")


def extract_audio(video: Path, out: Path) -> Path:
    """16 kHz mono WAV — what every ASR backend wants."""
    if out.exists():
        return out
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(out)])
    return out


def transcribe_whisper(wav: Path, model: str) -> list[dict]:
    """whisper.cpp with a multilingual model. large-v3, never *.en —
    the .en models are English-only and cannot read Korean."""
    exe = shutil.which("whisper-cli") or shutil.which("main") or shutil.which("whisper")
    if not exe:
        raise RuntimeError("whisper.cpp binary not found")
    if not Path(model).exists():
        raise RuntimeError(f"model not found: {model}")
    if ".en" in Path(model).name:
        raise RuntimeError(f"{Path(model).name} is English-only; Korean needs large-v3")

    out = wav.with_suffix("")
    run([exe, "-m", model, "-f", str(wav), "-l", "ko", "-oj", "-of", str(out)])
    data = json.loads(Path(f"{out}.json").read_text(encoding="utf-8"))
    segs = []
    for s in data.get("transcription", []):
        off = s.get("offsets", {})
        segs.append({
            "start": off.get("from", 0) / 1000.0,
            "end": off.get("to", 0) / 1000.0,
            "text": s.get("text", "").strip(),
        })
    return segs


def transcribe_gemini(wav: Path) -> list[dict]:
    """Gemini transcription. Costs one API call per chunk — this is a paid
    API. Used only when whisper is unavailable."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise RuntimeError("pip3 install google-genai")

    client = genai.Client(api_key=key)
    print("  uploading audio to Gemini (1 paid call)…")
    f = client.files.upload(file=str(wav))
    prompt = (
        "이 한국어 설교 오디오를 전사하라. 화자가 실제로 말한 그대로 적고, "
        "요약하거나 다듬지 말 것. JSON 배열만 출력하라. 각 원소는 "
        '{"start": 초(float), "end": 초(float), "text": "발화"} 형식이고, '
        "한 원소는 한 문장 또는 8초 이내로 끊는다. 설명 문장은 쓰지 말 것."
    )
    resp = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[f, prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    segs = json.loads(resp.text)
    return [{"start": float(s["start"]), "end": float(s["end"]),
             "text": str(s["text"]).strip()} for s in segs]


def cmd_transcribe(args):
    d = need(args.idea_id)
    video = find_source(d)
    wav = extract_audio(video, d / "source" / "audio16k.wav")
    print(f"==> audio: {wav.relative_to(REPO)}")

    model = os.environ.get("WHISPER_MODEL", "models/ggml-large-v3.bin")
    backends = [args.backend] if args.backend != "auto" else ["whisper", "gemini"]

    segs, used, errs = None, None, []
    for b in backends:
        try:
            print(f"==> transcribing via {b}")
            segs = transcribe_whisper(wav, model) if b == "whisper" else transcribe_gemini(wav)
            used = b
            break
        except Exception as e:  # noqa: BLE001 — report and try the next backend
            errs.append(f"  {b}: {e}")
            print(f"    {b} unavailable: {e}")

    if segs is None:
        die("no transcription backend worked:\n" + "\n".join(errs))

    (d / "transcript.json").write_text(
        json.dumps({"backend": used, "language": "ko", "segments": segs},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    write_srt(segs, d / "transcript.srt")
    print(f"==> {len(segs)} segments via {used} → transcript.json / transcript.srt")


def write_srt(segs: list[dict], path: Path, offset: float = 0.0):
    lines = []
    for i, s in enumerate(segs, 1):
        start, end = s["start"] - offset, s["end"] - offset
        if end <= 0:
            continue
        lines += [str(i), f"{ts(max(0.0, start))} --> {ts(end)}", s["text"], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def ass_ts(seconds: float) -> str:
    """Seconds → ASS timestamp (H:MM:SS.cc)."""
    cs = int(round(max(0.0, seconds) * 100))
    h, cs = divmod(cs, 360_000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def wrap_korean(text: str, per_line: int = 16, max_lines: int = 3) -> str:
    """Break on word boundaries into short lines.

    Korean has spaces between 어절, so wrapping on them is safe and reads far
    better than libass's own greedy fill at this font size.
    """
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > per_line:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return "\\N".join(lines[:max_lines])


def write_ass(segs: list[dict], path: Path, offset: float = 0.0,
              font_size: int = 64, margin_v: int = 260):
    """Burn-in subtitles as ASS.

    SRT carries no resolution, so libass falls back to a 384x288 script and
    scales every style number up from there — a Fontsize/MarginV tuned in real
    pixels lands in the wrong place. ASS lets us state PlayRes explicitly, so
    the numbers below mean what they say at 1080x1920.
    """
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {OUT_W}
PlayResY: {OUT_H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{FONT_NAME},{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,5,2,2,70,70,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    rows = []
    for s in segs:
        start, end = s["start"] - offset, s["end"] - offset
        if end <= 0:
            continue
        text = wrap_korean(s["text"].replace("\n", " ").strip())
        rows.append(f"Dialogue: 0,{ass_ts(start)},{ass_ts(end)},Default,,0,0,0,,{text}")
    path.write_text(head + "\n".join(rows) + "\n", encoding="utf-8")


# ----------------------------------------------------------------- clips ---
PLACEHOLDER_REASON = "왜 이 구간인가 — 근거를 문장으로"

CLIPS_TEMPLATE = [{
    "id": "clip-01",
    "start": "00:00:00",
    "end": "00:00:45",
    "title": "",
    "hook": "",
    "description": "",
    "reason": PLACEHOLDER_REASON,
    "has_worship_music": False,
    "congregation_visible": False,
    "crop": "center",
}]


def cmd_clips(args):
    d = need(args.idea_id)
    tj = d / "transcript.json"
    if not tj.exists():
        die("no transcript.json — run `transcribe` first")
    segs = json.loads(tj.read_text(encoding="utf-8"))["segments"]

    clips_path = d / "clips.json"
    if not clips_path.exists():
        clips_path.write_text(json.dumps(CLIPS_TEMPLATE, ensure_ascii=False, indent=2),
                              encoding="utf-8")
        print(f"==> wrote template {clips_path.relative_to(REPO)}")

    # Group segments into readable blocks so a person can actually scan it.
    print(f"\n=== transcript: {args.idea_id} "
          f"({len(segs)} segments, {hhmmss(segs[-1]['end']) if segs else '0'}) ===\n")
    block, block_start = [], segs[0]["start"] if segs else 0.0
    for s in segs:
        block.append(s["text"])
        if s["end"] - block_start >= args.window:
            print(f"[{hhmmss(block_start)}] {' '.join(block)}")
            block, block_start = [], s["end"]
    if block:
        print(f"[{hhmmss(block_start)}] {' '.join(block)}")

    print(f"\n=== now edit {clips_path.relative_to(REPO)} ===")
    print("clip 3개, 각 30~90초. reason 필드에 왜 그 구간인지 반드시 적을 것.")
    validate_clips(clips_path, segs, strict=False)


def validate_clips(path: Path, segs: list[dict], strict: bool = True) -> list[dict]:
    clips = json.loads(path.read_text(encoding="utf-8"))
    total = segs[-1]["end"] if segs else 0.0
    problems, flags = [], []

    for c in clips:
        cid = c.get("id", "?")
        start, end = parse_time(c["start"]), parse_time(c["end"])
        dur = end - start
        if dur <= 0:
            problems.append(f"{cid}: end is not after start")
        elif not 15 <= dur <= 180:
            problems.append(f"{cid}: {dur:.0f}s is outside 15–180s")
        if total and end > total + 1:
            problems.append(f"{cid}: ends at {hhmmss(end)}, past the source ({hhmmss(total)})")
        if strict:
            # An untouched template must not render. Its placeholder reason is
            # non-empty, so an "is it blank" check alone would wave it through.
            reason = c.get("reason", "").strip()
            if not reason or reason == PLACEHOLDER_REASON:
                problems.append(f"{cid}: reason is still the template placeholder — "
                                "write why this segment was chosen")
            for field in ("title", "hook"):
                if not c.get(field, "").strip():
                    problems.append(f"{cid}: {field} is empty")
        if c.get("has_worship_music"):
            flags.append(f"{cid}: 찬양 음원 포함 — Content ID 위험. 배포 전 개별 확인 필요")
        if c.get("congregation_visible"):
            flags.append(f"{cid}: 회중석 노출 — 크롭 확인 또는 동의 필요")

    for f in flags:
        print(f"  [FLAG] {f}")
    if problems:
        msg = "clips.json problems:\n" + "\n".join(f"  - {p}" for p in problems)
        if strict:
            die(msg)
        print(msg)
    return clips


# ---------------------------------------------------------------- render ---
def crop_filter(mode: str) -> str:
    """16:9 → 9:16. `center` is the safe default; `left`/`right` shift the
    window when the pastor stands off-centre."""
    x = {"center": "(iw-ow)/2", "left": "0", "right": "iw-ow"}.get(mode, "(iw-ow)/2")
    return f"crop=w=ih*9/16:h=ih:x={x}:y=0,scale={OUT_W}:{OUT_H}"


def cmd_render(args):
    d = need(args.idea_id)
    video = find_source(d)
    segs = json.loads((d / "transcript.json").read_text(encoding="utf-8"))["segments"]
    clips = validate_clips(d / "clips.json", segs, strict=True)

    out_dir = d / "renders"
    out_dir.mkdir(exist_ok=True)
    sub_dir = out_dir / "subs"
    sub_dir.mkdir(exist_ok=True)

    made = []
    for c in clips:
        cid = c["id"]
        if args.only and cid != args.only:
            continue
        start, end = parse_time(c["start"]), parse_time(c["end"])

        # Subtitles for just this window, clamped to the cut and retimed so the
        # clip starts at zero.
        window = [
            {"start": max(s["start"], start), "end": min(s["end"], end), "text": s["text"]}
            for s in segs if s["end"] > start and s["start"] < end
        ]
        ass = sub_dir / f"{cid}.ass"
        write_ass(window, ass, offset=start)
        write_srt(window, sub_dir / f"{cid}.srt", offset=start)  # for YouTube upload

        out = out_dir / f"{cid}.mp4"
        vf = (
            f"{crop_filter(c.get('crop', 'center'))},"
            f"subtitles={ass.as_posix()}:fontsdir={FONT_DIR}"
        )
        print(f"==> {cid}  {hhmmss(start)}–{hhmmss(end)}  ({end-start:.0f}s)")
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{start}", "-to", f"{end}", "-i", str(video),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(out),
        ])
        made.append((cid, out, c))

    # Human-facing package. Renders are gitignored; this file is the record.
    pkg = ["# 발행 패키지 — " + args.idea_id, "",
           "**업로드는 사람이 한다. 이 파일은 승인용 초안이다.**", ""]
    for cid, out, c in made:
        pkg += [
            f"## {cid}",
            f"- 파일: `renders/{out.name}` (gitignored)",
            f"- 구간: {c['start']} – {c['end']}",
            f"- 제목: {c.get('title','')}",
            f"- 후킹: {c.get('hook','')}",
            f"- 설명: {c.get('description','')}",
            f"- 선정 근거: {c.get('reason','')}",
        ]
        if c.get("has_worship_music"):
            pkg.append("- ⚠️ 찬양 음원 포함 — Content ID 확인 전 업로드 금지")
        if c.get("congregation_visible"):
            pkg.append("- ⚠️ 회중석 노출 — 크롭/동의 확인 필요")
        pkg.append("")
    (d / "publish-package.md").write_text("\n".join(pkg), encoding="utf-8")

    print(f"\n==> {len(made)} clip(s) in {out_dir.relative_to(REPO)}")
    print(f"==> 승인용 패키지: {(d / 'publish-package.md').relative_to(REPO)}")
    print("==> 업로드하지 않았다. 사람이 확인하고 직접 올린다.")


# ---------------------------------------------------------------- doctor ---
def cmd_doctor(_args):
    print("=== Tier 0 toolchain ===")
    for tool in ("ffmpeg", "yt-dlp", "whisper-cli", "npx"):
        p = shutil.which(tool)
        print(f"  {'OK  ' if p else 'MISS'}  {tool:<12} {p or '— not installed'}")

    fonts = list(Path(FONT_DIR).glob("NotoSansKR-*.ttf")) if Path(FONT_DIR).exists() else []
    print(f"  {'OK  ' if fonts else 'MISS'}  {'korean font':<12} "
          f"{len(fonts)} file(s) in {FONT_DIR}")

    model = os.environ.get("WHISPER_MODEL", "models/ggml-large-v3.bin")
    print(f"  {'OK  ' if Path(model).exists() else 'MISS'}  {'whisper model':<12} {model}")

    print(f"  {'OK  ' if os.environ.get('GEMINI_API_KEY') else 'MISS'}  "
          f"{'GEMINI_API_KEY':<12} (fallback transcription backend)")
    print("\nMissing render tools → bash scripts/setup_render_env.sh")
    print("Blocked downloads     → docs/environment-constraints.md")


# ------------------------------------------------------------------ main ---
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch"); f.add_argument("idea_id"); f.add_argument("--url", required=True)
    f.set_defaults(func=cmd_fetch)

    t = sub.add_parser("transcribe"); t.add_argument("idea_id")
    t.add_argument("--backend", choices=["auto", "whisper", "gemini"], default="auto")
    t.set_defaults(func=cmd_transcribe)

    c = sub.add_parser("clips"); c.add_argument("idea_id")
    c.add_argument("--window", type=float, default=12.0, help="seconds per printed block")
    c.set_defaults(func=cmd_clips)

    r = sub.add_parser("render"); r.add_argument("idea_id")
    r.add_argument("--only", help="render just this clip id")
    r.set_defaults(func=cmd_render)

    sub.add_parser("doctor").set_defaults(func=cmd_doctor)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
