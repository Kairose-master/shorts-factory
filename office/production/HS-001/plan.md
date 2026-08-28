# HS-001 — "I gave an AI $5 and told it to hire someone"

**Pillar A** (AI hired another AI) · **Priority 71** · **Status: approved, not produced**
Format: screen-demo · Target: 30s · 1080×1920 · Platforms: YouTube Shorts → TikTok → Reels

## Hypothesis

A literal, unexaggerated premise stated flat will out-hook a question or a
reveal, *because* the footage then delivers exactly what the hook promised. Arm A
of EXP-001.

## Hook

**Selected:** *"I gave an AI five dollars and told it to hire someone."*
Six other variants and the reasoning are in `../../memory/hooks.md`.

## Script — 30s

| t | On screen | Audio | Caption |
|---|---|---|---|
| 0.0–0.3 | cursor already typing, mid-sentence | — | — |
| 0.3–3.0 | the prompt lands in the chat | **NARRATOR:** "I gave an AI five dollars and told it to hire someone." | `I gave an AI $5 and told it to hire someone.` |
| 3.0–8.0 | the plan renders: subtasks, each with a price | NARRATOR: "It didn't do the work. It wrote a plan and put a price on every piece." | `it priced the work` |
| 8.0–12.0 | escrow confirms — amount visible | **AGENT-A:** "Escrowing four dollars and eighty cents." | `money locked before anyone starts` |
| 12.0–17.0 | **a different agent claims a subtask** — hold on the name change | **AGENT-B:** "Claimed." | `a different agent took it` |
| 17.0–22.0 | the deliverable comes back | NARRATOR: "Nobody asked me anything." | `no human in the loop` |
| 22.0–27.0 | grading verdict → escrow releases | **GRADER:** "Pass. Released." | `graded by neither of them` |
| 27.0–30.0 | balance ticks up. cut to black on the number | NARRATOR: "Five dollars. Two robots. One of them got paid." | `handsel` |

The turn is at **12.0s** — the moment the viewer sees a *second* agent. Everything
before it is setup; the shot must hold long enough for the name change to land.

## Shot list

| # | Shot | Dur | Source | MUST CONTAIN |
|---|---|---|---|---|
| s01 | prompt being typed | 3.0 | screen capture, MCP client | the literal sentence from the hook |
| s02 | plan with priced subtasks | 5.0 | same capture | a visible price next to a task |
| s03 | escrow confirmation | 4.0 | same capture | the dollar amount |
| s04 | second agent claims | 5.0 | same capture | **a different agent name than s02** |
| s05 | deliverable returns | 5.0 | same capture | actual output text, not a spinner |
| s06 | grading verdict | 5.0 | same capture | the word PASS and who issued it |
| s07 | balance | 3.0 | same capture | the number changing |

One continuous capture session; shots are timecodes into it, not separate takes.
**HS-006 is recorded in the same session** — that is why these two were approved
together.

## Assets

| Asset | Source | Cost |
|---|---|---|
| screen capture | `openmontage` → `cap_recorder` | free |
| NARRATOR VO | `voicebox` → Parler/Piper | free |
| AGENT-A / AGENT-B / GRADER VO | `voicebox` → eSpeak NG + effects, per `voice-casting.md` | free |
| captions | `openmontage` → `subtitle_gen`, burned in | free |
| title + end card | `penpot` → `export_shape` (falls back to a Remotion text card) | free |
| music bed | `music_library` / Freesound, low, ducked under VO | free |
| compose + render | Remotion, 1080×1920 | free |

**Total spend: $0.** No paid provider. No `HUMAN` step.

## Sandbox, not mainnet

Record on the **testnet sandbox** (`/try`, faucet money, same code as
production). The video must not imply the amounts are real USDC — an on-screen
`sandbox` marker stays visible, or the narrator says "test money." Recording on
mainnet would spend real money for a take that may be discarded, and would need
approval under the Charter's autonomy boundary.

## Factual accuracy — every claim traced

| Claim | Source in `research/handsel-model.md` |
|---|---|
| the plan prices subtasks | §1, `plan_delegation` |
| escrow happens before work | §1 "escrowed before work starts" |
| a different agent claims it | §1 |
| grading is by neither party | §4 "grader ≠ solver, enforced" |
| payment releases on pass | §1 |

**Not claimed:** any traction number, any speed claim, anything about the money
being real.

## Risks

- **The run fails or stalls on camera.** Acceptable — that becomes HS-006's
  footage. Do not fake a successful run.
- The turn at 12s is invisible if both agent names look alike. Check before
  recording; if they do, add a colour token from the Penpot kit.
- 30s is tight for seven beats. If QC flags pacing, cut s05 and let the verdict
  imply the delivery.

## Definition of done

`renders/final.mp4` at 1080×1920 with burned captions, `qc.md` scoring ≥30/45
with no gate under 3, three platform captions written, and an approval request
posted. **Then stop.**
