"""EP2 v2 — Shorts 제작 원칙 v1.0 고정 70초 포맷 렌더.

장면 = 인과 고리 1개 (원칙 6). 화면 텍스트는 구조 라벨만, 설명은 내레이션 (원칙 7).
구조: 결론 선공개(WTF) → 전제 → 인과사슬 → Second Hook → Payoff(사슬 회수) → 확장 → 하드컷.
"""
import sys, os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../../malgap-style")
from noir_kit import *
import shorts_ui as UI
from PIL import Image, ImageDraw

TOP = 560
KMT_BLUE = (36, 66, 122)
GREEN = (110, 168, 92)

def chain_node(d, cx, y, w, txt, col, fsz=54):
    d.rounded_rectangle([cx-w/2, y, cx+w/2, y+130], 24, fill=(28, 32, 46), outline=col, width=7)
    ctext(d, cx, y+34, txt, SAN(fsz), PAPER)

def chain_arrow(d, cx, y0, y1, col=AMBER):
    d.line([(cx, y0), (cx, y1-26)], fill=col, width=10)
    d.polygon([(cx-26, y1-30), (cx+26, y1-30), (cx, y1+4)], fill=col)

def b1():   # WTF: 결론 카드 — 보수당 = 복지·국영기업 (보는 글)
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1000, 500, (52, 46, 30)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([120, TOP+60, BW-120, TOP+860], 34, fill=(26, 30, 44),
                        outline=KMT_BLUE, width=10)
    d.rectangle([120, TOP+60, BW-120, TOP+240], fill=KMT_BLUE)
    ctext(d, BW/2, TOP+100, "보수당", SER(96), PAPER)
    ctext(d, BW/2, TOP+330, "복지 확대", SAN(88), (255, 228, 0))
    ctext(d, BW/2, TOP+520, "국영기업 수호", SAN(88), (255, 228, 0))
    ctext(d, BW/2, TOP+710, "民生 · 國營", SER(64), tuple(int(c*0.8) for c in PAPER))
    return im

def b2():   # 전제: 1946 갈림길
    im = night(); d = ImageDraw.Draw(im)
    cx, jy = BW/2, TOP+760
    d.line([(cx, jy+520), (cx, jy)], fill=(120, 124, 138), width=14)
    d.line([(cx, jy), (cx-300, jy-420)], fill=(70, 74, 88), width=10)     # 어두운 갈래
    d.line([(cx, jy), (cx+300, jy-420)], fill=AMBER, width=14)            # 국민당 승리
    d.ellipse([cx-26, jy-26, cx+26, jy+26], fill=PAPER)
    ctext(d, cx-330, jy-520, "공산당", SAN(50), (110, 114, 128))
    ctext(d, cx+330, jy-540, "국민당 승리", SAN(56), AMBER)
    ctext(d, BW/2, TOP+60, "1946", SER(170), PAPER, 8, INK)
    return im

def b3():   # 약속: 왜?
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+240, "왜?", SER(300), (255, 228, 0))
    ctext(d, BW/2, TOP+700, "역사가 답합니다", SER(80), PAPER)
    return im

def b4():   # 원인 A: 인과사슬 첫 고리
    im = night(); d = ImageDraw.Draw(im)
    chain_node(d, BW/2, TOP+60, 640, "국민당 승리", AMBER)
    chain_arrow(d, BW/2, TOP+190, TOP+280)
    chain_node(d, BW/2, TOP+280, 640, "반공 개발국가", AMBER)
    icons = ["국영 철강", "국영 반도체", "철도 · 항만"]
    for i, t in enumerate(icons):
        y = TOP+520+i*180
        d.rounded_rectangle([240, y, BW-240, y+130], 20, fill=(24, 28, 40),
                            outline=(100, 106, 122), width=5)
        d.ellipse([300, y+40, 350, y+90], fill=(120, 96, 44))
        ctext(d, BW/2+30, y+34, t, SAN(56), PAPER)
    return im

def b5():   # 원인 A2: 統盾工 (v1 재사용)
    im = night(); d = ImageDraw.Draw(im)
    for i, (ch, lab) in enumerate([("統", "통일"), ("盾", "반공"), ("工", "산업화")]):
        y = TOP+30+i*280
        d.rounded_rectangle([200, y, BW-200, y+240], 30, fill=(28, 32, 46),
                            outline=KMT_BLUE, width=8)
        ctext(d, 360, y+36, ch, SER(140), AMBER)
        ctext(d, 600, y+70, lab, SAN(80), PAPER, anchor="la")
    return im

def b6():   # 원인 B: 제도화 — 보험증 + 천젠궈 (v1 재사용 + 태그)
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([BW/2-360, TOP+60, BW/2+360, TOP+780], fill=PAPER)
    ctext(d, BW/2, TOP+120, "全民保險證", SER(88), INK)
    for k in range(5):
        w = 520-(k % 2)*140
        d.line([(BW/2-280, TOP+290+k*80), (BW/2-280+w, TOP+290+k*80)], fill=(150, 140, 124), width=8)
    st = seal_word("國民"); im.paste(st, (int(BW/2+80), TOP+500), st)
    name = "천젠궈 (63) · 국영기업 근속 34년"
    f = SAN(38); tw = d.textbbox((0, 0), name, font=f)[2]
    d.rounded_rectangle([BW/2-tw/2-20, 1700, BW/2+tw/2+20, 1772], 14, fill=INK)
    d.text((BW/2-tw/2, 1714), name, font=f, fill=PAPER)
    return im

def b7():   # 원인 B2: 민주화 이후에도 — 기존 질서 리본 + 실루엣 (v1 b4 재사용)
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1150, 470, (52, 48, 32)); d = ImageDraw.Draw(im)
    d.rectangle([180, 1180, 560, 1660], fill=(26, 30, 44), outline=(100, 106, 122), width=6)
    d.polygon([(160, 1180), (580, 1180), (370, 1020)], fill=(32, 36, 52))
    for wx in range(240, 520, 90):
        for wy in range(1250, 1600, 110):
            d.rectangle([wx, wy, wx+50, wy+66], fill=(120, 96, 44))
    d.rectangle([640, 1300, 1040, 1660], fill=(24, 28, 40), outline=(100, 106, 122), width=6)
    d.polygon([(640, 1300), (740, 1220), (840, 1300), (940, 1220), (1040, 1300)], fill=(24, 28, 40))
    d.rectangle([700, 1120, 760, 1300], fill=(40, 44, 58))
    d.rounded_rectangle([BW/2-330, TOP+60, BW/2+330, TOP+240], 26, fill=RED)
    ctext(d, BW/2, TOP+96, "기존 질서", SER(100), PAPER)
    ctext(d, BW/2, TOP+300, "民主化 이후에도", SAN(56), PAPER)
    return im

def b8():   # Second Hook: 뒤집힘 (v1 b7 재사용)
    im = night(); d = ImageDraw.Draw(im)
    d.line([(180, 1660), (BW-180, 1660)], fill=(90, 94, 108), width=6)
    for yr, x in [("1970", 260), ("1980", BW/2), ("1990", BW-260)]:
        big = yr == "1980"; r = 22 if big else 14
        d.ellipse([x-r, 1660-r, x+r, 1660+r], fill=AMBER)
        ctext(d, x, 1700, yr, SAN(56 if big else 44), AMBER if big else PAPER)
    d.rounded_rectangle([BW/2-460, TOP+120, BW/2-40, TOP+300], 22,
                        fill=(28, 36, 48), outline=STEEL, width=6)
    ctext(d, BW/2-250, TOP+150, "시장자유파", SAN(54), PAPER)
    d.rounded_rectangle([BW/2+40, TOP+430, BW/2+460, TOP+610], 22,
                        fill=(30, 44, 38), outline=GREEN, width=6)
    ctext(d, BW/2+250, TOP+460, "진보 연합", SAN(54), PAPER)
    d.line([(BW/2-240, TOP+310), (BW/2-140, TOP+400), (BW/2+60, TOP+470)],
           fill=AMBER, width=10, joint="curve")
    d.polygon([(BW/2+60, TOP+470), (BW/2-10, TOP+470), (BW/2+40, TOP+412)], fill=AMBER)
    ctext(d, BW/2, TOP+700, "정치가 뒤집힌다", SER(96), PAPER, 6, INK)
    return im

def b9():   # Payoff: 인과사슬 전체 회수 (원칙 5 — 논증)
    im = night(); d = ImageDraw.Draw(im)
    steps = [("국민당 승리", AMBER), ("반공 개발국가", AMBER),
             ("국가주도 산업화", AMBER), ("민주화", PAPER)]
    y = TOP+20
    for i, (t, col) in enumerate(steps):
        chain_node(d, BW/2, y, 620, t, col, 50)
        if i < 3: chain_arrow(d, BW/2, y+130, y+196)
        y += 196
    y += 10
    d.line([(BW/2, y-66), (BW/2-230, y+10)], fill=(255, 228, 0), width=8)
    d.line([(BW/2, y-66), (BW/2+230, y+10)], fill=GREEN, width=8)
    d.rounded_rectangle([120, y+10, BW/2-30, y+180], 22, fill=(28, 32, 46),
                        outline=(255, 228, 0), width=7)
    ctext(d, (120+BW/2-30)/2, y+38, "보수", SAN(48), (255, 228, 0))
    ctext(d, (120+BW/2-30)/2, y+104, "국가개입", SAN(44), PAPER)
    d.rounded_rectangle([BW/2+30, y+10, BW-120, y+180], 22, fill=(28, 32, 46),
                        outline=GREEN, width=7)
    ctext(d, (BW/2+30+BW-120)/2, y+38, "진보", SAN(48), GREEN)
    ctext(d, (BW/2+30+BW-120)/2, y+104, "민영화", SAN(44), PAPER)
    return im

def b10():  # 확장: 중국에서 한반도로
    im = night(); d = ImageDraw.Draw(im)
    d.polygon([(180, 900), (420, 760), (700, 820), (820, 1020), (700, 1260),
               (430, 1320), (230, 1160)], outline=(120, 124, 138), width=8)
    ctext(d, 450, 1010, "自由中國", SER(64), tuple(int(c*0.85) for c in PAPER))
    d.polygon([(850, 1060), (930, 1020), (990, 1120), (950, 1300), (870, 1330),
               (880, 1180)], outline=AMBER, width=8)
    ctext(d, 918, 1370, "한국", SAN(52), AMBER)
    d.line([(700, 1040), (860, 1120)], fill=AMBER, width=10)
    d.polygon([(860, 1120), (800, 1128), (836, 1074)], fill=AMBER)
    ctext(d, BW/2, TOP+60, "다음 뒤집힘", SER(96), PAPER, 6, INK)
    return im

def b11():  # 다음 모순 — 하드컷
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+180, "이 세계의", SER(110), PAPER)
    ctext(d, BW/2, TOP+380, "한국 보수는", SER(130), PAPER)
    ctext(d, BW/2, TOP+620, "친중입니다", SER(150), (255, 228, 0))
    return im

VOJ = json.load(open(f"{ROOT}/vo2/lines.json"))
GAP = 0.12
SC = []; t0 = 0.0
for p in VOJ:
    secs = p["dur"]+GAP+(0.10 if p["id"] == "s11" else 0)   # 하드컷: 꼬리 없음
    SC.append({"id": p["id"], "secs": secs, "t0": t0,
               "chips": UI.chunks_for(p["text"], p["dur"]+0.15)})
    t0 += secs
print(f"audio {mix_audio([(s['id'], s['secs']) for s in SC], f'{ROOT}/vo2', f'{ROOT}/mix2.wav', lead=0.15):.2f}s")

BULD = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11]
def smooth(p): return p*p*(3-2*p)
def make_anim(si, sc):
    def anim(im, t):
        UI.title_band(im, "자유중국의 보수는", "누구인가?",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP2",
                      world="가상 역사 · 국민당이 이긴 세계의 보수")
        for c, cs, cd in sc["chips"]:
            if cs <= t < cs+cd+0.10:
                UI.chip(im, c, t-cs); break
        return im
    return anim
SCENES = []
for i, sc in enumerate(SC):
    kb = (1.07, 1.00, 0, -25) if i % 2 == 0 else (1.00, 1.06, 15, 0)
    SCENES.append((BULD[i], sc["secs"], kb, make_anim(i, sc)))

import noir_kit as NK
_orig = NK.kb_crop
NK.kb_crop = lambda base, p, kb: _orig(base, smooth(p), kb)
n, rc = NK.encode(SCENES, f"{ROOT}/mix2.wav", f"{ROOT}/jayu_ep2_v2.mp4", seed0=2000, trans=0.20)
print("frames", n, "rc", rc)
