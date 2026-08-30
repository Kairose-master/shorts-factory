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
| `brand/shorts-format.md` | 기둥 E 시각 규격 · 자막 교정 루프 |
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
├── brand/shorts-format.md        기둥 E 시각 규격 (레퍼런스 포맷)
├── sop/                          ingest · logic-analysis · production-pipeline
│                                 quality-control · analytics-loop
├── sermons/<sermon-id>/          meta.json · transcript.json(gitignore)
│                                 summary.md · logic-map.md
└── production/
    ├── _engine/build_short.py    9:16 클립 렌더러
    └── <쇼츠-id>/                plan · script · qc · captions/  (renders/ 는 gitignore)
```

## 사이클 시작

**`sermon-shorts-office` 스킬을 호출한다.** 라우팅 테이블을 갖고 있다.

## 명령

```bash
python3 scripts/sermon_ingest.py --selftest        # 무과금 · 파서 회귀 테스트
python3 scripts/sermon_ingest.py --list            # 1 credit · 신규 설교 확인
python3 scripts/sermon_ingest.py --fetch --limit 3 # 1+3 credits · 자막까지
python3 scripts/verify_sermon_office.py            # 무과금 · 구조·근거·QUOTE 증거 검증

# 기둥 E 클립 렌더 (소스 영상 필요)
python3 sermon-office/production/_engine/build_short.py --help

# 기둥 A–D·F 나레이션 렌더 (소스 영상 불필요)
python3 sermon-office/production/_engine/build_narration.py --help
```

`verify_sermon_office.py`는 백로그를 고칠 때마다 돌린다. 백로그의 독립성 점수를
논리 지도의 값과 대조하고, 대본의 QUOTE 줄에 음성 대조 표시가 있는지 확인한다.

## 현황

- **게시 0편.** 채널 소유자(담임 장선기 목사)의 명시적 승인 없이는 게시되지 않는다.
- **논리 재분석 완료 2편** — `S-20260828-EZK47`(단위 5개 중 3개 후보) ·
  `S-20230101-hOnq3aZDGd0`(단위 3개 중 1개 후보)
- **백로그 7건**
- **완결 5편, 승인 대기** — SS-001(나레이션, PASS 35/45) · SS-002(E-음성 봉독, PASS 39/45)
  · SS-004(E-음성 해설, PASS 38/45) · SS-007(E-촬영, PASS 41/45)
  · **SS-008(E-촬영, PASS 42/45 — 최고점, 화면 슬라이드로 ASR 오류 교정)**
- **나레이션 포맷 사용 중단, 주일예배(E-촬영) 우선.** 채널 소유자 요청 —
  실제 음성·영상 클립만, 그중에서도 아버님 얼굴이 나오는 주일예배 촬영본 우선
- **수집된 설교 4편** — 겔47 새벽기도 2편 · 「테바」 주일예배(2023) ·
  「용서」 주일예배(2026)
- **수집된 설교 3편** — 겔47 새벽기도 2편 + 「테바를 타고 가는 인생」 주일예배 1편
- **벤치마크 조사 완료** — 갓피플TV 쇼츠 48편. 길이 기본값을 40–60초로 교정
- **사람이 풀어야 하는 차단 3개:**
  1. **소스 영상** — `googlevideo.com` 이 egress 정책으로 차단(L-07). 봇 확인이
     아니라 정책 거부이므로 우회 불가. 채널 소유자가 YouTube Studio에서 공급.
     **기둥 E 만 막힌다** — 기둥 A–D·F 는 소스 없이 렌더된다(L-08)
  2. **자막 교정 = 음성 대조** — `brand/shorts-format.md` §자막 교정 루프
  3. **리텐션·완주율** — 어떤 API로도 불가. `memory/analytics.md`
