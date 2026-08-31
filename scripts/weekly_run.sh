#!/usr/bin/env bash
# 주간 반복 실행 — 주일 설교 한 편 → 쇼츠 후보 렌더.
#
#   bash scripts/weekly_run.sh <유튜브-URL> [idea-id]
#
# idea-id를 생략하면 오늘 날짜로 SUN-YYYY-MM-DD 를 쓴다.
#
# 이 스크립트는 사람이 판단해야 하는 지점에서 **일부러 멈춘다.** 구간 선별은
# 자동화하지 않는다 — 전사본을 읽고 clips.json 을 채운 뒤 다시 실행하면
# 이어서 렌더한다. 업로드는 어느 단계에서도 하지 않는다.
set -euo pipefail

cd "$(dirname "$0")/.."

URL=${1:-}
ID=${2:-SUN-$(date +%F)}
[ -n "$URL" ] || { echo "usage: bash scripts/weekly_run.sh <youtube-url> [idea-id]"; exit 1; }

DIR="office/production/$ID"
PY="python3 scripts/sermon_shorts.py"

command -v ffmpeg >/dev/null 2>&1 || bash scripts/setup_render_env.sh

step() { printf '\n\033[1m━━ %s\033[0m\n' "$*"; }

# 1 ─ 원본 -----------------------------------------------------------------
if ls "$DIR"/source/sermon.* >/dev/null 2>&1; then
  step "1/4 원본 — 이미 있음, 건너뜀"
else
  step "1/4 원본 내려받기"
  $PY fetch "$ID" --url "$URL"
fi

# 2 ─ 전사 -----------------------------------------------------------------
if [ -f "$DIR/transcript.json" ]; then
  step "2/4 전사 — 이미 있음, 건너뜀"
else
  step "2/4 한국어 전사"
  $PY transcribe "$ID" --backend "${BACKEND:-auto}"
fi

# 3 ─ 구간 선별 (사람) ------------------------------------------------------
step "3/4 구간 선별"
# validate 는 부작용이 없다. 통과하면 사람이 이미 채운 것이고,
# 실패하면 (파일이 없거나 템플릿 그대로면) 아직 사람 차례다.
if $PY validate "$ID" >/dev/null 2>&1; then
  echo "clips.json 준비됨 — 렌더로 진행"
else
  $PY clips "$ID"
  cat <<EOF

━━ 여기서 멈춘다 ━━
$DIR/clips.json 을 채운 뒤 같은 명령을 다시 실행하면 렌더까지 이어진다.

  - 30~90초 구간 3개
  - title / hook / reason 은 필수. reason 은 "왜 이 구간인가"를 문장으로.
  - 찬양이 깔린 구간은 has_worship_music: true
  - 회중석이 잡히면 congregation_visible: true
  - 목사님이 화면 한쪽에 서 있으면 crop: "left" 또는 "right"
EOF
  exit 0
fi

# 4 ─ 렌더 -----------------------------------------------------------------
step "4/4 렌더"
$PY render "$ID"

cat <<EOF

━━ 완료 ━━
렌더:   $DIR/renders/          (gitignore 대상)
승인용: $DIR/publish-package.md

업로드는 하지 않았다. 위 패키지를 확인하고 사람이 직접 올린다.
⚠️ 표시가 붙은 클립은 저작권/초상권 확인 전 업로드 금지.
EOF
