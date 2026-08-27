"""「말값」 EP1 — 카툰판 렌더러.

로맨툰(13.87x, 실측 2d-animation/webtoon)의 형식을 따른다: 캐릭터 2인 대화극,
말풍선, 표정 연기, 내레이터 없음. 소재는 제로비(원가), 결말은 궁금소(판단 유보).
"""
import math, json, wave, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
INK    = "#14110F"
CREAM  = "#F2E9DC"
WHITE  = "#FFFFFF"
SKIN   = "#F5D5B8"
D_HAIR = "#3A2E28"   # 다혜
S_HAIR = "#55504A"   # 정사장
D_TOP  = "#5B7C99"
APRON  = "#C8452E"
TABLE  = "#C9B8A0"
OL = 7               # outline width

F_BUB  = ImageFont.truetype(f"{ROOT}/../malgap-ep1/NotoSansKR-Bold.ttf", 62)
F_TAG  = ImageFont.truetype(f"{ROOT}/../malgap-ep1/NotoSansKR-Bold.ttf", 38)
F_CARD = ImageFont.truetype(f"{ROOT}/../malgap-ep1/NotoSansKR-Bold.ttf", 100)
F_SER  = ImageFont.truetype(f"{ROOT}/../malgap-ep1/NotoSansKR-Bold.ttf", 42)

LINES = json.load(open(f"{ROOT}/vo/lines.json"))
BUBBLE = {  # manual wraps
 "l1":"사장님, 요거트 하나에\n3만 원이요?", "l2":"시그니처니까요.",
 "l3":"뭐가 다른데요?",                    "l4":"저희만의\n큐레이션입니다.",
 "l5":"토핑 세 개잖아요.",                 "l6":"프리미엄 토핑이죠.",
 "l7":"재료값은 얼마인데요?",               "l8":"그건…\n영업 비밀입니다.",
}
# per-line acting: (dahye_expr, sajang_expr)  expr=(eyes,mouth,sweat,spark)
ACT = {
 "l1": (("wide","flap",0,0), ("n","smile",0,0)),
 "l2": (("n","line",0,0),    ("closed","flap",0,0)),
 "l3": (("squint","flap",0,0),("n","smile",0,0)),
 "l4": (("n","line",0,0),    ("closed","flap",0,1)),
 "l5": (("half","flap",0,0), ("n","strain",1,0)),
 "l6": (("squint","line",0,0),("wide","flap",1,0)),
 "l7": (("sharp","flap",0,0),("wide","line",2,0)),
 "l8": (("half","line",0,0), ("away","flap",2,0)),
}

def rr(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def eyes(d, cx, cy, kind, look=0):
    dx = 52
    if kind == "n":
        for s in (-1,1): d.ellipse([cx+s*dx-9,cy-9,cx+s*dx+9,cy+9], fill=INK)
    elif kind == "wide":
        for s in (-1,1):
            d.ellipse([cx+s*dx-20,cy-20,cx+s*dx+20,cy+20], fill=WHITE, outline=INK, width=5)
            d.ellipse([cx+s*dx-8,cy-8,cx+s*dx+8,cy+8], fill=INK)
    elif kind == "closed":
        for s in (-1,1): d.arc([cx+s*dx-20,cy-12,cx+s*dx+20,cy+16], 200, 340, fill=INK, width=6)
    elif kind == "squint":
        for s in (-1,1):
            d.line([cx+s*dx-20,cy,cx+s*dx+20,cy], fill=INK, width=7)
            d.line([cx+s*dx-22,cy-22,cx+s*dx+18,cy-14] if s<0 else
                   [cx+s*dx-18,cy-14,cx+s*dx+22,cy-22], fill=INK, width=6)
    elif kind == "half":
        for s in (-1,1):
            d.ellipse([cx+s*dx-11,cy-6,cx+s*dx+11,cy+12], fill=INK)
            d.line([cx+s*dx-14,cy-8,cx+s*dx+14,cy-8], fill=INK, width=8)
    elif kind == "sharp":
        for s in (-1,1):
            d.ellipse([cx+s*dx-9,cy-9,cx+s*dx+9,cy+9], fill=INK)
            d.line([cx+s*dx-22,cy-26,cx+s*dx+20,cy-16] if s<0 else
                   [cx+s*dx-20,cy-16,cx+s*dx+22,cy-26], fill=INK, width=7)
    elif kind == "away":
        for s in (-1,1):
            d.ellipse([cx+s*dx-16,cy-16,cx+s*dx+16,cy+16], fill=WHITE, outline=INK, width=5)
            d.ellipse([cx+s*dx+2,cy-6,cx+s*dx+16,cy+8], fill=INK)  # pupils fled right

def mouth(d, cx, cy, kind, talking):
    if kind == "flap":
        if talking: d.ellipse([cx-24,cy-16,cx+24,cy+22], fill=INK)
        else:       d.line([cx-20,cy,cx+20,cy], fill=INK, width=7)
    elif kind == "smile":  d.arc([cx-26,cy-22,cx+26,cy+16], 20, 160, fill=INK, width=7)
    elif kind == "strain": d.line([cx-22,cy+4,cx-6,cy-4,cx+10,cy+4,cx+24,cy-4], fill=INK, width=6, joint="curve")
    else:                  d.line([cx-20,cy,cx+20,cy], fill=INK, width=7)

def sweat(d, cx, cy, n, p):
    for k in range(n):
        fall = (p*90 + k*30) % 60
        x, y = cx+95+k*16, cy-70+fall
        d.polygon([(x,y-16),(x-10,y+6),(x+10,y+6)], fill="#9EC7E8", outline=INK)
        d.ellipse([x-11,y-2,x+11,y+18], fill="#9EC7E8", outline=INK, width=4)

def sparkle(d, cx, cy, p):
    r = 26 + 5*math.sin(p*math.tau*2)
    x, y = cx-120, cy-95
    for a in range(4):
        t = a*math.pi/2 + 0.4
        d.line([x-math.cos(t)*r, y-math.sin(t)*r, x+math.cos(t)*r, y+math.sin(t)*r], fill="#E8A33D", width=7)

def dahye(d, cx, gy, expr, talking, p, lean=0):
    bob = 4*math.sin(p*math.tau*2.2) if talking else 1.5*math.sin(p*math.tau)
    cx += lean; cy = gy - 430 + bob
    rr(d, [cx-140, gy-300+bob, cx+140, gy+40], 60, D_TOP, INK, OL)          # torso
    d.ellipse([cx-118, cy-118, cx+118, cy+118], fill=SKIN, outline=INK, width=OL)
    d.pieslice([cx-126, cy-140, cx+126, cy+60], 180, 360, fill=D_HAIR)      # bob hair
    d.ellipse([cx-126, cy-40, cx-78, cy+108], fill=D_HAIR)                  # side hair
    d.ellipse([cx+78,  cy-40, cx+126, cy+108], fill=D_HAIR)
    d.rectangle([cx-70, cy-70, cx+70, cy-48], fill=D_HAIR)                  # bangs edge
    ey, ex = expr[0], cy+8
    eyes(d, cx, ex, ey); mouth(d, cx, cy+62, expr[1], talking)
    if expr[2]: sweat(d, cx, cy, expr[2], p)

def sajang(d, cx, gy, expr, talking, p):
    bob = 4*math.sin(p*math.tau*2.2) if talking else 1.5*math.sin(p*math.tau+1)
    cy = gy - 430 + bob
    rr(d, [cx-150, gy-300+bob, cx+150, gy+40], 60, WHITE, INK, OL)          # shirt
    rr(d, [cx-110, gy-240+bob, cx+110, gy+40], 40, APRON, INK, OL)          # apron
    d.line([cx-90, gy-240+bob, cx-40, gy-300+bob], fill=INK, width=6)       # straps
    d.line([cx+90, gy-240+bob, cx+40, gy-300+bob], fill=INK, width=6)
    d.ellipse([cx-118, cy-118, cx+118, cy+118], fill=SKIN, outline=INK, width=OL)
    d.pieslice([cx-122, cy-135, cx+122, cy+15], 180, 360, fill=S_HAIR)      # short hair
    ey = expr[0]
    eyes(d, cx, cy+8, ey); 
    d.arc([cx-34, cy+34, cx+34, cy+66], 200, 340, fill=S_HAIR, width=9)     # mustache
    mouth(d, cx, cy+74, expr[1], talking)
    if expr[2]: sweat(d, cx, cy, expr[2], p)
    if expr[3]: sparkle(d, cx, cy, p)

def yogurt(d, cx, gy):
    rr(d, [cx-150, gy-30, cx+150, gy+40], 22, TABLE, INK, 6)                # table
    top, bot, h = 46, 34, 62; cy = gy-30
    d.polygon([(cx-top,cy-h),(cx+top,cy-h),(cx+bot,cy),(cx-bot,cy)], fill=WHITE, outline=INK)
    for k in range(3):
        bx = cx+(k-1)*26
        d.ellipse([bx-14, cy-h-22, bx+14, cy-h+4], fill="#E8A33D" if k==1 else "#C8452E", outline=INK, width=4)
    d.text((cx+165, cy-h-10), "₩30,000+", font=F_TAG, fill=INK)             # price tag
def bubble(d, side, text):
    lines = text.split("\n")
    tw = max(d.textbbox((0,0), t, font=F_BUB)[2] for t in lines)
    th = len(lines)*84
    bw = tw + 110
    x0 = 70 if side=="L" else W-70-bw
    y0 = 300
    rr(d, [x0, y0, x0+bw, y0+th+56], 46, WHITE, INK, OL)
    tx = x0+bw*0.28 if side=="L" else x0+bw*0.72
    d.polygon([(tx-30,y0+th+50),(tx+34,y0+th+50),(tx-4,y0+th+150)], fill=WHITE, outline=INK)
    d.polygon([(tx-22,y0+th+40),(tx+26,y0+th+40),(tx-4,y0+th+138)], fill=WHITE)
    y = y0+34
    for t in lines:
        bb = d.textbbox((0,0), t, font=F_BUB)
        d.text((x0+(bw-bb[2])/2, y), t, font=F_BUB, fill=INK)
        y += 84

DX, SX, GY = 285, 795, 1730

def scene_frame(line, fi, dur, audio_dur):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    d.text((60, 90), "「말값」 EP1", font=F_SER, fill=INK)
    p = fi/FPS/dur
    talking = fi/FPS < audio_dur + 0.1
    flap = talking and (fi//5) % 2 == 0
    da, sa = ACT[line["id"]]
    spk = line["spk"]
    yogurt(d, W//2, GY-320)
    dahye(d, DX, GY, da, flap if spk=="dahye" else False, p, lean=18 if line["id"]=="l7" else 0)
    sajang(d, SX, GY, sa, flap if spk=="sajang" else False, p)
    if line["id"] in ("l1","l2"):
        for cx, name in ((DX,"다혜"),(SX,"정사장")):
            bb = d.textbbox((0,0), name, font=F_TAG)
            rr(d, [cx-bb[2]/2-16, GY+58, cx+bb[2]/2+16, GY+112], 14, INK)
            d.text((cx-bb[2]/2, GY+64), name, font=F_TAG, fill=CREAM)
    bubble(d, "L" if spk=="dahye" else "R", BUBBLE[line["id"]])
    return im

def endcard_frame(fi, dur):
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    p = fi/FPS/dur
    r = 12 + 2.5*math.sin(p*math.tau*2)
    d.ellipse([W/2-r, 520-r, W/2+r, 520+r], outline=CREAM, width=6)
    y = 800
    for t in ["말값 =", "3만 원 − ____원"]:
        bb = d.textbbox((0,0), t, font=F_CARD)
        d.text(((W-bb[2])/2, y), t, font=F_CARD, fill=CREAM); y += 160
    d.text((60, H-160), "「말값」 EP1 — 시그니처", font=F_SER, fill=CREAM)
    return im

# ---------- audio ----------
SR, GAP, ENDC = 24000, 0.55, 4.5
scenes = [(l, l["dur"] + GAP) for l in LINES]
TOTAL = sum(s for _, s in scenes) + ENDC
track = np.zeros(int(TOTAL*SR)+SR, dtype=np.float32)
t = 0.0
for l, sdur in scenes:
    with wave.open(f"{ROOT}/vo/{l['id']}.wav") as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
    a *= 0.30/max(np.sqrt((a**2).mean()), 1e-6)
    st = int((t+0.12)*SR); track[st:st+len(a)] += a
    t += sdur
track = np.clip(track[:int(TOTAL*SR)], -0.99, 0.99)
with wave.open(f"{ROOT}/mix.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track*32767).astype(np.int16).tobytes())
print(f"audio {TOTAL:.2f}s")

# ---------- video ----------
exe = imageio_ffmpeg.get_ffmpeg_exe()
proc = subprocess.Popen(
    [exe,"-y","-loglevel","error",
     "-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
     "-i",f"{ROOT}/mix.wav",
     "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",
     "-c:a","aac","-ar","48000","-b:a","160k","-shortest","-movflags","+faststart",
     f"{ROOT}/malgap_ep1_cartoon.mp4"], stdin=subprocess.PIPE)
n = 0
for l, sdur in scenes:
    for fi in range(int(sdur*FPS)):
        proc.stdin.write(scene_frame(l, fi, sdur, l["dur"]).tobytes()); n += 1
    print(f"  {l['id']} ok")
for fi in range(int(ENDC*FPS)):
    proc.stdin.write(endcard_frame(fi, ENDC).tobytes()); n += 1
proc.stdin.close(); proc.wait()
print("frames", n, "rc", proc.returncode)
