"""「말값」 No.6 시즌 한정 — 로맨툰 캐릭터 엔진: 다혜·정사장 대화극의 노이르 귀환."""
import sys, os, json, math
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{ROOT}/../malgap-style")
from noir_kit import *
from PIL import Image, ImageDraw

def tag(d, fg=PAPER): d.text((84, 120), "「말값」 No.6", font=SAN(44), fill=fg)

def dahye(d, px, gy, h=430):
    col = (12, 15, 24); top = gy-h
    d.ellipse([px-64, top, px+64, top+128], fill=col)
    d.pieslice([px-72, top-10, px+72, top+120], 180, 360, fill=(30, 24, 20))   # 단발 실루엣
    d.ellipse([px-74, top+40, px-38, top+150], fill=(30, 24, 20))
    d.ellipse([px+38, top+40, px+74, top+150], fill=(30, 24, 20))
    d.rounded_rectangle([px-84, top+140, px+84, gy], 40, fill=(38, 50, 66))

def sajang(d, px, gy, h=450):
    col = (12, 15, 24); top = gy-h
    d.ellipse([px-66, top, px+66, top+132], fill=col)
    d.pieslice([px-70, top-8, px+70, top+80], 180, 360, fill=(40, 38, 34))
    d.rounded_rectangle([px-92, top+142, px+92, gy], 40, fill=(210, 205, 195))  # 셔츠
    d.rounded_rectangle([px-66, top+190, px+66, gy], 30, fill=(150, 52, 36))    # 앞치마
def bubble(d, side, text, y0=430):
    f = SAN(58); lines = text.split("\n")
    tw = max(d.textbbox((0, 0), t, font=f)[2] for t in lines)
    bw = tw+120; th = len(lines)*84
    x0 = 90 if side == "L" else BW-90-bw
    d.rounded_rectangle([x0, y0, x0+bw, y0+th+52], 40, fill=PAPER, outline=(60, 56, 50), width=5)
    tx = x0+bw*0.3 if side == "L" else x0+bw*0.7
    d.polygon([(tx-26, y0+th+46), (tx+30, y0+th+46), (tx, y0+th+150)], fill=PAPER)
    y = y0+30
    for t in lines:
        bb = d.textbbox((0, 0), t, font=f)
        d.text((x0+(bw-bb[2])/2, y), t, font=f, fill=INK)
        y += 84

def base_line(text, side):
    im = night(); d = ImageDraw.Draw(im)
    im = glow(im, BW/2, 1000, 480, (56, 46, 28)); d = ImageDraw.Draw(im)
    d.line([(80, 1700), (BW-80, 1700)], fill=(52, 56, 74), width=5)
    d.rounded_rectangle([BW/2-150, 1180, BW/2+150, 1330], 20, fill=(46, 52, 68),
                        outline=(150, 152, 160), width=5)                       # 진열대
    for i, c in enumerate([(196, 62, 74), (232, 163, 61), (91, 124, 153)]):
        d.ellipse([BW/2-100+i*70, 1215, BW/2-40+i*70, 1295], fill=c)
    d.line([(BW/2+220, 900), (BW/2+220, 1050)], fill=(80, 82, 90), width=6)     # 한정 팻말
    d.rounded_rectangle([BW/2+120, 1040, BW/2+330, 1160], 16, fill=RED)
    ctext(d, BW/2+225, 1062, "한정", SAN(52), PAPER)
    dahye(d, BW/2-280, 1700); sajang(d, BW/2+300, 1700)
    bubble(d, side, text)
    tag(d); return im

def b_end():
    im = Image.new("RGB", (BW, BH), INK); d = ImageDraw.Draw(im)
    ctext(d, BW/2, 460, "말값", SER(280), PAPER)
    ctext(d, BW/2, 860, "=", SER(150), PAPER)
    ctext(d, BW/2, 1040, "시즌 한정", SER(160), PAPER)
    ctext(d, BW/2, 1280, "−  ____개월", SER(130), PAPER)
    d.line([(BW/2+30, 1460), (BW/2+300, 1460)], fill=RED, width=14)
    redbar(d, 1620, "빈칸은 당신이 채우세요")
    s = seal_empty(); im.paste(s, (BW-360, BH-480), s)
    ctext(d, BW/2, BH-260, "다음 시즌에도 이 팻말은 걸려 있을 것이다", SAN(42), PAPER)
    tag(d); return im

BUB = {"l1": "이거 지난달에도\n있지 않았어요?", "l2": "시즌 한정입니다.",
       "l3": "무슨 시즌인데요?", "l4": "이번 시즌이요.",
       "l5": "지난달은요?", "l6": "지난 시즌\n한정이었죠.",
       "l7": "그럼 다음 달엔요?", "l8": "다음 시즌 한정이\n나옵니다."}
VO = json.load(open(f"{ROOT}/vo/lines.json"))
GAP = 0.42
SC_A = [(p["id"], p["dur"]+GAP) for p in VO]+[("end", 4.2)]
print(f"audio {mix_audio(SC_A, f'{ROOT}/vo', f'{ROOT}/mix.wav'):.2f}s")
def mk(lid):
    side = "L" if lid in ("l1", "l3", "l5", "l7") else "R"
    return lambda: base_line(BUB[lid], side)
def anim_dot(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    r = 11+2.6*math.sin(t*3.1)
    d.ellipse([W/2-r, 250-r, W/2+r, 250+r], outline=PAPER, width=5)
    return im
SCENES = []
for i, (lid, secs) in enumerate(SC_A[:-1]):
    kb = (1.05, 1.00, -15 if i % 2 else 15, 0) if i % 2 else (1.00, 1.05, 15, 0)
    SCENES.append((mk(lid), secs, kb, None))
SCENES.append((b_end, 4.2, (1.00, 1.04, 0, 0), anim_dot))
n, rc = encode(SCENES, f"{ROOT}/mix.wav", f"{ROOT}/malgap_no6.mp4", seed0=800)
print("frames", n, "rc", rc)
