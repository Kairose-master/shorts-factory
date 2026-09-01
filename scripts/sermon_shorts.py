#!/usr/bin/env python3
"""Tier 0 sermon-to-Shorts pipeline — 방배동 예심교회.

Four stages, each runnable on its own so a failure never costs you the
stages that already succeeded:

  fetch       yt-dlp the sermon into office/production/<id>/source/
  transcribe  find the sermon inside the service, then transcribe just that
  clips       print the transcript for reading, then validate clips.json
  render      cut → 9:16 crop → Korean subtitle burn-in → MP4

A Sunday recording is the whole service, not a sermon: 60-85 minutes of which
the sermon is well under half, the rest worship, prayer, offering and notices.
`transcribe` therefore locates the sermon first and works only inside it —
cheaper, and it keeps every later stage away from the worship music, which is
where Content ID lives.

Clip selection is deliberately NOT automated. Stage `clips` prints a
timecoded transcript and stops; a human (or Claude) reads it and writes
clips.json with a stated reason per clip. A keyword heuristic cannot tell
the difference between a pastor's throwaway aside and the line the whole
sermon turns on, and guessing badly here is worse than not guessing.

Nothing in this file uploads anything. Rendering is the last step; publishing
is a human decision, every time.

Usage:
  python3 scripts/sermon_shorts.py sermons    [--pick]
  python3 scripts/sermon_shorts.py fetch      SUN-2026-08-30 --url <youtube-url>
  python3 scripts/sermon_shorts.py transcribe SUN-2026-08-30 [--backend auto] [--whole]
  python3 scripts/sermon_shorts.py clips      SUN-2026-08-30 [--window 12]
  python3 scripts/sermon_shorts.py render     SUN-2026-08-30 [--only clip-01]
  python3 scripts/sermon_shorts.py doctor
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROD = REPO / "office" / "production"
# Fonts ship with the repo rather than the system, so a render looks the same
# on every machine and needs no admin rights to set up. A system path still
# works if FONT_DIR is set.
FONT_DIR = os.environ.get("FONT_DIR", str(REPO / "assets" / "fonts"))
FONT_NAME = "Noto Sans KR"

# 9:16 at the resolution YouTube Shorts actually wants.
OUT_W, OUT_H = 1080, 1920

# Sermon delivery is slower than short-form pacing tolerates. 1.5x keeps the
# preacher's voice natural while cutting dead air; per-clip `speed` overrides.
DEFAULT_SPEED = 1.5

# ASS colours are &HAABBGGRR — byte-reversed from hex RGB, so yellow #FFFF00
# is written 00FFFF. Captions sit over the pulpit, which is white and brightly
# lit; white text washed out against it even with an outline. Yellow separates
# from both the pulpit and the dark green backdrop.
SUBTITLE_COLOUR = "&H0000FFFF"   # #FFFF00

# The Shorts player draws its own furniture over the bottom of the frame —
# channel handle, title, description, progress bar — so the bottom of a
# 1920-tall video is not ours to use. Captions are lifted clear of it.
SUBTITLE_MARGIN_V = 480

# Usable caption width is 1080 minus the side margins; at 64px a Korean glyph
# is about as wide as it is tall, so ~14 fit. Lines longer than this get wrapped
# again by libass, which quietly doubles the line count.
SUB_PER_LINE = 14


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
APIFY_ACTOR = "epctex~youtube-video-downloader"


def fetch_via_apify(url: str, dest: Path, quality: str = "480") -> Path:
    """Download the service through an Apify actor instead of locally.

    Only needed where yt-dlp cannot reach YouTube's media servers. In this
    hosted container it cannot: YouTube signs each media URL to the IP that
    asked for the metadata, and the request then egresses from a different
    proxy address, so the download 403s no matter which client yt-dlp
    pretends to be. The actor runs on Apify's own machines and hands back a
    file, which sidesteps the whole problem.

    It costs real money, per second of footage — see docs/porting-to-your-claude.md.
    On a normal machine use the default yt-dlp path and pay nothing.
    """
    import time
    import urllib.request

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        raise RuntimeError("APIFY_TOKEN not set")
    api = "https://api.apify.com/v2"
    hdr = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    body = json.dumps({"startUrls": [url], "quality": quality,
                       "storageType": "apify"}).encode()
    req = urllib.request.Request(f"{api}/acts/{APIFY_ACTOR}/runs", data=body,
                                 headers=hdr, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        run_info = json.load(r)["data"]
    run_id, dataset = run_info["id"], run_info["defaultDatasetId"]
    print(f"  apify run {run_id} — quality {quality}")

    while True:
        with urllib.request.urlopen(
                urllib.request.Request(f"{api}/actor-runs/{run_id}", headers=hdr),
                timeout=60) as r:
            status = json.load(r)["data"]["status"]
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        time.sleep(20)
    if status != "SUCCEEDED":
        raise RuntimeError(f"apify run {status}")

    with urllib.request.urlopen(
            urllib.request.Request(f"{api}/datasets/{dataset}/items", headers=hdr),
            timeout=60) as r:
        items = json.load(r)
    if not items or items[0].get("error"):
        raise RuntimeError(f"apify returned no file: {items[:1]}")
    item = items[0]
    print(f"  {item.get('durationSeconds')}s, charged ${item.get('totalCost')}")

    with urllib.request.urlopen(
            urllib.request.Request(item["output"]["url"], headers=hdr), timeout=1800) as r, \
            dest.open("wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def cmd_fetch(args):
    d = idea_dir(args.idea_id)
    src = d / "source"
    src.mkdir(parents=True, exist_ok=True)

    if args.via == "apify":
        print(f"==> fetching {args.url} via Apify (paid)")
        try:
            fetch_via_apify(args.url, src / "sermon.mp4", args.quality)
        except Exception as e:  # noqa: BLE001 — a paid step failing deserves a plain answer
            die(f"Apify fetch failed: {e}\n"
                "  APIFY_TOKEN is set in the environment, not in a file — see\n"
                "  docs/porting-to-your-claude.md. On a machine where yt-dlp can\n"
                "  reach YouTube, drop --via apify and pay nothing.")
        (d / "meta.json").write_text(
            json.dumps({"idea_id": args.idea_id, "source_url": args.url,
                        "fetched_via": "apify", "quality": args.quality},
                       ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"==> source in {src.relative_to(REPO)}")
        return

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


# Model ids move; the first that answers wins. A 503 here means the model is
# busy, not that the audio is bad, so the caller retries down this list.
GEMINI_MODELS = ["gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-2.5-pro"]

CHUNK_SECONDS = 540      # ~9 min per call
CHUNK_OVERLAP = 30       # trailing seconds re-sent with the next chunk


def _gemini_call(client, types, path: Path, prompt: str, max_tokens: int = 32000):
    """One generate_content, walking GEMINI_MODELS on overload."""
    import time
    f = client.files.upload(file=str(path))
    while f.state.name == "PROCESSING":
        time.sleep(4)
        f = client.files.get(name=f.name)
    last = None
    for attempt in range(len(GEMINI_MODELS) * 3):
        model = GEMINI_MODELS[min(attempt // 3, len(GEMINI_MODELS) - 1)]
        try:
            return client.models.generate_content(
                model=model, contents=[f, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", max_output_tokens=max_tokens))
        except Exception as e:  # noqa: BLE001 — overload is transient; try the next model
            last = e
            print(f"    {model}: {str(e)[:80]}")
            time.sleep(15)
    raise RuntimeError(f"every Gemini model failed: {last}")


def _gemini_client():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise RuntimeError("pip3 install google-genai")
    return genai.Client(api_key=key), types


TRANSCRIBE_PROMPT = (
    "한국 개신교 설교 오디오다. 들리는 그대로 한국어로 전사하라.\n"
    "- 요약하거나 문장을 다듬지 말 것. 실제 발화를 그대로 옮긴다.\n"
    "- 성경 인용, 예화, 반복 어구도 빠짐없이 옮긴다.\n"
    "- 한 원소는 한 문장 또는 8초 이내로 끊는다.\n"
    '- JSON 배열만 출력. 각 원소는 {"start": 초(float), "end": 초(float), "text": "발화"}\n'
    "  시간은 이 오디오 조각의 시작을 0으로 한 상대시간이다.\n"
    "- 설명 문장을 쓰지 말 것."
)


def transcribe_gemini(wav: Path, start: float = 0.0, end: float | None = None) -> list[dict]:
    """Gemini transcription, in overlapping chunks.

    A full service is over an hour, and one call for the whole thing gets
    truncated well before the end. Chunking fixes that but drops audio at
    every seam — the model reliably loses the last seconds of a clip — so
    each chunk re-sends CHUNK_OVERLAP seconds of the previous one and the
    duplicate segments are dropped on the way out.

    Paid: one call per chunk.
    """
    client, types = _gemini_client()
    total = (end if end is not None else probe_duration(wav)) - start
    n = max(1, int(total // (CHUNK_SECONDS - CHUNK_OVERLAP)) + 1)
    print(f"  {total/60:.0f}분 → {n} chunk(s), {n} paid call(s)")

    out: list[dict] = []
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(n):
            off = start + i * (CHUNK_SECONDS - CHUNK_OVERLAP)
            if off >= start + total:
                break
            piece = Path(tmp) / f"c{i}.mp3"
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-ss", f"{off}", "-t", f"{CHUNK_SECONDS}", "-i", str(wav),
                 "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", "48k",
                 str(piece)])
            resp = _gemini_call(client, types, piece, TRANSCRIBE_PROMPT)
            for s in json.loads(resp.text):
                seg = {"start": float(s["start"]) + off, "end": float(s["end"]) + off,
                       "text": str(s["text"]).strip()}
                # Overlap means the same words arrive twice; keep the first copy.
                if out and seg["start"] < out[-1]["end"] - 1.0:
                    continue
                out.append(seg)
            print(f"    chunk {i+1}/{n} ok ({len(out)} segments so far)")
    out.sort(key=lambda s: s["start"])
    return out


# Korean speech runs roughly 4-5 characters a second. A segment claiming far
# more time than its text needs means the model skipped audio inside it.
CHARS_PER_SECOND = 4.0
HOLE_SLACK = 8.0          # seconds of pause allowed before it counts as a hole
MIN_HOLE = 10.0           # don't bother re-transcribing anything shorter


def _norm(text: str) -> str:
    return "".join(text.split())


def dedupe_segments(segs: list[dict]) -> list[dict]:
    """Drop text the model transcribed twice at a chunk seam.

    The chunks overlap on purpose, so the seam audio is sent twice. Comparing
    timestamps is not enough to catch the repeat: the model's timings drift
    near the end of a chunk, and the second copy can start after the first
    copy's stated end, which makes the duplicate look like new material.
    Comparing the words themselves does catch it.
    """
    out: list[dict] = []
    for s in segs:
        key = _norm(s["text"])
        if not key:
            continue
        # Only look back over the seam-sized window, so a genuinely repeated
        # phrase far later in the sermon is left alone.
        if any(_norm(p["text"]) == key for p in out if s["start"] - p["start"] < 90):
            continue
        out.append(s)
    return out


def find_holes(segs: list[dict], window: tuple[float, float] | None = None) -> list[tuple[float, float]]:
    """Stretches of the sermon with no transcript against them.

    Two shapes: an outright gap between consecutive segments, and a segment
    whose stated duration is far longer than its own text could fill — the
    model quietly swallowed audio inside it and stretched the end timestamp
    to cover the loss.
    """
    holes = []
    for i, s in enumerate(segs):
        spoken = len(_norm(s["text"])) / CHARS_PER_SECOND
        if (s["end"] - s["start"]) - spoken > HOLE_SLACK:
            holes.append((s["start"] + spoken, s["end"]))
        if i + 1 < len(segs):
            gap = segs[i + 1]["start"] - s["end"]
            if gap > HOLE_SLACK:
                holes.append((s["end"], segs[i + 1]["start"]))
    if window:
        holes = [(max(a, window[0]), min(b, window[1])) for a, b in holes]
    return [(a, b) for a, b in holes if b - a >= MIN_HOLE]


def repair_transcript(wav: Path, segs: list[dict],
                      window: tuple[float, float] | None = None,
                      fill_holes: bool = False) -> list[dict]:
    """Clean a transcript: drop seam duplicates, clamp impossible durations.

    Hole-filling is off by default and rarely what you want. An over-long
    segment usually means the model's timestamps have drifted late rather
    than that it skipped audio — re-transcribing the "hole" then returns the
    same words a second time under different timings, which is worse than
    the gap. Measured on SUN-2026-04-26: what the transcript placed at 62:50
    is actually spoken at 62:22.
    """
    segs = dedupe_segments(sorted(segs, key=lambda s: s["start"]))
    # A cue must never outlive the next one, nor sit far longer than its own
    # words could fill — either way it would hang on screen over later speech.
    for i, s in enumerate(segs):
        cap = s["start"] + len(_norm(s["text"])) / CHARS_PER_SECOND + HOLE_SLACK
        s["end"] = min(s["end"], cap)
        if i + 1 < len(segs):
            s["end"] = min(s["end"], segs[i + 1]["start"])
    if not fill_holes:
        return segs

    holes = find_holes(segs, window)
    if not holes:
        return segs

    print(f"  전사 누락 {len(holes)}곳 재전사 ({len(holes)} paid call(s))")
    client, types = _gemini_client()
    with tempfile.TemporaryDirectory() as tmp:
        for a, b in holes:
            print(f"    {hhmmss(a)}–{hhmmss(b)} ({b-a:.0f}s)")
            piece = Path(tmp) / f"h{int(a)}.mp3"
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-ss", f"{a}", "-t", f"{b - a}", "-i", str(wav),
                 "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", "48k",
                 str(piece)])
            try:
                resp = _gemini_call(client, types, piece, TRANSCRIBE_PROMPT)
                for s in json.loads(resp.text):
                    segs.append({"start": float(s["start"]) + a,
                                 "end": float(s["end"]) + a,
                                 "text": str(s["text"]).strip()})
            except Exception as e:  # noqa: BLE001 — a hole we cannot fill is still worth reporting
                print(f"      재전사 실패: {str(e)[:70]}")

    segs = dedupe_segments(sorted(segs, key=lambda s: s["start"]))
    # Never let a cue outlive the next one starting.
    for i in range(len(segs) - 1):
        segs[i]["end"] = min(segs[i]["end"], segs[i + 1]["start"])
    return segs


def retime_window(wav: Path, start: float, end: float) -> list[dict]:
    """Re-transcribe one clip's window for accurate caption timings.

    The pass that produces the reading transcript works in nine-minute chunks,
    and the model's timestamps drift late across a chunk — measured at four to
    five seconds by the middle of one. That is invisible while reading the
    transcript and very visible once the words are burned under the picture.
    A short window re-transcribed on its own has almost nothing to drift over.

    One paid Gemini call per clip.
    """
    with tempfile.TemporaryDirectory() as tmp:
        piece = Path(tmp) / "w.mp3"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-ss", f"{start}", "-t", f"{end - start}", "-i", str(wav),
             "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", "48k", str(piece)])
        client, types = _gemini_client()
        resp = _gemini_call(client, types, piece, TRANSCRIBE_PROMPT)
    segs = [{"start": float(s["start"]) + start, "end": float(s["end"]) + start,
             "text": str(s["text"]).strip()} for s in json.loads(resp.text)]
    segs.sort(key=lambda s: s["start"])
    for i in range(len(segs) - 1):
        segs[i]["end"] = min(segs[i]["end"], segs[i + 1]["start"])
    return [s for s in segs if s["text"]]


def probe_duration(media: Path) -> float:
    """Duration in seconds. ffprobe is not in the static ffmpeg build here, so
    this parses ffmpeg's own banner instead of assuming ffprobe exists."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(media)],
                       capture_output=True, text=True)
    for line in p.stderr.splitlines():
        if "Duration:" in line:
            hh, mm, ss = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(hh) * 3600 + int(mm) * 60 + float(ss)
    raise RuntimeError(f"could not read duration of {media}")


SERMON_WINDOW_PROMPT = """이것은 한국 개신교 교회의 주일예배 실황 녹음 전체다.
예배 순서를 시간대별로 구분하라. 특히 다음을 정확히 찾아라:

1. 찬양/찬송이 나오는 모든 구간 (반주만 있는 구간 포함)
2. 대표기도, 봉헌, 광고 구간
3. **설교(말씀)가 시작되는 시점과 끝나는 시점** — 가장 중요하다.
   설교는 보통 성경 본문 봉독 직후 시작해 마침기도 직전에 끝난다.

JSON 배열만 출력. 각 원소는
{"start": 초(정수), "end": 초(정수), "type": "찬양|기도|봉헌|광고|성경봉독|설교|축도|기타", "note": "간단한 근거"}
설명 문장 쓰지 말 것."""


def detect_service_structure(audio: Path) -> list[dict]:
    """Split a full service recording into its parts. One paid Gemini call.

    Worth it before transcribing: a Sunday service runs 60-85 minutes and the
    sermon is well under half of that. Transcribing only the sermon is both
    cheaper and safer — every clip then starts life inside the sermon rather
    than somewhere in the worship set, where Content ID lives.
    """
    client, types = _gemini_client()
    resp = _gemini_call(client, types, audio, SERMON_WINDOW_PROMPT, max_tokens=8000)
    return json.loads(resp.text)


def cmd_transcribe(args):
    d = need(args.idea_id)
    video = find_source(d)
    wav = extract_audio(video, d / "source" / "audio16k.wav")
    print(f"==> audio: {wav.relative_to(REPO)}")

    # Find the sermon inside the service before transcribing any of it.
    window = None
    sp = d / "service-structure.json"
    if not args.whole and not args.no_structure:
        if sp.exists():
            structure = json.loads(sp.read_text(encoding="utf-8"))
            print(f"==> reusing {sp.relative_to(REPO)}")
        else:
            print("==> detecting service structure (1 paid call)")
            structure = detect_service_structure(wav)
            sp.write_text(json.dumps(structure, ensure_ascii=False, indent=2),
                          encoding="utf-8")
        sermon = [s for s in structure if s.get("type") == "설교"]
        if sermon:
            window = (float(min(s["start"] for s in sermon)),
                      float(max(s["end"] for s in sermon)))
            print(f"==> 설교 구간 {hhmmss(window[0])}–{hhmmss(window[1])} "
                  f"(전체 {hhmmss(probe_duration(wav))})")
            for s in structure:
                if s.get("type") == "찬양":
                    print(f"    [찬양] {hhmmss(s['start'])}–{hhmmss(s['end'])} — 클립 금지 구간")
        else:
            print("    설교 구간을 못 찾음 — 전체를 전사한다")

    model = os.environ.get("WHISPER_MODEL", "models/ggml-large-v3.bin")
    backends = [args.backend] if args.backend != "auto" else ["whisper", "gemini"]
    start, end = window if window else (0.0, None)

    segs, used, errs = None, None, []
    for b in backends:
        try:
            print(f"==> transcribing via {b}")
            segs = (transcribe_whisper(wav, model) if b == "whisper"
                    else transcribe_gemini(wav, start, end))
            used = b
            break
        except Exception as e:  # noqa: BLE001 — report and try the next backend
            errs.append(f"  {b}: {e}")
            print(f"    {b} unavailable: {e}")

    if segs is None:
        die("no transcription backend worked:\n" + "\n".join(errs))

    if used == "gemini" and not args.no_repair:
        print("==> 중복·누락 점검")
        before = len(segs)
        segs = repair_transcript(wav, segs, window)
        print(f"    {before} → {len(segs)} segments")

    out = {"backend": used, "language": "ko", "segments": segs}
    if window:
        out["sermon_window"] = {"start": window[0], "end": window[1]}
    (d / "transcript.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
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


def wrap_lines(text: str, per_line: int) -> list[str]:
    """Break on word boundaries into short lines.

    Korean has spaces between 어절, so wrapping on them is safe and reads far
    better than libass's own greedy fill at this font size. Never drops text —
    the caller decides what to do with more lines than it wants.
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
    return lines


def wrap_korean(text: str, per_line: int = SUB_PER_LINE, max_lines: int = 3) -> str:
    """Wrap to at most `max_lines`, keeping every word.

    `max_lines` is a layout hint, not a budget to spend text against: if the
    text needs more lines it gets them. Silently dropping the tail of a
    sentence is the worst possible failure here — it was cutting the payoff
    off the end of the preacher's own sentences.
    """
    return "\\N".join(wrap_lines(text, per_line))


def split_for_display(seg: dict, per_line: int = SUB_PER_LINE,
                      max_lines: int = 3) -> list[dict]:
    """One transcript segment → one or more subtitle cues.

    A segment can be eight seconds of speech, far more than fits on screen at
    a readable size. Rather than truncate it, split it into consecutive cues
    and share the segment's own duration between them in proportion to how
    much text each carries, so the words stay under the voice saying them.
    """
    lines = wrap_lines(seg["text"], per_line)
    if len(lines) <= max_lines:
        return [seg]

    groups = [lines[i:i + max_lines] for i in range(0, len(lines), max_lines)]
    weights = [sum(len(x) for x in g) for g in groups]
    total = sum(weights) or 1
    span = seg["end"] - seg["start"]

    out, t = [], seg["start"]
    for i, (g, w) in enumerate(zip(groups, weights)):
        end = seg["end"] if i == len(groups) - 1 else t + span * w / total
        out.append({"start": t, "end": end, "text": " ".join(g)})
        t = end
    return out


def write_ass(segs: list[dict], path: Path, offset: float = 0.0,
              font_size: int = 64, margin_v: int = SUBTITLE_MARGIN_V,
              title: str = "", duration: float = 0.0):
    """Burn-in subtitles as ASS, with an optional standing title card.

    SRT carries no resolution, so libass falls back to a 384x288 script and
    scales every style number up from there — a Fontsize/MarginV tuned in real
    pixels lands in the wrong place. ASS lets us state PlayRes explicitly, so
    the numbers below mean what they say at 1080x1920.

    The title sits at the top for the clip's whole length, not just the open:
    most viewers arrive mid-clip, and a sermon excerpt with no frame around it
    reads as a stranger talking. `duration` is the clip's length *before* any
    speed change, because the subtitle burn happens before the retime.
    """
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {OUT_W}
PlayResY: {OUT_H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{FONT_NAME},{font_size},{SUBTITLE_COLOUR},&H000000FF,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,5,2,2,70,70,{margin_v},1
Style: Title,{FONT_NAME},72,&H00FFFFFF,&H000000FF,&H00202020,&H00000000,1,0,0,0,100,100,0,0,1,6,0,8,60,60,110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    cues = []
    for s_ in segs:
        cues.extend(split_for_display(s_))

    rows = []
    if title and duration > 0:
        rows.append(f"Dialogue: 1,{ass_ts(0)},{ass_ts(duration)},Title,,0,0,0,,"
                    f"{wrap_korean(title, per_line=13, max_lines=3)}")
    for s in cues:
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


SELECT_PROMPT = """너는 한국 개신교 교회의 주일설교에서 유튜브 쇼츠로 쓸 구간을 고른다.

아래는 설교 전사본이다. 각 줄은 [초] 형식의 절대 시각과 발화다.

{transcript}

여기서 쇼츠 {count}편을 고른다. 규칙:

1. **반드시 {win_start}초 ~ {win_end}초 사이에서만 고른다.** 그 바깥은 찬양·기도·
   봉헌이라 저작권에 걸린다.
2. 각 구간은 **40~70초**. 배속이 걸려 실제로는 27~47초가 된다.
3. 한 구간은 **그 자체로 완결**되어야 한다. 문장 중간에서 시작하거나 끝나지 말 것.
4. **성경 지식이 없는 사람도 첫 문장부터 이해되는 대목**을 고른다. 인명·지명이
   많이 나오는 성경 서사 설명보다, 목사님이 일상 예화를 들거나 청중에게 직접
   말을 거는 대목이 낫다.
5. {count}편이 서로 **다른 각도**여야 한다. 같은 이야기를 잘라 붙이지 말 것.
6. 전사본에 시간 공백이 큰 곳(앞 줄의 끝과 다음 줄의 시작이 10초 이상 벌어진 곳)은
   자막이 비므로 그 구간을 걸치지 말 것.

각 편에 대해 쓴다:
- start, end: 초 단위 숫자 (전사본의 시각을 그대로 쓴다)
- title: 화면 상단과 유튜브 제목에 쓸 12자 내외의 문장. 그 구간의 말에서 뽑는다.
- hook: 그 구간에서 가장 강한 실제 발화 한 문장 (전사본에서 그대로 인용)
- reason: 왜 이 구간인가. 한두 문장으로 구체적으로. "좋아서"처럼 쓰지 말 것.

**JSON 배열만 출력한다. 설명 문장, 코드펜스, 그 외 아무것도 붙이지 말 것.**
형식: [{{"start": 3304.5, "end": 3354.0, "title": "...", "hook": "...", "reason": "..."}}]
"""


def _extract_json(text: str):
    """Pull the JSON array out of a model reply that may be wrapped in prose."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-z]*\n?|\n?```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\[.*\]", text, re.S)
        if not m:
            raise
        return json.loads(m.group(0))


def select_with_claude(prompt: str) -> list[dict]:
    """Ask the locally installed Claude Code to choose the clips.

    Uses the subscription already signed in on this machine, so it costs
    nothing extra and needs no API key. `-p` runs one query and exits.
    """
    exe = shutil.which("claude")
    if not exe:
        raise RuntimeError("claude CLI not found")
    p = subprocess.run([exe, "-p", prompt], capture_output=True, text=True, timeout=900)
    if p.returncode != 0:
        raise RuntimeError(f"claude -p failed: {p.stderr[:200]}")
    return _extract_json(p.stdout)


def select_with_gemini(prompt: str) -> list[dict]:
    """Fallback where the Claude CLI is not installed — the cloud container."""
    client, types = _gemini_client()
    for model in GEMINI_MODELS:
        try:
            r = client.models.generate_content(
                model=model, contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", max_output_tokens=8000))
            return _extract_json(r.text)
        except Exception as e:  # noqa: BLE001 — try the next model on overload
            print(f"    {model}: {str(e)[:70]}")
    raise RuntimeError("no Gemini model answered")


def cmd_select(args):
    """Choose the clips automatically instead of stopping for a person.

    The gate exists so that a *keyword heuristic* never picks the segments —
    it cannot tell a throwaway aside from the line a sermon turns on. A model
    that has read the whole transcript can, which is exactly what happens when
    a person asks Claude to do it by hand. This just removes the round trip.

    What stays enforced regardless of what the selector returns: clips must
    land inside the sermon window, run 15-180 seconds, and carry a reason.
    The copyright rule is structural, not a matter of the selector's judgement.
    """
    d = need(args.idea_id)
    data = json.loads((d / "transcript.json").read_text(encoding="utf-8"))
    segs = data["segments"]
    w = data.get("sermon_window")
    win = (w["start"], w["end"]) if w else (segs[0]["start"], segs[-1]["end"])

    lines = "\n".join(f"[{s['start']:.1f}] {s['text']}"
                      for s in segs if win[0] <= s["start"] <= win[1])
    prompt = SELECT_PROMPT.format(transcript=lines, count=args.count,
                                  win_start=int(win[0]), win_end=int(win[1]))

    backends = ([select_with_claude, select_with_gemini] if args.backend == "auto"
                else [select_with_claude] if args.backend == "claude"
                else [select_with_gemini])
    picked, errs = None, []
    for fn in backends:
        try:
            print(f"==> 구간 선별 — {fn.__name__}")
            picked = fn(prompt)
            break
        except Exception as e:  # noqa: BLE001 — report and try the next backend
            errs.append(f"  {fn.__name__}: {e}")
            print(f"    사용 불가: {str(e)[:90]}")
    if picked is None:
        die("구간 선별 실패:\n" + "\n".join(errs))

    crop = auto_crop(find_source(d))
    ec = d / "end-card.json"
    meta = json.loads(ec.read_text(encoding="utf-8")) if ec.exists() else {}
    desc_tail = (f"{meta.get('church','')} 주일예배 | {meta.get('scripture','')} | "
                 f"{meta.get('preacher','')}").strip(" |")

    clips = []
    for i, c in enumerate(picked[:args.count], 1):
        start, end = float(c["start"]), float(c["end"])
        # The selector proposes; the window is not negotiable.
        start, end = max(start, win[0]), min(end, win[1])
        if end - start < 15:
            print(f"    clip-{i:02d} 건너뜀 — 설교 구간으로 자르니 {end-start:.0f}초")
            continue
        clips.append({
            "id": f"clip-{len(clips)+1:02d}",
            "start": round(start, 1), "end": round(end, 1),
            "title": str(c.get("title", "")).strip(),
            "hook": str(c.get("hook", "")).strip(),
            "description": desc_tail,
            "reason": str(c.get("reason", "")).strip(),
            "has_worship_music": False,
            "congregation_visible": False,
            "crop": crop,
        })

    if not clips:
        die("설교 구간 안에서 쓸 만한 구간이 나오지 않았다")
    (d / "clips.json").write_text(json.dumps(clips, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
    print(f"==> {len(clips)}편 선별 → clips.json")
    for c in clips:
        print(f"    {c['id']}  {hhmmss(c['start'])}–{hhmmss(c['end'])}  {c['title']}")
    validate_clips(d / "clips.json", segs, strict=True)


def cmd_repair(args):
    """Run the duplicate/hole pass over a transcript that already exists."""
    d = need(args.idea_id)
    tj = d / "transcript.json"
    if not tj.exists():
        die("no transcript.json — run `transcribe` first")
    data = json.loads(tj.read_text(encoding="utf-8"))
    wav = extract_audio(find_source(d), d / "source" / "audio16k.wav")
    w = data.get("sermon_window")
    window = (w["start"], w["end"]) if w else None

    before = len(data["segments"])
    segs = repair_transcript(wav, data["segments"], window, fill_holes=args.fill_holes)
    data["segments"] = segs
    tj.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_srt(segs, d / "transcript.srt")
    print(f"==> {before} → {len(segs)} segments")


def cmd_validate(args):
    """Is clips.json ready to render? Exit 0 yes, 1 no. No side effects —
    weekly_run.sh uses this to decide whether a human still has to read the
    transcript, so it must not write anything."""
    d = need(args.idea_id)
    cj = d / "clips.json"
    if not cj.exists():
        print("clips.json not written yet")
        sys.exit(1)
    tj = d / "transcript.json"
    segs = json.loads(tj.read_text(encoding="utf-8"))["segments"] if tj.exists() else []
    clips = validate_clips(cj, segs, strict=True)  # exits 1 on any problem
    print(f"ok — {len(clips)} clip(s) ready to render")


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
END_CARD_SECONDS = 4.0
END_CARD_BG = "0x123A34"   # the sanctuary's stage green, so the cut reads as one piece


def _ass_escape(s: str) -> str:
    return s.replace("\\", "").replace("{", "(").replace("}", ")").strip()


def build_end_card(cfg: dict, out: Path, seconds: float = END_CARD_SECONDS) -> Path:
    """A card naming the service, so a viewer can go and find the full sermon.

    A short travels away from the channel that made it. Without this, an
    excerpt is an unattributed stranger talking; with it, the sermon is
    searchable by title and passage, which are exact and unique.
    """
    lines = [
        # (text, y, size, colour, bold)
        (cfg.get("date", ""),      560,  54, "&H00C8D8D4", 0),
        (cfg.get("scripture", ""), 690,  60, "&H0090E0C8", 1),
        (cfg.get("title", ""),     880,  78, "&H00FFFFFF", 1),
        (cfg.get("preacher", ""), 1180,  58, "&H00E8F0EE", 0),
        (cfg.get("church", ""),   1360,  68, "&H00FFFFFF", 1),
        (cfg.get("handle", ""),   1470,  48, "&H0098B0AC", 0),
    ]
    rows, styles = [], []
    for i, (text, y, size, colour, bold) in enumerate(lines):
        if not text:
            continue
        styles.append(
            f"Style: E{i},{FONT_NAME},{size},{colour},&H000000FF,&H00000000,&H00000000,"
            f"{bold},0,0,0,100,100,0,0,1,0,0,5,60,60,0,1")
        wrapped = wrap_korean(_ass_escape(text), per_line=14, max_lines=2)
        rows.append(f"Dialogue: 0,{ass_ts(0)},{ass_ts(seconds)},E{i},,0,0,0,,"
                    f"{{\\pos({OUT_W//2},{y})}}{wrapped}")

    ass = out.with_suffix(".ass")
    ass.write_text(
        f"[Script Info]\nScriptType: v4.00+\nPlayResX: {OUT_W}\nPlayResY: {OUT_H}\n"
        "WrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        + "\n".join(styles)
        + "\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, "
          "MarginV, Effect, Text\n" + "\n".join(rows) + "\n",
        encoding="utf-8")

    # Encoded to match the clip exactly, so the two concatenate without a re-encode.
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-f", "lavfi", "-i", f"color=c={END_CARD_BG}:s={OUT_W}x{OUT_H}:r=30:d={seconds}",
         "-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100:d={seconds}",
         "-vf", f"subtitles={ass.as_posix()}:fontsdir={FONT_DIR}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
         "-shortest", str(out)])
    return out


# This channel's stream has a fixed layout, measured on the 720p and 360p
# sources and identical in both once expressed as fractions of the frame:
#   - a graphic sidebar (passage, sermon title, logo) owns the right third
#   - a scripture caption band is burned across the top during readings
# Both are dead weight in a 9:16 crop — the sidebar pushes the preacher off
# centre, and the caption band gets sliced mid-word. Cutting them away also
# removes the empty air above his head, which frames him better on a phone.
LIVE_AREA_RIGHT = 0.634    # sidebar starts here (x=812 of 1280)
TOP_BAND = 0.243           # caption band height (y=175 of 720)


def auto_crop(video: Path) -> dict:
    """Work out the 9:16 window from the frame size, using this channel's layout."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video)],
                       capture_output=True, text=True)
    m = re.search(r"(\d{3,4})x(\d{3,4})", p.stderr)
    if not m:
        die(f"could not read frame size of {video}")
    w, h = int(m.group(1)), int(m.group(2))

    top = int(h * TOP_BAND)
    ch = h - top
    cw = int(ch * 9 / 16)
    live_centre = int(w * LIVE_AREA_RIGHT) // 2
    x = max(0, min(live_centre - cw // 2, w - cw))
    return {"x": x, "y": top, "h": ch}


def crop_filter(mode) -> str:
    """16:9 → 9:16.

    Three forms, increasingly specific:

    - `"center"` / `"left"` / `"right"` — full-height window, nudged sideways.
    - a number — the exact left edge in source pixels. A broadcast layout is
      rarely centred in the file: this church's stream parks a graphic sidebar
      over the right third, so `center` slices the preacher off.
    - `{"x":…, "y":…, "h":…}` — an explicit window. Needed when the stream
      burns a caption band across the top: a full-height crop clips that band
      mid-word, and cutting below it also drops the dead air above the
      preacher, which frames him far better for a phone.

    The window is always forced to 9:16 from its height, so only x/y/h are
    ever specified and the aspect can't be got wrong by hand.
    """
    if isinstance(mode, dict):
        h = int(mode["h"])
        return (f"crop=w={h}*9/16:h={h}:x={int(mode.get('x', 0))}:y={int(mode.get('y', 0))},"
                f"scale={OUT_W}:{OUT_H}")
    if isinstance(mode, (int, float)):
        x = str(int(mode))
    else:
        x = {"center": "(iw-ow)/2", "left": "0", "right": "iw-ow"}.get(mode, "(iw-ow)/2")
    return f"crop=w=ih*9/16:h=ih:x={x}:y=0,scale={OUT_W}:{OUT_H}"


def cmd_render(args):
    d = need(args.idea_id)
    video = find_source(d)
    segs = json.loads((d / "transcript.json").read_text(encoding="utf-8"))["segments"]
    clips = validate_clips(d / "clips.json", segs, strict=True)

    audio = extract_audio(video, d / "source" / "audio16k.wav") if args.retime else None

    out_dir = d / "renders"
    out_dir.mkdir(exist_ok=True)
    sub_dir = out_dir / "subs"
    sub_dir.mkdir(exist_ok=True)

    # Built once and appended to every clip — each short is discovered on its
    # own, so each one needs to say where it came from.
    end_card = None
    ec_path = d / "end-card.json"
    if ec_path.exists() and not args.no_end_card:
        cfg = json.loads(ec_path.read_text(encoding="utf-8"))
        end_card = build_end_card(cfg, out_dir / "_endcard.mp4")
        print(f"==> 엔드카드 {END_CARD_SECONDS:.0f}초 — {cfg.get('title','')}")

    made = []
    for c in clips:
        cid = c["id"]
        if args.only and cid != args.only:
            continue
        start, end = parse_time(c["start"]), parse_time(c["end"])

        # Subtitles for just this window, clamped to the cut and retimed so the
        # clip starts at zero.
        if args.retime:
            print(f"    {cid} 자막 재타이밍 (1 paid call)")
            src_segs = retime_window(audio, start, end)
        else:
            src_segs = segs
        window = [
            {"start": max(s["start"], start), "end": min(s["end"], end), "text": s["text"]}
            for s in src_segs if s["end"] > start and s["start"] < end
        ]
        speed = float(c.get("speed", DEFAULT_SPEED))
        if not 0.5 <= speed <= 2.0:
            die(f"{cid}: speed {speed} is outside atempo's 0.5–2.0 range")

        ass = sub_dir / f"{cid}.ass"
        write_ass(window, ass, offset=start,
                  title=c.get("title", "") if c.get("show_title", True) else "",
                  duration=end - start)
        write_srt(window, sub_dir / f"{cid}.srt", offset=start)  # for YouTube upload

        out = out_dir / f"{cid}.mp4"
        # Subtitles and title are burned at the original timing, then the whole
        # picture is retimed. Doing it this way keeps captions in sync for free:
        # each frame already carries its text, and setpts only moves the frame.
        vf = (
            f"{crop_filter(c.get('crop', 'center'))},"
            f"subtitles={ass.as_posix()}:fontsdir={FONT_DIR}"
        )
        af = None
        if speed != 1.0:
            vf += f",setpts=PTS/{speed}"
            af = f"atempo={speed}"

        dur = (end - start) / speed
        print(f"==> {cid}  {hhmmss(start)}–{hhmmss(end)}  "
              f"({end-start:.0f}s → {dur:.0f}s @ {speed}x)")
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{start}", "-to", f"{end}", "-i", str(video),
            "-vf", vf,
        ]
        if af:
            cmd += ["-af", af]
        body = out if end_card is None else out.with_name(f"{cid}.body.mp4")
        cmd += [
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-movflags", "+faststart",
            str(body),
        ]
        run(cmd)

        if end_card is not None:
            lst = out_dir / f"{cid}.concat.txt"
            lst.write_text(f"file '{body.resolve()}'\nfile '{end_card.resolve()}'\n",
                           encoding="utf-8")
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-f", "concat", "-safe", "0", "-i", str(lst),
                 "-c", "copy", "-movflags", "+faststart", str(out)])
            lst.unlink()
            body.unlink()

        made.append((cid, out, c))

    # Human-facing package. Renders are gitignored; this file is the record.
    # It is written from every clip in clips.json, not just the ones rendered
    # this run — a `--only` re-render used to leave a package listing one clip
    # and silently drop the rest of the approval notes.
    rendered = {cid for cid, _, _ in made}
    pkg = ["# 발행 패키지 — " + args.idea_id, "",
           "**업로드는 사람이 한다. 이 파일은 승인용 초안이다.**", ""]
    for c in clips:
        cid = c["id"]
        out = out_dir / f"{cid}.mp4"
        if cid not in rendered and not out.exists():
            continue
        pkg += [
            f"## {cid}",
            f"- 파일: `renders/{out.name}` (gitignored)",
            f"- 구간: {c['start']} – {c['end']}"
            + (f"  ({float(c.get('speed', DEFAULT_SPEED))}배속)"
               if float(c.get("speed", DEFAULT_SPEED)) != 1.0 else ""),
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

    has_whisper = bool(shutil.which("whisper-cli")) and Path(model).exists()
    has_gemini = bool(os.environ.get("GEMINI_API_KEY"))
    # Gemini is only the fallback. With whisper present its absence is not a
    # problem, and reporting it as MISS reads like a broken setup.
    if has_gemini:
        print(f"  OK    {'GEMINI_API_KEY':<12} (fallback / cloud transcription)")
    elif has_whisper:
        print(f"  n/a   {'GEMINI_API_KEY':<12} not needed — whisper handles transcription")
    else:
        print(f"  MISS  {'GEMINI_API_KEY':<12} needed: no whisper, so nothing can transcribe")

    print()
    if has_whisper:
        print("전사: whisper large-v3 (무료·오프라인). 준비 완료.")
    elif has_gemini:
        print("전사: Gemini (유료). whisper를 깔면 무료로 바뀐다 —")
        print("      bash scripts/setup_render_env.sh --with-whisper")
    else:
        print("전사 수단이 없다 → bash scripts/setup_render_env.sh --with-whisper")
    print("Missing render tools → bash scripts/setup_render_env.sh")


# ---------------------------------------------------------------- sermons ---
# The Sunday services live in the streams tab, not the videos tab — the videos
# tab is Wednesday services by other pastors, daily 새벽기도 and the children's
# ministry. See .claude/context/youtube-channel.md.
CHANNEL_STREAMS = os.environ.get(
    "SERMON_CHANNEL", "https://www.youtube.com/@yeshim1126/streams")
SERMON_PREACHER = os.environ.get("SERMON_PREACHER", "장선기")

# Titles date themselves inconsistently: 2026-08-30, 2025-9-28, 2025.8.31.
TITLE_DATE = re.compile(r"(20\d{2})\s*[.\-/]\s*(\d{1,2})\s*[.\-/]\s*(\d{1,2})")
TITLE_SCRIPTURE = re.compile(r"\[([^\]]+)\]")


def list_sermons(preacher: str = SERMON_PREACHER) -> list[dict]:
    """Every Sunday service on the channel, newest first. Metadata only —
    yt-dlp's flat listing costs nothing and downloads nothing."""
    import datetime as _dt

    if not shutil.which("yt-dlp"):
        die("yt-dlp not installed — run: bash scripts/setup_render_env.sh")
    p = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "%(id)s\t%(title)s\t%(duration)s",
         CHANNEL_STREAMS],
        capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip():
        die("could not list the channel.\n"
            f"  {p.stderr.strip().splitlines()[-1] if p.stderr.strip() else 'no output'}\n"
            "  If this mentions 403 or a tunnel, YouTube is blocked by this\n"
            "  environment's egress policy — see docs/environment-constraints.md.")

    out = []
    for line in p.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        vid, title = parts[0], parts[1]
        dur = int(float(parts[2])) if len(parts) > 2 and parts[2] not in ("NA", "") else 0
        m = TITLE_DATE.search(title)
        if not m:                       # concerts, specials — no service date
            continue
        if preacher and preacher not in title:
            continue
        y, mo, dd = (int(x) for x in m.groups())
        try:
            d = _dt.date(y, mo, dd)
        except ValueError:
            continue
        # The channel has mistyped a date before (2026-07-14 was a Tuesday; the
        # service was the 12th). Trust the weekday, not the typist: snap back to
        # the Sunday on or before it, and say so.
        sunday = d - _dt.timedelta(days=(d.weekday() + 1) % 7)
        sm = TITLE_SCRIPTURE.search(title)
        out.append({
            "id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "title": title,
            "title_date": d.isoformat(),
            "date": sunday.isoformat(),
            "date_suspect": sunday != d,
            "idea_id": f"SUN-{sunday.isoformat()}",
            "duration": dur,
            "scripture": sm.group(1).strip() if sm else "",
        })
    return out


def already_produced() -> set[str]:
    """Video ids that some production folder already refers to — meta.json for
    a scripted fetch, qc.md or plan.md for the ones cut by hand."""
    seen: set[str] = set()
    if not PROD.exists():
        return seen
    for p in PROD.rglob("*"):
        if p.is_file() and p.suffix in (".json", ".md") and p.stat().st_size < 2_000_000:
            try:
                seen.update(re.findall(r"(?:watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})",
                                       p.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                pass
    return seen


VIDEO_ID = re.compile(r"(?:watch\?v=|youtu\.be/|shorts/|live/)([A-Za-z0-9_-]{11})"
                      r"|^([A-Za-z0-9_-]{11})$")


def cmd_sermons(args):
    import random

    items = list_sermons(args.preacher)
    if not items:
        die("no Sunday services matched — check --preacher or SERMON_CHANNEL")

    # `--find` exists so a hand-pasted URL still gets its folder named after the
    # service date. Naming it after today is how SUN-2026-09-01 (a Tuesday)
    # happened.
    if args.find:
        m = VIDEO_ID.search(args.find.strip())
        if not m:
            die(f"not a YouTube URL or video id: {args.find}")
        vid = m.group(1) or m.group(2)
        hit = next((s for s in items if s["id"] == vid), None)
        if hit is None:
            # Not a Sunday service on this channel — a Wednesday service, a
            # 새벽기도, another channel entirely. The caller decides.
            print(f"# {vid} 는 이 채널의 장선기 목사 주일예배 목록에 없다",
                  file=sys.stderr)
            sys.exit(3)
        print(json.dumps(hit, ensure_ascii=False) if args.json else hit["url"])
        if not args.json:
            print(hit["idea_id"])
            print(f"# {hit['title']}", file=sys.stderr)
            if hit["date_suspect"]:
                print(f"# ⚠ 제목의 날짜 {hit['title_date']} 는 일요일이 아니다 → "
                      f"{hit['date']} 로 잡았다", file=sys.stderr)
        return

    done = already_produced()
    fresh = [s for s in items if s["id"] not in done]
    pool = items if args.include_done else fresh

    if args.pick:
        if not pool:
            die("every listed service has already been produced — pass --include-done "
                "to allow a repeat")
        rng = random.Random(args.seed)
        s = rng.choice(pool)
        if args.json:
            print(json.dumps(s, ensure_ascii=False))
        else:
            print(s["url"])
            print(s["idea_id"])
        if not args.json:
            print(f"# {s['title']}", file=sys.stderr)
            print(f"# {s['duration'] // 60}분"
                  + (f" · 본문 {s['scripture']}" if s["scripture"] else ""), file=sys.stderr)
            if s["date_suspect"]:
                print(f"# ⚠ 제목의 날짜 {s['title_date']} 는 일요일이 아니다 → "
                      f"{s['date']} 로 잡았다", file=sys.stderr)
        return

    if args.json:
        print(json.dumps(pool[:args.limit], ensure_ascii=False, indent=2))
        return

    print(f"{CHANNEL_STREAMS}  ·  {SERMON_PREACHER} 주일예배 "
          f"{len(items)}편 중 미제작 {len(fresh)}편\n")
    for s in pool[:args.limit]:
        mark = "  " if s["id"] not in done else "✓ "
        flag = " ⚠날짜" if s["date_suspect"] else ""
        print(f"{mark}{s['date']}  {s['duration'] // 60:>2}분  {s['id']}{flag}  {s['title']}")
    if not args.include_done:
        print(f"\n제작된 {len(items) - len(fresh)}편은 숨겼다 (--include-done 로 표시).")
    print("\n무작위로 하나 뽑아 그대로 돌리려면:  bash scripts/weekly_run.sh --auto")


# ------------------------------------------------------------------ main ---
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sm = sub.add_parser("sermons", help="list the channel's Sunday services, or pick one")
    sm.add_argument("--pick", action="store_true",
                    help="choose one at random and print its URL and idea-id")
    sm.add_argument("--seed", type=int, default=None, help="make --pick reproducible")
    sm.add_argument("--limit", type=int, default=20)
    sm.add_argument("--preacher", default=SERMON_PREACHER,
                    help="title must contain this name; '' for no filter")
    sm.add_argument("--include-done", action="store_true",
                    help="do not hide services already produced")
    sm.add_argument("--find", metavar="URL",
                    help="look one URL up in the listing and print its idea-id")
    sm.add_argument("--json", action="store_true")
    sm.set_defaults(func=cmd_sermons)

    f = sub.add_parser("fetch"); f.add_argument("idea_id"); f.add_argument("--url", required=True)
    f.add_argument("--via", choices=["yt-dlp", "apify"], default="yt-dlp",
                   help="apify downloads on Apify's machines (paid); use only where "
                        "yt-dlp cannot reach YouTube's media servers")
    f.add_argument("--quality", default="480",
                   help="apify only: 360/480/720/1080. Billed per second of footage, "
                        "so this is the cost dial. Note 480 actually returns 640x360.")
    f.set_defaults(func=cmd_fetch)

    t = sub.add_parser("transcribe"); t.add_argument("idea_id")
    t.add_argument("--backend", choices=["auto", "whisper", "gemini"], default="auto")
    t.add_argument("--whole", action="store_true",
                   help="transcribe the whole recording, not just the sermon")
    t.add_argument("--no-structure", action="store_true",
                   help="skip service-structure detection (saves one paid call)")
    t.add_argument("--no-repair", action="store_true",
                   help="skip the duplicate/hole repair pass")
    t.set_defaults(func=cmd_transcribe)

    c = sub.add_parser("clips"); c.add_argument("idea_id")
    c.add_argument("--window", type=float, default=12.0, help="seconds per printed block")
    c.set_defaults(func=cmd_clips)

    r = sub.add_parser("render"); r.add_argument("idea_id")
    r.add_argument("--only", help="render just this clip id")
    r.add_argument("--no-end-card", action="store_true",
                   help="skip the closing service card")
    r.add_argument("--retime", action="store_true",
                   help="re-transcribe each clip window for exact caption sync "
                        "(one paid Gemini call per clip)")
    r.set_defaults(func=cmd_render)

    sel = sub.add_parser("select", help="pick the clips automatically instead of stopping")
    sel.add_argument("idea_id")
    sel.add_argument("--count", type=int, default=3)
    sel.add_argument("--backend", choices=["auto", "claude", "gemini"], default="auto")
    sel.set_defaults(func=cmd_select)

    rp = sub.add_parser("repair", help="drop seam duplicates and clamp impossible cue lengths")
    rp.add_argument("idea_id")
    rp.add_argument("--fill-holes", action="store_true",
                    help="also re-transcribe gaps (usually timestamp drift, not real gaps)")
    rp.set_defaults(func=cmd_repair)

    v = sub.add_parser("validate"); v.add_argument("idea_id")
    v.set_defaults(func=cmd_validate)

    sub.add_parser("doctor").set_defaults(func=cmd_doctor)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
