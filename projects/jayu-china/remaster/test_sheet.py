"""char_kit QC 시트 — 캐릭터/배경/소품을 한 판에 렌더해 육안 검수."""
import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from char_kit import *
from PIL import Image, ImageDraw

OUTDIR = os.environ.get("QC_DIR", "/tmp/claude-0/-home-user-shorts-factory/04e8794f-bef2-5453-bd65-87d24bd25753/scratchpad")

# 판 1: 캐릭터 라인업
im = sky(hor=1500)
d = ImageDraw.Draw(im)
ground_line(d, 1500)
specs = [
    ("suit", "smug", "stand", None, TIE_R),
    ("suit_b", "neutral", "point_r", None, TIE_B),
    ("uniform", "neutral", "stand", "helmet", TIE_R),
    ("worker", "worried", "hold_case", "cap", TIE_R),
    ("student", "surprised", "hands_up", None, TIE_B),
    ("coat", "closed", "arms_cross", None, TIE_R),
]
for i, (o, e, p, h, t) in enumerate(specs):
    x = 160 + (i % 3) * 380
    y = 1000 if i < 3 else 1500
    person(d, x, y, h=430, outfit=o, expr=e, pose=p, hat=h, tie=t,
           facing=(-1 if i % 3 == 2 else (1 if i % 3 == 0 else 0)))
im.save(f"{OUTDIR}/ck_chars.png")

# 판 2: 씬 조합 — 압록강 보급 열차 (EP4 s4 후보)
im2 = sky(hor=1400, top=(20, 24, 34), bot=(52, 56, 68))
d2 = ImageDraw.Draw(im2)
forest(d2, hor=1400, seed=4, col=(34, 46, 40))
ground_line(d2, 1400)
train(d2, 950, 1330, s=1.0, cars=2)
smoke(d2, 900, 1120)
person(d2, 260, 1660, h=400, outfit="uniform", expr="smug", pose="point_r",
       hat="helmet", facing=1)
person(d2, 480, 1680, h=380, outfit="uniform", expr="surprised", pose="stand",
       hat="helmet", facing=-1)
im2.save(f"{OUTDIR}/ck_scene_train.png")

# 판 3: 항만 (EP4 s7 후보)
im3 = sky(hor=1300, top=(24, 28, 40), bot=(58, 60, 72))
d3 = ImageDraw.Draw(im3)
ship(d3, 950, 1120, s=0.9)
d3.rectangle([0, 1300, BW, BH], fill=(44, 42, 44))
d3.rectangle([0, 1290, BW, 1310], fill=(60, 64, 78))
crane(d3, 830, 1290, s=1.0)
containers(d3, 120, 1290, s=1.0)
person(d3, 380, 1620, h=430, outfit="suit", expr="smug", pose="point_r", facing=1)
im3.save(f"{OUTDIR}/ck_scene_harbor.png")

# 판 4: 프레임-인-프레임
fif = frame_in_frame(im2)
fif.save(f"{OUTDIR}/ck_fif.png")
print("saved 4 sheets")
