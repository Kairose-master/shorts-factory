#!/usr/bin/env python3
"""Korean <-> Chinese bilingual subtitles for a spoken video, end to end.

Stages (each is a subcommand; `run` chains them):

  transcribe  faster-whisper (large-v3-turbo, CPU int8) -> word-timed cues
  translate   Gemini: light ASR clean-up + translation into the other language
  build       styled .ass (source line over translation line) + .srt files
  render      ffmpeg: burn subtitles, loudness-normalise audio, title card

Free path: whisper runs locally. Gemini is the only metered call
(GEMINI_API_KEY) — roughly one request per 50 cues.

Usage:
  python3 scripts/bilingual_subtitles.py run VIDEO.mp4 --lang ko --out WORKDIR \
      --title-src "..." --title-dst "..." --meta "..." --badge "..." --church "..." \
      --reconstruct --bg-crop 640:360:640:360 --mp4 OUT.mp4 [--glossary "하나님=上帝, ..."]

`--reconstruct` is for videos that are a static slide over audio: the output
is rebuilt at --size on a blurred, text-free crop of the slide, with an intro
card, a persistent bilingual header, centred bilingual subtitles, a progress
bar and a clock. Without it the subtitles are burned onto the source frames.

Language codes: `ko` (Korean source, Chinese translation) or `zh` (Chinese
source, Korean translation). Chinese is always written in Simplified characters.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

OTHER = {"ko": "zh", "zh": "ko"}
LANG_NAME = {"ko": "Korean", "zh": "Simplified Chinese"}
FONT = {"ko": "Noto Sans CJK KR", "zh": "Noto Sans CJK SC"}

# Cue shaping. CJK reads fast; keep lines short and cues under ~6 s.
MAX_CHARS = {"ko": 26, "zh": 22}
MAX_CUE_SEC = 6.0
GAP_SPLIT_SEC = 0.9
MIN_CUE_SEC = 0.8

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    print("$", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run(cmd, check=True, **kw)


def ffmpeg_bin() -> str:
    for cand in ("ffmpeg", "/usr/local/bin/ffmpeg", "/usr/bin/ffmpeg"):
        if shutil.which(cand) or Path(cand).exists():
            return cand
    sys.exit("ffmpeg not found — apt-get install ffmpeg (needs libass)")


# --------------------------------------------------------------------------- #
# 1. transcribe
# --------------------------------------------------------------------------- #
def extract_wav(video: Path, wav: Path) -> None:
    if wav.exists():
        return
    sh([ffmpeg_bin(), "-y", "-loglevel", "error", "-i", str(video), "-vn", "-ac", "1",
        "-ar", "16000", "-c:a", "pcm_s16le", str(wav)])


def transcribe(video: Path, lang: str, out: Path, model_name: str = "large-v3-turbo") -> Path:
    from faster_whisper import WhisperModel  # heavy import, keep local

    out.mkdir(parents=True, exist_ok=True)
    wav = out / "audio16k.wav"
    extract_wav(video, wav)
    seg_path = out / "whisper_raw.json"
    if seg_path.exists():
        print("transcribe: reusing", seg_path)
        return seg_path

    model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=os.cpu_count() or 4)
    t0 = time.time()
    segments, info = model.transcribe(
        str(wav), language=lang, beam_size=5, word_timestamps=True,
        vad_filter=True, vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=False,  # fewer runaway repetitions on hymns
    )
    raw = []
    for s in segments:
        raw.append({
            "start": s.start, "end": s.end, "text": s.text.strip(),
            "avg_logprob": s.avg_logprob, "no_speech_prob": s.no_speech_prob,
            "compression_ratio": s.compression_ratio,
            "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in (s.words or [])],
        })
        if len(raw) % 25 == 0:
            print(f"  {len(raw)} segments, at {s.end:7.1f}s  ({time.time()-t0:.0f}s elapsed)", flush=True)
    seg_path.write_text(json.dumps({"language": info.language, "duration": info.duration,
                                    "model": model_name, "segments": raw}, ensure_ascii=False, indent=1))
    print(f"transcribe: {len(raw)} segments in {time.time()-t0:.0f}s -> {seg_path}")
    return seg_path


def is_junk(seg: dict) -> bool:
    """Whisper's usual failure modes on music and silence."""
    if not seg["text"]:
        return True
    if seg["no_speech_prob"] > 0.75 and seg["avg_logprob"] < -0.9:
        return True
    if seg["compression_ratio"] > 2.6:
        return True
    return False


def shape_cues(seg_path: Path, lang: str, out: Path) -> Path:
    """Re-cut whisper segments into subtitle-sized cues using word timings."""
    data = json.loads(seg_path.read_text())
    max_chars = MAX_CHARS[lang]
    cues, dropped = [], []
    for seg in data["segments"]:
        if is_junk(seg):
            dropped.append(seg)
            continue
        words = seg["words"] or [{"w": seg["text"], "s": seg["start"], "e": seg["end"], "p": 1}]
        buf, b_start, b_end = [], None, None

        def flush():
            nonlocal buf, b_start, b_end
            text = "".join(buf).strip() if lang == "zh" else " ".join(w.strip() for w in buf).strip()
            text = re.sub(r"\s+", " ", text)
            if text:
                cues.append({"start": round(b_start, 3), "end": round(max(b_end, b_start + MIN_CUE_SEC), 3), "src": text})
            buf, b_start, b_end = [], None, None

        for w in words:
            token = w["w"]
            if b_start is None:
                b_start = w["s"]
            gap = w["s"] - b_end if b_end is not None else 0
            cur_len = len("".join(buf)) if lang == "zh" else len(" ".join(buf))
            too_long = cur_len + len(token) > max_chars
            too_slow = b_end is not None and (w["e"] - b_start) > MAX_CUE_SEC
            if buf and (too_long or too_slow or gap > GAP_SPLIT_SEC):
                flush()
                b_start = w["s"]
            buf.append(token)
            b_end = w["e"]
            if lang == "zh" and re.search(r"[。！？!?]$", token.strip()) and len("".join(buf)) >= 8:
                flush()
            elif lang == "ko" and re.search(r"[.!?]$", token.strip()) and len(" ".join(buf)) >= 10:
                flush()
        if buf:
            flush()

    # no overlaps: a cue ends where the next one starts if they collide
    for a, b in zip(cues, cues[1:]):
        if a["end"] > b["start"]:
            a["end"] = round(max(b["start"] - 0.05, a["start"] + 0.3), 3)
    for i, c in enumerate(cues):
        c["id"] = i + 1
    cue_path = out / "cues.json"
    cue_path.write_text(json.dumps({"lang": lang, "cues": cues, "dropped": dropped}, ensure_ascii=False, indent=1))
    print(f"shape: {len(cues)} cues, {len(dropped)} whisper segments dropped as junk -> {cue_path}")
    return cue_path


# --------------------------------------------------------------------------- #
# 2. translate (Gemini)
# --------------------------------------------------------------------------- #
PROMPT = """You are subtitling a Korean Protestant church Sunday service ({service}).
The automatic speech recognition below is in {src_name}. For EVERY cue, return:
  "id"      the same id
  "src"     the {src_name} line, corrected only where the ASR is clearly wrong
            (misheard words, missing spacing/punctuation). Keep the speaker's
            wording; do not paraphrase, shorten, or add anything.
  "dst"     a faithful {dst_name} translation of that cue, natural spoken
            register, subtitle length (short). One cue = one translation; never
            merge or move content across cues. Use standard Christian
            terminology in the target language.{glossary}
  "garbled" true only if the cue is not intelligible speech at all (singing
            transcribed as nonsense, pure noise). Such cues are hidden.

Context cues (already handled, do not return them):
{context}

Cues to process (JSON array):
{batch}

Return ONLY a JSON array of objects with keys id, src, dst, garbled — same
order, same ids, nothing else."""


def gemini(prompt: str, key: str, retries: int = 5) -> str:
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json", "maxOutputTokens": 16000},
    }).encode()
    url = GEMINI_URL.format(model=GEMINI_MODEL, key=key)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            return d["candidates"][0]["content"]["parts"][0]["text"]
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            wait = 2 ** attempt * 3
            print(f"  gemini error ({e}); retry in {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError("Gemini failed repeatedly")


def translate(cue_path: Path, lang: str, out: Path, service: str, glossary: str = "", batch_size: int = 50) -> Path:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is unset — translation needs it. Nothing was called.")
    data = json.loads(cue_path.read_text())
    cues = data["cues"]
    dst_lang = OTHER[lang]
    bi_path = out / "bilingual.json"
    done: dict[int, dict] = {}
    if bi_path.exists():
        done = {c["id"]: c for c in json.loads(bi_path.read_text())["cues"] if "dst" in c}
        print(f"translate: resuming, {len(done)} cues already done")
    gl = f"\n  Glossary (must follow): {glossary}" if glossary else ""
    calls = 0

    def ask(batch: list[dict], ctx: list[dict]) -> dict[int, dict]:
        """One Gemini round-trip for a batch; on an unparsable reply retry, then
        split the batch in half so one bad reply never sinks the whole run."""
        nonlocal calls
        prompt = PROMPT.format(
            service=service, src_name=LANG_NAME[lang], dst_name=LANG_NAME[dst_lang], glossary=gl,
            context=json.dumps(ctx, ensure_ascii=False),
            batch=json.dumps([{"id": c["id"], "src": c["src"]} for c in batch], ensure_ascii=False),
        )
        for attempt in range(2):
            text = gemini(prompt, key)
            calls += 1
            try:
                res = json.loads(text)
                return {int(r["id"]): r for r in res if isinstance(r, dict) and "id" in r}
            except (json.JSONDecodeError, TypeError, ValueError):
                print(f"  unparsable Gemini reply for ids {batch[0]['id']}-{batch[-1]['id']} (attempt {attempt+1})", flush=True)
        if len(batch) > 4:
            half = len(batch) // 2
            return {**ask(batch[:half], ctx), **ask(batch[half:], batch[:half][-3:])}
        return {}

    for i in range(0, len(cues), batch_size):
        batch = [c for c in cues[i:i + batch_size] if c["id"] not in done]
        if not batch:
            continue
        ctx = [{"id": c["id"], "src": c["src"]} for c in cues[max(0, i - 3):i]]
        by_id = ask(batch, ctx)
        missing = [c["id"] for c in batch if c["id"] not in by_id]
        if missing:
            print(f"  batch {i//batch_size}: {len(missing)} ids missing from Gemini reply, kept ASR text untranslated")
        for c in batch:
            r = by_id.get(c["id"], {})
            done[c["id"]] = {**c, "asr": c["src"], "src": (r.get("src") or c["src"]).strip(),
                             "dst": (r.get("dst") or "").strip(), "garbled": bool(r.get("garbled", False))}
        merged = [done.get(c["id"], c) for c in cues]
        bi_path.write_text(json.dumps({"lang": lang, "dst_lang": dst_lang, "model": GEMINI_MODEL,
                                       "cues": merged}, ensure_ascii=False, indent=1))
        print(f"  translated {min(i+batch_size, len(cues))}/{len(cues)} (gemini calls: {calls})", flush=True)
    print(f"translate: done, {calls} Gemini calls -> {bi_path}")
    return bi_path


# --------------------------------------------------------------------------- #
# 3. build .ass / .srt
# --------------------------------------------------------------------------- #
def ts_srt(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


def ts_ass(t: float) -> str:
    cs = int(round(t * 100))
    return f"{cs//360000:d}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"


def ass_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", " ")


def fmt_clock(t: float) -> str:
    t = int(t)
    return f"{t//60:02d}:{t%60:02d}"


def build(bi_path: Path, out: Path, width: int, height: int, title_src: str, title_dst: str,
          meta: str = "", badge: str = "", church: str = "", duration: float = 0.0,
          intro_sec: float = 6.0) -> tuple[Path, list[Path]]:
    """Write bilingual.ass (the reconstructed layout) and three .srt files.

    Layout, on a PlayRes of width x height:
      * intro card (0 .. intro_sec): church, title in both languages, meta line
      * persistent header top-left from intro_sec: title src / title dst / meta
      * badge top-right (e.g. "한국어 설교 · 中文字幕")
      * subtitles: source line (white) over translation line (gold), centred
      * progress bar + clock along the bottom edge (one event per second)
    """
    data = json.loads(bi_path.read_text())
    lang, dst_lang = data["lang"], data["dst_lang"]
    cues = [c for c in data["cues"] if c.get("dst") and not c.get("garbled")]
    k = height / 1080  # every size below is designed at 1080p
    px = lambda v: max(1, round(v * k))
    outline = px(2.5)
    white, gold, grey, dim = "&H00FFFFFF", "&H008FDFFF", "&H00C8C8C8", "&H00909090"

    def style(name, font, size, colour, bold, align, ml, mr, mv, shadow=1):
        return (f"Style: {name},{font},{size},{colour},{colour},&H00101010,&H80000000,{-1 if bold else 0},"
                f"0,0,0,100,100,0,0,1,{outline},{shadow},{align},{ml},{mr},{mv},1\n")

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
"""
    header += style("Src", FONT[lang], px(58), white, True, 2, px(180), px(180), px(150))
    header += style("Dst", FONT[dst_lang], px(46), gold, False, 2, px(180), px(180), px(150))
    header += style("HeadSrc", FONT[lang], px(40), white, True, 7, px(80), px(80), px(56))
    header += style("HeadDst", FONT[dst_lang], px(32), gold, False, 7, px(80), px(80), px(56))
    header += style("HeadMeta", FONT["ko"], px(26), grey, False, 7, px(80), px(80), px(56))
    header += style("Badge", FONT["ko"], px(26), grey, False, 9, px(80), px(80), px(60))
    header += style("IntroChurch", FONT["ko"], px(34), grey, False, 5, px(120), px(120), 0)
    header += style("IntroSrc", FONT[lang], px(72), white, True, 5, px(120), px(120), 0)
    header += style("IntroDst", FONT[dst_lang], px(54), gold, False, 5, px(120), px(120), 0)
    header += style("IntroMeta", FONT["ko"], px(34), grey, False, 5, px(120), px(120), 0)
    header += style("Clock", FONT["ko"], px(24), dim, False, 3, px(80), px(80), px(34), shadow=0)
    header += style("Bar", FONT["ko"], px(20), gold, False, 7, 0, 0, 0, shadow=0)
    header += "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    ev = [header]
    E = ass_escape

    def dlg(layer, t0, t1, st, text):
        ev.append(f"Dialogue: {layer},{ts_ass(t0)},{ts_ass(t1)},{st},,0,0,0,,{text}\n")

    # intro card
    intro = [f"{{\\rIntroChurch}}{E(church)}" if church else "", f"{{\\rIntroSrc}}{E(title_src)}",
             f"{{\\rIntroDst}}{E(title_dst)}", f"{{\\rIntroMeta}}{E(meta)}" if meta else ""]
    dlg(2, 0.0, intro_sec, "IntroSrc", "{\\fad(500,700)}" + "\\N".join(x for x in intro if x))
    # persistent header + badge
    end_t = duration if duration else (cues[-1]["end"] + 2 if cues else intro_sec)
    head = [f"{{\\rHeadSrc}}{E(title_src)}", f"{{\\rHeadDst}}{E(title_dst)}"] + ([f"{{\\rHeadMeta}}{E(meta)}"] if meta else [])
    dlg(2, intro_sec, end_t, "HeadSrc", "{\\fad(600,0)}" + "\\N".join(head))
    if badge:
        dlg(2, intro_sec, end_t, "Badge", "{\\fad(600,0)}" + E(badge))
    # progress bar (track + fill) and clock, one second at a time
    if duration:
        x0, x1, y, h = px(80), width - px(80), height - px(22), px(5)
        dlg(1, 0, end_t, "Bar", f"{{\\an7\\pos(0,0)\\1c&H3A3A3A&\\bord0\\p1}}m {x0} {y} l {x1} {y} l {x1} {y+h} l {x0} {y+h}{{\\p0}}")
        for sec in range(int(duration) + 1):
            xf = x0 + (x1 - x0) * min(1.0, sec / duration)
            dlg(1, sec, min(sec + 1, end_t), "Bar", f"{{\\an7\\pos(0,0)\\bord0\\p1}}m {x0} {y} l {xf:.0f} {y} l {xf:.0f} {y+h} l {x0} {y+h}{{\\p0}}")
            dlg(1, sec, min(sec + 1, end_t), "Clock", f"{fmt_clock(sec)} / {fmt_clock(duration)}")
    # the subtitles themselves
    for c in cues:
        dlg(0, c["start"], c["end"], "Src", f"{E(c['src'])}\\N{{\\rDst}}{E(c['dst'])}")

    ass_path = out / "bilingual.ass"
    ass_path.write_text("".join(ev), encoding="utf-8")

    srts = []
    for name, key in ((lang, "src"), (dst_lang, "dst"), (f"{lang}-{dst_lang}", None)):
        p = out / f"subtitles.{name}.srt"
        chunks = []
        for i, c in enumerate(cues, 1):
            text = f"{c['src']}\n{c['dst']}" if key is None else c[key]
            chunks.append(f"{i}\n{ts_srt(c['start'])} --> {ts_srt(c['end'])}\n{text}\n")
        p.write_text("\n".join(chunks), encoding="utf-8")
        srts.append(p)
    print(f"build: {len(cues)} cues -> {ass_path.name}, {[s.name for s in srts]}")
    return ass_path, srts


# --------------------------------------------------------------------------- #
# 4. render
# --------------------------------------------------------------------------- #
def probe(video: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(video)],
                         capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    return {"width": s["width"], "height": s["height"], "duration": float(d["format"]["duration"])}


def measure_loudness(video: Path) -> dict:
    r = subprocess.run([ffmpeg_bin(), "-hide_banner", "-i", str(video), "-vn",
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    return json.loads(m.group(0)) if m else {}


def make_background(video: Path, out_png: Path, width: int, height: int, crop: str = "") -> Path:
    """A clean still to rebuild the video on: a text-free region of the source
    frame, blown up and softly blurred so its colour and glow survive but no
    original typography does. `crop` is an ffmpeg crop spec (w:h:x:y)."""
    vf = (f"crop={crop}," if crop else "") + f"scale={width}:{height}:flags=lanczos,gblur=sigma=18,eq=brightness=-0.03:saturation=1.2"
    at = min(60.0, probe(video)["duration"] / 2)
    sh([ffmpeg_bin(), "-y", "-loglevel", "error", "-ss", f"{at:.2f}", "-i", str(video), "-frames:v", "1", "-vf", vf, str(out_png)])
    if not out_png.exists():
        sys.exit(f"could not grab a background frame from {video}")
    return out_png


def render(video: Path, ass_path: Path, out_mp4: Path, crf: int = 21, preset: str = "medium",
           background: Path | None = None, size: tuple[int, int] | None = None) -> Path:
    """Burn the .ass onto the source video, or — with `background` — onto a
    still image (the reconstructed layout) using the source's audio only."""
    stats = measure_loudness(video)
    if stats:
        af = ("loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:"
              f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
              f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
              f"offset={stats['target_offset']},highpass=f=70")
    else:
        af = "loudnorm=I=-16:TP=-1.5:LRA=11,highpass=f=70"
    vf = f"ass={ass_path.as_posix()}:fontsdir=/usr/share/fonts,format=yuv420p"
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "warning", "-stats"]
    if background:
        dur = probe(video)["duration"]
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(background), "-i", str(video),
                "-map", "0:v:0", "-map", "1:a:0", "-t", f"{dur:.3f}", "-tune", "stillimage"]
    else:
        cmd += ["-i", str(video)]
    cmd += ["-vf", vf, "-af", af, "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", str(out_mp4)]
    sh(cmd)
    print(f"render: -> {out_mp4} ({out_mp4.stat().st_size/1e6:.1f} MB)")
    return out_mp4


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--lang", choices=("ko", "zh"), required=True, help="spoken language of the video")
        p.add_argument("--out", type=Path, required=True, help="work directory")

    p = sub.add_parser("transcribe"); p.add_argument("video", type=Path); common(p)
    p.add_argument("--model", default="large-v3-turbo")
    p = sub.add_parser("translate"); common(p)
    p.add_argument("--service", default="Sunday worship service"); p.add_argument("--glossary", default="")
    def layout(p):
        p.add_argument("--title-src", required=True, help="sermon/video title in the spoken language")
        p.add_argument("--title-dst", required=True, help="the same title in the other language")
        p.add_argument("--meta", default="", help="one line: scripture · date · service")
        p.add_argument("--badge", default="", help="top-right tag, e.g. '한국어 설교 · 中文字幕'")
        p.add_argument("--church", default="", help="church name line on the intro card")
        p.add_argument("--reconstruct", action="store_true",
                       help="rebuild on a clean still instead of burning onto the source frames")
        p.add_argument("--bg-crop", default="", help="crop w:h:x:y of a text-free source region for the still")
        p.add_argument("--size", default="1920x1080", help="output size in --reconstruct mode")

    def encode(p):
        p.add_argument("--mp4", type=Path, required=True); p.add_argument("--crf", type=int, default=21)
        p.add_argument("--preset", default="medium")

    p = sub.add_parser("build"); common(p); p.add_argument("video", type=Path); layout(p)
    p = sub.add_parser("render"); common(p); p.add_argument("video", type=Path); layout(p); encode(p)
    p = sub.add_parser("run"); p.add_argument("video", type=Path); common(p)
    p.add_argument("--model", default="large-v3-turbo"); p.add_argument("--service", default="Sunday worship service")
    p.add_argument("--glossary", default=""); layout(p); encode(p)
    a = ap.parse_args()

    a.out.mkdir(parents=True, exist_ok=True)
    if a.cmd in ("transcribe", "run"):
        seg = transcribe(a.video, a.lang, a.out, a.model)
        shape_cues(seg, a.lang, a.out)
    if a.cmd in ("translate", "run"):
        translate(a.out / "cues.json", a.lang, a.out, a.service, a.glossary)
    if a.cmd in ("build", "render", "run"):
        info = probe(a.video)
        w, h = (map(int, a.size.lower().split("x")) if a.reconstruct else (info["width"], info["height"]))
    if a.cmd in ("build", "run") or (a.cmd == "render" and not (a.out / "bilingual.ass").exists()):
        build(a.out / "bilingual.json", a.out, w, h, a.title_src, a.title_dst, a.meta, a.badge, a.church,
              info["duration"])
    if a.cmd in ("render", "run"):
        bg = make_background(a.video, a.out / "background.png", w, h, a.bg_crop) if a.reconstruct else None
        render(a.video, a.out / "bilingual.ass", a.mp4, a.crf, a.preset, bg, (w, h))


if __name__ == "__main__":
    main()
