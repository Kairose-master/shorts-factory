"""EP별 Remotion 데이터 생성: vo2 재생성(WordBoundary) → rmx/src/data/ep{N}.json + public/vo/ep{N}/.

사용: python3 mk_data.py <ep> '<title1>|<title2>' '<tag>' '<world>' — LINES는 ep{N}-short/gen_vo.py에서 파싱.
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import vo_kit

ep = int(sys.argv[1])
title = sys.argv[2].split("|")
tag = sys.argv[3]
world = sys.argv[4]
epdir = f"{ROOT}/../ep{ep}-short"

src = open(f"{epdir}/gen_vo.py", encoding="utf-8").read()
lines = re.findall(r'\("([^"]+)","([^"]+)","([^"]+)"\)', src)
assert len(lines) == 11, f"expected 11 lines, got {len(lines)}"

vo2 = f"{epdir}/vo2"
if not os.path.exists(f"{vo2}/lines.json"):
    vo_kit.generate(lines, vo2)

plan = json.load(open(f"{vo2}/lines.json"))
GAP, LEAD, FPS = 0.12, 0.15, 30
scenes, t0 = [], 0.0
for e in plan:
    secs = e["dur"] + GAP + (0.10 if e["id"] == "s11" else 0)
    chips = vo_kit.chips_from_words(e) or []
    scenes.append({"id": e["id"], "from": round(t0*FPS), "dur": round(secs*FPS),
                   "wav": f"vo/ep{ep}/{e['id']}.wav", "lead": LEAD,
                   "chips": [{"t": round((t+LEAD)*FPS), "d": round(d*FPS), "text": c}
                             for c, t, d in chips]})
    t0 += secs

data = {"fps": FPS, "durationInFrames": round(t0*FPS)+1, "scenes": scenes,
        "title": title, "tag": tag, "world": world}
os.makedirs(f"{ROOT}/rmx/public/vo/ep{ep}", exist_ok=True)
for e in plan:
    shutil.copy(f"{vo2}/{e['id']}.wav", f"{ROOT}/rmx/public/vo/ep{ep}/{e['id']}.wav")
json.dump(data, open(f"{ROOT}/rmx/src/data/ep{ep}.json", "w"), ensure_ascii=False, indent=1)
print(f"ep{ep}: {data['durationInFrames']} frames, {t0:.1f}s")
