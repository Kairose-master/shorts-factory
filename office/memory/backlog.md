# Content Backlog — v2, rebuilt on the Lawbook generator

**Rebuilt 2026-08-27** after the HS-006 correction. v1 generated ideas from the
product; this one generates them from **incidents**, per lesson L-07.

## How an entry gets made

```
REAL INCIDENT  →  which Lawbook axis/code it lands on  →  one short
```

One incident, one code, one video. The generator is the incident ledger below,
not a brainstorm. When the ledger grows, the backlog grows — that is the whole
point of the structure (`../research/verification-lawbook.md`).

## Posture — the field that keeps this honest

The 16 Lawbook codes are a **design proposal, not shipped product** — the source
document says so about itself twice. So every entry declares what it is allowed
to show:

| Posture | Meaning | What the video may put on a Handsel screen |
|---|---|---|
| **SHIPPED** | Handsel actually does this. Traceable to `../research/handsel-model.md`. | Real UI, real data |
| **CONCEPT** | The Lawbook proposes it; the product does not emit it. | Only with `CONCEPT` visible on screen, never as product UI |
| **GAP** | Handsel does **not** do this yet, and the incident proves it. | A build-in-public video about the gap. Never dressed as a feature. |

**A CONCEPT entry that ships without its label is a fabricated feature** — Charter
rule 1, and indefensible for a project selling verifiability.

## Scoring

`Priority = Hook×3 + Visual×2 + Relevance×2 + Novelty + Understandability − Difficulty×2`
0–10 each; **Difficulty is cost-to-make, so higher is worse.** Generated and
arithmetic-checked by script — do not hand-edit a `Pri` cell.

---

## The incident ledger

Every incident is a real, checkable event. Source in the last column.

| ID | Incident | Source |
|---|---|---|
| **I-01** | Job #20: three surfaces disagree about one job. `my_work` → `FAILED`; `get_job` → `Completed (done and paid)`; `get_work_proof` → `No proof recorded`. | live queries, 2026-08-27 |
| **I-02** | **$100 of real USDC sat in mainnet escrow for 30 days as an open "extract this without earning it" challenge. Job #2 came back `Refunded` — nobody took it.** Job #3 is a second run, currently `Accepted`. | `get_job 2`, `get_job 3` |
| **I-03** | Job #8: Handsel paid $5 to an outside agent to check whether its **own** mainnet/testnet labels were consistent — after admitting in the task text that they were genuinely wrong until 2026-08-04, and that a bot receipt once let a sandbox response be recorded as a mainnet success (§23, `failure-modes.md`). | `get_job 8` |
| **I-04** | `plan_delegation` split a $5 budget and spent $1 of it on a second agent to review the first one's work, unprompted. | `dlg-S711y4gs3O` |
| **I-05** | Nine agents on one account: 670, 367, 362, 361, 361 — and **five sitting at exactly 0.00**, never having earned. | `list_my_agents` |
| **I-06** | Market price for text work: median **$1.00**, range $0.10–$8.00, across **10 trades**. | `market_price` |
| **I-07** | An open job on the board with a bounty of **$0.000001**. | `browse_open_jobs` #10 |
| **I-08** | A real GitHub repo job on `Kairose-master/handsel`, mainnet App, escrowed from a label. | `browse_open_jobs` #7 |
| **I-09** | r/AI_Agents, 2026-08-22: *"My autonomous AI agent has earned $0 in 48 days and still owes me $155."* 79 upvotes, **62 comments**. | `../research/audience-signal-2026-08-27.md` |
| **I-10** | **The Office published a video claiming an agent "FAILED" and could not support it.** Caught by an external document, not by our own QC. | `../production/HS-006/qc-correction-2026-08-27.md` |

**I-02, I-03 and I-10 are the three strongest assets here and all three are about
being wrong or being tested.** That is not a coincidence — it is the positioning.

---

## The backlog

| ID | Title | Pillar | Incident | Lawbook code | Posture | H | V | N | U | R | D | **Pri** | Cost | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HS-024 | $100 on the internet. Try to take it. | C | I-02 | `SECURITY_BLOCKED` | SHIPPED | 10 | 8 | 9 | 9 | 9 | 3 | **76** | free | idea |
| HS-006b | Three came back with a proof. One did not. | C | I-01 | `VERIFICATION_INCONCLUSIVE` | GAP | 9 | 8 | 9 | 8 | 10 | 4 | **72** | free | **MADE — awaiting approval** |
| HS-001 | I gave an AI $5 and told it to hire someone | A | I-04 | `—` | SHIPPED | 9 | 7 | 8 | 8 | 10 | 3 | **71** | free | **MADE — awaiting approval** |
| HS-021 | My AI agent earned $0 in 48 days and owes me $155 | C | I-09 | `—` | SHIPPED | 10 | 7 | 8 | 9 | 9 | 4 | **71** | free | idea |
| HS-004 | A GitHub label that pays for its own fix | D | I-08 | `—` | SHIPPED | 9 | 9 | 9 | 8 | 10 | 6 | **70** | low | idea |
| HS-011 | An AI grading its own homework is not a reputation | E | — | `—` | SHIPPED | 9 | 6 | 7 | 9 | 10 | 3 | **69** | free | **MADE — awaiting approval** |
| HS-017 | The market, as a game floor | G | — | `—` | SHIPPED | 8 | 10 | 7 | 7 | 8 | 3 | **68** | free | idea |
| HS-025 | I paid someone $5 to check if I was lying | B | I-03 | `EVIDENCE_INVALID` | SHIPPED | 9 | 7 | 9 | 8 | 9 | 4 | **68** | free | idea |
| HS-027 | Five of my agents have never earned anything | F | I-05 | `—` | SHIPPED | 8 | 8 | 7 | 9 | 9 | 3 | **68** | free | idea |
| HS-009 | One click, and it starts working without me | D | — | `—` | SHIPPED | 8 | 8 | 7 | 8 | 9 | 3 | **67** | free | idea |
| HS-018 | Watch one dollar move between two robots | G | — | `—` | SHIPPED | 8 | 9 | 6 | 9 | 9 | 4 | **67** | free | idea |
| HS-029 | CAN'T VERIFY is not WORK FAILED | E | I-01 | `EVIDENCE_INACCESSIBLE` | CONCEPT | 9 | 7 | 8 | 8 | 8 | 3 | **67** | free | idea |
| HS-030 | Don't trust the score. Inspect the proof. | E | I-03 | `—` | SHIPPED | 8 | 8 | 7 | 8 | 9 | 3 | **67** | free | idea |
| HS-005 | Five AI agents. Ten dollars. No instructions. | C | — | `—` | SHIPPED | 10 | 8 | 9 | 9 | 7 | 6 | **66** | med | idea |
| HS-022 | 402 Payment Required | E | I-09 | `—` | SHIPPED | 8 | 8 | 7 | 7 | 9 | 3 | **66** | free | idea |
| HS-026 | We published a claim we could not back | B | I-10 | `ADJUDICATION_REVERSED` | GAP | 9 | 6 | 10 | 7 | 7 | 2 | **66** | free | idea |
| HS-019 | "Trust me bro" vs. a signed proof | H | I-03 | `—` | SHIPPED | 9 | 6 | 6 | 8 | 8 | 2 | **65** | free | idea |
| HS-015 | I built a dashboard designed to make me look bad | F | — | `—` | SHIPPED | 9 | 6 | 8 | 7 | 7 | 2 | **64** | free | idea |
| HS-014 | Robots have credit scores now. 300 to 990. | E | I-05 | `—` | SHIPPED | 7 | 7 | 6 | 8 | 9 | 3 | **61** | free | idea |
| HS-028 | The going rate is one dollar. Across ten trades. | E | I-06 | `—` | SHIPPED | 7 | 7 | 8 | 8 | 7 | 2 | **61** | free | idea |
| HS-020 | 한국 개발자가 만든 AI 노동시장 (KO cut) | D | — | `—` | SHIPPED | 7 | 7 | 7 | 8 | 8 | 3 | **60** | free | idea |
| HS-007 | The cheapest job on the board costs $0.000001 | C | I-07 | `—` | SHIPPED | 8 | 6 | 8 | 9 | 6 | 3 | **59** | free | idea |
| HS-012 | PASS does not mean PASS | E | — | `VERIFIER_DISAGREEMENT` | CONCEPT | 8 | 6 | 10 | 5 | 9 | 5 | **59** | free | idea |
| HS-023 | "Price becomes the advertisement" | E | I-09 | `—` | SHIPPED | 7 | 6 | 8 | 6 | 7 | 3 | **55** | free | idea |
| HS-003 | Every bug that cost me real money | B | I-03 | `—` | SHIPPED | 8 | 4 | 8 | 6 | 7 | 3 | **54** | free | idea |

<!-- 25 entries, priority verified -->

---

## Entries — the ones that changed

Only entries whose reasoning moved in the rebuild are written out. The rest keep
the notes they had in v1 (see git history for `backlog.md` before 2026-08-27).

### HS-024 — $100 on the internet. Try to take it. · **Pri 76, new top of backlog**

**Incident I-02. Posture: SHIPPED.** The strongest asset in the ledger and the
Office had missed it entirely.

$100 of **real USDC** was placed in `LaborMarketV2` escrow on Base mainnet as an
open challenge: *"extract this without grader-passed work entitling you to it.
Take it and it is yours — no claim form, no adjudication. The chain is the only
judge."* Job #2 ran its 30 days and settled `Refunded`. Job #3 is a second run,
live now.

- **Hook direction:** *"There's a hundred dollars sitting on the internet right
  now. The rules say: steal it and it's yours."*
- **Why it may work (Hook 10):** it is a bounty story, which is a proven
  short-form genre, and the stake is real money on a public chain — checkable by
  the viewer, which almost nothing in AI marketing is.
- **The turn:** the money came back. Not because anyone was stopped — because
  nobody managed it.
- **What it may NOT claim:** that the contracts are secure, or audited. They are
  **not audited** (DO NOT CLAIM ledger). One challenge surviving 30 days is one
  challenge surviving 30 days. The video must say that itself — which is
  stronger, not weaker: *"this isn't proof it's safe. It's just the only kind of
  evidence we can actually give you yet."*
- **Check before scripting:** #3's current state. It is live and could change.

### HS-025 — I paid someone $5 to check if I was lying · **Pri 68**

**Incident I-03. Posture: SHIPPED.**

Job #8's own task text admits Handsel's mainnet/testnet labels were genuinely
inconsistent until 2026-08-04, that README "try it free" links pointed at a v1
archive on a different contract, and that a bot receipt once let a sandbox
response be recorded as a mainnet success. Then it pays an outside agent $5 to
verify the corrections actually landed — with acceptance criteria demanding every
surface be named and every finding quote exact text.

- **Hook:** *"I wrote down every place my own product had lied. Then I paid a
  stranger to check I'd fixed them."*
- **Why it may work:** self-audit-as-product is rare and it is the exact behaviour
  the product sells. The company used its own labor market on itself.
- **Novelty 9** — nobody else is publishing this.

### HS-026 — We published a claim we could not back · **Pri 66**

**Incident I-10. Posture: GAP.** The Office's own failure, as content.

We made a video about independent verification that put the word `FAILED` on
screen as a work-quality verdict, passed our own QC at 42/45, and could not
support it once two more surfaces were checked.

- **Hook:** *"We made a video about verifying AI work. The video made a claim we
  hadn't verified."*
- **Why it may work (Novelty 10):** the correction *is* the demonstration. It
  shows the failure mode the product exists to prevent, using the people selling
  the product as the example.
- **Risk, and it is real:** this can read as either unusual integrity or as
  incompetence. Gate 8 (cringe) applies hard. It works only if the tone is flat
  and specific — the three surfaces, the exact word, the exact fix — and never
  self-congratulatory. **Do not make this until HS-006b has shipped**; a
  correction video before the corrected video is incoherent.

### HS-027 — Five of my agents have never earned anything · **Pri 68**

**Incident I-05. Posture: SHIPPED.** Nine agents: 670, 367, 362, 361, 361 —
and five at exactly `0.00`.

- **Hook:** *"Nine AI agents. Four have a credit score. Five have never earned a
  cent."*
- **Why it may work:** it is the cold start, on screen, undisguised — and the
  DO NOT CLAIM ledger says the cold start is the honest state. This turns the
  Office's biggest messaging constraint into the video.
- Pairs with HS-014 (what the 300–990 score means) and HS-021 (the audience's own
  version of the same pain).

### HS-029 — CAN'T VERIFY is not WORK FAILED · **Pri 67 · Posture: CONCEPT**

The Lawbook thesis as an explainer, built from incident I-01. **`EVIDENCE_INACCESSIBLE`
must appear labelled `CONCEPT` on screen** — Handsel does not emit it today.
Written as *"here is the distinction that matters, and here is a real job where
nobody could tell which side it fell on"*, not as a feature tour.

### HS-030 — Don't trust the score. Inspect the proof. · **Pri 67**

**Posture: SHIPPED.** The strongest line in the Lawbook document, and it maps to
something that genuinely exists: EIP-712-signed proofs at `/proof/<id>`, and the
fact that job #20 has **no** proof recorded is itself the demonstration — a
missing proof is information.

### HS-007 — The cheapest job on the board costs $0.000001 · **Pri 59, re-grounded**

Was a speculative "what's the cheapest job an AI will accept?" It is now anchored
to **incident I-07**: a real open posting at one millionth of a dollar. No longer
needs a paid experiment to make — the artefact already exists on the board.

---

## Retired in the rebuild

Not deleted — retired, with the reason, per the Charter. A retired idea can come
back when an incident grounds it.

| ID | Title | Why retired |
|---|---|---|
| HS-002 | Two AIs haggling over a price | Feature tour with no incident behind it. The negotiation channel exists, but nothing in the ledger shows it being used, so any video would be staged. **Revisit if** a real negotiation appears in the data. |
| HS-008 | No login. No wallet. Thirty seconds. | A product tour, not an incident. Novelty was already the lowest in v1 (4). Its job is better done as an end card on any other video. |
| HS-010 | Paste one URL and your agent has a job | Same problem: describes a capability rather than showing an event. **Revisit if** an external MCP worker actually claims and passes a job on this account. |
| HS-013 | Escrow, explained with two robots and a jar | Generic category education with no Handsel specificity — it would work identically for any escrow product, which is Gate 6's definition of failure. HS-018 covers the same ground with real money moving. |
| HS-016 | I wrote a prediction to be falsifiable, then falsified it | Could not verify the underlying story from any source I have. Unverifiable premise, so it cannot pass Gate 5. **Revisit if** the document is produced. |

## Rejected

Still none. `rejected.md` records rejections at QC or later; the five above are
**retired at idea stage**, which is a different thing and deliberately reversible.

## What changed, and what it cost

- **v1 had 24 entries; v2 has 25**, but 10 are now anchored to a checkable
  incident where v1 had 3.
- **The new #1 (HS-024, Pri 76) beats everything in v1.** It was sitting in the
  account's own job history the entire time. v1 never looked.
- Five entries retired for having no incident behind them.
- **Three of the four highest-value assets are about being wrong, being tested,
  or being unable to tell** — I-02, I-03, I-10. The Office's instinct in v1 was
  to sell capability. The evidence says the credible story is the opposite.
