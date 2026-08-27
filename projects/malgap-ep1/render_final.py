"""「말값」 No.1 시그니처 — 최종판. 간격 0.5s, 전 씬 발화 연결, Kruger 계보 선언 바."""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw

CUP = (210, 214, 222); YOG = (238, 234, 224)
BERRY = (196, 62, 74); CHOCO = (86, 62, 44)

def cup(d, cx, cy, s, with_spoon=True):
    top, bot, h = s*0.46, s*0.34, s*0.52
    d.polygon([(cx-top, cy-h), (cx+top, cy-h), (cx+bot, cy+h), (cx-bot, cy+h)],
              fill=(46, 52, 68), outline=CUP)
    d.polygon([(cx-top*0.55, cy-h), (cx-top*0.30, cy-h), (cx-bot*0.36, cy+h), (cx-bot*0.58, cy+h)],
              fill=(72, 80, 98))
    d.line([(cx-top, cy-h), (cx+top, cy-h)], fill=CUP, width=6)
    for k in range(4):
        rw = s*(0.40-k*0.085); ry = cy-h-s*0.10-k*s*0.135
        d.ellipse([cx-rw, ry-s*0.09, cx+rw, ry+s*0.09], fill=YOG,
                  outline=tuple(int(c*0.82) for c in YOG))
    d.polygon([(cx-s*0.04, cy-h-s*0.62), (cx+s*0.10, cy-h-s*0.74), (cx+s*0.07, cy-h-s*0.56)], fill=YOG)
    ty = cy-h-s*0.16
    for ddx in (-0.16, -0.06, -0.11):
        d.ellipse([cx+s*ddx-s*0.05, ty-s*0.05, cx+s*ddx+s*0.05, ty+s*0.05], fill=BERRY)
    for ddx in (0.10, 0.20):
        m = s*0.055
        d.polygon([(cx+s*ddx, ty-m), (cx+s*ddx+m, ty), (cx+s*ddx, ty+m), (cx+s*ddx-m, ty)], fill=AMBER)
    for ddx in (0.01, 0.30):
        d.ellipse([cx+s*ddx-s*0.04, ty-s*0.14, cx+s*ddx+s*0.04, ty-s*0.06], fill=CHOCO)
    if with_spoon:
        d.line([(cx+top*0.7, cy-h-s*0.5), (cx+top*1.25, cy-h-s*1.0)], fill=PAPER, width=int(s*0.05))
        d.ellipse([cx+top*0.5, cy-h-s*0.62, cx+top*0.9, cy-h-s*0.38], fill=PAPER)

def tag(d, fg=PAPER): d.text((84, 120), "「말값」 No.1", font=SAN(44), fill=fg)

def b1():
    im = night(); d = ImageDraw.Draw(im)
    d.polygon([(BW/2-90, 0), (BW/2+90, 0), (BW/2+430, 1660), (BW/2-430, 1660)], fill=(30, 32, 40))
    im = im.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(6))
    im = glow(im, BW/2, 1500, 470, (56, 46, 30)); d = ImageDraw.Draw(im)
    d.line([(90, 1665), (BW-90, 1665)], fill=(52, 56, 74), width=5)
    d.ellipse([BW/2-300, 1640, BW/2+300, 1698], fill=(10, 12, 20))
    cup(d, BW/2, 1420, 420)
    ctext(d, BW/2, 300, "30,000", SER(260), PAPER, 9, INK)
    ctext(d, BW/2, 620, "요거트 한 컵", SAN(58), PAPER)
    tag(d); return im

def b2():
    im = night()
    im = glow(im, BW/2, 1150, 560, (58, 48, 32)); d = ImageDraw.Draw(im)
    d.ellipse([BW/2-380, 1730, BW/2+380, 1800], fill=(10, 12, 20))
    cup(d, BW/2, 1250, 760)
    ctext(d, BW/2, 1880, "토핑 세 개", SER(110), PAPER, 7, INK)
    tag(d); return im

def b3():
    im = Image.new("RGB", (BW, BH), PAPER); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 700, "시그", SER(360), INK)
    ctext(d, BW/2, 1150, "니처", SER(360), INK)
    d.line([(BW/2-330, 1660), (BW/2+330, 1646)], fill=INK, width=16)
    s = seal_word()
    im.paste(s, (int(BW/2+265-s.width/2), int(580-s.height/2)), s)
    ctext(d, BW/2, BH-300, "이름이 붙는 순간", SAN(46), INK)
    tag(d, INK); return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 900, 470, (86, 60, 22)); d = ImageDraw.Draw(im)
    d.line([(BW/2-200, 420), (BW/2-160, 640)], fill=(80, 82, 90), width=7)
    d.line([(BW/2+200, 420), (BW/2+160, 640)], fill=(80, 82, 90), width=7)
    d.rectangle([BW/2-430, 640, BW/2+430, 1240], fill=WOOD, outline=(28, 22, 18), width=10)
    d.rectangle([BW/2-404, 666, BW/2+404, 1214], outline=(122, 96, 60), width=5)
    ctext(d, BW/2, 700, "메뉴", SAN(54), tuple(int(c*0.8) for c in PAPER))
    ctext(d, BW/2, 800, "시그니처 요거트", SER(88), AMBER)
    ctext(d, BW/2, 910, "30,000원", SER(96), AMBER)
    d.line([(BW/2-330, 1052), (BW/2+330, 1052)], fill=(122, 96, 60), width=4)
    ctext(d, BW/2, 1075, "요거트", SER(80), PAPER)
    ctext(d, BW/2, 1175, "____원", SER(72), tuple(int(c*0.85) for c in PAPER))
    ctext(d, BW/2, BH-330, "차별화 · Chamberlin (1933)", SAN(42), PAPER)
    tag(d); return im

def b5():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1050, 500, (52, 44, 30)); d = ImageDraw.Draw(im)
    cx, gy = BW/2, 1660
    d.rectangle([cx-190, gy, cx+190, gy+34], fill=(52, 56, 74))
    d.line([(cx, gy), (cx, 760)], fill=(150, 152, 160), width=14)
    bx0, by0 = cx-420, 760-67; bx1, by1 = cx+420, 760+67
    d.line([(bx0, by0), (bx1, by1)], fill=(170, 172, 180), width=13)
    d.ellipse([cx-16, 744, cx+16, 776], fill=(170, 172, 180))
    for px, py, side in ((bx0, by0, "L"), (bx1, by1, "R")):
        for off in (-120, 0, 120):
            d.line([(px, py), (px+off, py+150)], fill=(120, 122, 130), width=4)
        d.ellipse([px-160, py+140, px+160, py+205], fill=(60, 64, 80),
                  outline=(150, 152, 160), width=5)
        if side == "L": cup(d, px, py+40, 175, with_spoon=False)
        else:
            d.rounded_rectangle([px-150, py+30, px+150, py+140], 18, fill=PAPER)
            ctext(d, px, py+48, "시그니처", SER(58), INK)
    ctext(d, BW/2, 1840, "“얼추 재료비 5,000원…” — 제로비의 추정, 검증 전", SAN(44), PAPER)
    tag(d); return im

def b6():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 480, "말값", SER(280), PAPER)
    ctext(d, BW/2, 880, "=", SER(150), PAPER)
    ctext(d, BW/2, 1080, "30,000원", SER(160), PAPER)
    ctext(d, BW/2, 1300, "−  ____원", SER(140), PAPER)
    d.line([(BW/2+40, 1495), (BW/2+320, 1495)], fill=RED, width=14)
    redbar(d, 1640, "빈칸은 당신이 채우세요")
    s = seal_empty()
    im.paste(s, (BW-360, BH-480), s)
    ctext(d, BW/2, BH-260, "차별화된 이름은 가격을 스스로 정한다 · Chamberlin (1933)", SAN(38), PAPER)
    tag(d); return im

def anim_motes(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    rng = np.random.default_rng(7)
    for k in range(10):
        x0 = W/2 + rng.uniform(-180, 180)
        y = (1500 - (t*46 + k*137) % 1200)
        d.ellipse([x0-3, y-3, x0+3, y+3], fill=(242, 233, 220, 60))
    return im
def anim_glint(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    for k, (gx, gy) in enumerate([(W/2-70, 640), (W/2+95, 600), (W/2+10, 520)]):
        a = int(90*max(0, math.sin(t*2.4+k*2.1)))
        d.line([(gx-14, gy), (gx+14, gy)], fill=(255, 255, 255, a), width=3)
        d.line([(gx, gy-14), (gx, gy+14)], fill=(255, 255, 255, a), width=3)
    return im
def anim_dot(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 11+2.6*math.sin(t*3.1)
    d.ellipse([W/2-r, 250-r, W/2+r, 250+r], outline=PAPER, width=5)
    return im

VO = {p["id"]: p["dur"] for p in json.load(open(f"{ROOT}/vo-final/lines.json"))}
GAP = 0.5
SECS = {k: VO[k]+GAP for k in VO}; SECS["s6"] = VO["s6"]+1.3
SC_A = [("s1", SECS["s1"]), ("s2", SECS["s2"]), ("s3", SECS["s3"]),
        ("s4", SECS["s4"]), ("s5", SECS["s5"]), ("s6", SECS["s6"])]
total = mix_audio(SC_A, f"{ROOT}/vo-final", f"{ROOT}/mix-final.wav")
print(f"audio {total:.2f}s")
SCENES = [
 (b1, SECS["s1"], (1.08, 1.00, 0, -35), anim_motes),
 (b2, SECS["s2"], (1.10, 1.00, 0, 25), anim_glint),
 (b3, SECS["s3"], (1.00, 1.05, 0, 0), None),
 (b4, SECS["s4"], (1.06, 1.00, 0, -20), None),
 (b5, SECS["s5"], (1.07, 1.00, 0, 0), None),
 (b6, SECS["s6"], (1.00, 1.03, 0, 0), anim_dot),
]
n, rc = encode(SCENES, f"{ROOT}/mix-final.wav", f"{ROOT}/malgap_no1.mp4", seed0=100)
print("frames", n, "rc", rc)
