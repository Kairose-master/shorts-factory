"""EXP-E05 — 극장 실루엣 템플릿을 예배당 회중 실루엣으로 바꾼 오버레이 생성.
투명 배경 PNG. build_short_boxed.py의 박스 렌더 위에 얹는다.
"""
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(7)
W, H = 1080, 1920
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

BLACK = (8, 10, 14, 255)

# ── 회중 뒷모습 실루엣 밴드 (스크린 아래, 화면 최하단)
band_top = 1600
head_row_y = 1660
chair_row_y = 1760

# 의자 등받이 줄 — 가로로 촘촘하게, 높이를 살짝 흔들어 기계적으로 보이지 않게
x = -20
while x < W + 20:
    w = random.randint(46, 62)
    h = random.randint(150, 190)
    top = H - h
    draw.rounded_rectangle([x, top, x + w - 6, H + 20], radius=14, fill=BLACK)
    x += w

# 사람 머리·어깨 실루엣 — 의자 사이사이, 손 든 사람 몇 명 섞기
positions = list(range(20, W - 20, 58))
random.shuffle(positions)
raised_hand_idxs = set(random.sample(range(len(positions)), k=max(3, len(positions) // 5)))

for i, cx in enumerate(sorted(positions)):
    head_r = random.randint(20, 26)
    shoulder_w = random.randint(60, 78)
    shoulder_h = random.randint(90, 120)
    head_cy = head_row_y + random.randint(-14, 10)
    # 머리
    draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=BLACK)
    # 어깨(사다리꼴 근사 — 둥근 사각형)
    sh_top = head_cy + head_r - 6
    draw.rounded_rectangle(
        [cx - shoulder_w // 2, sh_top, cx + shoulder_w // 2, sh_top + shoulder_h],
        radius=22, fill=BLACK)
    # 손 든 사람 — 팔 두 개를 위로
    if i in raised_hand_idxs:
        arm_top = head_cy - head_r - random.randint(70, 110)
        for dx in (-1, 1):
            ax = cx + dx * random.randint(10, 18)
            draw.line([ax, sh_top + 10, ax + dx * 8, arm_top], fill=BLACK, width=13)
            # 손끝 살짝 벌어진 손가락 느낌
            draw.line([ax + dx * 8, arm_top, ax + dx * 8 - 6, arm_top - 14], fill=BLACK, width=8)
            draw.line([ax + dx * 8, arm_top, ax + dx * 8 + 10, arm_top - 10], fill=BLACK, width=8)

# 부드러운 하단 비네트(암전된 예배당 느낌) — 실루엣 위에 살짝 덮는 대신
# 화면 최하단만 완전 암전되도록 그라디언트
vignette = Image.new("L", (1, H), 0)
for y in range(H):
    if y < 1500:
        a = 0
    else:
        a = int(255 * min(1.0, (y - 1500) / (H - 1500)) ** 1.6)
    vignette.putpixel((0, y), a)
vignette = vignette.resize((W, H))
black_layer = Image.new("RGBA", (W, H), (5, 8, 12, 255))
img = Image.alpha_composite(img, Image.composite(black_layer, Image.new("RGBA", (W, H), (0, 0, 0, 0)), vignette))

img = img.filter(ImageFilter.GaussianBlur(0.6))  # 실루엣 가장자리 살짝 부드럽게

if __name__ == "__main__":
    import sys
    from pathlib import Path
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("congregation-silhouette.png")
    img.save(out)
    print("saved", img.size, "->", out)
