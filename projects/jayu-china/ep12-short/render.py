"""EP12 「2080 자유중국 총선」 — 원칙 v1.0 고정 70초 포맷 렌더. 시즌1 피날레.

WTF: 5표 배지가 찍히고 좌우 자가 부러져 떨어진다.
Payoff: 좌우 한 줄 축에 X, 이슈 다섯 축이 세로로 선다.
정본 §13 준수: 결과 대신 질문으로 끝난다 (시즌2 예고).
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
LBLUE = (110, 150, 205)
RRED = (205, 110, 100)
PURP = (170, 140, 205)
CYAN = (120, 190, 205)

ISSUES = [("經", "경제"), ("外", "외교"), ("福", "복지"), ("地", "지역"), ("技", "기술")]
PARTY_COL = [AMBER, GREEN, LBLUE, PURP, CYAN]

def issue_card(d, x0, y, x1, ch, lab, opts=None, h=150):
    d.rounded_rectangle([x0, y, x1, y+h], 22, fill=(28, 32, 46), outline=STEEL, width=6)
    ctext(d, x0+95, y+26, ch, SER(64), AMBER)
    ctext(d, x0+185, y+30, lab, SAN(48), PAPER, anchor="la")
    if opts:
        for i, (t, col) in enumerate(opts):
            ox0 = x0+185+i*300
            d.rounded_rectangle([ox0, y+88, ox0+270, y+138], 14,
                                fill=tuple(int(c*0.28) for c in col), outline=col, width=4)
            ctext(d, ox0+135, y+96, t, SAN(32), PAPER)

def b1():
    im = night()
    return glow(im, BW/2, 1000, 500, (46, 42, 34))

def s1_overlay(im, t):
    """'5票' 스탬프 + 좌우 자가 부러진다 (1080 좌표계)."""
    OW = UI.W
    d = ImageDraw.Draw(im, "RGBA")
    e0 = UI.ease_out_back(min(1, max(t, 0)/0.35))
    if t > 0:
        s = min(e0, 1.05)
        d.ellipse([OW//2-int(230*s), 800-int(230*s), OW//2+int(230*s), 800+int(230*s)],
                  outline=(255, 228, 0, 255), width=10)
        d.text((OW//2, 800), "5票", font=SER(int(150*s)), fill=(242, 233, 220, 255), anchor="mm")
    if t > 0.9:
        a = int(255*min(1, (t-0.9)/0.2))
        prog = min(1, (t-0.9)/0.5)
        drop = int(90*prog*prog)
        d.line([(OW//2-330, 1180+drop//3), (OW//2-40, 1210+drop)], fill=(110, 150, 205, a), width=16)
        d.line([(OW//2+40, 1210+drop), (OW//2+330, 1180+drop//3)], fill=(205, 110, 100, a), width=16)
        d.text((OW//2-360, 1120+drop//3), "좌", font=SAN(40), fill=(110, 150, 205, a), anchor="ma")
        d.text((OW//2+360, 1120+drop//3), "우", font=SAN(40), fill=(205, 110, 100, a), anchor="ma")
        if t > 1.25:
            a2 = int(255*min(1, (t-1.25)/0.2))
            d.text((OW//2, 1330), "버리고 오세요", font=SER(60), fill=(150, 154, 166, a2), anchor="ma")
    return im

def b2():   # 전제: 1946 갈림길 → 2080 (시리즈 앵커, 피날레 확장)
    im = night(); d = ImageDraw.Draw(im)
    cx, jy = BW/2, TOP+760
    d.line([(cx, jy+520), (cx, jy)], fill=(120, 124, 138), width=14)
    d.line([(cx, jy), (cx-300, jy-420)], fill=(70, 74, 88), width=10)
    d.line([(cx, jy), (cx+300, jy-420)], fill=AMBER, width=14)
    d.ellipse([cx-26, jy-26, cx+26, jy+26], fill=PAPER)
    ctext(d, cx-330, jy-520, "공산당", SAN(50), (110, 114, 128))
    ctext(d, cx+330, jy-540, "국민당 승리", SAN(56), AMBER)
    ctext(d, BW/2, TOP+40, "1946 → 2080", SER(130), PAPER, 8, INK)
    ctext(d, BW/2, TOP+230, "총선", SER(96), YELLOW)
    return im

def b3():   # 약속: 투표용지 — 이슈 5줄
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([200, TOP+90, BW-200, TOP+880], 26, fill=(242, 233, 220))
    ctext(d, BW/2, TOP+130, "選擧 投票", SAN(42), (120, 110, 96))
    for i, (ch, lab) in enumerate(ISSUES):
        y = TOP+230+i*125
        d.rectangle([270, y, 320, y+50], outline=(90, 84, 74), width=5)
        ctext(d, 400, y-6, ch, SER(56), (150, 60, 40))
        ctext(d, 500, y, lab, SAN(48), (20, 17, 15), anchor="la")
    return im

def b4():   # 원인A: 경제·외교 두 이슈 카드
    im = night(); d = ImageDraw.Draw(im)
    issue_card(d, 140, TOP+170, BW-140, "經", "경제",
               [("지킨다", AMBER), ("쪼갠다", GREEN)])
    issue_card(d, 140, TOP+400, BW-140, "外", "외교",
               [("동맹", CYAN), ("패권", RRED)])
    ctext(d, BW/2, TOP+40, "첫 두 표", SER(72), PAPER, 5, INK)
    ctext(d, BW/2, TOP+640, "같은 당이 아닐 수도", SAN(48), (150, 154, 166))
    return im

def b5():   # 원인A2: 두 표 집계
    im = night(); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+90, "2 / 5", SER(170), YELLOW)
    d.rounded_rectangle([300, TOP+380, BW-300, TOP+520], 22, fill=(28, 32, 46),
                        outline=STEEL, width=6)
    ctext(d, BW/2, TOP+416, "벌써 다른 당?", SAN(56), PAPER)
    return im

def b6():   # 원인B: 복지·지역·기술
    im = night(); d = ImageDraw.Draw(im)
    issue_card(d, 140, TOP+120, BW-140, "福", "복지",
               [("성역", AMBER), ("개혁", PURP)])
    issue_card(d, 140, TOP+340, BW-140, "地", "지역",
               [("난징", AMBER), ("성 자치", LBLUE)])
    issue_card(d, 140, TOP+560, BW-140, "技", "기술",
               [("국가 규제", AMBER), ("성·민간", CYAN)])
    ctext(d, BW/2, TOP+30, "남은 세 표", SER(72), PAPER, 5, INK)
    return im

def b7():   # 원인B2: 흩어진 표 — 당별 기둥에 체크 분산
    im = night(); d = ImageDraw.Draw(im)
    names = ["국민당", "진보당", "자치연합", "청년당", "미래당"]
    marks = [2, 1, 1, 0, 1]
    for i, (nm, col, mk) in enumerate(zip(names, PARTY_COL, marks)):
        x = 190 + i*220
        d.rounded_rectangle([x-95, TOP+200, x+95, TOP+640], 20, fill=(24, 27, 38),
                            outline=col, width=6)
        ctext(d, x, TOP+230, nm, SAN(36), col)
        for j in range(mk):
            y = TOP+330+j*130
            d.line([(x-40, y+40), (x-8, y+76)], fill=PAPER, width=10)
            d.line([(x-8, y+76), (x+48, y+8)], fill=PAPER, width=10)
    ctext(d, BW/2, TOP+40, "당신의 5표는", SER(72), PAPER, 5, INK)
    ctext(d, BW/2, TOP+720, "몇 개의 당에?", SER(100), YELLOW)
    return im

def b8():   # Second Hook: 승자는 연합
    im = night(); d = ImageDraw.Draw(im)
    xs = [250, 620, 990]
    for x, col, nm in zip(xs, [AMBER, LBLUE, CYAN], ["국민당", "자치연합", "미래당"]):
        d.rounded_rectangle([x-140, TOP+260, x+140, TOP+440], 22, fill=(28, 32, 46),
                            outline=col, width=7)
        ctext(d, x, TOP+310, nm, SAN(44), col)
    d.line([(xs[0], TOP+250), (xs[0], TOP+150), (xs[2], TOP+150), (xs[2], TOP+250)],
           fill=YELLOW, width=8)
    d.line([(xs[1], TOP+250), (xs[1], TOP+150)], fill=YELLOW, width=8)
    ctext(d, BW/2, TOP+70, "聯合", SER(84), YELLOW)
    ctext(d, BW/2, TOP+560, "승자는 정당이 아니라,", SER(76), PAPER)
    ctext(d, BW/2, TOP+680, "연합이다", SER(110), YELLOW)
    return im

def b9():   # Payoff: 좌우 한 줄 축에 X — 이슈 다섯 축
    im = night(); d = ImageDraw.Draw(im)
    d.line([(200, TOP+180), (BW-200, TOP+180)], fill=(100, 106, 122), width=10)
    ctext(d, 240, TOP+100, "좌", SAN(40), LBLUE)
    ctext(d, BW-240, TOP+100, "우", SAN(40), RRED)
    d.line([(BW/2-140, TOP+120), (BW/2+140, TOP+250)], fill=RED, width=13)
    d.line([(BW/2+140, TOP+120), (BW/2-140, TOP+250)], fill=RED, width=13)
    for i, (ch, lab) in enumerate(ISSUES):
        x = 210 + i*205
        d.line([(x, TOP+380), (x, TOP+640)], fill=PARTY_COL[i], width=8)
        ctext(d, x, TOP+660, lab, SAN(36), (150, 154, 166))
    ctext(d, BW/2, TOP+780, "축은 하나가 아니라,", SER(76), PAPER)
    ctext(d, BW/2, TOP+890, "다섯이었다", SER(104), YELLOW)
    return im

def b10():  # 확장: 시즌 결산 스트립
    im = night(); d = ImageDraw.Draw(im)
    rows = [("EP2", "복지를 지키는 보수"), ("EP3", "민영화를 외치는 진보"),
            ("EP5", "반중은 진보의 구호"), ("EP9", "독립 없는 대만 선거"),
            ("EP10", "보수는 시장이 아니다")]
    for i, (ep, txt) in enumerate(rows):
        y = TOP+140+i*135
        d.rounded_rectangle([170, y, BW-170, y+112], 18, fill=(24, 27, 38),
                            outline=(80, 86, 100), width=5)
        ctext(d, 300, y+28, ep, SAN(44), AMBER)
        ctext(d, 420, y+32, txt, SAN(42), PAPER, anchor="la")
    ctext(d, BW/2, TOP+30, "시즌의 이유, 한 판에", SER(64), PAPER, 5, INK)
    return im

def b11():  # 다음 모순 — 시즌2 예고 (질문만 남긴다)
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+100, "왜 우리는 자꾸,", SER(96), PAPER)
    ctext(d, BW/2, TOP+320, "한 줄로 세우려", SER(110), PAPER)
    ctext(d, BW/2, TOP+540, "했을까?", SER(150), YELLOW)
    ctext(d, BW/2, TOP+850, "시즌 2 「자유중국의 철학」", SAN(50), (150, 154, 166))
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
        UI.title_band(im, "당신에게 5표", "2080 총선",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP12",
                      world="가상 역사 · 국민당이 이긴 세계 · 시즌 피날레")
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep12.mp4", seed0=12000, trans=0.20)
print("frames", n, "rc", rc)
