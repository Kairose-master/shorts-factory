#!/usr/bin/env python3
"""Generate Korean narration for a longform episode, one file per spoken beat.

One call per beat, not one per scene. That is the whole design: the storyboard
is the pipeline's single timing source, so audio must conform to it rather than
the other way round. Generating per beat lets every line be placed at exactly
its storyboard `t`, which makes drift impossible by construction instead of
merely small.

Each speaker gets its own voice. A single-voice render of a two-speaker script
is a content failure, not a cosmetic one — the argument depends on the viewer
hearing a second speaker.

Engines
  edge    Microsoft Edge neural voices. Free, no credential, good Korean,
          ~1-2s per line. The default.
  gemini  Gemini TTS. Better direction-following (it takes a style prompt in
          Korean), but the free tier allows only 10 requests per day per model,
          which is far short of a full episode.

Usage:
  python3 scripts/generate_narration.py --storyboard <p> --out <dir>
          [--engine edge|gemini] [--only S08] [--workers 3] [--force]
"""
import argparse
import asyncio
import base64
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

RATE = 48000

# ---------------------------------------------------------------- voice casting

EDGE_VOICES = {
    # Calm, young adult, intellectually curious. Not sermon-like, not announcer.
    # Slowed slightly: the script's silences only read as silences if the speech
    # around them is unhurried.
    "narrator": {"voice": "ko-KR-InJoonNeural", "rate": "-3%", "pitch": "-2Hz"},
    # Distinct timbre and flatter delivery. A different gender is the bluntest
    # available separation, and separation is the point. NOT processed into a
    # machine voice: making it sound synthetic answers the episode's question in
    # the sound design, which is the one thing the episode refuses to do.
    "ai": {"voice": "ko-KR-SunHiNeural", "rate": "-8%", "pitch": "-4Hz"},
}
EDGE_VOICES["copy"] = EDGE_VOICES["ai"]

GEMINI_VOICES = {
    "narrator": {
        "voice": "Charon",
        "style": ("차분하고 사색적인 한국어 내레이션으로 읽어주세요. 설교하는 톤이나 "
                  "아나운서 톤이 아니라, 지적으로 호기심이 많은 20대 후반이 조용한 "
                  "방에서 혼자 생각하며 말하듯이. 서두르지 마세요."),
    },
    "ai": {
        "voice": "Schedar",
        "style": ("감정을 절제한 평탄한 톤으로 읽어주세요. 기계음이 아니라, 자기 "
                  "상태를 조심스럽게 설명하는 사람처럼. 확신 없이, 그러나 또렷하게."),
    },
}
GEMINI_VOICES["copy"] = GEMINI_VOICES["ai"]
GEMINI_MODEL = "gemini-3.1-flash-tts-preview"


def ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def to_wav(src: Path, dst: Path):
    """Normalise whatever the engine returned to 48k mono WAV."""
    subprocess.run(
        [ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", str(src),
         "-ar", str(RATE), "-ac", "1", "-y", str(dst)],
        check=True,
    )


# ---------------------------------------------------------------------- engines

def edge_setup():
    """edge-tts opens a direct websocket with a certifi-only SSL context, so in
    a proxied container it both bypasses HTTPS_PROXY and fails to trust the
    proxy's CA. Route it through the proxy and build the context from the
    environment's own CA bundle — extending trust to the configured CA, never
    skipping verification."""
    import edge_tts.communicate as C
    for ca in ("/root/.ccr/ca-bundle.crt", os.environ.get("SSL_CERT_FILE", "")):
        if ca and Path(ca).exists():
            C._SSL_CTX = ssl.create_default_context(cafile=ca)
            break
    return os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")


async def edge_synth(text, speaker, tmp: Path, proxy):
    import edge_tts
    cfg = EDGE_VOICES.get(speaker, EDGE_VOICES["narrator"])
    await edge_tts.Communicate(
        text, cfg["voice"], rate=cfg["rate"], pitch=cfg["pitch"], proxy=proxy
    ).save(str(tmp))


def gemini_synth(text, speaker, key, tmp: Path):
    cfg = GEMINI_VOICES.get(speaker, GEMINI_VOICES["narrator"])
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{GEMINI_MODEL}:generateContent?key={key}")
    body = {
        "contents": [{"parts": [{"text": f"{cfg['style']}\n\n{text}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": cfg["voice"]}}
            },
        },
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        d = json.load(r)
    part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
    pcm = base64.b64decode(part["data"])
    rate = int(part["mimeType"].split("rate=")[1]) if "rate=" in part["mimeType"] else 24000
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(pcm)


# ------------------------------------------------------------------------- main

def spoken_beats(sb):
    out = []
    for scene in sb["scenes"]:
        for i, b in enumerate(scene["beats"]):
            if b.get("vo"):
                out.append({
                    "key": f"{scene['id']}_{i:02d}", "scene": scene["id"],
                    "t": b["t"], "dur": b["dur"], "vo": b["vo"],
                    "speaker": b.get("speaker") or scene.get("voice") or "narrator",
                })
    return out


async def run(a, beats, out: Path):
    proxy = edge_setup() if a.engine == "edge" else None
    key = os.environ.get("GEMINI_API_KEY") if a.engine == "gemini" else None
    if a.engine == "gemini" and not key:
        print("GEMINI_API_KEY is not set.", file=sys.stderr)
        return [], [("-", "no credential")]

    sem = asyncio.Semaphore(a.workers)
    done, failures = [], []

    async def work(b, idx):
        async with sem:
            dst = out / "beats" / f"{b['key']}.wav"
            tmp = out / "beats" / f".{b['key']}.tmp"
            for attempt in range(5):
                try:
                    if a.engine == "edge":
                        await edge_synth(b["vo"], b["speaker"], tmp, proxy)
                    else:
                        await asyncio.to_thread(
                            gemini_synth, b["vo"], b["speaker"], key, tmp)
                    await asyncio.to_thread(to_wav, tmp, dst)
                    tmp.unlink(missing_ok=True)
                    with wave.open(str(dst)) as w:
                        secs = w.getnframes() / w.getframerate()
                    done.append(b["key"])
                    print(f"  [{len(done)}/{len(beats)}] {b['key']} {secs:5.2f}s")
                    return
                except Exception as exc:
                    if attempt == 4:
                        failures.append((b["key"], f"{type(exc).__name__}: {exc}"))
                        print(f"  {b['key']} FAILED: {str(exc)[:90]}")
                        return
                    await asyncio.sleep(2 * (attempt + 1))

    await asyncio.gather(*(work(b, i) for i, b in enumerate(beats)))
    return done, failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--storyboard", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--engine", choices=["edge", "gemini"], default="edge")
    ap.add_argument("--only")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    sb = json.loads(Path(a.storyboard).read_text(encoding="utf-8"))
    beats = spoken_beats(sb)
    if a.only:
        beats = [b for b in beats if b["scene"] == a.only]

    out = Path(a.out)
    (out / "beats").mkdir(parents=True, exist_ok=True)
    todo = [b for b in beats
            if a.force or not (out / "beats" / f"{b['key']}.wav").exists()]
    print(f"engine={a.engine}  {len(beats)} spoken beats, {len(todo)} to generate "
          f"({len(beats) - len(todo)} cached)")

    t0 = time.time()
    _, failures = asyncio.run(run(a, todo, out))

    report = []
    for b in beats:
        f = out / "beats" / f"{b['key']}.wav"
        if not f.exists():
            continue
        with wave.open(str(f)) as w:
            secs = w.getnframes() / w.getframerate()
        report.append({**b, "audioSec": round(secs, 2),
                       "overrun": round(secs - b["dur"], 2)})
    (out / "beats.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    over = [r for r in report if r["overrun"] > 0]
    print(f"\n{len(report)}/{len(beats)} beats present  ({time.time() - t0:.0f}s)")
    print(f"overruns (line longer than its beat): {len(over)}"
          + (f", worst {max(r['overrun'] for r in over):+.2f}s" if over else ""))
    if failures:
        print(f"FAILURES: {len(failures)}")
        for k, e in failures[:10]:
            print(f"  {k}: {e[:110]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
