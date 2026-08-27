# HS-011 — "An AI grading its own homework is not a reputation"

**Pillar E** (developer education) · **Priority 69** · **Status: approved, not produced**
Format: animated explainer · Target: 35s · 1080×1920 · Platforms: YouTube Shorts → Reels → TikTok

## Hypothesis

The concept video does not need product footage to be understood, and will be
**shared** more than the demos because it needs no context to forward. Arm A of
EXP-002.

This is the compounding video. It makes every other Handsel video legible, which
is why an education slot ships every cycle.

## Hook

**Selected:** *"This AI says it did a great job. It's also the one that graded it."*
Six other variants in `../../memory/hooks.md`. Variant D — *"An AI that is
confidently wrong looks exactly like one that is right."* — is the strongest line
available and is deployed inside the script at 0:08, where it lands harder than
as an opener.

## Script — 35s

Structure: QUESTION → SURPRISE → DEMO → PAYOFF. **No product footage. No UI.
No logo until the end card.**

| t | On screen | Audio | Caption |
|---|---|---|---|
| 0.0–0.4 | one box, already drawing itself | — | — |
| 0.4–4.0 | box labelled **WORKER**. An arrow leaves it, curves, and returns to itself. Label: **GRADE** | **NARRATOR:** "This AI says it did a great job. It's also the one that graded it." | `it graded itself` |
| 4.0–8.0 | the loop pulses. A green ✓ appears inside the box | NARRATOR: "So the score means nothing. It's a claim about a claim." | `a claim about a claim` |
| 8.0–13.0 | everything else fades; the line types on | NARRATOR: "An AI that is confidently wrong looks exactly like one that is right." | `confidently wrong looks like right` |
| 13.0–17.0 | zoom out: a human figure reading every output, one by one, tiring | NARRATOR: "Which is why you still read every output yourself." | `so you check all of it. forever.` |
| 17.0–23.0 | **the arrow detaches.** A second box slides in: **GRADER**. Worker → Grader → verdict | NARRATOR: "Unless the grading isn't done by the worker." | `move the grading out` |
| 23.0–29.0 | a third element: **HIDDEN ANSWER**, drawn behind the Grader, with a dashed line showing the Worker cannot see it | **GRADER:** "The answer was generated with the problem. The solver never sees it." | `the solver never sees the answer` |
| 29.0–35.0 | verdict → a signed proof card → money moves | NARRATOR: "Now the score is worth something. It was never yours to give." | `handsel` |

The whole video is one continuous diagram that **transforms**. Nothing is
replaced by a cut; every element earns its position by moving from the previous
state. That is what makes an abstract idea watchable muted.

## Shot list

| # | Shot | Dur | Source | MUST CONTAIN |
|---|---|---|---|---|
| s01 | self-grading loop | 3.6 | Remotion/HyperFrames | the arrow visibly returning to its origin |
| s02 | green ✓ inside the loop | 4.0 | same | the ✓ *inside* the same box |
| s03 | the aphorism, typed | 5.0 | same | the line, legible, full-width |
| s04 | human reading outputs | 4.0 | same | repetition — the tiring, not the reading |
| s05 | grader detaches | 6.0 | same | **two separate boxes and one arrow between them** |
| s06 | hidden answer | 6.0 | same | the dashed line the worker cannot cross |
| s07 | proof + payment | 6.0 | same + Penpot proof card | a signature glyph |

## Assets

| Asset | Source | Cost |
|---|---|---|
| all motion | `openmontage` → Remotion (or HyperFrames if the brief goes GSAP-heavy) | free |
| NARRATOR VO | `voicebox` → Parler/Piper | free |
| GRADER VO | `voicebox` → eSpeak NG + `Vocoder`, per `voice-casting.md` | free |
| diagram tokens (worker · grader · job · verdict) | `penpot` → the four Handsel tokens | free |
| captions | burned in | free |
| music | sparse bed, low | free |

**Total spend: $0.** No generative model. No `HUMAN` step. Deliberately: a video
arguing for verifiable process should not be made of unverifiable generated
imagery.

## Factual accuracy — every claim traced

| Claim | Source in `research/handsel-model.md` |
|---|---|
| self-graded scores are not credible | §2, the founding problem, stated verbatim |
| "confidently wrong looks exactly like right" | §2 — quoted from the repo |
| grading is moved off the worker | §1 |
| the answer is generated with the problem, solver never sees it | §4, Proving Ground |
| every verdict becomes a signed proof | §1, EIP-712 |

**Not claimed:** the four grader modalities, evidence classes, or anything about
credit. All true, all cut — one idea per video. Credit is HS-014, evidence
classes are HS-012.

## Risks

- **Abstraction dies muted if the motion is weak.** The transformation at 17s is
  load-bearing; if it reads as a cut rather than a detachment, the video fails.
  Preview s05 alone before building the rest.
- The 8–13s aphorism beat pauses the diagram for 5 seconds. Retention risk. If
  QC flags pacing, keep the line as caption-only over continuing motion.
- Risk of reading as an anti-AI video. The framing must stay *this is how you
  make AI work trustworthy*, never *AI cannot be trusted*. Check gate 8.

## Definition of done

Same as HS-001. Publish at least 48 hours after the EXP-001 pair so the two
experiments do not contaminate each other's posting windows.
