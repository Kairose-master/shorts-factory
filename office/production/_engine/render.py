#!/usr/bin/env python3
"""Minimal deterministic 9:16 frame renderer for the Growth Office.

Draws frames with Pillow, one PNG per frame, then FFmpeg muxes them with the
Piper narration. No browser, no Node, no network, no paid provider.

A video is a list of Element objects. Each element declares when it is alive
(t0..t1) and draws itself for a given time. Everything is a pure function of t,
so a render is reproducible and a single frame can be previewed in isolation.
"""
from __future__ import annotations
import math, os, subprocess, sys
from dataclasses import dataclass, field
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONTS = Path("/mnt/skills/examples/canvas-design/canvas-fonts")

# Palette. Dark because the audience watches at night on a phone, and because
# every surface the videos depict (a terminal, a job board) is dark already.
BG      = (11, 13, 14)
INK     = (245, 245, 244)
MUTED   = (113, 113, 122)
DIM     = (39, 41, 43)
PASS    = (52, 211, 153)
FAIL    = (248, 113, 113)
MONEY   = (250, 204, 21)
ACCENT  = (129, 140, 248)

# Safe area: TikTok's right rail and bottom caption bar eat real estate.
SAFE_L, SAFE_R, SAFE_T, SAFE_B = 80, 130, 300, 420
CAP_Y = 1500  # caption baseline — above every platform's bottom furniture

_fc: dict = {}
def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(str(FONTS / f"{name}.ttf"), size)
    return _fc[k]

DISPLAY, BODY, MONO, MONOB = "Outfit-Bold", "InstrumentSans-Regular", "JetBrainsMono-Regular", "JetBrainsMono-Bold"

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def ease_out(t):  return 1 - (1 - clamp(t)) ** 3
def ease_in_out(t):
    t = clamp(t)
    return 4*t*t*t if t < .5 else 1 - (-2*t + 2) ** 3 / 2
def ramp(t, t0, dur):
    """0 before t0, 1 after t0+dur, eased between."""
    return ease_out((t - t0) / dur) if dur > 0 else (1.0 if t >= t0 else 0.0)

def mix(c1, c2, a):
    a = clamp(a)
    return tuple(round(x + (y - x) * a) for x, y in zip(c1, c2))
def fade(c, a):
    return mix(BG, c, a)

# ---------- text helpers ----------
def wrap(draw, text, f, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

def text_block(draw, text, f, y, color, maxw=None, align="center", x=None,
               line_gap=1.22, stroke=0, stroke_fill=BG):
    maxw = maxw or (W - SAFE_L - SAFE_R)
    lines = wrap(draw, text, f, maxw)
    lh = f.size * line_gap
    for i, ln in enumerate(lines):
        wpx = draw.textlength(ln, font=f)
        if align == "center":   px = (W - wpx) / 2
        elif align == "left":   px = x if x is not None else SAFE_L
        else:                   px = (x if x is not None else W - SAFE_R) - wpx
        draw.text((px, y + i * lh), ln, font=f, fill=color,
                  stroke_width=stroke, stroke_fill=stroke_fill)
    return y + len(lines) * lh

# ---------- elements ----------
@dataclass
class El:
    t0: float = 0.0
    t1: float = 1e9
    def alive(self, t): return self.t0 <= t < self.t1
    def draw(self, d, t, img=None): ...

@dataclass
class Caption(El):
    """Burned-in caption. Most of the audience watches muted; this is the track
    that has to carry the video on its own."""
    text: str = ""
    size: int = 62
    color: tuple = INK
    y: int = CAP_Y
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .18) * (1 - ramp(t, self.t1 - .18, .18))
        if a <= .01: return
        f = font(DISPLAY, self.size)
        lines = wrap(d, self.text, f, W - SAFE_L - SAFE_R)
        y = self.y - (len(lines) - 1) * f.size * .62
        text_block(d, self.text, f, y, fade(self.color, a),
                   stroke=8, stroke_fill=BG)

@dataclass
class Title(El):
    text: str = ""
    size: int = 96
    color: tuple = INK
    y: int = 700
    rise: int = 40
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .35) * (1 - ramp(t, self.t1 - .25, .25))
        if a <= .01: return
        off = (1 - ease_out((t - self.t0) / .5)) * self.rise
        text_block(d, self.text, font(DISPLAY, self.size), self.y + off,
                   fade(self.color, a))

@dataclass
class Mono(El):
    """Machine output. Monospace because the audience reads code all day and
    reads a proportional font as marketing."""
    text: str = ""
    size: int = 40
    color: tuple = MUTED
    y: int = 900
    x: int = SAFE_L
    typing: float = 0.0   # seconds to type it out; 0 = appear whole
    bold: bool = False
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .15) * (1 - ramp(t, self.t1 - .15, .15))
        if a <= .01: return
        s = self.text
        if self.typing:
            n = int(len(s) * clamp((t - self.t0) / self.typing))
            s = s[:n] + ("█" if n < len(s) and int(t * 6) % 2 else "")
        f = font(MONOB if self.bold else MONO, self.size)
        d.text((self.x, self.y), s, font=f, fill=fade(self.color, a))

@dataclass
class Box(El):
    """A labelled node. The four nouns that carry every Handsel explainer —
    worker, grader, job, verdict — are all boxes."""
    label: str = ""
    x: float = 0; y: float = 0; w: float = 380; h: float = 200
    color: tuple = INK
    fill: tuple = None
    size: int = 46
    dash: bool = False
    grow: float = .45
    move_to: tuple = None      # (x, y) — animate position over move_dur
    move_at: float = None
    move_dur: float = .8
    def pos(self, t):
        x, y = self.x, self.y
        if self.move_to and self.move_at is not None:
            p = ease_in_out((t - self.move_at) / self.move_dur)
            x += (self.move_to[0] - self.x) * p
            y += (self.move_to[1] - self.y) * p
        return x, y
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .01 if self.grow == 0 else .25) * (1 - ramp(t, self.t1 - .2, .2))
        if a <= .01: return
        s = ease_out((t - self.t0) / self.grow) if self.grow else 1.0
        s = .82 + .18 * clamp(s)
        x, y = self.pos(t)
        w, h = self.w * s, self.h * s
        r = [x - w/2, y - h/2, x + w/2, y + h/2]
        col = fade(self.color, a)
        if self.fill:
            d.rounded_rectangle(r, 22, fill=fade(self.fill, a * .9))
        if self.dash:
            step, on = 26, 14
            x0, y0, x1, y1 = r
            for px in range(int(x0), int(x1), step):
                d.line([px, y0, min(px+on, x1), y0], fill=col, width=4)
                d.line([px, y1, min(px+on, x1), y1], fill=col, width=4)
            for py in range(int(y0), int(y1), step):
                d.line([x0, py, x0, min(py+on, y1)], fill=col, width=4)
                d.line([x1, py, x1, min(py+on, y1)], fill=col, width=4)
        else:
            d.rounded_rectangle(r, 22, outline=col, width=5)
        f = font(DISPLAY, self.size)
        tw = d.textlength(self.label, font=f)
        d.text((x - tw/2, y - f.size*.62), self.label, font=f, fill=col)

@dataclass
class Arrow(El):
    """Straight arrow between two points, drawn progressively."""
    p0: tuple = (0, 0); p1: tuple = (0, 0)
    color: tuple = MUTED
    width: int = 6
    grow: float = .6
    label: str = ""
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .2) * (1 - ramp(t, self.t1 - .2, .2))
        if a <= .01: return
        p = ease_out((t - self.t0) / self.grow) if self.grow else 1.0
        x0, y0 = self.p0; x1, y1 = self.p1
        xe, ye = x0 + (x1-x0)*p, y0 + (y1-y0)*p
        col = fade(self.color, a)
        d.line([x0, y0, xe, ye], fill=col, width=self.width)
        if p > .9:
            ang = math.atan2(y1-y0, x1-x0); L = 26
            for s in (2.6, -2.6):
                d.line([x1, y1, x1 + L*math.cos(ang+s), y1 + L*math.sin(ang+s)],
                       fill=col, width=self.width)
        if self.label and p > .5:
            f = font(MONO, 32)
            tw = d.textlength(self.label, font=f)
            mx, my = (x0+x1)/2, (y0+y1)/2
            d.text((mx - tw/2, my - 52), self.label, font=f, fill=col,
                   stroke_width=8, stroke_fill=BG)

@dataclass
class SelfLoop(El):
    """An arrow that leaves a box and returns to it. The whole of HS-011's
    opening argument is this one shape."""
    cx: float = 0; cy: float = 0; rw: float = 300; rh: float = 210
    color: tuple = FAIL
    width: int = 6
    grow: float = .9
    label: str = ""
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .2) * (1 - ramp(t, self.t1 - .2, .2))
        if a <= .01: return
        p = clamp(ease_out((t - self.t0) / self.grow)) if self.grow else 1.0
        col = fade(self.color, a)
        pts, N = [], 90
        for i in range(int(N * p) + 1):
            th = -math.pi*.45 + (2*math.pi*.9) * (i / N)
            pts.append((self.cx + self.rw*math.cos(th), self.cy + self.rh*math.sin(th)))
        if len(pts) > 1:
            d.line(pts, fill=col, width=self.width, joint="curve")
        if p > .95 and len(pts) > 2:
            (xa, ya), (xb, yb) = pts[-2], pts[-1]
            ang = math.atan2(yb-ya, xb-xa); L = 26
            for s in (2.6, -2.6):
                d.line([xb, yb, xb + L*math.cos(ang+s), yb + L*math.sin(ang+s)],
                       fill=col, width=self.width)
        if self.label and p > .6:
            f = font(MONO, 34)
            tw = d.textlength(self.label, font=f)
            d.text((self.cx - tw/2, self.cy - self.rh - 66), self.label,
                   font=f, fill=col, stroke_width=8, stroke_fill=BG)

@dataclass
class Row(El):
    """One line of a real data table (an agent, a job, a verdict)."""
    left: str = ""; right: str = ""
    y: float = 0
    color: tuple = INK
    rcolor: tuple = None
    size: int = 40
    slide: float = 60
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .3) * (1 - ramp(t, self.t1 - .2, .2))
        if a <= .01: return
        off = (1 - ease_out((t - self.t0) / .5)) * self.slide
        f = font(MONO, self.size)
        d.text((SAFE_L, self.y + off), self.left, font=f, fill=fade(self.color, a))
        if self.right:
            fb = font(MONOB, self.size)
            tw = d.textlength(self.right, font=fb)
            d.text((W - SAFE_R - tw, self.y + off), self.right, font=fb,
                   fill=fade(self.rcolor or self.color, a))

@dataclass
class Flash(El):
    """A full-frame wash. Used once, on the FAIL."""
    color: tuple = FAIL
    peak: float = .22
    def draw(self, d, t, img=None):
        p = clamp((t - self.t0) / max(self.t1 - self.t0, .001))
        a = math.sin(math.pi * p) * self.peak
        if a <= .01: return
        d.rectangle([0, 0, W, H], fill=mix(BG, self.color, a))

@dataclass
class Rule(El):
    y: float = 0
    color: tuple = DIM
    grow: float = .5
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .2) * (1 - ramp(t, self.t1 - .2, .2))
        if a <= .01: return
        p = ease_out((t - self.t0) / self.grow)
        d.line([SAFE_L, self.y, SAFE_L + (W - SAFE_L - SAFE_R) * p, self.y],
               fill=fade(self.color, a), width=3)

@dataclass
class Counter(El):
    """A number that ticks. Money moving is the only thing worth animating."""
    prefix: str = "$"; a0: float = 0.0; a1: float = 0.0
    y: float = 0
    size: int = 120
    color: tuple = MONEY
    dur: float = 1.0
    dp: int = 2
    def draw(self, d, t, img=None):
        a = ramp(t, self.t0, .2) * (1 - ramp(t, self.t1 - .2, .2))
        if a <= .01: return
        p = ease_out((t - self.t0) / self.dur)
        v = self.a0 + (self.a1 - self.a0) * p
        s = f"{self.prefix}{v:,.{self.dp}f}"
        f = font(MONOB, self.size)
        tw = d.textlength(s, font=f)
        d.text(((W - tw)/2, self.y), s, font=f, fill=fade(self.color, a))

@dataclass
class Grain(El):
    """A 1px vignette so flat dark backgrounds do not band on phone screens."""
    def draw(self, d, t, img=None):
        d.rectangle([0, 0, W, 6], fill=BG)

# ---------- driver ----------
def render(name: str, duration: float, elements: list, outdir: Path,
           audio: Path = None, fps: int = FPS):
    frames = outdir / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    for old in frames.glob("*.png"): old.unlink()
    n = int(duration * fps)
    for i in range(n):
        t = i / fps
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        for el in elements:
            if el.alive(t):
                el.draw(d, t, img)
        img.save(frames / f"f{i:05d}.png")
        if i % 60 == 0:
            print(f"  {name}: {i}/{n}", flush=True)
    out = outdir / "final.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-framerate", str(fps), "-i", str(frames / "f%05d.png")]
    if audio and Path(audio).exists():
        cmd += ["-i", str(audio), "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "19",
            "-pix_fmt", "yuv420p", "-r", str(fps), str(out)]
    subprocess.run(cmd, check=True)
    for f in frames.glob("*.png"): f.unlink()
    frames.rmdir()
    print(f"  -> {out}")
    return out
