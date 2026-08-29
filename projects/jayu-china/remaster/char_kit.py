"""char_kit — 자유중국 리마스터 v2 일러스트 킷.

레퍼런스(숫자로 보는 역사) 문법의 자체 구현: 둥근 흰 얼굴 + 점 눈 캐릭터,
굵은 외곽선, 저채도 다크 팔레트, 씬 배경. 원작 모사가 아니라 어법 채택 —
캐릭터·배경 조형은 전부 이 파일의 오리지널 드로잉이다.

좌표계: noir_kit 베이스 (BW=1240, BH=2200). 장면 요소 y540~1410 안전 구역.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BW, BH = 1240, 2200
OUT = (26, 22, 19)          # 외곽선
SKIN = (246, 243, 236)      # 얼굴/손
# 의상 팔레트 (저채도)
SUIT_D = (52, 56, 70)       # 짙은 양복
SUIT_B = (74, 92, 120)      # 푸른 양복
SUIT_R = (118, 60, 52)      # 붉은 재킷
UNI_G = (96, 102, 84)       # 군복 그린
WORK_B = (94, 78, 56)       # 작업 점퍼
COAT_G = (120, 106, 74)     # 코트
SHIRT = (222, 216, 202)
TIE_R = (152, 58, 46)
TIE_B = (66, 96, 130)
HAIR = (38, 33, 28)

OW_ = 9  # 기본 외곽선 두께


# ---------- 저수준 ----------
def oell(d, box, fill, w=OW_):
    d.ellipse(box, fill=fill, outline=OUT, width=w)

def orrect(d, box, r, fill, w=OW_):
    d.rounded_rectangle(box, r, fill=fill, outline=OUT, width=w)

def opoly(d, pts, fill, w=OW_):
    d.polygon(pts, fill=fill, outline=OUT, width=w)


# ---------- 얼굴 ----------
def face(d, cx, cy, r, expr="neutral", facing=0):
    """둥근 흰 얼굴. facing: -1 왼쪽, 0 정면, 1 오른쪽 (이목구비 시프트)."""
    oell(d, [cx-r, cy-r, cx+r, cy+r], SKIN, max(7, int(r*0.10)))
    fx = cx + facing * r * 0.18
    er = max(6, int(r * 0.115))
    ey = cy - r*0.06
    dx = r * 0.36
    if expr == "wink":
        d.ellipse([fx-dx-er, ey-er, fx-dx+er, ey+er], fill=OUT)
        d.line([fx+dx-er*1.5, ey, fx+dx+er*1.5, ey], fill=OUT, width=max(5, er-2))
    elif expr == "closed":
        for sx in (-1, 1):
            ex = fx + sx*dx
            d.arc([ex-er*1.8, ey-er*1.2, ex+er*1.8, ey+er*1.4], 25, 155,
                  fill=OUT, width=max(5, er-2))
    else:
        for sx in (-1, 1):
            ex = fx + sx*dx
            d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=OUT)
    mw = r*0.28; my = cy + r*0.46
    lw = max(6, er-1)
    if expr == "smug":
        d.arc([fx-mw*1.2, my-mw*1.4, fx+mw*0.9, my+mw*0.2], 210, 330, fill=OUT, width=lw)
    elif expr == "worried":
        d.arc([fx-mw, my+2, fx+mw, my+mw*1.5], 205, 335, fill=OUT, width=lw)
    elif expr == "shout":
        oell(d, [fx-mw*0.60, my-mw*0.45, fx+mw*0.60, my+mw*0.66], (78, 44, 40), max(4, lw-2))
    elif expr == "surprised":
        oell(d, [fx-mw*0.38, my-mw*0.34, fx+mw*0.38, my+mw*0.44], (78, 44, 40), max(4, lw-2))
    elif expr == "smile":
        d.arc([fx-mw, my-mw*1.2, fx+mw, my+mw*0.3], 20, 160, fill=OUT, width=lw)
    else:
        d.line([fx-mw*0.6, my, fx+mw*0.6, my], fill=OUT, width=lw)


# ---------- 인물 ----------
def person(d, cx, fy, h=430, outfit="suit", expr="neutral", facing=0,
           pose="stand", tie=TIE_R, coat=None, hat=None, arm_raise=0.0,
           reach=None):
    """fy = 발끝 y. h = 전체 키. 머리:몸 ≈ 1:1.35 (SD 비율).

    outfit: suit / suit_b / suit_r / uniform / worker / coat / student
    pose:   stand / point_l / point_r / hands_up / arms_cross / hold_case / wave
    hat:    None / helmet / cap
    """
    col = {"suit": SUIT_D, "suit_b": SUIT_B, "suit_r": SUIT_R, "uniform": UNI_G,
           "worker": WORK_B, "coat": COAT_G, "student": (58, 62, 78)}.get(outfit, SUIT_D)
    if coat: col = coat
    r = h * 0.235                       # 머리 반지름
    bh = h - r*2                        # 몸 높이
    bw2 = h * 0.190                     # 몸 반폭
    ty = fy - bh                        # 어깨(몸 상단) y
    hy = ty - r*0.86                    # 머리 중심 y
    lw = max(8, int(h*0.022))

    # 다리
    leg_c = tuple(int(c*0.62) for c in col)
    d.rectangle([cx-bw2*0.62, fy-bh*0.30, cx-bw2*0.12, fy], fill=leg_c, outline=OUT, width=lw)
    d.rectangle([cx+bw2*0.12, fy-bh*0.30, cx+bw2*0.62, fy], fill=leg_c, outline=OUT, width=lw)
    # 신발
    for sx in (-1, 1):
        x0 = cx + sx*bw2*0.37
        d.ellipse([x0-bw2*0.34, fy-h*0.035, x0+bw2*0.34, fy+h*0.02], fill=OUT)
    # 몸통
    orrect(d, [cx-bw2, ty, cx+bw2, fy-bh*0.24], int(bw2*0.55), col, lw)
    # 셔츠 V + 넥타이 (양복 계열)
    if outfit in ("suit", "suit_b", "suit_r", "student"):
        opoly(d, [(cx-bw2*0.42, ty+lw), (cx+bw2*0.42, ty+lw), (cx, ty+bh*0.30)], SHIRT, max(5, lw-2))
        opoly(d, [(cx-bw2*0.14, ty+bh*0.06), (cx+bw2*0.14, ty+bh*0.06),
                  (cx, ty+bh*0.40)], tie, max(4, lw-3))
    if outfit == "uniform":   # 벨트 + 단추
        d.rectangle([cx-bw2, fy-bh*0.44, cx+bw2, fy-bh*0.36], fill=(48, 44, 36), outline=OUT, width=max(4, lw-3))
        for k in range(3):
            d.ellipse([cx-6, ty+bh*0.10+k*bh*0.09, cx+6, ty+bh*0.10+k*bh*0.09+12], fill=(210, 190, 120))
    if outfit == "worker":
        d.rectangle([cx-bw2, ty+bh*0.16, cx+bw2, ty+bh*0.22], fill=(60, 50, 36), outline=OUT, width=max(4, lw-3))

    # 팔 (외곽선 있는 캡슐)
    hr = max(10, int(h*0.048))          # 손 반지름
    ay = ty + bh*0.16                   # 어깨 관절
    aw = int(h*0.056)
    def arm(sx, ang_deg, ln=bh*0.60):
        a = math.radians(ang_deg)
        sx0, sy0 = cx + sx*bw2*0.78, ay
        ex_, ey_ = sx0 + sx*math.cos(a)*ln, ay + math.sin(a)*ln
        d.line([sx0, sy0, ex_, ey_], fill=OUT, width=aw+2*max(4, lw-3))
        d.line([sx0, sy0, ex_, ey_], fill=col, width=aw)
        oell(d, [ex_-hr, ey_-hr, ex_+hr, ey_+hr], SKIN, max(5, lw-2))
        return ex_, ey_
    hands = {}
    if pose == "stand":
        hands["l"] = arm(-1, 76); hands["r"] = arm(1, 76)
    elif pose == "point_r":
        hands["l"] = arm(-1, 78); hands["r"] = arm(1, -35 - 20*arm_raise, bh*0.70)
    elif pose == "point_l":
        hands["r"] = arm(1, 78); hands["l"] = arm(-1, -35 - 20*arm_raise, bh*0.70)
    elif pose == "hands_up":
        hands["l"] = arm(-1, -58, bh*0.64); hands["r"] = arm(1, -58, bh*0.64)
    elif pose == "wave":
        hands["l"] = arm(-1, 76); hands["r"] = arm(1, -66, bh*0.58)
    elif pose == "arms_cross":
        for sx in (-1, 1):
            x0, y0 = cx + sx*bw2*0.78, ay
            x1, y1 = cx - sx*bw2*0.40, ay + bh*0.26
            d.line([x0, y0, x1, y1], fill=OUT, width=aw+2*max(4, lw-3))
            d.line([x0, y0, x1, y1], fill=col, width=aw)
        for sx in (-1, 1):
            x1, y1 = cx - sx*bw2*0.40, ay + bh*0.26
            oell(d, [x1-hr, y1-hr, x1+hr, y1+hr], SKIN, max(5, lw-2))
    elif pose == "hold_case":
        hands["l"] = arm(-1, 76)
        ex_, ey_ = arm(1, 70); hands["r"] = (ex_, ey_)
        orrect(d, [ex_-h*0.11, ey_+hr*0.6, ex_+h*0.11, ey_+hr*0.6+h*0.14], 10, (76, 60, 42), max(5, lw-2))
    elif pose == "reach_r":     # 오른쪽으로 손 내밀기 (악수). reach=(x,y)면 그 점까지
        hands["l"] = arm(-1, 78)
        if reach:
            sx0 = cx + bw2*0.78
            ang = math.degrees(math.atan2(reach[1]-ay, reach[0]-sx0))
            hands["r"] = arm(1, ang, math.hypot(reach[0]-sx0, reach[1]-ay))
        else:
            hands["r"] = arm(1, 6, bh*0.66)
    elif pose == "reach_l":
        hands["r"] = arm(1, 78)
        if reach:
            sx0 = cx - bw2*0.78
            ang = math.degrees(math.atan2(reach[1]-ay, sx0-reach[0]))
            hands["l"] = arm(-1, ang, math.hypot(reach[0]-sx0, reach[1]-ay))
        else:
            hands["l"] = arm(-1, 6, bh*0.66)
    elif pose == "hold_sign":   # 피켓 들기 (양손 위)
        hands["l"] = arm(-1, -74, bh*0.55); hands["r"] = arm(1, -74, bh*0.55)

    # 머리
    face(d, cx, hy, r, expr=expr, facing=facing)
    if hat == "helmet":
        d.pieslice([cx-r*1.08, hy-r*1.30, cx+r*1.08, hy+r*0.30], 180, 360,
                   fill=(76, 80, 68), outline=OUT, width=lw)
        d.rounded_rectangle([cx-r*1.14, hy-r*0.56, cx+r*1.14, hy-r*0.36], 10,
                            fill=(76, 80, 68), outline=OUT, width=max(4, lw-3))
    elif hat == "cap":
        d.pieslice([cx-r*1.0, hy-r*1.26, cx+r*1.0, hy+r*0.24], 180, 360,
                   fill=(54, 58, 72), outline=OUT, width=lw)
        bx0, bx1 = (cx, cx+r*1.42) if facing >= 0 else (cx-r*1.42, cx)
        d.rounded_rectangle([bx0, hy-r*0.62, bx1, hy-r*0.42], 8,
                            fill=(54, 58, 72), outline=OUT, width=max(4, lw-3))
    elif hat != "none":  # 기본 머리카락: 이마 위 캡 (눈 위에서 끝남)
        d.pieslice([cx-r*0.99, hy-r*1.0, cx+r*0.99, hy+r*0.16], 180, 360, fill=HAIR)
    return hands


# ---------- 배경 ----------
def sky(top=(22, 26, 38), bot=(48, 52, 66), hor=1340):
    """그라데이션 하늘 + 지면. hor = 지평선 y."""
    g = np.linspace(0, 1, hor)[:, None]
    arr = (np.array(top)[None, None, :]*(1-g[..., None]) +
           np.array(bot)[None, None, :]*g[..., None]).astype(np.uint8)
    a = np.zeros((BH, BW, 3), np.uint8)
    a[:hor] = np.repeat(arr, BW, axis=1)
    a[hor:] = (34, 32, 34)
    return Image.fromarray(a)


def ground_line(d, hor=1340, col=(58, 54, 52)):
    d.rectangle([0, hor, BW, hor+16], fill=col)


def building(d, x0, y0, x1, hor, col=(46, 50, 62), win=(96, 92, 70), arch=False):
    d.rectangle([x0, y0, x1, hor], fill=col, outline=OUT, width=8)
    d.rectangle([x0, y0, x1, y0+26], fill=tuple(int(c*0.7) for c in col), outline=OUT, width=6)
    step = 74
    wy = y0 + 60
    while wy < hor - 90:
        wx = x0 + 34
        while wx < x1 - 60:
            if arch:
                d.pieslice([wx, wy, wx+40, wy+62], 180, 360, fill=win)
                d.rectangle([wx, wy+30, wx+40, wy+56], fill=win)
            else:
                d.rectangle([wx, wy, wx+40, wy+50], fill=win)
            wx += step
        wy += step + 26
    return


def skyline(d, hor=1340, seed=0, y_min=640):
    rng = np.random.default_rng(seed)
    x = -40
    while x < BW:
        w = int(rng.integers(150, 320))
        y0 = int(rng.integers(y_min, max(y_min+40, hor-320)))
        building(d, x, y0, x+w, hor,
                 col=(int(40+rng.integers(0, 14)), int(44+rng.integers(0, 14)), int(56+rng.integers(0, 12))))
        x += w - 18


def forest(d, hor=1340, seed=1, col=(36, 48, 38)):
    rng = np.random.default_rng(seed)
    x = -60
    while x < BW + 60:
        h = int(rng.integers(360, 660)); w = int(rng.integers(150, 240))
        y0 = hor - h
        for k in range(3):
            yy = y0 + k*h*0.28
            opoly(d, [(x, yy+h*0.42), (x+w/2, yy), (x+w, yy+h*0.42)],
                  tuple(int(c*(1-0.08*k)) for c in col), 7)
        d.rectangle([x+w/2-16, hor-40, x+w/2+16, hor], fill=(50, 40, 30), outline=OUT, width=5)
        x += int(w*0.8)


def cloudband(d, y, w=520, col=(60, 64, 80)):
    for k, (dx, r) in enumerate([(-w*0.3, 90), (0, 120), (w*0.3, 84)]):
        d.ellipse([BW/2+dx-r, y-r*0.6, BW/2+dx+r, y+r*0.6], fill=col)


# ---------- 소품 ----------
def train(d, x, y, s=1.0, col=(70, 76, 92), accent=(232, 163, 61), cars=2):
    """측면 열차, 오른쪽 진행. x = 기관차 앞코, y = 레일 윗면, s = 스케일."""
    ch, cw = 170*s, 360*s
    lw = max(6, int(8*s))
    # 레일 + 침목
    x_tail = x - cw*(cars+1.4)
    for tx in np.arange(x_tail, x+200*s, 66*s):
        d.line([tx, y+8*s, tx, y+30*s], fill=(96, 80, 46), width=int(10*s))
    d.line([x_tail, y+8*s, x+200*s, y+8*s], fill=(120, 104, 62), width=int(12*s))
    # 객차 (기관차 뒤로)
    for k in range(int(cars)):
        x1 = x - cw*1.06 - k*(cw+18*s)
        orrect(d, [x1-cw, y-ch, x1, y-16*s], int(20*s), col, lw)
        for wx in np.linspace(x1-cw+64*s, x1-64*s, 3):
            d.rounded_rectangle([wx-34*s, y-ch+28*s, wx+34*s, y-ch+82*s], int(8*s),
                                fill=(186, 190, 176), outline=OUT, width=max(4, lw-3))
        for wx in (x1-cw+76*s, x1-76*s):
            oell(d, [wx-28*s, y-42*s, wx+28*s, y+14*s], (42, 42, 46), max(4, lw-2))
    # 기관차: 앞코가 오른쪽(x)
    body = [(x-cw, y-16*s), (x-cw, y-ch*1.06), (x-90*s, y-ch*1.06),
            (x, y-ch*0.62), (x, y-16*s)]
    opoly(d, body, accent, lw)
    d.rounded_rectangle([x-cw*0.94, y-ch*0.98, x-cw*0.60, y-ch*0.54], int(8*s),
                        fill=(186, 190, 176), outline=OUT, width=max(4, lw-3))
    d.ellipse([x-30*s, y-ch*0.52, x-6*s, y-ch*0.36], fill=(255, 232, 160), outline=OUT, width=max(3, lw-4))
    for wx in (x-cw*0.72, x-cw*0.24):
        oell(d, [wx-30*s, y-44*s, wx+30*s, y+14*s], (42, 42, 46), max(4, lw-2))
    d.rectangle([x-cw*0.52, y-ch*1.28, x-cw*0.38, y-ch*1.02], fill=(70, 74, 84), outline=OUT, width=max(4, lw-3))


def ship(d, cx, wl, s=1.0, col=(64, 70, 84)):
    """화물선. wl = 흘수선 y."""
    opoly(d, [(cx-330*s, wl-90*s), (cx+330*s, wl-90*s), (cx+270*s, wl+40*s), (cx-270*s, wl+40*s)], col)
    d.rectangle([cx+90*s, wl-200*s, cx+230*s, wl-90*s], fill=(96, 100, 112), outline=OUT, width=7)
    d.rectangle([cx+130*s, wl-260*s, cx+190*s, wl-200*s], fill=(96, 100, 112), outline=OUT, width=6)
    for k in range(3):
        d.rectangle([cx-280*s+k*130*s, wl-150*s, cx-170*s+k*130*s, wl-90*s],
                    fill=[(120, 96, 44), (91, 104, 123), (140, 70, 52)][k], outline=OUT, width=6)


def crane(d, x, gy, s=1.0, col=(108, 112, 126), dir=1):
    """게이트형 타워 + 지브. dir=1 오른쪽으로 지브, -1 왼쪽."""
    for sx in (-1, 1):
        d.line([(x+sx*70*s, gy), (x+sx*40*s, gy-540*s)], fill=OUT, width=int(30*s))
        d.line([(x+sx*70*s, gy), (x+sx*40*s, gy-540*s)], fill=col, width=int(20*s))
    d.line([(x-40*s, gy-540*s), (x+40*s, gy-540*s)], fill=col, width=int(22*s))
    j0, j1 = x - dir*160*s, x + dir*360*s
    d.line([(j0, gy-500*s), (j1, gy-570*s)], fill=OUT, width=int(26*s))
    d.line([(j0, gy-500*s), (j1, gy-570*s)], fill=col, width=int(16*s))
    tx = x + dir*270*s
    d.line([(tx, gy-552*s), (tx, gy-330*s)], fill=col, width=int(9*s))
    orrect(d, [tx-60*s, gy-330*s, tx+60*s, gy-250*s], 8, (120, 96, 44), 7)


def containers(d, x, gy, s=1.0):
    for i, c in enumerate([(120, 96, 44), (91, 104, 123), (140, 70, 52)]):
        orrect(d, [x+i*210*s, gy-90*s, x+i*210*s+190*s, gy], 6, c, 7)
    orrect(d, [x+105*s, gy-180*s, x+295*s, gy-96*s], 6, (100, 84, 60), 7)


def ballot_box(d, cx, gy, s=1.0, col=(74, 66, 54), slot=True, mark="票"):
    orrect(d, [cx-170*s, gy-260*s, cx+170*s, gy], int(16*s), col, 9)
    d.polygon([(cx-170*s, gy-260*s), (cx-130*s, gy-320*s), (cx+130*s, gy-320*s), (cx+170*s, gy-260*s)],
              fill=tuple(int(c*0.8) for c in col), outline=OUT, width=8)
    if slot:
        d.rectangle([cx-70*s, gy-306*s, cx+70*s, gy-288*s], fill=OUT)


def paper(d, cx, cy, w, h, rot=0, col=(236, 230, 216)):
    p = Image.new("RGBA", (int(w+40), int(h+40)), (0, 0, 0, 0))
    pd = ImageDraw.Draw(p)
    pd.rectangle([20, 20, w+20, h+20], fill=col, outline=OUT, width=7)
    return p.rotate(rot, expand=True, resample=Image.BICUBIC), pd


def flagpole(d, x, gy, fh, fw, col, s=1.0):
    """fw 양수 = 오른쪽으로 펄럭, 음수 = 왼쪽."""
    d.line([(x, gy), (x, gy-fh)], fill=(120, 116, 108), width=int(12*s))
    d.ellipse([x-10, gy-fh-14, x+10, gy-fh+6], fill=(180, 170, 140))
    hh = abs(fw)*0.62
    opoly(d, [(x, gy-fh+8), (x+fw, gy-fh+8+hh*0.10), (x+fw, gy-fh+8+hh*0.90),
              (x, gy-fh+8+hh)], col, 7)


def smoke(d, x, y, s=1.0, col=(84, 88, 100)):
    for k, (dx, dy, r) in enumerate([(0, 0, 46), (34, -60, 60), (86, -130, 78)]):
        d.ellipse([x+dx*s-r*s, y+dy*s-r*s, x+dx*s+r*s, y+dy*s+r*s], fill=col)


def picket(d, cx, top_y, w, h2, txt_draw=None, col=(232, 226, 212), pole_to=None):
    """피켓. txt_draw(d, cx, cy) 콜백으로 문구를 그린다."""
    if pole_to:
        d.line([cx, top_y+h2, cx, pole_to], fill=(120, 108, 84), width=14)
    orrect(d, [cx-w/2, top_y, cx+w/2, top_y+h2], 14, col, 9)
    if txt_draw:
        txt_draw(d, cx, top_y + h2/2)


def bridge(d, x0, x1, deck_y, s=1.0, col=(84, 78, 70)):
    """트러스 다리 (강 위 철교)."""
    d.rectangle([x0, deck_y, x1, deck_y+26*s], fill=col, outline=OUT, width=7)
    n = max(3, int((x1-x0)/(190*s)))
    step = (x1-x0)/n
    for k in range(n):
        ax = x0 + k*step
        d.line([ax, deck_y, ax+step/2, deck_y-120*s], fill=col, width=int(14*s))
        d.line([ax+step/2, deck_y-120*s, ax+step, deck_y], fill=col, width=int(14*s))
    d.line([x0, deck_y-120*s, x1, deck_y-120*s], fill=col, width=int(12*s))
    for k in range(n+1):
        d.line([x0+k*step, deck_y+26*s, x0+k*step, deck_y+90*s], fill=col, width=int(16*s))


def anchor_1946(SER, SAN, ctext, night):
    """시리즈 앵커: 1946 갈림길 — v2 일러스트판 (전 EP 공유, 코드 동일 유지)."""
    im = sky(top=(18, 22, 32), bot=(46, 50, 62), hor=1020)
    d = ImageDraw.Draw(im)
    forest(d, hor=1020, seed=46, col=(30, 40, 34))
    d.rectangle([0, 1020, BW, BH], fill=(40, 38, 40))
    ground_line(d, 1020)
    cx, jy = BW/2, 1420
    # 분기 선로: 지면 위, 아래에서 갈라져 지평선으로
    def track(p0, p1, col, w):
        d.line([p0, p1], fill=OUT, width=w+10)
        d.line([p0, p1], fill=col, width=w)
    for t in np.linspace(0.06, 0.94, 8):     # 침목 (줄기)
        yy = 1900 - (1900-jy)*t
        ww = 90 - 34*t
        d.line([cx-ww, yy, cx+ww, yy], fill=(96, 80, 46), width=12)
    track((cx, 1900), (cx, jy), (120, 124, 138), 18)
    track((cx, jy), (cx-330, 1075), (76, 80, 94), 12)
    track((cx, jy), (cx+330, 1075), (232, 163, 61), 16)
    d.ellipse([cx-28, jy-28, cx+28, jy+28], fill=(246, 243, 236), outline=OUT, width=9)
    # 표지판
    ctext(d, cx-340, 1130, "공산당", SAN(46), (124, 128, 140), 4, OUT)
    ctext(d, cx+340, 1100, "국민당 승리", SAN(54), (232, 163, 61), 4, OUT)
    ctext(d, BW/2, 700, "1946", SER(170), (246, 243, 236), 8, OUT)
    return im


# ---------- 프레임-인-프레임 ----------
def frame_in_frame(scene, pad_x=90, top=520, bot=1500):
    """scene(BW×BH 일부)을 카드로 앉히고 뒤에 블러 확대판을 깐다."""
    bg = scene.resize((BW//3, BH//3)).resize((BW, BH)).filter(ImageFilter.GaussianBlur(22))
    bg = Image.eval(bg, lambda v: int(v*0.55))
    card = scene.crop((0, top, BW, bot))
    cw = BW - pad_x*2
    ch = int(card.height * cw / card.width)
    card = card.resize((cw, ch), Image.LANCZOS)
    y0 = top + 40
    d = ImageDraw.Draw(bg)
    d.rectangle([pad_x-14, y0-14, pad_x+cw+14, y0+ch+14], fill=(14, 13, 12))
    bg.paste(card, (pad_x, y0))
    return bg
