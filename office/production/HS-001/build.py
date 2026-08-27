#!/usr/bin/env python3
"""HS-001 — "I gave an AI $5 and told it to hire someone"

Pillar A. 30s. Every string on screen is copied verbatim from a real
plan_delegation call (dlg-S711y4gs3O, 2026-08-27) — see
office/production/_source/captured-2026-08-27.md. That call is free and escrows
nothing, so the video never depicts money moving, and says so on screen.

The turn at 0:12 is that the planner paid a second agent to check the first
one's work without being asked to. The product's own thesis, unprompted, in its
own output.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_engine"))
from render import *          # noqa
import voice

DUR = 30.0
OUT = HERE / "renders"; OUT.mkdir(exist_ok=True)

LINES = [
    (0.30, "NARRATOR", "I gave an A.I. five dollars and told it to hire someone."),
    (4.10, "NARRATOR", "It didn't do the work."),
    (5.90, "NARRATOR", "It wrote a plan, and put a price on every piece."),
    (9.60, "NARRATOR", "Four dollars to write it."),
    (12.10,"NARRATOR", "One dollar to a second agent, to check the first one's work."),
    (16.60,"NARRATOR", "Nobody told it to do that."),
    (19.20,"NARRATOR", "And it wrote down what done means, before anyone started."),
    (24.30,"NARRATOR", "Five dollars. Two workers."),
    (26.80,"NARRATOR", "One of them exists only to not trust the other."),
]

# Verbatim from the real acceptance criteria on subtask 2.
CRIT = "Verdict is clearly APPROVE or REVISE"

E = [
    # 0.0-4.0 · the ask, typed
    Mono(t0=0.15, t1=4.3, text="> hire someone to write this. budget $5",
         size=36, color=INK, x=SAFE_L, y=560, typing=2.0, bold=True),
    Mono(t0=4.3, t1=24.0, text="> hire someone to write this. budget $5",
         size=36, color=MUTED, x=SAFE_L, y=560),
    Caption(t0=0.45, t1=4.0, text="I gave an AI $5 and told it to hire someone"),

    # 4.0-9.4 · it planned instead
    Mono(t0=4.4, t1=9.4, text="planning...", size=40, color=MUTED,
         x=SAFE_L, y=700),
    Caption(t0=4.2, t1=5.8, text="it didn't do the work"),
    Caption(t0=5.9, t1=9.4, text="it priced the work"),

    # 9.4-16.4 · the real plan, one row at a time
    Rule(t0=9.5, t1=24.0, y=730),
    Mono(t0=9.5, t1=24.0, text="delegation plan · total $5.00", size=34,
         color=MUTED, x=SAFE_L, y=660),
    Row(t0=9.8, t1=24.0, y=800, size=38, color=INK, rcolor=MONEY,
        left="write the explainer", right="$4.00"),
    Row(t0=12.3, t1=24.0, y=915, size=38, color=INK, rcolor=MONEY,
        left="review the explainer", right="$1.00"),
    Mono(t0=13.4, t1=24.0, text="  → a different agent. checks the first one.",
         size=32, color=ACCENT, x=SAFE_L, y=985),
    Caption(t0=9.8, t1=12.1, text="$4.00 to write it"),
    Caption(t0=12.3, t1=16.4, text="$1.00 to check the writer"),
    Caption(t0=16.6, t1=19.0, text="nobody told it to do that"),

    # 19.0-24.0 · acceptance criteria, before anyone starts
    Rule(t0=19.3, t1=24.0, y=1100),
    Mono(t0=19.4, t1=24.0, text="accept when:", size=32, color=MUTED,
         x=SAFE_L, y=1145),
    Mono(t0=19.9, t1=24.0, text=CRIT, size=36, color=PASS,
         x=SAFE_L, y=1205, typing=1.6, bold=True),
    Caption(t0=19.4, t1=24.0, text="\"done\" was defined before anyone started"),

    # 24.0-30.0 · the line
    Title(t0=24.4, t1=27.0, text="$5.00", size=150, color=MONEY, y=760, rise=24),
    Title(t0=25.3, t1=27.0, text="two workers", size=72, color=MUTED, y=960, rise=18),
    Caption(t0=24.5, t1=26.7, text="five dollars. two workers."),
    Title(t0=27.2, t1=30.0, text="One of them exists only\nto not trust the other.",
          size=76, color=INK, y=820, rise=30),
    Caption(t0=27.3, t1=29.9, text="one exists only to not trust the other"),
    Title(t0=28.6, t1=30.0, text="handsel-main.vercel.app", size=48,
          color=MUTED, y=1180, rise=12),

    # Honesty marker, on screen for the whole run: this is a real planner
    # output, and it is only a plan. Nothing was escrowed and the video must
    # never be readable as showing money move.
    Mono(t0=0.0, t1=30.0, text="real output · plan only · nothing escrowed",
         size=28, color=MUTED, x=SAFE_L, y=SAFE_T - 120),
    Grain(),
]

if __name__ == "__main__":
    print("HS-001: narration")
    track = voice.build_track(LINES, DUR, OUT / "narration.wav", OUT / "_vo")
    print("HS-001: frames")
    render("HS-001", DUR, E, OUT, audio=track)
