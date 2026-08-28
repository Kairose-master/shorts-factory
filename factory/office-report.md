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
