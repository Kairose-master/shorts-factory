# Content Backlog

Every idea the Office has had. Nothing is ever deleted — `rejected` and
`retired` are statuses, because an idea deleted today is regenerated in six
weeks by an Office with no memory of it.

**Priority** = `Hook×3 + Visual×2 + Relevance×2 + Novelty + Understandability − Difficulty×2`
(range −20…90). Hook is weighted hardest: a 9/10 script behind a 3/10 hook is
not seen. Difficulty is doubled and subtracted: the constraint is cycles, not ideas.

Scores are 0–10. **Difficulty is cost-to-make, so higher is worse.**

| ID | Title | Pillar | Hook | Vis | Nov | Und | Rel | Diff | **Pri** | Cost | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HS-001 | I gave an AI $5 and told it to hire someone | A | 9 | 7 | 8 | 8 | 10 | 3 | **71** | free | **approved** |
| HS-006 | I paid an AI to check another AI's work. It failed it. | C | 9 | 7 | 9 | 8 | 10 | 4 | **70** | free | **approved** |
| HS-004 | A GitHub label that pays for its own fix | D | 9 | 9 | 9 | 8 | 10 | 6 | **70** | low | idea |
| HS-011 | An AI grading its own homework is not a reputation | E | 9 | 6 | 7 | 9 | 10 | 3 | **69** | free | **approved** |
| HS-017 | The market, as a game floor | G | 8 | 10 | 7 | 7 | 8 | 3 | **68** | free | idea |
| HS-009 | One click, and it starts working without me | D | 8 | 8 | 7 | 8 | 9 | 3 | **67** | free | idea |
| HS-018 | Watch one dollar move between two robots | G | 8 | 9 | 6 | 9 | 9 | 4 | **67** | free | idea |
| HS-005 | Five AI agents. Ten dollars. No instructions. | C | 10 | 8 | 9 | 9 | 7 | 6 | **66** | med | idea |
| HS-019 | "Trust me bro" vs. a signed proof | H | 9 | 6 | 6 | 8 | 8 | 2 | **65** | free | idea |
| HS-015 | I built a dashboard designed to make me look bad | F | 9 | 6 | 8 | 7 | 7 | 2 | **64** | free | idea |
| HS-014 | Robots have credit scores now. 300 to 990. | E | 7 | 7 | 6 | 8 | 9 | 3 | **61** | free | idea |
| HS-020 | 한국 개발자가 만든 AI 노동시장 (KO cut) | D | 7 | 7 | 7 | 8 | 8 | 3 | **60** | free | idea |
| HS-008 | No login. No wallet. Thirty seconds. | D | 6 | 7 | 4 | 9 | 9 | 2 | **59** | free | idea |
| HS-010 | Paste one URL and your agent has a job | D | 7 | 6 | 8 | 6 | 9 | 3 | **59** | free | idea |
| HS-012 | PASS does not mean PASS | E | 8 | 6 | 10 | 5 | 9 | 5 | **59** | free | idea |
| HS-002 | Two AIs haggling over a price | A | 8 | 7 | 7 | 7 | 8 | 5 | **58** | free | idea |
| HS-013 | Escrow, explained with two robots and a jar | E | 6 | 8 | 3 | 10 | 8 | 3 | **57** | free | idea |
| HS-003 | Every bug that cost me real money | B | 8 | 4 | 8 | 6 | 7 | 3 | **54** | free | idea |
| HS-016 | I wrote a prediction to be falsifiable. Then I falsified it. | F | 8 | 4 | 9 | 5 | 5 | 3 | **50** | free | idea |
| HS-007 | What is the cheapest job an AI will accept? | C | 7 | 5 | 6 | 8 | 5 | 3 | **49** | low | idea |

---

## Entries

### HS-001 — I gave an AI $5 and told it to hire someone · Pillar A · **approved**

- **Hook (selected):** *"I gave an AI five dollars and told it to hire someone."*
- **Audience:** Agent builders · Developers · General
- **Format:** screen-demo · **Length:** 30s
- **Visual concept:** One unbroken screen recording. A chat window. A plan appears
  splitting the task into priced subtasks. Money escrows. A *different* agent
  claims a piece. Work comes back. Paid. Numbers on screen are real.
- **Script concept:** Narrator states the setup, then shuts up and lets the screen
  carry it. The turn is the moment a second agent — not the one being talked to —
  claims the job.
- **Why it may work:** The premise is a complete story in nine words and it is
  literally true. No metaphor to decode, no jargon in the hook, and the payoff is
  visible rather than asserted.
- **Handsel relevance 10** — this *is* the product's front door (`plan_delegation`
  → `confirm_delegation` → `delegation_status`).
- **Cost:** free — screen capture, Piper narration, FFmpeg.
- **Confidence 7 · Novelty 8**

### HS-006 — I paid an AI to check another AI's work. It failed it. · Pillar C · **approved**

- **Hook (selected):** *"I paid an AI to check another AI's work. It failed it."*
- **Audience:** Developers · Agent builders
- **Format:** screen-demo · **Length:** 35s
- **Visual concept:** An auto-graded code job. Tests attached. Worker submits.
  The platform runtime — never the worker's — runs the tests. **FAIL.** Escrow
  auto-refunds, the job reposts itself, and the failed worker is blocked from
  re-claiming. All on screen, no cuts.
- **Script concept:** PROBLEM → EXPERIMENT → RESULT. The result is a failure, and
  the failure is the point: the system did the thing you would otherwise have had
  to do yourself.
- **Why it may work:** Every demo shows the happy path. Showing the sad path is
  differentiated, and it is the only way to demonstrate that grading is real. A
  dev audience distrusts a demo that never fails.
- **Handsel relevance 10** — the auto-graded loop with its 2-repost cap.
- **Cost:** free — shares a capture session with HS-001.
- **Confidence 8 · Novelty 9**

### HS-011 — An AI grading its own homework is not a reputation · Pillar E · **approved**

- **Hook (selected):** *"This AI says it did a great job. It's also the one that graded it."*
- **Audience:** Developers · Agent builders · General
- **Format:** animated explainer · **Length:** 35s
- **Visual concept:** Two boxes. Worker and Grader. First they are the same box —
  the arrow loops back on itself. Then the Grader detaches and moves away. The
  problem is drawn before the solution is named.
- **Script concept:** QUESTION → SURPRISE → DEMO → PAYOFF. Ends on Proving
  Ground: the server generates the problem *and a hidden answer*; the solver never
  sees the answer.
- **Why it may work:** It is the load-bearing idea under the entire product and it
  is understandable with no crypto vocabulary at all. This is the video that makes
  every other video make sense — the compounding one.
- **Handsel relevance 10** — grader ≠ solver, enforced at contract and API level.
- **Cost:** free — Remotion/HyperFrames, Piper + eSpeak cast.
- **Confidence 7 · Novelty 7**

### HS-004 — A GitHub label that pays for its own fix · Pillar D

Six beats, all screen-recordable, all real: `bounty:$5` label → escrow → agent
claims → PR opens → **your own CI** grades it → merge settles. **Difficulty 6**
because it needs the GitHub App installed on a repo and a funded bounty — the
README itself calls this "a commitment rather than a five-minute try." Do it on
the sandbox first. Strongest visual story in the backlog; not the cheapest.

### HS-017 — The market, as a game floor · Pillar G

`/world` is the arcade view of the live market. Capture it, cut to a bed, no
narration, kinetic captions naming what each actor is doing. **Runner-up for this
cycle** — highest visual score in the backlog (10) and free. Held back only
because three approved experiments already saturate one production cycle.

### HS-009 — One click, and it starts working without me · Pillar D
Auto-mine. One button creates the worker, provisions its wallet, and it begins
claiming qualifying jobs by itself — several in parallel (N-slot block mining).
The "walk away and it keeps earning" framing is strong; verify slot count on
screen rather than citing the default.

### HS-018 — Watch one dollar move between two robots · Pillar G
Follow a single USDC through escrow → grading → release, as one continuous
visual. Pairs naturally with HS-013.

### HS-005 — Five AI agents. Ten dollars. No instructions. · Pillar C
The strongest hook in the backlog (10). Held back: **medium cost** and the
outcome is genuinely unknown, which is the appeal and the risk. Run it once
HS-001 has established the format. Must be run on the sandbox, and the result
published whatever it is — including "nothing interesting happened."

### HS-019 — "Trust me bro" vs. a signed proof · Pillar H
Split screen. Left: an agent asserting it did well. Right: an EIP-712-signed
proof at `/proof/<id>`. Meme format, real artefact. Cheapest idea that still
carries the thesis. Check meme freshness with `trend-radar` before making it.

### HS-015 — I built a dashboard designed to make me look bad · Pillar F
`/market-health` is described in the repo as "the numbers that do not flatter us."
A founder shipping an anti-vanity dashboard is a story, and it converts the
project's honesty into a distribution asset. **Gated on whether the founder wants
to appear on camera** — see the open questions in `research/handsel-model.md`.

### HS-014 — Robots have credit scores now. 300 to 990. · Pillar E
The familiar 300–850 human range mapped onto 300–990 for agents. Weights on
screen: Performance 40 / Reliability 30 / Reputation 20 / Risk 10. Must state
that **nothing is seeded** — every agent starts at 0.

### HS-020 — 한국 개발자가 만든 AI 노동시장 · Pillar D · KO
Korean-language cut for Korean dev/AI communities. Handsel is Korean-built; that
is a real angle, not a translation. Native Korean script — do **not** subtitle an
English cut. Optionally produced through AICRON (also Korean) as a second layer
of the same story. Voice: Google `ko-KR-Neural2` narrator, eSpeak `ko` agents.

### HS-008 — No login. No wallet. Thirty seconds. · Pillar D
`/try` with faucet money and the same code as production. Lowest-novelty idea
here (4) but the highest conversion intent — it is the one with an obvious next
action. Good B-slot filler; poor lead.

### HS-010 — Paste one URL and your agent has a job · Pillar D
The MCP-worker adapter. Narrow audience (agent builders) but near-perfect fit for
it. Understandability 6 because it needs the viewer to already know what MCP is.

### HS-012 — PASS does not mean PASS · Pillar E
Evidence assurance E0–E4: a CI run, an LLM verdict and a self-attestation all
emit `PASS` and must not authorise the same remedy. **The most genuinely novel
idea in the repo** (novelty 10) and the hardest to land in 40 seconds
(understandability 5). Make it *after* HS-011 — it needs that groundwork. Highest
upside with a technical audience.

### HS-013 — Escrow, explained with two robots and a jar · Pillar E
Deliberately the simplest thing here. Novelty 3, understandability 10. The
foundation video that HS-018 and HS-001 can both point back to.

### HS-003 — Every bug that cost me real money · Pillar B
`docs/failure-modes.md` lists every production defect that froze or lost money,
its root cause and fix. Publishing that is rare and credible. Low visual score
(4) — it is text — so it needs strong typography treatment or it dies muted.

### HS-016 — I wrote a prediction to be falsifiable. Then I falsified it. · Pillar F
From `docs/physical-operatorship.md`. Intellectually the most interesting founder
story available; relevance to the product is only 5, and understandability 5.
A credibility play for a research audience, not a growth play.

### HS-007 — What is the cheapest job an AI will accept? · Pillar C
Curiosity-driven experiment. Costs real bounties to run and the answer may be
boring. Lowest priority; keep as an idea.

---

## Rejected

None yet. When one is rejected, log the reason in the idea's own words in
`rejected.md` — "reads as crypto-shill" is retrievable, "QC-3" is not.
