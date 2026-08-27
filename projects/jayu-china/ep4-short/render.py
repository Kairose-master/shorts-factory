"""EP4 「한국 보수는 왜 친중이 되었나」 — 원칙 v1.0 고정 70초 포맷 렌더.

정본 §8 시각 지침 준수: 한미중 삼각도 대신 한국전쟁 기억·철도·재계·안보 협력의
계보를 시각으로 연결. 좌표 안전 규칙: 장면 요소 base y 540~1410, 태그류 1700~1780.
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

def korea(d, ox, oy, s, outline=AMBER, width=8):
    pts = [(850, 1060), (930, 1020), (990, 1120), (950, 1300), (870, 1330), (880, 1180)]
    d.polygon([(ox+(x-850)*s, oy+(y-1020)*s) for x, y in pts], outline=outline, width=width)

def b1():   # WTF 배경 — 텍스트는 s1_overlay
    im = night()
    return glow(im, BW/2, 1000, 500, (54, 42, 30))

def s1_overlay(im, t):
    OW = UI.W  # anim은 kb_crop 이후 1080 출력 좌표계
    d = ImageDraw.Draw(im, "RGBA")
    e0 = UI.ease_out_back(min(1, max(t, 0)/0.34))
    w2 = int((OW-200)/2*e0)
    if w2 > 8:
        d.rounded_rectangle([OW/2-w2, TOP+60, OW/2+w2, TOP+860], 34,
                            fill=(34, 28, 26, 255), outline=RED, width=10)
        hw = min(w2, OW//2-120)
        d.rectangle([OW/2-hw, TOP+64, OW/2+hw, TOP+240], fill=(*RED, 255))
    lines = [("한국 보수당", SER(92), PAPER, TOP+104, 0.10),
             ("親中", SER(200), YELLOW, TOP+330, 0.34),
             ("친중입니다", SAN(80), PAPER, TOP+650, 0.52)]
    for txt, f, col, y, t0 in lines:
        if t <= t0: continue
        e = UI.ease_out_back((t-t0)/0.30)
        a = int(255*min(1, (t-t0)/0.18))
        lay = Image.new("RGBA", (OW, 300), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        dd.text((OW//2, 10), txt, font=f, fill=col+(a,), anchor="ma")
        sc = 0.90+0.10*min(e, 1.15)
        nw, nh = int(OW*sc), int(300*sc)
        lay = lay.resize((nw, nh))
        im.paste(lay, ((OW-nw)//2, y+int((1-min(e, 1))*30)), lay)
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

def b3():   # 약속
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+200, "역사가", SER(150), PAPER)
    ctext(d, BW/2, TOP+460, "달랐으니까요", SER(130), YELLOW)
    return im

def b4():   # 원인 A: 중공군 없는 한국전쟁 — 압록강을 넘은 보급 열차
    im = night(); d = ImageDraw.Draw(im)
    korea(d, 620, 820, 3.2, outline=(150, 154, 166), width=10)
    d.line([(150, 900), (700, 830)], fill=STEEL, width=12)                  # 압록강
    ctext(d, 250, 940, "압록강", SAN(44), STEEL)
    for k in range(9):                                                       # 철도 침목
        x = 180+k*62
        d.line([(x, 760-(x-180)*0.09-16), (x, 760-(x-180)*0.09+16)], fill=(120, 96, 44), width=8)
    d.line([(150, 762), (720, 712)], fill=AMBER, width=10)                   # 선로
    d.rounded_rectangle([300, 640, 560, 720], 16, fill=(40, 44, 58), outline=AMBER, width=6)
    d.ellipse([330, 706, 374, 750], fill=(30, 32, 42), outline=AMBER, width=5)
    d.ellipse([480, 706, 524, 750], fill=(30, 32, 42), outline=AMBER, width=5)
    ctext(d, 430, 656, "보급 열차", SAN(44), PAPER)
    card_y = 1500
    d.rounded_rectangle([BW/2-300, card_y, BW/2+300, card_y+140], 22,
                        fill=(28, 32, 46), outline=(100, 106, 122), width=6)
    ctext(d, BW/2-60, card_y+38, "중공군", SAN(62), (150, 154, 166))
    d.line([(BW/2+90, card_y+30), (BW/2+230, card_y+110)], fill=RED, width=12)
    d.line([(BW/2+230, card_y+30), (BW/2+90, card_y+110)], fill=RED, width=12)
    return im

def b5():   # 원인 A2: 동맹 — 같은 편
    im = night(); d = ImageDraw.Draw(im)
    for i, lab in enumerate(["자유중국", "한국"]):
        x0 = 220+i*(BW-440-220)+i*220
        x0 = 250 if i == 0 else BW-250-0
        px = 320 if i == 0 else BW-320
        d.line([(px, TOP+160), (px, TOP+760)], fill=(90, 94, 108), width=12)
        d.polygon([(px+6, TOP+160), (px+320 if i == 0 else px-320, TOP+230),
                   (px+6, TOP+300)] if i == 0 else
                  [(px-6, TOP+160), (px-320, TOP+230), (px-6, TOP+300)], fill=AMBER)
        ctext(d, px+(160 if i == 0 else -160), TOP+196, lab, SAN(44), INK)
    st = seal_word("同盟"); im.paste(st, (int(BW/2-st.width/2), TOP+430), st)
    ctext(d, BW/2, TOP+900, "같은 편의 기억", SER(84), PAPER, 5, INK)
    return im

def b6():   # 원인 B: 대륙 종단 철도 — 부산→난징
    im = night(); d = ImageDraw.Draw(im)
    stops = [("부산", 880, 1360), ("서울", 700, 1090), ("신의주", 520, 820), ("난징", 300, 560)]
    for k in range(len(stops)-1):
        d.line([(stops[k][1], stops[k][2]), (stops[k+1][1], stops[k+1][2])], fill=AMBER, width=10)
    for name, x, y in stops:
        big = name in ("부산", "난징")
        r = 22 if big else 14
        d.ellipse([x-r, y-r, x+r, y+r], fill=AMBER if big else (150, 154, 166))
        ctext(d, x+40, y-30, name, SAN(54 if big else 44),
              YELLOW if big else PAPER, anchor="la")
    ctext(d, BW/2, TOP+40, "수출길 = 대륙", SER(92), PAPER, 6, INK)
    return im

def b7():   # 원인 B2: 재계 — 항만 크레인 + 실명 시민
    im = night(); d = ImageDraw.Draw(im)
    d.rectangle([0, 1300, BW, 1320], fill=(60, 64, 78))                      # 부두
    for i in range(3):                                                       # 컨테이너
        d.rectangle([160+i*250, 1210, 160+i*250+200, 1300],
                    fill=[(120, 96, 44), (91, 104, 123), (140, 70, 52)][i])
    d.line([(760, 1300), (760, 700)], fill=(100, 106, 122), width=16)        # 크레인
    d.line([(560, 780), (1040, 780)], fill=(100, 106, 122), width=14)
    d.line([(920, 780), (920, 980)], fill=(100, 106, 122), width=8)
    d.rectangle([860, 980, 980, 1060], fill=(120, 96, 44))
    ctext(d, BW/2, TOP+40, "지킬 것이 많은 쪽", SER(84), PAPER, 5, INK)
    name = "김도현 (58) · 부산 물류가문 3대"
    f = SAN(38); tw = d.textbbox((0, 0), name, font=f)[2]
    d.rounded_rectangle([BW/2-tw/2-20, 1700, BW/2+tw/2+20, 1772], 14, fill=INK)
    d.text((BW/2-tw/2, 1714), name, font=f, fill=PAPER)
    return im

def b8():   # Second Hook: 반공의 방향 — 베이징이 아니라 모스크바
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([140, TOP+520, BW/2-60, TOP+700], 24,
                        fill=(24, 28, 40), outline=(90, 96, 112), width=6)
    ctext(d, (140+BW/2-60)/2, TOP+566, "베이징", SAN(56), (120, 124, 138))
    d.rounded_rectangle([BW/2+60, TOP+520, BW-140, TOP+700], 24,
                        fill=(34, 26, 28), outline=RED, width=8)
    ctext(d, (BW/2+60+BW-140)/2, TOP+566, "모스크바", SAN(56), (230, 140, 128))
    cx, cy = BW/2, TOP+260
    d.ellipse([cx-30, cy-30, cx+30, cy+30], fill=PAPER)
    d.line([(cx, cy), (BW-240, TOP+500)], fill=RED, width=12)                # 바늘 → 모스크바
    d.polygon([(BW-240, TOP+500), (BW-300, TOP+488), (BW-262, TOP+444)], fill=RED)
    ctext(d, BW/2, TOP+880, "反共의 방향", SER(96), PAPER, 6, INK)
    return im

def b9():   # Payoff: 사슬 회수
    im = night(); d = ImageDraw.Draw(im)
    steps = [("중공군 없는 전쟁", PAPER), ("적대 기억 없음", PAPER),
             ("동맹 + 대륙경제", AMBER), ("보수 = 친중", YELLOW)]
    y = TOP+40
    for i, (t, col) in enumerate(steps):
        chain_node(d, BW/2, y, 660, t, col, 50)
        if i < 3: chain_arrow(d, BW/2, y+126, y+206)
        y += 206
    ctext(d, BW/2, y+40, "기억이 다르면 묶음이 다르다", SAN(50),
          tuple(int(c*0.9) for c in PAPER))
    return im

def b10():  # 확장: 질문
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+140, "그럼, 누가", SER(120), PAPER)
    ctext(d, BW/2, TOP+360, "중국 의존을", SER(120), PAPER)
    ctext(d, BW/2, TOP+580, "비판할까?", SER(140), YELLOW)
    return im

def b11():  # 다음 모순 — 하드컷
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+160, "\"중국 자본을", SER(130), PAPER)
    ctext(d, BW/2, TOP+380, "막아라\"", SER(130), PAPER)
    ctext(d, BW/2, TOP+680, "— 진보의 구호", SER(110), (140, 200, 130))
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
        UI.title_band(im, "한국 보수는 왜", "친중이 되었나?",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP4",
                      world="가상 역사 · 국민당이 이긴 세계의 한국")
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep4.mp4", seed0=4000, trans=0.20)
print("frames", n, "rc", rc)
