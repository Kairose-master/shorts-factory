#!/usr/bin/env python3
"""HS-034 — the company, running.

Same real run as HS-032 (dlg-AJin4S4WA4: $7.00 escrowed, $7.00 paid, six roles),
but shown as a floor rather than argued as a list. Work physically moves between
desks, screens flicker while a worker thinks, a status light turns green when it
finishes, and the treasury drains as everyone gets paid.

Narration is deliberately sparse. If the picture needs a sentence to explain what
just happened, the picture is wrong.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ENG = HERE.parent / "_engine"
sys.path.insert(0, str(ENG))
from render import *          # noqa
from floor import *           # noqa
import voice

DUR = 37.0
OUT = HERE / "renders"; OUT.mkdir(exist_ok=True)

LINES = [
    (0.30, "NARRATOR", "This is an A.I. company. Six workers, one question."),
    (5.00, "NARRATOR", "Four of them research at the same time."),
    (11.60,"NARRATOR", "Everything they find goes to one desk."),
    (16.40,"NARRATOR", "That desk writes the decision."),
    (20.60,"NARRATOR", "Then this one attacks it. Before I see it."),
    (26.00,"NARRATOR", "It passed."),
    (28.40,"NARRATOR", "So the company pays everybody."),
    (33.00,"NARRATOR", "Seven dollars. Nobody clocked in."),
]

SFX = [
    (0.05, "impact",        -10),
    (2.40, "notification",  -16), (2.72, "notification", -16),
    (3.04, "notification",  -16), (3.36, "notification", -16),
    (3.68, "notification",  -16), (4.00, "notification", -16),
    (5.20, "digital",       -15),
    (11.9, "whoosh",        -14),
    (16.6, "digital",       -14),
    (20.8, "warning",       -12),
    (25.9, "success",        -9),
    (28.7, "cash",           -7),
    (33.2, "click",         -13),
]

CL, CR = 285, 750
R1, R2, R3 = 700, 950, 1200
TREAS_Y = 500

D = {
    "aws":   Desk(t0=2.3, t1=37.0, label="AWS",        x=CL, y=R1, dim_until=2.5,
                  busy=(5.2, 11.4),  done_at=11.4),
    "azure": Desk(t0=2.6, t1=37.0, label="Azure",      x=CR, y=R1, dim_until=2.8,
                  busy=(5.4, 11.7),  done_at=11.7),
    "cf":    Desk(t0=2.9, t1=37.0, label="Cloudflare", x=CL, y=R2, dim_until=3.1,
                  busy=(5.6, 12.0),  done_at=12.0),
    "ind":   Desk(t0=3.2, t1=37.0, label="Independent",x=CR, y=R2, dim_until=3.4,
                  busy=(5.8, 12.3),  done_at=12.3),
    "arch":  Desk(t0=3.5, t1=37.0, label="Architect",  x=CL, y=R3, dim_until=3.7,
                  busy=(15.6, 20.2), done_at=20.2),
    "red":   Desk(t0=3.8, t1=37.0, label="Red team",   x=CR, y=R3, dim_until=4.0,
                  busy=(21.0, 25.6), done_at=25.6),
}
for k, pay in [("aws",29.1),("azure",29.4),("cf",29.7),("ind",30.0),
               ("arch",30.3),("red",30.6)]:
    D[k].paid_at = pay

ARCH_TOP = desk_edge(D["arch"], "top")
ARCH_R   = desk_edge(D["arch"], "right")
RED_L    = desk_edge(D["red"], "left")
TREAS    = (W / 2, TREAS_Y + 40)

def to_arch(src, bow):
    return desk_edge(D[src], "bottom"), ARCH_TOP, bow

E = [
    Floor(t0=0.6, t1=37.0),

    Treasury(t0=1.0, t1=37.0, x=W/2, y=TREAS_Y, total=7.00, steps=[
        (29.2, 6.00), (29.5, 5.00), (29.8, 4.00),
        (30.1, 3.00), (30.4, 1.00), (30.7, 0.00)]),

    # wires — the org chart, drawn once and then used
    *[Wire(t0=4.4 + i*0.12, t1=37.0, a=a, b=b, bow=bow)
      for i,(a,b,bow) in enumerate([
          to_arch("aws",  0.10), to_arch("azure", -0.14),
          to_arch("cf",   0.16), to_arch("ind",  -0.10)])],
    Wire(t0=19.9, t1=37.0, a=ARCH_R, b=RED_L, bow=-0.30),

    *D.values(),

    Caption(t0=0.5, t1=4.9, text="an AI company · six workers"),
    Caption(t0=5.2, t1=11.4, text="four research at the same time"),

    # 11.4-15.6 · findings converge on one desk
    *[Packet(t0=s, t1=s+1.5, a=a, b=b, bow=bow, color=ACCENT, size=17)
      for s,(a,b,bow) in zip([11.5,11.8,12.1,12.4],
                             [to_arch("aws",0.10), to_arch("azure",-0.14),
                              to_arch("cf",0.16),  to_arch("ind",-0.10)])],
    Pulse(t0=13.9, t1=14.9, x=ARCH_TOP[0], y=ARCH_TOP[1], color=ACCENT, r1=140),
    Caption(t0=11.7, t1=16.2, text="everything goes to one desk"),

    # 15.6-20.2 · the decision gets written
    Caption(t0=16.5, t1=20.4, text="it writes the decision"),
    Pulse(t0=20.0, t1=21.0, x=D["arch"].x, y=D["arch"].y, color=PASS, r1=170),

    # 20.2-25.6 · red team attacks it
    Packet(t0=20.4, t1=21.4, a=ARCH_R, b=RED_L, bow=-0.30, color=FAIL, size=18),
    Caption(t0=20.8, t1=25.7, text="then this one attacks it"),
    Mono(t0=21.4, t1=25.6, text="challenging the decision", size=30,
         color=FAIL, x=SAFE_L, y=1330),

    # 25.6-28.4 · verdict
    Pulse(t0=25.7, t1=27.0, x=D["red"].x, y=D["red"].y, color=PASS, r1=210),
    Title(t0=25.9, t1=28.3, text="PASSED", size=96, color=PASS, y=1340, rise=18),
    Caption(t0=26.0, t1=28.2, text="it passed"),

    # 28.4-33.0 · payday
    *[Coin(t0=s, t1=s+0.9, a=TREAS, b=(D[k].x, D[k].y), bow=0.10 if D[k].x < W/2 else -0.10)
      for s,k in [(28.8,"aws"),(29.1,"azure"),(29.4,"cf"),
                  (29.7,"ind"),(30.0,"arch"),(30.3,"red")]],
    Caption(t0=28.7, t1=32.8, text="the company pays everybody"),

    # 33.0-37.0 · land it
    # The end card stacks into the caption band if it is not watched: $7.00 at
    # 140pt runs to ~1470 and captions live at 1500. Reuse the caption slot for
    # the URL instead of stacking a third line under it.
    Title(t0=33.2, t1=37.0, text="$7.00", size=124, color=MONEY, y=1310, rise=20),
    Caption(t0=33.3, t1=35.3, text="nobody clocked in."),
    Caption(t0=35.5, t1=36.9, text="handsel-main.vercel.app", color=MUTED, size=54),
    Grain(),
]

if __name__ == "__main__":
    print("HS-034: narration")
    vo = voice.build_track(LINES, DUR, OUT / "_vo.wav", OUT / "_vo")
    print("HS-034: sfx")
    track = voice.mix_sfx(vo, SFX, DUR, OUT / "narration.wav")
    print("HS-034: frames")
    render("HS-034", DUR, E, OUT, audio=track)
