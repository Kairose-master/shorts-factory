---
name: open-generative-ai
description: Use when a shot needs a generative image, video, or lip-sync clip and the job should stay scriptable (no human at a GUI) — Muapi.ai is a single paid REST API in front of 250+ generation models (Flux, Kling, Sora, Veo among them), and Open-Generative-AI (github.com/Anil-matcha/Open-Generative-AI, MIT) is an open-source Electron/web front end for it. Needs MUAPI_API_KEY, which is NOT set in this workspace — say so and stop rather than inventing one. Paid, metered per generation; gated like every other paid provider in CLAUDE.md.
---

# Open-Generative-AI / Muapi — the scriptable generation API

Evaluated 2026-09-01 at the channel owner's request
(`github.com/Anil-matcha/Open-Generative-AI`). Two things are actually being
described here, and they are not the same:

1. **Open-Generative-AI** — an MIT-licensed Electron/web app. Its own README
   markets it as an alternative to subscription AI-video platforms. It has no
   generation capability of its own.
2. **Muapi.ai** — the paid API the app calls for every generation. "Powered by
   Muapi.ai" — one `x-api-key`, one credit balance, 250+ models across image,
   video, audio and lip-sync, reachable directly over REST with no app in the
   loop at all.

**The app is UI sugar. The API is the actual capability.** For this office's
scripted, no-GUI pipeline, calling Muapi's REST API directly (curl, the same
shape as `scrapecreators-api`) is the right integration — not cloning the repo,
running `npm run setup`, and driving an Electron window.

## What this adds over what's already installed

| | Free path (OpenMontage) | AICRON | Muapi.ai |
|---|---|---|---|
| Cost | $0 | subscription | pay-per-generation credits |
| Interface | scripted | human at a GUI | REST API |
| Automatable | yes | **no** — no public API | **yes** |
| Model range | Piper/Remotion/HyperFrames only | 200+, one canvas | 250+, one API |

AICRON (`.claude/skills/aicron/SKILL.md`) is deliberately human-operated — it
has no API, so a plan that uses it always stops for a person. Muapi is the
opposite trade: it *can* run inside an autonomous stage, at the cost of a
metered bill per call and no operator judgment in the loop. Route here only
when both are true:

1. The shot genuinely needs generative image/video/lip-sync the free path
   (Archive.org footage, Remotion, HyperFrames, Piper) cannot produce.
2. The job should stay scriptable — no operator available, or the volume is
   too high for a human to sit at AICRON for each shot.

If a human operator IS available and the volume is low, prefer AICRON — one
subscription beats per-call billing for a handful of shots, and a person
catches a bad generation before it costs a second call.

## The credential this needs — not set

**`MUAPI_API_KEY` is not in `.env.example` or `.env` in this workspace.**
Per the ground rules in `CLAUDE.md` ("never invent a credential"), this skill
cannot be used until:

1. A human signs up at Muapi.ai and generates an `x-api-key` in the developer
   panel (per Muapi's own docs — this office has not evaluated their pricing
   or terms in enough depth to recommend a plan).
2. `MUAPI_API_KEY=` is added to `.env.example` (done, see below) and filled
   into `.env`.

Until then, any plan that reaches this skill should say "MUAPI_API_KEY is
missing, here's what it would let us do" and stop — the same pattern as any
other missing key in this repo.

## How to call it, once a key exists

Muapi is a REST API, not an SDK dependency — no npm install, no cloning the
Open-Generative-AI repo required. The shape (confirm exact paths against
Muapi's current docs before the first real call, since this has not been
run yet in this workspace):

```bash
curl -s -X POST "https://api.muapi.ai/v1/generate" \
  -H "x-api-key: $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model id from Muapi'"'"'s catalog>",
    "input": { "prompt": "<prompt>", "aspect_ratio": "9:16" }
  }'
```

Submission is async — poll or receive a webhook, then fetch the output asset
URL. Failed generations are not billed (per Muapi's pricing page), so a
malformed request costs nothing — but don't rely on that as a reason to skip
validating inputs first.

## Rules

- **Metered per generation.** Falls under the cost gate in `CLAUDE.md` — say
  which model and roughly how many calls a shot will take before running it,
  same as ScrapeCreators/Apify/Gemini.
- **Never invent `MUAPI_API_KEY`.** If it's not in `.env`, name it and stop.
- **Commercial-use terms are per-model and per-provider**, same caveat as
  AICRON — Muapi aggregates other companies' models; check the specific
  model's terms before publishing generated output, don't assume Muapi's own
  MIT-adjacent marketing covers what the underlying model licenses.
- Generated media inherits the AI-disclosure duties in `viral-tiktok-content`
  and `viral-instagram-reels`.
- Default to the free path (OpenMontage) first, AICRON second when a human is
  available. Reach for this only when the job specifically needs to stay
  scriptable and paid generation is worth it — never as a first move.
