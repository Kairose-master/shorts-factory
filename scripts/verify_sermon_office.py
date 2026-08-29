#!/usr/bin/env python3
"""sermon-office/ 검증 — 구조, 백로그 산술, 근거 추적, 자세 등급.

이 오피스의 위험은 "쇼츠가 안 만들어지는 것"이 아니라 "목사님이 하지 않은 말이
쇼츠에 들어가는 것"이다. 검증기가 실제로 막는 것은 그쪽이다.

  · 백로그의 독립성 점수가 논리 지도의 값과 다르면 판단이 사실처럼 보인다
  · 대본의 QUOTE 줄에 음성 대조 표시가 없으면 자막 오류가 그대로 화면에 나간다
  · 근거 없는 대본 줄은 출처가 없는 주장이다

사용법: python3 scripts/verify_sermon_office.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OFFICE = ROOT / "sermon-office"
POSTURES = {"QUOTE", "RECONSTRUCTED", "EDITORIAL"}
PILLARS = set("ABCDEF")
REQUIRED = [
    "CHARTER.md",
    "README.md",
    "research/channel-model.md",
    "memory/backlog.md",
    "memory/hooks.md",
    "memory/published.md",
    "memory/rejected.md",
    "memory/experiments.md",
    "memory/analytics.md",
    "memory/lessons.md",
    "sop/ingest.md",
    "sop/logic-analysis.md",
    "sop/production-pipeline.md",
    "sop/quality-control.md",
    "sop/analytics-loop.md",
]

errors, warnings = [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def check_structure():
    for rel in REQUIRED:
        if not (OFFICE / rel).is_file():
            err(f"필수 문서 없음: sermon-office/{rel}")
    model = OFFICE / "research" / "channel-model.md"
    if model.is_file() and "DO NOT CLAIM" not in model.read_text(encoding="utf-8"):
        err("channel-model.md 에 DO NOT CLAIM 원장이 없음 — QC 게이트 6이 대조할 대상이 사라짐")


def load_logic_independence(sermon_id):
    """논리 지도에서 단위별 독립성 점수를 읽는다. {'U5': 10, ...}"""
    lm = OFFICE / "sermons" / sermon_id / "logic-map.md"
    if not lm.is_file():
        return None
    text = lm.read_text(encoding="utf-8")
    out, unit = {}, None
    for line in text.splitlines():
        m = re.match(r"##\s+(U\d+)\b", line)
        if m:
            unit = m.group(1)
            continue
        if unit and "독립성" in line and line.lstrip().startswith("|"):
            m = re.search(r"\*\*(\d+)\*\*|\|\s*(\d+)\s*\|", line)
            if m:
                out[unit] = int(m.group(1) or m.group(2))
                unit = None
    return out


def check_backlog():
    path = OFFICE / "memory" / "backlog.md"
    if not path.is_file():
        return
    rows = [l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("| SS-")]
    if not rows:
        warn("백로그에 항목이 없음")
        return

    seen, prev = set(), None
    cache = {}
    for line in rows:
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) != 16:
            err(f"{c[0] if c else '?'}: 열이 16개가 아님 ({len(c)}개)")
            continue
        rid, pillar, sermon, unit, posture = c[0], c[2], c[3], c[4], c[6]

        try:
            H, I, U, V, N, D = (int(c[i]) for i in range(7, 13))
            pri = int(c[13].strip("*"))
        except ValueError:
            err(f"{rid}: 점수 칸에 숫자가 아닌 값")
            continue

        calc = H * 3 + I * 2 + U * 2 + V + N - D * 2
        if calc != pri:
            err(f"{rid}: Pri 가 {pri} 인데 공식은 {calc}")
        if any(not 0 <= x <= 10 for x in (H, I, U, V, N, D)):
            err(f"{rid}: 0-10 범위를 벗어난 점수")
        if rid in seen:
            err(f"{rid}: 중복 ID — ID 는 재사용하지 않는다")
        seen.add(rid)
        if not re.fullmatch(r"SS-\d{3}[a-z]?", rid):
            err(f"{rid}: ID 형식이 SS-NNN 이 아님")
        if prev is not None and pri > prev:
            err(f"{rid}: 정렬 어긋남 ({pri} 가 {prev} 뒤에 옴)")
        prev = pri

        if posture not in POSTURES:
            err(f"{rid}: 자세 {posture!r} 가 {sorted(POSTURES)} 중에 없음")
        if pillar not in PILLARS:
            err(f"{rid}: 기둥 {pillar!r} 가 A-F 가 아님")

        # 근거 추적: 설교와 단위가 실재하고, 독립성이 논리 지도와 일치하는가
        if not (OFFICE / "sermons" / sermon).is_dir():
            err(f"{rid}: 설교 {sermon} 가 sermons/ 에 없음 — 근거 없는 백로그 항목")
            continue
        if sermon not in cache:
            cache[sermon] = load_logic_independence(sermon)
        indep = cache[sermon]
        if indep is None:
            err(f"{rid}: {sermon}/logic-map.md 가 없음 — 논리 재분석 없이 백로그에 올라옴")
        elif unit not in indep:
            err(f"{rid}: 단위 {unit} 가 {sermon}/logic-map.md 에 없음")
        elif indep[unit] != I:
            err(f"{rid}: 독립성이 백로그 {I} · 논리 지도 {indep[unit]} — 두 값은 같아야 한다")
        elif I < 7:
            err(f"{rid}: 독립성 {I} — 7 미만은 쇼츠 후보가 아니다 (logic-analysis.md 4단계)")


def check_sermons():
    d = OFFICE / "sermons"
    if not d.is_dir():
        return
    for meta_path in sorted(d.glob("*/meta.json")):
        sid = meta_path.parent.name
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{sid}: meta.json 파싱 실패 — {e}")
            continue
        for field in ("sermon_id", "video_id", "sermon_start_ms_estimated",
                      "quote_audio_verified", "caption_kind"):
            if field not in meta:
                err(f"{sid}: meta.json 에 {field} 없음")
        if meta.get("sermon_id") != sid:
            err(f"{sid}: meta.json 의 sermon_id 가 폴더명과 다름 ({meta.get('sermon_id')})")
        if meta.get("caption_kind") == "asr" and meta.get("quote_audio_verified"):
            warn(f"{sid}: 자동 자막인데 quote_audio_verified=true — 누가 대조했는지 기록되어야 함")
        if (meta_path.parent / "summary.md").is_file() and \
           not (meta_path.parent / "logic-map.md").is_file():
            warn(f"{sid}: 요약은 있는데 논리 지도가 없음 — 백로그로 갈 수 없다")


def check_scripts():
    """대본의 모든 내용 줄은 자세 등급을 달고, QUOTE 는 음성 대조를 통과해야 한다."""
    d = OFFICE / "production"
    if not d.is_dir():
        return
    for script in sorted(d.glob("*/script.md")):
        pid = script.parent.name
        in_body = False
        tagged = quotes = verified = 0
        for i, line in enumerate(script.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("## 대본"):
                in_body = True
                continue
            if in_body and line.startswith("## "):
                in_body = False
            if not in_body:
                continue
            s = line.strip()
            if not s or s.startswith(("|", ">", "-", "#", "`")):
                continue
            m = re.match(r"\[(QUOTE|RECONSTRUCTED|EDITORIAL)\b([^\]]*)\]", s)
            if not m:
                err(f"{pid}/script.md:{i}: 자세 등급 없는 대본 줄 — 근거 없는 주장")
                continue
            tagged += 1
            if m.group(1) == "QUOTE":
                quotes += 1
                if "음성대조 ✅" not in m.group(2):
                    err(f"{pid}/script.md:{i}: QUOTE 인데 '음성대조 ✅' 표시가 없음 "
                        f"— 자동 자막을 인용하면 헌장 하드 룰 1 위반")
                else:
                    verified += 1
            if m.group(1) != "EDITORIAL" and not re.search(r"\d{1,2}:\d{2}", m.group(2)):
                err(f"{pid}/script.md:{i}: {m.group(1)} 인데 타임코드 근거가 없음")
        if tagged == 0:
            warn(f"{pid}/script.md: '## 대본' 절을 찾지 못했거나 내용이 없음")
        else:
            print(f"  {pid}/script.md — {tagged}줄 태깅 · QUOTE {verified}/{quotes} 대조됨")


def check_quote_provenance():
    """자세가 QUOTE 인 항목은, 렌더가 존재한다면 자막 검증 증거가 있어야 한다.

    노란 자막은 화면에서 '목사님이 이렇게 말했다' 고 주장한다. ASR 초안으로
    렌더한 것을 QUOTE 라고 부르면 헌장 하드 룰 1 위반이다.
    """
    path = OFFICE / "memory" / "backlog.md"
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| SS-"):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) != 16 or c[6] != "QUOTE":
            continue
        rid = c[0]
        d = OFFICE / "production" / rid
        if not d.is_dir():
            continue
        rendered = (d / "renders" / "final.mp4").is_file()
        verified = (d / "captions" / "captions-verified.json").is_file()
        status = c[15]
        if rendered and not verified:
            if "승인" in status and "대기" not in status:
                err(f"{rid}: QUOTE 인데 captions-verified.json 없이 승인 상태 — "
                    f"자막이 검증되지 않았다")
            else:
                warn(f"{rid}: QUOTE 렌더가 있으나 captions/captions-verified.json 이 없음 "
                     f"— 아직 QUOTE 가 아니다 (음성 대조 겸 자막 교정 필요)")
        if verified:
            try:
                meta = json.loads((d / "captions" / "captions-verified.json")
                                  .read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                err(f"{rid}: captions-verified.json 파싱 실패 — {e}")
                continue
            if meta.get("posture") != "QUOTE":
                err(f"{rid}: captions-verified.json 의 posture 가 QUOTE 가 아님")
            print(f"  {rid} — 자막 검증됨 · {meta.get('cue_count')}큐 · "
                  f"{meta.get('sermon')}")


def check_published():
    p = OFFICE / "memory" / "published.md"
    if not p.is_file():
        return
    rows = [l for l in p.read_text(encoding="utf-8").splitlines()
            if l.startswith("| SS-")]
    for line in rows:
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) > 6 and not c[6]:
            err(f"{c[0]}: 게시 기록에 승인자가 비어 있음 — 승인 없는 게시는 헌장 자율경계 1 위반")


def main():
    print("sermon-office 검증\n")
    check_structure()
    check_backlog()
    check_sermons()
    check_scripts()
    check_quote_provenance()
    check_published()

    for w in warnings:
        print(f"  경고  {w}")
    for e in errors:
        print(f"  오류  {e}")
    print()
    if errors:
        print(f"FAILED — 오류 {len(errors)}건, 경고 {len(warnings)}건")
        return 1
    print(f"OK — 오류 없음, 경고 {len(warnings)}건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
