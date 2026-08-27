"""「자유중국」 EP1 숏폼판 — 트럭과 환율의 서사. noir_kit 기반 아카이브 노이르."""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw
import numpy as _np

def tag(d, fg=PAPER): d.text((84, 120), "「자유중국」 EP1", font=SAN(44), fill=fg)

def truck(d, x, y, s=1.0, col=(150, 152, 160)):
    d.rounded_rectangle([x, y-46*s, x+150*s, y], 8, fill=col)
    d.rounded_rectangle([x+150*s, y-34*s, x+205*s, y], 6, fill=col)
    for wx in (x+40*s, x+170*s):
        d.ellipse([wx-16*s, y-8*s, wx+16*s, y+24*s], fill=(30, 32, 40), outline=col, width=4)

def b1():
    im = night(); d = ImageDraw.Draw(im)
    pts = [(180, 620), (420, 520), (700, 560), (960, 470), (1120, 640), (1050, 900),
           (820, 1010), (560, 960), (330, 1010), (200, 840)]                       # 만주 실루엣(양식화)
    d.polygon(pts, fill=(26, 30, 42), outline=(90, 96, 112))
    im = glow(im, 660, 760, 330, (52, 46, 30)); d = ImageDraw.Draw(im)
    for k in range(3):
        truck(d, 300+k*260, 1450+k*90, 1.0-k*0.12)
    d.line([(880, 1420), (1060, 1330)], fill=AMBER, width=10)                      # 방향 전환 화살표
    d.polygon([(1060, 1330), (990, 1330), (1040, 1275)], fill=AMBER)
    ctext(d, BW/2, 250, "1946", SER(230), PAPER, 9, INK)
    ctext(d, BW/2, 540, "만주 · 트럭 3만 대", SAN(56), PAPER)
    tag(d); return im

def b2():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([BW/2-330, 430, BW/2+330, 1150], fill=PAPER)                       # 조약문
    for k in range(9):
        w = 480 - (k % 3)*90
        d.line([(BW/2-260, 540+k*62), (BW/2-260+w, 540+k*62)], fill=(150, 140, 124), width=9)
    st = seal_word("履行"); im.paste(st, (int(BW/2+120), 960), st)
    y = 1450
    for k in range(4):                                                              # 무기 궤짝
        d.rectangle([200+k*230, y, 380+k*230, y+150], fill=WOOD, outline=(28, 22, 18), width=7)
        d.line([(200+k*230, y+75), (380+k*230, y+75)], fill=(122, 96, 60), width=5)
    d.line([(BW/2, 1290), (BW/2, 1400)], fill=AMBER, width=10)
    d.polygon([(BW/2-34, 1360), (BW/2+34, 1360), (BW/2, 1425)], fill=AMBER)
    ctext(d, BW/2, 260, "조약 이행", SER(120), PAPER, 7, INK)
    ctext(d, BW/2, 1680, "무기고 → 국민정부군", SAN(54), PAPER)
    tag(d); return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    ox, oy = 220, 1500
    d.line([(ox, oy), (ox, 560)], fill=(150, 152, 160), width=8)
    d.line([(ox, oy), (BW-160, oy)], fill=(150, 152, 160), width=8)
    pts = [(ox+40+i*70, oy-90-(1.55**i)*14) for i in range(10)]                     # 폭주하던 물가
    pts += [(pts[-1][0]+70+i*60, pts[-1][1]) for i in range(3)]                     # 멈춤
    d.line(pts[:10], fill=RED, width=11, joint="curve")
    d.line(pts[9:], fill=AMBER, width=12)
    d.rounded_rectangle([BW/2-260, 380, BW/2+260, 560], 18, fill=(46, 52, 68),
                        outline=PAPER, width=6)                                     # 지폐
    d.ellipse([BW/2-70, 400, BW/2+70, 540], outline=PAPER, width=6)
    ctext(d, BW/2, 428, "圓", SAN(84), PAPER)
    ctext(d, BW/2, 200, "1948", SER(160), PAPER, 8, INK)
    ctext(d, BW/2, 1620, "인플레이션, 멈추다", SAN(56), PAPER)
    tag(d); return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    for k, (mx, mh) in enumerate([(260, 420), (560, 560), (880, 470), (1080, 380)]):
        d.polygon([(mx-260, 1450), (mx, 1450-mh), (mx+260, 1450)], fill=(20, 24, 34))  # 옌안 산
    d.rectangle([0, 1450, BW, 2200], fill=(14, 17, 26))
    d.rectangle([BW-360, 520, BW-160, 900], fill=(22, 25, 36), outline=(70, 74, 88), width=6)  # 모스크바 아파트
    d.rectangle([BW-320, 580, BW-270, 650], fill=AMBER)                             # 불 켜진 창 하나
    for wx in (BW-320, BW-250):
        for wy in (680, 760, 830):
            d.rectangle([wx, wy, wx+50, wy+58], fill=(30, 33, 46))
    ctext(d, 380, 250, "1949", SER(150), PAPER, 8, INK)
    ctext(d, BW-260, 320, "1956", SER(90), tuple(int(c*0.9) for c in PAPER), 6, INK)
    ctext(d, BW/2, 1600, "옌안 포위 — 그리고 모스크바의 방 한 칸", SAN(50), PAPER)
    tag(d); return im

def b5():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1000, 430, (40, 38, 32)); d = ImageDraw.Draw(im)
    d.rectangle([BW/2-14, 620, BW/2+14, 1520], fill=(70, 72, 84))                   # 빈 깃대
    d.ellipse([BW/2-26, 580, BW/2+26, 632], fill=(70, 72, 84))
    d.rectangle([BW/2-220, 1520, BW/2+220, 1600], fill=(34, 36, 46))
    ctext(d, BW/2, 240, "성립하지 않은 나라", SER(104), PAPER, 7, INK)
    ctext(d, BW/2, 1700, "대약진 없음 · 문화대혁명 없음", SAN(52), PAPER)
    tag(d); return im

def b6():
    im = night(); d = ImageDraw.Draw(im)
    data = [("1978", "난징의 봄"), ("1987", "계엄 해제"), ("1993", "첫 직선제")]
    for k, (yr, label) in enumerate(data):
        y = 520 + k*420
        d.line([(200, y+140), (BW-200, y+140)], fill=(60, 64, 80), width=4)
        d.ellipse([250-16, y+124, 250+16, y+156], fill=AMBER)
        ctext(d, 480, y, yr, SER(120), PAPER, 6, INK, anchor="la")
        d.text((480, y+150), label, font=SAN(56), fill=tuple(int(c*0.92) for c in PAPER))
    ctext(d, BW/2, 250, "민주화의 계단", SAN(60), PAPER)
    tag(d); return im

def b7():
    im = night(); d = ImageDraw.Draw(im)
    for k, (x0, hgt) in enumerate([(120, 500), (330, 720), (560, 900), (800, 640), (1010, 560)]):
        d.rectangle([x0, 1900-hgt, x0+170, 1900], fill=(22, 26, 38))                 # 스카이라인
        rng = _np.random.default_rng(k)
        for _ in range(10):
            wx = int(rng.uniform(x0+16, x0+130)); wy = int(rng.uniform(1900-hgt+30, 1840))
            d.rectangle([wx, wy, wx+22, wy+28], fill=(120, 96, 44))
    cols = [RED, AMBER, STEEL, (110, 168, 92), PAPER, (150, 110, 170)]              # 6당 반원 의회
    cx, cy = BW/2, 1050
    for i, col in enumerate(cols):
        a0 = math.pi + i*math.pi/6
        for r in (300, 380, 460):
            x, y = cx+math.cos(a0+math.pi/12)*r, cy+math.sin(a0+math.pi/12)*r
            d.ellipse([x-26, y-26, x+26, y+26], fill=col)
    ctext(d, BW/2, 250, "여섯 개의 정당", SER(110), PAPER, 7, INK)
    tag(d); return im

def b8():
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([120, 560, BW/2-40, 1060], 30, fill=(46, 30, 28), outline=RED, width=8)
    ctext(d, (120+BW/2-40)/2, 620, "보수당", SAN(64), PAPER)
    ctext(d, (120+BW/2-40)/2, 760, "복지", SER(150), PAPER)
    ctext(d, (120+BW/2-40)/2, 950, "확대", SER(90), PAPER)
    d.rounded_rectangle([BW/2+40, 900, BW-120, 1400], 30, fill=(28, 36, 48), outline=STEEL, width=8)
    ctext(d, (BW/2+40+BW-120)/2, 960, "진보당", SAN(64), PAPER)
    ctext(d, (BW/2+40+BW-120)/2, 1100, "민영화", SER(130), PAPER)
    ctext(d, BW/2, 250, "이상한 나라", SER(120), PAPER, 7, INK)
    ctext(d, BW/2, 1650, "당신이 아는 지도가 뒤집혀 있다", SAN(54), PAPER)
    tag(d); return im

def b9():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 560, "누가 보수고", SER(150), PAPER)
    ctext(d, BW/2, 800, "누가 진보인가", SER(150), PAPER)
    redbar(d, 1250, "당신의 답을 남겨주세요")
    ctext(d, BW/2, BH-380, "「자유중국」 — 12부작", SAN(52), PAPER)
    ctext(d, BW/2, BH-290, "EP2. 자유중국의 보수는 누구인가", SAN(44),
          tuple(int(c*0.85) for c in PAPER))
    tag(d); return im

def anim_dot(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 11+2.6*math.sin(t*3.1)
    d.ellipse([W/2-r, 250-r, W/2+r, 250+r], outline=PAPER, width=5)
    return im

VO = {p["id"]: p["dur"] for p in json.load(open(f"{ROOT}/vo/lines.json"))}
GAP = 0.30
SECS = {k: VO[k]+GAP for k in VO}; SECS["s9"] = VO["s9"]+1.4
SC_A = [(k, SECS[k]) for k in ["s1","s2","s3","s4","s5","s6","s7","s8","s9"]]
print(f"audio {mix_audio(SC_A, f'{ROOT}/vo', f'{ROOT}/mix.wav', lead=0.15):.2f}s")
BULD = [b1,b2,b3,b4,b5,b6,b7,b8,b9]
SCENES = []
for i,(k,s) in enumerate(SC_A):
    kb = (1.07,1.00,0,-25) if i%2==0 else (1.00,1.06,15,0)
    SCENES.append((BULD[i], s, kb, anim_dot if k=="s9" else None))
n, rc = encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep1_short.mp4", seed0=900)
print("frames", n, "rc", rc)
