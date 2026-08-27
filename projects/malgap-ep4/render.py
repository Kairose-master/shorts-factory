"""「말값」 No.4 큐레이션 — 책트폭행(선언형) + Stigler(1961) 탐색비용 + 제로비 10^57 인용."""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw
import numpy as _np

TOPC = [(196, 62, 74), (232, 163, 61), (86, 62, 44), (91, 124, 153), (238, 234, 224)]
def tag(d, fg=PAPER): d.text((84, 120), "「말값」 No.4", font=SAN(44), fill=fg)

def b1():
    im = night(); d = ImageDraw.Draw(im)
    rng = _np.random.default_rng(11)
    for _ in range(240):                                                     # 토핑의 바다
        x, y = rng.uniform(80, BW-80), rng.uniform(900, 2050)
        r = rng.uniform(9, 26)
        c = TOPC[int(rng.integers(0, 5))]
        d.ellipse([x-r, y-r, x+r, y+r], fill=tuple(int(v*0.75) for v in c))
    ctext(d, BW/2-90, 300, "10", SER(260), PAPER, 9, INK)
    ctext(d, BW/2+210, 300, "57", SER(130), AMBER, 6, INK)
    ctext(d, BW/2, 660, "토핑 조합의 경우의 수", SAN(56), PAPER)
    ctext(d, BW/2, 760, "— 제로비 실측 인용", SAN(42), tuple(int(c*0.85) for c in PAPER))
    tag(d); return im

def b2():
    im = Image.new("RGB", (BW, BH), PAPER); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 700, "큐레", SER(340), INK)
    ctext(d, BW/2, 1130, "이션", SER(340), INK)
    d.line([(BW/2-330, 1620), (BW/2+330, 1606)], fill=INK, width=16)
    s = seal_word()
    im.paste(s, (int(BW/2+265-s.width/2), int(560-s.height/2)), s)
    tag(d, INK); return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 800, 430, (48, 46, 32)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([BW/2-360, 660, BW/2+360, 960], 40, fill=(46, 52, 68),
                        outline=(150, 152, 160), width=7)                     # 쟁반
    for i, c in enumerate(TOPC[:3]):                                          # 선택된 셋
        x = BW/2-160+i*160
        d.ellipse([x-52, 760, x+52, 864], fill=c)
    rng = _np.random.default_rng(5)
    for _ in range(120):                                                      # 남은 무리
        x, y = rng.uniform(120, BW-120), rng.uniform(1350, 2000)
        r = rng.uniform(9, 22)
        g = int(rng.uniform(40, 70))
        d.ellipse([x-r, y-r, x+r, y+r], fill=(g, g+4, g+12))
    d.line([(BW/2, 1000), (BW/2, 1300)], fill=AMBER, width=8)                 # 픽업 선
    d.polygon([(BW/2-26, 1300), (BW/2+26, 1300), (BW/2, 1240)], fill=AMBER)
    ctext(d, BW/2, 300, "골라주는 사람", SER(120), PAPER, 7, INK)
    tag(d); return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2-120, 950, 380, (50, 46, 32)); d = ImageDraw.Draw(im)
    d.ellipse([BW/2-380, 700, BW/2+60, 1140], outline=(150, 152, 160), width=16)  # 돋보기
    d.line([(BW/2+20, 1100), (BW/2+280, 1420)], fill=(150, 152, 160), width=26)
    d.ellipse([BW/2+130, 380, BW/2+470, 720], outline=AMBER, width=12)            # 시계
    d.line([(BW/2+300, 550), (BW/2+300, 440)], fill=AMBER, width=10)
    d.line([(BW/2+300, 550), (BW/2+380, 590)], fill=AMBER, width=10)
    ctext(d, BW/2, 1620, "고르는 수고 = 진짜 비용", SER(88), PAPER, 6, INK)
    ctext(d, BW/2, BH-330, "탐색 비용 · Stigler (1961) The Economics of Information", SAN(40), PAPER)
    tag(d); return im

def b5():
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([BW/2-340, 420, BW/2+340, 1720], fill=PAPER)                  # 영수증
    d.polygon([(BW/2-340, 1720)]+[(BW/2-340+i*68, 1760 if i % 2 else 1720) for i in range(1, 11)]
              +[(BW/2+340, 1720)], fill=PAPER)
    ctext(d, BW/2, 480, "영수증", SAN(52), INK)
    rows = [("요거트", "＿＿＿"), ("토핑 A", "＿＿＿"), ("토핑 B", "＿＿＿"), ("토핑 C", "＿＿＿")]
    y = 620
    for name, won in rows:
        d.text((BW/2-260, y), name, font=SAN(52), fill=INK)
        d.text((BW/2+260, y), won, font=SAN(52), fill=INK, anchor="ra")
        y += 120
    d.line([(BW/2-260, y+10), (BW/2+260, y+10)], fill=INK, width=5); y += 60
    d.text((BW/2-260, y), "큐레이션", font=SAN(58), fill=RED)
    d.text((BW/2+260, y), "____", font=SAN(58), fill=RED, anchor="ra")
    ctext(d, BW/2, BH-300, "그 값은 어느 영수증에도 없다", SAN(46), PAPER)
    tag(d); return im

def b6():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 480, "말값", SER(280), PAPER)
    ctext(d, BW/2, 880, "=", SER(150), PAPER)
    ctext(d, BW/2, 1060, "골라준 값", SER(150), PAPER)
    ctext(d, BW/2, 1290, "−  ____원", SER(140), PAPER)
    d.line([(BW/2+50, 1480), (BW/2+330, 1480)], fill=RED, width=14)
    redbar(d, 1640, "빈칸은 당신이 채우세요")
    s = seal_empty(); im.paste(s, (BW-360, BH-480), s)
    ctext(d, BW/2, BH-260, "이 단어엔 진짜 값이 있다 — 얼마인지 안 적을 뿐", SAN(40), PAPER)
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
 (b1, SECS["s1"], (1.08, 1.00, 0, -25), None),
 (b2, SECS["s2"], (1.00, 1.05, 0, 0), None),
 (b3, SECS["s3"], (1.07, 1.00, 0, 15), None),
 (b4, SECS["s4"], (1.00, 1.06, 0, 0), None),
 (b5, SECS["s5"], (1.07, 1.00, 0, -15), None),
 (b6, SECS["s6"], (1.00, 1.04, 0, 0), anim_dot),
]
n, rc = encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/malgap_no4.mp4", seed0=600)
print("frames", n, "rc", rc)
