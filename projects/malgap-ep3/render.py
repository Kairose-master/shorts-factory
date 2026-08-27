"""「말값」 No.3 프리미엄 — 달빛부부(완벽→균열) + 내손내싼(지연 명명) + Veblen (1899)."""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw

def tag(d, fg=PAPER): d.text((84, 120), "「말값」 No.3", font=SAN(44), fill=fg)

def box(d, cx, cy, s, ribbon=True):
    d.rectangle([cx-s, cy-s*0.72, cx+s, cy+s*0.72], fill=(46, 52, 68), outline=(150, 152, 160), width=6)
    d.rectangle([cx-s, cy-s*0.72, cx+s, cy-s*0.40], fill=(58, 66, 84), outline=(150, 152, 160), width=6)
    if ribbon:
        d.rectangle([cx-s*0.14, cy-s*0.72, cx+s*0.14, cy+s*0.72], fill=(90, 100, 120))

def tag_price(d, cx, y, txt, accent=False):
    f = SAN(52); tw = d.textbbox((0, 0), txt, font=f)[2]
    d.line([(cx, y-70), (cx+46, y)], fill=(150, 152, 160), width=5)
    d.rounded_rectangle([cx-30, y, cx+tw+70, y+96], 14, fill=PAPER)
    d.ellipse([cx-12, y+38, cx+8, y+58], fill=INK)
    d.text((cx+24, y+16), txt, font=f, fill=RED if accent else INK)

def b1():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1000, 470, (40, 40, 34)); d = ImageDraw.Draw(im)
    for i, t in enumerate(["더 무겁고,", "더 어둡고,", "더 조용한"]):
        y = 620 + i*330
        d.rounded_rectangle([BW/2-330+i*40, y, BW/2+330+i*40, y+200], 24,
                            fill=(28, 31, 42), outline=(90, 96, 112), width=5)
        ctext(d, BW/2+i*40, y+48, t, SER(88), PAPER)
    ctext(d, BW/2, 1750, "단어가 있습니다", SAN(60), PAPER)
    tag(d); return im

def b2():
    im = Image.new("RGB", (BW, BH), PAPER); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 700, "프리", SER(340), INK)
    ctext(d, BW/2, 1130, "미엄", SER(340), INK)
    d.line([(BW/2-330, 1620), (BW/2+330, 1606)], fill=INK, width=16)
    s = seal_word()
    im.paste(s, (int(BW/2+265-s.width/2), int(560-s.height/2)), s)
    tag(d, INK); return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1050, 500, (48, 46, 34)); d = ImageDraw.Draw(im)
    d.line([(100, 1420), (BW-100, 1420)], fill=(52, 56, 74), width=5)
    box(d, BW/2-250, 1200, 210); box(d, BW/2+250, 1200, 210)
    ctext(d, BW/2, 350, "같은 상자", SER(130), PAPER, 7, INK)
    ctext(d, BW/2, 540, "같은 공장 · 같은 원단", SAN(54), PAPER)
    tag(d); return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1050, 500, (48, 46, 34)); d = ImageDraw.Draw(im)
    d.line([(100, 1420), (BW-100, 1420)], fill=(52, 56, 74), width=5)
    box(d, BW/2-250, 1200, 210); box(d, BW/2+250, 1200, 210)
    tag_price(d, BW/2-330, 760, "____원")
    tag_price(d, BW/2+60, 700, "____원 ×2", accent=True)
    ctext(d, BW/2, 300, "다른 건 가격표뿐", SER(110), PAPER, 7, INK)
    tag(d); return im

def b5():
    im = night(); d = ImageDraw.Draw(im)
    ox, oy = 240, 1560
    d.line([(ox, oy), (ox, 520)], fill=(150, 152, 160), width=8)          # y: 판매량
    d.line([(ox, oy), (BW-160, oy)], fill=(150, 152, 160), width=8)       # x: 가격
    ctext(d, BW-230, oy+40, "가격 →", SAN(44), PAPER, anchor="ma")
    d.text((ox-60, 470), "판매량", font=SAN(44), fill=PAPER)
    pts = [(ox+80+i*(BW-480)/9, oy-120-(i**1.6)*34) for i in range(10)]   # 우상향
    d.line(pts, fill=AMBER, width=12, joint="curve")
    d.ellipse([pts[-1][0]-46, pts[-1][1]-46, pts[-1][0]+46, pts[-1][1]+46],
              fill=AMBER, outline=(120, 84, 20), width=6)
    ctext(d, pts[-1][0], pts[-1][1]-36, "$", SAN(52), (60, 42, 10))
    ctext(d, BW/2, 280, "비쌀수록 팔린다", SER(110), PAPER, 7, INK)
    ctext(d, BW/2, BH-330, "베블런 효과 · Veblen (1899) 유한계급론", SAN(42), PAPER)
    tag(d); return im

def b6():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 480, "말값", SER(280), PAPER)
    ctext(d, BW/2, 880, "=", SER(150), PAPER)
    ctext(d, BW/2, 1080, "____원", SER(170), PAPER)
    ctext(d, BW/2, 1320, "−  ____원", SER(150), PAPER)
    d.line([(BW/2-260, 1275), (BW/2+20, 1275)], fill=RED, width=14)
    d.line([(BW/2+60, 1515), (BW/2+340, 1515)], fill=RED, width=14)
    redbar(d, 1660, "빈칸은 당신이 채우세요")
    s = seal_empty(); im.paste(s, (BW-360, BH-480), s)
    ctext(d, BW/2, BH-260, "이번 편은 가격마저 빈칸이다 — 그것이 프리미엄", SAN(40), PAPER)
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
 (b1, SECS["s1"], (1.06, 1.00, 0, -25), None),
 (b2, SECS["s2"], (1.00, 1.05, 0, 0), None),
 (b3, SECS["s3"], (1.08, 1.00, 0, 0), None),
 (b4, SECS["s4"], (1.00, 1.06, 0, -15), None),
 (b5, SECS["s5"], (1.07, 1.00, 0, 15), None),
 (b6, SECS["s6"], (1.00, 1.04, 0, 0), anim_dot),
]
n, rc = encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/malgap_no3.mp4", seed0=500)
print("frames", n, "rc", rc)
