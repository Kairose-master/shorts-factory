"""EP7 「일본 좌파가 재무장을 주장한 이유」 — 원칙 v1.0 고정 70초 포맷 렌더. ACT III.

WTF: 한 실루엣에 모순된 두 말풍선(기지 축소 / 군비 증강) — 같은 사람.
좌표 안전 규칙: 장면 요소 base y 540~1410, 태그류 1700~1780. 오버레이는 1080 출력 좌표계.
한자는 한국 한자음 범위(反戰·自律·同盟 등)만 사용.
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
    return glow(im, BW/2, 1050, 480, (40, 44, 34))

def s1_overlay(im, t):
    """한 실루엣 + 모순된 두 말풍선 스태거 (출력 1080 좌표계)."""
    OW = UI.W
    d = ImageDraw.Draw(im, "RGBA")
    e0 = min(1, max(t, 0)/0.30)
    a0 = int(255*e0)
    px, gy = OW//2, 1330
    d.ellipse([px-46, gy-420, px+46, gy-328], fill=(230, 205, 180, a0))
    d.pieslice([px-50, gy-428, px+50, gy-352], 180, 360, fill=(40, 34, 30, a0))
    d.rounded_rectangle([px-70, gy-334, px+70, gy], 36, fill=(52, 56, 68, a0))
    def bubble(x0, y0, x1, y1, txt, t0, tail_x):
        if t <= t0: return
        e = UI.ease_out_back((t-t0)/0.30)
        a = int(255*min(1, (t-t0)/0.18))
        w = (x1-x0)*min(e, 1.05)/2; cx = (x0+x1)/2
        d.rounded_rectangle([cx-w, y0, cx+w, y1], 26, fill=(242, 233, 220, a))
        if e > 0.6:
            d.text((cx, (y0+y1)/2-30), txt, font=SAN(46), fill=(20, 17, 15, a), anchor="ma")
            d.polygon([(tail_x, y1-4), (tail_x+70, y1-4), (px, gy-380)], fill=(242, 233, 220, a))
    bubble(60, 620, 520, 800, "미군기지\n축소", 0.12, 330)
    bubble(OW-520, 700, OW-60, 880, "일본군\n강화", 0.40, OW-400)
    if t > 0.80:
        a = int(255*min(1, (t-0.80)/0.2))
        d.text((OW//2, 1450), "같은 사람의 말", font=SAN(56), fill=(255, 228, 0, a),
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
    ctext(d, BW/2, TOP+160, "좌파입니다", SER(140), YELLOW)
    ctext(d, BW/2, TOP+460, "왜?", SER(220), PAPER)
    return im

def b4():   # 원인 A: 기존 질서 = 미군 — 열도 + 기지 + 우산
    im = night(); d = ImageDraw.Draw(im)
    jp = [(300, 800), (520, 700), (760, 760), (900, 900), (820, 1120),
          (600, 1220), (380, 1160), (280, 980)]
    d.polygon(jp, outline=(150, 154, 166), width=9)
    for bx, by in ((470, 880), (700, 940), (560, 1080)):
        d.ellipse([bx-16, by-16, bx+16, by+16], fill=RED)
        d.polygon([(bx, by-40), (bx-12, by-16), (bx+12, by-16)], fill=RED)
    cx, cy = BW/2, TOP+130
    d.arc([cx-330, cy, cx+330, cy+560], 180, 360, fill=STEEL, width=14)      # 우산
    d.line([(cx, cy+280), (cx, cy+520)], fill=STEEL, width=10)
    ctext(d, cx, cy-70, "안보 우산", SAN(54), (150, 180, 205))
    ctext(d, BW/2, 1500, "기존 질서 = 미군", SER(84), PAPER, 5, INK)
    return im

def b5():   # 원인 A2: 우파 = 동맹 질서 수호
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([BW/2-360, TOP+150, BW/2+360, TOP+390], 28,
                        fill=(28, 32, 46), outline=YELLOW, width=8)
    ctext(d, BW/2, TOP+200, "우파", SAN(64), YELLOW)
    ctext(d, BW/2, TOP+300, "동맹 = 국익", SAN(52), PAPER)
    st = seal_word("同盟"); im.paste(st, (int(BW/2-st.width/2), TOP+520), st)
    ctext(d, BW/2, TOP+900, "질서를 지키는 쪽", SER(80), PAPER, 5, INK)
    return im

def b6():   # 원인 B: 좌파의 언어 — 자율 3종
    im = night(); d = ImageDraw.Draw(im)
    for i, (ch, lab) in enumerate([("基地", "기지 반대"), ("主權", "주권 회복"), ("自立", "대미 자립")]):
        y = TOP+30+i*280
        d.rounded_rectangle([200, y, BW-200, y+240], 30, fill=(26, 32, 28),
                            outline=GREEN, width=8)
        ctext(d, 370, y+36, ch, SER(120), AMBER)
        ctext(d, 640, y+70, lab, SAN(76), PAPER, anchor="la")
    d.rounded_rectangle([BW/2-200, 1445, BW/2+200, 1545], 20, outline=GREEN, width=6)
    ctext(d, BW/2, 1465, "자율의 언어", SAN(54), (160, 210, 150))
    return im

def b7():   # 원인 B2: 등식
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+140, "자율의 값", SER(120), PAPER)
    ctext(d, BW/2, TOP+380, "=", SER(160), (150, 152, 160))
    ctext(d, BW/2, TOP+600, "자주국방", SER(150), YELLOW)
    return im

def b8():   # Second Hook: 평화 집회의 군비 서명 부스
    im = night(); d = ImageDraw.Draw(im)
    fx = 290
    d.line([(fx, TOP+160), (fx, TOP+820)], fill=(90, 94, 108), width=12)
    d.polygon([(fx+6, TOP+160), (fx+390, TOP+245), (fx+6, TOP+330)], fill=GREEN)
    ctext(d, fx+140, TOP+206, "反戰", SER(76), INK, anchor="la")
    d.rectangle([BW/2+30, TOP+520, BW-140, TOP+820], fill=(58, 46, 40))       # 서명대
    d.rectangle([BW/2+60, TOP+420, BW-170, TOP+520], fill=PAPER)
    ctext(d, (BW/2+60+BW-170)/2, TOP+440, "軍備 증강 서명", SAN(42), INK)
    for k in range(3):
        d.line([(BW/2+90, TOP+700+k*34), (BW-200, TOP+700+k*34)], fill=(120, 110, 96), width=6)
    ctext(d, BW/2, 1420, "같은 부스", SER(88), PAPER, 6, INK)
    return im

def b9():   # Payoff: 사슬 회수
    im = night(); d = ImageDraw.Draw(im)
    steps = [("원칙: 자율", GREEN), ("미군 감축", PAPER),
             ("방위 공백", PAPER), ("결론: 재무장", YELLOW)]
    y = TOP+40
    for i, (t, col) in enumerate(steps):
        chain_node(d, BW/2, y, 640, t, col, 50)
        if i < 3: chain_arrow(d, BW/2, y+126, y+206)
        y += 206
    ctext(d, BW/2, y+30, "원칙이 같아도", SAN(48), tuple(int(c*0.9) for c in PAPER))
    ctext(d, BW/2, y+110, "질서가 다르면 결론이 뒤집힌다", SAN(48),
          tuple(int(c*0.9) for c in PAPER))
    return im

def b10():  # 확장: 질문
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+160, "그럼 친미는,", SER(120), PAPER)
    ctext(d, BW/2, TOP+420, "보수일까?", SER(160), YELLOW)
    return im

def b11():  # 다음 모순 — 하드컷 (정본 EP8 훅)
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+120, "1950 친미 보수", SER(110), PAPER)
    ctext(d, BW/2, TOP+340, "2050 친미 진보", SER(110), (140, 200, 130))
    ctext(d, BW/2, TOP+620, "동시에 존재합니다", SER(120), YELLOW)
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
        UI.title_band(im, "일본 좌파는 왜", "재무장을 외쳤나?",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP7",
                      world="가상 역사 · 국민당이 이긴 세계의 일본")
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep7.mp4", seed0=7000, trans=0.20)
print("frames", n, "rc", rc)
