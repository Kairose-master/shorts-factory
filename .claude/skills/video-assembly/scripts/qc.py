#!/usr/bin/env python3
"""Gate a finished render against the plan it was built from.

    python3 qc.py --video project/final.mp4 --plan project/plan.json

Checks the file, not the intention: container duration against the plan, stream
resolution and fps, that an audio track exists and is near the platform's
-14 LUFS, that the picture does not end black or frozen, and that the plan is
internally consistent. Exits non-zero so it can gate a commit.

It decodes twelve frames and the audio envelope. It does not judge whether the
video is any good — that is what ``--sheet`` is for: it writes a contact sheet
and tells you to open it.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

OK, WARN, ERR = "ok  ", "WARN", "FAIL"


def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def probe(video):
    """Duration, size and fps parsed from ffmpeg's banner — no ffprobe needed."""
    txt = subprocess.run([ffmpeg_exe(), "-i", video], capture_output=True, text=True).stderr
    info = {"duration": None, "w": None, "h": None, "fps": None, "audio": False}
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", txt)
    if m:
        info["duration"] = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
    m = re.search(r"Video: .*?(\d{2,5})x(\d{2,5})", txt)
    if m:
        info["w"], info["h"] = int(m[1]), int(m[2])
    m = re.search(r"([\d.]+) fps", txt)
    if m:
        info["fps"] = float(m[1])
    info["audio"] = " Audio: " in txt
    return info


def frames(video, at, count, w=108, h=192):
    """`count` consecutive decoded frames starting at `at` seconds, downscaled."""
    raw = subprocess.run(
        [ffmpeg_exe(), "-v", "error", "-ss", f"{at:.3f}", "-i", video,
         "-frames:v", str(count), "-vf", f"scale={w}:{h}", "-f", "rawvideo",
         "-pix_fmt", "gray", "-"], capture_output=True).stdout
    n = w * h
    return [raw[i * n:(i + 1) * n] for i in range(len(raw) // n)]


def loudness(video):
    txt = subprocess.run(
        [ffmpeg_exe(), "-v", "info", "-i", video, "-af", "ebur128=peak=true",
         "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", txt)
    return float(m[-1]) if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--tolerance", type=float, default=0.30, help="seconds vs plan")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--allow-freeze", action="store_true")
    ap.add_argument("--sheet", help="also write a contact sheet here")
    args = ap.parse_args()

    rows, bad = [], 0

    def say(level, name, detail):
        nonlocal bad
        if level == ERR:
            bad += 1
        rows.append((level, name, detail))

    video = Path(args.video)
    if not video.is_file() or video.stat().st_size == 0:
        print(f"[{ERR}] file            {video} missing or empty")
        return 1
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))

    # --- the plan has to make sense before the file is judged against it
    prev_end, plan_bad = 0.0, []
    for s in plan["scenes"]:
        if s["start"] + 1e-6 < prev_end:
            plan_bad.append(f"{s['id']} starts before {prev_end:.2f}s")
        if s.get("vo_seconds", 0) > s["dur"] + 1e-6:
            plan_bad.append(f"{s['id']} narration {s['vo_seconds']:.2f}s > slot {s['dur']:.2f}s")
        prev_end = s["start"] + s["dur"]
    if prev_end > plan["duration"] + 1e-6:
        plan_bad.append(f"scenes end at {prev_end:.2f}s, plan says {plan['duration']:.2f}s")
    say(ERR if plan_bad else OK, "plan",
        "; ".join(plan_bad) if plan_bad else
        f"{len(plan['scenes'])} scenes, {plan['duration']:.2f}s, no overlap")

    info = probe(str(video))
    say(OK if info["duration"] else ERR, "container",
        f"{info['duration']:.2f}s {info['w']}x{info['h']} {info['fps']}fps"
        if info["duration"] else "unreadable")

    if info["duration"] is not None:
        delta = info["duration"] - plan["duration"]
        say(OK if abs(delta) <= args.tolerance else ERR, "duration",
            f"{info['duration']:.2f}s vs plan {plan['duration']:.2f}s ({delta:+.2f}s)")

    say(OK if (info["w"], info["h"]) == (plan["width"], plan["height"]) else ERR, "resolution",
        f"{info['w']}x{info['h']} vs plan {plan['width']}x{plan['height']}")
    say(OK if info["fps"] and abs(info["fps"] - plan["fps"]) < 0.5 else ERR, "fps",
        f"{info['fps']} vs plan {plan['fps']}")

    if not info["audio"]:
        say(ERR, "audio", "no audio stream — a silent short is a dead short")
    else:
        lu = loudness(str(video))
        if lu is None:
            say(WARN, "loudness", "ebur128 produced no reading")
        else:
            off = lu - args.lufs
            say(OK if abs(off) <= 2.0 else WARN, "loudness",
                f"{lu:.1f} LUFS vs target {args.lufs:.1f} ({off:+.1f})")

    dur = info["duration"] or plan["duration"]
    tail = frames(str(video), max(0, dur - 0.45), 6)
    if not tail:
        say(ERR, "tail", "could not decode the last half second")
    else:
        brightest = max(max(f) for f in tail)
        say(OK if brightest > 24 else ERR, "black tail",
            f"peak luma {brightest} in the last 0.45s")
        if not args.allow_freeze:
            moved = any(a != b for a, b in zip(tail, tail[1:]))
            say(OK if moved else ERR, "frozen end",
                "moving" if moved else "identical frames — reads as a crash, and Shorts loops into it")

    if args.sheet:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "motion-graphics" / "scripts"))
        try:
            import mg

            mg.contact_sheet(str(video), args.sheet)
            say(WARN, "sheet", f"{args.sheet} — OPEN IT. Nothing here judges the content")
        except Exception as exc:  # noqa: BLE001 - reported, never fatal
            say(WARN, "sheet", f"not written: {exc}")

    for level, name, detail in rows:
        print(f"[{level}] {name:<12} {detail}")
    print(f"\n{len(rows)} checks, {bad} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
