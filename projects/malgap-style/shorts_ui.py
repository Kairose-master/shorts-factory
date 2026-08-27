"""shorts_ui — 한국 Shorts 실측 인터페이스 킷.

레퍼런스: 사용자 제공 스크린샷 2종 (슬라쇼츠TV / 이고바), uploads 보관.
문법: ① 상단 검정 타이틀 밴드(흰 줄 + 노랑 강조줄) ② 하단 노랑-온-블랙 진행 칩
③ 풀블리드 푸티지 ④ 우측 액션바·하단 UI 세이프마진.

애니메이션 규율: remotion-motion-graphics 스킬의 non-negotiable 3규칙을 PIL로 이식 —
선형 보간 금지(전부 ease), 입장은 2–3속성 동시(투명도+이동+스케일), 스태거.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
YELLOW = (255, 228, 0)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
_F = os.path.join(os.path.dirname(__file__), "..", "malgap-ep1", "NotoSansKR-Bold.ttf")
FT = lambda s: ImageFont.truetype(_F, s)

# ---------- easing (선형 금지) ----------
def ease_out_cubic(p): p = min(max(p, 0), 1); return 1 - (1 - p) ** 3
def ease_out_back(p, s=1.4):
    p = min(max(p, 0), 1); p -= 1
    return 1 + p * p * ((s + 1) * p + s)

# ---------- 상단 타이틀 밴드 ----------
def title_band(im, line_w, line_y, t, y0=88, tag="「자유중국」 EP1"):
    """흰 줄 + 노랑 줄, 스태거 0.13s. 입장: 슬라이드다운+페이드+스케일."""
    def line_layer(txt, font, fill, ent):
        e = ease_out_cubic(ent / 0.42)
        a = int(255 * min(1, ent / 0.22)) if ent > 0 else 0
        lay = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.text((W // 2, 10), txt, font=font, fill=fill + (a,),
               stroke_width=10, stroke_fill=(0, 0, 0, a), anchor="ma")
        sc = 0.94 + 0.06 * e
        nw, nh = int(W * sc), int(200 * sc)
        lay = lay.resize((nw, nh))
        dy = int((1 - e) * -46)
        return lay, ((W - nw) // 2, dy)
    band_h = 420
    bh = int(band_h * ease_out_cubic(min(1, max(t, 0)) / 0.38)) if t < 0.38 else band_h
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, 0, W, y0 + bh - 88], fill=(*BLACK, 255))
    if t > 0.05:
        lay, (lx, dy) = line_layer(line_w, FT(92), WHITE, t - 0.05)
        im.paste(lay, (lx, y0 + dy), lay)
    if t > 0.18:
        lay, (lx, dy) = line_layer(line_y, FT(104), YELLOW, t - 0.18)
        im.paste(lay, (lx, y0 + 150 + dy), lay)
    d.text((W - 40, y0 + band_h - 150), tag, font=FT(34),
           fill=(200, 200, 200, 230), anchor="ra")
    return im

# ---------- 하단 진행 칩 ----------
def chip(im, text, ent, y=1430, style="yellow"):
    """노랑-온-블랙 칩(기본) / 흰 박스(이고바형). 입장: 팝(오버슛)+상승+페이드."""
    e = ease_out_back(ent / 0.30)
    a = int(255 * min(1, max(ent, 0) / 0.16))
    size = 58
    f = FT(size)
    pad_x, pad_y = 34, 20
    tmp = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    tw = tmp.textbbox((0, 0), text, font=f)[2]
    while tw > W - 200 and size > 36:          # 화면 폭 초과 방지
        size -= 4; f = FT(size)
        tw = tmp.textbbox((0, 0), text, font=f)[2]
    cw, ch = tw + pad_x * 2, size + pad_y * 2
    lay = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if style == "yellow":
        d.rounded_rectangle([20, 20, 20 + cw, 20 + ch], 16, fill=(0, 0, 0, min(a, 215)))
        d.text((20 + cw // 2, 20 + pad_y - 4), text, font=f, fill=YELLOW + (a,), anchor="ma")
    else:
        d.rounded_rectangle([20, 20, 20 + cw, 20 + ch], 10, fill=(255, 255, 255, min(a, 240)))
        d.text((20 + cw // 2, 20 + pad_y - 4), text, font=f, fill=(15, 15, 15, a), anchor="ma")
    sc = 0.86 + 0.14 * e
    nw, nh = int(lay.width * sc), int(lay.height * sc)
    lay = lay.resize((nw, nh))
    dy = int((1 - ease_out_cubic(min(1, ent / 0.30))) * 34)
    im.paste(lay, ((W - nw) // 2, y + dy - (nh - lay.height) // 2), lay)
    return im

# ---------- 내레이션 → 칩 청크 ----------
def chunks_for(text, dur, max_chars=15):
    """문장을 칩 단위로 쪼개고 글자수 비례로 시간 배분."""
    words = text.replace("…", "…|").replace(". ", ".|").replace(", ", ",|").split("|")
    words = [w.strip() for w in words if w.strip()]
    out, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > max_chars and cur:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    # 쉼표 없는 과장 청크는 중앙 근처 공백에서 한 번 더 쪼갠다(폰트 축소 방지)
    fixed = []
    for c in out:
        while len(c) > max_chars + 8 and " " in c:
            mid = len(c) // 2
            cands = [i for i, ch in enumerate(c) if ch == " "]
            cut = min(cands, key=lambda i: abs(i - mid))
            fixed.append(c[:cut].strip()); c = c[cut:].strip()
        fixed.append(c)
    out = [c for c in fixed if c]
    total = sum(len(c) for c in out) or 1
    sched, t = [], 0.0
    for c in out:
        d = dur * len(c) / total
        sched.append((c, t, d)); t += d
    return sched
