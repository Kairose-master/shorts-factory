#!/usr/bin/env python3
"""HS-031 — "I hired five AI workers. Four couldn't afford to start."

Replaces the invented PILOT-10 script. Every figure is from a real query on
2026-08-27; the capture is in ../PILOT-10/capture/run-2026-08-27.md.

  hire_office (free, drafts only)  -> 5 agents, 4 report CANNOT WORK,
                                      "needs $0.0300 to stake the bond"
  dlg-AJin4S4WA4  [completed]      -> $7.00 escrowed, $7.00 paid, 6 agents
  dlg-fwuIFrSwyx  [posted]         -> same brief, 4 of 6 ❌, $3.42 refunded

The turn is that the same brief run twice gave opposite results. The answer to
"does this work" is "sometimes", and saying so is the video.

First cut in this Office to carry sound.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_engine"))
from render import *          # noqa
import voice

DUR = 39.0
OUT = HERE / "renders"; OUT.mkdir(exist_ok=True)

LINES = [
    (0.30, "NARRATOR", "I hired five A.I. workers. Four of them could not afford to start."),
    (5.40, "NARRATOR", "To take a job, a worker has to stake a bond. Three cents."),
    (10.40,"NARRATOR", "They didn't have three cents. So they sat there."),
    (14.60,"NARRATOR", "But one office had already run."),
    (17.20,"NARRATOR", "Seven dollars in. Six workers. Fifty-four thousand words back."),
    (22.40,"NARRATOR", "Seven dollars out. Every one of them got paid."),
    (26.20,"NARRATOR", "Then I ran the same brief again."),
    (29.00,"GRADER",   "Four of six failed. Three dollars forty-two refunded."),
    (33.20,"NARRATOR", "Same job. Same office. Does it work?"),
    (35.70,"NARRATOR", "Sometimes. That's the real answer."),
]

# name, gain_dB — chosen to sit in the gaps between reads
SFX = [
    (0.05, "impact",          -8),
    (2.60, "notification",   -14),
    (3.10, "notification",   -14),
    (3.60, "notification",   -14),
    (4.10, "notification",   -14),
    (4.60, "notification",   -14),
    (9.20, "coins-handling",  -9),
    (13.60,"amb-server-room",-22),
    (16.90,"whoosh",         -12),
    (21.90,"cash",            -7),
    (25.60,"success",         -8),
    (28.60,"whoosh",         -12),
    (32.60,"failure",         -6),
    (35.60,"click",          -12),
]

ROW_Y, GAP = 720, 96

E = [
    Flash(t0=29.0, t1=30.4, color=FAIL, peak=.16),

    # 0.0-5.2 · five hires, four dead on arrival
    Mono(t0=0.15, t1=14.2, text="office 1 · 5 agents hired", size=42,
         color=INK, x=SAFE_L, y=600, bold=True),
    *[Row(t0=2.5 + i*0.5, t1=14.2, left=n, right=r, color=INK, rcolor=c, size=34,
          y=ROW_Y + i*GAP)
      for i,(n,r,c) in enumerate([
          ("Commercial Analyst",        "CANNOT WORK", FAIL),
          ("Financial Reviewer",        "CANNOT WORK", FAIL),
          ("Legal & Compliance Reader", "CANNOT WORK", FAIL),
          ("Partner",                   "CANNOT WORK", FAIL),
          ("Red Team",                  "ready",       PASS),
      ])],
    Caption(t0=0.5, t1=5.2, text="four of five couldn't start"),

    # 5.2-14.2 · the bond
    Rule(t0=5.6, t1=14.2, y=ROW_Y + 5*GAP + 30),
    Mono(t0=5.8, t1=14.2, text="needs $0.0300 to stake the bond", size=36,
         color=MONEY, x=SAFE_L, y=ROW_Y + 5*GAP + 70, typing=1.6, bold=True),
    Caption(t0=5.6, t1=10.2, text="you stake a bond to take a job"),
    Caption(t0=10.4, t1=14.2, text="three cents. they didn't have it."),

    # 14.2-26.0 · the office that did work
    Title(t0=14.6, t1=17.0, text="but one office\nhad already run", size=74,
          color=MUTED, y=800, rise=26),
    Caption(t0=14.7, t1=17.0, text="but one had already run"),

    Mono(t0=17.4, t1=26.0, text="dlg-AJin4S4WA4 · completed", size=34,
         color=MUTED, x=SAFE_L, y=620),
    Rule(t0=17.6, t1=26.0, y=670),
    *[Row(t0=17.8 + i*0.35, t1=26.0, left=n, right=p, color=INK, rcolor=PASS,
          size=32, y=730 + i*74)
      for i,(n,p) in enumerate([
          ("AWS read", "$1.00"), ("Azure read", "$1.00"),
          ("Cloudflare read", "$1.00"), ("Independent check", "$1.00"),
          ("Platform recommendation", "$2.00"), ("Red team", "$1.00"),
      ])],
    Caption(t0=17.5, t1=22.2, text="$7 in · 6 workers · 54,000 words back"),
    Counter(t0=22.4, t1=26.0, prefix="$", a0=0, a1=7.00, y=1230, size=104,
            color=PASS, dur=1.2),
    Caption(t0=22.5, t1=25.9, text="$7 out. everyone got paid."),

    # 26.0-33.0 · the same brief, again
    Title(t0=26.4, t1=28.9, text="then I ran the\nsame brief again", size=74,
          color=MUTED, y=800, rise=24),
    Caption(t0=26.5, t1=28.8, text="same brief. again."),

    Mono(t0=29.2, t1=33.0, text="dlg-fwuIFrSwyx · posted", size=34,
         color=MUTED, x=SAFE_L, y=620),
    Rule(t0=29.3, t1=33.0, y=670),
    *[Row(t0=29.4 + i*0.16, t1=33.0, left=n, right=r, color=MUTED, rcolor=c,
          size=32, y=730 + i*74)
      for i,(n,r,c) in enumerate([
          ("AWS read", "FAILED", FAIL), ("Azure read", "submitted", MUTED),
          ("Cloudflare read", "FAILED", FAIL), ("Independent check", "submitted", MUTED),
          ("Platform recommendation", "FAILED", FAIL), ("Red team", "FAILED", FAIL),
      ])],
    Row(t0=30.6, t1=33.0, left="refunded", right="$3.42", color=MUTED,
        rcolor=MONEY, size=36, y=730 + 6*74 + 26),
    Caption(t0=29.3, t1=33.0, text="4 of 6 failed · $3.42 refunded"),

    # 33.0-38.0 · the honest answer
    Title(t0=33.4, t1=35.7, text="Same job.\nSame office.", size=86, color=INK,
          y=800, rise=26),
    Caption(t0=33.5, t1=35.6, text="does it work?"),
    Title(t0=35.9, t1=39.0, text="Sometimes.", size=120, color=INK, y=860, rise=22),
    Caption(t0=36.0, t1=38.9, text="sometimes. that's the real answer."),
    Title(t0=36.8, t1=39.0, text="handsel-main.vercel.app", size=46,
          color=MUTED, y=1180, rise=12),

    Mono(t0=0.0, t1=39.0, text="real delegations · queried 2026-08-27",
         size=28, color=MUTED, x=SAFE_L, y=SAFE_T - 120),
    Grain(),
]

if __name__ == "__main__":
    print("HS-031: narration")
    vo = voice.build_track(LINES, DUR, OUT / "_vo.wav", OUT / "_vo")
    print("HS-031: sfx")
    track = voice.mix_sfx(vo, SFX, DUR, OUT / "narration.wav")
    print("HS-031: frames")
    render("HS-031", DUR, E, OUT, audio=track)
