"""EP3 「자유중국의 진보는 왜 시장을 원했나」 — 원칙 v1.0 고정 70초 포맷 렌더.

장면 = 인과 고리 1개. 화면 텍스트는 구조 라벨만.
S1(WTF)은 kinetic-typography 스킬의 스태거 리빌 레시피를 PIL로 이식 —
줄 단위 0.14s 스태거 + ease_out_back 팝 + 페이드 (첫 2초 투자, 원칙 8).
S4/S5는 같은 레이아웃·반대 색의 대구(對句) 카드 — 기존 질서 vs 개혁의 언어.
"""
import sys, os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../../malgap-style")
from noir_kit import *
import shorts_ui as UI
from PIL import Image, ImageDraw

TOP = 560
KMT_BLUE = (36, 66, 122)
GREEN = (110, 168, 92)
YELLOW = (255, 228, 0)

def chain_node(d, cx, y, w, txt, col, fsz=50):
    d.rounded_rectangle([cx-w/2, y, cx+w/2, y+130], 24, fill=(28, 32, 46), outline=col, width=7)
    ctext(d, cx, y+34, txt, SAN(fsz), PAPER)

def chain_arrow(d, cx, y0, y1, col=AMBER):
    d.line([(cx, y0), (cx, y1-26)], fill=col, width=10)
    d.polygon([(cx-26, y1-30), (cx+26, y1-30), (cx, y1+4)], fill=col)

def hanzi_cards(im, items, outline_col):
    d = ImageDraw.Draw(im)
    for i, (ch, lab) in enumerate(items):
        y = TOP+30+i*280
        d.rounded_rectangle([200, y, BW-200, y+240], 30, fill=(28, 32, 46),
                            outline=outline_col, width=8)
        ctext(d, 360, y+36, ch, SER(140), AMBER)
        ctext(d, 600, y+70, lab, SAN(80), PAPER, anchor="la")
    return im

def b1():   # WTF 배경 — 텍스트는 anim에서 스태거 입장
    im = night();
    im = glow(im, BW/2, 1000, 500, (34, 50, 36))
    return im

def s1_overlay(im, t):
    """진보당 결론 카드 — 줄별 스태거 팝 (kinetic-typography 레시피)."""
    d = ImageDraw.Draw(im, "RGBA")
    e0 = UI.ease_out_back(min(1, max(t, 0)/0.34))
    w2 = int((BW-240)/2*e0)
    if w2 > 8:
        d.rounded_rectangle([BW/2-w2, TOP+60, BW/2+w2, TOP+860], 34,
                            fill=(26, 34, 30, 255), outline=GREEN, width=10)
        hw = min(w2, BW//2-120)
        d.rectangle([BW/2-hw, TOP+64, BW/2+hw, TOP+240], fill=(*GREEN, 255))
    lines = [("진보당", SER(96), PAPER, TOP+100, 0.10),
             ("민영화", SAN(88), YELLOW, TOP+330, 0.34),
             ("개방 · 언론자유", SAN(80), YELLOW, TOP+520, 0.48),
             ("市場 · 改革", SER(64), (200, 202, 190), TOP+710, 0.62)]
    for txt, f, col, y, t0 in lines:
        if t <= t0: continue
        e = UI.ease_out_back((t-t0)/0.30)
        a = int(255*min(1, (t-t0)/0.18))
        lay = Image.new("RGBA", (BW, 220), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        dd.text((BW//2, 10), txt, font=f, fill=col+(a,), anchor="ma")
        sc = 0.90+0.10*min(e, 1.15)
        nw, nh = int(BW*sc), int(220*sc)
        lay = lay.resize((nw, nh))
        im.paste(lay, ((BW-nw)//2, y+int((1-min(e,1))*30)), lay)
    return im

def b2():   # 전제: 1946 갈림길
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

def b3():   # 약속: 모순? → 필연
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+180, "모순?", SER(240), PAPER)
    ctext(d, BW/2, TOP+640, "필연입니다", SER(110), YELLOW)
    return im

def b4():   # 원인 A: 기존 질서 = 국가 (대구 카드 앞면)
    im = night()
    im = hanzi_cards(im, [("營", "국영기업"), ("央", "중앙집권"), ("檢", "신문 검열")], RED)
    d = ImageDraw.Draw(im)
    # 베이스(1240x2200)→출력 크롭 특성상 TOP 위는 밴드에 가려짐 — 라벨은 카드 아래로
    d.rounded_rectangle([BW/2-220, 1445, BW/2+220, 1545], 20, outline=RED, width=6)
    ctext(d, BW/2, 1465, "기존 질서", SAN(54), (230, 140, 128))
    return im

def b5():   # 원인 A2: 개혁의 언어 (대구 카드 뒷면 — 같은 배치, 반대 색)
    im = night()
    im = hanzi_cards(im, [("市", "시장개혁"), ("分", "지방분권"), ("言", "언론자유")], GREEN)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([BW/2-250, 1445, BW/2+250, 1545], 20, outline=GREEN, width=6)
    ctext(d, BW/2, 1465, "개혁의 언어", SAN(54), (160, 210, 150))
    return im

def b6():   # 원인 B: 1980년대 민주화 연합 결집 + 실명 시민
    im = night(); d = ImageDraw.Draw(im)
    banner_y = TOP+120
    d.rounded_rectangle([BW/2-380, banner_y, BW/2+380, banner_y+170], 26,
                        fill=(30, 44, 38), outline=GREEN, width=8)
    ctext(d, BW/2, banner_y+40, "민주화 연합 1980", SAN(64), PAPER)
    labs = ["시장자유파", "분권파", "언론인", "학생"]
    for i, lab in enumerate(labs):
        x = 200 + i*(BW-400)//3
        y = TOP+560
        d.line([(x, y), (x, y+240)], fill=(90, 94, 108), width=8)
        d.polygon([(x+5, y), (x+215, y+36), (x+5, y+86)], fill=GREEN)
        ctext(d, x+34, y+16, lab, SAN(38), INK, anchor="la")
        d.line([(x, y), (BW/2 + (i-1.5)*90, banner_y+176)], fill=(70, 90, 78), width=5)
    name = "쉬리핑 (44) · 국영 신문 퇴사 기자"
    f = SAN(38); tw = d.textbbox((0, 0), name, font=f)[2]
    cx = max(tw/2+90, min(BW/2, BW-tw/2-90))
    d.rounded_rectangle([cx-tw/2-20, 1700, cx+tw/2+20, 1772], 14, fill=INK)
    d.text((cx-tw/2, 1714), name, font=f, fill=PAPER)
    return im

def b7():   # 원인 B2: 등식
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+180, "개혁의 언어", SER(110), PAPER)
    ctext(d, BW/2, TOP+420, "=", SER(160), (150, 152, 160))
    ctext(d, BW/2, TOP+640, "시장", SER(170), YELLOW)
    return im

def b8():   # Second Hook: 국영기업 노조가 보수 편에
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([120, TOP+120, BW/2-40, TOP+300], 24,
                        fill=(28, 32, 46), outline=YELLOW, width=7)
    ctext(d, (120+BW/2-40)/2, TOP+164, "보수", SAN(60), YELLOW)
    d.rounded_rectangle([BW/2+40, TOP+120, BW-120, TOP+300], 24,
                        fill=(28, 32, 46), outline=GREEN, width=7)
    ctext(d, (BW/2+40+BW-120)/2, TOP+164, "진보", SAN(60), GREEN)
    fx, fy = BW/2+180, TOP+760
    d.line([(fx, fy), (fx, fy+300)], fill=(90, 94, 108), width=10)
    d.polygon([(fx+6, fy), (fx+330, fy+52), (fx+6, fy+124)], fill=(170, 80, 60))
    ctext(d, fx+40, fy+24, "국영기업 노조", SAN(40), PAPER, anchor="la")
    pts = [(fx-40, fy+60), (BW/2-160, TOP+420)]
    d.line(pts, fill=AMBER, width=12)
    d.polygon([(BW/2-160, TOP+420), (BW/2-90, TOP+452), (BW/2-124, TOP+386)], fill=AMBER)
    ctext(d, BW/2, TOP+1030, "지킬 것이 있는 쪽으로", SER(80), PAPER, 5, INK)
    return im

def b9():   # Payoff: 사슬 회수 (EP2 v2와 대구)
    im = night(); d = ImageDraw.Draw(im)
    steps = [("기존 질서 = 국가", RED), ("바꿀 말은 반대말", PAPER), ("개혁의 언어 = 시장", GREEN)]
    y = TOP+60
    for i, (t, col) in enumerate(steps):
        chain_node(d, BW/2, y, 700, t, col, 52)
        if i < 2: chain_arrow(d, BW/2, y+130, y+210)
        y += 210
    y += 30
    d.line([(BW/2, y-80), (BW/2-230, y+10)], fill=YELLOW, width=8)
    d.line([(BW/2, y-80), (BW/2+230, y+10)], fill=GREEN, width=8)
    d.rounded_rectangle([120, y+10, BW/2-30, y+180], 22, fill=(28, 32, 46),
                        outline=YELLOW, width=7)
    ctext(d, (120+BW/2-30)/2, y+38, "보수", SAN(48), YELLOW)
    ctext(d, (120+BW/2-30)/2, y+104, "국가를 지킨다", SAN(40), PAPER)
    d.rounded_rectangle([BW/2+30, y+10, BW-120, y+180], 22, fill=(28, 32, 46),
                        outline=GREEN, width=7)
    ctext(d, (BW/2+30+BW-120)/2, y+38, "진보", SAN(48), GREEN)
    ctext(d, (BW/2+30+BW-120)/2, y+104, "시장으로 바꾼다", SAN(40), PAPER)
    return im

def b10():  # 확장: 국경 밖
    im = night(); d = ImageDraw.Draw(im)
    d.polygon([(180, 900), (420, 760), (700, 820), (820, 1020), (700, 1260),
               (430, 1320), (230, 1160)], outline=(120, 124, 138), width=8)
    ctext(d, 450, 1010, "自由中國", SER(64), tuple(int(c*0.85) for c in PAPER))
    d.polygon([(850, 1060), (930, 1020), (990, 1120), (950, 1300), (870, 1330),
               (880, 1180)], outline=AMBER, width=8)
    ctext(d, 918, 1370, "한국", SAN(52), AMBER)
    d.line([(700, 1040), (860, 1120)], fill=AMBER, width=10)
    d.polygon([(860, 1120), (800, 1128), (836, 1074)], fill=AMBER)
    ctext(d, BW/2, TOP+60, "더 큰 뒤집힘", SER(96), PAPER, 6, INK)
    return im

def b11():  # 다음 모순 — 하드컷
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+140, "이 세계의 한국은", SER(100), PAPER)
    ctext(d, BW/2, TOP+360, "보수가 친중", SER(140), YELLOW)
    ctext(d, BW/2, TOP+600, "진보가 반중", SER(140), (140, 200, 130))
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
        UI.title_band(im, "자유중국의 진보는", "왜 시장을 원했나?",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP3",
                      world="가상 역사 · 국민당이 이긴 세계의 진보")
        for c, cs, cd in sc["chips"]:
            if cs <= t < cs+cd+0.10:
                UI.chip(im, c, t-cs); break
        return im
    return anim
SCENES = []
for i, sc in enumerate(SC):
    kb = (1.07, 1.00, 0, -25) if i % 2 == 0 else (1.00, 1.06, 15, 0)
    if i == 0: kb = (1.00, 1.02, 0, 0)   # WTF는 오버레이 팝이 주인공 — 줌 최소화
    SCENES.append((BULD[i], sc["secs"], kb, make_anim(i, sc)))

import noir_kit as NK
_orig = NK.kb_crop
NK.kb_crop = lambda base, p, kb: _orig(base, smooth(p), kb)
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep3.mp4", seed0=3000, trans=0.20)
print("frames", n, "rc", rc)
