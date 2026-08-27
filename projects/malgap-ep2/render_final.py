"""「말값」 No.2 정통 — 최종판. 간격 0.5s, 논리 연결 내레이션, 선언 바."""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw

BROTH = (216, 212, 196)
def tag(d, fg=PAPER): d.text((84, 120), "「말값」 No.2", font=SAN(44), fill=fg)

def b1():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1450, 560, (60, 50, 34)); d = ImageDraw.Draw(im)
    d.line([(70, 1815), (BW-70, 1815)], fill=(52, 56, 74), width=4)
    cx, cy = BW/2, 1500
    d.ellipse([cx-430, cy+180, cx+430, cy+280], fill=(10, 12, 20))
    d.polygon([(cx-420, cy-60), (cx+420, cy-60), (cx+290, cy+220), (cx-290, cy+220)], fill=BRASS)
    d.polygon([(cx-420, cy-60), (cx+420, cy-60), (cx+405, cy-10), (cx-405, cy-10)],
              fill=tuple(int(c*1.22) for c in BRASS))
    d.ellipse([cx-150, cy+220, cx+150, cy+280], fill=tuple(int(c*0.7) for c in BRASS))
    d.ellipse([cx-400, cy-125, cx+400, cy+5], fill=tuple(int(c*0.55) for c in BRASS))
    d.ellipse([cx-372, cy-112, cx+372, cy-8], fill=BROTH)
    for k in range(5):
        rr = 210-k*38
        d.arc([cx-rr, cy-60-rr//3, cx+rr, cy-60+rr//3], 15+k*9, 330-k*12, fill=(74, 60, 48), width=13)
    d.ellipse([cx+120, cy-108, cx+260, cy-38], fill=PAPER)
    d.ellipse([cx+158, cy-90, cx+225, cy-56], fill=AMBER)
    for i in range(3):
        d.polygon([(cx-260+i*36, cy-104), (cx-236+i*36, cy-108), (cx-196+i*36, cy-56),
                   (cx-220+i*36, cy-52)], fill=STEEL)
    d.line([(cx-330, cy-260), (cx+150, cy-64)], fill=PAPER, width=11)
    d.line([(cx-330, cy-236), (cx+162, cy-78)], fill=tuple(int(c*0.8) for c in PAPER), width=11)
    ctext(d, BW/2, 320, "16,000", SER(280), PAPER, 10, INK)
    ctext(d, BW/2, 660, "냉면 한 그릇", SAN(58), PAPER)
    tag(d); return im

def b2():
    im = Image.new("RGB", (BW, BH), PAPER); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 760, "정", SER(430), INK)
    ctext(d, BW/2, 1250, "통", SER(430), INK)
    d.line([(BW/2-330, 1810), (BW/2+330, 1795)], fill=INK, width=16)
    s = seal_word()
    im.paste(s, (int(BW/2+275-s.width/2), int(640-s.height/2)), s)
    tag(d, INK); return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    for x0, x1, ht in [(0, 300, 620), (BW-270, BW, 540), (250, 430, 760), (BW-460, BW-250, 820)]:
        d.rectangle([x0, ht, x1, 1980], fill=(12, 15, 23))
        rng = np.random.default_rng(x0)
        for _ in range(4):
            wx = int(rng.uniform(x0+24, x1-52)); wy = int(rng.uniform(ht+60, 1700))
            d.rectangle([wx, wy, wx+30, wy+42], fill=(120, 90, 40))
    im = glow(im, BW/2, 880, 430, (95, 66, 22)); d = ImageDraw.Draw(im)
    d.line([(BW/2-190, 480), (BW/2-150, 700)], fill=(80, 82, 90), width=7)
    d.line([(BW/2+190, 480), (BW/2+150, 700)], fill=(80, 82, 90), width=7)
    d.rectangle([BW/2-320, 700, BW/2+320, 1060], fill=WOOD, outline=(28, 22, 18), width=10)
    d.rectangle([BW/2-296, 724, BW/2+296, 1036], outline=(122, 96, 60), width=5)
    ctext(d, BW/2, 770, "원조 평양옥", SER(120), AMBER)
    ctext(d, BW/2, 930, "since 19__", SAN(64), tuple(int(c*0.85) for c in PAPER))
    ctext(d, BW/2, BH-330, "1단계 — 간판은 신호다 · Spence (1973)", SAN(42), PAPER)
    tag(d); return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([0, 1740, BW, 2200], fill=(20, 23, 34))
    lx = BW-240
    d.line([(lx, 420), (lx, 1760)], fill=(60, 63, 74), width=16)
    d.line([(lx, 420), (lx-140, 470)], fill=(60, 63, 74), width=12)
    d.ellipse([lx-190, 440, lx-110, 510], fill=AMBER)
    im = glow(im, lx-150, 480, 330, (110, 76, 24)); d = ImageDraw.Draw(im)
    door_x = 130
    d.rectangle([door_x-70, 1150, door_x+90, 1760], fill=(30, 26, 20))
    d.rectangle([door_x-40, 1210, door_x+60, 1760], fill=(180, 130, 50))
    hs = [(920, 1.0), (790, .96), (665, 1.03), (545, .94), (430, 1.0), (325, .97), (230, .92)]
    for i, (px, sc) in enumerate(hs):
        hh = int(300*sc); top = 1760-hh
        d.ellipse([px-34, top, px+34, top+72], fill=(9, 11, 17))
        d.rounded_rectangle([px-52, top+62, px+52, 1760], 30, fill=(9, 11, 17))
        d.polygon([(px-46, 1760), (px+46, 1760), (px+150+i*8, 1855), (px+30+i*8, 1855)],
                  fill=(14, 16, 24))
        d.line([(px-52, top+95), (px+52, top+95)], fill=(190, 140, 60), width=4)
    ctext(d, BW/2, BH-330, "2단계 — 맛은 먹기 전에 모른다 · Akerlof (1970)", SAN(42), PAPER)
    tag(d); return im

def b5():
    im = night(); d = ImageDraw.Draw(im)
    cx, cy, R = BW/2, 1100, 470
    d.ellipse([cx-R-60, cy-R-60, cx+R+60, cy+R+60], fill=(24, 27, 40))
    d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=BRASS)
    d.ellipse([cx-R+42, cy-R+42, cx+R-42, cy+R-42], fill=tuple(int(c*0.62) for c in BRASS))
    d.ellipse([cx-R+58, cy-R+58, cx+R-58, cy+R-58], fill=(226, 223, 210))
    for k in range(3):
        rr = 120-k*34
        d.arc([cx-rr, cy-rr, cx+rr, cy+rr], 30+k*40, 260+k*30, fill=(150, 138, 118), width=9)
    d.polygon([(cx-180, cy-210), (cx-90, cy-260), (cx-60, cy-215), (cx-150, cy-170)],
              fill=(238, 240, 240))
    d.polygon([(cx+120, cy+150), (cx+205, cy+120), (cx+230, cy+185), (cx+150, cy+210)],
              fill=(232, 236, 238))
    d.line([(cx+220, cy-420), (cx+470, cy+150)], fill=PAPER, width=12)
    ctext(d, BW/2, 1720, "“걸레 빤 물”", SER(120), PAPER, 8, INK)
    ctext(d, BW/2, 1885, "— 실제로 붙은 비판", SAN(52), tuple(int(c*0.9) for c in PAPER))
    tag(d); return im

def b6():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 480, "말값", SER(280), PAPER)
    ctext(d, BW/2, 880, "=", SER(150), PAPER)
    ctext(d, BW/2, 1080, "16,000원", SER(160), PAPER)
    ctext(d, BW/2, 1300, "−  ____원", SER(140), PAPER)
    d.line([(BW/2+40, 1495), (BW/2+320, 1495)], fill=RED, width=14)
    redbar(d, 1640, "빈칸은 당신이 채우세요")
    s = seal_empty()
    im.paste(s, (BW-360, BH-480), s)
    ctext(d, BW/2, BH-260, "정보가 비대칭일 때 신호에 값이 붙는다 · Akerlof · Spence", SAN(38), PAPER)
    tag(d); return im

def anim_steam(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    for k in range(3):
        ph = t*1.4+k*2.1
        pts = [(W/2+(k-1)*120+math.sin(q/9*5+ph)*46*(1-q/9*0.4), 1120-q*52) for q in range(10)]
        d.line(pts, fill=(242, 233, 220, 46), width=16, joint="curve")
    return im
def anim_ripple(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 90+(t*118) % 260
    a = max(0, int(70*(1-r/350)))
    d.ellipse([W/2-r, 930-r*0.94, W/2+r, 930+r*0.94], outline=(255, 255, 255, a), width=4)
    return im
def anim_dot(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 11+2.6*math.sin(t*3.1)
    d.ellipse([W/2-r, 250-r, W/2+r, 250+r], outline=PAPER, width=5)
    return im

VO = {p["id"]: p["dur"] for p in json.load(open(f"{ROOT}/vo-final/lines.json"))}
GAP = 0.5
SECS = {k: VO[k]+GAP for k in VO}; SECS["s6"] = VO["s6"]+1.3
SC_A = [(k, SECS[k]) for k in ["s1", "s2", "s3", "s4", "s5", "s6"]]
total = mix_audio(SC_A, f"{ROOT}/vo-final", f"{ROOT}/mix-final.wav")
print(f"audio {total:.2f}s")
SCENES = [
 (b1, SECS["s1"], (1.08, 1.00, 0, -35), anim_steam),
 (b2, SECS["s2"], (1.00, 1.05, 0, 0), None),
 (b3, SECS["s3"], (1.07, 1.00, 25, 0), None),
 (b4, SECS["s4"], (1.00, 1.06, -30, 0), None),
 (b5, SECS["s5"], (1.10, 1.00, 0, 25), anim_ripple),
 (b6, SECS["s6"], (1.00, 1.03, 0, 0), anim_dot),
]
n, rc = encode(SCENES, f"{ROOT}/mix-final.wav", f"{ROOT}/malgap_no2.mp4", seed0=200)
print("frames", n, "rc", rc)
