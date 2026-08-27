"""EP6 「미국보다 중국이 더 가까운 한국」 — 원칙 v1.0 고정 70초 포맷 렌더.

생활사 편: 철도 밤기차, 칠판, 승진 사다리, 음악 차트, 부녀 식탁(정본 템플릿의
생활세계 장면). WTF는 두 지원서가 같은 줄에 서는 등가 카드.
좌표 안전 규칙: 장면 요소 base y 540~1410, 태그류 1700~1780.
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

def b1():
    im = night()
    return glow(im, BW/2, 1000, 500, (44, 46, 34))

def s1_overlay(im, t):
    """두 유학 지원서가 같은 줄에 — 카드 A, =, 카드 B 순 스태거.

    주의: anim 오버레이는 kb_crop 이후의 1080 출력 좌표계에 그린다 (UI.W 기준).
    베이스(1240) 좌표를 쓰면 우측으로 80px 밀려 잘린다."""
    OW = UI.W
    d = ImageDraw.Draw(im, "RGBA")
    def card(cx, label, sub, t0, col):
        if t <= t0: return
        e = UI.ease_out_back((t-t0)/0.32)
        a = int(255*min(1, (t-t0)/0.18))
        w, h = int(380*min(e, 1.1)), int(560*min(e, 1.1))
        d.rounded_rectangle([cx-w/2, 900-h/2, cx+w/2, 900+h/2], 26,
                            fill=(242, 233, 220, a), outline=(*col, a), width=8)
        if e > 0.6:
            d.text((cx, 900-h/2+60), "入學願書", font=SAN(34), fill=(120, 110, 96, a), anchor="ma")
            d.text((cx, 900-110), label, font=SER(105), fill=(*INK, a), anchor="ma")
            d.text((cx, 900+150), sub, font=SAN(40), fill=(90, 84, 74, a), anchor="ma")
    card(265, "南京", "대륙 종단선", 0.10, AMBER)
    card(OW-265, "보스턴", "태평양 항로", 0.50, STEEL)
    if t > 0.34:
        a = int(255*min(1, (t-0.34)/0.16))
        e = UI.ease_out_back((t-0.34)/0.30)
        f = SER(int(150*min(e, 1.1))+1)
        d.text((OW//2, 830), "=", font=f, fill=(255, 228, 0, a), anchor="ma")
    if t > 0.85:
        a = int(255*min(1, (t-0.85)/0.2))
        d.text((OW//2, 1300), "같은 줄에 섭니다", font=SAN(56), fill=(242, 233, 220, a),
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
    ctext(d, BW/2, TOP+150, "정치는 싸운다", SER(110), PAPER)
    ctext(d, BW/2, TOP+430, "생활은?", SER(180), YELLOW)
    return im

def b4():   # 원인 A: 밤기차 — 국경이 아니라 노선
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, 950, 700, 180, (60, 58, 40)); d = ImageDraw.Draw(im)
    d.ellipse([880, 630, 1020, 770], fill=(210, 200, 170))                    # 달
    d.ellipse([850, 615, 975, 740], fill=(24, 28, 40))
    d.line([(120, 1400), (BW-80, 900)], fill=(90, 94, 108), width=8)          # 야간 선로
    for k in range(12):
        x = 160+k*88
        y = 1400-(x-120)*(500/(BW-200))
        d.line([(x-14, y+22), (x+14, y+22)], fill=(70, 74, 88), width=6)
    tx, ty = 520, 1180
    for k in range(3):                                                        # 객차 3량
        d.rounded_rectangle([tx+k*190-0, ty-k*86-60, tx+k*190+170, ty-k*86+30], 14,
                            fill=(40, 44, 58), outline=AMBER, width=5)
        for wx in range(tx+k*190+20, tx+k*190+150, 44):
            d.rectangle([wx, ty-k*86-40, wx+26, ty-k*86-6], fill=(232, 200, 90))
    ctext(d, BW/2, TOP+40, "국경이 아니라 노선", SER(88), PAPER, 6, INK)
    ctext(d, 350, 1500, "부산발 · 매일 밤", SAN(46), tuple(int(c*0.9) for c in PAPER))
    return im

def b5():   # 원인 A2: 칠판 — 중국어 정규 과목
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([150, TOP+120, BW-150, TOP+880], 24, fill=(30, 44, 38),
                        outline=(120, 96, 44), width=14)
    ctext(d, BW/2, TOP+200, "中國語", SER(170), (235, 230, 215))
    d.line([(320, TOP+520), (BW-320, TOP+520)], fill=(200, 196, 180), width=4)
    ctext(d, BW/2, TOP+580, "1교시 · 중국어", SAN(56), (220, 216, 200))
    ctext(d, BW/2, TOP+690, "초등 정규 과목", SAN(48), (200, 196, 180))
    return im

def b6():   # 원인 B: 승진 사다리 — 대륙 지사
    im = night(); d = ImageDraw.Draw(im)
    steps = [("사원", (90, 96, 112)), ("대리", (90, 96, 112)),
             ("대륙 지사", AMBER), ("임원", YELLOW)]
    x0, y0 = 330, 1330
    for i, (lab, col) in enumerate(steps):
        x, y = x0+i*160, y0-i*230
        d.rounded_rectangle([x, y, x+380, y+130], 20, fill=(28, 32, 46),
                            outline=col, width=7)
        ctext(d, x+190, y+34, lab, SAN(50), PAPER if col == (90, 96, 112) else col)
        if i < 3:
            d.line([(x+300, y-8), (x+340, y-92)], fill=(120, 124, 138), width=8)
    ctext(d, BW/2, TOP+40, "승진 코스", SER(92), PAPER, 6, INK)
    return im

def b7():   # 원인 B2: 차트 + 드라마
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([150, TOP+100, BW-150, TOP+620], 26, fill=(26, 30, 44),
                        outline=(100, 106, 122), width=6)
    ctext(d, 220, TOP+140, "주간 차트", SAN(44), PAPER, anchor="la")
    rows = [("1", "上海 밴드", YELLOW), ("2", "서울 발라드", PAPER), ("3", "광저우 힙합", PAPER)]
    for i, (n, t, col) in enumerate(rows):
        y = TOP+240+i*110
        ctext(d, 240, y, n, SER(56), AMBER, anchor="la")
        ctext(d, 330, y+6, t, SAN(48), col, anchor="la")
    d.rounded_rectangle([150, TOP+700, BW-150, TOP+1010], 26, fill=(26, 30, 44),
                        outline=(100, 106, 122), width=6)
    d.polygon([(240, TOP+790), (240, TOP+930), (360, TOP+860)], fill=RED)
    ctext(d, 420, TOP+800, "주말 드라마", SAN(44), PAPER, anchor="la")
    ctext(d, 420, TOP+880, "항저우 로케", SAN(52), YELLOW, anchor="la")
    return im

def person(d, px, gy, h, col, old=False):
    top = gy-h
    d.ellipse([px-40, top, px+40, top+84], fill=(230, 205, 180))
    if old:
        d.pieslice([px-44, top-6, px+44, top+56], 180, 360, fill=(200, 200, 205))
    else:
        d.pieslice([px-44, top-8, px+44, top+60], 180, 360, fill=(40, 34, 30))
    d.rounded_rectangle([px-62, top+78, px+62, gy], 34, fill=col)

def b8():   # Second Hook: 같은 식탁 — 아버지의 피켓, 딸의 노트북
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([180, 1230, BW-180, 1270], fill=(58, 46, 40))                 # 식탁
    d.rectangle([220, 1270, 260, 1420], fill=(48, 38, 33))
    d.rectangle([BW-260, 1270, BW-220, 1420], fill=(48, 38, 33))
    person(d, 330, 1230, 360, (60, 62, 72), old=True)
    person(d, BW-330, 1230, 340, (46, 66, 92), old=False)
    d.rounded_rectangle([150, 640, 470, 760], 14, fill=PAPER)                 # 피켓
    ctext(d, 310, 668, "규제하라", SAN(46), RED)
    d.line([(310, 760), (310, 880)], fill=(120, 110, 96), width=10)
    lp = BW-430                                                               # 노트북
    d.polygon([(lp, 1230), (lp+220, 1230), (lp+240, 1150), (lp+20, 1150)], fill=(70, 90, 110))
    d.rectangle([lp+30, 1010, lp+230, 1150], fill=(28, 32, 46), outline=(120, 124, 138), width=5)
    ctext(d, lp+130, 1050, "南京", SAN(40), YELLOW)
    for px, ty, name in ((330, 1700, "박성호 (41) · 오늘 집회"),
                         (BW-330, 1780, "박지은 (24) · 내일 난징 면접")):
        f = SAN(36); tw = d.textbbox((0, 0), name, font=f)[2]
        px = min(max(px, tw/2+90), BW-tw/2-90)
        d.rounded_rectangle([px-tw/2-18, ty, px+tw/2+18, ty+64], 12, fill=INK)
        d.text((px-tw/2, ty+10), name, font=f, fill=PAPER)
    return im

def b9():   # Payoff: 사슬 회수
    im = night(); d = ImageDraw.Draw(im)
    steps = [("지도가 바뀐다", PAPER), ("노선이 생긴다", AMBER),
             ("일상이 바뀐다", AMBER), ("정치는 그 다음", YELLOW)]
    y = TOP+40
    for i, (t, col) in enumerate(steps):
        chain_node(d, BW/2, y, 660, t, col, 50)
        if i < 3: chain_arrow(d, BW/2, y+126, y+206)
        y += 206
    ctext(d, BW/2, y+40, "정치는 진영을, 생활은 노선을", SAN(50),
          tuple(int(c*0.9) for c in PAPER))
    return im

def b10():  # 확장: 같은 지도, 반대 방향 — 일본
    im = night(); d = ImageDraw.Draw(im)
    d.polygon([(180, 900), (420, 760), (700, 820), (820, 1020), (700, 1260),
               (430, 1320), (230, 1160)], outline=(120, 124, 138), width=8)
    ctext(d, 450, 1010, "自由中國", SER(60), tuple(int(c*0.85) for c in PAPER))
    korea = [(850, 1000), (930, 960), (990, 1060), (950, 1240), (870, 1270), (880, 1120)]
    d.polygon(korea, outline=AMBER, width=7)
    d.line([(700, 1000), (860, 1060)], fill=AMBER, width=9)                   # 한국: 대륙으로
    d.polygon([(720, 996), (780, 984), (756, 1034)], fill=AMBER)
    jp = [(900, 1420), (1010, 1360), (1120, 1400), (1150, 1500), (1040, 1560), (930, 1520)]
    d.polygon(jp, outline=RED, width=8)
    ctext(d, 1020, 1600, "일본", SAN(50), (230, 140, 128))
    d.line([(1030, 1380), (1140, 1250)], fill=RED, width=10)                  # 일본: 반대로
    d.polygon([(1140, 1250), (1082, 1262), (1118, 1310)], fill=RED)
    ctext(d, BW/2, TOP+40, "같은 지도, 반대 방향", SER(84), PAPER, 5, INK)
    return im

def b11():  # 다음 모순 — 하드컷
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+160, "이 세계의 일본에선", SER(96), PAPER)
    ctext(d, BW/2, TOP+400, "좌파가", SER(150), YELLOW)
    ctext(d, BW/2, TOP+660, "재무장을 외칩니다", SER(110), PAPER)
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
        UI.title_band(im, "미국보다 중국이", "더 가까운 한국",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP6",
                      world="가상 역사 · 국민당이 이긴 세계의 한국")
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep6.mp4", seed0=6000, trans=0.20)
print("frames", n, "rc", rc)
