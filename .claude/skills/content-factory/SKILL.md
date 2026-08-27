---
name: content-factory
description: This skill should be used when the user asks to produce, select, QA, publish-queue, or analyze short-form content as a pipeline — "다음 에피소드 만들어", "아이디어 뽑아", "발행 큐 정리", "성과 확인", "훅 토너먼트", or any GENERATE→LEARN loop request. It loads the user's Content Factory master prompt as the single source of truth for gates, scoring, and output format.
---

# Content Factory 운영 스킬

## 발동 시 반드시

1. `factory/MASTER-PROMPT-v1.md`를 읽고 그 절차·게이트·출력형식(§18)을 따른다.
   이 파일이 SSOT다 — 이 스킬 문서는 색인일 뿐이다.
2. 시리즈 Canon이 있으면 함께 읽는다 (자유중국: `projects/jayu-china/canon/`).
3. 제작 전 §19 세 질문에 답을 명기한다. 답 없으면 제작 금지.

## 상태 파일

- 발행 큐·예측: `factory/queue.json` (§12, §14)
- 성과 스냅샷: `python3 factory/analytics.py` → `factory/analytics.jsonl` (§13, 영상당 1크레딧)

## 토큰 규율 (factory/README.md 상세)

- 렌더/QC/성과 수집은 스크립트로 — LLM은 대본·검수·판정만.
- 새 에피소드는 `projects/jayu-china/ep3-short/`를 템플릿으로 복제.
- 기계적 다건 처리(아이디어 1차 스코어링 등)는 Agent `model: haiku` 팬아웃.
- 적대 검수(§7)는 작성 맥락과 분리된 별도 Agent로 실행한다.

## 핵심 게이트 요약

- Q = 0.25H+0.20C+0.15V+0.15R+0.15P+0.10N — 80+ RELEASE, 70~79 REVISE, <70 HOLD.
- 치명적 사실 오류·Canon 충돌 → 점수 무관 발행 금지, RETURN TO STAGE.
- 발행 결정·Canon 변경·상위 아이디어 선정은 사용자(Editor-in-Chief) 체크포인트.
- 생산량 ≠ 발행량. 탈락물은 HOLD/REVISE/ARCHIVE로 queue.json에 기록.
