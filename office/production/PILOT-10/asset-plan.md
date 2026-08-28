# PILOT — "I gave an AI company $10" · ASSET_HUNTER first boot

**Purpose: prove `SCRIPT → ASSET DISCOVERY → ASSET CREATION → EDITOR HANDOFF`
works without the editor searching for media.** Not a publish candidate.

Target 26s · 1080×1920 · 20 beats of 0.5–3s.

---

## ⚠️ Before anything: the premise has not happened

Handsel ships `hire_office` and `list_office_templates` — **6 real templates**
with suggested budgets: talent-agency $2, bootstrap-desk $4, research-desk $6,
securities-desk $8, **due-diligence-desk $10**, cloud-options-desk $12.

So *"I gave an AI company $10"* maps cleanly onto a real, shipped feature — and
**nobody has run it.** There is no capture of it. Every hero beat below is
therefore `RECORD_HANDSEL`, i.e. **the footage must be created before this video
can exist.**

That is the pilot's most useful finding: the asset layer works, and it reports
that the protagonist footage does not exist yet rather than papering over it with
stock. Per the Charter, running it on **mainnet costs real USDC and needs
approval**; the sandbox is free and is the right place.

---

## Beat table

`SRC` = asset decision engine outcome. **B1–B20, none longer than 3s.**

| # | t | HEARING | SEEING | MUST UNDERSTAND | EMOTION | SRC |
|---|---|---|---|---|---|---|
| B1 | 0.0–0.8 | *"I gave"* | `$10.00` slams in, hard cut, no logo | a specific small sum | curiosity | `REMOTION_GENERATED` |
| B2 | 0.8–1.8 | *"an AI company"* | office template card resolves: **Due Diligence Desk** | it is a *company*, not a chatbot | surprise | `RECORD_HANDSEL` |
| B3 | 1.8–2.8 | *"ten dollars."* | treasury `$0.00 → $10.00` ticks | the money is now theirs | anticipation | `RECORD_HANDSEL` + `REMOTION_GENERATED` overlay |
| B4 | 2.8–4.2 | *"I didn't tell it what to do."* | five role cards deal out: commercial · financial · legal · partner · red-team | it has *staff* | escalation | `RECORD_HANDSEL` |
| B5 | 4.2–5.6 | — (beat) | contract lines connect the five | they are wired to each other | structure | `REMOTION_GENERATED` |
| B6 | 5.6–7.4 | *"It hired its own staff."* | three roles activate in parallel | work started without me | momentum | `RECORD_HANDSEL` |
| B7 | 7.4–8.6 | *"Three of them worked at once."* | `$1.67` × 3 debits | each one costs | cost pressure | `REMOTION_GENERATED` |
| B8 | 8.6–10.0 | *"Then a fourth one read all three."* | partner card pulls from the three | synthesis, not duplication | order | `REMOTION_GENERATED` |
| B9 | 10.0–11.6 | *"and a fifth attacked the result."* | red-team card turns adversarial | **it argues with itself** | tension | `REMOTION_GENERATED` |
| B10 | 11.6–13.0 | — | `REVISE` stamp; work returns to partner | rejection is a loop, not an end | reversal | `REMOTION_GENERATED` (`VerifierStamp` state=`REVISE`) |
| B11 | 13.0–14.4 | *"Nobody asked me anything."* | cursor idle, nothing to click | no human in the loop | unease | `RECORD_HANDSEL` |
| B12 | 14.4–16.0 | *"The treasury went down."* | `$10.00 → $1.67` counter | money actually left | consequence | `REMOTION_GENERATED` (`TreasuryCounter`) |
| B13 | 16.0–17.4 | *"Every dollar went to a different worker."* | five debits fan to five wallets | it is a payroll, not a bill | realisation | `REMOTION_GENERATED` (`MoneyTransfer` ×5) |
| B14 | 17.4–19.0 | *"I got a memo back."* | the assembled deliverable scrolls | there is a real output | payoff | `RECORD_HANDSEL` |
| B15 | 19.0–20.4 | *"I didn't write any of it."* | scroll continues, hands nowhere | authorship is not mine | payoff | `RECORD_HANDSEL` |
| B16 | 20.4–21.6 | — | hold on one paragraph, punch 110% | it is legible work | credibility | `RECORD_HANDSEL` |
| B17 | 21.6–23.0 | *"Ten dollars."* | `$10.00` returns, now spent | bookend | closure | `REMOTION_GENERATED` |
| B18 | 23.0–24.2 | *"One company."* | the five cards collapse into one | it was an org all along | resolution | `REMOTION_GENERATED` |
| B19 | 24.2–25.4 | *"Nobody clocked in."* | empty seats / zero avatars | no humans, stated plainly | quiet | `REMOTION_GENERATED` |
| B20 | 25.4–26.0 | — | `handsel-main.vercel.app` | where to go | — | `EXISTING_HANDSEL_ASSET` |

## Source tally — and what it says

| Source | Beats | Note |
|---|---|---|
| `REMOTION_GENERATED` | **11** | agent-native concepts; no honest stock equivalent |
| `RECORD_HANDSEL` | **8** | **all blocked — footage does not exist yet.** B3 is a hybrid (capture + generated overlay) and counts here: the overlay cannot be composited over footage that does not exist. |
| `EXISTING_HANDSEL_ASSET` | 1 | end card |
| `PEXELS_VIDEO` / `PEXELS_PHOTO` / `UNSPLASH_PHOTO` | **0** | see below |

**Zero stock beats, and that is the right answer, not a consequence of the
missing keys.** I ran query generation for the two beats that could plausibly
take stock (B1 money, B11 idle cursor):

- B1 — `money counting` · `ten dollar bill` · `cash on table` · `digital wallet
  payment` · `startup funding` · `capital allocation` · `investment animation` ·
  `finance transaction`. Every result would be a *human* handling *physical*
  cash. The video's entire claim is that no human touched it. **Stock here would
  contradict the script.** → `REMOTION_GENERATED`.
- B11 — `empty desk` · `idle computer` · `office at night` · `nobody working` ·
  `abandoned workstation`. Generic and slower to read than the product's own idle
  cursor. → `RECORD_HANDSEL`.

This is the decision engine working as designed: real behaviour first, generated
motion for agent-native ideas, stock only as texture — and here there is no
texture worth buying.

## Motion requests → MOTION_DESIGNER

Nine requests, resolved by **six** primitives — B7/B13 and B12/B17 and B3 share
components with different props, which is the anti-duplication rule doing its job.

| Request | Primitive | Props | Reuse |
|---|---|---|---|
| `mo-001` B1/B17 | `TreasuryCounter` | `from:0 to:10`, then `10→0` spent state | 2 beats |
| `mo-002` B3/B12 | `TreasuryCounter` | `0→10`; `10→1.67` | shares `mo-001` |
| `mo-003` B5 | `ContractLine` | 5 endpoints, `state:proposed` | new |
| `mo-004` B7/B13 | `MoneyTransfer` | `amount:1.67`, 5 destinations | 2 beats |
| `mo-005` B8 | `ContractLine` | converging, `state:escrowed` | shares `mo-003` |
| `mo-006` B9 | `AgentBattle` | red-team vs partner | new |
| `mo-007` B10 | `VerifierStamp` | **`verdict:REVISE`** | new — and note it is neither PASS nor FAIL, which is exactly why the primitive needs more than two states |
| `mo-008` B18 | `OfficeHire` | collapse variant | new |
| `mo-009` B19 | `AgentSpawn` | zero-avatar/empty state | new |

## Gaps — the honest blockers

| Code | What | Why |
|---|---|---|
| `RECORD_HANDSEL` ×8 | B2, B3, B4, B6, B11, B14, B15, B16 | **Nobody has run `hire_office` with $10.** Sandbox run needed; mainnet needs approval and real USDC. |
| `BLOCKED: PEXELS_API_KEY_REQUIRED` | — | Costs this pilot **nothing** — zero stock beats. |
| `BLOCKED: FREESOUND_API_KEY_REQUIRED` | all SFX | Counter ticks, the `REVISE` stamp and the five debits all want sound. **Free key.** Highest-value unblock for this video. |
| `BLOCKED: UNSPLASH_ACCESS_KEY_REQUIRED` | — | Not needed here. |

## A note on how these numbers were checked

The counts above are generated and asserted by the script that emits
`asset-handoff.json`, not counted by hand. It caught this document claiming 7
capture beats when there are 8 — B3 is a hybrid, and a generated overlay cannot
composite over footage that does not exist. Corrected here. The same script
asserts every beat is 0.5–3.0s and that the timeline has no gaps.

## Provenance

`asset-manifest.json` is initialised with **zero external assets** — nothing has
been downloaded, so nothing needs a licence row yet. All nine motion requests
will register as `source: "remotion"`, `license: "proprietary-owned"`,
`commercial_use: true`. All eight captures register as
`source: "handsel-capture"`, same licence.

**No asset in this plan carries `license: UNKNOWN`.**

## What the editor would receive today

`asset-handoff.json` holds all 20 beats. **12 of 20 are resolvable right now**
(11 generated + 1 existing). **8 are blocked on one sandbox run.** The editor
does not have to search for anything in either case — blocked beats carry the
capture instruction, not a research task.

**Pipeline verdict: the chain works.** The one thing standing between this plan
and a cut is a product run that has never been performed — which the asset layer
surfaced rather than hid.
