"""「말값」 No.2 정통 — Ledger Noir 렌더러.

디자인 철학: projects/malgap-style/philosophy.md (canvas-design 1단계 산출물)
레퍼런스: projects/malgap-style/reference-board.png — 9채널 썸네일 실측
경제학 각주: Akerlof (1970) 정보 비대칭 / Spence (1973) 신호 이론
"""
import math, json, wave, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.abspath(__file__))
STYLE = f"{ROOT}/../malgap-style"
W, H = 1080, 1920            # output
BW, BH = 1240, 2200          # illustrated base (Ken Burns headroom)
FPS = 30

NIGHT_T = (16, 19, 30); NIGHT_B = (35, 40, 56)
PAPER = (242, 233, 220); INK = (20, 17, 15)
AMBER = (232, 163, 61);  STEEL = (91, 124, 153)
RED = (200, 69, 46);     BRASS = (156, 126, 78)
BROTH = (216, 212, 196); WOOD = (58, 46, 40)

SER = lambda s: ImageFont.truetype(f"{STYLE}/NotoSerifKR-Black.ttf", s)
SAN = lambda s: ImageFont.truetype(f"{ROOT}/../malgap-ep1/NotoSansKR-Bold.ttf", s)

def night(w=BW, h=BH):
    g = np.linspace(0, 1, h)[:, None]
    arr = (np.array(NIGHT_T)[None, None, :] * (1 - g[..., None]) +
           np.array(NIGHT_B)[None, None, :] * g[..., None]).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, w, axis=1))

def glow(im, cx, cy, r, color, strength=1.0):
    layer = Image.new("RGB", im.size, (0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(int(c * strength) for c in color))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.55))
    return Image.fromarray(np.minimum(255, np.asarray(im).astype(int) + np.asarray(layer)).astype(np.uint8))

def ctext(d, cx, y, txt, font, fill, stroke=0, sfill=None, anchor="ma"):
    d.text((cx, y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill, anchor=anchor)

def footnote(d, lines, fg=PAPER, y0=None):
    y = y0 or BH - 330
    for i, t in enumerate(lines):
        ctext(d, BW / 2, y + i * 62, t, SAN(40 if i else 46), tuple(int(c*0.92) for c in fg) if i else fg)

def tag(d, fg=PAPER):
    d.text((84, 120), "「말값」 No.2", font=SAN(44), fill=fg)

# ---------- illustrated bases ----------
def base_s1():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1450, 560, (60, 50, 34)); d = ImageDraw.Draw(im)
    d.line([(70, 1815), (BW-70, 1815)], fill=(52, 56, 74), width=4)              # table edge
    cx, cy = BW/2, 1500
    d.ellipse([cx-430, cy+180, cx+430, cy+280], fill=(10, 12, 20))               # shadow
    d.polygon([(cx-420, cy-60), (cx+420, cy-60), (cx+290, cy+220), (cx-290, cy+220)], fill=BRASS)
    d.polygon([(cx-420, cy-60), (cx+420, cy-60), (cx+405, cy-10), (cx-405, cy-10)],
              fill=tuple(int(c*1.22) for c in BRASS))                            # rim light band
    d.ellipse([cx-150, cy+220, cx+150, cy+280], fill=tuple(int(c*0.7) for c in BRASS))
    d.ellipse([cx-400, cy-125, cx+400, cy+5], fill=tuple(int(c*0.55) for c in BRASS))
    d.ellipse([cx-372, cy-112, cx+372, cy-8], fill=BROTH)                        # broth
    for k in range(5):                                                            # noodle swirl
        rr = 210 - k*38
        d.arc([cx-rr, cy-60-rr//3, cx+rr, cy-60+rr//3], 15+k*9, 330-k*12,
              fill=(74, 60, 48), width=13)
    d.ellipse([cx+120, cy-108, cx+260, cy-38], fill=PAPER)                       # egg
    d.ellipse([cx+158, cy-90, cx+225, cy-56], fill=AMBER)
    for i in range(3):                                                            # cucumber
        d.polygon([(cx-260+i*36, cy-104), (cx-236+i*36, cy-108), (cx-196+i*36, cy-56),
                   (cx-220+i*36, cy-52)], fill=STEEL)
    d.line([(cx-330, cy-260), (cx+150, cy-64)], fill=PAPER, width=11)            # chopsticks
    d.line([(cx-330, cy-236), (cx+162, cy-78)], fill=tuple(int(c*0.8) for c in PAPER), width=11)
    ctext(d, BW/2, 320, "16,000", SER(280), PAPER, 10, INK)                      # monument
    ctext(d, BW/2, 660, "냉면 한 그릇 — 만육천 원", SAN(58), PAPER)
    tag(d); return im

def base_s2():
    im = Image.new("RGB", (BW, BH), PAPER); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 760, "정", SER(430), INK)
    ctext(d, BW/2, 1250, "통", SER(430), INK)
    d.line([(BW/2-330, 1810), (BW/2+330, 1795)], fill=INK, width=16)             # brush stroke
    sx, sy = BW/2+275, 640                                                        # unstamped seal
    seal = Image.new("RGBA", (230, 230), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seal)
    sd.rectangle([8, 8, 222, 222], outline=RED, width=14)
    sd.text((115, 112), "말값", font=SAN(72), fill=RED, anchor="mm")
    seal = seal.rotate(-7, expand=True)
    im.paste(seal, (int(sx-seal.width/2), int(sy-seal.height/2)), seal)
    footnote(d, ["값이 붙는 단어", "연작 두 번째"], fg=INK)
    tag(d, INK); return im

def base_s3():
    im = night(); d = ImageDraw.Draw(im)
    for x0, x1, ht in [(0, 300, 620), (BW-270, BW, 540), (250, 430, 760), (BW-460, BW-250, 820)]:
        d.rectangle([x0, ht, x1, 1980], fill=(12, 15, 23))                        # buildings
        rng = np.random.default_rng(x0)
        for _ in range(4):
            wx = int(rng.uniform(x0+24, x1-52)); wy = int(rng.uniform(ht+60, 1700))
            d.rectangle([wx, wy, wx+30, wy+42], fill=(120, 90, 40))
    im = glow(im, BW/2, 880, 430, (95, 66, 22)); d = ImageDraw.Draw(im)          # sign halo
    d.line([(BW/2-190, 480), (BW/2-150, 700)], fill=(80, 82, 90), width=7)       # chains
    d.line([(BW/2+190, 480), (BW/2+150, 700)], fill=(80, 82, 90), width=7)
    d.rectangle([BW/2-320, 700, BW/2+320, 1060], fill=WOOD, outline=(28, 22, 18), width=10)
    d.rectangle([BW/2-296, 724, BW/2+296, 1036], outline=(122, 96, 60), width=5)
    ctext(d, BW/2, 770, "원조 평양옥", SER(120), AMBER)
    ctext(d, BW/2, 930, "since 19__", SAN(64), tuple(int(c*0.85) for c in PAPER))
    d.polygon([(BW/2-260, 1975), (BW/2+260, 1975), (BW/2+180, 1810), (BW/2-180, 1810)],
              fill=(26, 24, 20))                                                  # doorway light spill
    footnote(d, ["1단계 — 오래된 간판", "간판은 신호다 · Spence (1973)"])
    tag(d); return im

def base_s4():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([0, 1740, BW, 2200], fill=(20, 23, 34))                           # ground
    lx = BW - 240
    d.line([(lx, 420), (lx, 1760)], fill=(60, 63, 74), width=16)                  # lamppost
    d.line([(lx, 420), (lx-140, 470)], fill=(60, 63, 74), width=12)
    d.ellipse([lx-190, 440, lx-110, 510], fill=AMBER)
    im = glow(im, lx-150, 480, 330, (110, 76, 24)); d = ImageDraw.Draw(im)
    door_x = 130
    d.rectangle([door_x-70, 1150, door_x+90, 1760], fill=(30, 26, 20))
    d.rectangle([door_x-40, 1210, door_x+60, 1760], fill=(180, 130, 50))          # lit door
    hs = [(920, 1.00), (790, .96), (665, 1.03), (545, .94), (430, 1.0), (325, .97), (230, .92)]
    for i, (px, sc) in enumerate(hs):                                             # queue silhouettes
        hh = int(300 * sc); top = 1760 - hh
        col = (9, 11, 17)
        d.ellipse([px-34, top, px+34, top+72], fill=col)
        d.rounded_rectangle([px-52, top+62, px+52, 1760], 30, fill=col)
        d.polygon([(px-46, 1760), (px+46, 1760), (px+150+i*8, 1855), (px+30+i*8, 1855)],
                  fill=(14, 16, 24))                                              # long shadow
        d.line([(px-52, top+95), (px+52, top+95)], fill=(190, 140, 60), width=4)  # rim light
    footnote(d, ["2단계 — 줄", "맛은 먹기 전에 알 수 없다 · Akerlof (1970)"])
    tag(d); return im

def base_s5():
    im = night(); d = ImageDraw.Draw(im)
    cx, cy, R = BW/2, 1150, 470
    d.ellipse([cx-R-60, cy-R-60, cx+R+60, cy+R+60], fill=(24, 27, 40))            # table ring
    d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=BRASS)
    d.ellipse([cx-R+42, cy-R+42, cx+R-42, cy+R-42], fill=tuple(int(c*0.62) for c in BRASS))
    d.ellipse([cx-R+58, cy-R+58, cx+R-58, cy+R-58], fill=(226, 223, 210))         # very pale broth
    for k in range(3):                                                             # sparse noodles
        rr = 120 - k*34
        d.arc([cx-rr, cy-rr, cx+rr, cy+rr], 30+k*40, 260+k*30, fill=(150, 138, 118), width=9)
    d.polygon([(cx-180, cy-210), (cx-90, cy-260), (cx-60, cy-215), (cx-150, cy-170)],
              fill=(238, 240, 240))                                               # ice
    d.polygon([(cx+120, cy+150), (cx+205, cy+120), (cx+230, cy+185), (cx+150, cy+210)],
              fill=(232, 236, 238))
    d.line([(cx+220, cy-420), (cx+470, cy+150)], fill=PAPER, width=12)            # chopstick
    ctext(d, BW/2, 1780, "“걸레 빤 물”", SER(120), PAPER, 8, INK)
    ctext(d, BW/2, 1945, "— 실제로 붙은 비판", SAN(52), tuple(int(c*0.9) for c in PAPER))
    tag(d); return im

def base_s6():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 560, "말값", SER(300), PAPER)
    ctext(d, BW/2, 980, "=", SER(160), PAPER)
    ctext(d, BW/2, 1200, "16,000원", SER(170), PAPER)
    ctext(d, BW/2, 1440, "−  ____원", SER(150), PAPER)
    d.line([(BW/2+40, 1650), (BW/2+330, 1650)], fill=RED, width=14)               # blank underline
    seal = Image.new("RGBA", (190, 190), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seal); sd.rectangle([6, 6, 184, 184], outline=RED, width=12)
    seal = seal.rotate(-7, expand=True)
    im.paste(seal, (BW-360, BH-560), seal)                                        # empty seal: 찍히지 않은 인주
    footnote(d, ["정보가 비대칭일 때, 신호에 값이 붙는다", "Akerlof (1970) · Spence (1973)"], y0=BH-300)
    tag(d); return im

# ---------- animation ----------
VO = {p["id"]: p for p in json.load(open(f"{ROOT}/vo/lines.json"))}
SCENES = [
 ("s1", base_s1, 6.0, (1.10, 1.00, 0, -40), "steam"),
 ("s2", base_s2, 5.5, (1.00, 1.06, 0, 0),   None),
 ("s3", base_s3, 6.0, (1.08, 1.00, 30, 0),  "pulse"),
 ("s4", base_s4, 5.0, (1.00, 1.07, -35, 0), "pulse"),
 ("s5", base_s5, 7.5, (1.12, 1.00, 0, 30),  "ripple"),
 ("s6", base_s6, 5.5, (1.00, 1.03, 0, 0),   "dot"),
]
TOTAL = sum(s[2] for s in SCENES)

yy, xx = np.mgrid[0:H, 0:W]
vig = 1 - 0.34 * (((xx - W/2) / (W/2)) ** 2 + ((yy - H/2) / (H/2)) ** 2) ** 1.4
vig = vig[..., None]

def kb_crop(base, p, kb):
    s0, s1, dx, dy = kb
    s = s0 + (s1 - s0) * p
    cw, ch = int(W * s), int(H * s)
    cx = (BW - cw) / 2 + dx * (1 - p) * 2
    cy = (BH - ch) / 2 + dy * (1 - p) * 2
    return base.crop((int(cx), int(cy), int(cx + cw), int(cy + ch))).resize((W, H), Image.LANCZOS)

def animate(im, kind, p, rng):
    d = ImageDraw.Draw(im, "RGBA")
    if kind == "steam":
        for k in range(3):
            ph = p * math.tau * 1.2 + k * 2.1
            pts = [(W/2 + (k-1)*120 + math.sin(t/9*5 + ph)*46*(1 - t/9*0.4),
                    1120 - t * 52) for t in range(10)]
            d.line(pts, fill=(242, 233, 220, 46), width=16, joint="curve")
    elif kind == "ripple":
        r = 90 + (p * 260) % 260
        a = max(0, int(70 * (1 - r/350)))
        d.ellipse([W/2-r, 960-r*0.94, W/2+r, 960+r*0.94], outline=(255, 255, 255, a), width=4)
    elif kind == "dot":
        r = 11 + 2.6 * math.sin(p * math.tau * 2)
        d.ellipse([W/2-r, 300-r, W/2+r, 300+r], outline=PAPER, width=5)
    return im

# ---------- audio (reuse) ----------
SR, LEAD = 24000, 0.35
track = np.zeros(int(TOTAL*SR)+SR, dtype=np.float32); t = 0.0
for sid, _, secs, *_ in SCENES:
    if sid in VO:
        with wave.open(f"{ROOT}/vo/{sid}.wav") as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
        a *= 0.30/max(np.sqrt((a**2).mean()), 1e-6)
        st = int((t+LEAD)*SR); track[st:st+len(a)] += a
    t += secs
track = np.clip(track[:int(TOTAL*SR)], -0.99, 0.99)
with wave.open(f"{ROOT}/mix.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track*32767).astype(np.int16).tobytes())

exe = imageio_ffmpeg.get_ffmpeg_exe()
proc = subprocess.Popen(
    [exe,"-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}",
     "-r",str(FPS),"-i","-","-i",f"{ROOT}/mix.wav",
     "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",
     "-c:a","aac","-ar","48000","-b:a","160k","-shortest","-movflags","+faststart",
     f"{ROOT}/malgap_no2.mp4"], stdin=subprocess.PIPE)
n = 0
for si, (sid, builder, secs, kb, anim) in enumerate(SCENES):
    base = builder()
    grain_cache = {}
    for fi in range(int(secs * FPS)):
        p = fi / FPS / secs
        im = kb_crop(base, p, kb)
        if anim: im = animate(im, anim, fi / FPS / 2.2, None)
        gk = fi // 3
        if gk not in grain_cache:
            grain_cache = {gk: np.random.default_rng(si*997+gk).integers(-7, 8, (H, W, 1))}
        arr = np.asarray(im).astype(np.int16) + grain_cache[gk]
        arr = np.clip(arr * vig, 0, 255).astype(np.uint8)
        proc.stdin.write(arr.tobytes()); n += 1
    print(f"  {sid} ok ({n})")
proc.stdin.close(); proc.wait()
print("frames", n, "rc", proc.returncode)
