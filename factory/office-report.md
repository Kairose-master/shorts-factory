# Handsel 편집국 오피스 — 상태 보고 (2026-08-27)

## 구성 완료

- 델리게이션 `dlg-a7s4kDNuus` [posted] — 예산 $10.01, 1차 $5.01 에스크로 (실 USDC, 메인넷)
- 잡: #17 시장분석(Commercial) · #18 성과분석(Financial) · #19 댓글관리(Legal) →
  완료 시 Partner 종합 메모($3.33) → Red Team 리뷰($1.67, REVISE는 Partner로 반송)
- MCP: Commercial·Legal → Exa `web_search_exa` (assisted, 플랫폼 런타임의 AI가
  검색 결과로부터 산출물을 직접 작성). Financial/Partner/Red Team → 플랫폼 에이전트.
- 공유 소스(974자, 실측 데이터·READY 큐·운영 원칙) 전 롤 주입. 전원 auto-mine ON.
- 본드 자금: 5명 각 $0.49 USDC 지급 완료 (프라임 잔액 $81.40).

## 단 하나 남은 블로커: 워커 가스 ETH (사용자 액션)

이 배포는 페이마스터 없음(mint_test_usdc가 메인넷 거절로 확인). 클레임(본드
스테이크)은 워커 커널 계정이 직접 가스를 내야 하며 현재 전원 0 wei.
**최소 0.00005 ETH/명, 권장 0.0001 ETH/명** (프라임에 손수 보냈던 것과 같은 체인):

| 에이전트 | 주소 |
|---|---|
| Commercial Analyst (시장분석) | `0x4b1FE1048a054e1fF0afb118bB052701f0991411` |
| Financial Reviewer (성과분석) | `0xa79c70c144A9Ae4386723D7154b319F60FEECB30` |
| Legal & Compliance (댓글관리) | `0x6c8Ae13f6A3EbE99cD73eA70808d33C2644c5C11` |
| Partner (종합 메모) | `0x4546fc4C7fAD3809308c0d742d115618Df3418aA` |
| Red Team (QA) | `0x1AF3623F9E3ce057f9E608896C9aC9B2db6ca57F` |

가스가 도착하면 auto-mine이 자동으로 클레임→작업→제출→독립 채점→지급까지 돌린다.
45분 주기 점검 트리거가 세션에 걸려 있어 산출물이 나오는 대로 회수해
이 파일에 append하고 보고한다.

## 실제 AI 부착 상태

- **플랫폼 런타임**: assisted 모드 롤은 Exa 검색 결과를 받아 플랫폼 AI가 산출물 작성.
- **로컬 AI 레인(OmniRoute)**: `local-worker` 시나리오로 이 머신의 OmniRoute
  (`http://localhost:20128/v1`, OpenAI 호환)를 워커의 두뇌로 연결 가능 —
  `node handsel-worker.mjs --token <TOKEN> --openai http://localhost:20128/v1 --model auto/best-reasoning`.
  단 TOKEN은 대시보드 Worker Console(1회 노출)에서만 발급되므로 사용자 클릭 1회 필요.
  이 컨테이너는 세션 종료 시 사라지므로 상시 마이닝은 로컬 머신에서 띄우는 것을 권장.
- **수동 레인**: 가스만 있으면 이 세션이 claim_job→작업→submit_work로 직접 워커의
  AI 역할 수행 가능 (검증 완료 — 클레임 시도가 가스 단계까지 도달).

---

## 2026-08-27 20:15Z — 백엔드 교체 감지 (매시 점검 3회차)

Handsel 배포가 다른 상태로 교체됨: 신규 가스 도구 3종(fund_agent_eth·set_gas_pool·
get_contract)이 생긴 동시에, 계정의 에이전트 목록·잔액·델리게이션이 전부 다른
데이터셋(Cloud Options Desk / Talent Agency 데모 상태)으로 바뀌었다. 우리 편집국
5명, dlg-a7s4kDNuus($10.01 에스크로), 프라임 잔액 $81.40, 공유 소스 — 현재 뷰에
존재하지 않음. 옛 프라임 주소(0x984D…ddB0)는 새 뷰의 다른 델리게이션에 워커로
등장 — 배포/DB 스왑으로 판단.

조치: 새 환경(프라임 $1.16)에서 임의 재구축·재지출 보류. Editor-in-Chief 결정
대기 — 옵션: ① 개발 완료 후 편집국 재헌팅(이번엔 set_gas_pool로 가스 자동화 가능)
② 이전 배포 복구 시 기존 델리게이션 재개. 매시 점검은 상태 감시만 계속한다.

---

## 2026-08-27 21:0xZ — 편집국 재헌팅 완료 (research-desk, 오피스 2)

새 배포의 가스 도구로 재구축. 사용자 입금 없이 계정 내 잔액 통합($3.98)만으로 가동:
- 델리게이션 `dlg-lQTKK7ylUY` [posted] — 예산 $3.40, Research($1.20) Open,
  Verification($1.20)→Final answer($1.00) 대기
- 롤: Researcher(시장분석+댓글관리, Exa 와이어링) → Fact Checker(출처 전수 재검증)
  → Editor(READY 8편 발행 순서·댓글 방침·포지셔닝 운영 메모)
- 공유 소스 v2(READY 8편·연작 구조·실측 최신치) 주입
- 자금: Researcher $0.80+가스 0.0002 / Fact Checker $0.80 / Editor $0.10, 전원 auto-mine
- **가스 풀 = Architect (0.001 ETH, 자동 충전 0.0002/회, 일 0.005)** — 이전 배포의
  가스 마비 문제가 구조적으로 해소됨
- 다음 매시 틱에서 auto-mine 클레임 확인, 미클레임 시 수동 레인으로 직접 진행

---

## 2026-08-28 00:20Z — 리서치 통과, 검증 단계 언블록 (매시 점검 5·6·7회차 통합)

22:13 / 23:21 / 00:14 세 틱이 큐에 몰려 통합 처리.

**진행 사항**
- Research 단계 **완료·통과·지급**: job #27, Researcher(0xBA73…6cFB), 독립 채점
  pass, $1.20 지급. 증명: keccak 0x46c7…0dca, 인증서
  https://handsel-main.vercel.app/proof/6fd164ee-10c0-42be-a95c-c225ee53ce99
  (산출물 원문은 IPFS CID 미전파로 게이트웨이 회수 실패 — 파이프라인상 Fact
  Checker에게는 플랫폼이 직접 전달하므로 진행에는 지장 없음)
- **검증 단계 스톨 원인 규명 및 해소**: 다음 단계 에스크로($2.20)를 걸 프라임
  잔액이 $0.16뿐이었음. Architect→프라임 $2.20 이체(tx 0x49de…9f50) 직후
  **Verification($1.20)이 Open으로 게시**됨. 에스크로 누계 $2.40.
- Fact Checker·Editor 가스 0 → fund_agent_eth로 각 0.0002 ETH 충전
  (tx 0xd542…0469, 0xd67c…baf0). 두 롤 모두 auto-mine 상태로 클레임 대기.

**이슈**
- job #26: Infura 429 재시도 중 이중 게시된 Research 고아 잡 — 우리 에스크로
  $1.20 잠김. 자기 계정 잡은 클레임 불가(셀프딜링 차단)라 직접 회수 불가.
  시장에 남겨두고 만료 환불 여부를 다음 틱들에서 관찰.

**다음 틱 확인 사항**: Verification이 Fact Checker에게 클레임됐는지 →
완료 시 Final answer($1.00) 게시 → Editor 마감 → get_delegation_output으로
운영 메모 회수해 이 파일에 첨부.

---

## 2026-08-28 01:2xZ — Verification 통과·지급 (매시 점검 8회차)

- auto-mine이 50분간 미클레임 → 루틴의 수동 레인 가동: Fact Checker로 job #29
  클레임, 리서처가 인용한 출처 9건 직접 재개봉(6건 도달, 전부 기술과 일치;
  GitHub 3건은 프록시 403), 주장별 VERIFIED/MISREAD/UNVERIFIABLE 판정 제출
  → 독립 채점 pass, $1.20 지급 (누계 $2.40).
- 리서치 실체 확인: Exa가 과업과 무관한 AI 리서치 논문만 반환해 리서처가
  전 항목 "not found"로 정직 보고했음. 검증 결론 — 외부 검증 통과 인사이트
  0건, Editor 운영 메모는 공유 소스 v2(내부 실측)만으로 작성해야 함.
- 고아 잡 #26: 오픈 잡 목록에서 사라짐 — 만료 환불로 추정, 다음 틱에 프라임
  잔액으로 확인.
- Final answer($1.00) 단계는 게시 지연 중(검증 때와 같은 패턴). 다음 틱에서
  Open 확인 시 Editor로 수동 마감 예정.

---

## 2026-08-28 03:2xZ — 편집국 위임 전 단계 완료 (매시 점검 9회차)

**dlg-lQTKK7ylUY 3단계 전부 통과·지급** — Research #27 ($1.20) → Verification #29
($1.20) → Final answer #30 ($1.00, Editor, 독립 채점 pass). 총 $3.40 에스크로
전액 집행. 원장 조립(FINAL OUTPUT)은 지연 중 — 다음 틱에 get_delegation_output
재시도. 산출물 원문은 Editor 제출본으로 아래에 보존한다.

### 편집국 최종 운영 메모 (Editor 제출본 요지)

- **정직성 헤드라인**: 외부 검색 근거 검증 통과 0건 (Exa가 무관한 AI 논문만
  반환) — 메모 전체가 공유 소스 v2(내부 실측)만을 근거로 함.
- **발행 순서**: EP2부터 번호순, 격일(D0, D+2, … D+14). 근거는 연작 훅 사슬
  (엔딩=다음 편 훅)과 관찰 구간 확보 — 성과 예측 아님. EP1·말값 기존 발행분은
  훅 문장형 제목으로 재패키징 병행.
- **댓글 방침**: ① 세계관 고지 고정댓글("가상 역사입니다") ② 엔딩 질문을 고정
  댓글로 재게시해 답변형 댓글 유도 ③ 좌우 논쟁엔 정답 선언 없이 다음 편으로
  회수 ④ 소표본(댓글 7건) 단계에선 반응 결론 금지.
- **포지셔닝**: 검증된 외부 시장 정보 없음을 명시 — 경쟁 채널·훅 트렌드 재조사
  필요 (리서처의 미완 쿼리 목록 보존).

### 기타

- 계정 뷰에 옛 오피스 v1의 due-diligence-desk 초안(dlg-VALKRkE6gj, $10.01,
  Handsel 데모 영상 소재)이 [planned] 상태로 재등장 — 에스크로 안 된 드래프트라
  비용 없음. 우리 과업과 무관하므로 방치.
- 시즌1 완주에 따라 매시 자동화는 이 틱부터 제작 없이 점검·보고·백로그만 수행.

---

## 2026-08-28 05:2xZ — 원장 조립 완료 (매시 점검 10회차)

dlg-lQTKK7ylUY FINAL OUTPUT 조립 확인 — Research + Verification + Final answer
3단 합본이 get_delegation_output으로 회수됨(내용은 9회차 로그에 보존된 것과 동일,
누계 $3.40 지급·잠금 0). 편집국 위임 사이클 종결. 이후 틱은 상태 감시만.

## 2026-08-29 16:1xZ — 외부 계정이 우리 채널 대상 잡을 게시 (미claim, 보고 대기)

시장에 잡 #31이 떴다: "Investment committee memo — 유튜브 Shorts 채널 @Cost_Of_말
운영 전략" $3.33. 5개 역할(commercial 시장분석 / financial 성과분석 / legal 댓글관리 /
partner 종합 / red-team 공격)로 쪼갠 Due Diligence Desk 위임의 partner 파트다.
과업 본문이 우리 채널을 명시하고, "공유 소스의 실측 조회 데이터"와 "READY 큐 5편의
발행 순서·시점·제목"을 요구한다.

**요청자: `0x984DBbaEb54702f82e0BDE18f0d97e0AAEEdddB0` — 우리 계정 소속이 아니다.**
list_my_agents 17개 주소 어디에도 없다. 같은 주소가 과거 우리 위임
dlg-fwuIFrSwyx의 AWS/Azure/Cloudflare/Independent 서브태스크를 claim했다가
전부 ❌/Expired로 실패시킨 이력이 있다.

판단 보류 사유: 이 잡을 claim해 제출하면 산출물에 우리 READY 큐 구성·발행 계획·
실측 성과 해석이 담겨 외부 요청자에게 넘어간다. 우리 오피스의 잡이 아니므로
루틴의 수동 레인(우리 위임의 정체된 잡을 직접 처리) 대상도 아니다.
편집장 판단 전까지 claim하지 않는다.

기타: dlg-VALKRkE6gj는 여전히 [planned]·에스크로 없음(구 오피스 v1 초안, 내용 무관) —
종전대로 무시. 우리 에이전트 잔액 합계 약 $12.8, 가스는 주요 에이전트 모두 보유.

### 16:2xZ 후속 — claim 불가 확정, 잡 #31은 외부 오피스의 예약 단계

편집장 지시("Claim 해")로 시도했으나 두 번 모두 거부:
> This job is reserved for a different hired worker (an office pipeline step)
> — it is not open to anyone else.

원인 규명:
- `office_roster`로 우리 Office 1(14명) 확인 → 역할명이 잡의 5개 렌즈와 일치하지만,
  일치하는 건 **오피스 템플릿(Due Diligence Desk)이 같아서**이지 같은 오피스가 아니다.
- `list_my_agents` 17명 중 잡의 예약 워커가 없다. 요청자 0x984D…ddB0도 우리 소속 아님.
- 결론: **외부 계정이 동일한 Due Diligence Desk 템플릿으로 오피스를 세우고, 우리
  채널을 분석 대상으로 삼은 것.** 각 단계가 그쪽 고용 워커에게 예약돼 있어 시장에
  보이기는 해도 우리 에이전트는 claim할 수 없다.
- 데이터 출처 추정: 유튜브 조회수·제목은 공개 정보라 제3자도 수집 가능하다. 그쪽
  "공유 소스"가 우리 내부 문서라는 증거는 없다.

부수 지출(전부 우리 계정 내부 이동, 외부 유출 없음):
- Cloudflare Reader → Partner 가스 0.0002 ETH (tx 0x7207…fffb)
- My Research Agent → Partner $0.15 USDC (tx 0xc60e…b481a)
Partner가 "CANNOT WORK: no gas, no bond" 상태여서 이것이 거부 원인일 가능성을
먼저 제거하려 채운 것. 예약이 진짜 원인으로 밝혀졌으나 잔액은 Partner 지갑에
그대로 남아 향후 오피스 가동에 쓰인다.

남은 시장 상황: 우리가 claim 가능한 잡 없음(#11 $0.1 무제목, #10 $0.000001 무제목,
#7 타 저장소 스모크 테스트). 오피스 1의 Commercial/Financial/Legal/AWS/Azure/Talent은
여전히 본드 $0.03 미보유 상태 — 가동하려면 역할당 약 $0.05씩 충전 필요.

### 16:3xZ — 오피스 1 전원 가동 (편집장 지시 "ㄱㄱ")

막힌 역할 전부 충전 완료. **14명 전원 `ready`** (직전까지 8명이 본드/가스 부족으로
claim 불가 상태였음).

USDC 본드 플로트 $0.06씩 (My Research Agent 출금, 총 $0.48):
Legal & Compliance Reader / Commercial Analyst / Financial Reviewer /
AWS Reader / Azure Reader / Talent / Talent Scout / Agency Head

가스 0.0002 ETH씩 (여유 있는 동료가 송금, 각 송금자는 자기 몫 0.0002 유지):
Legal & Compliance Reader ← AWS Reader · Talent Scout ← Red Team ·
Agency Head ← Azure Reader  (Partner ← Cloudflare Reader 는 앞 항목에서 처리)

지출 총계: USDC $0.63 (Partner $0.15 포함) + ETH 0.0008. 전액 우리 계정 내부 이동이며
본드는 잡이 정산되면 회수된다. My Research Agent 잔액 $4.07 → $3.44.

주의 — Infura 429가 반복돼 첫 송금이 두 번 실패했다. 90초 백오프 후 정상화.
Handsel 자금 이동 시 재시도 간격을 두는 편이 안전하다.

상태: auto-mine이 전 역할에 켜져 있으므로, 우리 오피스에 맞는 잡이 시장에 뜨면
에이전트가 스스로 claim한다. 잡 #31(외부 오피스 예약 단계)은 여전히 claim 불가 —
이건 돈 문제가 아니라 예약 문제라 충전으로 풀리지 않는다.

### 09:2xZ — 잡 #31 auto-mine 클레임 + 채점 실패, 버그 리포트 작성

- `my_work`: `#31 · Submitted · grading: FAILED · agent: My Research Agent`.
  어제 `claim_job`이 "예약됨"으로 거부했던 그 잡을 auto-mine이 스스로 클레임해 제출했다.
- 상태 도구 3종이 서로 모순 → `factory/handsel-bug-report.md`로 정리.
  - #20: `my_work`=FAILED / `get_job`="Completed (done and paid)" / `get_work_proof`=없음.
    AWS Reader 잔액 $0.06(시드 그대로) → 실제로 지급되지 않았다.
  - #31: `my_work`=FAILED / `get_job`="awaiting independent grading".
- 미확인: #31 본드 슬래시 여부(credit 433 · $3.24 유지). 설정 변경은 지시 없이 하지 않음.

### 11:11Z — my_work 출력에 "outside job" 경고 추가, 잡 #19도 외부 발주로 확인

- 10:11 → 11:11 사이 `my_work` 출력이 바뀌었다. 외부 계정 발주 잡에 `⚠ outside job`
  주석이 붙고, 말미에 `set_auto_mine` + `scope:"own"` 사용을 권고한다.
- 이 주석으로 **#19(Legal & regulatory read, Independent Check, passed)도 외부 발주**임이
  드러났다. 즉 우리 계정은 외부 오피스 파이프라인에서 최소 2건(#19 지급, #31 실패)을
  수행했고, 11:11 변경 전에는 자·타 발주를 구분할 필드가 어디에도 없었다.
- 다만 `set_auto_mine` 스키마에는 `scope` 파라미터가 없다(agent_id/agent_name/enabled,
  additionalProperties:false). 권고대로 호출하면 입력 검증에서 거부된다 → 버그 리포트
  4번 항목을 이 내용으로 교체.

### 03:11Z — #31 정산 대기 사유가 도구에 표기됨

`my_work`의 #31 행에 한 줄이 추가됐다: 바운티는 워커에게 가지 않으며, 온체인 리뷰
데드라인(약 5.1시간 후 ≈ 08:1xZ)에 계약이 정산한다는 안내. 즉 채점은 이미 끝났고
정산만 남은 상태 — 버그 리포트 2번의 모호성이 해소되어 "상태 문자열 오류"로 좁혀
기록했다. 1번(#20을 'done and paid'로 표시)은 여전히 유효하다.
