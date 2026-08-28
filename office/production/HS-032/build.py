#!/usr/bin/env python3
"""HS-032 — "I hired an entire company for $7."

The promotional cut. Written for someone who has never heard of Handsel.

Rules this one follows that HS-031 broke:
  * No protocol vocabulary. No escrow, bond, delegation id, USDC, on-chain,
    verification, MCP. A stranger must not need a glossary.
  * The product narrative leads: build an AI company, give it money, watch it
    do business. The Office is the subject, not a mechanism.
  * It ends on the payoff, not on a caveat.

Source: dlg-AJin4S4WA4, a real completed run — $7.00 escrowed, $7.00 paid, six
roles, ~54,000 words assembled. Captured in ../PILOT-10/capture/run-2026-08-27.md.
The task itself was a technical infrastructure question; the video does not
explain it, because the viewer does not need to understand the question to
understand that six specialists answered it and were paid.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_engine"))
from render import *          # noqa
import voice

DUR = 34.0
OUT = HERE / "renders"; OUT.mkdir(exist_ok=True)

LINES = [
    (0.30, "NARRATOR", "Yesterday I hired an entire company."),
    (3.10, "NARRATOR", "It cost seven dollars."),
    (5.40, "NARRATOR", "Not one A.I. Six of them, with different jobs."),
    (9.60, "NARRATOR", "Three of them went and researched at the same time."),
    (14.20,"NARRATOR", "A fourth read all three, and wrote the decision."),
    (18.80,"NARRATOR", "Then a fifth one attacked it. Before I ever saw it."),
    (24.00,"NARRATOR", "Fifty-four thousand words came back."),
    (27.20,"NARRATOR", "Every worker got paid. Seven dollars, all in."),
    (31.20,"NARRATOR", "That's a company. It cost less than lunch."),
]

SFX = [
    (0.05, "impact",        -9),
    (5.60, "notification", -15), (5.95, "notification", -15),
    (6.30, "notification", -15), (6.65, "notification", -15),
    (7.00, "notification", -15), (7.35, "notification", -15),
    (9.80, "whoosh",       -13),
    (14.40,"digital",      -13),
    (19.00,"warning",      -11),
    (23.90,"transition",   -13),
    (27.40,"cash",          -6),
    (30.90,"success",       -8),
]

# 2 x 3 grid of role cards — "a company" reads as a floor plan, not a list.
CX = [305, 745]
CY = [720, 950, 1180]
CARDS = [
    ("AWS",         0, 0), ("Azure",        1, 0),
    ("Cloudflare",  0, 1), ("Independent",  1, 1),
    ("Architect",   0, 2), ("Red team",     1, 2),
]
def card(i, t0, t1, color=INK, size=40):
    label, cx, cy = CARDS[i]
    return Box(t0=t0, t1=t1, label=label, x=CX[cx], y=CY[cy],
               w=390, h=170, color=color, size=size)

E = [
    # 0.0-5.2 · the claim
    Title(t0=0.4, t1=3.0, text="I hired an entire company.", size=88,
          color=INK, y=820, rise=30),
    Counter(t0=3.2, t1=5.2, prefix="$", a0=0, a1=7.00, y=800, size=170,
            color=MONEY, dur=0.9),
    Caption(t0=0.5, t1=3.0, text="I hired an entire company"),
    Caption(t0=3.2, t1=5.2, text="it cost seven dollars"),

    # 5.2-9.4 · the floor fills
    Mono(t0=5.5, t1=23.6, text="one company · six jobs", size=36,
         color=MUTED, x=SAFE_L, y=600),
    *[card(i, 5.7 + i*0.35, 23.6) for i in range(6)],
    Caption(t0=5.6, t1=9.4, text="not one AI. six, with different jobs."),

    # 9.4-14.0 · three research in parallel
    *[card(i, 9.8, 14.0, color=ACCENT, size=42) for i in (0, 1, 2)],
    Caption(t0=9.8, t1=14.0, text="three researched at the same time"),

    # 14.0-18.6 · the fourth synthesises
    card(4, 14.4, 18.6, color=PASS, size=42),
    Arrow(t0=14.7, t1=18.6, p0=(CX[0], CY[1] + 95), p1=(CX[0], CY[2] - 95),
          color=PASS, grow=.6, width=5),
    Arrow(t0=14.9, t1=18.6, p0=(CX[1], CY[1] + 95), p1=(CX[0] + 180, CY[2] - 60),
          color=PASS, grow=.7, width=5),
    Caption(t0=14.4, t1=18.6, text="a fourth read all three and decided"),

    # 18.6-23.6 · the fifth attacks it
    card(5, 19.0, 23.6, color=FAIL, size=42),
    Arrow(t0=19.4, t1=23.6, p0=(CX[1] - 180, CY[2]), p1=(CX[0] + 180, CY[2]),
          color=FAIL, grow=.5, width=6),
    Mono(t0=20.0, t1=23.6, text="argues with the decision", size=32,
         color=FAIL, x=SAFE_L, y=CY[2] + 150),
    Caption(t0=19.0, t1=23.6, text="a fifth one attacked it. before I saw it."),

    # 23.6-31.0 · the payoff
    Title(t0=24.1, t1=27.0, text="54,000 words", size=112, color=INK,
          y=780, rise=26),
    Mono(t0=25.0, t1=27.0, text="came back finished", size=38, color=MUTED,
         x=SAFE_L, y=980),
    Caption(t0=24.2, t1=27.0, text="54,000 words came back"),

    *[Row(t0=27.5 + i*0.16, t1=31.0, left=n, right=p, color=INK, rcolor=PASS,
          size=32, y=760 + i*72)
      for i,(n,p) in enumerate([
          ("AWS", "$1.00"), ("Azure", "$1.00"), ("Cloudflare", "$1.00"),
          ("Independent", "$1.00"), ("Architect", "$2.00"), ("Red team", "$1.00"),
      ])],
    Counter(t0=28.6, t1=31.0, prefix="$", a0=0, a1=7.00, y=1230, size=110,
            color=MONEY, dur=1.0),
    Caption(t0=27.4, t1=31.0, text="every worker got paid · $7 all in"),

    # 31.0-34.0 · land it
    Title(t0=31.4, t1=34.0, text="That's a company.", size=94, color=INK,
          y=830, rise=24),
    Caption(t0=31.5, t1=33.9, text="it cost less than lunch"),
    Title(t0=32.5, t1=34.0, text="handsel-main.vercel.app", size=50,
          color=MUTED, y=1120, rise=12),
    Grain(),
]

if __name__ == "__main__":
    print("HS-032: narration")
    vo = voice.build_track(LINES, DUR, OUT / "_vo.wav", OUT / "_vo")
    print("HS-032: sfx")
    track = voice.mix_sfx(vo, SFX, DUR, OUT / "narration.wav")
    print("HS-032: frames")
    render("HS-032", DUR, E, OUT, audio=track)
