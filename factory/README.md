# Content Factory — 운영 스캐폴딩

`MASTER-PROMPT-v1.md`(사용자 정본, §0 원칙 5의 SSOT)를 실행 가능한 형태로 내린 것.
발동은 `.claude/skills/content-factory/SKILL.md` 경유.

## 루프 → 도구 매핑

| 단계 | 도구 | LLM 토큰 |
|---|---|---|
| GENERATE (아이디어·훅 토너먼트 §2-3) | LLM — 세션 내, 정본 §18 형식 | 소 |
| VERIFY (§5-7 팩트·캐논·적대 검수) | LLM — Reviewer 역할 분리 | 소 |
| SELECT (§10-11) | queue.json 판정 기록 | 0 |
| PRODUCE (§4, 8) | `gen_vo.py`/`render.py` 템플릿 복제 — ep3-short가 참조 구현 | 0 (대본만 LLM) |
| QA (§9) | 프레임 시트 스크립트 + 육안 검수 | 소 (프레임 읽기) |
| QUEUE (§12) | `queue.json` | 0 |
| OBSERVE (§13) | `analytics.py` (ScrapeCreators, 영상당 1크레딧) — 24H/72H/7D 트리거 | 0 |
| LEARN (§14-15) | `analytics.jsonl` + queue의 prediction 대조 — 표본 20+ 전 규칙 변경 금지 | 소 |

## 토큰 재활용 규칙 (반복작업)

1. **렌더·QC·성과 수집은 전부 스크립트** — LLM 토큰 0. 새 에피소드의 신규 LLM 작업은
   대본과 장면 설계뿐이다.
2. **템플릿 재사용**: `projects/jayu-china/ep3-short/{gen_vo,render}.py`가 70초 포맷의
   참조 구현. 새 EP는 LINES와 장면 빌더만 교체한다. 좌표 안전 규칙(베이스 1240×2200,
   장면 요소 y 540~1410, 칩 밴드 회피)은 ep3 storyboard에 명문화되어 있다.
3. **정본은 디스크에**: 마스터 프롬프트를 대화에 다시 붙이지 않는다 — 스킬이 파일을
   읽는다. 세션 프롬프트 캐시(1h TTL)가 반복 참조를 재활용한다.
4. **기계적 팬아웃은 저비용 모델로**: 다건 아이디어 스코어링·후보 정리 같은 기계적
   단계는 Agent 도구에 `model: haiku`로 위임한다. 판정·검수(§7)는 본 모델 유지.
5. **분석은 append-only JSONL** — 재수집 없이 누적 스냅샷으로 시계열을 만든다.

## 파일

- `MASTER-PROMPT-v1.md` — 정본 (변경 금지)
- `queue.json` — §12 발행 큐 + §14 예측 (T0 실측 2026-08-27 시드)
- `analytics.py` — §13 스냅샷 수집기
- `analytics.jsonl` — 스냅샷 누적 (gitignore 대상 아님 — 학습 데이터)
