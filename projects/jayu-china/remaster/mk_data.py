"""EP별 Remotion 데이터 생성 — 포맷 v2.0 (45초 · 10씬 · 페이오프 전진).

대본은 scripts/ep{N}.json (v2.0 재배치본)에서 읽는다. 없으면 ep{N}-short/gen_vo.py의
구(v1.0) 11줄로 폴백. Gemini TTS로 내레이션을 생성해 vo3/에 캐시하고
rmx/src/data/ep{N}.json + rmx/public/vo/ep{N}/ 을 갱신한다.

사용: python3 mk_data.py <ep> [--regen]      (편당 Gemini TTS 10콜)
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import evo_kit as tts_kit          # edge-tts 구 단위 (무료·무제한) — 편집장 결정 2026-08-29


ep = int(sys.argv[1])
regen = "--regen" in sys.argv
epdir = f"{ROOT}/../ep{ep}-short"
spath = f"{ROOT}/scripts/ep{ep}.json"

if os.path.exists(spath):
    S = json.load(open(spath, encoding="utf-8"))
    lines = [tuple(x) for x in S["lines"]]
    title, tag, world = S["title"], S["tag"], S["world"]
    vo = f"{epdir}/vo4"
else:                                    # 폴백: 구 포맷 (v1.0 11줄)
    src = open(f"{epdir}/gen_vo.py", encoding="utf-8").read()
    lines = re.findall(r'\("([^"]+)","([^"]+)","([^"]+)"\)', src)
    title = sys.argv[2].split("|"); tag = sys.argv[3]; world = sys.argv[4]
    vo = f"{epdir}/vo4"

if regen or not os.path.exists(f"{vo}/lines.json"):
    tts_kit.generate(lines, vo)

plan = json.load(open(f"{vo}/lines.json"))
GAP, LEAD, FPS = 0.26, 0.15, 30
# 씬 최소 길이 — 내레이션이 빨라져도 비주얼 비트(스탬프 착지·사슬 캐스케이드·
# 지도 드로우온)가 완결되도록 보장. 남는 시간은 침묵이 아니라 아트 홀드.
# v2.0 상한 규칙: 어떤 씬도 6초를 넘기지 않는다(넘으면 대본을 쪼갠다).
MIN_SECS = {"s1": 3.2, "s8": 4.4, "s10": 3.2}
MAX_SECS = 6.4
scenes, t0, over = [], 0.0, []
for e in plan:
    secs = e["dur"] + GAP + (0.10 if e["id"] == plan[-1]["id"] else 0)
    secs = max(secs, MIN_SECS.get(e["id"], 2.6))
    if secs > MAX_SECS:
        over.append((e["id"], round(secs, 1)))
    scenes.append({"id": e["id"], "from": round(t0*FPS), "dur": round(secs*FPS),
                   "wav": f"vo/ep{ep}/{e['id']}.wav", "lead": LEAD,
                   "chips": [{"t": round((s+LEAD)*FPS), "d": max(8, round(d*FPS)), "text": c}
                             for c, s, d in e["chips"]]})
    t0 += secs

data = {"fps": FPS, "durationInFrames": round(t0*FPS)+1, "scenes": scenes,
        "title": title, "tag": tag, "world": world}
os.makedirs(f"{ROOT}/rmx/public/vo/ep{ep}", exist_ok=True)
for e in plan:
    shutil.copy(f"{vo}/{e['id']}.wav", f"{ROOT}/rmx/public/vo/ep{ep}/{e['id']}.wav")
json.dump(data, open(f"{ROOT}/rmx/src/data/ep{ep}.json", "w"), ensure_ascii=False, indent=1)
print(f"ep{ep}: {len(scenes)}씬 {data['durationInFrames']} frames = {t0:.1f}s")
if over:
    print(f"  ⚠ 6.4초 상한 초과 (대본 분할 필요): {over}")
