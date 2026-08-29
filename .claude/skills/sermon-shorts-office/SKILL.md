---
name: sermon-shorts-office
description: 방배동 예심교회(@yeshim1126) 설교 영상을 쇼츠로 만드는 모든 요청에 먼저 호출한다 — 새 설교 수집, 설교 요약, 논리적 재분석(논증 재구성), 쇼츠 각도 도출, 훅·대본 작성, 제작, 품질 검사, 게시 승인 요청, 성과 측정. 오피스의 14단계 파이프라인, 자세 등급(QUOTE/RECONSTRUCTED/EDITORIAL), 자율 경계(사람 승인 없이 게시 금지), 목사님이 하지 않은 말을 만들지 않는 규칙, 그리고 설치된 다른 스킬들로의 라우팅을 소유한다. Use for any request about the 예심교회 sermon channel, sermon shorts, sermon summarization, sermon logic analysis, or Korean church short-form video.
---

# 예심교회 설교 쇼츠 오피스

`sermon-office/` 에 사는 상시 콘텐츠 운영. 아래를 실행하기 전에
**`sermon-office/CHARTER.md` 를 읽는다** — 헌장이 법이고 이 파일은 라우팅표다.

> 이 스킬은 `shorts-factory` **위에** 있다. `shorts-factory` 는 일반 리서치
> 파이프라인과 43개 upstream 스킬을 소유한다. 이 스킬은 예심교회 채널,
> 오피스의 기억, 승인 경계, 그리고 **남의 설교를 다룰 때의 제약**을 소유한다.
> 이 채널 관련 요청은 여기서 시작한다.

## 무엇보다 먼저

1. **`sermon-office/research/channel-model.md` 를 읽는다.** 모든 쇼츠의 모든
   사실 주장이 이 문서의 한 줄로 추적되어야 한다.
2. **§8 DO NOT CLAIM 원장을 읽는다.** 8개 항목. QC 게이트 6이 한 줄씩 대조한다.
3. **§5 자막 품질을 읽는다.** 자동 자막은 **교회 어휘에서 체계적으로 틀린다**
   (`사순절 → 사진들`, `기업 → 기여`, `천국 문 → 전국문`). 이것이 자세 등급이
   존재하는 이유다.
4. **`sermon-office/memory/` 를 확인한다** — backlog · hooks · rejected · lessons.
   거부된 개념을 다시 생성하거나 버린 훅을 다시 제안하지 않는다.

## 절대 굽지 않는 두 규칙

**1. 목사님이 하지 않은 말을 하게 하지 않는다.**

모든 문장은 셋 중 하나다:

| 등급 | 화면에 허용되는 것 |
|---|---|
| **QUOTE** | 목사님 발화로 표기 가능. **음성 대조 완료 필수** |
| **RECONSTRUCTED** | 나레이션 가능. **따옴표 금지**, 목사님 발화로 표기 금지 |
| **EDITORIAL** | 명백히 제작자의 목소리 |

자막에서 복사한 것은 QUOTE가 아니다. **EDITORIAL을 QUOTE처럼 보이게 하면
위조이고 자동 REJECT다.**

**2. 사람 승인 없이 아무것도 게시하지 않는다.**

승인권자는 **채널 소유자(담임 장선기 목사)** 다. 매번, 사전 포괄 승인 없음.
"테스트 업로드"도 게시다. 함께 승인이 필요한 것: 유료 API 지출, 교리적 판단,
오피스 밖 접촉, 돈·권한·자격증명, 기록 삭제.

그 밖의 전부 — 수집·요약·논리 재분석·아이디어·훅·대본·장면 계획·무료 렌더·
QC·`sermon-office/memory/` 기록 — 는 묻지 않고 실행한다.

## 라우팅

| 요청 | 가는 곳 |
|---|---|
| "새 설교 올라왔나" / "설교 가져와" | `sermon-office/sop/ingest.md` → 저장소 루트의 `sermon_ingest.py` |
| "이 설교 요약해줘" | `transcript-intelligence` → `sermons/<id>/summary.md` |
| **"논리적으로 재분석해줘"** | **`sermon-office/sop/logic-analysis.md`** — 이 오피스의 핵심 공정 |
| "쇼츠 아이디어 뽑아줘" | **논리 지도의 독립성 7 이상 단위** → 다섯 축. 브레인스토밍 금지 |
| "훅 써줘" | `viral-hooks` → 변형 전부 `memory/hooks.md` 에 기록 |
| "이 훅 어때" | `hook-anatomy` |
| "대본 써줘" | `viral-short-form` → `viral-youtube-shorts` |
| "화면에 뭐 띄우지" | `asset-hunter`; 빈 곳은 `motion-designer` |
| **"클립으로 쇼츠 만들어줘" (기둥 E)** | **`sermon-office/brand/shorts-format.md`** → `production/_engine/build_short.py` |
| "영상 만들어줘" (기둥 A–D·F) | `openmontage` (+ `voicebox` 나레이션, `penpot` 정적 요소) |
| "자막 어떻게 다나" | `brand/shorts-format.md` §자막 교정 루프 — 교정이 곧 음성 대조다 |
| "이거 나가도 되나" | `sermon-office/sop/quality-control.md` — 아홉 게이트 |
| "캡션 써줘" | `viral-captions-and-ctas` → `platform-fluency` |
| "올려줘" | **정지. 패키징하고 승인을 요청한다.** |
| "성과 어때" | `sermon-office/sop/analytics-loop.md` → `comment-mining`, `read-the-room` |
| "시청자가 누구야" | `comment-mining` (유료) · `read-the-room` (무료) — **아직 미조사** |
| "이 채널 다시 조사해줘" | `scrapecreators-api` → `research/runs/` 에 Method 블록과 함께 |

가장 **좁은** 스킬을 고른다. `viral-hooks` 는 생성하고 `hook-anatomy` 는 진단한다.

## 아이디어는 어디서 오나 — 생성기

**브레인스토밍하지 않는다.** 백로그는 생성된다:

```
설교 → 논증 단위 → 독립성 점수 → 다섯 축 → 백로그 한 행
```

`sermon-office/sop/logic-analysis.md` 의 5단계를 따른다. 요약:

1. 설교를 논증 단위(U1…Un)로 자른다 — 전환어와 절 번호 재언급이 경계다
2. 각 단위를 Toulmin 골격으로 재구성 — 본문·주장·근거·**전제**·한정·반론·적용
3. 근거를 유형으로 표시 — `T` 본문 · `C` 문맥 · `D` 교리 · `I` 예화 · `E` 경험 · `A` 적용확장
4. **독립성 0–10** 을 매긴다. **7 미만은 쇼츠 후보가 아니다**
5. 다섯 축(논증·긴장·본문·적용·반전)에서 **성립하는 것만** 뽑는다

**전제 칸이 비면 그 단위는 분석되지 않은 것이다.** 모든 논증에 다리가 있다.
못 찾았으면 `(찾지 못함)` 이라고 적는다 — 채워 넣지 않는다.

**논리 재분석의 목적은 비평이 아니라 선별이다.** 산출물은 "이 설교의 논리에
문제가 있다"가 아니라 "어떤 주장이 40분의 문맥 없이 60초 안에서 혼자 설 수
있는가"다. 논리 지도는 **오피스 내부 문서이며 게시되지 않는다.**

## 기둥 E의 시각 포맷

레퍼런스는 갓피플TV(@GODpeopleTV). 규격은 `sermon-office/brand/shorts-format.md`
가 소유하고, `production/_engine/build_short.py` 가 구현한다.

```
상단 8–21%   흰색 대형 훅 2줄     = EDITORIAL (오피스가 쓴 말)
중앙          설교 영상 9:16 크롭
하단 ~78%    노란 자막 #FFE000    = QUOTE (목사님이 한 말)
81.7% 이하    유튜브 UI — 침범 금지
```

**두 색이 다른 것은 디자인이 아니라 자세 등급의 시각적 구현이다.** 흰 글씨에
목사님 말을 넣거나 노란 글씨에 오피스가 지어낸 말을 넣으면 등급 위조다.

**자막 교정 루프 — 이 포맷의 핵심 공정:**

```
build_short.py            → captions/captions-draft.tsv  (ASR, RECONSTRUCTED)
build_short.py --verify   → renders/verify.mp4
사람: verify.mp4 를 들으며 draft.tsv 를 고친다  ← 이 행위가 곧 음성 대조다
build_short.py --captions <고친파일>  → QUOTE + captions/captions-verified.json
```

`captions-verified.json` 이 없는 렌더는 노란 자막이 있어도 **QUOTE가 아니다.**
검증기가 확인한다.

**길이 기본값 40–60초** (35–50초 우선). 벤치마크 중앙값은 66초다 — 설교 쇼츠는
일반 숏폼 조언보다 길다. 논증을 깨면서까지 줄이지 않는다.

**소스 영상은 채널 소유자가 공급한다.** 이 컨테이너는 YouTube 다운로드가
차단되어 있다(교훈 L-07). `--still` 은 레이아웃 확인용이며 게시물이 아니다.

## 기둥 — E가 기본값이다

| | 기둥 | 기본 등급 |
|---|---|---|
| A | 본문 한 구절 | RECONSTRUCTED |
| B | 질문과 대답 (설교가 답하는 반론) | RECONSTRUCTED |
| C | 오늘의 적용 | RECONSTRUCTED |
| D | 성경 배경 | RECONSTRUCTED |
| **E** | **설교 클립 — 실제 설교 30초 + 번인 자막** | **QUOTE** |
| F | 시리즈 관통선 (현재 에스겔 연속강해) | RECONSTRUCTED |

채널에는 이미 **1,268편의 실제 설교 영상**이 있고 **쇼츠는 0편**이다. 가장 싸고
가장 진짜인 쇼츠는 합성이 아니라 **잘라내기**다. 다만 이 판단은 아직 검증되지
않았다 — 실험 **E-01**이 그것을 시험한다.

## 이 오피스가 만들지 않는 것

`research/channel-model.md` §8 전체를 읽되, 가장 자주 걸리는 것:

- **조건부 축복.** "이렇게 하면 복 받는다", 헌금·치유·재정 성공 보장.
  설교 원문에 있어도 훅이나 CTA로 승격시키지 않는다.
- **정치·이민·조세·타 교단.** 설교 안에 있다는 사실이 쇼츠 소재가 될 이유는
  아니다. 실제 거부 사례 두 건이 `memory/rejected.md` R-01·R-02 에 있다.
- **성도 개인 사연·실명.** 당사자 동의를 오피스가 받을 수 없다.
- **설교에 없는 교리적 입장.** 이견이 생기면 만들지 않고 사람에게 올린다.
- **목사님 음성 클론.** 승인 없이 시도하지 않는다.
- **성장·인기 과장.** 실측은 구독자 174명, 최근 30편 중앙값 11.5회다.

## 사이클

```
수집 → 요약 → 논리 재분석 → 각도 → 백로그 → 훅 → 대본 → 샷·자산 →
게이트 → 제작 → QC → 패키징 → 승인 → 게시 → 측정 → 버킷 → 교훈 → 다시 수집
```

전체 단계표: `sermon-office/sop/production-pipeline.md`

## 상시 규칙

- **한 쇼츠에 한 논증.** 두 번째 논증은 두 번째 쇼츠다.
- **성경 장·절을 화면에 표기한다.** 시청자가 확인할 수 있어야 한다.
- **자막은 언제나 번인.** 대부분 무음으로 본다.
- **CTA는 전편 설교로 보낸다.** 쇼츠가 설교를 대체한다고 말하지 않는다.
- **한 실험에 한 변수.** 두 팔, 게시 **전에** 가설 기록.
- **관측 1회는 교훈이 아니다.** `관측 N회` 없는 교훈은 의견이다.
- **거부를 기록한다** — 살릴 것과 함께.
- 조회수 원값은 성과가 아니다. 실측 baseline 대비로만.
- 바이럴을 약속하지 않는다.

## 비용 게이트

**무료:** Piper · eSpeak · Remotion · FFmpeg · 모든 산문 스킬 · `read-the-room` ·
기둥 E(원본 영상 잘라내기) · `verify_sermon_office.py` · `sermon_ingest.py --selftest`

**과금:** ScrapeCreators(수집 1 + 자막/댓글 각 1 credit) · Apify · TubeLab ·
Gemini · 모든 생성형 provider.

계획이 몇 호출을 할지 **먼저** 말한다. `sermon_ingest.py` 는 기본 dry-run이며
`--fetch` 없이는 과금하지 않는다.

## 검증

```bash
python3 ./scripts/sermon_ingest.py --selftest      # 제목 파서 회귀 테스트
python3 ./scripts/verify_sermon_office.py          # 구조·백로그 산술·근거 추적·QUOTE 증거
```

백로그를 고칠 때마다, 대본을 쓸 때마다 돌린다. 검증기는 백로그의 독립성 점수를
논리 지도의 값과 대조하고, 대본의 QUOTE 줄에 음성 대조 표시가 있는지 확인한다.
