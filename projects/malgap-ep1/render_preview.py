"""Standalone boil-style preview. Mimics gen_boil's wobbly line art with PIL so
the panels can be seen while video-studio is unreachable. NOT the render path."""
import math, random, importlib.util
from PIL import Image, ImageDraw, ImageFont

FONT="projects/malgap-ep1/NotoSansKR-Bold.ttf"
INK="#14110F"; PAPER="#F2E9DC"; RED="#C8452E"
W,H=540,960

spec=importlib.util.spec_from_file_location("shapes","projects/malgap-ep1/boil_shapes.py")
mod=importlib.util.module_from_spec(spec)
mod.__dict__["math"]=math

def wob(d,pts,c,rng,w,amp):
    out=[]
    for x,y in pts:
        out.append((x+rng.uniform(-amp,amp), y+rng.uniform(-amp,amp)))
    if len(out)>1: d.line(out,fill=c,width=int(w),joint="curve")
mod.__dict__["wob"]=wob
mod.__dict__["circle"]=lambda *a,**k: None
mod.__dict__["box"]=lambda *a,**k: None
spec.loader.exec_module(mod)

def rings(d,c,rng,w,p,cx,cy,s):
    for k in range(4):
        r=s*(0.12+0.10*k)*(1+0.04*math.sin(p*math.tau+k))
        pts=[(cx+math.cos(math.tau*i/47)*r, cy+math.sin(math.tau*i/47)*r) for i in range(48)]
        wob(d,pts,c,rng,w,2.4)

SCENES=[
 ("S1 HOOK",   rings,          None,                    INK,PAPER,6.0),
 ("S2 REVEAL", mod.s_spark,    "시그니처",                PAPER,INK,5.0),
 ("S3 BEAT1",  mod.s_cup,      "요거트에\n토핑 세 개",      INK,PAPER,6.0),
 ("S4 BEAT2",  mod.s_coin,     "3만 원",                 INK,PAPER,6.0),
 ("S5 BEAT3",  mod.s_scale,    "재료값\n____원",          INK,PAPER,6.0),
 ("S6 LANDING",mod.s_period,   "말값 =\n3만 원 − ____",   INK,PAPER,5.0),
]

def panel(idx,label,fn,text,bg,fg,secs):
    im=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im)
    rng=random.Random(1000+idx)
    # mark in upper half, card in lower half — never overlapping (boil render note)
    fn(d,fg,rng,3,0.25,W*0.5,H*0.34,W*0.62)
    if text:
        f=ImageFont.truetype(FONT,54)
        y=H*0.66
        for line in text.split("\n"):
            bb=d.textbbox((0,0),line,font=f)
            d.text(((W-(bb[2]-bb[0]))/2, y), line, font=f, fill=fg)
            y+=68
    fs=ImageFont.truetype(FONT,22)
    d.text((18,18), f"{label}  {secs}s", font=fs, fill=fg)
    d.rectangle([2,2,W-3,H-3],outline=fg,width=2)
    return im

panels=[panel(i,*sc) for i,sc in enumerate(SCENES)]
sheet=Image.new("RGB",(W*3+40*4,H*2+40*3),"#8A8175")
for i,p in enumerate(panels):
    r,c=divmod(i,3)
    sheet.paste(p,(40+(W+40)*c, 40+(H+40)*r))
sheet.save("projects/malgap-ep1/preview_contactsheet.png")
for i,p in enumerate(panels): p.save(f"projects/malgap-ep1/panel_{i+1}.png")
print("wrote contact sheet", sheet.size)
