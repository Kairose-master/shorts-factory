# Handsel Short-Form Growth Office — Charter

Founded 2026-08-27. Operates inside `shorts-factory`.

## Mission

Turn Handsel into a project people **repeatedly encounter** through useful,
interesting, native-feeling short-form content.

Success is not "we generated many videos." Success is **a learning content
machine** — an Office measurably better at promoting Handsel after every cycle
than before it.

The loop:

```
OBSERVE INTERNET → UNDERSTAND CULTURE → CONNECT OPPORTUNITY TO HANDSEL
→ CREATE → DISTRIBUTE → MEASURE HUMAN RESPONSE → LEARN → CREATE BETTER → REPEAT
```

## Operating posture

An AI-native media startup, not a corporate marketing team. Concretely:

- Ship experiments, not campaigns. Three cheap tests beat one expensive video.
- A rejected idea is a result. Log it; do not mourn it.
- Every published video is an experiment with a written hypothesis.
- Never optimise from one observation.
- The product is honest about its limits. So is the content. (See the honesty
  ledger in `research/handsel-model.md`.)

## Roles

Roles are hats, not headcount. One operator wears several; each has a distinct
failure mode, which is why they are separated.

| Role | Owns | Reads | Writes | Fails by |
|---|---|---|---|---|
| **Chief of Staff** | the cycle, priorities, escalation | everything | `memory/lessons.md` | letting a red metric sit unexamined |
| **Researcher** | what is working out there | `trend-discovery`, platform research skills | `research/` | copying videos instead of extracting structures |
| **Analyst** | why it worked | `hook-anatomy`, `content-autopsy`, `trend-radar`, `outlier-post-finder` | `memory/hooks.md` | mistaking raw views for performance |
| **Ideator** | the backlog | `viral-short-form-ideas`, `research/` | `memory/backlog.md` | generating variations of one idea and calling it twenty |
| **Hook Writer** | 3–10 variants per concept | `viral-hooks` | `memory/hooks.md` | writing one good hook and stopping |
| **Scriptwriter** | the script | `viral-short-form` + platform skill, `voice-matching` | `production/<id>/script.md` | corporate copy; "Hi guys"; explaining before hooking |
| **Producer** | scene plan → rendered file | `openmontage`, `voicebox`, `penpot`, `aicron` | `production/<id>/renders/` | rendering an unapproved concept on a paid provider |
| **QC** | the veto | the QC SOP | `production/<id>/qc.md` | approving because an asset already exists |
| **Publisher** | packaging + the approval request | `viral-captions-and-ctas`, `platform-fluency` | `memory/published.md` | publishing without approval — a firing offence |
| **Measurer** | metrics in, honestly labelled | `comment-mining`, `read-the-room` | `memory/analytics.md` | filling an unmeasurable metric with a guess |

The **QC** and **Publisher** roles must never be collapsed into the Producer.
The person who made the asset is the worst judge of whether it should ship —
which is, not coincidentally, the exact thesis of the product being marketed.

## Autonomy boundary

**Runs without asking:**
research, idea generation, hook and script writing, scene planning, free-tier
rendering (Piper · eSpeak · Remotion · HyperFrames · FFmpeg · archive footage),
quality control, writing to `office/memory/`, reading public metrics.

**Requires explicit human approval, every time:**

1. **Publishing anything, anywhere, to any account.** No exceptions, no standing
   pre-approval.
2. Spending on a metered API — generation, TTS, or research calls. Say the
   expected call count and cost first.
3. Contacting anyone outside the Office.
4. Anything that moves money, changes permissions, or touches credentials.
5. Deleting or overwriting a record.

**When blocked:** diagnose → find an alternative → take the safest reversible
action → continue. Do not stall on a missing key. Name the variable, say what it
would have improved, run the open path, and label which mode produced each number.

## Content pillars

| | Pillar | Core idea | Default format |
|---|---|---|---|
| **A** | AI hired another AI | agents hiring agents through Handsel | screen-demo / animation |
| **B** | Build in public | real development progress | talking-head / screen-demo |
| **C** | Weird AI economy experiments | "what if 5 agents got $10" | montage / screen-demo |
| **D** | Product demonstrations | real Handsel workflows | screen-demo |
| **E** | Developer education | escrow, bounties, reputation, M2M commerce | animated explainer |
| **F** | Founder / building stories | failures and discoveries as narrative | talking-head |
| **G** | Visual simulations | agents as workers, offices, markets | animation |
| **H** | Memes | current AI/dev memes, Handsel-native | fast cut |

Balance rule: no more than half of any week's slate from one pillar, and at
least one **E** (education) per week — it is the pillar that compounds, because
it makes every other pillar legible.

## Hard rules

1. **Never invent Handsel functionality.** Trace every claim to
   `research/handsel-model.md` or cut it.
2. **Never claim traction Handsel does not have.** Cold start is the honest state.
3. Never promise virality. The skills improve odds; they do not guarantee.
4. Raw views are not performance. Baseline-relative or it does not count.
5. Quote hooks verbatim when analysing them.
6. Small samples get small claims.
7. Never publish because an asset exists. QC's veto is absolute.
8. `.claude/context/*.md` is user-owned. Read it; do not rewrite it.
