# shorts-factory

A short-form video research and scripting workspace, and the home of the
**Handsel Short-Form Growth Office** (`office/`).

71 Agent Skills are installed under `.claude/skills/`:

- **60 skills tracked in `skills-lock.json`**, left **byte-identical to
  upstream** so `npx skills update` keeps working. This includes the official
  Remotion skills, which as of 2026-09-04 install into `.agents/skills/` and
  are symlinked into `.claude/skills/` — one skill per topic
  (`remotion-create`, `remotion-render`, `remotion-captions`, …) instead of the
  old single `remotion-best-practices` bundle with nested subfolders.
- **4 motion skills from `npx reborn-motion-skills`** (2026-09-04):
  `motion-graphics`, `cinematic-camera`, `terminal-inserts`,
  `article-highlights`. `motion-graphics` owns a hard delivery gate
  (`scripts/promptible-gate.mjs`): research → approved-reference preflight →
  BUILD AUTHORIZED → candidate evidence → **independent critic subagent** →
  DELIVERY AUTHORIZED. The builder may not grade its own work, and the gate
  rejects any category below 8/10 or an average below 8.5. Known upstream gap:
  `terminal-inserts/SKILL.md` references a bundled
  `examples/kickbacks-spinner-terminals.mp4` that the package does not ship, so
  `verify_skills.py` reports one error there until upstream fixes it.
  The gate verifies its bundled approved reference MP4s by SHA-256, and those
  MP4s are **gitignored** by this repo's `*.mp4` rule (same treatment as
  `vendor/OpenMontage`): a fresh clone must re-run `npx reborn-motion-skills`
  before `promptible-gate.mjs init` will pass. The contact sheets are
  committed, so the reference set is still readable from the repo alone.

- **8 local skills** authored here and deliberately *not* in the lock file:
  `handsel-growth-office`, `openmontage`, `voicebox`, `penpot`, `airtable`,
  `aicron`, `zapier-mcp` — plus `shorts-factory` itself. `npx skills update`
  will not touch them.
- **1 vendored upstream skill**, `last30days` (MIT,
  [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)),
  copied byte-identical but not in the lock file. **It needs Python 3.12+**,
  which this container does not ship — `LAST30DAYS_PYTHON` in
  `.claude/settings.json` points at a `uv`-managed 3.12. `verify_skills.py`
  reports its 3.12-only syntax as a warning naming that requirement, not an
  error.

Run `python3 scripts/verify_skills.py` after any change to the skills tree,
and `python3 scripts/verify_backlog.py` after any change to the Office backlog.

## Start here

**For any Handsel promotion or content request, invoke the
`handsel-growth-office` skill first** (`.claude/skills/handsel-growth-office/SKILL.md`).
It owns the Growth Office in `office/` — the mission, the memory, the approval
boundary, and the rule that nothing publishes without explicit human approval.

For a generic research or scripting request with no Handsel angle, invoke the
**`shorts-factory`** skill instead (`.claude/skills/shorts-factory/SKILL.md`). It owns the nine-stage
pipeline, the ask-to-skill routing table, the cost gate on paid APIs, and the
run-mode rule below. The sections here are the workspace conventions it assumes.

## Run mode

Check credentials before planning a run:

```bash
for k in SCRAPECREATORS_API_KEY APIFY_TOKEN TUBELAB_API_KEY GEMINI_API_KEY; do
  printf '%-26s %s\n' "$k" "$(printenv "$k" >/dev/null && echo SET || echo unset)"
done
```

- **API mode** — the relevant key is set. Every stage available.
- **Open mode** — keys missing. Stages 1–2 run from public web sources, stages
  6–9 run at full strength. Outliers become *reported* performance rather than
  measured baselines.

Missing keys are not a reason to stall. Name the variable, say what it would
have improved, and run open mode. State which mode produced each number.

## Ground rules

- **Never invent a credential.** If a skill needs a key that is not in `.env`,
  say which variable is missing and stop. Do not substitute a placeholder, and
  do not fall back to scraping a site by hand to work around a missing key.
- **Metered APIs cost money per call.** ScrapeCreators, Apify, TubeLab and
  Gemini all bill per request. Run them when the user asks for a run, not to
  explore. Say roughly how many calls a plan will make before making them.
- **Prose skills are free.** Everything from `vyralcontent` and the seven
  `scrollmark` social skills is pure analysis — no key, no network, no cost.
  Reach for those first when the question is "how should this be written",
  and reach for the data layer only when the question is "what is actually
  happening out there".
- `.claude/context/*.md` is user-owned configuration. Read it, don't rewrite it.

## The pipeline

Each stage names the skill that owns it. Stages 1–6 need live data; 7–9 do not.

| # | Stage | Skill | Needs |
|---|-------|-------|-------|
| 1 | Discover | `trend-discovery`, `competitor-social-research`, `creator-profile-teardown` | ScrapeCreators |
| 2 | Collect | `youtube-research`, `tiktok-research`, `instagram-research`, `x-research` | Apify / TubeLab |
| 3 | Outlier detection | `outlier-post-finder` (cross-platform), or the per-platform `analyze_posts.py` / `find_outliers.py` | either |
| 4 | Transcript | `transcript-intelligence` (fetches), `video-content-analyzer` (watches the video) | ScrapeCreators / Gemini |
| 5 | Comment mining | `comment-mining`, `audience-research`, `read-the-room` | ScrapeCreators (`read-the-room` is free) |
| 6 | Hook analysis | `hook-anatomy` (structural), `viral-hooks` (generative), `content-autopsy` (post-mortem) | none |
| 7 | Trend clustering | `trend-radar` | none |
| 8 | Content idea | `viral-short-form-ideas`, `content-planner`, `repurpose-engine`, `content-repurposing` | none / mixed |
| 9 | Script | `viral-short-form` + the platform skill (`viral-youtube-shorts`, `viral-tiktok-content`, `viral-instagram-reels`), then `viral-captions-and-ctas`, `voice-matching` | none |

`content-planner` orchestrates stages 2–3 across all four platforms at once and
writes into `content-plans/`. It is the most expensive single entry point —
it fans out to every configured account.

## Routing

Pick the **narrowest** skill that matches the ask.

- "what's blowing up in X niche" → `trend-discovery`
- "why did this video pop" → `content-autopsy`, then `hook-anatomy`
- "what does this creator do right" → `creator-profile-teardown`
- "beat this creator's baseline" → `outlier-post-finder` (baseline-relative, not raw views)
- "what are viewers saying" → `comment-mining` for extraction, `read-the-room` for subtext
- "is this trend worth riding" → `trend-radar`
- "write me hooks" → `viral-hooks`; "critique this hook" → `hook-anatomy`
- "write the script" → `viral-short-form` for shape, the platform skill for tuning
- "what are people actually saying about X this month" → `last30days`
  (Reddit · Hacker News · Polymarket keyless and free; X/TikTok/YouTube/
  Instagram need keys. Run it before generating a backlog — see lesson L-07.)
- Raw endpoint lookup → `scrapecreators-api` (the data layer the others call)

Two skills that look duplicated are kept on purpose:

- `hook-anatomy` (scrollmark) diagnoses an existing hook; `viral-hooks` (vyral)
  generates batches from named archetypes. Analysis vs. generation.
- `trend-radar` (scrollmark) judges whether a trend is worth joining and when;
  `trend-discovery` (ScrapeCreators) finds trends from live API data. Judgement
  vs. discovery — `trend-discovery` feeds `trend-radar`.
- `repurpose-engine` (scrollmark) is platform-adaptation strategy;
  `content-repurposing` (ScrapeCreators) turns a specific fetched video into
  concrete assets. Strategy vs. execution.
- `content-planner` (head-of-content) plans from **your tracked accounts**;
  `viral-short-form-ideas` ideates from **pillars and mining**, no API.

## Output layout

Platform research writes timestamped run folders at the repo root:

```
{platform}-research/{YYYY-MM-DD_HHMMSS}/
├── raw.json             # unmodified API response
├── outliers.json        # baseline-relative scoring
├── video-analysis.json  # Gemini hook/structure extraction
└── report.md            # the readable artifact
```

Run folders are gitignored — they are large and reproducible. Commit the
`report.md` of a run you want to keep by moving it out of the run folder.

## Extending: adding a platform

The skills tree is flat and each skill is self-contained, so a new platform is
a new folder, not a change to any existing skill. To add 抖音 / 小红书 / 哔哩哔哩
(none of which any installed skill covers today — see README):

1. Add a data-layer skill (`douyin-research`, `xiaohongshu-research`,
   `bilibili-research`) modelled on `.claude/skills/scrapecreators-api/SKILL.md`.
   Bilibili has an official open API; Douyin needs the Open Platform or a
   third-party provider; Xiaohongshu has no public API at all.
2. Register its credential in `.env.example` next to the others.
3. Add a context file under `.claude/context/` for the accounts to track,
   matching the existing `*-accounts.md` shape.
4. Leave stages 6–9 alone. `hook-anatomy`, `trend-radar`, `viral-hooks` and the
   scripting skills are platform-agnostic and will consume the new data as-is.
   Only add a `viral-douyin-content`-style skill if the platform's *algorithm*
   differs enough to change the writing — for Douyin it does.
5. Re-run `python3 scripts/verify_skills.py`.

Use the `skill-creator` skill to scaffold, and `mcp-builder` if the platform is
better served as an MCP server than as curl-in-a-skill. Add the new skill to the
routing table in `.claude/skills/shorts-factory/references/routing.md` so it is
reachable, and delete its row from the "Not routable" list there.

## The Growth Office

`office/` is the Handsel Short-Form Growth Office — a standing content operation,
not a run folder. It is **committed** because it is the Office's memory and must
survive the container.

```
office/
├── CHARTER.md                 mission · roles · autonomy boundary · pillars
├── research/handsel-model.md  the verified product model + DO NOT CLAIM ledger
├── memory/                    backlog · hooks · published · rejected
│                              experiments · analytics · lessons
├── sop/                       production-pipeline · quality-control · analytics-loop
└── production/<idea-id>/      plan · script · hooks · qc  (renders gitignored)
```

Two rules override everything else in this file when the Office is running:

1. **Nothing publishes without explicit human approval.** Every time.
2. **Never invent Handsel functionality.** Every factual claim traces to a line in
   `office/research/handsel-model.md`, or it is cut.

## The render layer

`vendor/OpenMontage` (AGPL-3.0, gitignored) is the only capability here that
produces an actual `.mp4`; every other skill produces text. Install or repair it
with `bash .claude/skills/openmontage/scripts/install.sh`. It is outside the
skills tree on purpose — copyleft source does not get merged into this repo.

The free render path needs no key: Piper/eSpeak narration, Remotion or
HyperFrames composition, Archive.org/NASA/Wikimedia footage, FFmpeg post. Use it
for every experiment. Paid generation is a Gate-gated exception, not a default.

## Reporting standard

Every report opens with a **Method** block — mode, sources, sample size, date,
and what was not checked — and follows the hard rules in the `shorts-factory`
skill: cite or drop it, raw views are not performance, quote hooks verbatim,
small samples get small claims, never promise virality.
