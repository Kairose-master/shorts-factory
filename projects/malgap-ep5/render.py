"""「말값」 No.5 국룰 — 당몰이(구조 서술→증언 유발) + Schelling(1960) 조정."""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw

def tag(d, fg=PAPER): d.text((84, 120), "「말값」 No.5", font=SAN(44), fill=fg)

def person(d, px, gy, h=320, cup=True, col=(9, 11, 17)):
    top = gy-h
    d.ellipse([px-34, top, px+34, top+72], fill=col)
    d.rounded_rectangle([px-52, top+62, px+52, gy], 30, fill=col)
    if cup:
        d.rectangle([px+44, top+150, px+86, top+220], fill=PAPER, outline=(150, 148, 140))
        d.line([(px+44, top+168), (px+86, top+168)], fill=(150, 148, 140), width=4)

def b1():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 900, 470, (86, 60, 22)); d = ImageDraw.Draw(im)
    d.line([(BW/2-200, 420), (BW/2-160, 640)], fill=(80, 82, 90), width=7)
    d.line([(BW/2+200, 420), (BW/2+160, 640)], fill=(80, 82, 90), width=7)
    d.rectangle([BW/2-430, 640, BW/2+430, 1180], fill=WOOD, outline=(28, 22, 18), width=10)
    d.rectangle([BW/2-404, 666, BW/2+404, 1154], outline=(122, 96, 60), width=5)
    ctext(d, BW/2, 700, "메뉴", SAN(54), tuple(int(c*0.8) for c in PAPER))
    ctext(d, BW/2, 800, "아메리카노 · 라떼 · 에이드", SER(64), PAPER)
    d.line([(BW/2-330, 940), (BW/2+330, 940)], fill=(122, 96, 60), width=4)
    d.rounded_rectangle([BW/2-260, 990, BW/2+260, 1110], 26, fill=RED)
    ctext(d, BW/2, 1012, "1인 1메뉴", SAN(64), PAPER)
    ctext(d, BW/2, 1420, "메뉴판에 없는 규칙", SER(96), PAPER, 6, INK)
    tag(d); return im

def b2():
    im = Image.new("RGB", (BW, BH), PAPER); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 660, "국", SER(430), INK)
    ctext(d, BW/2, 1150, "룰", SER(430), INK)
    d.line([(BW/2-330, 1700), (BW/2+330, 1686)], fill=INK, width=16)
    s = seal_word()
    im.paste(s, (int(BW/2+275-s.width/2), int(560-s.height/2)), s)
    tag(d, INK); return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1100, 520, (52, 48, 32)); d = ImageDraw.Draw(im)
    d.rectangle([0, 1620, BW, 2200], fill=(20, 23, 34))
    for i in range(5):
        person(d, 180+i*(BW-360)/4, 1620, h=310+((i*37) % 40))
    ctext(d, BW/2, 300, "누가 정했는지", SER(110), PAPER, 7, INK)
    ctext(d, BW/2, 470, "아무도 모른다 — 그런데 다들 지킨다", SAN(54), PAPER)
    tag(d); return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    cx, cy = BW/2, 1080
    for k in range(8):                                                        # 수렴 화살표
        a = math.tau*k/8
        x0, y0 = cx+math.cos(a)*430, cy+math.sin(a)*430
        x1, y1 = cx+math.cos(a)*150, cy+math.sin(a)*150
        d.line([(x0, y0), (x1, y1)], fill=STEEL, width=10)
        ha = a+math.pi
        for s in (-0.42, 0.42):
            d.line([(x1, y1), (x1+math.cos(ha+s)*54, y1+math.sin(ha+s)*54)], fill=STEEL, width=10)
    d.ellipse([cx-64, cy-64, cx+64, cy+64], fill=AMBER, outline=(120, 84, 20), width=6)
    ctext(d, BW/2, 300, "규칙 = 눈치의 절약", SER(100), PAPER, 7, INK)
    ctext(d, BW/2, BH-330, "조정과 포컬 포인트 · Schelling (1960)", SAN(42), PAPER)
    tag(d); return im

def b5():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1100, 500, (52, 46, 32)); d = ImageDraw.Draw(im)
    d.rectangle([0, 1620, BW, 2200], fill=(20, 23, 34))
    xs = [180+i*(BW-360)/4 for i in range(5)]
    for i, px in enumerate(xs):
        person(d, px, 1620, h=310+((i*37) % 40), cup=(i != 2))
    tx = xs[2]
    for i, px in enumerate(xs):                                               # 시선 점선
        if i == 2: continue
        steps = 9
        for q in range(steps):
            t0, t1 = q/steps, (q+0.55)/steps
            d.line([(px+(tx-px)*t0, 1240+(60*abs(i-2))*t0),
                    (px+(tx-px)*t1, 1240+(60*abs(i-2))*t1)], fill=RED, width=5)
    ctext(d, BW/2, 300, "어기는 순간", SER(120), PAPER, 7, INK)
    ctext(d, BW/2, 480, "눈치라는 값을 낸다", SAN(58), PAPER)
    tag(d); return im

def b6():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 480, "말값", SER(280), PAPER)
    ctext(d, BW/2, 880, "=", SER(150), PAPER)
    ctext(d, BW/2, 1060, "국룰", SER(170), PAPER)
    ctext(d, BW/2, 1300, "−  당신의 사정", SER(120), PAPER)
    redbar(d, 1560, "당신의 국룰을 남겨주세요")
    s = seal_empty(); im.paste(s, (BW-360, BH-480), s)
    ctext(d, BW/2, BH-260, "경험담이 이 편의 빈칸이다", SAN(42), PAPER)
    tag(d); return im

def anim_dot(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 11+2.6*math.sin(t*3.1)
    d.ellipse([W/2-r, 250-r, W/2+r, 250+r], outline=PAPER, width=5)
    return im

VO = {p["id"]: p["dur"] for p in json.load(open(f"{ROOT}/vo/lines.json"))}
GAP = 0.5
SECS = {k: VO[k]+GAP for k in VO}; SECS["s6"] = VO["s6"]+1.3
SC_A = [(k, SECS[k]) for k in ["s1", "s2", "s3", "s4", "s5", "s6"]]
print(f"audio {mix_audio(SC_A, f'{ROOT}/vo', f'{ROOT}/mix.wav'):.2f}s")
SCENES = [
 (b1, SECS["s1"], (1.07, 1.00, 0, -25), None),
 (b2, SECS["s2"], (1.00, 1.05, 0, 0), None),
 (b3, SECS["s3"], (1.08, 1.00, 0, 20), None),
 (b4, SECS["s4"], (1.00, 1.06, 0, 0), None),
 (b5, SECS["s5"], (1.07, 1.00, 0, 15), None),
 (b6, SECS["s6"], (1.00, 1.04, 0, 0), anim_dot),
]
n, rc = encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/malgap_no5.mp4", seed0=700)
print("frames", n, "rc", rc)
