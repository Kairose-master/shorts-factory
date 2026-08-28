#!/usr/bin/env python3
"""Office-floor primitives — a company you can watch run.

The base engine draws boxes and type. That is right for an argument and wrong
for "watch it do business": a viewer should see work move between desks, desks
light up while they think, and money land when the work passes.

Everything is still a pure function of t, so the whole floor is reproducible and
any single frame can be previewed.

Coordinates are the same 1080x1920 space as render.py.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field

from render import (W, H, BG, INK, MUTED, DIM, PASS, FAIL, MONEY, ACCENT,
                    El, clamp, ease_out, ease_in_out, ramp, mix, fade, font,
                    DISPLAY, MONO, MONOB, SAFE_L, SAFE_R)

DESK_W, DESK_H = 386, 132
SCREEN_W, SCREEN_H = 84, 56


# ---------- geometry ----------
def bezier(p0, p1, p2, t):
    """Quadratic. Work travelling in a straight line looks like a diagram;
    a slight arc looks like it is being carried."""
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def arc_ctrl(a, b, bow=0.18):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    return (mx - dy * bow, my + dx * bow)


# ---------- floor ----------
@dataclass
class Floor(El):
    """A faint grid. Without it the desks float in nothing and the frame reads
    as a slide rather than a place."""
    y0: float = 460
    y1: float = 1420
    step: int = 64
    color: tuple = (26, 28, 30)
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .6) * (1 - ramp(t, self.t1 - .4, .4))
        if a <= .01:
            return
        c = fade(self.color, a)
        for x in range(SAFE_L - 40, W - SAFE_R + 60, self.step):
            d.line([x, self.y0, x, self.y1], fill=c, width=1)
        for y in range(int(self.y0), int(self.y1), self.step):
            d.line([SAFE_L - 40, y, W - SAFE_R + 60, y], fill=c, width=1)


@dataclass
class Desk(El):
    """One worker at a station.

    `busy` windows make the screen flicker; `done_at` turns the status light
    green and stops the flicker. `paid_at` briefly rims the desk in money.
    """
    label: str = ""
    x: float = 0; y: float = 0
    color: tuple = INK
    busy: tuple = None          # (start, end) — thinking
    done_at: float = None
    paid_at: float = None
    dim_until: float = None     # greyed out before it is hired
    seat: bool = True

    def status(self, t):
        if self.done_at is not None and t >= self.done_at:
            return PASS
        if self.busy and self.busy[0] <= t < self.busy[1]:
            return MONEY
        return DIM

    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .3) * (1 - ramp(t, self.t1 - .25, .25))
        if a <= .01:
            return
        live = not (self.dim_until and t < self.dim_until)
        base = self.color if live else DIM
        s = .86 + .14 * clamp(ease_out((t - self.t0) / .45))
        w, h = DESK_W * s, DESK_H * s
        r = [self.x - w / 2, self.y - h / 2, self.x + w / 2, self.y + h / 2]

        # desk body
        d.rounded_rectangle(r, 16, outline=fade(base, a), width=4)

        # screen — the thing that flickers while the worker thinks
        sx, sy = self.x - w / 2 + 34, self.y
        sr = [sx, sy - SCREEN_H / 2, sx + SCREEN_W, sy + SCREEN_H / 2]
        working = live and self.busy and self.busy[0] <= t < self.busy[1]
        if working:
            # deterministic flicker: a hash of the frame, not randomness
            k = int(t * 12) * 2654435761 % 97 / 97.0
            glow = mix(DIM, ACCENT, .35 + .5 * k)
            d.rounded_rectangle(sr, 5, fill=fade(glow, a * .85))
            for i in range(3):
                ly = sy - 14 + i * 13
                lw = SCREEN_W * (0.35 + 0.55 * ((k * (i + 3)) % 1.0))
                d.line([sx + 8, ly, sx + 8 + lw, ly], fill=fade(INK, a * .7), width=3)
        else:
            d.rounded_rectangle(sr, 5, outline=fade(DIM if not live else MUTED, a), width=3)

        # status light
        col = self.status(t) if live else DIM
        cx, cy = self.x + w / 2 - 30, self.y - h / 2 + 26
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=fade(col, a))
        if working:
            p = (math.sin(t * 7) + 1) / 2
            d.ellipse([cx - 8 - 7 * p, cy - 8 - 7 * p, cx + 8 + 7 * p, cy + 8 + 7 * p],
                      outline=fade(col, a * (1 - p) * .8), width=2)

        # money rim on payment
        if self.paid_at is not None and 0 <= t - self.paid_at < .7:
            g = 1 - (t - self.paid_at) / .7
            d.rounded_rectangle([r[0] - 5, r[1] - 5, r[2] + 5, r[3] + 5], 20,
                                outline=fade(MONEY, a * g), width=4)

        f = font(DISPLAY, 34)
        tw = d.textlength(self.label, font=f)
        d.text((sx + SCREEN_W + 22, self.y - f.size * .62), self.label,
               font=f, fill=fade(base if live else DIM, a))


WIRE = (58, 63, 68)     # brighter than DIM — a route you can actually follow


@dataclass
class Wire(El):
    """A route between two desks. Visible, but never louder than a packet."""
    a: tuple = (0, 0); b: tuple = (0, 0)
    color: tuple = WIRE
    grow: float = .5
    bow: float = 0.16
    def pts(self, n=26):
        c = arc_ctrl(self.a, self.b, self.bow)
        return [bezier(self.a, c, self.b, i / n) for i in range(n + 1)]
    def draw(self, d, t, img=None):
        al = ramp(t, self.t0, .3) * (1 - ramp(t, self.t1 - .3, .3))
        if al <= .01:
            return
        p = clamp(ease_out((t - self.t0) / self.grow)) if self.grow else 1.0
        pts = self.pts()
        n = max(int(len(pts) * p), 2)
        d.line(pts[:n], fill=fade(self.color, al), width=4, joint="curve")


@dataclass
class Packet(El):
    """A unit of work in transit. This is the thing that makes the floor read
    as active rather than as a diagram of an org chart."""
    a: tuple = (0, 0); b: tuple = (0, 0)
    color: tuple = ACCENT
    size: int = 13
    bow: float = 0.16
    trail: int = 5
    def draw(self, d, t, img=None):
        dur = max(self.t1 - self.t0, .001)
        p = clamp((t - self.t0) / dur)
        c = arc_ctrl(self.a, self.b, self.bow)
        for i in range(self.trail):
            q = clamp(p - i * 0.035)
            x, y = bezier(self.a, c, self.b, ease_in_out(q))
            s = self.size * (1 - i / (self.trail + 1))
            al = (1 - i / self.trail) * (1 - abs(0.5 - p) * 0.25)
            d.rounded_rectangle([x - s, y - s, x + s, y + s], 4,
                                fill=fade(self.color, al))


@dataclass
class Coin(Packet):
    """Money. Same motion, round, and it lands rather than passes through."""
    color: tuple = MONEY
    size: int = 12
    def draw(self, d, t, img=None):
        dur = max(self.t1 - self.t0, .001)
        p = clamp((t - self.t0) / dur)
        c = arc_ctrl(self.a, self.b, self.bow)
        for i in range(4):
            q = clamp(p - i * 0.04)
            x, y = bezier(self.a, c, self.b, ease_out(q))
            s = self.size * (1 - i / 6)
            d.ellipse([x - s, y - s, x + s, y + s],
                      fill=fade(self.color, (1 - i / 5) * 0.95))


@dataclass
class Pulse(El):
    """An expanding ring. Something happened here."""
    x: float = 0; y: float = 0
    color: tuple = PASS
    r0: float = 14; r1: float = 120
    def draw(self, d, t, img=None):
        dur = max(self.t1 - self.t0, .001)
        p = clamp((t - self.t0) / dur)
        r = self.r0 + (self.r1 - self.r0) * ease_out(p)
        a = (1 - p) ** 1.6
        if a <= .02:
            return
        d.ellipse([self.x - r, self.y - r, self.x + r, self.y + r],
                  outline=fade(self.color, a), width=max(int(5 * (1 - p)) + 1, 1))


@dataclass
class Treasury(El):
    """The money the company holds, as a bar that visibly drains."""
    x: float = W / 2; y: float = 0
    w: float = 640; h: float = 26
    total: float = 7.0
    steps: list = field(default_factory=list)   # [(t, remaining)]
    def value(self, t):
        v = self.total
        for ts, rem in self.steps:
            if t >= ts:
                v = rem
        return v
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .35) * (1 - ramp(t, self.t1 - .3, .3))
        if a <= .01:
            return
        x0, x1 = self.x - self.w / 2, self.x + self.w / 2
        d.rounded_rectangle([x0, self.y, x1, self.y + self.h], 13,
                            outline=fade(DIM, a), width=3)
        frac = clamp(self.value(t) / self.total)
        # ease the drain so the bar moves rather than jumping
        if self.steps:
            prev, nxt, ts = self.total, self.value(t), None
            for s_t, rem in self.steps:
                if t >= s_t:
                    ts, prev_rem = s_t, prev
                    prev = rem
            if ts is not None and t - ts < .45:
                k = ease_out((t - ts) / .45)
                frac = clamp((prev_rem + (nxt - prev_rem) * k) / self.total)
        if frac > 0:
            d.rounded_rectangle([x0 + 3, self.y + 3, x0 + 3 + (self.w - 6) * frac,
                                 self.y + self.h - 3], 11, fill=fade(MONEY, a * .9))
        f = font(MONOB, 34)
        s = f"${self.value(t):.2f}"
        d.text((x1 + 18, self.y - 6), s, font=f, fill=fade(MONEY, a))
        f2 = font(MONO, 26)
        d.text((x0, self.y - 40), "treasury", font=f2, fill=fade(MUTED, a))


def desk_edge(desk, side):
    """Anchor points so wires and packets leave and arrive at the desk edge."""
    if side == "bottom":
        return (desk.x, desk.y + DESK_H / 2)
    if side == "top":
        return (desk.x, desk.y - DESK_H / 2)
    if side == "left":
        return (desk.x - DESK_W / 2, desk.y)
    return (desk.x + DESK_W / 2, desk.y)
