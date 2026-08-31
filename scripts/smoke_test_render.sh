#!/usr/bin/env bash
# Prove the render half of the Tier 0 pipeline works in this container.
#
# Builds a synthetic 16:9 "sermon" with a Korean transcript, runs
# clips → render, and checks the output is a real 1080x1920 MP4 with the
# Korean subtitles burned in. Needs no network and no source video, so it
# still passes when YouTube is blocked (see docs/environment-constraints.md).
#
#   bash scripts/smoke_test_render.sh
set -euo pipefail

cd "$(dirname "$0")/.."
ID=_smoketest
DIR="office/production/$ID"

command -v ffmpeg >/dev/null || { echo "ffmpeg missing — run scripts/setup_render_env.sh"; exit 1; }

rm -rf "$DIR"
mkdir -p "$DIR/source"

echo "==> building synthetic source"
ffmpeg -y -hide_banner -loglevel error \
  -f lavfi -i "testsrc2=size=1920x1080:rate=30:duration=100" \
  -f lavfi -i "sine=frequency=220:duration=100" \
  -c:v libx264 -preset ultrafast -c:a aac -shortest "$DIR/source/sermon.mp4"

python3 - "$DIR" <<'PY'
import json, sys, pathlib
lines = [
    "오늘 본문은 우리에게 아주 단순한 질문 하나를 던집니다",
    "당신은 지금 무엇을 붙들고 살고 있습니까",
    "많은 분들이 불안을 붙들고 삽니다",
    "그런데 성경은 정반대를 말합니다",
    "하나님의 은혜는 우리가 생각하는 것보다 큽니다",
    "우리가 실패한 그 자리에서도 은혜는 멈추지 않습니다",
    "그래서 오늘 이 말씀을 꼭 붙드시기 바랍니다",
    "여러분의 한 주간이 이 은혜 위에 서기를 축복합니다",
]
segs = [{"start": i * 12.0, "end": i * 12.0 + 11.0, "text": t} for i, t in enumerate(lines)]
d = pathlib.Path(sys.argv[1])
(d / "transcript.json").write_text(
    json.dumps({"backend": "synthetic", "language": "ko", "segments": segs},
               ensure_ascii=False, indent=2), encoding="utf-8")

clips = [
    {"id": "clip-01", "start": "00:00:00", "end": "00:00:36",
     "title": "당신은 무엇을 붙들고 삽니까", "hook": "당신은 지금 무엇을 붙들고 살고 있습니까",
     "description": "주일설교 중", "reason": "질문형 도입이 답을 미뤄 이탈이 늦다",
     "crop": "center"},
    {"id": "clip-02", "start": "00:00:36", "end": "00:01:12",
     "title": "은혜는 멈추지 않습니다", "hook": "하나님의 은혜는 생각보다 큽니다",
     "description": "주일설교 중", "reason": "'그런데'로 시작해 대비 구조가 이미 들어 있다",
     "has_worship_music": True, "congregation_visible": True, "crop": "left"},
]
(d / "clips.json").write_text(json.dumps(clips, ensure_ascii=False, indent=2), encoding="utf-8")
PY

echo "==> an unedited template must be rejected"
python3 - "$DIR" <<'PY'
import json, sys, pathlib
sys.path.insert(0, "scripts")
import sermon_shorts
pathlib.Path(sys.argv[1], "clips.template.json").write_text(
    json.dumps(sermon_shorts.CLIPS_TEMPLATE, ensure_ascii=False, indent=2), encoding="utf-8")
PY
cp "$DIR/clips.json" "$DIR/clips.real.json"
cp "$DIR/clips.template.json" "$DIR/clips.json"
if python3 scripts/sermon_shorts.py render "$ID" >/dev/null 2>&1; then
  echo "FAIL: template clips.json rendered — the placeholder guard is broken"; exit 1
fi
echo "    ok — rejected"
cp "$DIR/clips.real.json" "$DIR/clips.json"

echo "==> rendering"
python3 scripts/sermon_shorts.py render "$ID"

fail=0
for c in clip-01 clip-02; do
  f="$DIR/renders/$c.mp4"
  [ -s "$f" ] || { echo "FAIL: $f missing or empty"; fail=1; continue; }
  # `ffmpeg -i` with no output always exits non-zero; guard it against set -e.
  dim=$(ffmpeg -hide_banner -i "$f" 2>&1 | grep -o '[0-9]\{3,4\}x[0-9]\{3,4\}' | head -1 || true)
  [ "$dim" = "1080x1920" ] || { echo "FAIL: $c is $dim, expected 1080x1920"; fail=1; }
  grep -q "PlayResY: 1920" "$DIR/renders/subs/$c.ass" || { echo "FAIL: $c.ass lacks real-pixel PlayRes"; fail=1; }
  grep -q "하나님\|당신은\|그런데" "$DIR/renders/subs/$c.ass" || { echo "FAIL: $c.ass has no Korean text"; fail=1; }
  echo "    ok — $c $dim"
done

[ -f "$DIR/publish-package.md" ] || { echo "FAIL: no publish-package.md"; fail=1; }
grep -q "Content ID" "$DIR/publish-package.md" || { echo "FAIL: worship-music flag missing from package"; fail=1; }
echo "    ok — publish package carries the copyright flags"

rm -f "$DIR/clips.template.json" "$DIR/clips.real.json"
if [ "$fail" -eq 0 ]; then
  echo; echo "PASS — render layer works. Artifacts left in $DIR for inspection."
else
  echo; echo "FAILED"; exit 1
fi
