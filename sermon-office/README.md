# 예심교회 설교 쇼츠 오피스

**방배동 예심교회**(`@yeshim1126`) 채널의 설교를 요약하고 논리적으로 재구성해
쇼츠로 만드는 상시 콘텐츠 운영. 실행 폴더가 아니라 **오피스의 기억**이므로
커밋된다.

Handsel Growth Office(`office/`)와 같은 골격을 쓰되, **남의 설교를 다룬다**는
사실에서 나오는 제약이 얹혀 있다. 그 제약이 이 오피스의 본체다.

## 읽는 순서

| 문서 | 내용 |
|---|---|
| `CHARTER.md` | 미션 · 역할 · 자율 경계 · **자세 등급** · 기둥 · 하드 룰 |
| `research/channel-model.md` | 검증된 채널 사실 + **DO NOT CLAIM 원장** |
| `sop/logic-analysis.md` | 논리 재분석 — 이 오피스의 핵심 공정 |
| `memory/backlog.md` | 설교에서 도출된 쇼츠 후보 |
| `sop/production-pipeline.md` | 14단계 |
| `sop/quality-control.md` | 아홉 게이트와 거부권 |
| `sop/analytics-loop.md` | 결과가 교훈이 되는 경로 |

## 구조

```
sermon-office/
├── CHARTER.md
├── research/
│   ├── channel-model.md          검증된 사실 + DO NOT CLAIM
│   └── runs/                     조사 보고서 (Method 블록 필수)
├── memory/                       backlog · hooks · published · rejected
│                                 experiments · analytics · lessons
├── sop/                          ingest · logic-analysis · production-pipeline
│                                 quality-control · analytics-loop
├── sermons/<sermon-id>/          meta.json · transcript.json(gitignore)
│                                 summary.md · logic-map.md
└── production/<쇼츠-id>/          plan · hooks · script · qc  (렌더는 gitignore)
```

## 사이클 시작

**`sermon-shorts-office` 스킬을 호출한다.** 라우팅 테이블을 갖고 있다.

## 명령

```bash
python3 scripts/sermon_ingest.py --selftest        # 무과금 · 파서 회귀 테스트
python3 scripts/sermon_ingest.py --list            # 1 credit · 신규 설교 확인
python3 scripts/sermon_ingest.py --fetch --limit 3 # 1+3 credits · 자막까지
python3 scripts/verify_sermon_office.py            # 무과금 · 구조·근거 검증
```

`verify_sermon_office.py`는 백로그를 고칠 때마다 돌린다. 백로그의 독립성 점수를
논리 지도의 값과 대조하고, 대본의 QUOTE 줄에 음성 대조 표시가 있는지 확인한다.

## 현황

- **게시 0편.** 채널 소유자(담임 장선기 목사)의 명시적 승인 없이는 게시되지 않는다.
- **수집된 설교 2편** — `S-20260828-EZK47`, `S-20260827-EZK47`
- **논리 재분석 완료 1편** — `S-20260828-EZK47` (단위 5개 중 3개가 쇼츠 후보)
- **백로그 6건**, 전부 무료 제작 가능
- **제작됨 1편** — SS-001, 승인 대기
- **최대 역량 공백:** 리텐션·완주율 지표에 접근할 수 없다. 채널 소유자의
  YouTube Studio가 필요하다. `memory/analytics.md` 참조.
