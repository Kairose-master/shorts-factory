# shorts-factory

A short-form video research and scripting workspace. 43 Agent Skills are installed
under `.claude/skills/`, pulled from five upstream repositories and left
**byte-identical to upstream** so `npx skills update` keeps working.

Run `python3 scripts/verify_skills.py` after any change to the skills tree.

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
better served as an MCP server than as curl-in-a-skill.
