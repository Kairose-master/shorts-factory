"""Render 「말값」 EP1 to MP4.

Not the official path — video-studio/gen_boil is unreachable behind the egress
proxy, so this reimplements the boil grammar directly: wobbly single-weight line
art, flat two-colour scenes, hold-3 redraw, typography set on the art, no captions.
"""
import math, random, subprocess, wave, importlib.util, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = "projects/malgap-ep1"
W, H, FPS, HOLD = 1080, 1920, 30, 3
INK, PAPER = "#14110F", "#F2E9DC"
FONT = f"{ROOT}/NotoSansKR-Bold.ttf"

spec = importlib.util.spec_from_file_location("shapes", f"{ROOT}/boil_shapes.py")
mod = importlib.util.module_from_spec(spec)
mod.__dict__["math"] = math

def wob(d, pts, c, rng, w, amp):
    out = [(x + rng.uniform(-amp, amp), y + rng.uniform(-amp, amp)) for x, y in pts]
    if len(out) > 1:
        d.line(out, fill=c, width=int(w), joint="curve")

mod.__dict__.update(wob=wob, circle=lambda *a, **k: None, box=lambda *a, **k: None)
spec.loader.exec_module(mod)

def rings(d, c, rng, w, p, cx, cy, s):
    for k in range(4):
        r = s * (0.12 + 0.10 * k) * (1 + 0.04 * math.sin(p * math.tau + k))
        pts = [(cx + math.cos(math.tau * i / 47) * r, cy + math.sin(math.tau * i / 47) * r)
               for i in range(48)]
        wob(d, pts, c, rng, w, 2.4)

SCENES = [
    dict(id="s1", mark=rings,        card=None,                     bg=INK,   fg=PAPER, secs=6.0),
    dict(id="s2", mark=mod.s_spark,  card="시그니처",                 bg=PAPER, fg=INK,   secs=5.0),
    dict(id="s3", mark=mod.s_cup,    card="요거트에\n토핑 세 개",       bg=INK,   fg=PAPER, secs=6.0),
    dict(id="s4", mark=mod.s_coin,   card="3만 원",                  bg=INK,   fg=PAPER, secs=6.0),
    dict(id="s5", mark=mod.s_scale,  card="재료값\n____원",           bg=INK,   fg=PAPER, secs=6.0),
    dict(id="s6", mark=mod.s_period, card="말값 =\n3만 원 − ____",    bg=INK,   fg=PAPER, secs=5.0),
]
TOTAL = sum(s["secs"] for s in SCENES)
f_card = ImageFont.truetype(FONT, 104)

def frame(si, sc, fi):
    im = Image.new("RGB", (W, H), sc["bg"])
    d = ImageDraw.Draw(im)
    rng = random.Random(9000 + si * 977 + fi // HOLD)      # redraw every HOLD frames
    p = (fi / FPS) / sc["secs"]
    sc["mark"](d, sc["fg"], rng, 5, p, W * 0.5, H * 0.33, W * 0.60)
    if sc["card"] and fi >= int(0.45 * FPS):               # card lands after the mark
        y = H * 0.63
        for line in sc["card"].split("\n"):
            bb = d.textbbox((0, 0), line, font=f_card)
            d.text(((W - (bb[2] - bb[0])) / 2, y), line, font=f_card, fill=sc["fg"])
            y += 132
    return im

# ---- audio: narration placed at each scene start + lead-in, padded to TOTAL
SR = 24000
track = np.zeros(int(TOTAL * SR), dtype=np.float32)
t = 0.0
for sc in SCENES:
    path = f"{ROOT}/vo/{sc['id']}.wav"
    if os.path.exists(path):
        with wave.open(path) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        a *= 0.30 / max(np.sqrt((a ** 2).mean()), 1e-6)     # even out per-line level
        st = int((t + 0.35) * SR)
        seg = a[: len(track) - st]
        track[st:st + len(seg)] += seg
    t += sc["secs"]
track = np.clip(track, -0.99, 0.99)
with wave.open(f"{ROOT}/mix.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype(np.int16).tobytes())
print(f"audio {len(track)/SR:.2f}s")

# ---- video
exe = imageio_ffmpeg.get_ffmpeg_exe()
proc = subprocess.Popen(
    [exe, "-y", "-loglevel", "error",
     "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-i", f"{ROOT}/mix.wav",
     "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
     f"{ROOT}/malgap_ep1.mp4"], stdin=subprocess.PIPE)
n = 0
for si, sc in enumerate(SCENES):
    for fi in range(int(sc["secs"] * FPS)):
        proc.stdin.write(frame(si, sc, fi).tobytes()); n += 1
    print(f"  {sc['id']} done ({n} frames)")
proc.stdin.close(); proc.wait()
print("frames", n, "rc", proc.returncode)
