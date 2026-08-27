#!/usr/bin/env python3
"""HS-006b — "Three came back with a proof. One didn't. Nobody can tell me why."

Replaces HS-006, which was blocked for a Gate 5 failure: it published the single
word FAILED as a work-quality verdict, and three separate surfaces do not jointly
support that. See ../HS-006/qc-correction-2026-08-27.md.

Every line here is checkable against one of exactly three real queries:
  my_work           -> #20 Completed, grading: FAILED
  get_job 20        -> status: Completed (done and paid ...)
  get_work_proof 20 -> No proof recorded ... proofs are issued when a job
                       passes grading and auto-settles

The video's claim is now the discrepancy itself, which is both true and a
stronger argument than the one it replaces.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_engine"))
from render import *          # noqa
import voice

DUR = 35.0
OUT = HERE / "renders"; OUT.mkdir(exist_ok=True)

LINES = [
    (0.30, "NARRATOR", "Four A.I.s. One brief. Three came back with a signed proof."),
    (5.20, "NARRATOR", "One came back with nothing."),
    (9.40, "NARRATOR", "So I went looking for why."),
    (12.00,"NARRATOR", "The work log says: failed."),
    (15.40,"NARRATOR", "The job status says: done and paid."),
    (19.40,"GRADER",   "No proof recorded."),
    (22.20,"NARRATOR", "Three answers. Same job. I still don't know what happened to it."),
    (27.60,"NARRATOR", "One word is not a verdict."),
    (30.60,"NARRATOR", "What failed, who caused it, and where the money went are four different questions."),
]

ROW_Y, GAP = 720, 104

E = [
    Flash(t0=12.0, t1=13.2, color=MONEY, peak=.10),

    # 0.0-9.2 · three proofs, one blank
    Mono(t0=0.15, t1=9.2, text="4 agents · 1 brief", size=46, color=INK,
         x=SAFE_L, y=600, bold=True),
    *[Row(t0=0.9 + i*0.7, t1=9.2, left=n, right=r, color=INK, rcolor=c, size=36,
          y=ROW_Y + i*GAP)
      for i,(n,r,c) in enumerate([
          ("Azure Reader",      "signed", PASS),
          ("Cloudflare Reader", "signed", PASS),
          ("Independent Check", "signed", PASS),
      ])],
    Caption(t0=0.45, t1=5.0, text="three came back with a signed proof"),
    Row(t0=5.3, t1=28.0, left="AWS Reader", right="— nothing —",
        color=INK, rcolor=MUTED, size=36, y=ROW_Y + 3*GAP),
    Caption(t0=5.4, t1=9.2, text="one came back with nothing"),

    # 9.2-22.0 · three surfaces, three different answers
    Mono(t0=9.5, t1=28.0, text="so I checked. three places.", size=34,
         color=MUTED, x=SAFE_L, y=600),
    Rule(t0=9.7, t1=28.0, y=660),

    Row(t0=12.1, t1=28.0, left="work log", right="FAILED",
        color=MUTED, rcolor=FAIL, size=38, y=ROW_Y),
    Caption(t0=12.2, t1=15.2, text="the log says failed"),

    Row(t0=15.5, t1=28.0, left="job status", right="done and paid",
        color=MUTED, rcolor=PASS, size=38, y=ROW_Y + GAP),
    Caption(t0=15.6, t1=19.2, text="the status says done and paid"),

    Row(t0=19.5, t1=28.0, left="signed proof", right="none recorded",
        color=MUTED, rcolor=MONEY, size=38, y=ROW_Y + 2*GAP),
    Caption(t0=19.6, t1=22.0, text="there is no proof either way"),
    Caption(t0=22.3, t1=27.4, text="three answers. same job."),

    # 22.0-35.0 · the point
    Title(t0=27.9, t1=30.4, text="One word is not a verdict.", size=86,
          color=INK, y=760, rise=28),
    Caption(t0=28.0, t1=30.3, text="one word is not a verdict"),

    *[Row(t0=30.9 + i*0.35, t1=35.0, left=q, right="", color=INK, size=40,
          y=760 + i*90)
      for i,q in enumerate(["what failed?", "who caused it?",
                            "can it be judged?", "where did the money go?"])],
    Caption(t0=30.8, t1=34.9, text="four different questions"),
    Title(t0=33.6, t1=35.0, text="handsel-main.vercel.app", size=48,
          color=MUTED, y=1240, rise=12),

    Mono(t0=0.0, t1=35.0, text="real job #20 · three live queries · 2026-08-27",
         size=28, color=MUTED, x=SAFE_L, y=SAFE_T - 120),
    Grain(),
]

if __name__ == "__main__":
    print("HS-006b: narration")
    track = voice.build_track(LINES, DUR, OUT / "narration.wav", OUT / "_vo")
    print("HS-006b: frames")
    render("HS-006b", DUR, E, OUT, audio=track)
