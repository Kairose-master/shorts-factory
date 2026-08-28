"""EP10 「자유중국의 20대는 누구를 보수라 부를까」 — 원칙 v1.0 고정 70초 포맷 렌더. ACT IV 시작.

WTF: '保守 = 市場' 등식에서 市場에 붉은 X — 2080년의 상식 카드.
Payoff: 지키면 保守 / 바꾸면 進步 — 내용이 아니라 위치 다이어그램.
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

def b1():
    im = night()
    return glow(im, BW/2, 1000, 500, (46, 42, 34))

def s1_overlay(im, t):
    """상식 카드 스태거 — '保守 = 市場'이 찍히고 市場에 붉은 X, 노란 ? (1080 좌표계)."""
    OW = UI.W
    d = ImageDraw.Draw(im, "RGBA")
    e0 = UI.ease_out_back(min(1, max(t, 0)/0.32))
    w = int(400*min(e0, 1.06)); h = int(300*min(e0, 1.06))
    d.rounded_rectangle([OW//2-w, 850-h, OW//2+w, 850+h], 22, fill=(242, 233, 220, 255))
    if e0 > 0.5:
        d.text((OW//2, 850-h+40), "2080년의 상식?", font=SAN(40),
               fill=(120, 110, 96), anchor="ma")
        stamps = [("保守", OW//2-210, 0.40), ("=", OW//2, 0.55), ("市場", OW//2+210, 0.68)]
        for txt, x, t0 in stamps:
            if t <= t0: continue
            a = int(255*min(1, (t-t0)/0.16))
            d.text((x, 850), txt, font=SER(120), fill=(20, 17, 15, a), anchor="mm")
        if t > 0.95:
            a2 = int(255*min(1, (t-0.95)/0.18))
            x0, x1 = OW//2+90, OW//2+330
            d.line([(x0, 780), (x1, 920)], fill=(200, 69, 46, a2), width=14)
            d.line([(x1, 780), (x0, 920)], fill=(200, 69, 46, a2), width=14)
        if t > 1.25:
            a3 = int(255*min(1, (t-1.25)/0.2))
            d.text((OW//2, 850+h+30), "?", font=SER(130), fill=(255, 228, 0, a3), anchor="ma")
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
    ctext(d, BW/2, TOP+180, "이 세계 20대의", SER(110), PAPER)
    ctext(d, BW/2, TOP+420, "보수는?", SER(180), YELLOW)
    return im

def b4():   # 원인 A: 할아버지 세대의 기억 — 국가가 만든 세 가지
    im = night(); d = ImageDraw.Draw(im)
    for i, (ch, lab) in enumerate([("鐵", "국가가 깐 철도"), ("工", "국가가 세운 공단"),
                                   ("金", "국가가 만든 연금")]):
        y = TOP+80+i*185
        d.rounded_rectangle([170, y, 950, y+165], 24, fill=(28, 32, 46),
                            outline=STEEL, width=7)
        ctext(d, 285, y+28, ch, SER(84), AMBER)
        ctext(d, 400, y+50, lab, SAN(50), PAPER, anchor="la")
    ctext(d, BW/2, TOP+660, "그걸 지키자는 게", SER(76), PAPER)
    ctext(d, BW/2, TOP+770, "보수가 됐다", SER(108), YELLOW)
    return im

def b5():   # 원인 A2: 기억이 묶는다 — 밧줄 원 안의 묶음
    im = night(); d = ImageDraw.Draw(im)
    cx, cy = BW/2, TOP+420
    d.ellipse([cx-420, cy-280, cx+420, cy+280], outline=AMBER, width=10)
    for txt, ox, oy in [("복지", -230, -90), ("국가", 90, -160), ("질서", -60, 90)]:
        d.rounded_rectangle([cx+ox-115, cy+oy-55, cx+ox+115, cy+oy+55], 20,
                            fill=(28, 32, 46), outline=(80, 86, 100), width=6)
        ctext(d, cx+ox, cy+oy-30, txt, SAN(52), PAPER)
    ctext(d, BW/2, TOP+40, "논리가 아니라", SER(80), PAPER, 5, INK)
    ctext(d, BW/2, TOP+760, "기억이 묶는다", SER(108), YELLOW)
    return im

def b6():   # 원인 B: 복지는 공기 — 파장 배경
    im = night()
    im = glow(im, BW/2, 900, 430, (40, 46, 40))
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(4):
        y = TOP+520+i*120
        d.arc([120, y, BW-120, y+240], 200, 340, fill=(150, 180, 205, 120-i*22), width=8)
    ctext(d, BW/2, TOP+100, "태어나 보니", SER(84), PAPER)
    ctext(d, BW/2, TOP+250, "복지는 공기", SER(130), YELLOW)
    ctext(d, BW/2, TOP+900, "이념이 아니라, 원래 있던 질서", SAN(52), (150, 154, 166))
    return im

def b7():   # 원인 B2: 난징대 캠퍼스 — 실명 시민
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([260, TOP+270, 980, TOP+350], fill=(60, 64, 78))           # 정문 상판
    ctext(d, BW/2, TOP+282, "南京大學", SAN(48), PAPER)
    d.rectangle([320, TOP+350, 400, TOP+780], fill=(46, 50, 64))
    d.rectangle([840, TOP+350, 920, TOP+780], fill=(46, 50, 64))
    d.rectangle([0, TOP+780, BW, TOP+800], fill=(60, 64, 78))
    ctext(d, BW/2, TOP+40, "보수 아저씨 = 연금 지키는 사람", SER(68), PAPER, 5, INK)
    name = "천위팅 (20) · 난징대 2학년"
    f = SAN(38); tw = d.textbbox((0, 0), name, font=f)[2]
    d.rounded_rectangle([BW/2-tw/2-20, 1700, BW/2+tw/2+20, 1772], 14, fill=INK)
    d.text((BW/2-tw/2, 1714), name, font=f, fill=PAPER)
    return im

def b8():   # Second Hook: 같은 말, 다른 이름
    im = night(); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+40, "같은 말, 다른 이름", SER(80), PAPER, 5, INK)
    for i, (world, label, col) in enumerate([("여러분의 세계", "= 보수", STEEL),
                                             ("이 세계", None, RED)]):
        x0 = 130 if i == 0 else BW/2+50
        x1 = BW/2-50 if i == 0 else BW-130
        d.rounded_rectangle([x0, TOP+200, x1, TOP+700], 26, fill=(24, 27, 38),
                            outline=(80, 86, 100), width=7)
        ctext(d, (x0+x1)/2, TOP+240, world, SAN(40), (150, 154, 166))
        ctext(d, (x0+x1)/2, TOP+330, "복지를 줄이고", SAN(46), PAPER)
        ctext(d, (x0+x1)/2, TOP+400, "시장에 맡기자", SAN(46), PAPER)
        if label:
            ctext(d, (x0+x1)/2, TOP+540, label, SER(76), col)
    st = seal_word("急進", 200)
    im.paste(st, (int(BW/2+50+(BW-130-BW/2-50)/2-st.width/2), TOP+490), st)
    return im

def b9():   # Payoff: 내용이 아니라 위치
    im = night(); d = ImageDraw.Draw(im)
    d.line([(BW/2, TOP+140), (BW/2, TOP+560)], fill=(100, 106, 122), width=8)
    ctext(d, BW/2, TOP+70, "기존 질서", SAN(42), (150, 154, 166))
    for i, (verb, ch, col) in enumerate([("지키면", "保守", STEEL), ("바꾸면", "進步", GREEN)]):
        x0 = 140 if i == 0 else BW/2+80
        x1 = BW/2-80 if i == 0 else BW-140
        d.rounded_rectangle([x0, TOP+180, x1, TOP+520], 26, fill=(28, 32, 46),
                            outline=col, width=8)
        ctext(d, (x0+x1)/2, TOP+230, verb, SAN(52), PAPER)
        ctext(d, (x0+x1)/2, TOP+320, ch, SER(110), col)
    ctext(d, BW/2, TOP+640, "내용이 아니라", SER(88), PAPER)
    ctext(d, BW/2, TOP+770, "위치다", SER(120), YELLOW)
    return im

def b10():  # 확장: 라벨로는 모른다
    im = night(); d = ImageDraw.Draw(im)
    for txt, x, y in [("좌파", 330, TOP+150), ("우파", 880, TOP+210),
                      ("보수", 420, TOP+400), ("진보", 820, TOP+460)]:
        d.rounded_rectangle([x-140, y, x+140, y+110], 22, fill=(28, 32, 46),
                            outline=(80, 86, 100), width=6)
        ctext(d, x, y+22, txt, SAN(56), (150, 154, 166))
        ctext(d, x+110, y-36, "?", SER(76), RED)
    ctext(d, BW/2, TOP+700, "라벨로는,", SER(88), PAPER)
    ctext(d, BW/2, TOP+820, "모른다", SER(120), YELLOW)
    return im

def b11():  # 다음 모순 — 하드컷 (EP11 분류 게임 훅)
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+120, "이 사람은", SER(100), PAPER)
    ctext(d, BW/2, TOP+340, "좌파입니까,", SER(140), PAPER)
    ctext(d, BW/2, TOP+610, "우파입니까?", SER(140), YELLOW)
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
        UI.title_band(im, "2080년 캠퍼스의", "보수와 진보",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP10",
                      world="가상 역사 · 국민당이 이긴 세계의 2080년")
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep10.mp4", seed0=10000, trans=0.20)
print("frames", n, "rc", rc)
