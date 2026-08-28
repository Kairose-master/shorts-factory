# HS-006 — "I paid an AI to check another AI's work. It failed it."

**Pillar C** (weird AI economy experiments) · **Priority 70** · **Status: approved, not produced**
Format: screen-demo · Target: 35s · 1080×1920 · Platforms: YouTube Shorts → TikTok → Reels

## Hypothesis

A developer audience distrusts demos that never fail. Showing the grader
**rejecting** work will hold attention better than showing a successful
transaction, despite the weaker premise. Arm B of EXP-001 — and the arm the
Office expects to win (prior P-02).

## Hook

**Selected:** *"I paid an AI to check another AI's work. It failed it."*
Five other variants in `../../memory/hooks.md`. Variant C — *"The tests failed.
Nobody had to notice."* — is used as the pinned-comment line instead.

## Script — 35s

| t | On screen | Audio | Caption |
|---|---|---|---|
| 0.0–0.4 | test file already scrolling | — | — |
| 0.4–4.0 | the job posting, acceptance tests attached | **NARRATOR:** "I paid an AI to check another AI's work." | `I paid an AI to check another AI's work` |
| 4.0–7.0 | worker claims, starts writing | NARRATOR: "This one wrote the code." | `worker: writing` |
| 7.0–11.0 | submission | **AGENT-B:** "Submitting." | `submitted` |
| 11.0–15.0 | **hold** — tests running, and the runner is labelled *platform*, not *worker* | NARRATOR: "The tests don't run on its machine. They run on ours." | `the worker does not grade itself` |
| 15.0–19.0 | **FAIL** — red, held longer than comfortable | **GRADER:** "Failed." | `FAILED` |
| 19.0–24.0 | escrow refunds — amount returns | NARRATOR: "My money came back on its own." | `escrow auto-refunded` |
| 24.0–29.0 | the job reposts itself; the failed worker greys out | NARRATOR: "The job reposted itself. That worker can't take it again." | `reposted · that worker is blocked` |
| 29.0–35.0 | cut to black, one line | NARRATOR: "I didn't check any of that. That's the point." | `handsel` |

The **FAIL at 15s must be held past comfort** — roughly 4 seconds on a red state.
Every other demo on the internet cuts away from red. Not cutting away is the
entire differentiator.

## Shot list

| # | Shot | Dur | Source | MUST CONTAIN |
|---|---|---|---|---|
| s01 | job post with tests attached | 3.6 | screen capture | the acceptance-test field, populated |
| s02 | worker claims | 3.0 | same | the worker's name |
| s03 | submission | 4.0 | same | submitted artefact |
| s04 | tests running, platform-side | 4.0 | same | **the runner labelled as platform, not worker** |
| s05 | FAIL | 4.0 | same | red verdict, legible at thumbnail size |
| s06 | refund | 5.0 | same | the amount returning to balance |
| s07 | repost + worker blocked | 5.0 | same | the same spec live again |
| s08 | end card | 6.0 | Penpot | — |

Same capture session as HS-001. Record HS-001's happy path first, then attach
failing tests and run again — one session, two videos, one variable changed.

## Assets

Identical stack to HS-001: `cap_recorder`, `voicebox` cast (NARRATOR + AGENT-B +
GRADER), `subtitle_gen` burned in, Penpot end card, Remotion compose.
**Total spend: $0.** No paid provider, no `HUMAN` step.

## Factual accuracy — every claim traced

| Claim | Source in `research/handsel-model.md` |
|---|---|
| acceptance tests can be attached to a job | §4 "auto-graded code jobs" |
| tests run on the platform runtime, never the worker's | §4, verbatim |
| a fail auto-refunds the escrow | §4 |
| the job reposts automatically | §4 |
| the failed worker is blocked from re-claiming | §4 |

**Not claimed:** that this is fully autonomous in general (jobs *without* tests
need a human Approve/Dispute — §DO NOT CLAIM). The narrator says "I didn't check
any of that" about **this** job, which is true, and the caption does not
generalise.

Also **not claimed:** the 2-repost cap or the `$50` auto-release ceiling. Both are
true and both are one detail too many for 35 seconds. They belong in HS-012.

## Risks

- **The failure must be genuine.** Write code that actually fails the tests. A
  staged failure in a video about verification would be indefensible if noticed,
  and it is the kind of thing that gets noticed.
- Red-on-dark at 1080×1920 can be illegible in a feed thumbnail. Check s05 at
  phone scale before rendering; the Penpot kit's fail token exists for this.
- "Failed" as a hook can read as *the product* failing. The caption at 11s does
  the disambiguating work — do not cut it for time.

## Definition of done

Same as HS-001. Published only after HS-001, within the same 48-hour window and
at a comparable posting time, or EXP-001 is confounded.
