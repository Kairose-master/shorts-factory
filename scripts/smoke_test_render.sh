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

echo "==> no subtitle text may be dropped"
python3 - "$DIR" <<'PY2' || { echo "FAIL: subtitle text was lost in wrapping"; fail=1; }
import json, sys, pathlib
sys.path.insert(0, "scripts")
import sermon_shorts as ss
d = pathlib.Path(sys.argv[1])
segs = json.loads((d / "transcript.json").read_text(encoding="utf-8"))["segments"]
# A long line must survive wrapping intact, split across cues if need be.
segs = segs + [{"start": 0.0, "end": 9.0, "text":
                "여러분들 머리는 베어 가지고 지울 수 있겠지만은 그 사람의 한 말이 내 마음에 "
                "꽂힌 것을 제거할 수 있을까요, 없을까요? 없어요."}]
for x in segs:
    want = "".join(x["text"].split())
    cues = ss.split_for_display(x)
    got = "".join("".join(ss.wrap_korean(c["text"]).replace("\\N", " ").split()) for c in cues)
    assert got == want, f"lost text:\n  want {want}\n  got  {got}"
    assert abs(cues[0]["start"] - x["start"]) < 1e-6
    assert abs(cues[-1]["end"] - x["end"]) < 1e-6
print("    ok — all subtitle text survives wrapping")
PY2

echo "==> a hand-corrected caption file wins over the transcript"
python3 - "$DIR" <<'PY4' || { echo "FAIL: caption override"; fail=1; }
import pathlib, sys
sys.path.insert(0, "scripts")
import sermon_shorts as ss
d = pathlib.Path(sys.argv[1])
cap = d / "captions"; cap.mkdir(exist_ok=True)
(cap / "clip-01.srt").write_text(
    "1\n00:00:00,000 --> 00:00:03,000\n고친말이맞다\n\n", encoding="utf-8")
segs = ss.read_srt(cap / "clip-01.srt")
assert segs and segs[0]["text"] == "고친말이맞다", segs
# render reads it back at offset 0, because an edited file is already
# clip-relative — the same path the burn-in takes.
ass = d / "renders" / "subs" / "_override_test.ass"
ass.parent.mkdir(parents=True, exist_ok=True)
ss.write_ass(segs, ass, offset=0.0, title="", duration=3.0)
body = ass.read_text(encoding="utf-8")
assert "고친말이맞다" in body, body[-300:]
assert "0:00:00.00,0:00:03.00" in body, body[-300:]
ass.unlink()
(cap / "clip-01.srt").unlink()
# Whatever the editor saved it as, the words have to survive.
good = "1\n00:00:00,000 --> 00:00:03,000\n고친말이맞다\n\n"
for enc in ("utf-8", "utf-8-sig", "cp949"):
    f = cap / f"enc-{enc}.srt"
    f.write_bytes(good.encode(enc))
    assert ss.read_srt(f)[0]["text"] == "고친말이맞다", enc
    f.unlink()
f = cap / "crlf.srt"; f.write_bytes(good.replace("\n", "\r\n").encode("utf-8"))
assert ss.read_srt(f)[0]["text"] == "고친말이맞다"
f.unlink()

# And a file that would render wrong must stop the render, not pass through.
for name, data in (("noTime", b"1\n\xea\xb8\x80\xec\x9e\x90\xeb\xa7\x8c\n\n"),
                   ("mojibake", "1\n00:00:00,000 --> 00:00:03,000\n".encode()
                                + b"\xed\xa0\x80\xff\xfe"),
                   ("reversed", "1\n00:00:05,000 --> 00:00:02,000\n뒤집힘\n\n".encode())):
    f = cap / f"{name}.srt"; f.write_bytes(data)
    try:
        ss.check_caption_file(f, 45.0)
        raise AssertionError(f"{name} should have been refused")
    except SystemExit:
        pass
    f.unlink()
cap.rmdir()
print("    ok — edited captions reach the burn-in, timings preserved")
print("    ok — CP949/BOM/CRLF read, broken files refused")
PY4

echo "==> end card is built from the channel's own video title"
python3 - "$DIR" <<'PY3' || { echo "FAIL: end card"; fail=1; }
import pathlib, sys
sys.path.insert(0, "scripts")
import sermon_shorts as ss

# Both title shapes the channel has used, new and old.
for idea, title, want_ref, want_title in [
    ("SUN-2026-04-26",
     "2026-04-26 [삼하 2:24-32] 이기는데 집착하지 말라. 잃는다. / 장선기 목사",
     "사무엘하 2:24-32", "이기는데 집착하지 말라. 잃는다."),
    ("SUN-2024-06-23",
     "2024.06.23 택하신 곳으로 나아가야 하는 이유 신명기 12:1-8 장선기목사",
     "신명기 12:1-8", "택하신 곳으로 나아가야 하는 이유"),
]:
    c = ss.end_card_from_title(idea, title)
    assert c["scripture"] == want_ref, c
    assert c["title"] == want_title, c
    assert c["preacher"].endswith("장선기 목사"), c
    assert c["church"] == "방배동 예심교회", c
    assert c["date"].endswith("주일예배"), c

out = pathlib.Path(sys.argv[1]) / "renders" / "_endcard_test.mp4"
ss.build_end_card(c, out)
ass = out.with_suffix(".ass").read_text(encoding="utf-8")
for must in ("PlayResY: 1920", "방배동 예심교회", "신명기", "장선기 목사", "2024년 6월 23일"):
    assert must in ass, f"missing from end card: {must}"
print("    ok — end card carries date, passage, title, preacher, church")
PY3
python3 -c "
import subprocess,sys
p=subprocess.run(['ffmpeg','-hide_banner','-i','$DIR/renders/_endcard_test.mp4'],capture_output=True,text=True)
assert '1080x1920' in p.stderr, p.stderr[-400:]
print('    ok — end card renders 1080x1920')
" || { echo "FAIL: end card resolution"; fail=1; }

[ -f "$DIR/publish-package.md" ] || { echo "FAIL: no publish-package.md"; fail=1; }
grep -q "Content ID" "$DIR/publish-package.md" || { echo "FAIL: worship-music flag missing from package"; fail=1; }
echo "    ok — publish package carries the copyright flags"

rm -f "$DIR/clips.template.json" "$DIR/clips.real.json"
rm -f "$DIR/renders/_endcard_test.mp4" "$DIR/renders/_endcard_test.ass"
if [ "$fail" -eq 0 ]; then
  echo; echo "PASS — render layer works. Artifacts left in $DIR for inspection."
else
  echo; echo "FAILED"; exit 1
fi
