"""EP1 v2 — 실측 Shorts 인터페이스(슬라쇼츠TV형) + remotion-motion-graphics 규율 적용.

v1 대비: 상단 노랑 타이틀 밴드(다속성 입장·스태거), 하단 노랑 칩 자막(구절 동기화·
팝 입장), 씬 아트는 밴드 아래로 재배치, KB 줌도 ease 적용(선형 금지).
"""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../../malgap-style")
from noir_kit import *
import shorts_ui as UI
from PIL import Image, ImageDraw
import numpy as _np

TOP = 560   # 밴드 아래 안전선

def truck(d, x, y, s=1.0, col=(150, 152, 160)):
    d.rounded_rectangle([x, y-46*s, x+150*s, y], 8, fill=col)
    d.rounded_rectangle([x+150*s, y-34*s, x+205*s, y], 6, fill=col)
    for wx in (x+40*s, x+170*s):
        d.ellipse([wx-16*s, y-8*s, wx+16*s, y+24*s], fill=(30, 32, 40), outline=col, width=4)

def b1():
    im = night(); d = ImageDraw.Draw(im)
    pts = [(180, TOP+120), (420, TOP+20), (700, TOP+60), (960, TOP-30), (1120, TOP+140),
           (1050, TOP+400), (820, TOP+510), (560, TOP+460), (330, TOP+510), (200, TOP+340)]
    d.polygon(pts, fill=(26, 30, 42), outline=(90, 96, 112))
    im = glow(im, 660, TOP+260, 330, (52, 46, 30)); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+560, "1946", SER(200), PAPER, 9, INK)
    for k in range(3):
        truck(d, 300+k*260, 1560+k*80, 1.0-k*0.12)
    d.line([(880, 1530), (1060, 1440)], fill=AMBER, width=10)
    d.polygon([(1060, 1440), (990, 1440), (1040, 1385)], fill=AMBER)
    return im

def b2():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([BW/2-330, TOP, BW/2+330, TOP+680], fill=PAPER)
    for k in range(8):
        w = 480 - (k % 3)*90
        d.line([(BW/2-260, TOP+110+k*62), (BW/2-260+w, TOP+110+k*62)], fill=(150, 140, 124), width=9)
    st = seal_word("履行"); im.paste(st, (int(BW/2+120), TOP+500), st)
    y = 1500
    for k in range(4):
        d.rectangle([200+k*230, y, 380+k*230, y+150], fill=WOOD, outline=(28, 22, 18), width=7)
        d.line([(200+k*230, y+75), (380+k*230, y+75)], fill=(122, 96, 60), width=5)
    d.line([(BW/2, TOP+740), (BW/2, 1450)], fill=AMBER, width=10)
    d.polygon([(BW/2-34, 1410), (BW/2+34, 1410), (BW/2, 1472)], fill=AMBER)
    return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    ox, oy = 220, 1600
    d.line([(ox, oy), (ox, TOP+120)], fill=(150, 152, 160), width=8)
    d.line([(ox, oy), (BW-160, oy)], fill=(150, 152, 160), width=8)
    pts = [(ox+40+i*70, oy-90-(1.55**i)*14) for i in range(10)]
    pts += [(pts[-1][0]+70+i*60, pts[-1][1]) for i in range(3)]
    d.line(pts[:10], fill=RED, width=11, joint="curve")
    d.line(pts[9:], fill=AMBER, width=12)
    d.rounded_rectangle([BW/2-260, TOP, BW/2+260, TOP+180], 18, fill=(46, 52, 68),
                        outline=PAPER, width=6)
    d.ellipse([BW/2-70, TOP+20, BW/2+70, TOP+160], outline=PAPER, width=6)
    ctext(d, BW/2, TOP+48, "圓", SAN(84), PAPER)
    ctext(d, BW/2+240, TOP+230, "1948", SER(110), PAPER, 7, INK)
    return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    for k, (mx, mh) in enumerate([(260, 380), (560, 520), (880, 430), (1080, 340)]):
        d.polygon([(mx-260, 1560), (mx, 1560-mh), (mx+260, 1560)], fill=(20, 24, 34))
    d.rectangle([0, 1560, BW, 2200], fill=(14, 17, 26))
    d.rectangle([BW-360, TOP+60, BW-160, TOP+440], fill=(22, 25, 36), outline=(70, 74, 88), width=6)
    d.rectangle([BW-320, TOP+120, BW-270, TOP+190], fill=AMBER)
    for wx in (BW-320, BW-250):
        for wy in (TOP+220, TOP+300, TOP+370):
            d.rectangle([wx, wy, wx+50, wy+58], fill=(30, 33, 46))
    ctext(d, 360, TOP+60, "1949", SER(130), PAPER, 8, INK)
    ctext(d, BW-500, TOP+200, "1956", SER(80), tuple(int(c*0.9) for c in PAPER), 5, INK, anchor="ra")
    return im

def b5():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1150, 430, (40, 38, 32)); d = ImageDraw.Draw(im)
    d.rectangle([BW/2-14, TOP+160, BW/2+14, 1620], fill=(70, 72, 84))
    d.ellipse([BW/2-26, TOP+120, BW/2+26, TOP+172], fill=(70, 72, 84))
    d.rectangle([BW/2-220, 1620, BW/2+220, 1700], fill=(34, 36, 46))
    return im

def b6():
    im = night(); d = ImageDraw.Draw(im)
    data = [("1978", "난징의 봄"), ("1987", "계엄 해제"), ("1993", "첫 직선제")]
    for k, (yr, label) in enumerate(data):
        y = TOP+80 + k*360
        d.line([(200, y+140), (BW-200, y+140)], fill=(60, 64, 80), width=4)
        d.ellipse([250-16, y+124, 250+16, y+156], fill=AMBER)
        ctext(d, 480, y, yr, SER(110), PAPER, 6, INK, anchor="la")
        d.text((480, y+140), label, font=SAN(52), fill=tuple(int(c*0.92) for c in PAPER))
    return im

def b7():
    im = night(); d = ImageDraw.Draw(im)
    for k, (x0, hgt) in enumerate([(120, 450), (330, 650), (560, 820), (800, 580), (1010, 500)]):
        d.rectangle([x0, 1950-hgt, x0+170, 1950], fill=(22, 26, 38))
        rng = _np.random.default_rng(k)
        for _ in range(10):
            wx = int(rng.uniform(x0+16, x0+130)); wy = int(rng.uniform(1950-hgt+30, 1890))
            d.rectangle([wx, wy, wx+22, wy+28], fill=(120, 96, 44))
    cols = [RED, AMBER, STEEL, (110, 168, 92), PAPER, (150, 110, 170)]
    cx, cy = BW/2, TOP+620
    for i, col in enumerate(cols):
        a0 = math.pi + i*math.pi/6
        for r in (300, 380, 460):
            x, y = cx+math.cos(a0+math.pi/12)*r, cy+math.sin(a0+math.pi/12)*r
            d.ellipse([x-26, y-26, x+26, y+26], fill=col)
    return im

def b8():
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([120, TOP+40, BW/2-40, TOP+540], 30, fill=(46, 30, 28), outline=RED, width=8)
    ctext(d, (120+BW/2-40)/2, TOP+100, "보수당", SAN(60), PAPER)
    ctext(d, (120+BW/2-40)/2, TOP+230, "복지", SER(140), PAPER)
    ctext(d, (120+BW/2-40)/2, TOP+420, "확대", SER(84), PAPER)
    d.rounded_rectangle([BW/2+40, TOP+380, BW-120, TOP+880], 30, fill=(28, 36, 48), outline=STEEL, width=8)
    ctext(d, (BW/2+40+BW-120)/2, TOP+440, "진보당", SAN(60), PAPER)
    ctext(d, (BW/2+40+BW-120)/2, TOP+580, "민영화", SER(120), PAPER)
    return im

def b9():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+150, "누가 보수고", SER(140), PAPER)
    ctext(d, BW/2, TOP+370, "누가 진보인가", SER(140), PAPER)
    redbar(d, TOP+740, "당신의 답을 남겨주세요")
    ctext(d, BW/2, BH-420, "EP2. 자유중국의 보수는 누구인가", SAN(44),
          tuple(int(c*0.85) for c in PAPER))
    return im

VOJ = json.load(open(f"{ROOT}/vo/lines.json"))
GAP = 0.12
SC = []
t0 = 0.0
for p in VOJ:
    secs = p["dur"]+GAP + (1.0 if p["id"] == "s9" else 0)
    SC.append({"id": p["id"], "secs": secs, "text": p["text"], "t0": t0,
               "chips": UI.chunks_for(p["text"], p["dur"]+0.15)})
    t0 += secs
print(f"audio {mix_audio([(s['id'], s['secs']) for s in SC], f'{ROOT}/vo', f'{ROOT}/mix.wav', lead=0.15):.2f}s")

BULD = [b1, b2, b3, b4, b5, b6, b7, b8, b9]
def smooth(p): return p*p*(3-2*p)   # KB도 선형 금지

def make_anim(si, sc):
    def anim(im, t):
        tv = sc["t0"] + t
        UI.title_band(im, "중국이 공산화되지", "않았다면?",
                      tv if si == 0 else 10.0)
        for c, cs, cd in sc["chips"]:
            if cs <= t < cs+cd+0.10:
                UI.chip(im, c, t-cs)
                break
        return im
    return anim

SCENES = []
for i, sc in enumerate(SC):
    kb = (1.07, 1.00, 0, -25) if i % 2 == 0 else (1.00, 1.06, 15, 0)
    SCENES.append((BULD[i], sc["secs"], kb, make_anim(i, sc)))

# eased KB: monkeypatch kb_crop progress
import noir_kit as NK
_orig = NK.kb_crop
def eased_kb(base, p, kb): return _orig(base, smooth(p), kb)
NK.kb_crop = eased_kb
import importlib
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep1_v2.mp4", seed0=950, trans=0.20)
print("frames", n, "rc", rc)
