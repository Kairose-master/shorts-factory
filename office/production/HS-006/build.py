#!/usr/bin/env python3
"""HS-006 — "I paid four AIs to answer the same question. One of them failed."

Pillar C. 35s. Arm B of EXP-001.

Every verdict on screen is a real row from this account's my_work, captured
2026-08-27 (see _source/captured-2026-08-27.md). Four agents were given the same
brief; three passed and one failed. Nothing here is staged — which matters,
because a staged failure would prove nothing about a grader.

The FAIL is held past comfort. Every demo on the internet cuts away from red.
Not cutting away is the entire differentiator.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_engine"))
from render import *          # noqa
import voice

DUR = 35.0
OUT = HERE / "renders"; OUT.mkdir(exist_ok=True)

LINES = [
    (0.30, "NARRATOR", "I paid four A.I.s to answer the same question."),
    (3.60, "NARRATOR", "Same brief. Same grader. None of them graded themselves."),
    (8.40, "NARRATOR", "Three passed."),
    (13.60,"GRADER",   "Failed."),
    (16.20,"NARRATOR", "That one is real. I didn't stage it, and I didn't catch it."),
    (21.00,"NARRATOR", "I never read the work."),
    (23.40,"NARRATOR", "The verdict came from something that wasn't the worker, and wasn't me."),
    (28.60,"NARRATOR", "Every A.I. demo shows you the part that works."),
    (32.00,"NARRATOR", "This is the part that has to."),
]

BRIEF = "a webhook receiver · 5M requests/month"
ROW_Y = 780
GAP   = 118

E = [
    # Background wash on the FAIL. Listed first so it sits BEHIND the rows —
    # the three passes must stay readable through it, or the comparison the
    # video exists to make vanishes at its own climax.
    Flash(t0=13.5, t1=14.6, color=FAIL, peak=.20),

    # 0.0-3.4 · the setup
    Mono(t0=0.15, t1=8.2, text="4 agents · 1 brief", size=46, color=INK,
         x=SAFE_L, y=640, bold=True),
    Mono(t0=1.1, t1=8.2, text=BRIEF, size=30, color=MUTED, x=SAFE_L, y=720),
    Caption(t0=0.45, t1=3.4, text="I paid four AIs the same question"),

    # 3.4-8.2 · names appear, no verdicts yet
    *[Row(t0=3.7 + i * 0.28, t1=28.4, left=n, right="", color=INK, size=38,
          y=ROW_Y + 60 + i * GAP)
      for i, n in enumerate(["AWS Reader", "Azure Reader",
                             "Cloudflare Reader", "Independent Check"])],
    Caption(t0=3.7, t1=8.2, text="same brief · same grader"),

    # 8.2-13.4 · three pass
    Row(t0=8.6,  t1=28.4, left="Azure Reader",      right="passed",
        color=INK, rcolor=PASS, size=38, y=ROW_Y + 60 + 1 * GAP, slide=0),
    Row(t0=9.6,  t1=28.4, left="Cloudflare Reader", right="passed",
        color=INK, rcolor=PASS, size=38, y=ROW_Y + 60 + 2 * GAP, slide=0),
    Row(t0=10.6, t1=28.4, left="Independent Check", right="passed",
        color=INK, rcolor=PASS, size=38, y=ROW_Y + 60 + 3 * GAP, slide=0),
    Caption(t0=8.6, t1=13.2, text="three passed"),

    # 13.4-21.0 · the one that didn't. Held.
    Row(t0=13.6, t1=28.4, left="AWS Reader", right="FAILED",
        color=INK, rcolor=FAIL, size=38, y=ROW_Y + 60, slide=0),
    Caption(t0=13.7, t1=16.0, text="one did not", color=FAIL),
    Caption(t0=16.3, t1=20.8, text="real verdict. not staged."),

    # 21.0-28.4 · nobody on my side looked
    Rule(t0=21.1, t1=28.4, y=ROW_Y + 60 + 4 * GAP + 40),
    Mono(t0=21.3, t1=28.4, text="reviewed by me:  never", size=34,
         color=MUTED, x=SAFE_L, y=ROW_Y + 60 + 4 * GAP + 80),
    Caption(t0=21.2, t1=23.2, text="I never read the work"),
    Caption(t0=23.5, t1=28.3, text="the verdict came from neither of us"),

    # 28.4-35.0 · the line
    Title(t0=28.8, t1=32.0, text="Every AI demo shows you\nthe part that works.",
          size=76, color=MUTED, y=780, rise=28),
    Caption(t0=28.9, t1=31.8, text="every demo shows the part that works"),
    Title(t0=32.2, t1=35.0, text="This is the part\nthat has to.", size=88,
          color=INK, y=820, rise=26),
    Caption(t0=32.3, t1=34.9, text="this is the part that has to"),
    Title(t0=33.4, t1=35.0, text="handsel-main.vercel.app", size=48,
          color=MUTED, y=1160, rise=12),

    Mono(t0=0.0, t1=35.0, text="real graded verdicts · captured 2026-08-27",
         size=28, color=MUTED, x=SAFE_L, y=SAFE_T - 120),
    Grain(),
]

if __name__ == "__main__":
    print("HS-006: narration")
    track = voice.build_track(LINES, DUR, OUT / "narration.wav", OUT / "_vo")
    print("HS-006: frames")
    render("HS-006", DUR, E, OUT, audio=track)
