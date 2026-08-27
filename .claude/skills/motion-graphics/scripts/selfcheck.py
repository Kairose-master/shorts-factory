#!/usr/bin/env python3
"""Prove the motion-graphics toolchain works on this machine.

Renders a 3-second card, a contact sheet, and prints what it used. Run this
before storyboarding anything: it fails in seconds instead of at minute forty
of a render.

    python3 .claude/skills/motion-graphics/scripts/selfcheck.py --out /tmp/mg
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/mg-selfcheck")
    args = ap.parse_args()

    missing = []
    for mod in ("PIL", "imageio_ffmpeg"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        print("MISSING:", ", ".join(missing))
        print("fix: pip install pillow imageio-ffmpeg")
        return 1

    import mg

    for family, path in mg.FONT_FILES.items():
        if not Path(path).is_file():
            print(f"MISSING FONT {family}: {path}")
            return 1

    out = Path(args.out)
    video = out / "selfcheck.mp4"

    def frame(t, i):
        im, d = mg.canvas()
        p = mg.seg(t, 0.15, 0.5)
        y = 900 - int(40 * (1 - p))
        d.text((mg.SAFE["l"], y), "motion-graphics", font=mg.font("sans-bold", 96),
               fill=mg.mix(mg.PAPER, mg.INK, p))
        mg.rule(d, y + 130, mg.SAFE["l"], mg.SAFE["r"], mg.ACCENT, 6, mg.seg(t, 0.5, 0.6))
        d.text((mg.SAFE["l"], y + 170),
               mg.counter(0, 100, mg.seg(t, 0.8, 1.4), "{:>3.0f}% checked"),
               font=mg.font("mono", 52), fill=mg.MUTED)
        if mg.caret(t):
            d.rectangle((mg.SAFE["l"], y + 260, mg.SAFE["l"] + 26, y + 302), fill=mg.INK)
        return im

    mg.render(frame, 3.0, video, progress_every=0)
    sheet = mg.contact_sheet(str(video), str(out / "selfcheck-sheet.jpg"), cols=3, rows=2)

    print("\nOK — this machine can render motion graphics.")
    print(f"  ffmpeg  {mg.ffmpeg_exe()}")
    print(f"  video   {video}")
    print(f"  sheet   {sheet}   <- open it, do not trust the exit code alone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
