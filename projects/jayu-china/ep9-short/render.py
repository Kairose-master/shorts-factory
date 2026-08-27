"""EP9 「대만독립이 없는 세계의 대만 정치」 — 원칙 v1.0 고정 70초 포맷 렌더. ACT III 마지막.

WTF: 투표용지에서 '獨立' 항목이 줄 그어져 사라진 쟁점 목록.
Payoff: 안보의 언어 → 회계의 언어 번역 다이어그램.
좌표 안전 규칙 준수, 오버레이는 1080 출력 좌표계, 한자는 한국 한자음 범위.
"""
import sys, os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../../malgap-style")
from noir_kit import *
import shorts_ui as UI
from PIL import Image, ImageDraw

TOP = 560
GREEN = (110, 168, 92)
YELLOW = (255, 228, 0)

def chain_node(d, cx, y, w, txt, col, fsz=48):
    d.rounded_rectangle([cx-w/2, y, cx+w/2, y+126], 24, fill=(28, 32, 46), outline=col, width=7)
    ctext(d, cx, y+34, txt, SAN(fsz), PAPER)

def chain_arrow(d, cx, y0, y1, col=AMBER):
    d.line([(cx, y0), (cx, y1-24)], fill=col, width=10)
    d.polygon([(cx-24, y1-28), (cx+24, y1-28), (cx, y1+2)], fill=col)

def taiwan(d, ox, oy, s=1.0, outline=AMBER, width=9):
    pts = [(540, 800), (640, 760), (700, 900), (660, 1120), (560, 1200), (500, 1000)]
    d.polygon([(ox+(x-540)*s, oy+(y-760)*s) for x, y in pts], outline=outline, width=width)

def b1():
    im = night()
    return glow(im, BW/2, 1000, 500, (46, 42, 34))

def s1_overlay(im, t):
    """투표용지 스태거 — 쟁점 항목이 차례로 찍히고 '獨立'은 줄이 그어진다 (1080 좌표계)."""
    OW = UI.W
    d = ImageDraw.Draw(im, "RGBA")
    e0 = UI.ease_out_back(min(1, max(t, 0)/0.32))
    w = int(340*min(e0, 1.06)); h = int(430*min(e0, 1.06))
    d.rounded_rectangle([OW//2-w, 880-h, OW//2+w, 880+h], 22, fill=(242, 233, 220, 255))
    if e0 > 0.5:
        d.text((OW//2, 880-h+44), "選擧 爭點", font=SAN(40), fill=(120, 110, 96), anchor="ma")
        items = [("예산 배분", 0.30, False), ("항만 운영", 0.44, False),
                 ("교과서 권한", 0.58, False), ("獨立", 0.76, True)]
        for i, (txt, t0, struck) in enumerate(items):
            if t <= t0: continue
            a = int(255*min(1, (t-t0)/0.18))
            y = 880-h+150+i*160
            d.rectangle([OW//2-w+60, y+8, OW//2-w+110, y+58], outline=(90, 84, 74, a), width=5)
            col = (160, 154, 144, a) if struck else (20, 17, 15, a)
            d.text((OW//2-w+150, y), txt, font=SER(62), fill=col, anchor="la")
            if struck and t > t0+0.22:
                a2 = int(255*min(1, (t-t0-0.22)/0.15))
                tw = 300
                d.line([(OW//2-w+140, y+38), (OW//2-w+150+tw, y+38)], fill=(200, 69, 46, a2), width=10)
    return im

def b2():   # 전제: 1946 갈림길 (시리즈 앵커)
    im = night(); d = ImageDraw.Draw(im)
    cx, jy = BW/2, TOP+760
    d.line([(cx, jy+520), (cx, jy)], fill=(120, 124, 138), width=14)
    d.line([(cx, jy), (cx-300, jy-420)], fill=(70, 74, 88), width=10)
    d.line([(cx, jy), (cx+300, jy-420)], fill=AMBER, width=14)
    d.ellipse([cx-26, jy-26, cx+26, jy+26], fill=PAPER)
    ctext(d, cx-330, jy-520, "공산당", SAN(50), (110, 114, 128))
    ctext(d, cx+330, jy-540, "국민당 승리", SAN(56), AMBER)
    ctext(d, BW/2, TOP+60, "1946", SER(170), PAPER, 8, INK)
    return im

def b3():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+180, "그럼 무엇으로", SER(120), PAPER)
    ctext(d, BW/2, TOP+430, "싸울까?", SER(170), YELLOW)
    return im

def b4():   # 원인 A: 존재 질문의 부재 — 두 유령 카드에 X
    im = night(); d = ImageDraw.Draw(im)
    for i, txt in enumerate(["분리의 공포", "병합의 위협"]):
        x0 = 150 if i == 0 else BW/2+70
        x1 = BW/2-70 if i == 0 else BW-150
        d.rounded_rectangle([x0, TOP+220, x1, TOP+560], 26, fill=(24, 27, 38),
                            outline=(80, 86, 100), width=7)
        ctext(d, (x0+x1)/2, TOP+340, txt, SAN(52), (130, 134, 148))
        d.line([(x0+40, TOP+260), (x1-40, TOP+520)], fill=RED, width=12)
        d.line([(x1-40, TOP+260), (x0+40, TOP+520)], fill=RED, width=12)
    ctext(d, BW/2, TOP+700, "존재를 묻는 질문이", SER(84), PAPER)
    ctext(d, BW/2, TOP+840, "없다", SER(130), YELLOW)
    return im

def b5():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+160, "질문이 사라진 자리를", SER(96), PAPER)
    ctext(d, BW/2, TOP+400, "생활이 채운다", SER(120), YELLOW)
    return im

def b6():   # 원인 B: 난징과의 거리 — 3 쟁점 카드
    im = night(); d = ImageDraw.Draw(im)
    d.ellipse([170, TOP+120, 330, TOP+280], fill=(30, 36, 50), outline=AMBER, width=9)
    ctext(d, 250, TOP+164, "南京", SAN(44), AMBER)
    taiwan(d, 830, TOP+560, 0.75, outline=(150, 154, 166), width=8)
    d.line([(330, TOP+220), (860, TOP+660)], fill=(90, 94, 108), width=7)
    for i, (ch, lab) in enumerate([("稅", "세금 배분"), ("港", "항만 운영"), ("敎", "교과서 권한")]):
        y = TOP+300+i*195
        d.rounded_rectangle([170, y, 700, y+172], 24, fill=(28, 32, 46),
                            outline=STEEL, width=7)
        ctext(d, 285, y+30, ch, SER(84), AMBER)
        ctext(d, 400, y+52, lab, SAN(50), PAPER, anchor="la")
    return im

def b7():   # 원인 B2: 가오슝 항만 — 실명 시민
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([0, 1300, BW, 1320], fill=(60, 64, 78))
    for i in range(3):
        d.rectangle([180+i*260, 1210, 180+i*260+210, 1300],
                    fill=[(120, 96, 44), (91, 104, 123), (140, 70, 52)][i])
    d.line([(700, 1300), (700, 720)], fill=(100, 106, 122), width=16)
    d.line([(500, 800), (1000, 800)], fill=(100, 106, 122), width=14)
    d.line([(880, 800), (880, 1000)], fill=(100, 106, 122), width=8)
    d.rectangle([820, 1000, 940, 1080], fill=(91, 104, 123))
    ctext(d, BW/2, TOP+40, "국기가 아니라 하역료", SER(80), PAPER, 5, INK)
    name = "린원제 (52) · 가오슝 항만 노동자"
    f = SAN(38); tw = d.textbbox((0, 0), name, font=f)[2]
    d.rounded_rectangle([BW/2-tw/2-20, 1700, BW/2+tw/2+20, 1772], 14, fill=INK)
    d.text((BW/2-tw/2, 1714), name, font=f, fill=PAPER)
    return im

def b8():   # Second Hook: 두 섬의 공통 구호 — 自治
    im = night(); d = ImageDraw.Draw(im)
    taiwan(d, 250, TOP+240, 1.0, outline=AMBER, width=9)
    ctext(d, 400, TOP+740, "臺灣", SAN(48), tuple(int(c*0.9) for c in PAPER))
    d.polygon([(820, TOP+420), (930, TOP+380), (1000, TOP+470), (950, TOP+560), (840, TOP+540)],
              outline=(150, 180, 205), width=8)
    ctext(d, 910, TOP+610, "香港", SAN(48), (150, 180, 205))
    st = seal_word("自治"); im.paste(st, (int(BW/2-st.width/2), TOP+600), st)
    ctext(d, BW/2, 1420, "두 섬의 공통 구호", SER(80), PAPER, 5, INK)
    return im

def b9():   # Payoff: 언어의 번역
    im = night(); d = ImageDraw.Draw(im)
    chain_node(d, BW/2, TOP+60, 660, "안보의 언어", (230, 140, 128), 52)
    ctext(d, BW/2, TOP+230, "독립 · 통일 · 위협", SAN(44), (150, 154, 166))
    chain_arrow(d, BW/2, TOP+310, TOP+420)
    ctext(d, BW/2+120, TOP+330, "번역", SAN(40), AMBER, anchor="la")
    chain_node(d, BW/2, TOP+420, 660, "회계의 언어", GREEN, 52)
    ctext(d, BW/2, TOP+590, "예산 · 권한 · 배분율", SAN(44), (150, 154, 166))
    ctext(d, BW/2, TOP+710, "존재를 안 물으면", SER(88), PAPER)
    ctext(d, BW/2, TOP+850, "예산을 묻는다", SER(96), YELLOW)
    return im

def b10():  # 확장: 투표함
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1050, 320, (52, 48, 34)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([BW/2-260, 950, BW/2+260, 1330], 24, fill=(40, 44, 58),
                        outline=AMBER, width=9)
    d.rectangle([BW/2-110, 920, BW/2+110, 952], fill=INK)
    d.rounded_rectangle([BW/2-70, 760, BW/2+90, 900], 10, fill=PAPER)         # 투입되는 표
    ctext(d, BW/2, TOP+40, "이제, 투표할 차례", SER(88), PAPER, 5, INK)
    return im

def b11():  # 다음 모순 — 하드컷 (정본 EP10 훅)
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+140, "2080년 대학생에게", SER(96), PAPER)
    ctext(d, BW/2, TOP+380, "보수는", SER(150), PAPER)
    ctext(d, BW/2, TOP+650, "시장이 아닙니다", SER(120), YELLOW)
    return im

VOJ = json.load(open(f"{ROOT}/vo/lines.json"))
GAP = 0.12
SC = []; t0 = 0.0
for p in VOJ:
    secs = p["dur"]+GAP+(0.10 if p["id"] == "s11" else 0)
    SC.append({"id": p["id"], "secs": secs, "t0": t0,
               "chips": UI.chunks_for(p["text"], p["dur"]+0.15)})
    t0 += secs
print(f"audio {mix_audio([(s['id'], s['secs']) for s in SC], f'{ROOT}/vo', f'{ROOT}/mix.wav', lead=0.15):.2f}s")

BULD = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11]
def smooth(p): return p*p*(3-2*p)
def make_anim(si, sc):
    def anim(im, t):
        if si == 0:
            im = s1_overlay(im, t)
        UI.title_band(im, "독립이 사라진", "대만의 선거",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP9",
                      world="가상 역사 · 국민당이 이긴 세계의 대만")
        for c, cs, cd in sc["chips"]:
            if cs <= t < cs+cd+0.10:
                UI.chip(im, c, t-cs); break
        return im
    return anim
SCENES = []
for i, sc in enumerate(SC):
    kb = (1.07, 1.00, 0, -25) if i % 2 == 0 else (1.00, 1.06, 15, 0)
    if i == 0: kb = (1.00, 1.02, 0, 0)
    SCENES.append((BULD[i], sc["secs"], kb, make_anim(i, sc)))

import noir_kit as NK
_orig = NK.kb_crop
NK.kb_crop = lambda base, p, kb: _orig(base, smooth(p), kb)
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep9.mp4", seed0=9000, trans=0.20)
print("frames", n, "rc", rc)
