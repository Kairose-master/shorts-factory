"""EP4 「한국 보수는 왜 친중이 되었나」 — 리마스터 v2 (일러스트 씬 + 실측 자막).

리마스터 원칙: 내용·대본·정본 준거는 v1 그대로, 시각만 레퍼런스급 일러스트로.
스펙: ../remaster/SPEC.md. 좌표: 장면 요소 base y540~1410, 태그 1700~1772.
"""
import sys, os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../../malgap-style")
sys.path.insert(0, f"{ROOT}/../remaster")
from noir_kit import *
import shorts_ui as UI
import char_kit as CK
import vo_kit
from PIL import Image, ImageDraw

TOP = 560
GREEN = (110, 168, 92)
YELLOW = (255, 228, 0)


def b1():   # WTF: 한중 정치인 악수 — 텍스트는 s1_overlay
    im = CK.sky(top=(20, 22, 34), bot=(50, 52, 64), hor=1360)
    d = ImageDraw.Draw(im)
    CK.skyline(d, hor=1360, seed=41, y_min=760)
    CK.ground_line(d, 1360)
    mid = (BW//2, 1180)
    CK.person(d, 430, 1385, h=560, outfit="suit_b", expr="smug", facing=1,
              pose="reach_r", tie=CK.TIE_B, reach=mid)
    CK.person(d, 810, 1385, h=560, outfit="suit", expr="smug", facing=-1,
              pose="reach_l", tie=CK.TIE_R, reach=(mid[0]-8, mid[1]+6))
    ctext(d, 350, 1460, "한국 보수당", SAN(40), PAPER, 4, INK)
    ctext(d, 900, 1460, "자유중국", SAN(40), (236, 196, 120), 4, INK)
    return im


def s1_overlay(im, t):
    OW = UI.W
    d = ImageDraw.Draw(im, "RGBA")
    if t > 0.10:
        a = int(255*min(1, (t-0.10)/0.20))
        d.text((OW//2, 420), "한국 보수당은", font=SAN(54), fill=PAPER+(a,),
               stroke_width=8, stroke_fill=(0, 0, 0, a), anchor="ma")
    if t > 0.42:
        e = UI.ease_out_back((t-0.42)/0.30)
        sc = 0.55 + 0.40*min(e, 1.2)
        lay = Image.new("RGBA", (520, 320), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        dd.rectangle([16, 16, 504, 304], outline=RED+(255,), width=16)
        dd.text((260, 40), "親中", font=SER(190), fill=YELLOW+(255,), anchor="ma")
        lay = lay.rotate(-7, expand=True, resample=Image.BICUBIC)
        nw, nh = int(lay.width*sc), int(lay.height*sc)
        lay = lay.resize((nw, nh))
        a = int(255*min(1, (t-0.42)/0.16))
        lay.putalpha(lay.getchannel("A").point(lambda v: v*a//255))
        im.paste(lay, (OW//2-nw//2, 625-nh//2), lay)
    return im


def b2():   # 전제: 1946 갈림길 (시리즈 앵커 v2)
    return CK.anchor_1946(SER, SAN, ctext, night)


def b3():   # 약속: 타이포 + 어깨 으쓱
    im = CK.sky(top=(16, 17, 24), bot=(30, 31, 40), hor=1430)
    d = ImageDraw.Draw(im)
    CK.ground_line(d, 1430, col=(44, 42, 44))
    ctext(d, BW/2, TOP+90, "이유는", SER(140), PAPER)
    ctext(d, BW/2, TOP+330, "역사가 달랐다", SER(126), YELLOW)
    CK.person(d, BW/2, 1520, h=390, outfit="student", expr="smile",
              pose="hands_up", tie=CK.TIE_B)
    return im


def b4():   # 원인A: 압록강 철교를 건너는 보급 열차
    im = CK.sky(top=(18, 22, 32), bot=(48, 52, 64), hor=1210)
    d = ImageDraw.Draw(im)
    CK.forest(d, hor=1210, seed=4, col=(32, 44, 38))
    d.rectangle([0, 1210, BW, 1520], fill=(38, 52, 66))          # 강
    for k in range(5):
        d.arc([80+k*240, 1240+18*(k % 2), 300+k*240, 1300], 200, 340,
              fill=(66, 84, 100), width=8)
    CK.bridge(d, -40, BW+40, 1150, s=1.0)
    CK.train(d, 980, 1150, s=0.86, cars=2)
    CK.smoke(d, 890, 900, s=0.9)
    d.rectangle([0, 1520, BW, BH], fill=(40, 38, 40))            # 남안
    CK.person(d, 260, 1700, h=430, outfit="uniform", expr="smile", hat="helmet",
              pose="wave", facing=1)
    CK.person(d, 480, 1720, h=400, outfit="uniform", expr="surprised", hat="helmet",
              pose="stand", facing=1)
    ctext(d, 300, 1180, "압록강", SAN(44), (140, 168, 190))
    # 중공군 없음 카드
    d.rounded_rectangle([BW/2-280, 680, BW/2+280, 820], 22,
                        fill=(28, 32, 46), outline=(100, 106, 122), width=6)
    ctext(d, BW/2-70, 716, "중공군", SAN(62), (150, 154, 166))
    d.line([(BW/2+90, 710), (BW/2+230, 790)], fill=RED, width=12)
    d.line([(BW/2+230, 710), (BW/2+90, 790)], fill=RED, width=12)
    return im


def b5():   # 원인A2: 같은 편 — 두 병사 + 同盟
    im = CK.sky(top=(20, 24, 34), bot=(52, 56, 68), hor=1380)
    d = ImageDraw.Draw(im)
    CK.cloudband(d, 700, col=(46, 50, 64))
    CK.ground_line(d, 1380)
    CK.flagpole(d, 200, 1380, 640, 260, (176, 122, 50))
    CK.flagpole(d, BW-200, 1380, 640, -260, (74, 92, 120))
    CK.person(d, 505, 1400, h=460, outfit="uniform", expr="smile", hat="helmet",
              facing=1, pose="stand")
    CK.person(d, 735, 1400, h=430, outfit="uniform", expr="smile", hat="helmet",
              facing=-1, pose="stand")
    ctext(d, 300, 1450, "자유중국군", SAN(38), (236, 196, 120), 4, INK)
    ctext(d, 950, 1450, "한국군", SAN(38), PAPER, 4, INK)
    st = seal_word("同盟"); im.paste(st, (int(BW/2-st.width/2), 545), st)
    ctext(d, BW/2, 878, "같은 편의 기억", SER(76), PAPER, 5, INK)
    return im


def b6():   # 원인B: 대륙 종단 철도 부산→난징
    im = CK.sky(top=(16, 20, 30), bot=(44, 48, 60), hor=1500)
    d = ImageDraw.Draw(im)
    CK.skyline(d, hor=1500, seed=6, y_min=1150)
    CK.ground_line(d, 1500)
    stops = [("부산", 850, 1400), ("서울", 660, 1120), ("신의주", 500, 860), ("난징", 300, 620)]
    for k in range(len(stops)-1):
        d.line([(stops[k][1], stops[k][2]), (stops[k+1][1], stops[k+1][2])],
               fill=INK, width=22)
        d.line([(stops[k][1], stops[k][2]), (stops[k+1][1], stops[k+1][2])],
               fill=AMBER, width=12)
    for name, x, y in stops:
        big = name in ("부산", "난징")
        r = 24 if big else 15
        d.ellipse([x-r, y-r, x+r, y+r], fill=AMBER if big else (150, 154, 166),
                  outline=INK, width=6)
        if name == "부산":
            ctext(d, x-44, y-70, name, SAN(56), YELLOW, 4, INK, anchor="ra")
        else:
            ctext(d, x+44, y-32, name, SAN(56 if big else 44),
                  YELLOW if big else PAPER, 4, INK, anchor="la")
    CK.train(d, 1210, 1500, s=0.46, cars=1)
    ctext(d, BW/2, TOP+20, "수출길 = 대륙", SER(92), PAPER, 6, INK)
    return im


def b7():   # 원인B2: 부산항 재계 — 김도현
    im = CK.sky(top=(24, 28, 40), bot=(58, 60, 72), hor=1290)
    d = ImageDraw.Draw(im)
    CK.ship(d, 930, 1120, s=0.9)
    d.rectangle([0, 1290, BW, BH], fill=(44, 42, 44))
    d.rectangle([0, 1280, BW, 1302], fill=(60, 64, 78))
    CK.crane(d, 900, 1280, s=0.94, dir=-1)
    CK.containers(d, 100, 1280, s=0.95)
    CK.person(d, 420, 1660, h=520, outfit="suit", expr="smug", facing=1,
              pose="hold_case", tie=CK.TIE_R)
    ctext(d, BW/2, TOP+20, "지킬 것이 많은 쪽", SER(84), PAPER, 5, INK)
    name = "김도현 (58) · 부산 물류가문 3대"
    f = SAN(38); tw = d.textbbox((0, 0), name, font=f)[2]
    d.rounded_rectangle([BW/2-tw/2-20, 1780, BW/2+tw/2+20, 1852], 14, fill=INK)
    d.text((BW/2-tw/2, 1794), name, font=f, fill=PAPER)
    return im


def b8():   # Second Hook: 반공 보수의 시선 — 모스크바
    im = CK.sky(top=(20, 20, 30), bot=(46, 44, 54), hor=1420)
    d = ImageDraw.Draw(im)
    CK.ground_line(d, 1420)
    CK.person(d, BW/2, 1460, h=460, outfit="coat", expr="closed", facing=0,
              pose="arms_cross")
    ctext(d, BW/2, 555, "反共의 방향", SER(84), PAPER, 6, INK)
    d.rounded_rectangle([120, 760, 520, 920], 24,
                        fill=(24, 28, 40), outline=(90, 96, 112), width=6)
    ctext(d, 320, 800, "베이징", SAN(56), (120, 124, 138))
    d.rounded_rectangle([BW-520, 760, BW-120, 920], 24,
                        fill=(34, 26, 28), outline=RED, width=8)
    ctext(d, BW-320, 800, "모스크바", SAN(56), (230, 140, 128))
    cx, cy = BW/2, 715
    d.ellipse([cx-26, cy-26, cx+26, cy+26], fill=PAPER, outline=INK, width=6)
    d.line([(cx, cy), (BW-300, 775)], fill=RED, width=14)
    d.polygon([(BW-300, 775), (BW-360, 761), (BW-322, 719)], fill=RED)
    ctext(d, BW/2, 1500, "이 세계의 반공 보수", SAN(40), (200, 196, 188), 4, INK)
    return im


def b9():   # Payoff: 인과 사슬 (다이어그램 유지 + 배경만 씬)
    im = CK.sky(top=(15, 16, 23), bot=(32, 33, 42), hor=1560)
    d = ImageDraw.Draw(im)
    CK.skyline(d, hor=1560, seed=9, y_min=1300)
    CK.ground_line(d, 1560)
    steps = [("중공군 없는 전쟁", PAPER), ("적대 기억 없음", PAPER),
             ("동맹 + 대륙경제", AMBER), ("보수 = 친중", YELLOW)]
    y = TOP+30
    for i, (t, col) in enumerate(steps):
        d.rounded_rectangle([BW/2-330, y, BW/2+330, y+126], 24,
                            fill=(28, 32, 46), outline=col, width=7)
        ctext(d, BW/2, y+34, t, SAN(50), col if col != PAPER else PAPER)
        if i < 3:
            d.line([(BW/2, y+126), (BW/2, y+182)], fill=AMBER, width=10)
            d.polygon([(BW/2-24, y+178), (BW/2+24, y+178), (BW/2, y+208)], fill=AMBER)
        y += 206
    ctext(d, BW/2, y+36, "기억이 다르면 묶음이 다르다", SAN(50),
          tuple(int(c*0.9) for c in PAPER))
    return im


def b10():  # 확장: 질문 + 고민하는 청년
    im = CK.sky(top=(16, 17, 24), bot=(30, 31, 40), hor=1450)
    d = ImageDraw.Draw(im)
    CK.ground_line(d, 1450, col=(44, 42, 44))
    ctext(d, BW/2, TOP+20, "그럼, 누가", SER(120), PAPER)
    ctext(d, BW/2, TOP+220, "중국 의존을", SER(120), PAPER)
    ctext(d, BW/2, TOP+420, "비판할까?", SER(140), YELLOW)
    CK.person(d, BW/2, 1560, h=350, outfit="student", expr="worried",
              pose="stand", tie=CK.TIE_B)
    return im


def b11():  # 다음 모순: 진보의 피켓 시위 — 하드컷
    im = CK.sky(top=(14, 18, 16), bot=(30, 38, 30), hor=1420)
    d = ImageDraw.Draw(im)
    CK.skyline(d, hor=1420, seed=11, y_min=900)
    CK.ground_line(d, 1420)
    def sign_txt(dd, cx, cy):
        dd.text((cx, cy-56), "중국 자본을", font=SAN(60), fill=INK, anchor="ma")
        dd.text((cx, cy+12), "막아라", font=SAN(68), fill=RED, anchor="ma")
    CK.picket(d, 400, 590, 560, 240, txt_draw=sign_txt, pole_to=1160)
    CK.person(d, 400, 1470, h=440, outfit="worker", expr="shout", hat="cap",
              pose="hold_sign", facing=0)
    CK.person(d, 880, 1470, h=460, outfit="suit_r", expr="shout",
              pose="hands_up", facing=0)
    ctext(d, 880, 700, "진보의", SER(92), (140, 200, 130), 6, INK)
    ctext(d, 880, 852, "구호", SER(92), (140, 200, 130), 6, INK)
    return im


VOJ = json.load(open(f"{ROOT}/vo2/lines.json"))
GAP = 0.12
LEAD = 0.15
SC = []; t0 = 0.0
for p in VOJ:
    secs = p["dur"]+GAP+(0.10 if p["id"] == "s11" else 0)
    chips = vo_kit.chips_from_words(p) or UI.chunks_for(p["text"], p["dur"]+0.15)
    SC.append({"id": p["id"], "secs": secs, "t0": t0,
               "chips": [(c, t+LEAD, dur) for c, t, dur in chips]})
    t0 += secs
print(f"audio {mix_audio([(s['id'], s['secs']) for s in SC], f'{ROOT}/vo2', f'{ROOT}/mix.wav', lead=LEAD):.2f}s")

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
