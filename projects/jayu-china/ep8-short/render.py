"""EP8 「친미는 좌파인가 우파인가?」 — 원칙 v1.0 고정 70초 포맷 렌더.

WTF: 1950/2050 두 시대 카드의 등가 배치 — 같은 '친미'가 다른 색.
Payoff: 축 이동 비포/애프터 — 시리즈 테제("질서가 다르면 결론이 뒤집힌다")의
축 버전. 좌표 안전 규칙 준수, 오버레이는 1080 출력 좌표계, 한자는 한국 한자음 범위.
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

def b1():
    im = night()
    return glow(im, BW/2, 1000, 500, (44, 44, 36))

def s1_overlay(im, t):
    """1950/2050 두 시대 카드 스태거 (1080 출력 좌표계)."""
    OW = UI.W
    d = ImageDraw.Draw(im, "RGBA")
    def card(cx, era, word, col, t0):
        if t <= t0: return
        e = UI.ease_out_back((t-t0)/0.32)
        a = int(255*min(1, (t-t0)/0.18))
        w, h = int(400*min(e, 1.08)), int(600*min(e, 1.08))
        d.rounded_rectangle([cx-w/2, 880-h/2, cx+w/2, 880+h/2], 26,
                            fill=(28, 32, 46, a), outline=(*col, a), width=9)
        if e > 0.6:
            d.text((cx, 880-h/2+50), era, font=SER(84), fill=(242, 233, 220, a), anchor="ma")
            d.text((cx, 880-60), "친미", font=SER(110), fill=(*col, a), anchor="ma")
            d.text((cx, 880+130), word, font=SAN(56), fill=(*col, a), anchor="ma")
    card(268, "1950", "= 보수", YELLOW, 0.10)
    card(OW-268, "2050", "= 진보", GREEN, 0.45)
    if t > 0.85:
        a = int(255*min(1, (t-0.85)/0.2))
        d.text((OW//2, 1290), "같은 세계, 같은 말", font=SAN(54), fill=(242, 233, 220, a),
               anchor="ma", stroke_width=8, stroke_fill=(20, 17, 15, a))
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
    ctext(d, BW/2, TOP+150, "같은 친미가", SER(120), PAPER)
    ctext(d, BW/2, TOP+400, "왜 옮겼을까?", SER(140), YELLOW)
    return im

def b4():   # 원인 A: 1950 — 미국이 축
    im = night(); d = ImageDraw.Draw(im)
    cx, cy = BW/2, TOP+780
    for k in range(8):                                                        # 방사선
        import math
        ang = k*math.pi/4
        d.line([(cx+90*math.cos(ang), cy+90*math.sin(ang)),
                (cx+330*math.cos(ang), cy+330*math.sin(ang))], fill=(70, 84, 100), width=6)
    d.ellipse([cx-100, cy-100, cx+100, cy+100], fill=(28, 36, 52), outline=STEEL, width=10)
    ctext(d, cx, cy-44, "美", SER(96), PAPER)
    ctext(d, BW/2, TOP+40, "1950 · 反共 질서의 축", SAN(56), (150, 180, 205))
    d.rounded_rectangle([BW/2-320, TOP+130, BW/2+320, TOP+290], 26,
                        fill=(28, 32, 46), outline=YELLOW, width=8)
    ctext(d, BW/2, TOP+172, "친미 = 보수", SAN(60), YELLOW)
    return im

def b5():   # 원인 A2: 그때의 반미 = 급진
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+180, "그때의 반미는", SER(110), PAPER)
    ctext(d, BW/2, TOP+430, "反질서", SER(170), (230, 140, 128))
    ctext(d, BW/2, TOP+720, "급진의 말", SER(110), PAPER)
    return im

def b6():   # 원인 B: 중심 이동 — 축이 자유중국으로
    im = night(); d = ImageDraw.Draw(im)
    d.ellipse([180, TOP+340, 420, TOP+580], outline=(90, 104, 120), width=8)   # 옛 축(미국, 흐려짐)
    ctext(d, 300, TOP+412, "美", SER(76), (110, 124, 140))
    d.line([(440, TOP+440), (700, TOP+480)], fill=AMBER, width=12)             # 이동 화살표
    d.polygon([(700, TOP+480), (636, TOP+498), (664, TOP+444)], fill=AMBER)
    im2 = glow(im, 860, TOP+520, 260, (56, 50, 34)); d = ImageDraw.Draw(im2)
    d.ellipse([720, TOP+380, 1000, TOP+660], fill=(30, 36, 50), outline=AMBER, width=12)
    ctext(d, 860, TOP+460, "中", SER(110), AMBER)
    ctext(d, BW/2, TOP+40, "중심이 옮겨간다", SER(84), PAPER, 5, INK)
    d.rounded_rectangle([BW/2-360, TOP+880, BW/2+360, TOP+1040], 26,
                        fill=(28, 32, 46), outline=AMBER, width=8)
    ctext(d, BW/2, TOP+922, "기존 질서 = 자유중국", SAN(52), PAPER)
    return im2

def b7():   # 원인 B2: 미국 = 균형추
    im = night(); d = ImageDraw.Draw(im)
    cx, py = BW/2, TOP+260
    d.line([(cx, py), (cx, py+500)], fill=(100, 106, 122), width=14)
    d.polygon([(cx-90, py+520), (cx+90, py+520), (cx, py+470)], fill=(100, 106, 122))
    d.line([(cx-380, py-20), (cx+380, py-20)], fill=(140, 144, 156), width=12)  # 수평 들보
    d.rounded_rectangle([cx-500, py+0, cx-260, py+140], 20, fill=(28, 32, 46),
                        outline=AMBER, width=7)
    ctext(d, cx-380, py+36, "질서", SAN(52), AMBER)
    d.rounded_rectangle([cx+260, py+0, cx+500, py+140], 20, fill=(28, 36, 52),
                        outline=STEEL, width=7)
    ctext(d, cx+380, py+36, "美", SER(60), (150, 180, 205))
    ctext(d, BW/2, TOP+900, "개혁의 지렛대", SER(88), PAPER, 5, INK)
    return im

def b8():   # Second Hook: 진보 깃발에 미국이
    im = night(); d = ImageDraw.Draw(im)
    fx = 340
    d.line([(fx, TOP+140), (fx, TOP+800)], fill=(90, 94, 108), width=14)
    d.polygon([(fx+8, TOP+140), (fx+560, TOP+300), (fx+8, TOP+460)], fill=GREEN)
    ctext(d, fx+70, TOP+200, "自由貿易", SAN(48), INK, anchor="la")
    ctext(d, fx+70, TOP+270, "美國", SAN(48), INK, anchor="la")
    ctext(d, fx+70, TOP+340, "改革", SAN(48), INK, anchor="la")
    ctext(d, BW/2, 1400, "깃발의 색은, 진보", SER(80), PAPER, 5, INK)
    return im

def b9():   # Payoff: 축 이동 비포/애프터
    im = night(); d = ImageDraw.Draw(im)
    chain_node(d, BW/2-260, TOP+60, 440, "1950 축 = 美", STEEL, 44)
    chain_node(d, BW/2-260, TOP+250, 440, "친미 = 보수", YELLOW, 44)
    d.line([(BW/2-260, TOP+186), (BW/2-260, TOP+244)], fill=(120, 124, 138), width=8)
    chain_node(d, BW/2+260, TOP+60, 440, "2050 축 = 中", AMBER, 44)
    chain_node(d, BW/2+260, TOP+250, 440, "친미 = 진보", GREEN, 44)
    d.line([(BW/2+260, TOP+186), (BW/2+260, TOP+244)], fill=(120, 124, 138), width=8)
    d.line([(BW/2-40, TOP+150), (BW/2+40, TOP+150)], fill=AMBER, width=10)
    d.polygon([(BW/2+44, TOP+150), (BW/2-4, TOP+128), (BW/2-4, TOP+172)], fill=AMBER)
    ctext(d, BW/2, TOP+510, "축이 움직이면", SER(92), PAPER)
    ctext(d, BW/2, TOP+670, "같은 방향도", SER(92), PAPER)
    ctext(d, BW/2, TOP+830, "반대편이 된다", SER(100), YELLOW)
    return im

def b10():  # 확장: 대만
    im = night(); d = ImageDraw.Draw(im)
    d.polygon([(540, 800), (640, 760), (700, 900), (660, 1120), (560, 1200), (500, 1000)],
              outline=AMBER, width=9)
    ctext(d, BW/2, 1300, "臺灣", SER(84), tuple(int(c*0.9) for c in PAPER))
    ctext(d, BW/2, TOP+60, "가장 낯선 곳", SER(96), PAPER, 6, INK)
    return im

def b11():  # 다음 모순 — 하드컷 (정본 EP9 훅)
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+140, "이 세계 대만 선거의", SER(96), PAPER)
    ctext(d, BW/2, TOP+360, "최대 쟁점은", SER(120), PAPER)
    ctext(d, BW/2, TOP+620, "독립이 아닙니다", SER(130), YELLOW)
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
        UI.title_band(im, "친미는 좌파인가", "우파인가?",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP8",
                      world="가상 역사 · 국민당이 이긴 세계의 동아시아")
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep8.mp4", seed0=8000, trans=0.20)
print("frames", n, "rc", rc)
