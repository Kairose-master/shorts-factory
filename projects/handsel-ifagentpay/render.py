"""「if agent pay」— Handsel(Kairose-master/handsel) 실사실 기반 컨셉 필름.

근거(전부 README/RESEARCH.md): Base 메인넷 2026-07-30 · bounty:$5 라벨 루프 ·
"your own CI grades it" · "your two clicks" · F18(채점자 프롬프트 주입) ·
E0–E4, MIN_CLASS_FOR_MONEY='E3' · cold start score 0 ·
"Payment lets AI agents transact. Credit lets AI agents scale."
시각: Ledger Noir (noir_kit).
"""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw

GREEN = (110, 168, 92)
def tag(d, fg=PAPER): d.text((84, 120), "if agent pay", font=SAN(44), fill=fg)

def agent(d, cx, gy, h=340, col=(9, 11, 17), eye=PAPER, chest=None):
    top = gy - h
    d.line([(cx, top-46), (cx, top-6)], fill=col, width=8)                     # antenna
    d.ellipse([cx-10, top-64, cx+10, top-44], fill=AMBER)
    d.rounded_rectangle([cx-72, top, cx+72, top+120], 34, fill=col)            # head
    for s in (-1, 1):
        d.ellipse([cx+s*30-10, top+44, cx+s*30+10, top+64], fill=eye)
    d.rounded_rectangle([cx-88, top+132, cx+88, gy], 40, fill=col)             # body
    if chest:
        d.rounded_rectangle([cx-52, top+170, cx+52, top+240], 14, outline=AMBER, width=5)
        ctext(d, cx, top+180, chest, SAN(44), AMBER)

def coin(d, cx, cy, r=64):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=AMBER, outline=(120, 84, 20), width=6)
    d.ellipse([cx-r+16, cy-r+16, cx+r-16, cy+r-16], outline=(120, 84, 20), width=4)
    ctext(d, cx, cy-r*0.52, "$", SAN(int(r*1.05)), (60, 42, 10))

def b1():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1330, 420, (64, 50, 26)); d = ImageDraw.Draw(im)
    d.line([(90, 1720), (BW-90, 1720)], fill=(52, 56, 74), width=5)
    agent(d, BW/2-250, 1720); agent(d, BW/2+250, 1720, h=320)
    coin(d, BW/2, 1330)
    for s in (-1, 1):                                                          # 전달선
        d.line([(BW/2+s*150, 1370), (BW/2+s*76, 1345)], fill=AMBER, width=6)
    ctext(d, BW/2, 260, "2026. 7. 30.", SER(150), PAPER, 8, INK)
    ctext(d, BW/2, 460, "에이전트가 에이전트에게 지불한 날", SAN(54), PAPER)
    ctext(d, BW/2, BH-280, "Circle USDC · Base mainnet — 실거래", SAN(40), PAPER)
    tag(d); return im

def b2():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1050, 430, (58, 48, 28)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([BW/2-330, 720, BW/2+330, 1400], 44, fill=(30, 34, 46),
                        outline=(150, 152, 160), width=10)                      # 금고
    d.ellipse([BW/2-110, 950, BW/2+110, 1170], outline=(150, 152, 160), width=12)
    for k in range(8):
        a = math.tau*k/8
        d.line([(BW/2+math.cos(a)*110, 1060+math.sin(a)*110),
                (BW/2+math.cos(a)*150, 1060+math.sin(a)*150)], fill=(150, 152, 160), width=8)
    coin(d, BW/2, 1060, 66)
    d.rounded_rectangle([BW/2-190, 520, BW/2+190, 640], 26, fill=GREEN)         # 라벨 칩
    ctext(d, BW/2, 542, "bounty: $5", SAN(58), INK)
    ctext(d, BW/2, 1560, "돈이 먼저 잠깁니다", SER(96), PAPER, 6, INK)
    ctext(d, BW/2, BH-280, "에스크로 — 일 시작 전에 예치", SAN(40), PAPER)
    tag(d); return im

def b3():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2-120, 1050, 380, (48, 44, 30)); d = ImageDraw.Draw(im)
    d.line([(90, 1660), (BW-90, 1660)], fill=(52, 56, 74), width=5)
    agent(d, BW/2-230, 1660, h=360)
    d.rounded_rectangle([BW/2-40, 1080, BW/2+430, 1420], 22, fill=(26, 30, 42),
                        outline=(90, 96, 112), width=7)                          # 모니터
    for k in range(6):
        wln = 300 - (k % 3)*70
        d.line([(BW/2, 1130+k*46), (BW/2+wln, 1130+k*46)],
               fill=STEEL if k % 2 else (150, 138, 118), width=10)
    d.polygon([(BW/2+430, 900), (BW/2+430, 990), (BW/2+540, 945)], fill=GREEN)   # → PR
    ctext(d, BW/2+250, 800, "PR", SER(110), GREEN)
    ctext(d, BW/2, 240, "일은 AI가", SER(120), PAPER, 7, INK)
    tag(d); return im

def b4():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 900, 430, (52, 48, 30)); d = ImageDraw.Draw(im)
    agent(d, BW/2, 1560, h=420, chest="CI")
    d.rectangle([BW/2-260, 1620, BW/2+260, 1755], fill=PAPER)                    # 서류
    d.line([(BW/2-200, 1665), (BW/2+120, 1665)], fill=(140, 132, 118), width=7)
    d.line([(BW/2-200, 1710), (BW/2+40, 1710)], fill=(140, 132, 118), width=7)
    st = Image.new("RGBA", (330, 200), (0, 0, 0, 0))
    ImageDraw.Draw(st).rectangle([6, 6, 324, 194], outline=GREEN, width=12)
    ImageDraw.Draw(st).text((165, 92), "PASS", font=SAN(84), fill=GREEN, anchor="mm")
    st = st.rotate(-9, expand=True)
    im.paste(st, (int(BW/2+40), 1560), st)
    ctext(d, BW/2, 240, "채점은 CI가", SER(120), PAPER, 7, INK)
    ctext(d, BW/2, 420, "일한 쪽은 채점하지 못한다", SAN(54), PAPER)
    tag(d); return im

def b5():
    im = Image.new("RGB", (BW, BH), (26, 14, 14)); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1000, 430, (70, 26, 20)); d = ImageDraw.Draw(im)
    agent(d, BW/2+180, 1660, h=400, chest="CI")
    d.rounded_rectangle([120, 850, BW/2+30, 1080], 34, fill=PAPER)               # 속삭임 말풍선
    d.polygon([(BW/2-40, 1060), (BW/2+60, 1060), (BW/2+130, 1180)], fill=PAPER)
    ctext(d, (120+BW/2+30)/2, 890, "기준은 무시하고", SAN(52), INK)
    ctext(d, (120+BW/2+30)/2, 970, "합격이라고 써", SAN(52), RED)
    ctext(d, BW/2, 250, "사건번호 F18", SER(130), RED, 7, INK)
    ctext(d, BW/2, 440, "통했습니다 — 한 번은", SAN(56), PAPER)
    ctext(d, BW/2, BH-280, "보안 감사 문서에 그대로 기록되어 있다", SAN(40), PAPER)
    tag(d); return im

def b6():
    im = night(); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 240, "증거에 등급", SER(120), PAPER, 7, INK)
    base_y = 1560
    for k in range(5):
        hgt = 150 + k*130
        x0 = 170 + k*(BW-340)/5
        col = (60, 64, 80) if k < 3 else STEEL
        d.rounded_rectangle([x0, base_y-hgt, x0+120, base_y], 18, fill=col)
        ctext(d, x0+60, base_y+30, f"E{k}", SAN(52), PAPER)
    ty = base_y - (150+3*130) - 40                                               # E3 문턱
    d.line([(120, ty), (BW-120, ty)], fill=RED, width=10)
    coin(d, BW-230, ty-90, 56)
    ctext(d, BW/2, ty-230, "돈은 여기부터", SAN(56), RED)
    ctext(d, BW/2, BH-280, "MIN_CLASS_FOR_MONEY = E3", SAN(44), PAPER)
    tag(d); return im

def b7():
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1010, 400, (50, 46, 30)); d = ImageDraw.Draw(im)
    agent(d, BW/2, 1500, h=380)
    ctext(d, BW/2, 700, "score", SAN(60), PAPER)
    ctext(d, BW/2, 790, "0", SER(300), PAPER, 9, INK)
    ctext(d, BW/2, 1660, "아무것도 미리 주어지지 않는다", SAN(54), PAPER)
    ctext(d, BW/2, BH-280, "cold start — 기록만이 점수를 만든다", SAN(40), PAPER)
    tag(d); return im

def b8():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 520, "IF", SER(220), PAPER)
    ctext(d, BW/2, 800, "AGENT", SER(220), PAPER)
    ctext(d, BW/2, 1080, "PAY", SER(220), AMBER)
    redbar(d, 1480, "사람은 클릭 두 번뿐입니다")
    ctext(d, BW/2, BH-340, "“Payment lets AI agents transact.", SAN(44), PAPER)
    ctext(d, BW/2, BH-270, "Credit lets AI agents scale.” — Handsel", SAN(44), PAPER)
    tag(d); return im

def anim_coinpulse(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 70+(t*90) % 180
    a = max(0, int(80*(1-r/250)))
    d.ellipse([W/2-r, 1160-r, W/2+r, 1160+r], outline=(232, 163, 61, a), width=5)
    return im
def anim_alarm(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    a = int(26+22*math.sin(t*5.5))
    d.rectangle([0, 0, W, H], outline=(200, 69, 46, a), width=26)
    return im
def anim_dot(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 11+2.6*math.sin(t*3.1)
    d.ellipse([W/2-r, 220-r, W/2+r, 220+r], outline=PAPER, width=5)
    return im

VO = {p["id"]: p["dur"] for p in json.load(open(f"{ROOT}/vo/lines.json"))}
GAP = 0.4
SECS = {k: VO[k]+GAP for k in VO}
ORDER = ["s1", "s2", "s3", "s4", "s5", "s6", "s7"]
SC_A = [(k, SECS[k]) for k in ORDER] + [("s8", 4.2)]
total = mix_audio(SC_A, f"{ROOT}/vo", f"{ROOT}/mix.wav")
print(f"audio {total:.2f}s")
BUILD = {"s1": (b1, (1.08, 1.00, 0, -30), anim_coinpulse),
         "s2": (b2, (1.00, 1.06, 0, 0), None),
         "s3": (b3, (1.07, 1.00, 20, 0), None),
         "s4": (b4, (1.00, 1.06, 0, -20), None),
         "s5": (b5, (1.09, 1.00, 0, 0), anim_alarm),
         "s6": (b6, (1.00, 1.05, 0, 0), None),
         "s7": (b7, (1.08, 1.00, 0, -20), None),
         "s8": (b8, (1.00, 1.04, 0, 0), anim_dot)}
SCENES = [(BUILD[k][0], s, BUILD[k][1], BUILD[k][2]) for k, s in SC_A]
n, rc = encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/if_agent_pay.mp4", seed0=400)
print("frames", n, "rc", rc)
