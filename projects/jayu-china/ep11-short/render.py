"""EP11 「이 정치인은 좌파입니까, 우파입니까?」 — 원칙 v1.0 고정 70초 포맷 렌더. 참여형 분류 게임.

WTF: 공약 3개가 찍히고 '左? 右?'가 갈라진다.
Payoff: 전쟁·동맹·산업 → 공약 묶음 인과사슬 — 이념이 아니라 역사.
공약 칩은 현실 나침반 색(좌=청, 우=적)으로 칠해 한 카드 안에서 충돌을 보이게 한다.
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
LBLUE = (110, 150, 205)   # 현실 나침반의 '좌' 색
RRED = (205, 110, 100)    # 현실 나침반의 '우' 색

CANDS = [
    ("1", [("국영 철도 사수", LBLUE), ("무역 개방", RRED)]),
    ("2", [("민영화 확대", RRED), ("외국 자본 규제", LBLUE)]),
    ("3", [("복지 확대", LBLUE), ("군비 증강", RRED)]),
    ("4", [("감세", RRED), ("재벌 해체", LBLUE)]),
]

def cand_card(d, x0, y0, x1, num, pledges, dim=False):
    mut = 0.45 if dim else 1.0
    d.rounded_rectangle([x0, y0, x1, y0+330], 26, fill=(24, 27, 38),
                        outline=tuple(int(c*mut) for c in (150, 154, 166)), width=7)
    d.ellipse([x0+30, y0+28, x0+110, y0+108], outline=tuple(int(c*mut) for c in AMBER), width=6)
    ctext(d, x0+70, y0+44, num, SER(48), tuple(int(c*mut) for c in AMBER))
    for i, (txt, col) in enumerate(pledges):
        y = y0+140+i*90
        d.rounded_rectangle([x0+30, y, x1-30, y+74], 16,
                            fill=tuple(int(c*0.28*mut) for c in col),
                            outline=tuple(int(c*mut) for c in col), width=5)
        ctext(d, (x0+x1)/2, y+16, txt, SAN(40), tuple(int(c*mut) for c in PAPER))

def ruler(d, cx, y, w=380):
    """현실 좌우 자 — 청→적 그라데이션 바."""
    steps = 40
    for i in range(steps):
        f = i/(steps-1)
        col = tuple(int(LBLUE[k]*(1-f)+RRED[k]*f) for k in range(3))
        d.rectangle([cx-w/2+i*w/steps, y, cx-w/2+(i+1)*w/steps, y+26], fill=col)
    ctext(d, cx-w/2-45, y-12, "좌", SAN(36), LBLUE)
    ctext(d, cx+w/2+45, y-12, "우", SAN(36), RRED)

def b1():
    im = night()
    return glow(im, BW/2, 1000, 500, (46, 42, 34))

def s1_overlay(im, t):
    """공약 3개가 차례로 찍히고 '左? 右?'가 갈라진다 (1080 좌표계)."""
    OW = UI.W
    d = ImageDraw.Draw(im, "RGBA")
    pills = [("복지 확대", 0.10, LBLUE), ("시장 개방", 0.42, RRED), ("군비 증강", 0.74, RRED)]
    for i, (txt, t0, col) in enumerate(pills):
        if t <= t0: continue
        e = UI.ease_out_back(min(1, (t-t0)/0.30))
        w = int(280*min(e, 1.05)); y = 660+i*150
        a = int(255*min(1, (t-t0)/0.18))
        d.rounded_rectangle([OW//2-w, y, OW//2+w, y+112], 20,
                            fill=(24, 27, 38, a), outline=(*col, a), width=7)
        d.text((OW//2, y+28), txt, font=SAN(52), fill=(242, 233, 220, a), anchor="ma")
    if t > 1.15:
        a2 = int(255*min(1, (t-1.15)/0.22))
        d.text((OW//2-190, 1210), "左?", font=SER(140), fill=(*LBLUE, a2), anchor="ma")
        d.text((OW//2+190, 1210), "右?", font=SER(140), fill=(*RRED, a2), anchor="ma")
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

def b3():   # 약속: 후보 4명 실루엣
    im = night(); d = ImageDraw.Draw(im)
    for i in range(4):
        x0 = 170 if i % 2 == 0 else BW/2+50
        y0 = TOP+160 if i < 2 else TOP+560
        x1 = x0+400
        d.rounded_rectangle([x0, y0, x1, y0+330], 26, fill=(24, 27, 38),
                            outline=(80, 86, 100), width=7)
        ctext(d, (x0+x1)/2, y0+40, str(i+1), SER(72), AMBER)
        ctext(d, (x0+x1)/2, y0+160, "?", SER(110), (130, 134, 148))
    ctext(d, BW/2, TOP+30, "직접 분류해 보세요", SER(72), PAPER, 5, INK)
    return im

def b4():   # 원인A: 후보 1·2
    im = night(); d = ImageDraw.Draw(im)
    cand_card(d, 150, TOP+170, BW/2-60, *CANDS[0])
    cand_card(d, BW/2+60, TOP+170, BW-150, *CANDS[1])
    ctext(d, BW/2, TOP+40, "첫 두 명", SER(72), PAPER, 5, INK)
    ctext(d, BW/2, TOP+610, "한 카드 안에, 두 색", SAN(48), (150, 154, 166))
    return im

def b5():   # 원인A2: 벌써 헷갈리죠?
    im = night(); d = ImageDraw.Draw(im)
    cand_card(d, 150, TOP+430, BW/2-60, *CANDS[0], dim=True)
    cand_card(d, BW/2+60, TOP+430, BW-150, *CANDS[1], dim=True)
    ctext(d, BW/2, TOP+90, "벌써", SER(110), PAPER)
    ctext(d, BW/2, TOP+250, "헷갈리죠?", SER(130), YELLOW)
    return im

def b6():   # 원인B: 후보 3·4
    im = night(); d = ImageDraw.Draw(im)
    cand_card(d, 150, TOP+170, BW/2-60, *CANDS[2])
    cand_card(d, BW/2+60, TOP+170, BW-150, *CANDS[3])
    ctext(d, BW/2, TOP+40, "남은 두 명", SER(72), PAPER, 5, INK)
    ctext(d, BW/2, TOP+610, "이번에도, 두 색", SAN(48), (150, 154, 166))
    return im

def b7():   # 원인B2: 네 명 모두 자 위에서 반씩
    im = night(); d = ImageDraw.Draw(im)
    for i in range(4):
        cx = 330 if i % 2 == 0 else BW-330
        cy = TOP+200 if i < 2 else TOP+480
        d.rounded_rectangle([cx-90, cy-70, cx+90, cy+10], 18, fill=(24, 27, 38),
                            outline=(100, 106, 122), width=5)
        ctext(d, cx, cy-58, str(i+1), SER(48), AMBER)
        ruler(d, cx, cy+50, 330)
        d.polygon([(cx-14, cy+44), (cx+14, cy+44), (cx, cy+80)], fill=PAPER)
    ctext(d, BW/2, TOP+700, "네 명 모두,", SER(80), PAPER)
    ctext(d, BW/2, TOP+820, "반씩 걸친다", SER(104), YELLOW)
    return im

def b8():   # Second Hook: 자연스러운 동맹
    im = night(); d = ImageDraw.Draw(im)
    pts = [(BW/2, TOP+180), (BW-260, TOP+400), (BW/2, TOP+620), (260, TOP+400)]
    for a in range(4):
        for b in range(a+1, 4):
            d.line([pts[a], pts[b]], fill=(120, 96, 44), width=5)
    for i, (x, y) in enumerate(pts):
        d.ellipse([x-70, y-70, x+70, y+70], fill=(28, 32, 46), outline=AMBER, width=7)
        ctext(d, x, y-34, str(i+1), SER(56), AMBER)
    ctext(d, BW/2, TOP+760, "속임수가 아니라,", SER(76), PAPER)
    ctext(d, BW/2, TOP+870, "자연스러운 동맹", SER(96), YELLOW)
    return im

def b9():   # Payoff: 이념이 아니라 역사
    im = night(); d = ImageDraw.Draw(im)
    for i, txt in enumerate(["전쟁", "동맹", "산업"]):
        x = 260 + i*360
        d.rounded_rectangle([x-140, TOP+140, x+140, TOP+270], 22, fill=(28, 32, 46),
                            outline=STEEL, width=6)
        ctext(d, x, TOP+172, txt, SAN(52), PAPER)
    d.line([(BW/2, TOP+290), (BW/2, TOP+420)], fill=AMBER, width=10)
    d.polygon([(BW/2-24, TOP+416), (BW/2+24, TOP+416), (BW/2, TOP+448)], fill=AMBER)
    d.rounded_rectangle([BW/2-330, TOP+460, BW/2+330, TOP+590], 22, fill=(28, 32, 46),
                        outline=AMBER, width=8)
    ctext(d, BW/2, TOP+492, "공약 묶음", SAN(54), AMBER)
    ctext(d, BW/2, TOP+680, "이념이 아니라", SER(84), PAPER)
    ctext(d, BW/2, TOP+800, "역사가 묶는다", SER(104), YELLOW)
    return im

def b10():  # 확장: 고장 난 나침반
    im = night(); d = ImageDraw.Draw(im)
    cx, cy = BW/2, TOP+400
    d.ellipse([cx-260, cy-260, cx+260, cy+260], outline=(100, 106, 122), width=10)
    ctext(d, cx, cy-250+18, "左", SAN(44), LBLUE)
    ctext(d, cx, cy+250-70, "右", SAN(44), RRED)
    d.line([(cx-30, cy-160), (cx+70, cy+40)], fill=PAPER, width=12)     # 부러진 바늘
    d.line([(cx+70, cy+40), (cx-90, cy+150)], fill=(150, 154, 166), width=8)
    d.line([(cx-150, cy-60), (cx+180, cy+90)], fill=RED, width=10)      # 균열
    ctext(d, BW/2, TOP+740, "자가, 다른 세계의", SER(80), PAPER)
    ctext(d, BW/2, TOP+860, "자일 뿐", SER(110), YELLOW)
    return im

def b11():  # 다음 모순 — 하드컷 (EP12 총선 훅)
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+120, "다음 편", SER(90), PAPER)
    ctext(d, BW/2, TOP+330, "2080 자유중국 총선", SER(110), PAPER)
    ctext(d, BW/2, TOP+590, "당신에게, 5표", SER(140), YELLOW)
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
        UI.title_band(im, "나침반이 고장나는", "분류 게임",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP11",
                      world="가상 역사 · 국민당이 이긴 세계의 선거")
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep11.mp4", seed0=11000, trans=0.20)
print("frames", n, "rc", rc)
