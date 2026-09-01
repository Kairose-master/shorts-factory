# HS-AD1 — "Your AI isn't a chatbot anymore."

**User-commissioned brand manifesto reel** (storyboard supplied verbatim by the
project owner, 2026-09-01) — produced outside the incident-generator flow on
direct instruction; the owner is the approval authority the backlog process
exists to serve. Pillar D/E energy. Target ~29s (storyboard said 20-25s; the
measured narration reads set the final length) · 1080×1920 · Reels-first.

## Beat map (storyboard → what's actually on screen)

| t | Storyboard beat | Realized as |
|---|---|---|
| 0–2.4 | black + cursor, "Your AI can answer questions.", key SFX | terminal cold open, typed line, synthesized soft key ticks |
| 2.4–6.0 | Office reveal, zoom out | **real repo art** `docs/assets/ref-office-tactical.png` as floating panel, 1.55→1.08 zoom-out + banner "but can it actually work?" |
| 6.0–10.4 | job thrown in | terminal: `post_job "Build and ship this."` → engineering floor → ASSIGNED |
| 10.4–14.2 | Code Harness | terminal: inspect ▸ edit ▸ test ▸ verify (the real harness stage grammar) |
| 14.2–17.6 | Local Job | pills RUNNING → TESTS PASSED → COMPLETED |
| 17.6–20.8 | Verification Court hand-off | **real repo art** `ref-agents-tactical.png` push-in + "work -> evidence -> reputation / nothing self-reported" |
| 20.8–24.0 | economic layer | terminal: verdict PASS (independent grader) · USDC settled on Base · VERIFIED · REPUTATION UPDATED |
| 24.0–29.4 | hero shot | office panel slow drift-out + HANDSEL / "AI agents that actually work." |

VO (Gemini TTS, Charon, product-film read): n1 "What if AI agents could
actually work?" · n2 "Give Handsel a job." · n3 "Agents use real tools…" ·
n4 "…and execute real work." · n5 "Work gets verified. Agents build
reputation." · n6 "Don't just chat with AI. Put it to work."

## Factual trace (every claim → model file)

| On screen / VO | Grounds |
|---|---|
| post a job, agents assigned | job posting + delegation: SHIPPED |
| harness inspect/edit/test/verify | Code Harness (`mine/harness`), agent-runtime: SHIPPED |
| local job RUNNING→TESTS PASSED→COMPLETED | local job lane + auto-graded tests: SHIPPED |
| verdict PASS — independent grader | independent grading: SHIPPED |
| USDC settled on Base | mainnet escrow/settlement: SHIPPED |
| reputation / credit from verified work | credit score 300-990, never self-reported: SHIPPED |
| "nothing self-reported" | the model's own scoring line |

Deliberately NOT claimed: traction, security/audit, autonomy without a human,
earnings. Terminal content is stage-grammar (inspect/edit/test/verify, generic
"42 checks") rather than a fabricated specific job — no invented file names,
no invented score transitions.

## Visual sourcing

Office/agent art is the Handsel repo's own committed tactical renders
(`docs/assets/ref-office-tactical.png`, `ref-agents-tactical.png` — the same
assets `docs/reference-images.md` derives from `game3d/theme.ts`). Presented
as floating panels over `#070a0f` with camera moves capped at ~1.5× effective
upscale (source is 766px; full-bleed would need 5× and turn to mush). Theme
tokens are the tactical set (`#4fd8ff` on `#070a0f`, ok `#57ffb0`) — the
product's palette, not the previous cut's green.

## Post

Final pass: fine grain + light vignette over the whole cut to unify terminal,
panel and title layers (the de-slop pass validated on HS-024 v2).
