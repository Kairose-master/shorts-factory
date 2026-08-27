"""Ledger Noir 공용 렌더 킷 — No.1/No.2 재제작이 공유하는 헬퍼.
철학: philosophy.md · 레퍼런스: reference-board.png + references.md"""
import math, wave, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg, os

W, H = 1080, 1920
BW, BH = 1240, 2200
FPS = 30
NIGHT_T = (16, 19, 30); NIGHT_B = (35, 40, 56)
PAPER = (242, 233, 220); INK = (20, 17, 15)
AMBER = (232, 163, 61);  STEEL = (91, 124, 153)
RED = (200, 69, 46);     WOOD = (58, 46, 40)
BRASS = (156, 126, 78)

_STYLE = os.path.dirname(os.path.abspath(__file__))
SER = lambda s: ImageFont.truetype(f"{_STYLE}/NotoSerifKR-Black.ttf", s)
SAN = lambda s: ImageFont.truetype(f"{_STYLE}/../malgap-ep1/NotoSansKR-Bold.ttf", s)

def night(w=BW, h=BH):
    g = np.linspace(0, 1, h)[:, None]
    arr = (np.array(NIGHT_T)[None, None, :] * (1 - g[..., None]) +
           np.array(NIGHT_B)[None, None, :] * g[..., None]).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, w, axis=1))

def glow(im, cx, cy, r, color, blur=0.55):
    layer = Image.new("RGB", im.size, (0, 0, 0))
    ImageDraw.Draw(layer).ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(r*blur))
    return Image.fromarray(np.minimum(255, np.asarray(im).astype(int)+np.asarray(layer)).astype(np.uint8))

def ctext(d, cx, y, txt, font, fill, stroke=0, sfill=None, anchor="ma"):
    d.text((cx, y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill, anchor=anchor)

def redbar(d, cy, txt, size=56):
    """Kruger 계보의 선언 바 — 흰 글자, 붉은 띠. 원작 모사 아님, 어법 인용."""
    f = SAN(size)
    bb = d.textbbox((0, 0), txt, font=f)
    w = bb[2]-bb[0]+120
    d.rectangle([BW/2-w/2, cy, BW/2+w/2, cy+size+44], fill=RED)
    d.text((BW/2, cy+22), txt, font=f, fill=PAPER, anchor="ma")

def seal_empty(size=190):
    seal = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(seal).rectangle([6, 6, size-6, size-6], outline=RED, width=12)
    return seal.rotate(-7, expand=True)

def seal_word(txt="말값", size=230):
    seal = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seal)
    sd.rectangle([8, 8, size-8, size-8], outline=RED, width=14)
    sd.text((size//2, size//2-3), txt, font=SAN(int(size*0.31)), fill=RED, anchor="mm")
    return seal.rotate(-7, expand=True)

_yy, _xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.34*(((_xx-W/2)/(W/2))**2 + ((_yy-H/2)/(H/2))**2)**1.4)[..., None]

def kb_crop(base, p, kb):
    s0, s1, dx, dy = kb
    s = s0 + (s1-s0)*p
    cw, ch = int(W*s), int(H*s)
    cx = (BW-cw)/2 + dx*(1-p)*2
    cy = (BH-ch)/2 + dy*(1-p)*2
    return base.crop((int(cx), int(cy), int(cx+cw), int(cy+ch))).resize((W, H), Image.LANCZOS)

def mix_audio(scenes, vo_dir, out_wav, lead=0.22):
    """scenes: [(sid, secs)] — 내레이션을 씬 앞에 붙이고 전체 트랙 생성."""
    SR = 24000
    total = sum(s for _, s in scenes)
    track = np.zeros(int(total*SR)+SR, dtype=np.float32); t = 0.0
    for sid, secs in scenes:
        p = f"{vo_dir}/{sid}.wav"
        if os.path.exists(p):
            with wave.open(p) as w:
                a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
            a *= 0.30/max(np.sqrt((a**2).mean()), 1e-6)
            st = int((t+lead)*SR); track[st:st+len(a)] += a
        t += secs
    track = np.clip(track[:int(total*SR)], -0.99, 0.99)
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((track*32767).astype(np.int16).tobytes())
    return total

def encode(scenes, mix_wav, out_mp4, seed0=0):
    """scenes: [(builder, secs, kb, anim_fn|None)] — KB+그레인+비네트로 파이프 인코딩."""
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen(
        [exe, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix_wav,
         "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-ar", "48000", "-b:a", "160k", "-shortest",
         "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    n = 0
    for si, (builder, secs, kb, anim) in enumerate(scenes):
        base = builder()
        gc = {}
        for fi in range(int(secs*FPS)):
            p = fi/FPS/secs
            im = kb_crop(base, p, kb)
            if anim: im = anim(im, fi/FPS)
            gk = fi//3
            if gk not in gc:
                gc = {gk: np.random.default_rng(seed0+si*991+gk).integers(-5, 6, (H, W, 1))}
            arr = np.clip((np.asarray(im).astype(np.int16)+gc[gk])*VIG, 0, 255).astype(np.uint8)
            proc.stdin.write(arr.tobytes()); n += 1
        print(f"  scene{si+1} ok ({n})")
    proc.stdin.close(); proc.wait()
    return n, proc.returncode
