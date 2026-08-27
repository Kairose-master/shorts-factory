"""「말값」 No.2 정통 — 미디어아트 연작 렌더러.

문법 차용: 궁금소 171x "미라가 만들어지는 과정" — 과정 서술, 판단 없이 종료.
숫자 근거: 제로비 평양냉면 transcript verbatim — 16,000원, "걸레 빤 물" 비판.
형식: boil 추상 (먹지/종이 2색, 씬당 마크 1 + 카드 1, 캡션 off) = EP1 연작 동일.
"""
import math, random, json, wave, subprocess, os, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, HOLD = 1080, 1920, 30, 3
INK, PAPER = "#14110F", "#F2E9DC"
FONT = f"{ROOT}/../malgap-ep1/NotoSansKR-Bold.ttf"
F_CARD = ImageFont.truetype(FONT, 96)
F_SUB  = ImageFont.truetype(FONT, 54)
F_SER  = ImageFont.truetype(FONT, 42)

spec = importlib.util.spec_from_file_location("shapes", f"{ROOT}/boil_shapes.py")
mod = importlib.util.module_from_spec(spec)
mod.__dict__["math"] = math
def wob(d, pts, c, rng, w, amp):
    out = [(x + rng.uniform(-amp, amp), y + rng.uniform(-amp, amp)) for x, y in pts]
    if len(out) > 1: d.line(out, fill=c, width=int(w), joint="curve")
mod.__dict__.update(wob=wob, circle=lambda *a, **k: None, box=lambda *a, **k: None)
spec.loader.exec_module(mod)

VO = {p["id"]: p for p in json.load(open(f"{ROOT}/vo/lines.json"))}
# id, mark, card(main, sub), bg, fg, secs  — s5 stretched to 7.5s: narration 6.91s
SCENES = [
 ("s1", mod.s_bowl,      None,                          INK,   PAPER, 6.0),
 ("s2", mod.s_steam,     ("정통", None),                 PAPER, INK,   5.5),
 ("s3", mod.s_signboard, ("1단계", "오래된 간판"),         INK,   PAPER, 6.0),
 ("s4", mod.s_queue,     ("2단계", "줄"),                INK,   PAPER, 5.0),
 ("s5", mod.s_bowl,      ("3단계", "“걸레 빤 물” — 실제 비판"), INK, PAPER, 7.5),
 ("s6", mod.s_period,    ("말값 =", "16,000원 − ____원"), INK,   PAPER, 5.5),
]
TOTAL = sum(s[5] for s in SCENES)

def frame(si, sid, mark, card, bg, fg, secs, fi):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    rng = random.Random(4000 + si * 733 + fi // HOLD)
    p = fi / FPS / secs
    mark(d, fg, rng, 5, p, W * 0.5, H * 0.33, W * 0.60)
    if sid == "s5":  # thin broth: overdraw sparse horizontal lines fading
        for k in range(2):
            y = H * 0.33 + 40 + k * 26
            wob(d, [(W * 0.30, y), (W * 0.70, y)], fg, rng, 2, 1.5)
    if card and fi >= int(0.45 * FPS):
        main, sub = card
        y = H * 0.60
        bb = d.textbbox((0, 0), main, font=F_CARD)
        d.text(((W - bb[2]) / 2, y), main, font=F_CARD, fill=fg)
        if sub:
            bb2 = d.textbbox((0, 0), sub, font=F_SUB)
            d.text(((W - bb2[2]) / 2, y + 140), sub, font=F_SUB, fill=fg)
    d.text((60, 90), "「말값」 No.2", font=F_SER, fill=fg)
    return im

SR, LEAD = 24000, 0.35
track = np.zeros(int(TOTAL * SR) + SR, dtype=np.float32)
t = 0.0
for sid, *_, secs in [(s[0], s[5]) for s in SCENES]:
    pass
t = 0.0
for s in SCENES:
    sid, secs = s[0], s[5]
    if sid in VO:
        with wave.open(f"{ROOT}/vo/{sid}.wav") as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        a *= 0.30 / max(np.sqrt((a ** 2).mean()), 1e-6)
        st = int((t + LEAD) * SR); track[st:st + len(a)] += a
    t += secs
track = np.clip(track[:int(TOTAL * SR)], -0.99, 0.99)
with wave.open(f"{ROOT}/mix.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype(np.int16).tobytes())
print(f"audio {TOTAL:.2f}s")

exe = imageio_ffmpeg.get_ffmpeg_exe()
proc = subprocess.Popen(
    [exe, "-y", "-loglevel", "error",
     "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-i", f"{ROOT}/mix.wav",
     "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-ar", "48000", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
     f"{ROOT}/malgap_no2.mp4"], stdin=subprocess.PIPE)
n = 0
for si, s in enumerate(SCENES):
    sid, mark, card, bg, fg, secs = s
    for fi in range(int(secs * FPS)):
        proc.stdin.write(frame(si, sid, mark, card, bg, fg, secs, fi).tobytes()); n += 1
    print(f"  {sid} ok")
proc.stdin.close(); proc.wait()
print("frames", n, "rc", proc.returncode)
