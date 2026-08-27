#!/usr/bin/env python3
"""Lay narration onto the silent render at the plan's scene starts, normalise, mux.

    python3 mux.py --video project/silent.mp4 --plan project/plan.json \
        --out project/final.mp4 [--music bed.wav --music-db -22]

Each scene's wav is placed at its ``start`` from ``plan.json`` — never
concatenated — so a picture edit and an audio edit cannot drift apart. Output is
loudness-normalised to -14 LUFS, which is where TikTok, Reels and Shorts all
normalise to; louder gets turned down, quieter stays quiet.
"""
import argparse
import array
import json
import shutil
import subprocess
import wave
from pathlib import Path


def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def measure(exe, wav, target):
    """Analysis pass. Single-pass loudnorm lands 1-2 LUFS quiet; this fixes that."""
    r = subprocess.run(
        [exe, "-hide_banner", "-i", wav, "-af",
         f"loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True)
    start = r.stderr.rfind("{")
    if start == -1:
        return None
    try:
        return json.loads(r.stderr[start:r.stderr.rfind("}") + 1])
    except json.JSONDecodeError:
        return None


def read_wav(path, sr):
    with wave.open(str(path)) as w:
        if w.getframerate() != sr or w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise SystemExit(f"{path}: need mono 16-bit {sr}Hz, got "
                             f"{w.getnchannels()}ch {w.getsampwidth() * 8}bit {w.getframerate()}Hz")
        return array.array("h", w.readframes(w.getnframes()))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sr", type=int, default=24000)
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--music", help="optional bed, any format ffmpeg reads")
    ap.add_argument("--music-db", type=float, default=-22.0, help="bed level under the voice")
    ap.add_argument("--one-pass", action="store_true",
                    help="skip the analysis pass; lands 1-2 LUFS under target")
    args = ap.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    sr, total = args.sr, plan["duration"]
    bed = array.array("h", bytes(int(total * sr) * 2))

    for s in plan["scenes"]:
        vo = read_wav(s["vo"], sr)
        at = int(s["start"] * sr)
        for i, v in enumerate(vo):
            j = at + i
            if j >= len(bed):
                break
            mixed = bed[j] + v
            bed[j] = 32767 if mixed > 32767 else -32768 if mixed < -32768 else mixed

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    voice_wav = out.with_suffix(".voice.wav")
    with wave.open(str(voice_wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bed.tobytes())

    exe = ffmpeg_exe()
    norm = f"loudnorm=I={args.lufs}:TP=-1.5:LRA=11"
    if not args.one_pass:
        m = measure(exe, str(voice_wav), args.lufs)
        if m:
            norm += (f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
                     f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
                     f":offset={m['target_offset']}:linear=true")
            print(f"  measured {m['input_i']} LUFS → normalising to {args.lufs}")
        else:
            print("  WARN: loudnorm analysis produced no numbers; falling back to one pass")
    cmd = [exe, "-y", "-loglevel", "error", "-i", args.video, "-i", str(voice_wav)]
    if args.music:
        cmd += ["-i", args.music]
        fc = (f"[2:a]volume={args.music_db}dB,atrim=0:{total},afade=t=out:st={max(0, total - 1.2)}:d=1.2[m];"
              f"[1:a][m]amix=inputs=2:duration=first:dropout_transition=0[mix];"
              f"[mix]{norm}[a]")
    else:
        fc = f"[1:a]{norm}[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-shortest", str(out)]
    subprocess.run(cmd, check=True)
    voice_wav.unlink()
    print(f"  wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
