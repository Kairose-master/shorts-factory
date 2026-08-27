#!/usr/bin/env python3
"""「기준선」 — 구독자 대비 정상 조회수. Tier A: 코드로만 그린 한국어 숏폼.

plan.json (실측 내레이션 + 단어 경계)을 읽어 silent.mp4를 쓴다.
자막은 9/9 채널이 전부 번인이라 필수 요소로 취급한다 (research §4 발견 1).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SK = ROOT.parents[1] / ".claude" / "skills" / "motion-graphics" / "scripts"
sys.path.insert(0, str(SK))

import captions  # noqa: E402
import fonts  # noqa: E402
import mg  # noqa: E402

# --- 다크 그레이드. 악센트는 오직 '배수'에만 쓴다 ------------------------------
BG, FG, MUTED, ACC = (16, 20, 24), (240, 237, 230), (138, 143, 150), (229, 179, 61)
mg.PAPER, mg.INK, mg.MUTED, mg.ACCENT = BG, FG, MUTED, ACC
mg.FONT_FILES["kr"] = fonts.korean(400)
mg.FONT_FILES["kr-bold"] = fonts.korean(700)
mg.FONT_FILES["kr-black"] = fonts.korean(900)

L, R = mg.SAFE["l"], mg.SAFE["r"]
COL = R - L
CAP_Y = 1276

PLAN = json.loads((ROOT / "plan.json").read_text(encoding="utf-8"))
S = {s["id"]: s for s in PLAN["scenes"]}
TOTAL = PLAN["duration"]

# 실측값 — research/kr-9channels-production-2026-08-27/report.md §1
# 채널명은 화면에 쓰지 않는다: 발견은 분포에 관한 것이고, 특정 채널을 지목할
# 이유가 없다. (한 채널은 성인물 인접이라 노출 자체가 브랜드 리스크다.)
RATIOS = [11.16, 1.06, 0.37, 0.29, 0.25, 0.23, 0.13, 0.06, 0.04]
RECENT365 = [50, 64, 61, 2, 6, 0, 36, 16, 2]


def at(sid, i):
    ws = S[sid]["words"]
    return S[sid]["start"] + ws[min(i, len(ws) - 1)]["t"]


def kf(size, w="kr-bold"):
    return mg.font(w, size)


def fade(d, xy, text, fnt, p, base=FG, align="left", right=R):
    if p <= 0:
        return
    x, y = xy
    if align == "center":
        x = x + (right - x - d.textlength(text, font=fnt)) / 2
    elif align == "right":
        x = right - d.textlength(text, font=fnt)
    d.text((x, y), text, font=fnt, fill=mg.mix(BG, base, p))


def rise(d, xy, text, fnt, p, base=FG, dist=30, align="left"):
    fade(d, (xy[0], xy[1] + int(dist * (1 - p))), text, fnt, p, base, align)


def chrome(d, t):
    f = mg.font("mono", 26)
    d.text((L, 150), "「기준선」  No.1", font=kf(34), fill=MUTED)
    d.text((R - d.textlength("n=550 shorts · 9 channels", font=f), 154),
           "n=550 shorts · 9 channels", font=f, fill=MUTED)
    d.line([(L, 206), (R, 206)], fill=mg.mix(BG, MUTED, 0.4), width=2)
    mg.rule(d, 206, L, R, ACC, 4, t / TOTAL)


# --------------------------------------------------------------------------
def s1(d, im, t):
    rise(d, (L, 400), "구독자 99만 채널", kf(52, "kr"), mg.seg(t, at("s1", 0), 0.4), MUTED)
    p = mg.seg(t, at("s1", 4), 0.5)
    rise(d, (L, 486), "숏츠 한 편 조회수", kf(60), p)
    fade(d, (L, 590), mg.counter(0, 1100, mg.seg(t, at("s1", 6), 0.9), "{:,.0f}만"),
         kf(150, "kr-black"), mg.seg(t, at("s1", 6), 0.3), ACC)
    q = mg.seg(t, at("s1", 11), 0.5)
    mg.rule(d, 830, L, R, MUTED, 3, q)
    rise(d, (L, 872), "정상은 몇 배일까요?", kf(74), q)


def s2(d, im, t):
    rise(d, (L, 430), "한국 숏폼 채널", kf(56, "kr"), mg.seg(t, at("s2", 0), 0.4), MUTED)
    fade(d, (L, 520), mg.counter(0, 9, mg.seg(t, at("s2", 2), 0.8), "{:.0f}개"),
         kf(120, "kr-black"), mg.seg(t, at("s2", 2), 0.3))
    rise(d, (L, 720), "숏츠", kf(56, "kr"), mg.seg(t, at("s2", 4), 0.4), MUTED)
    fade(d, (L, 800), mg.counter(0, 550, mg.seg(t, at("s2", 4), 1.0), "{:,.0f}편"),
         kf(120, "kr-black"), mg.seg(t, at("s2", 4), 0.3), ACC)
    rise(d, (L, 980), "2026-08-27 · 전수 집계", mg.font("mono", 32),
         mg.seg(t, at("s2", 6), 0.4), MUTED)


def s3(d, im, t):
    rise(d, (L, 420), "기준은 조회수가 아닙니다", kf(58), mg.seg(t, at("s3", 0), 0.4), MUTED)
    p = mg.seg(t, at("s3", 3), 0.5)
    if p > 0:
        mg.panel(d, (L, 560, R, 900), None, 18, mg.mix(BG, MUTED, p * 0.8), 3)
        fade(d, (L, 620), "중앙값", kf(84), p, FG, "center")
        mg.rule(d, 730, L + 180, R - 180, ACC, 5, mg.seg(t, at("s3", 3) + 0.25, 0.4))
        fade(d, (L, 760), "구독자 수", kf(84), mg.seg(t, at("s3", 4), 0.45), FG, "center")
    fade(d, (L, 950), "절대 조회수는 채널 크기만 말해 준다", kf(40, "kr"),
         mg.seg(t, at("s3", 5), 0.4), MUTED, "center")


def s4(d, im, t):
    rise(d, (L, 400), "아홉 채널, 중앙값 ÷ 구독자", kf(52), mg.seg(t, at("s4", 0), 0.4), MUTED)
    base, w, gap = 1090, 84, 26
    x0 = (mg.W - (9 * w + 8 * gap)) / 2
    hi = 520.0
    for k, r in enumerate(RATIOS):
        p = mg.seg(t, at("s4", 0) + 0.15 + k * 0.06, 0.4)
        if p <= 0:
            continue
        h = max(3, (min(r, 2.0) / 2.0) * hi * mg.ease_out(p))
        col = ACC if r >= 1.0 else mg.mix(BG, FG, 0.55)
        x = x0 + k * (w + gap)
        d.rounded_rectangle((x, base - h, x + w, base), radius=6,
                            fill=mg.mix(BG, col, p))
    line_p = mg.seg(t, at("s4", 2), 0.6)
    if line_p > 0:
        y = base - (0.4 / 2.0) * hi
        mg.rule(d, y, L, R, (229, 90, 70), 3, line_p)
        fade(d, (L, y - 52), "0.4배", kf(32, "kr"), line_p, (229, 90, 70), "right")
    fade(d, (L, 1140), "일곱 개가 이 선 아래", kf(52), mg.seg(t, at("s4", 4), 0.45),
         FG, "center")


def s5(d, im, t):
    rise(d, (L, 400), "1위", kf(50, "kr"), mg.seg(t, at("s5", 0), 0.4), MUTED)
    fade(d, (L, 470), mg.counter(0, 11.16, mg.seg(t, at("s5", 1), 0.9), "{:.2f}배"),
         kf(160, "kr-black"), mg.seg(t, at("s5", 1), 0.3), ACC)
    fade(d, (L, 660), "중앙값이 구독자 수의 11배", kf(42, "kr"),
         mg.seg(t, at("s5", 1) + 0.5, 0.4), MUTED)

    p = mg.seg(t, at("s5", 4), 0.5)   # "그런데 최고 기록도"
    if p > 0:
        mg.rule(d, 780, L, R, MUTED, 2, p)
        fade(d, (L, 820), "그 채널의 최고 기록", kf(46, "kr"), p, MUTED)
        fade(d, (L, 890), mg.counter(0, 3.5, mg.seg(t, at("s5", 6), 0.9), "{:.1f}배"),
             kf(120, "kr-black"), mg.seg(t, at("s5", 6), 0.3), FG)
    fade(d, (L, 1080), "천장이 낮은 게 아니라, 바닥이 없다", kf(50),
         mg.seg(t, at("s5", 9), 0.45), ACC)


def s6(d, im, t):
    rise(d, (L, 400), "최근 365일 발행 편수", kf(52), mg.seg(t, at("s6", 0), 0.4), MUTED)
    cell, gapx, top = 250, 30, 520
    x0 = (mg.W - (3 * cell + 2 * gapx)) / 2
    for k, n in enumerate(RECENT365):
        p = mg.seg(t, at("s6", 0) + 0.2 + k * 0.05, 0.35)
        if p <= 0:
            continue
        cx, cy = x0 + (k % 3) * (cell + gapx), top + (k // 3) * 168
        dead = n <= 2
        col = mg.mix(BG, (229, 90, 70) if dead else FG, p)
        d.rounded_rectangle((cx, cy, cx + cell, cy + 140), radius=12,
                            outline=col, width=3)
        txt = f"{n}편"
        d.text((cx + (cell - d.textlength(txt, font=kf(64))) / 2, cy + 34),
               txt, font=kf(64), fill=col)
    fade(d, (L, 1040), "셋은 사실상 멈췄다", kf(56), mg.seg(t, at("s6", 2), 0.45),
         FG, "center")
    # 사실을 담은 숫자는 굴리지 않는다 — 굴러가는 중간값이 스크린샷으로 남는다
    fade(d, (L, 1130), "한 채널은 915일째", kf(46, "kr"),
         mg.seg(t, at("s6", 6), 0.4), (229, 90, 70), "center")


def s7(d, im, t):
    f = kf(72)
    for k, ln in enumerate(mg.wrap(d, "당신 채널의 중앙값을 구독자 수로 나눠 보세요", f, COL)):
        rise(d, (L, 560 + k * 100), ln, f, mg.seg(t, at("s7", 0) + k * 0.16, 0.4))
    fade(d, (L, 880), "그게 진짜 성적표입니다", kf(60), mg.seg(t, at("s7", 4), 0.45), ACC)
    mg.rule(d, 990, L, R, ACC, 6, mg.seg(t, TOTAL - 1.2, 1.1, mg.ease_in_out))


DRAW = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}


def build():
    """Caption cards are grouped once, and sized to the LONGEST card, not the mean."""
    from PIL import Image, ImageDraw
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    cards = []
    for s in PLAN["scenes"]:
        for c in captions.chunk(s["words"], max_chars=18):
            cards.append({**c, "start": c["start"] + s["start"],
                          "end": c["end"] + s["start"],
                          "words": [{**w, "t": w["t"] + s["start"]} for w in c["words"]]})
    cap_font = captions.fit(probe, cards, lambda n: kf(n), COL - 40, start=62, min_size=40)
    print(f"  {len(cards)} caption cards, font {cap_font.size}px")
    return cards


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "silent.mp4"))
    args = ap.parse_args()
    cards = build()
    cap_font = captions.fit(
        __import__("PIL.ImageDraw", fromlist=["ImageDraw"]).Draw(
            __import__("PIL.Image", fromlist=["Image"]).new("RGB", (8, 8))),
        cards, lambda n: kf(n), COL - 40, start=62, min_size=40)

    def frame(t, i):
        im, d = mg.canvas(BG)
        chrome(d, t)
        for s in PLAN["scenes"]:
            if s["start"] <= t < s["start"] + s["dur"] or (
                    s is PLAN["scenes"][-1] and t >= s["start"]):
                DRAW[s["id"]](d, im, t)
                break
        captions.draw(d, cards, t, cap_font, CAP_Y, L, R,
                      fill=FG, highlight=ACC, shadow=(0, 0, 0), stroke=7)
        return im

    mg.render(frame, TOTAL, args.out, fps=PLAN["fps"], w=PLAN["width"],
              h=PLAN["height"], progress_every=240)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
