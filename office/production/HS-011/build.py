#!/usr/bin/env python3
"""HS-011 — "An AI grading its own homework is not a reputation"

Pillar E. 35s. No product footage, no UI, no generated imagery: a video arguing
for verifiable process should not be made of unverifiable pictures. One diagram
that transforms, so nothing is ever replaced by a cut.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_engine"))
from render import *          # noqa
import voice

DUR = 35.0
OUT = HERE / "renders"; OUT.mkdir(exist_ok=True)

LINES = [
    (0.35, "NARRATOR", "This A.I. says it did a great job. It's also the one that graded it."),
    (5.4,  "NARRATOR", "So the score means nothing. It's a claim about a claim."),
    (9.6,  "NARRATOR", "An A.I. that is confidently wrong looks exactly like one that is right."),
    (14.6, "NARRATOR", "Which is why you still read every output yourself."),
    (18.4, "NARRATOR", "Unless the grading isn't done by the worker."),
    (22.6, "GRADER",   "The answer is generated with the problem. The solver never sees it."),
    (28.0, "NARRATOR", "Now the score is worth something."),
    (31.2, "NARRATOR", "It was never yours to give."),
]

CX, CY = 540, 780
LX, RX = 300, 770      # far enough apart that the arrow between them reads

E = [
    # 0.0-5.2 · the self-grading loop
    Box(t0=0.0, t1=17.6, label="WORKER", x=CX, y=CY, w=430, h=210,
        color=INK, move_to=(LX, CY), move_at=17.0, move_dur=1.1),
    SelfLoop(t0=0.9, t1=14.5, cx=CX, cy=CY, rw=330, rh=250, color=FAIL,
             label="grades itself", grow=1.5),
    Caption(t0=0.5, t1=5.2, text="it graded itself"),

    # 5.2-9.4 · a claim about a claim
    Title(t0=5.6, t1=9.4, text="98 / 100", size=112, color=PASS, y=1090, rise=26),
    Mono(t0=6.6, t1=9.4, text="reported by: WORKER", size=38, color=MUTED,
         x=SAFE_L + 40, y=1250),
    Caption(t0=5.6, t1=9.4, text="a claim about a claim"),

    # 9.4-14.4 · the aphorism, over the held diagram
    Title(t0=9.9, t1=14.3, text="Confidently wrong looks exactly like right.",
          size=82, color=INK, y=1050, rise=34),
    Caption(t0=10.1, t1=14.3, text="you cannot tell them apart"),

    # 14.4-17.6 · so you check all of it
    *[Row(t0=14.6 + i * 0.16, t1=17.6,
          left=f"output {i+1:03d}", right="you check it",
          rcolor=MUTED, color=DIM if i % 2 else MUTED, size=32,
          y=1040 + i * 44) for i in range(9)],
    Caption(t0=14.8, t1=17.6, text="so you check all of it. forever."),

    # 17.6-22.4 · the grader detaches
    Box(t0=17.9, t1=35.0, label="GRADER", x=RX, y=CY, w=340, h=210, color=ACCENT),
    Arrow(t0=18.6, t1=35.0, p0=(LX + 185, CY), p1=(RX - 190, CY),
          color=MUTED, grow=.7),
    Box(t0=17.7, t1=35.0, label="WORKER", x=LX, y=CY, w=340, h=210, color=INK, grow=0),
    Caption(t0=18.5, t1=22.4, text="move the grading out"),

    # 22.4-27.8 · the hidden answer
    Box(t0=22.8, t1=35.0, label="ANSWER", x=RX, y=CY + 340, w=330, h=170,
        color=MONEY, dash=True, size=40),
    Arrow(t0=23.4, t1=35.0, p0=(RX, CY + 250), p1=(RX, CY + 165),
          color=MONEY, grow=.5, width=5),
    Mono(t0=24.4, t1=27.8, text="solver never sees this", size=34, color=MONEY,
         x=SAFE_L, y=CY + 480),
    Caption(t0=23.0, t1=27.8, text="the answer exists before the work does"),

    # 27.8-35.0 · the verdict is worth something
    Title(t0=28.2, t1=32.2, text="PASS", size=132, color=PASS, y=1200, rise=22),
    Mono(t0=29.2, t1=32.2, text="signed · verifiable · not self-reported",
         size=32, color=MUTED, x=SAFE_L, y=1370),
    Caption(t0=28.4, t1=31.6, text="now the score means something"),
    Caption(t0=31.7, t1=34.9, text="it was never yours to give"),
    Title(t0=32.6, t1=35.0, text="handsel-main.vercel.app", size=50,
          color=MUTED, y=1230, rise=14),
    Grain(),
]

if __name__ == "__main__":
    print("HS-011: narration")
    track = voice.build_track(LINES, DUR, OUT / "narration.wav", OUT / "_vo")
    print("HS-011: frames")
    render("HS-011", DUR, E, OUT, audio=track)
