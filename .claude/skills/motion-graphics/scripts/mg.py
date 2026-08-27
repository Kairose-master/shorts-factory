"""Code-drawn motion graphics for vertical short-form video.

Every frame is computed from a time value, so a render is deterministic,
free, and re-runnable: no generation credits, no model calls, no stock
licence. Import this from a project's ``render.py``:

    import mg
    def frame(t, i):
        im, d = mg.canvas()
        mg.text_block(d, (mg.SAFE["l"], 700), ["hello"], mg.font("sans-bold", 92), mg.INK)
        return im
    mg.render(frame, 6.0, "out.mp4")

Requires: pillow, numpy, imageio-ffmpeg. Nothing else, and nothing paid.
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# canvas
# --------------------------------------------------------------------------
W, H, FPS = 1080, 1920, 30

#: Pixels the platform UI is allowed to cover. Nothing that must be read
#: goes outside this box — see references/animation-rules.md, "Safe area".
SAFE = {"l": 96, "r": W - 96, "t": 260, "b": H - 380}

INK = (20, 20, 22)
PAPER = (243, 239, 230)
MUTED = (122, 116, 108)
ACCENT = (198, 58, 46)

FONT_FILES = {
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sans-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "mono-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "serif-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
}
_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(family: str, size: int) -> ImageFont.FreeTypeFont:
    key = (family, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_FILES[family], size)
    return _font_cache[key]


def canvas(bg=PAPER) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (W, H), bg)
    return im, ImageDraw.Draw(im)


# --------------------------------------------------------------------------
# easing
# --------------------------------------------------------------------------
def clamp01(x: float) -> float:
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def linear(t: float) -> float:
    return clamp01(t)


def ease_out(t: float) -> float:
    """Cubic. The default: fast start, soft landing. Reads as confident."""
    t = clamp01(t)
    return 1 - (1 - t) ** 3


def ease_in(t: float) -> float:
    t = clamp01(t)
    return t ** 3


def ease_in_out(t: float) -> float:
    t = clamp01(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def ease_out_back(t: float, overshoot: float = 1.2) -> float:
    """Small overshoot. Use once per video, on the one thing that matters."""
    t = clamp01(t)
    c3 = overshoot + 1
    return 1 + c3 * (t - 1) ** 3 + overshoot * (t - 1) ** 2


def seg(t: float, start: float, dur: float, ease=ease_out) -> float:
    """Local eased progress of a sub-animation that begins at ``start``.

    Returns 0 before it starts and 1 after it ends, so a caller can write
    every element against the scene clock and never track state.
    """
    if dur <= 0:
        return 1.0 if t >= start else 0.0
    return ease((t - start) / dur)


def hold(t: float, start: float, dur: float) -> bool:
    """True while a beat is on screen (used to gate drawing, not fading)."""
    return start <= t < start + dur


# --------------------------------------------------------------------------
# text
# --------------------------------------------------------------------------
def wrap(d: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = f"{cur} {wd}".strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_font(d, text: str, family: str, max_w: int, start: int, min_size: int = 28):
    """Largest size in ``family`` that keeps ``text`` on one line."""
    size = start
    while size > min_size and d.textlength(text, font=font(family, size)) > max_w:
        size -= 2
    return font(family, size)


def text_block(d, xy, lines, fnt, fill, leading: float = 1.26, align: str = "left",
               max_x: int | None = None, opacity: float = 1.0, bg=None):
    """Draw wrapped lines from a top-left anchor. Returns the y after the block."""
    x, y = xy
    if opacity < 1.0 and bg is not None:
        fill = mix(bg, fill, opacity)
    step = int(fnt.size * leading)
    right = max_x if max_x is not None else SAFE["r"]
    for ln in lines:
        if align == "center":
            lx = x + (right - x - d.textlength(ln, font=fnt)) / 2
        elif align == "right":
            lx = right - d.textlength(ln, font=fnt)
        else:
            lx = x
        d.text((lx, y), ln, font=fnt, fill=fill)
        y += step
    return y


def reveal_words(line: str, p: float) -> str:
    """Word-by-word reveal. Cheaper on attention than a typewriter."""
    words = line.split()
    n = int(round(clamp01(p) * len(words)))
    return " ".join(words[:n])


def typewriter(line: str, p: float) -> str:
    return line[: int(round(clamp01(p) * len(line)))]


# --------------------------------------------------------------------------
# colour + primitives
# --------------------------------------------------------------------------
def mix(a, b, p: float):
    p = clamp01(p)
    return tuple(int(round(a[i] + (b[i] - a[i]) * p)) for i in range(3))


def rule(d, y: int, x0: int, x1: int, color, width: int = 3, p: float = 1.0):
    """A horizontal rule that draws itself left to right."""
    p = clamp01(p)
    if p <= 0:
        return
    d.line([(x0, y), (x0 + (x1 - x0) * p, y)], fill=color, width=width)


def panel(d, box, fill=None, radius: int = 20, outline=None, width: int = 3):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def progress_bar(d, box, p: float, fg, bg, radius: int = 8):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=radius, fill=bg)
    p = clamp01(p)
    if p > 0:
        d.rounded_rectangle((x0, y0, x0 + (x1 - x0) * p, y1), radius=radius, fill=fg)


def counter(a: float, b: float, p: float, fmt: str = "{:,.0f}") -> str:
    """An eased number roll. Format with a fixed width so it does not jitter."""
    return fmt.format(a + (b - a) * clamp01(p))


def caret(t: float, period: float = 1.0) -> bool:
    """Blinking cursor state, for anything that should look like it is running."""
    return (t % period) < period * 0.55


# --------------------------------------------------------------------------
# encoding
# --------------------------------------------------------------------------
def ffmpeg_exe() -> str:
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


class Encoder:
    """Raw RGB straight into libx264. No PNG scratch files, no temp dir."""

    def __init__(self, path, w=W, h=H, fps=FPS, crf=18, preset="medium"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.proc = subprocess.Popen(
            [
                ffmpeg_exe(), "-y", "-loglevel", "error",
                "-f", "rawvideo", "-pix_fmt", "rgb24",
                "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                "-an", "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path),
            ],
            stdin=subprocess.PIPE,
        )

    def add(self, im: Image.Image):
        self.proc.stdin.write(im.tobytes())

    def close(self):
        self.proc.stdin.close()
        if self.proc.wait() != 0:
            raise RuntimeError("ffmpeg encode failed")


def render(frame_fn, duration: float, path, fps: int = FPS, w: int = W, h: int = H,
           crf: int = 18, progress_every: int = 60) -> str:
    """Render ``frame_fn(t, i) -> Image`` for ``duration`` seconds."""
    n = int(round(duration * fps))
    enc = Encoder(path, w, h, fps, crf)
    for i in range(n):
        im = frame_fn(i / fps, i)
        if im.size != (w, h):
            raise ValueError(f"frame {i} is {im.size}, expected {(w, h)}")
        enc.add(im)
        if progress_every and i % progress_every == 0:
            print(f"  frame {i}/{n}", flush=True)
    enc.close()
    print(f"  wrote {path} ({n} frames, {n / fps:.2f}s)")
    return str(path)


def contact_sheet(video: str, out: str, cols: int = 4, rows: int = 3, tile_w: int = 270):
    """Pull an even grid of frames so a human can actually look at the render."""
    dur = duration_of(video)
    n = cols * rows
    tile_h = int(tile_w * H / W)
    sheet = Image.new("RGB", (cols * tile_w, rows * tile_h), (0, 0, 0))
    for k in range(n):
        ts = dur * (k + 0.5) / n
        raw = subprocess.run(
            [ffmpeg_exe(), "-v", "error", "-ss", f"{ts:.3f}", "-i", video,
             "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            capture_output=True).stdout
        if len(raw) < W * H * 3:
            continue
        im = Image.frombytes("RGB", (W, H), raw[: W * H * 3]).resize((tile_w, tile_h))
        sheet.paste(im, ((k % cols) * tile_w, (k // cols) * tile_h))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"  wrote {out}")
    return out


def duration_of(video: str) -> float:
    """Seconds, from ffprobe when it exists and from ffmpeg's banner when it does not."""
    import json
    import shutil

    probe = shutil.which("ffprobe")
    if probe:
        r = subprocess.run([probe, "-v", "error", "-show_format", "-of", "json", video],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return float(json.loads(r.stdout)["format"]["duration"])
    out = subprocess.run([ffmpeg_exe(), "-i", video], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            hms = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = hms.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"could not read duration of {video}")


__all__ = [n for n in dir() if not n.startswith("_")]
