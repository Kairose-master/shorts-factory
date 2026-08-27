"""EP5 「"중국 자본을 막아라" — 한국 진보의 탄생」 — 원칙 v1.0 고정 70초 포맷 렌더.

EP4의 거울: EP4 빨강 카드 親中(보수) ↔ EP5 초록 카드 反中(진보).
정본 §8 시각언어 사용: 신문(재계 사설), 깃발(노조), 정책 대립 카드, 저울.
좌표 안전 규칙: 장면 요소 base y 540~1410, 태그류 1700~1780.
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

def b1():
    im = night()
    return glow(im, BW/2, 1000, 500, (34, 52, 36))

def s1_overlay(im, t):
    OW = UI.W  # anim은 kb_crop 이후 1080 출력 좌표계
    d = ImageDraw.Draw(im, "RGBA")
    e0 = UI.ease_out_back(min(1, max(t, 0)/0.34))
    w2 = int((OW-200)/2*e0)
    if w2 > 8:
        d.rounded_rectangle([OW/2-w2, TOP+60, OW/2+w2, TOP+860], 34,
                            fill=(26, 34, 30, 255), outline=GREEN, width=10)
        hw = min(w2, OW//2-120)
        d.rectangle([OW/2-hw, TOP+64, OW/2+hw, TOP+240], fill=(*GREEN, 255))
    lines = [("진보당", SER(92), INK, TOP+104, 0.10),
             ("反中", SER(200), YELLOW, TOP+330, 0.34),
             ("중국 자본을 막아라", SAN(72), PAPER, TOP+660, 0.52)]
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

def b3():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+180, "누가?", SER(190), PAPER)
    ctext(d, BW/2, TOP+520, "왜?", SER(240), YELLOW)
    return im

def b4():   # 원인 A: 통합의 청구서 — 들어오는 자본 / 나가는 공장
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([130, TOP+120, BW/2-50, TOP+960], 28, fill=(30, 26, 26),
                        outline=RED, width=8)
    ctext(d, (130+BW/2-50)/2, TOP+170, "들어온다", SAN(52), (230, 140, 128))
    ctext(d, (130+BW/2-50)/2, TOP+300, "中資", SER(120), PAPER)
    for i, t in enumerate(["항만", "플랫폼", "부동산"]):
        y = TOP+520+i*130
        d.rounded_rectangle([180, y, BW/2-100, y+96], 16, fill=(26, 30, 42))
        ctext(d, (180+BW/2-100)/2, y+22, t, SAN(46), PAPER)
    d.rounded_rectangle([BW/2+50, TOP+120, BW-130, TOP+960], 28, fill=(26, 30, 28),
                        outline=(90, 96, 112), width=8)
    ctext(d, (BW/2+50+BW-130)/2, TOP+170, "나간다", SAN(52), (150, 154, 166))
    ctext(d, (BW/2+50+BW-130)/2, TOP+300, "工場", SER(120), (150, 154, 166))
    for i, t in enumerate(["조선", "가전", "섬유"]):
        y = TOP+520+i*130
        d.rounded_rectangle([BW/2+100, y, BW-180, y+96], 16, fill=(24, 27, 38))
        ctext(d, (BW/2+100+BW-180)/2, y+22, t, SAN(46), (150, 154, 166))
    return im

def b5():   # 원인 A2: 저울 — 수혜는 재계로, 청구서는 노동으로
    im = night(); d = ImageDraw.Draw(im)
    cx, py = BW/2, TOP+220
    d.line([(cx, py), (cx, py+520)], fill=(100, 106, 122), width=14)         # 기둥
    d.polygon([(cx-90, py+540), (cx+90, py+540), (cx, py+490)], fill=(100, 106, 122))
    d.line([(cx-380, py+40), (cx+380, py-60)], fill=(140, 144, 156), width=12)  # 기운 들보
    d.rounded_rectangle([cx-500, py+60, cx-260, py+200], 20, fill=(28, 32, 46),
                        outline=AMBER, width=7)                              # 무거운 쪽(수혜)
    ctext(d, cx-380, py+96, "재계", SAN(54), AMBER)
    d.rounded_rectangle([cx+260, py-200, cx+500, py-60], 20, fill=(28, 32, 46),
                        outline=(90, 96, 112), width=7)
    ctext(d, cx+380, py-164, "노동", SAN(54), (150, 154, 166))
    ctext(d, cx-380, py+240, "수혜", SAN(42), tuple(int(c*0.9) for c in PAPER))
    ctext(d, cx+380, py-20, "청구서", SAN(42), (230, 140, 128))
    name = "박성호 (41) · 인천 조선소 용접공"
    f = SAN(38); tw = d.textbbox((0, 0), name, font=f)[2]
    d.rounded_rectangle([BW/2-tw/2-20, 1700, BW/2+tw/2+20, 1772], 14, fill=INK)
    d.text((BW/2-tw/2, 1714), name, font=f, fill=PAPER)
    return im

def b6():   # 원인 B: 네 가지 말 (정본 명시 4종) — 2x2 카드
    im = night(); d = ImageDraw.Draw(im)
    items = [("主權", "산업주권"), ("勞動", "노동"), ("文化", "문화자율"), ("外交", "다변화")]
    for i, (ch, lab) in enumerate(items):
        r, c = divmod(i, 2)
        x0, y0 = 150+c*(BW//2-90), TOP+80+r*420
        d.rounded_rectangle([x0, y0, x0+BW//2-150, y0+340], 26, fill=(26, 32, 28),
                            outline=GREEN, width=8)
        ctext(d, x0+(BW//2-150)/2, y0+50, ch, SER(110), AMBER)
        ctext(d, x0+(BW//2-150)/2, y0+220, lab, SAN(56), PAPER)
    return im

def b7():   # 원인 B2: 등식
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+140, "기존 질서와", SER(110), PAPER)
    ctext(d, BW/2, TOP+340, "싸우는 쪽", SER(120), PAPER)
    ctext(d, BW/2, TOP+580, "= 진보", SER(160), YELLOW)
    return im

def b8():   # Second Hook: 뒤집힌 장면 — 노조 깃발 主權 / 재계 신문 開放
    im = night(); d = ImageDraw.Draw(im)
    fx = 300
    d.line([(fx, TOP+180), (fx, TOP+840)], fill=(90, 94, 108), width=12)
    d.polygon([(fx+6, TOP+180), (fx+400, TOP+265), (fx+6, TOP+350)], fill=RED)
    ctext(d, fx+150, TOP+230, "主權", SER(76), PAPER, anchor="la")
    ctext(d, fx+40, TOP+900, "노조 집회", SAN(46), PAPER, anchor="la")
    nx0, ny0 = BW/2+60, TOP+420
    d.rectangle([nx0, ny0, BW-130, ny0+560], fill=PAPER)                      # 신문
    ctext(d, (nx0+BW-130)/2, ny0+36, "自由日報", SAN(40), (120, 110, 96))
    d.line([(nx0+40, ny0+110), (BW-170, ny0+110)], fill=(150, 140, 124), width=4)
    ctext(d, (nx0+BW-130)/2, ny0+150, "開放", SER(130), INK)
    for k in range(4):
        d.line([(nx0+40, ny0+360+k*46), (BW-170-(k % 2)*80, ny0+360+k*46)],
               fill=(170, 160, 144), width=7)
    ctext(d, (nx0+BW-130)/2, ny0+600, "재계 사설", SAN(46), PAPER)
    return im

def b9():   # Payoff: 분기 회수
    im = night(); d = ImageDraw.Draw(im)
    chain_node(d, BW/2, TOP+60, 700, "대륙 의존", AMBER, 52)
    y0 = TOP+186
    d.line([(BW/2, y0), (BW/2-250, y0+120)], fill=YELLOW, width=9)
    d.line([(BW/2, y0), (BW/2+250, y0+120)], fill=GREEN, width=9)
    chain_node(d, BW/2-250, y0+130, 420, "만든 쪽", YELLOW, 46)
    chain_node(d, BW/2+250, y0+130, 420, "청구서 받는 쪽", GREEN, 40)
    chain_arrow(d, BW/2-250, y0+256, y0+336, YELLOW)
    chain_arrow(d, BW/2+250, y0+256, y0+336, GREEN)
    d.rounded_rectangle([BW/2-460, y0+340, BW/2-40, y0+470], 22, fill=(28, 32, 46),
                        outline=YELLOW, width=7)
    ctext(d, BW/2-250, y0+372, "지킨다 = 보수", SAN(44), YELLOW)
    d.rounded_rectangle([BW/2+40, y0+340, BW/2+460, y0+470], 22, fill=(28, 32, 46),
                        outline=GREEN, width=7)
    ctext(d, BW/2+250, y0+372, "저항한다 = 진보", SAN(44), GREEN)
    ctext(d, BW/2, y0+560, "무엇에 의존하는지가", SAN(48), PAPER)
    ctext(d, BW/2, y0+640, "누가 저항하는지를 정한다", SAN(48), PAPER)
    return im

def b10():  # 확장: 정당은 싸우고 청년은 떠난다
    im = night(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([170, TOP+200, BW/2-60, TOP+380], 26, fill=PAPER)
    ctext(d, (170+BW/2-60)/2, TOP+246, "막아라!", SAN(52), INK)
    d.polygon([(330, TOP+374), (410, TOP+374), (350, TOP+450)], fill=PAPER)
    d.rounded_rectangle([BW/2+60, TOP+200, BW-170, TOP+380], 26, fill=PAPER)
    ctext(d, (BW/2+60+BW-170)/2, TOP+246, "열어라!", SAN(52), INK)
    d.polygon([(BW-330, TOP+374), (BW-250, TOP+374), (BW-290, TOP+450)], fill=PAPER)
    px, gy = BW/2, 1400
    d.ellipse([px-40, gy-420, px+40, gy-336], fill=(230, 205, 180))          # 청년
    d.pieslice([px-44, gy-428, px+44, gy-360], 180, 360, fill=(40, 34, 30))
    d.rounded_rectangle([px-62, gy-342, px+62, gy], 34, fill=(46, 66, 92))
    d.rounded_rectangle([px+42, gy-300, px+86, gy-120], 16, fill=(70, 90, 110))
    d.line([(px+140, gy-160), (px+330, gy-160)], fill=AMBER, width=10)       # 제 갈 길
    d.polygon([(px+330, gy-160), (px+270, gy-190), (px+270, gy-130)], fill=AMBER)
    ctext(d, BW/2, TOP+40, "정당은 싸우고", SER(84), PAPER, 5, INK)
    return im

def b11():  # 다음 모순 — 하드컷
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, TOP+150, "이 세계의 대학생에겐", SER(88), PAPER)
    ctext(d, BW/2, TOP+360, "중국 유학이", SER(140), YELLOW)
    ctext(d, BW/2, TOP+600, "미국 유학만큼", SER(120), PAPER)
    ctext(d, BW/2, TOP+810, "자연스럽습니다", SER(110), PAPER)
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
        UI.title_band(im, "중국 자본을 막아라", "진보의 탄생",
                      (sc["t0"]+t) if si == 0 else 10.0, tag="「자유중국」 EP5",
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
n, rc = NK.encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/jayu_ep5.mp4", seed0=5000, trans=0.20)
print("frames", n, "rc", rc)
