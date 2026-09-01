#!/usr/bin/env bash
# 주간 반복 실행 — 주일 설교 한 편 → 쇼츠 후보 렌더.
#
#   bash scripts/weekly_run.sh <유튜브-URL> [idea-id]
#   bash scripts/weekly_run.sh --auto <유튜브-URL> [idea-id]   전부 자동
#   bash scripts/weekly_run.sh --auto                          영상까지 알아서 고름
#
# URL을 생략하면 채널 streams 탭에서 아직 안 만든 주일예배를 무작위로 하나
# 뽑는다(`sermons --pick`). idea-id는 그 예배 날짜에서 나온다 — 오늘 날짜가
# 아니다. 주일이 아닌 날에 돌려도 SUN-<그 주일> 이 붙는다.
#
# 기본값은 구간 선별에서 **멈추는 것**이다. 전사본을 읽고 clips.json 을 채운 뒤
# 다시 실행하면 이어서 렌더한다.
#
# --auto 를 붙이면 그 선별까지 모델이 한다(전사본을 읽고 고른다 — 키워드
# 휴리스틱이 아니다). 설교 구간 안쪽인지, 길이가 맞는지, 근거가 붙었는지는
# 선별 결과와 무관하게 파이프라인이 강제한다.
#
# 업로드는 어느 단계에서도 하지 않는다.
set -euo pipefail

cd "$(dirname "$0")/.."

AUTO=0
if [ "${1:-}" = "--auto" ]; then AUTO=1; shift; fi

URL=${1:-}
ID=${2:-}

if [ -z "$URL" ]; then
  # 아직 안 만든 주일예배 중에서 무작위. 메타데이터만 읽으므로 무료다.
  printf '\n\033[1m━━ 대상 선정\033[0m\n'
  PICK=$(python3 scripts/sermon_shorts.py sermons --pick) || exit 1
  URL=$(printf '%s\n' "$PICK" | sed -n 1p)
  [ -n "$ID" ] || ID=$(printf '%s\n' "$PICK" | sed -n 2p)
  echo "$URL"
fi
[ -n "$ID" ] || ID=SUN-$(date +%F)

# zsh does not treat `#` as a comment the way bash does, so a copied line with
# a trailing note arrives here as arguments. Say that, rather than handing
# yt-dlp a `#` and letting it fail three layers down.
case "$URL" in
  http://*|https://*) ;;
  *)
    echo "URL이 아니다: '$URL'" >&2
    echo >&2
    echo "  붙여넣은 줄에 주석(# ...)이 딸려 오지 않았는지 보라 — zsh는 bash와" >&2
    echo "  달리 #를 주석으로 취급하지 않아 그대로 인자가 된다." >&2
    echo >&2
    echo "  URL 없이 채널에서 알아서 고르게 하려면 인자를 아무것도 주지 않는다:" >&2
    echo "    bash scripts/weekly_run.sh --auto" >&2
    exit 1 ;;
esac

case "$ID" in
  SUN-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;;
  *) echo "경고: idea-id '$ID' 가 SUN-YYYY-MM-DD 모양이 아니다." >&2 ;;
esac

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
elif [ "$AUTO" = 1 ]; then
  # 사람 대신 모델이 전사본을 읽고 고른다. 설교 구간·길이·근거는
  # 선별 결과와 무관하게 파이프라인이 강제한다.
  $PY select "$ID" --count 3
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

멈추지 않고 끝까지 가려면 --auto 를 붙인다:
  bash scripts/weekly_run.sh --auto "$URL" $ID
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
