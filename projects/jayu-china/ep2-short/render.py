"""EP2 「자유중국의 보수는 누구인가」 — canon §10 비트, EP1 v2 인터페이스."""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../../malgap-style")
from noir_kit import *
import shorts_ui as UI
from PIL import Image, ImageDraw, ImageFilter
import numpy as _np

TOP = 560
KMT_BLUE = (36, 66, 122)

def pledge_card(d, y, txt, delay_ok=True):
    d.rounded_rectangle([140, y, BW-140, y+150], 22, fill=(30, 34, 48),
                        outline=(120, 126, 142), width=5)
    d.ellipse([180, y+55, 220, y+95], fill=AMBER)
    ctext(d, 260, y+40, txt, SAN(56), PAPER, anchor="la")

def b1():
    im = night(); d = ImageDraw.Draw(im)
    for i, t in enumerate(["국영 반도체 투자 확대", "복지연금 유지",
                           "국방비 증액", "지방정부 권한 제한"]):
        pledge_card(d, TOP+60+i*230, t)
    return im

def b2():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1100, 430, (48, 44, 32)); d = ImageDraw.Draw(im)
    cx, cy, R = BW/2, 1080, 380
    d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=(150, 152, 160), width=14)
    d.ellipse([cx-R+50, cy-R+50, cx+R-50, cy+R-50], outline=(90, 96, 112), width=5)
    ctext(d, cx-R+90, cy-34, "左", SER(76), STEEL)
    ctext(d, cx+R-90, cy-34, "右", SER(76), RED, anchor="ma")
    pts = [(cx-20, cy-40), (cx+150, cy-190), (cx+180, cy-140), (cx+30, cy-6),
           (cx+90, cy+180), (cx+40, cy+205), (cx-24, cy+30)]        # 꺾인 바늘
    d.polygon(pts, fill=PAPER)
    d.ellipse([cx-34, cy-34, cx+34, cy+34], fill=(40, 44, 58), outline=PAPER, width=8)
    ctext(d, BW/2, TOP+40, "고장난 나침반", SER(110), PAPER, 7, INK)
    return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    items = [("統", "통일"), ("盾", "반공"), ("工", "산업화")]
    for i, (ch, lab) in enumerate(items):
        y = TOP+30+i*280
        d.rounded_rectangle([200, y, BW-200, y+240], 30, fill=(28, 32, 46),
                            outline=KMT_BLUE, width=8)
        ctext(d, 360, y+36, ch, SER(140), AMBER)
        ctext(d, 600, y+70, lab, SAN(80), PAPER, anchor="la")
    return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1150, 470, (52, 48, 32)); d = ImageDraw.Draw(im)
    d.rectangle([180, 1180, 560, 1660], fill=(26, 30, 44), outline=(100, 106, 122), width=6)  # 청사
    d.polygon([(160, 1180), (580, 1180), (370, 1020)], fill=(32, 36, 52))
    for wx in range(240, 520, 90):
        for wy in range(1250, 1600, 110):
            d.rectangle([wx, wy, wx+50, wy+66], fill=(120, 96, 44))
    d.rectangle([640, 1300, 1040, 1660], fill=(24, 28, 40), outline=(100, 106, 122), width=6)  # 공장
    d.polygon([(640, 1300), (740, 1220), (840, 1300), (940, 1220), (1040, 1300)], fill=(24, 28, 40))
    d.rectangle([700, 1120, 760, 1300], fill=(40, 44, 58))
    for k in range(3):
        d.ellipse([730+k*36-26, 1040-k*40, 730+k*36+26, 1092-k*40], outline=(120, 122, 132), width=6)
    d.rounded_rectangle([BW/2-330, TOP+60, BW/2+330, TOP+240], 26, fill=RED)
    ctext(d, BW/2, TOP+96, "기존 질서", SER(100), PAPER)
    ctext(d, BW/2, TOP+300, "= 국가가 만든 나라", SAN(56), PAPER)
    return im

def b5():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([BW/2-360, TOP+60, BW/2+360, TOP+780], fill=PAPER)
    ctext(d, BW/2, TOP+120, "全民保險證", SER(88), INK)
    for k in range(5):
        w = 520-(k % 2)*140
        d.line([(BW/2-280, TOP+290+k*80), (BW/2-280+w, TOP+290+k*80)], fill=(150, 140, 124), width=8)
    st = seal_word("國民"); im.paste(st, (int(BW/2+80), TOP+500), st)
    return im

def b6():
    im = night(); d = ImageDraw.Draw(im)
    labs = [("국가개발", AMBER), ("시장", STEEL), ("유교", (110, 168, 92)), ("주권", RED)]
    for i, (lab, col) in enumerate(labs):
        r, c = divmod(i, 2)
        x0, y0 = 150+c*(BW//2-90), TOP+60+r*380
        d.line([(x0+60, y0), (x0+60, y0+250)], fill=(90, 94, 108), width=10)
        d.polygon([(x0+66, y0), (x0+380, y0+50), (x0+66, y0+120)], fill=col)
        ctext(d, x0+120, y0+24, lab, SAN(54), INK if col in (AMBER, PAPER) else PAPER, anchor="la")
        ctext(d, x0+60, y0+270, "保守", SER(56), tuple(int(v*0.85) for v in PAPER))
    return im

def b7():
    im = night(); d = ImageDraw.Draw(im)
    d.line([(180, 1660), (BW-180, 1660)], fill=(90, 94, 108), width=6)
    for yr, x in [("1970", 260), ("1980", BW/2), ("1990", BW-260)]:
        big = yr == "1980"
        r = 22 if big else 14
        d.ellipse([x-r, 1660-r, x+r, 1660+r], fill=AMBER)
        ctext(d, x, 1700, yr, SAN(56 if big else 44), AMBER if big else PAPER)
    d.rounded_rectangle([BW/2-460, TOP+120, BW/2-40, TOP+300], 22,
                        fill=(28, 36, 48), outline=STEEL, width=6)
    ctext(d, BW/2-250, TOP+150, "시장자유파", SAN(54), PAPER)
    d.rounded_rectangle([BW/2+40, TOP+430, BW/2+460, TOP+610], 22,
                        fill=(30, 44, 38), outline=(110, 168, 92), width=6)
    ctext(d, BW/2+250, TOP+460, "진보 연합", SAN(54), PAPER)
    pts = [(BW/2-240, TOP+310), (BW/2-140, TOP+400), (BW/2+60, TOP+470)]
    d.line(pts, fill=AMBER, width=10, joint="curve")
    d.polygon([(BW/2+60, TOP+470), (BW/2-10, TOP+470), (BW/2+40, TOP+412)], fill=AMBER)
    ctext(d, BW/2, TOP+700, "1980년대의 자리", SER(96), PAPER, 6, INK)
    return im

def person(d, px, gy, h, col, old=False):
    top = gy-h
    d.ellipse([px-40, top, px+40, top+84], fill=(230, 205, 180))
    if old:
        d.pieslice([px-44, top-6, px+44, top+56], 180, 360, fill=(200, 200, 205))
        d.line([(px+56, top+150), (px+80, gy)], fill=(120, 110, 96), width=12)   # 지팡이
    else:
        d.pieslice([px-44, top-8, px+44, top+60], 180, 360, fill=(40, 34, 30))
        d.rounded_rectangle([px+42, top+120, px+86, top+300], 16, fill=(70, 90, 110))  # 백팩
    d.rounded_rectangle([px-62, top+78, px+62, gy], 34, fill=col)

def b8():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([BW/2-220, 1050, BW/2+220, 1560], fill=(20, 24, 36))            # 공장 배경
    d.rectangle([BW/2-60, 950, BW/2, 1050], fill=(34, 38, 52))
    d.rectangle([0, 1560, BW, 2200], fill=(16, 19, 28))
    person(d, 300, 1560, 420, (60, 62, 72), old=True)
    person(d, BW-300, 1560, 400, (46, 66, 92), old=False)
    for px, ty, name in ((300, 1740, "천젠궈 (63) · 국영기업 퇴직"),
                         (BW-300, 1820, "린샤오 (24) · 창업가")):
        f = SAN(36)
        tw = d.textbbox((0, 0), name, font=f)[2]
        px = min(max(px, tw/2+90), BW-tw/2-90)
        d.rounded_rectangle([px-tw/2-18, ty, px+tw/2+18, ty+66], 12, fill=INK)
        d.text((px-tw/2, ty+12), name, font=f, fill=PAPER)
    d.rounded_rectangle([120, TOP+40, BW/2+30, TOP+220], 28, fill=PAPER)
    ctext(d, (120+BW/2+30)/2, TOP+66, "\"부모 세대가 만든 산업\"", SAN(44), INK)
    d.polygon([(340, TOP+214), (420, TOP+214), (360, TOP+300)], fill=PAPER)
    d.rounded_rectangle([BW/2-30, TOP+340, BW-120, TOP+520], 28, fill=PAPER)
    ctext(d, (BW/2-30+BW-120)/2, TOP+366, "\"낡은 기득권이죠\"", SAN(44), INK)
    d.polygon([(BW-340, TOP+514), (BW-260, TOP+514), (BW-300, TOP+600)], fill=PAPER)
    return im

def b9():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+80, "보수가 이상한 게", SER(120), PAPER)
    ctext(d, BW/2, TOP+270, "아니라", SER(120), PAPER)
    ctext(d, BW/2, TOP+560, "'기존 질서'가", SER(130), (255, 228, 0))
    ctext(d, BW/2, TOP+760, "달랐다", SER(150), (255, 228, 0))
    return im

def b10():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+120, "그럼, 진보는", SER(140), PAPER)
    ctext(d, BW/2, TOP+340, "누구인가", SER(140), PAPER)
    redbar(d, TOP+700, "당신의 분류를 남겨주세요")
    ctext(d, BW/2, BH-200, "EP3. 자유중국의 진보는 누구인가", SAN(44),
          tuple(int(c*0.85) for c in PAPER))
    return im

VOJ = json.load(open(f"{ROOT}/vo/lines.json"))
GAP = 0.12
SC = []; t0 = 0.0
for p in VOJ:
    secs = p["dur"]+GAP+(1.0 if p["id"] == "s10" else 0)
    SC.append({"id": p["id"], "secs": secs, "t0": t0,
               "chips": UI.chunks_for(p["text"], p["dur"]+0.15)})
    t0 += secs
print(f"audio {mix_audio([(s['id'], s['secs']) for s in SC], f'{ROOT}/vo', f'{ROOT}/mix.wav', lead=0.15):.2f}s")

BULD = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10]
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep2.mp4", seed0=1000, trans=0.20)
print("frames", n, "rc", rc)
