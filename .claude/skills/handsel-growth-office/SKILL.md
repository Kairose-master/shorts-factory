---
name: handsel-growth-office
description: Invoke first for any Handsel promotion, marketing, or short-form content request — researching what to make, generating or ranking content ideas, writing hooks or scripts about Handsel, producing a video, quality-checking one, packaging it for publish, or reading results back into strategy. Owns the Office's fourteen-step pipeline, the role map, the autonomy boundary (nothing publishes without human approval), the factual-accuracy rule against inventing Handsel functionality, and routing to the 49 installed skills.
---

# Handsel Short-Form Growth Office

The Office is a **learning content machine** for growing awareness and adoption of
Handsel. It lives in `office/` at the repo root. Read `office/CHARTER.md` before
acting on anything below — it is the constitution; this file is the routing table.

> This skill sits **above** `shorts-factory`. `shorts-factory` owns the generic
> research pipeline and the 43 upstream skills. This one owns the Handsel mission,
> the Office's memory, and the approval boundary. For a Handsel request, start here.

## Before anything else

1. **Read `office/research/handsel-model.md`.** Every factual claim in every
   script must trace to a line in it. **Never invent Handsel functionality.** If
   a claim cannot be traced, it does not go in the video.
2. **Read its DO NOT CLAIM ledger.** Handsel is at a genuine cold start with no
   formal contract audit. Claiming traction or security would be false *and*
   off-brand for a project that ships a page called "the numbers that do not
   flatter us."
3. **Check `office/memory/`** — backlog, hooks, rejected, lessons. Do not
   regenerate a rejected concept or re-propose a discarded hook.

## The autonomy boundary — the one rule that never bends

**Nothing publishes without explicit human approval.** Not a draft to a live
account, not a scheduled post, not a "test" upload. Every time, no standing
pre-approval.

Also needs approval: spending on any metered API, contacting anyone outside the
Office, moving money, changing permissions, deleting a record.

Everything else — research, ideation, hooks, scripts, scene plans, free-tier
rendering, QC, writing to `office/memory/` — runs without asking.

**When blocked:** diagnose → find an alternative → take the safest reversible
action → continue. Never stall on a missing key. Name the variable, say what it
would have improved, run the open path, label which mode produced each number.

## Routing

| The ask | Go to |
|---|---|
| "what's working in AI/dev short-form" | `trend-discovery` → `trend-radar` |
| "why did that video pop" | `content-autopsy` → `hook-anatomy` |
| "give me Handsel video ideas" | `viral-short-form-ideas` + `office/memory/backlog.md` |
| "write hooks" | `viral-hooks` → log every variant to `office/memory/hooks.md` |
| "critique this hook" | `hook-anatomy` |
| "write the script" | `viral-short-form` → the platform skill |
| "make the video" | `openmontage` (+ `voicebox`, `penpot`, `aicron`) |
| "narration / which voice" | `voicebox` — its bundled voice-casting reference holds the standing cast |
| "title card, brand consistency" | `penpot` → `brand-kit` |
| "generative shot the free path can't do" | `aicron` — **HUMAN step, paid** |
| "is it good enough" | `office/sop/quality-control.md` |
| "write the caption" | `viral-captions-and-ctas` → `platform-fluency` |
| "publish it" | **stop. Package it and request approval.** |
| "how did it do" | `office/sop/analytics-loop.md` → `comment-mining`, `read-the-room` |
| "store this in a database" | `airtable` (schema) — Notion today, Airtable when connected |
| "make something happen outside" | `zapier-mcp` — **not connected**; read it before promising |

Pick the **narrowest** skill that matches. `viral-hooks` generates, `hook-anatomy`
diagnoses. `trend-discovery` finds, `trend-radar` judges.

## The cycle

```
observe → ideate → score → GATE → produce → QC → package → APPROVE → publish
→ measure → bucket the failure → lesson → back to observe
```

Full step table: `.claude/skills/openmontage/references/office-integration.md`.
SOPs: `office/sop/`.

## Standing rules

- **One idea per video.** A second idea is a second video.
- **One variable per experiment.** Two arms. Hypothesis written *before* publishing.
- **Never optimise from one observation.** `Observations: 1` is a note, not a lesson.
- **`unmeasured` is written, never estimated.** A guessed retention figure poisons
  every lesson derived from it.
- **Log the rejects.** Ideas, hooks, renders. In plain words, with what was worth
  keeping.
- Raw views are not performance — baseline-relative or it does not count.
- Never promise virality.

## Cost gate

Free: Piper · eSpeak · Remotion · HyperFrames · FFmpeg · archive footage · every
prose skill · `read-the-room`.

Metered: ScrapeCreators · Apify · TubeLab · Gemini · every generative provider ·
AICRON. Say roughly how many calls a plan makes **before** making them, and never
run a paid provider before the Gate.
