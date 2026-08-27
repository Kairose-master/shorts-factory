#!/usr/bin/env python3
"""「The Bill」 — a zero-credit motion graphics Short about what one-prompt video costs.

Reads projects/the-bill/plan.json (scene starts derived from measured narration,
with TTS word boundaries) and writes silent.mp4. Every reveal is anchored to the
word it belongs to, taken from plan["scenes"][i]["words"].

    python3 projects/the-bill/render.py [--out silent.mp4] [--cpu-seconds N]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / ".claude" / "skills" / "motion-graphics" / "scripts"))

from PIL import Image, ImageDraw  # noqa: E402

import mg  # noqa: E402

# --- brand: two colours and one accent; the accent only ever marks money -----
mg.PAPER = (243, 239, 230)
mg.INK = (20, 20, 22)
mg.MUTED = (122, 116, 108)
mg.ACCENT = (198, 58, 46)
PAPER, INK, MUTED, ACCENT = mg.PAPER, mg.INK, mg.MUTED, mg.ACCENT

L, R = mg.SAFE["l"], mg.SAFE["r"]
COL = R - L

PLAN = json.loads((ROOT / "plan.json").read_text(encoding="utf-8"))
SCENES = {s["id"]: s for s in PLAN["scenes"]}
TOTAL = PLAN["duration"]
CPU_SECONDS = None  # set from --cpu-seconds; None prints an em dash


# --------------------------------------------------------------------------
def at(sid, word_index):
    """Absolute time of a word in a scene, from the TTS boundaries."""
    s = SCENES[sid]
    ws = s["words"]
    i = min(word_index, len(ws) - 1)
    return s["start"] + ws[i]["t"]


def fade(d, xy, text, fnt, p, base=INK, align="left", right=R, bg=PAPER):
    """Fade a single line in against the paper, so contrast is exact mid-fade."""
    if p <= 0:
        return
    col = mg.mix(bg, base, p)
    x, y = xy
    if align == "center":
        x = x + (right - x - d.textlength(text, font=fnt)) / 2
    elif align == "right":
        x = right - d.textlength(text, font=fnt)
    d.text((x, y), text, font=fnt, fill=col)


def rise(d, xy, text, fnt, p, base=INK, dist=34, align="left", right=R):
    x, y = xy
    fade(d, (x, y + int(dist * (1 - p))), text, fnt, p, base, align, right)


def pop(im, cx, y, text, fnt, fill, p):
    """One scale-pop per video. This is it."""
    if p <= 0:
        return
    tmp = Image.new("RGBA", (mg.W, int(fnt.size * 1.6)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    w = td.textlength(text, font=fnt)
    td.text(((mg.W - w) / 2, 0), text, font=fnt, fill=(*fill, 255))
    s = 0.90 + 0.10 * mg.ease_out_back(p)
    a = int(255 * mg.ease_out(min(1.0, p * 2)))
    sc = tmp.resize((int(mg.W * s), int(tmp.height * s)), Image.LANCZOS)
    sc.putalpha(sc.getchannel("A").point(lambda v: v * a // 255))
    im.paste(sc, (int(cx - sc.width / 2), int(y)), sc)


def chrome(d, t, i, n):
    """Top telemetry and the running credit meter. The tool, visibly working."""
    f = mg.font("mono", 30)
    d.text((L, 150), "render.py  ·  the-bill", font=f, fill=MUTED)
    d.text((R - d.textlength(f"frame {i:04d}/{n:04d}", font=f), 150),
           f"frame {i:04d}/{n:04d}", font=f, fill=MUTED)
    d.line([(L, 208), (R, 208)], fill=mg.mix(PAPER, MUTED, 0.35), width=2)
    mg.rule(d, 208, L, R, INK, 4, t / TOTAL)
    d.text((L, 232), f"{t:05.2f}s / {TOTAL:05.2f}s", font=mg.font("mono", 26), fill=MUTED)

    d.text((L, 1452), "CREDITS USED", font=mg.font("mono", 30), fill=MUTED)
    d.text((L + 250, 1424), "0", font=mg.font("sans-bold", 62), fill=ACCENT)
    d.text((L + 300, 1452), "· and that is checkable", font=mg.font("mono", 30), fill=MUTED)


def caret(d, x, y, t):
    if mg.caret(t, 0.6):
        d.rectangle((x, y, x + 30, y + 58), fill=INK)


# --------------------------------------------------------------------------
def s1(d, im, t, tl):
    rise(d, (L, 470), "Python and ffmpeg", mg.font("sans", 54), mg.seg(t, at("s1", 0), 0.4), MUTED)
    f = mg.font("sans-bold", 78)
    lines = mg.wrap(d, "drew every frame of this video.", f, COL)
    for k, ln in enumerate(lines):
        rise(d, (L, 552 + k * 96), ln, f, mg.seg(t, at("s1", 3) + k * 0.14, 0.4))
    pop(im, mg.W / 2, 830, "ZERO", mg.font("sans-bold", 176), ACCENT, mg.seg(t, at("s1", 9), 0.5, mg.linear))
    pop(im, mg.W / 2, 1010, "CREDITS", mg.font("sans-bold", 176), ACCENT, mg.seg(t, at("s1", 9) + 0.12, 0.5, mg.linear))
    mg.rule(d, 1230, L, R, INK, 3, mg.seg(t, at("s1", 11), 0.5))
    rise(d, (L, 1262), "the part nobody shows you", mg.font("sans", 48),
         mg.seg(t, at("s1", 12), 0.4), MUTED)


def s2(d, im, t, tl):
    fh = mg.font("sans-bold", 58)
    for k, ln in enumerate(mg.wrap(d, "The hooks that beat their own channels", fh, COL)):
        rise(d, (L, 420 + k * 74), ln, fh, mg.seg(t, at("s2", 0) + k * 0.12, 0.4))
    rise(d, (L, 574), "16 outlier openings · Shorts + TikTok · 2026-08-27",
         mg.font("mono", 32), mg.seg(t, at("s2", 5), 0.4), MUTED)

    dim = mg.seg(t, at("s2", 10), 0.5)          # "Not one mentions cost"
    cell, gap, top = 105, 20, 650
    gw = 4 * cell + 3 * gap
    x0 = (mg.W - gw) / 2
    for k in range(16):
        p = mg.seg(t, at("s2", 4) + k * 0.055, 0.35)
        if p <= 0:
            continue
        cx = x0 + (k % 4) * (cell + gap)
        cy = top + (k // 4) * (cell + gap)
        col = mg.mix(mg.mix(PAPER, INK, p), mg.mix(PAPER, MUTED, 0.5), dim)
        h = int(cell * mg.ease_out(p))
        d.rounded_rectangle((cx, cy + cell - h, cx + cell, cy + cell),
                            radius=min(10, max(1, h // 3)), fill=col)

    if dim > 0:
        fade(d, (L, 1150 - int(24 * (1 - dim))), "0 / 16", mg.font("sans-bold", 120),
             dim, ACCENT, "center")
        fade(d, (L, 1300), "mention what it costs", mg.font("sans", 46),
             mg.seg(t, at("s2", 12), 0.4), INK, "center")


def s3(d, im, t, tl):
    rise(d, (L, 440), "Their comment sections do.", mg.font("sans", 50),
         mg.seg(t, at("s3", 0), 0.4), MUTED)

    p = mg.seg(t, at("s3", 4), 0.45)            # "Quote:"
    if p > 0:
        f = mg.font("sans-bold", 62)
        quote = "They always “forget” to mention the part about the COST of CREDITS."
        lines = mg.wrap(d, quote, f, COL - 60)
        box_h = len(lines) * int(f.size * 1.3) + 90
        y0 = 620
        d.rectangle((L, y0, L + 10, y0 + box_h), fill=mg.mix(PAPER, ACCENT, p))
        for k, ln in enumerate(lines):
            fade(d, (L + 52, y0 + 44 + k * int(f.size * 1.3)), ln, f,
                 mg.seg(t, at("s3", 4) + 0.1 + k * 0.1, 0.4))
        fade(d, (L + 52, y0 + box_h + 24), "— YouTube comment, AI-tools Shorts",
             mg.font("mono", 32), mg.seg(t, at("s3", 9), 0.4), MUTED)
    caret(d, L, 1330, t)


def s4(d, im, t, tl):
    steps = [
        ("the video", "20.59× — the strongest hook in the set", at("s4", 1), INK),
        ("the model", "credited on screen", at("s4", 5), INK),
        ("a paid generator", "billed per generation", at("s4", 15), ACCENT),
    ]
    y = 430
    for k, (title, label, t0, col) in enumerate(steps):
        p = mg.seg(t, t0, 0.4)
        if p > 0:
            box = (L, y + int(26 * (1 - p)), R, y + 152 + int(26 * (1 - p)))
            mg.panel(d, box, None, 16, mg.mix(PAPER, col, p), 3)
            fade(d, (L + 40, box[1] + 26), title, mg.font("sans-bold", 60), p, col)
            fade(d, (L + 40, box[1] + 98), label, mg.font("mono", 30), p * 0.9, MUTED)
        if k < 2:
            ap = mg.seg(t, t0 + 0.35, 0.3)
            if ap > 0:
                ay = y + 152
                d.line([(mg.W / 2, ay + 6), (mg.W / 2, ay + 6 + 56 * ap)],
                       fill=mg.mix(PAPER, MUTED, ap), width=4)
                if ap > 0.85:
                    d.polygon([(mg.W / 2 - 14, ay + 52), (mg.W / 2 + 14, ay + 52),
                               (mg.W / 2, ay + 74)], fill=MUTED)
        y += 216

    f = mg.font("sans", 50)
    for k, ln in enumerate(mg.wrap(d, "“the same as praising McDonald’s for discovering potatoes”", f, COL)):
        fade(d, (L, 1180 + k * 66), ln, f, mg.seg(t, at("s4", 19) + k * 0.12, 0.4), MUTED)
    fade(d, (L, 1330), "— the reply under it", mg.font("mono", 30),
         mg.seg(t, at("s4", 22), 0.4), MUTED)


def s5(d, im, t, tl):
    fade(d, (L, 430), "THIS VIDEO’S BILL", mg.font("mono-bold", 52),
         mg.seg(t, at("s5", 0), 0.4))
    mg.rule(d, 500, L, R, INK, 3, mg.seg(t, at("s5", 0) + 0.15, 0.5))

    fm = mg.font("mono", 36)
    items = [("Voice          free endpoint", "$0.00", at("s5", 4)),
             ("Frames         Python + ffmpeg", "$0.00", at("s5", 6)),
             ("Stock footage  none", "$0.00", at("s5", 9)),
             ("Generation credits", "0", at("s5", 11))]
    y = 560
    for label, amount, t0 in items:
        p = mg.seg(t, t0, 0.35)
        if p > 0:
            col = mg.mix(PAPER, INK, p)
            d.text((L, y), label, font=fm, fill=col)
            aw = d.textlength(amount, font=fm)
            lx = L + d.textlength(label, font=fm) + 16
            dots = int((R - aw - 16 - lx) / d.textlength(".", font=fm))
            if dots > 0:
                d.text((lx, y), "." * dots, font=fm, fill=mg.mix(PAPER, MUTED, p))
            d.text((R - aw, y), amount, font=fm, fill=col)
        y += 62

    tp = mg.seg(t, at("s5", 12) + 0.35, 0.45)
    if tp > 0:
        mg.rule(d, 830, L, R, INK, 4, tp)
        fade(d, (L, 866), "TOTAL", mg.font("mono-bold", 52), tp)
        f = mg.font("sans-bold", 128)
        fade(d, (L, 930), "$0.00", f, tp, ACCENT, "right")
        foot = ("plus %s of render time on one machine"
                % (f"~{CPU_SECONDS:.0f} s" if CPU_SECONDS else "a few minutes"))
        fade(d, (L, 1120), foot, mg.font("mono", 32), mg.seg(t, at("s5", 12) + 0.9, 0.4), MUTED)
        fade(d, (L, 1170), "no card on file, no per-frame charge, re-runnable",
             mg.font("mono", 32), mg.seg(t, at("s5", 12) + 1.1, 0.4), MUTED)


def s6(d, im, t, tl):
    f = mg.font("sans-bold", 76)
    head = "Ask the next person selling you a one-prompt workflow"
    lines = mg.wrap(d, head, f, COL)
    for k, ln in enumerate(lines):
        rise(d, (L, 620 + k * 96), ln, f, mg.seg(t, at("s6", 0) + k * 0.16, 0.4))
    y = 620 + len(lines) * 96 + 30
    ft = mg.font("sans-bold", 70)
    for k, ln in enumerate(mg.wrap(d, "what their number was.", ft, COL)):
        fade(d, (L, y + k * 88), ln, ft, mg.seg(t, at("s6", 11) + k * 0.12, 0.4), ACCENT)
    y += 88 * (len(mg.wrap(d, "what their number was.", ft, COL)) - 1)
    # the outro move: runs past the last word and through the tail, so the file
    # never ends on a held frame
    mg.rule(d, y + 118, L, R, ACCENT, 6, mg.seg(t, TOTAL - 1.15, 1.05, mg.ease_in_out))
    caret(d, L, y + 150, t)


DRAW = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}


def frame_fn(n):
    def frame(t, i):
        im, d = mg.canvas(PAPER)
        chrome(d, t, i, n)
        for s in PLAN["scenes"]:
            if s["start"] <= t < s["start"] + s["dur"] or (
                    s is PLAN["scenes"][-1] and t >= s["start"]):
                DRAW[s["id"]](d, im, t, t - s["start"])
                break
        return im
    return frame


def main() -> int:
    global CPU_SECONDS
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "silent.mp4"))
    ap.add_argument("--cpu-seconds", type=float, default=None,
                    help="measured wall clock of the previous identical render")
    args = ap.parse_args()
    CPU_SECONDS = args.cpu_seconds

    n = int(round(TOTAL * PLAN["fps"]))
    mg.render(frame_fn(n), TOTAL, args.out, fps=PLAN["fps"],
              w=PLAN["width"], h=PLAN["height"], progress_every=180)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
