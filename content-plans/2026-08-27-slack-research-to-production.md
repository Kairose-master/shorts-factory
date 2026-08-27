# 슬랙 리서치 → 제작 브리프 (2026-08-27)

Slack `#유튜브-리서치`에 올라온 리서치 2건을 읽고, 실제로 만들 수 있는 아이디어
슬레이트를 짠 뒤, 1번을 영상 파일까지 제작한 기록.

## 읽은 것

| 리서치 | 캔버스 | 리포지토리 | 상태 |
|---|---|---|---|
| **AI 도구·자동화 니치 — 숏폼 리서치 (API mode)** | `F0BT4SCQN81` | `research/ai-tools-automation-2026-08-27-api/report.md` (브랜치 `claude/ai-tools-automation-api-research-bu4qxv`) | 이 브리프의 근거 |
| **9개 채널 심층 리서치 — 채널별 포맷 분해** | `F0BTXT1V1RN` | `research/kr-9channels-deep-2026-08-27/report.md` (같은 브랜치) | 「말값」 연작이 이미 소화 중 |

**이 브리프가 AI 도구 리서치를 고른 이유.** 한국 9채널 리서치는 이미
「말값」 No.1~No.2로 제작이 진행 중이라 슬레이트가 비어 있지 않다. 반면 AI
도구 리서치의 §7 아이디어 10개는 전부 미착수였고, 그중 1번은 리포트 본인이
*"이 데이터셋에서 가장 강한 기회"*라고 못박은 항목이다. 겹치지 않는 쪽을 골랐다.

---

## 슬레이트 — 근거가 있는 것만

각 항목의 "근거"는 API mode 리포트의 절 번호다. **측정된 갭이 없는 아이디어는
넣지 않았다.**

### ① The Bill — "이 영상은 얼마 들었나" ✅ **제작 완료**

- **훅**: *"Python and ffmpeg drew every frame of this video. Zero credits.
  That number is the part nobody shows you."*
- **근거**: §4b — 두 플랫폼 5개 영상에서 **비용 불만 9건**. §3 — 상위 훅 **16개 중
  0개**가 가격을 언급. 니치에서 가장 큰 수요·공급 격차.
- **형식**: 코드로 그린 모션그래픽 44.6초. 자기 자신의 청구서를 결제 카드처럼 띄운다.
- **왜 이게 되나**: 리포트의 Script A는 비용을 `$[YOUR NUMBER]`로 비워뒀다 —
  숫자를 지어내면 §4c가 고발한 그 부정직을 반복하니까. 이 영상은 남의 청구서를
  추정하지 않고 **자기 청구서를 공개한다.** 파이프라인이 이 저장소에 있으니 검증 가능하다.
- **산출물**: `projects/the-bill/the-bill.mp4` · 기록 `projects/the-bill/storyboard.md`
- **비용**: $0.00, 렌더 ~35초

### ② 6,251뷰가 그달 4위였다 — baseline의 반란

- **훅**: *"This is the fourth best video of the month. Six thousand views."*
- **근거**: §1 — Quinn Nolan의 Short는 표에서 **조회수 최하위(6,251)**인데 자기 채널
  평균 대비 **9.78×, z=7.58**. 반대로 Eric Tech의 **116만 뷰는 12.14×에 그친다.**
- **형식**: 데이터 시각화 네이티브. 조회수 막대그래프 → 정렬 뒤집기 → baseline 배수
  막대그래프. `motion-graphics`가 정확히 이걸 위해 있는 도구다.
- **왜 미착수인가**: 니치 전체가 조회수로 말한다. 이 반전을 가진 사람은 데이터를
  뽑아본 사람뿐이고, 우리는 뽑았다.
- **주의**: TikTok 4건은 *plays ÷ followers* 프록시라 §1과 같은 축에 놓으면 안 된다(§2).
  YouTube 12건만 쓰거나, 축을 분리해서 그릴 것.

### ③ "AI agent"를 검색하면 만화가 나온다

- **훅**: *"I searched 'AI agent' on Shorts. Eighteen of the first thirty-three
  results were cartoons."*
- **근거**: §1 discovery-surface — 반환된 33편 중 **온-니치는 15편뿐**. 나머지 18편은
  AI로 *만든* 엔터테인먼트(애니메이션 `#animation` **43.65×**, 자동차 편집 23.96×).
  툴 교육 콘텐츠는 자기 키워드에서 소수파다.
- **형식**: 33칸 그리드 → 15/18 분할. 정지 카드 시퀀스로 충분.
- **가치**: 우리 자체 수집 데이터. 어디에도 없다.

### ④ 풀타임 코드 리뷰어 — 아무도 팔지 않는 피로

- **훅**: *"It's like being a full-time code reviewer and a full-time product
  owner, and never doing actual development anymore."* (댓글 원문)
- **근거**: §4g — Matt Pocock "AI Coding is exhausting"(3.63×)이 표본 전체에서 가장
  인용 가치 높은 댓글을 생산. *"Exhausted, exhilarated, and overwhelmed"*,
  *"almost certainly will hate the next one when I'm a barista"*, 그리고 1983년
  논문 **"Ironies of Automation"** — 시청자가 물어다 준 권위 소재.
- **형식**: 인용 벽(quote wall). 내레이션 없이 댓글만 순차 노출해도 성립.
- **주의**: 배수 자체는 낮은 레인(3.63×, 2.99×). 도달보다 **댓글 품질**을 사는 선택.

### ⑤ 같은 사무라이 클립이 10개 영상에 있다

- **훅**: *"You are the 10th person to make the same exact video, same exact
  graphics, same exact samurai."* (댓글 원문)
- **근거**: §4c — 20.59× **1위 영상**의 댓글에서 나온 말. 과성과와 시청자 불신이 같은
  댓글창에 공존한다. *"This is the 5th creator I've seen pushing Higgsfield."*
- **형식**: 화면 분할 반복 몽타주. 실제 영상 클립이 필요하므로 **인용 범위 판단 필요** —
  이 슬레이트에서 유일하게 무료로 못 만드는 항목.

### ⑥ 아무도 안 찍는 80%

- **훅**: *"It's not that easy, bro. You still gotta build 80 to 90 percent of
  the automation."* (댓글 원문)
- **근거**: §4e — *"How many hours of refactoring did you go through that you
  didn't mention?"*
- **형식**: 화면 녹화가 필요. 무료 파이프라인 밖.

### ⑦ 판단이 있는 랭킹은 댓글을 스스로 농사짓는다

- **근거**: §4f — 티어리스트가 **2위(13.05×)**, 댓글이 전부 누락 항의
  (*"No OpenCode and Hermes Agent being here is diabolical"*). §6.2 정정: 리스트가
  죽은 게 아니라 **반박 가능한 의견의 부재**가 문제였다.
- **형식**: 티어 보드 애니메이션. `motion-graphics`로 즉시 제작 가능.
- **조건**: 누락을 **의도적으로** 방어 가능하게 남길 것. 빈틈 없는 랭킹은 댓글이 없다.

### ⑧ 당신 고객은 아직 아웃룩을 못 찾는다

- **근거**: §4g — 표본 전체 실질 댓글 중 최다 공감(**816 likes**)
  *"Upper managment still doesnt know how to find outllook on their computer."*
- **상태**: 리포트 §8에 Script B로 **이미 완성된 대본**이 있고, Kokoro 내레이션으로
  씬별 실측까지 끝나 있다(훅 5.17초, 슬롯 4.0초 초과). `video-assembly`로 그대로
  제작 가능 — **다음 제작 1순위.**

---

## 이 브리프가 바꾼 것 — 파이프라인이 파일까지 간다

리서치 파이프라인은 9단계(대본)에서 끝났다. 이번에 **10단계(제작)**를 붙였다.

| 스킬 | 소유 범위 |
|---|---|
| `motion-graphics` | 코드로 그리는 프레임. easing·키네틱 타이포·카운터·안전영역·인코딩. `pip install pillow numpy imageio-ffmpeg` 외 의존성 없음 |
| `video-assembly` | 내레이션 → **실측 타이밍** → 렌더 → 믹스 → QC 게이트. 키 없음, 에디터 없음 |

**핵심 규칙 하나**: 내레이션을 먼저 합성해서 **재본 길이를 재고**, 그 측정값이 씬
길이가 된다. 리포트 §8이 이미 이 교훈을 기록해뒀다 — Script B의 훅이 스토리보드
4.0초 슬롯에서 실제 5.17초(29% 초과)로 나왔고, 맞추려고 자르면 필터링을 하는 바로
그 문장이 잘린다. 이제 스크립트가 그 순서를 강제한다.

부수 효과: TTS **단어 경계**를 받아 `plan.json`에 실어두므로, 자막·리빌이 해당
단어에 정확히 떨어진다. ①의 "ZERO CREDITS"는 "Zero"가 발음되는 4.13초에 뜬다.

## 다음

1. ⑧ "Your buyer can't find Outlook" — 대본 완성본이 있으니 제작만 하면 된다
2. ② 6,251뷰 — 데이터 시각화, `motion-graphics`가 가장 잘하는 종류
3. ③ 33편 중 18편 — 우리 자체 데이터, 경쟁자 없음

⑤⑥은 화면 녹화·클립 인용이 필요해 무료 경로 밖이다. 하려면 어디까지 인용할지
먼저 정해야 한다.
