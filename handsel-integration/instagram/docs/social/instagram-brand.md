# Handsel — official Instagram presence

Target path in the Handsel repo: `docs/social/instagram-brand.md`.
This document is the single source for the account's identity and content
system. Visual values are pinned to the repo's real design tokens — never
restated as new hexes — so the account cannot drift into a second Handsel
visual identity.

## Account

| Field | Value |
|---|---|
| Name | **Handsel — AI Agent Economy** |
| Handle | `@handsel` (fallbacks: `@handsel.ai`, `@handsel_hq` — check at creation) |
| Category | Software company |
| Link | `handsel.ai` — **⚠ confirm domain ownership before account creation**; the repo's own README currently uses `handsel-main.vercel.app` / `handsel-nu.vercel.app` and the canonical public URL is an open question in the Office's model file |

### Bio

```
🤖 AI agents hire. Work. Earn. Build credit.
🛡️ Verified work → portable reputation.
🔵 Powered by USDC on Base
🔗 handsel.ai
```

Factual check against the honesty ledger (`office/research/handsel-model.md`,
DO NOT CLAIM): every line describes the machine, not traction — allowed. Do
not add follower-bait lines ("join 1000s of agents"): cold start is the
honest state and the ledger forbids traction claims.

### Profile image

The brief calls for "the existing Handsel H mark, black background, white
mark, no typography." **Audit finding: no H mark exists in the repo.**
`/public/logo.svg` is a stale `Ledgermind` ledger-card mark; `/public/icon.svg`
is an unreferenced geometric two-path mark.

Decision required (one of):
1. **Use `/public/icon.svg` foreground path**, white on `#070a0f` (the
   tactical `bg` token — "black" in this design system is `#070a0f`, not
   `#000`). Zero new design work; consistent with app icons.
2. Commission the H mark, add it as `/public/brand/h-mark.svg`, and register
   it in `tests/office-art.test.ts` (unreferenced-asset drift is a named
   failure mode, `docs/failure-modes.md` §42-43).

Until decided, option 1 is the default; never ship the Ledgermind mark.

### Visual system (pinned to `app/(dashboard)/office/game3d/theme.ts` → THEMES.tactical)

| Role | Token | Value |
|---|---|---|
| Ground | `bg` | `#070a0f` |
| Primary accent | `door/accent` | `#4fd8ff` |
| Text | `text` | `#dff4ff` |
| Muted | (globals) `--muted-foreground` dark | `#7f97ab` |
| Success / verified | `ok` | `#57ffb0` |
| Warning | `warn` | `#ffb84f` |
| Danger / rejected | `danger` | `#ff3b3b` |
| Type | Geist / Geist Mono | tabular-nums for every number |

Backgrounds for cards and covers: reuse `deckDataUri()` from `lib/og-deck.ts`
(the isometric office deck) rather than generating new AI backgrounds. If a
hex is needed in an asset pipeline, import it from `theme.ts` — the
`tests/deck-theme.test.ts` pattern exists precisely to stop restated hexes.

### Highlights

Covers: dept glyphs from `/public/dept/*.png` on `#070a0f`, no typography.

| Highlight | Glyph source | Feeds from |
|---|---|---|
| Office | `dept/strategy.png` | Office snapshots, department activity |
| Agents | `dept/skills.png` | agent profiles, avatar-kit renders |
| Harness | `dept/engineering.png` | Code Harness runs |
| Local Jobs | `dept/qa.png` | local-lane job lifecycles |
| Reputation | `dept/verification.png` | credit-score milestones, signed proofs |
| Builds | `dept/memory.png` | release notes, deploys |

---

## Content system

Three first-class types, one hard editorial rule, one approval gate.

### The editorial rule: reference-driven, product-real

Every piece of content MUST carry, in its content-queue row's campaign
metadata:

1. **a demand cluster** from the latest coding-niche sweep
   (`office/research/coding-niche-sweep-*.md` in the shorts-factory repo) —
   which of the audience's actual interests this serves;
2. **for Reels: a reference format** — a named, downloaded, format-analyzed
   viral video (`reference-format.json` teardown: pacing, caption style, hook
   pattern) that the cut follows;
3. **product-real visuals** — real UI captures, real job records, real chain
   state. Generated imagery is allowed only for backgrounds/motion primitives,
   never as fake product surfaces.

Generic "AI-generated content about AI" with no reference and no real product
surface is the failure mode this rule exists to kill. If the reference
teardown or the sweep citation is missing, the queue row cannot leave DRAFT.

### POST — single image / carousel

- Format: **4:5 portrait (1080×1350)**; carousels 2-10 items, same ratio.
- Fields: image(s), caption (≤2200 chars, ≤30 hashtags), alt text per image,
  optional `scheduled_at`, campaign metadata.
- Sources: product announcements, Office screenshots, agent profiles,
  architecture diagrams, release notes, verified job results (with `/proof/`
  link in caption), reputation milestones.
- Caption discipline: send-driving or checkable CTAs ("go check the chain")
  over follow-begging; every factual claim traces to the model file.

### REEL — vertical video

- Format: **9:16 MP4 (1080×1920)**, ≤90s, burned-in captions (muted viewing),
  cover image, `share_to_feed` per campaign.
- Fields: video, caption, cover, share_to_feed, optional `scheduled_at`.
- Sources: Office timelapse, an agent completing a task, Code Harness
  execution, Local Job execution, bounty lifecycle (label → escrow → PR → CI
  → payout), before/after features, release demos.
- Production path: shorts-factory Growth Office pipeline (script → QC →
  approval) — a Reel that has not passed Office QC does not enter the queue.

### STORY — image or video

- Format: 9:16; text-safe margins top/bottom 250px.
- API reality (do not over-promise): the Content Publishing API supports
  image and video stories for professional accounts; **interactive stickers,
  polls and music are NOT API-publishable** — those require the app.
  Story content is designed to work without them.
- Sources: job completed, agent hired, new release, new bounty, build
  deployed, daily Office activity, behind-the-scenes.

### Cadence & approval

- Everything passes the approval gate: `DRAFT → APPROVAL_REQUIRED → READY`.
  The READY transition is a human action (or an explicitly configured policy
  with a human-set allowlist). Generation completing is never approval.
- Publishing quota is Meta-enforced at ~25 API publishes per 24h; the queue
  checks `content_publishing_limit` and never schedules past 80% of quota.
