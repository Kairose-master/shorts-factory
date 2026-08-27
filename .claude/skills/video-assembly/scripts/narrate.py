#!/usr/bin/env python3
"""Synthesise narration and measure it. This runs BEFORE any frame is drawn.

Reads a lines file, writes one wav per line plus ``timing.json`` carrying the
**measured** duration of each. Those measurements are the scene clock; a
storyboard's guessed durations are not.

    python3 narrate.py --lines project/lines.json --out project/vo

lines.json:
    [{"id": "s1", "text": "..."},
     {"id": "s2", "text": "...", "voice": "en-US-AvaNeural"}]

Needs ``pip install edge-tts`` and outbound network. Behind an egress proxy the
script passes ``HTTPS_PROXY`` through to edge-tts, which does not read it itself.
"""
import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path

DEFAULT_VOICE = "en-US-AndrewNeural"


def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def is_cjk(text: str) -> bool:
    return any("\u3040" <= c <= "\u9fff" or "\uac00" <= c <= "\ud7af" for c in text)


def wav_seconds(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


async def synth(text: str, voice: str, rate: str, mp3: Path) -> list[dict]:
    """Write the audio and return the engine's word boundaries.

    Boundaries are what let a renderer land a reveal on the word it belongs to
    instead of on a guess. Offsets are seconds from the start of this line.
    """
    import edge_tts

    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    comm = edge_tts.Communicate(text, voice, rate=rate, proxy=proxy,
                                boundary="WordBoundary")
    words = []
    with open(mp3, "wb") as fh:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                fh.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                words.append({"t": round(chunk["offset"] / 1e7, 3),
                              "dur": round(chunk["duration"] / 1e7, 3),
                              "text": chunk["text"]})
    return words


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--rate", default="+0%", help='e.g. "-5%" to slow every line')
    ap.add_argument("--sr", type=int, default=24000)
    args = ap.parse_args()

    lines = json.loads(Path(args.lines).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    exe = ffmpeg_exe()

    timing = []
    for item in lines:
        sid, text = item["id"], item["text"]
        voice = item.get("voice", args.voice)
        rate = item.get("rate", args.rate)
        mp3, wav = out / f"{sid}.mp3", out / f"{sid}.wav"
        words_timed = asyncio.run(synth(text, voice, rate, mp3))
        if not mp3.exists() or mp3.stat().st_size == 0:
            print(f"FAIL {sid}: TTS returned no audio", file=sys.stderr)
            return 1
        subprocess.run([exe, "-y", "-loglevel", "error", "-i", str(mp3),
                        "-ar", str(args.sr), "-ac", "1", str(wav)], check=True)
        mp3.unlink()
        secs = wav_seconds(wav)
        words = len(text.split())
        chars = len([c for c in text if not c.isspace()])
        timing.append({"id": sid, "text": text, "voice": voice, "rate": rate,
                       "wav": str(wav), "seconds": round(secs, 3), "words": words,
                       "wpm": round(words / secs * 60, 1),
                       "chars": chars, "cps": round(chars / secs, 2),
                       "words_timed": words_timed})
        rate = (f"{timing[-1]['cps']:5.2f} chars/s" if is_cjk(text)
                else f"{timing[-1]['wpm']:5.1f} wpm")
        print(f"  {sid:>4}  {secs:6.2f}s  {chars:3d} chars  {rate}")

    (out / "timing.json").write_text(json.dumps(timing, indent=2, ensure_ascii=False))
    total = sum(t["seconds"] for t in timing)
    chars = sum(t["chars"] for t in timing)
    print(f"\n  total narration {total:.2f}s across {len(timing)} lines "
          f"({chars} chars, {chars / total:.2f} chars/s)")
    print(f"  wrote {out / 'timing.json'}  <- scene durations come from here, not the storyboard")
    if not any(t["words_timed"] for t in timing):
        print("  WARN: no word boundaries returned — reveals will have to be placed by ear")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
