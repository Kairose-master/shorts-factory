"""「말값」 No.1 시그니처 — Ledger Noir 재제작.

철학: projects/malgap-style/philosophy.md · 레퍼런스: reference-board.png
경제학 각주: Chamberlin (1933) 독점적 경쟁 — 차별화된 이름은 가격 설정력을 만든다.
숫자 근거: 제로비 transcript verbatim — "3만 원이 넘습니다", "얼추 재료비 5,000원"(그의 추정).
"""
import math, json, wave, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.abspath(__file__))
STYLE = f"{ROOT}/../malgap-style"
W, H = 1080, 1920
BW, BH = 1240, 2200
FPS = 30

NIGHT_T = (16, 19, 30); NIGHT_B = (35, 40, 56)
PAPER = (242, 233, 220); INK = (20, 17, 15)
AMBER = (232, 163, 61);  STEEL = (91, 124, 153)
RED = (200, 69, 46);     WOOD = (58, 46, 40)
CUP = (210, 214, 222);   YOG = (238, 234, 224)
BERRY = (196, 62, 74);   CHOCO = (86, 62, 44)

SER = lambda s: ImageFont.truetype(f"{STYLE}/NotoSerifKR-Black.ttf", s)
SAN = lambda s: ImageFont.truetype(f"{ROOT}/NotoSansKR-Bold.ttf", s)

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

def footnote(d, lines, fg=PAPER, y0=None):
    y = y0 or BH - 330
    for i, t in enumerate(lines):
        ctext(d, BW/2, y + i*62, t, SAN(40 if i else 46),
              tuple(int(c*0.92) for c in fg) if i else fg)

def tag(d, fg=PAPER):
    d.text((84, 120), "「말값」 No.1", font=SAN(44), fill=fg)

def cup(d, cx, cy, s, with_spoon=True):
    """froyo cup: tapered clear cup, swirl, exactly three toppings."""
    top, bot, h = s*0.46, s*0.34, s*0.52
    d.polygon([(cx-top, cy-h), (cx+top, cy-h), (cx+bot, cy+h), (cx-bot, cy+h)],
              fill=(46, 52, 68), outline=CUP)
    d.polygon([(cx-top*0.55, cy-h), (cx-top*0.30, cy-h), (cx-bot*0.36, cy+h), (cx-bot*0.58, cy+h)],
              fill=(72, 80, 98))                                        # glass highlight
    d.line([(cx-top, cy-h), (cx+top, cy-h)], fill=CUP, width=6)
    for k in range(4):                                                   # yogurt swirl
        rw = s*(0.40 - k*0.085); ry = cy - h - s*0.10 - k*s*0.135
        d.ellipse([cx-rw, ry-s*0.09, cx+rw, ry+s*0.09], fill=YOG,
                  outline=tuple(int(c*0.82) for c in YOG))
    d.polygon([(cx-s*0.04, cy-h-s*0.62), (cx+s*0.10, cy-h-s*0.74), (cx+s*0.07, cy-h-s*0.56)],
              fill=YOG)                                                  # tip curl
    ty = cy - h - s*0.16                                                 # three toppings
    for ddx in (-0.16, -0.06, -0.11):
        d.ellipse([cx+s*ddx-s*0.05, ty-s*0.05, cx+s*ddx+s*0.05, ty+s*0.05], fill=BERRY)
    for ddx in (0.10, 0.20):
        m = s*0.055
        d.polygon([(cx+s*ddx, ty-m), (cx+s*ddx+m, ty), (cx+s*ddx, ty+m), (cx+s*ddx-m, ty)], fill=AMBER)
    for ddx in (0.01, 0.30):
        d.ellipse([cx+s*ddx-s*0.04, ty-s*0.14, cx+s*ddx+s*0.04, ty-s*0.06], fill=CHOCO)
    if with_spoon:
        d.line([(cx+top*0.7, cy-h-s*0.5), (cx+top*1.25, cy-h-s*1.0)], fill=PAPER, width=int(s*0.05))
        d.ellipse([cx+top*0.5, cy-h-s*0.62, cx+top*0.9, cy-h-s*0.38], fill=PAPER)

# ---------- bases ----------
def base_s1():
    im = night(); d = ImageDraw.Draw(im)
    d.polygon([(BW/2-90, 0), (BW/2+90, 0), (BW/2+430, 1660), (BW/2-430, 1660)],
              fill=(30, 32, 40))                                         # light cone body
    im = im.filter(ImageFilter.GaussianBlur(6))
    im = glow(im, BW/2, 1500, 470, (56, 46, 30)); d = ImageDraw.Draw(im)
    d.line([(90, 1665), (BW-90, 1665)], fill=(52, 56, 74), width=5)      # counter
    d.ellipse([BW/2-300, 1640, BW/2+300, 1698], fill=(10, 12, 20))       # shadow
    cup(d, BW/2, 1420, 420)
    ctext(d, BW/2, 300, "₩ ____", SER(250), PAPER, 9, INK)
    ctext(d, BW/2, 620, "단어 하나의 값", SAN(58), PAPER)
    tag(d); return im

def base_s2():
    im = Image.new("RGB", (BW, BH), PAPER); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 700, "시그", SER(360), INK)
    ctext(d, BW/2, 1150, "니처", SER(360), INK)
    d.line([(BW/2-330, 1660), (BW/2+330, 1646)], fill=INK, width=16)
    seal = Image.new("RGBA", (230, 230), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seal)
    sd.rectangle([8, 8, 222, 222], outline=RED, width=14)
    sd.text((115, 112), "말값", font=SAN(72), fill=RED, anchor="mm")
    seal = seal.rotate(-7, expand=True)
    im.paste(seal, (int(BW/2+265-seal.width/2), int(580-seal.height/2)), seal)
    footnote(d, ["값이 붙는 단어", "연작 첫 번째"], fg=INK)
    tag(d, INK); return im

def base_s3():
    im = night()
    im = glow(im, BW/2, 1150, 560, (58, 48, 32)); d = ImageDraw.Draw(im)
    d.ellipse([BW/2-380, 1730, BW/2+380, 1800], fill=(10, 12, 20))
    cup(d, BW/2, 1250, 760)
    ctext(d, BW/2, 1880, "토핑 세 개", SER(110), PAPER, 7, INK)
    footnote(d, ["재료의 전부"], y0=BH-160)
    tag(d); return im

def base_s4():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 900, 470, (86, 60, 22)); d = ImageDraw.Draw(im)
    d.line([(BW/2-200, 420), (BW/2-160, 640)], fill=(80, 82, 90), width=7)
    d.line([(BW/2+200, 420), (BW/2+160, 640)], fill=(80, 82, 90), width=7)
    d.rectangle([BW/2-430, 640, BW/2+430, 1240], fill=WOOD, outline=(28, 22, 18), width=10)
    d.rectangle([BW/2-404, 666, BW/2+404, 1214], outline=(122, 96, 60), width=5)
    ctext(d, BW/2, 700, "메뉴", SAN(54), tuple(int(c*0.8) for c in PAPER))
    ctext(d, BW/2, 800, "시그니처 요거트", SER(88), AMBER)
    ctext(d, BW/2, 910, "30,000원", SER(96), AMBER)
    d.line([(BW/2-330, 1052), (BW/2+330, 1052)], fill=(122, 96, 60), width=4)
    ctext(d, BW/2, 1075, "요거트", SER(80), PAPER)
    ctext(d, BW/2, 1175, "____원", SER(72), tuple(int(c*0.85) for c in PAPER))
    footnote(d, ["같은 컵, 다른 이름", "이름이 다르면 경쟁자가 없다 · Chamberlin (1933)"])
    tag(d); return im

def base_s5():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1050, 500, (52, 44, 30)); d = ImageDraw.Draw(im)
    cx, gy = BW/2, 1660
    d.rectangle([cx-190, gy, cx+190, gy+34], fill=(52, 56, 74))
    d.line([(cx, gy), (cx, 760)], fill=(150, 152, 160), width=14)
    tilt = 0.16                                                          # word side heavier
    bx0, by0 = cx-420, 760+int(-420*tilt); bx1, by1 = cx+420, 760+int(420*tilt)
    d.line([(bx0, by0), (bx1, by1)], fill=(170, 172, 180), width=13)
    d.ellipse([cx-16, 744, cx+16, 776], fill=(170, 172, 180))
    for px, py, side in ((bx0, by0, "L"), (bx1, by1, "R")):
        for off in (-120, 0, 120):
            d.line([(px, py), (px+off, py+150)], fill=(120, 122, 130), width=4)
        d.ellipse([px-160, py+140, px+160, py+205], fill=(60, 64, 80),
                  outline=(150, 152, 160), width=5)
        if side == "L":
            cup(d, px, py+40, 175, with_spoon=False)                     # light: the thing
        else:
            card = [px-150, py+30, px+150, py+140]
            d.rounded_rectangle(card, 18, fill=PAPER)
            ctext(d, px, py+48, "시그니처", SER(58), INK)                  # heavy: the word
    ctext(d, BW/2, 1820, "“얼추 재료비 5,000원…”", SER(88), PAPER, 6, INK)
    ctext(d, BW/2, 1950, "— 제로비의 추정, 검증 전", SAN(48), tuple(int(c*0.9) for c in PAPER))
    tag(d); return im

def base_s6():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 560, "말값", SER(300), PAPER)
    ctext(d, BW/2, 980, "=", SER(160), PAPER)
    ctext(d, BW/2, 1200, "30,000원", SER(170), PAPER)
    ctext(d, BW/2, 1440, "−  ____원", SER(150), PAPER)
    d.line([(BW/2+40, 1650), (BW/2+330, 1650)], fill=RED, width=14)
    seal = Image.new("RGBA", (190, 190), (0, 0, 0, 0))
    ImageDraw.Draw(seal).rectangle([6, 6, 184, 184], outline=RED, width=12)
    seal = seal.rotate(-7, expand=True)
    im.paste(seal, (BW-360, BH-560), seal)
    footnote(d, ["차별화된 이름은 가격을 스스로 정한다", "Chamberlin (1933) · 독점적 경쟁"], y0=BH-300)
    tag(d); return im

VO = {p["id"]: p for p in json.load(open(f"{ROOT}/vo-noir/lines.json"))}
SCENES = [
 ("s1", base_s1, 7.0, (1.10, 1.00, 0, -40), "motes"),
 ("s2", base_s2, 5.5, (1.00, 1.06, 0, 0),   None),
 ("s3", base_s3, 6.0, (1.12, 1.00, 0, 30),  "glint"),
 ("s4", base_s4, 5.5, (1.00, 1.07, 0, -25), "pulse"),
 ("s5", base_s5, 6.5, (1.08, 1.00, 0, 0),   None),
 ("s6", base_s6, 5.5, (1.00, 1.03, 0, 0),   "dot"),
]
TOTAL = sum(s[2] for s in SCENES)

yy, xx = np.mgrid[0:H, 0:W]
vig = (1 - 0.34*(((xx-W/2)/(W/2))**2 + ((yy-H/2)/(H/2))**2)**1.4)[..., None]

def kb_crop(base, p, kb):
    s0, s1, dx, dy = kb
    s = s0 + (s1-s0)*p
    cw, ch = int(W*s), int(H*s)
    cx = (BW-cw)/2 + dx*(1-p)*2
    cy = (BH-ch)/2 + dy*(1-p)*2
    return base.crop((int(cx), int(cy), int(cx+cw), int(cy+ch))).resize((W, H), Image.LANCZOS)

def animate(im, kind, tsec):
    d = ImageDraw.Draw(im, "RGBA")
    if kind == "motes":
        rng = np.random.default_rng(7)
        for k in range(10):
            x0 = W/2 + rng.uniform(-180, 180)
            y = (1500 - (tsec*46 + k*137) % 1200)
            d.ellipse([x0-3, y-3, x0+3, y+3], fill=(242, 233, 220, 60))
    elif kind == "glint":
        ph = tsec*2.4
        for k, (gx, gy) in enumerate([(W/2-70, 640), (W/2+95, 600), (W/2+10, 520)]):
            a = int(90*max(0, math.sin(ph+k*2.1)))
            d.line([(gx-14, gy), (gx+14, gy)], fill=(255, 255, 255, a), width=3)
            d.line([(gx, gy-14), (gx, gy+14)], fill=(255, 255, 255, a), width=3)
    elif kind == "pulse":
        a = int(26 + 20*math.sin(tsec*2.2))
        d.ellipse([W/2-330, 420, W/2+330, 1080], outline=(232, 163, 61, a), width=3)
    elif kind == "dot":
        r = 11 + 2.6*math.sin(tsec*3.1)
        d.ellipse([W/2-r, 300-r, W/2+r, 300+r], outline=PAPER, width=5)
    return im

SR, LEAD = 24000, 0.35
track = np.zeros(int(TOTAL*SR)+SR, dtype=np.float32); t = 0.0
for sid, _, secs, *_ in SCENES:
    if sid in VO:
        with wave.open(f"{ROOT}/vo-noir/{sid}.wav") as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
        a *= 0.30/max(np.sqrt((a**2).mean()), 1e-6)
        st = int((t+LEAD)*SR); track[st:st+len(a)] += a
    t += secs
track = np.clip(track[:int(TOTAL*SR)], -0.99, 0.99)
with wave.open(f"{ROOT}/mix-noir.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track*32767).astype(np.int16).tobytes())

exe = imageio_ffmpeg.get_ffmpeg_exe()
proc = subprocess.Popen(
    [exe, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
     "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", f"{ROOT}/mix-noir.wav",
     "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-ar", "48000", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
     f"{ROOT}/malgap_no1.mp4"], stdin=subprocess.PIPE)
n = 0
for si, (sid, builder, secs, kb, anim) in enumerate(SCENES):
    base = builder()
    gc = {}
    for fi in range(int(secs*FPS)):
        p = fi/FPS/secs
        im = kb_crop(base, p, kb)
        if anim: im = animate(im, anim, fi/FPS)
        gk = fi//3
        if gk not in gc:
            gc = {gk: np.random.default_rng(si*991+gk).integers(-5, 6, (H, W, 1))}
        arr = np.clip((np.asarray(im).astype(np.int16)+gc[gk])*vig, 0, 255).astype(np.uint8)
        proc.stdin.write(arr.tobytes()); n += 1
    print(f"  {sid} ok ({n})")
proc.stdin.close(); proc.wait()
print("frames", n, "rc", proc.returncode)
