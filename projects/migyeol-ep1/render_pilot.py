"""「미결」 No.1 — 가드너 미술관 도난 사건 (1990, 미해결).

문법: 궁금소 171x 과정 서술 — 고유명사+연도+숫자 인입, 시간순, 판단 없이 종료.
사실관계: FBI·가드너 미술관 공식 — 1990.3.18 / 경찰복 2인 / 81분 / 13점 /
베르메르·렘브란트 / $500M / 현상금 $10M / 빈 액자 상시 게시 / 미검거.
시각: Ledger Noir (noir_kit) — 빈 액자가 이 회차의 '빈칸'이다.
"""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw, ImageFilter

GOLD = (188, 154, 82); DGOLD = (120, 96, 48)
def tag(d, fg=PAPER): d.text((84, 120), "「미결」 No.1", font=SAN(44), fill=fg)

def cop(d, px, gy, h=330, cap=True):
    col = (9, 11, 17)
    top = gy - h
    d.ellipse([px-36, top+34, px+36, top+106], fill=col)
    if cap:
        d.rectangle([px-40, top+30, px+40, top+52], fill=(16, 20, 30))
        d.ellipse([px-46, top+16, px+46, top+52], fill=(16, 20, 30))
        d.line([(px-46, top+52), (px+52, top+52)], fill=(190, 150, 60), width=4)  # 모자 배지선
    d.rounded_rectangle([px-58, top+96, px+58, gy], 30, fill=col)

def frame_rect(d, box, ornate=True):
    x0, y0, x1, y1 = box
    d.rectangle([x0-26, y0-26, x1+26, y1+26], fill=DGOLD)
    d.rectangle([x0-16, y0-16, x1+16, y1+16], fill=GOLD)
    d.rectangle([x0, y0, x1, y1], fill=(26, 24, 30))
    if ornate:
        for cx, cy in ((x0-21, y0-21), (x1+21, y0-21), (x0-21, y1+21), (x1+21, y1+21)):
            d.ellipse([cx-12, cy-12, cx+12, cy+12], fill=GOLD)

def b1():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([100, 760, BW-100, 1660], fill=(15, 18, 27))                     # facade
    d.polygon([(60, 760), (BW-60, 760), (BW/2, 560)], fill=(19, 22, 32))         # pediment
    for k in range(4):                                                            # columns
        x = 190 + k*(BW-380)/3
        d.rectangle([x-34, 800, x+34, 1660], fill=(24, 28, 40))
    d.rectangle([BW/2-130, 1180, BW/2+130, 1660], fill=(30, 26, 20))             # door
    im = glow(im, BW/2, 1150, 220, (105, 72, 24)); d = ImageDraw.Draw(im)
    d.ellipse([BW/2-24, 1120, BW/2+24, 1168], fill=AMBER)                        # lamp
    cop(d, BW/2-105, 1660); cop(d, BW/2+105, 1660, h=315)
    ctext(d, BW/2, 250, "1990. 3. 18.", SER(150), PAPER, 8, INK)
    ctext(d, BW/2, 450, "새벽 1시, 보스턴", SAN(56), PAPER)
    tag(d); return im

def b2():
    im = Image.new("RGB", (BW, BH), (13, 15, 22)); d = ImageDraw.Draw(im)
    d.polygon([(BW-160, 480), (BW-100, 420), (240, 1560), (60, 1440)], fill=(34, 34, 40))
    im = im.filter(ImageFilter.GaussianBlur(5))
    im = glow(im, BW-130, 450, 180, (120, 100, 50)); d = ImageDraw.Draw(im)
    d.rectangle([0, 1560, BW, 2200], fill=(10, 12, 18))
    for px in (BW/2-130, BW/2+130):                                               # 묶인 두 사람
        cop(d, px, 1560, h=250, cap=False)
        for ry in (1400, 1450, 1500):
            d.line([(px-64, ry), (px+64, ry+14)], fill=(96, 78, 40), width=9)
    ctext(d, BW/2, 1720, "81분", SER(230), PAPER, 9, INK)
    tag(d); return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, BW, BH], fill=(22, 22, 28))
    im = glow(im, BW/2, 950, 620, (46, 40, 30)); d = ImageDraw.Draw(im)
    frame_rect(d, (150, 620, 545, 1140))
    for k in range(5):                                                            # 폭풍 바다 (양식화)
        d.arc([170+k*10, 760+k*54, 525-k*10, 1000+k*40], 190, 350, fill=(120, 130, 150), width=9)
    d.polygon([(300, 800), (360, 690), (410, 810), (350, 850)], fill=(80, 88, 104))
    frame_rect(d, (695, 620, 1090, 1140))
    d.rectangle([730, 700, 1050, 1100], fill=(50, 44, 40))                        # 실내악 (양식화)
    d.ellipse([780, 860, 860, 1010], fill=(180, 160, 120))
    d.ellipse([920, 840, 990, 980], fill=(150, 130, 100))
    d.rectangle([760, 720, 1020, 800], fill=(94, 80, 60))
    ctext(d, BW/2, 1350, "13점", SER(210), PAPER, 9, INK)
    ctext(d, BW/2, 1620, "5억 달러어치", SAN(60), PAPER)
    ctext(d, BW/2, BH-280, "베르메르 「합주」 — 현존 36점 중 하나였다", SAN(42), PAPER)
    tag(d); return im

def b4():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 420, "$10,000,000", SER(140), PAPER, 8, (40, 34, 28))
    ctext(d, BW/2, 620, "현상금 — 지금도 유효", SAN(56), PAPER)
    for px, q in ((BW/2-160, "?"), (BW/2+160, "?")):
        cop(d, px, 1560, h=380)
        ctext(d, px, 1180, q, SER(150), RED)
    d.line([(150, 1660), (BW-150, 1660)], fill=(60, 63, 74), width=5)
    ctext(d, BW/2, BH-280, "용의선상 다수 — 기소 0명", SAN(44), PAPER)
    tag(d); return im

def b5():
    im = Image.new("RGB", (BW, BH), (24, 23, 28)); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1000, 520, (52, 46, 34)); d = ImageDraw.Draw(im)
    frame_rect(d, (270, 560, BW-270, 1460))
    d.line([(BW/2-60, 1610), (BW/2+60, 1610)], fill=(70, 66, 60), width=6)       # 명패
    ctext(d, BW/2, 1650, "렘브란트 「갈릴리 바다의 폭풍」", SAN(44), PAPER)
    ctext(d, BW/2, 1720, "1990년 3월 18일부터 이 상태", SAN(40),
          tuple(int(c*0.85) for c in PAPER))
    tag(d); return im

def b6():
    im = Image.new("RGB", (BW, BH), (18, 17, 22)); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 900, 430, (42, 38, 30)); d = ImageDraw.Draw(im)
    frame_rect(d, (330, 520, BW-330, 1290))
    ctext(d, BW/2, 1420, "미결", SER(200), PAPER)
    redbar(d, 1720, "추리는 당신의 몫입니다")
    ctext(d, BW/2, BH-260, "미해결 — FBI 수사·현상금 진행 중 (1990– )", SAN(40), PAPER)
    tag(d); return im

def anim_snow(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    rng = np.random.default_rng(3)
    for k in range(14):
        x0 = rng.uniform(60, W-60)
        y = (t*34 + k*149) % (H+40) - 20
        d.ellipse([x0-2.5, y-2.5, x0+2.5, y+2.5], fill=(242, 233, 220, 52))
    return im
def anim_flash(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    a = int(20+14*math.sin(t*2.6))
    d.polygon([(W-90, 360), (W-40, 320), (170, 1400), (30, 1290)], fill=(255, 230, 170, a))
    return im
def anim_dot(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 11+2.6*math.sin(t*3.1)
    d.ellipse([W/2-r, 250-r, W/2+r, 250+r], outline=PAPER, width=5)
    return im

VO = {p["id"]: p["dur"] for p in json.load(open(f"{ROOT}/vo/lines.json"))}
GAP = 0.4
SECS = {k: VO[k]+GAP for k in VO}; SECS["s6"] = VO["s6"]+1.3
SC_A = [(k, SECS[k]) for k in ["s1", "s2", "s3", "s4", "s5", "s6"]]
total = mix_audio(SC_A, f"{ROOT}/vo", f"{ROOT}/mix.wav")
print(f"audio {total:.2f}s")
SCENES = [
 (b1, SECS["s1"], (1.08, 1.00, 0, -30), anim_snow),
 (b2, SECS["s2"], (1.00, 1.06, 20, 0), anim_flash),
 (b3, SECS["s3"], (1.09, 1.00, 0, 20), None),
 (b4, SECS["s4"], (1.00, 1.05, 0, 0), None),
 (b5, SECS["s5"], (1.10, 1.00, 0, -20), None),
 (b6, SECS["s6"], (1.00, 1.04, 0, 0), anim_dot),
]
n, rc = encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/migyeol_no1.mp4", seed0=300)
print("frames", n, "rc", rc)
