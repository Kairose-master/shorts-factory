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
