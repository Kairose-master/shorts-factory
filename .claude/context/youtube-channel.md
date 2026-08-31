# YouTube Channel Context

## Channel Information
- **Channel Name:** 방배동 예심교회
- **Channel Handle:** @yeshim1126
- **Channel ID:** _미확인_ — `UC`로 시작하는 24자. 아래 "채널 ID 얻는 법" 참조.
  추측해서 채우지 말 것.

## Niche & Positioning
- **Primary Niche:** 설교 클립 / 한국 개신교 지역교회
- **Content Style:** 주일설교 발췌형 쇼츠 — 9:16, 한국어 자막 번인, 원본 음성 그대로
- **Target Audience:** 교인 · 지역 주민 · 비신자

## Content Strategy
- **Typical Video Length:** 쇼츠 30~90초 / 원본 설교 30~50분
- **Upload Frequency:** 주 1회 (주일 설교 기준)
- **Best Performing Topics:** _데이터 없음_ — 실제 발행 후 채운다

## Goals
- **Growth Targets:** _미정_
- **Content Goals:** 설교 한 편 → 쇼츠 3편. 렌더까지 자동, 업로드는 사람이 승인 후 수동.

## 이 채널의 제작 규칙

파이프라인: `scripts/weekly_run.sh` · 자세한 것은 `docs/session-handoff.md`.

- **업로드 자동화 없음.** `render`가 마지막 단계이고
  `office/production/<idea-id>/publish-package.md` 는 승인용 초안이다.
- **찬양 음원** — 예배 실황의 찬양 구간은 Content ID 위험이 있다. CCLI는 예배
  사용 범위이지 유튜브 배포 범위가 아니다. 설교 발췌를 우선하고, 찬양이 깔린
  구간은 `has_worship_music: true` 로 표시해 승인 패키지에 경고가 따라가게 한다.
- **회중석 초상권** — 성도 얼굴이 잡히면 `congregation_visible: true`.
  크롭(`crop: left|right`)으로 피하거나 그 구간을 버린다.
- **음성 합성 금지.** 목사님 음성을 클로닝하거나 안 하신 말씀을 만들지 않는다.
  실제 하신 말씀을 자르는 것만 한다.
- **구간 선별은 사람(또는 전사본을 읽은 Claude)이 한다.** 자동 휴리스틱을 쓰지
  않으며, `clips.json` 의 `reason` 이 비어 있거나 템플릿 문구 그대로면
  렌더가 거부된다.

## 채널 ID 얻는 법

egress 정책상 이 컨테이너에서 youtube.com에 접근할 수 없어 핸들로부터
자동 조회가 불가능하다. 셋 중 아무거나:

1. YouTube Studio → 설정 → 채널 → 고급 설정 → "채널 ID" 복사
2. <https://www.youtube.com/@yeshim1126> 접속 → 페이지 소스에서
   `"channelId":"UC...` 검색
3. 브라우저 콘솔: `ytInitialData.metadata.channelMetadataRenderer.externalId`

채널 ID는 Tier 2~3 리서치 스킬에서만 쓰인다. **Tier 0 파이프라인은 설교 영상
URL만 있으면 채널 ID 없이 그대로 돈다.**

## 벤치마킹 대상

아직 없음. `.claude/context/instagram-accounts.md` 와 함께 채운다.
단, ScrapeCreators / Apify 호스트도 현재 egress에서 막혀 있어 리서치 스킬은
허용목록 확장 전까지 실행 불가다 — 키가 아니라 네트워크 문제다.
