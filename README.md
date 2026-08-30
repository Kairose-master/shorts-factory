# shorts-factory

A video research, scripting and production workspace for Claude Code. Two
pipelines: **short-form** (research-led, 30-second artifacts) and **longform**
(a 10–20 minute video essay, in `episodes/`).

73 Agent Skills under `.claude/skills/` — 43 from five upstream repositories and
left byte-identical to upstream, plus 30 authored here. `CLAUDE.md` holds the
routing rules; this file covers install, credentials and verification.

## Quick start

```bash
cp .env.example .env          # then fill in only the keys you intend to use
python3 scripts/verify_skills.py
```

Claude Code discovers `.claude/skills/` automatically whenever it runs inside
this repo. To use the skills from anywhere:

```bash
./scripts/install_global.sh --dry-run   # preview
./scripts/install_global.sh             # symlink into ~/.claude/skills/
```

The script never replaces a real directory it did not create; a name clash is
reported and skipped, and `--prefix` installs as `shorts-factory--<name>` instead.

## What's installed

| Source | Count | Skills |
|---|---|---|
| [ScrapeCreators/social-media-research-skills](https://github.com/ScrapeCreators/social-media-research-skills) | 13 | `scrapecreators-api`, `outlier-post-finder`, `transcript-intelligence`, `comment-mining`, `competitor-social-research`, `trend-discovery`, `creator-profile-teardown`, `audience-research`, `social-listening-brief`, `product-demand-research`, `influencer-prospecting`, `content-repurposing`, `ad-library-teardown` |
| [scrollmark/social-skills](https://github.com/scrollmark/social-skills) | 16 | `hook-anatomy`, `trend-radar`, `content-autopsy`, `read-the-room`, `platform-fluency`, `voice-matching`, `repurpose-engine`, `agent-interview`, `video-formats`, `brand-kit`, `media-acquisition`, `audio-acquisition`, `subject-compositing`, `edit-handoff`, `video-production`, `studio-setup` |
| [vyralcontent/content-skills](https://github.com/vyralcontent/content-skills) | 7 | `viral-short-form`, `viral-hooks`, `viral-short-form-ideas`, `viral-youtube-shorts`, `viral-tiktok-content`, `viral-instagram-reels`, `viral-captions-and-ctas` |
| [bradautomates/head-of-content](https://github.com/bradautomates/head-of-content) | 6 | `youtube-research`, `tiktok-research`, `instagram-research`, `x-research`, `video-content-analyzer`, `content-planner` |
| [anthropics/skills](https://github.com/anthropics/skills) | 1 | `mcp-builder` |
| authored here — short-form + Office | 9 | `shorts-factory`, `handsel-growth-office`, `openmontage`, `voicebox`, `penpot`, `airtable`, `aicron`, `zapier-mcp`, `last30days` (vendored, MIT) |
| authored here — longform | 13 | `longform-factory`, `philosophy-script`, `theology-red-team`, `hook-tournament`, `storyboard-director`, `avatar-director`, `visual-metaphor`, `remotion-video`, `subtitle-qc`, `thumbnail-director`, `video-red-team`, `youtube-publisher`, `analytics-review` |

Provenance and content hashes live in `skills-lock.json`, written by the
official `skills` CLI. `npx skills update` upgrades in place — it tracks only
the 43 upstream skills and will not touch the ones authored here.

### Why only one skill from `anthropics/skills`

That repository is a general demonstration set, not a content-research set. Of
its 20 skills, five (`skill-creator`, `docx`, `pdf`, `pptx`, `xlsx`) are already
installed in this environment as managed skills — reinstalling would shadow
them, so they were left alone. The remaining fourteen (`algorithmic-art`,
`slack-gif-creator`, `canvas-design`, `internal-comms`, `theme-factory`,
`frontend-design`, `web-artifacts-builder`, `brand-guidelines`, `academy-guide`,
`doc-coauthoring`, `discernment-nudge`, `claude-api`, `webapp-testing`,
`template-skill`) do not serve short-form research and were skipped rather than
added as noise. `mcp-builder` was installed because it is the tool for turning a
new platform's API into a proper integration — see *Adding a platform* below.

## Credentials

Nothing here ships a key, and no skill should invent one.

**Where the secret should live depends on where you are running.** In a cloud
session, do not create a `.env` file at all — put the values in the
environment instead, so nothing sensitive is ever written to disk in the repo.

| Where you run | Where the key goes |
|---|---|
| Claude Code cloud session | **Environment variables in the environment's settings** — injected at container start. No file on disk, nothing to leak, and it dies with the container ([docs](https://code.claude.com/docs/en/claude-code-on-the-web)) |
| GitHub Actions (scheduled runs) | **Actions secrets**, referenced as `env:` in the workflow. These are *not* visible to an interactive session |
| Local machine | `.env` — already gitignored |

GitHub Secrets only decrypt inside a Workflow run. They do not reach an
interactive session, so they are the answer for automation and not for a
session you are typing into.

A `pre-commit` hook in `.githooks/` refuses any commit that stages an env file
or a line that looks like a filled-in key. Enable it once per clone:

```bash
git config core.hooksPath .githooks
```

Skills read keys from the environment either way, so `export SCRAPECREATORS_API_KEY=...`
and a `.env` file are interchangeable from their point of view.

Every variable is documented in `.env.example` with its provider and cost model.

### Getting the keys

| Key | Where | Free tier | Notes |
|---|---|---|---|
| `SCRAPECREATORS_API_KEY` | [app.scrapecreators.com](https://app.scrapecreators.com) | **100 credits, no card**, plus up to 7,000 more for feedback / starring their repo. Credits never expire | 1 credit ≈ 1 request; **cached results cost 0**. Paid: $47 / 25k credits, $497 / 500k |
| `APIFY_TOKEN` | [console.apify.com](https://console.apify.com) → Settings → Integrations | $5/month platform credit, no card | ⚠️ Free plan has **trial-only access to rented Actors** — the TikTok/Instagram/X scrapers are rented, so sustained use needs Starter ($29/mo) |
| `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Yes, generous | Google account only |
| `TUBELAB_API_KEY` | [tubelab.net](https://tubelab.net) → Settings → API | Check `/pricing` | Pricing page is JS-rendered and could not be verified here |

Verify a key works without spending anything:

```bash
python3 scripts/check_keys.py
```

It calls only free account/metadata endpoints — never a scrape. `--offline`
does a presence check with no network at all.

| Variable | Used by | Required? | Purpose |
|---|---|---|---|
| `SCRAPECREATORS_API_KEY` | all 13 ScrapeCreators skills | Required for live data | Public social data across TikTok, Instagram, YouTube, Reddit, X, LinkedIn, Facebook, Threads, Bluesky, Pinterest, Rumble and ad libraries |
| `APIFY_TOKEN` | `tiktok-research`, `instagram-research`, `x-research` | Required for those three | Apify scraper actors. The X/Twitter actor needs a paid Apify plan |
| `TUBELAB_API_KEY` | `youtube-research` | Required for YouTube outliers | TubeLab Outliers + Transcripts API |
| `GEMINI_API_KEY` | `video-content-analyzer`, and the video pass in `tiktok-research` / `instagram-research` | Required for video analysis | Watches a video and extracts hook, structure, CTA |
| `ANTHROPIC_API_KEY` | `mcp-builder` (`scripts/evaluation.py` only) | Optional | Scoring an MCP server you built. Not needed to write one |
| `VIDEO_STUDIO_BRANDS`, `VIDEO_STUDIO_STYLES` | `brand-kit` | Optional | Override where brand presets are stored |
| `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `FREESOUND_API_KEY`, `ELEVENLABS_API_KEY`, `REPLICATE_API_TOKEN` | `media-acquisition`, `audio-acquisition`, `studio-setup` | Optional | Stock and generated media. Not needed for research, ideation or scripting |

All four required providers are **metered per request**. Skills call them only
when you ask for a run.

## Dependencies

Installed in this environment:

- `ffmpeg` / `ffprobe` — audio measurement, loudness, keying
- Python: `apify-client`, `google-genai`, `python-dotenv`, `requests`, `pyyaml`

Not installed, and only needed for the video *production* track:

- `video-studio-engine` — powers `video-production`, `subject-compositing`,
  `edit-handoff`, most of `media-acquisition` and parts of `brand-kit`,
  `video-formats` and `audio-acquisition`. Install from the source repo, not PyPI:
  ```bash
  pip install 'video-studio-engine[standard] @ https://github.com/scrollmark/social-skills/archive/refs/heads/master.tar.gz'
  ```
- **Remotion** (Node) — the renderer behind `video-production`. It requires a
  paid Company Licence above three people and for hosted or automated
  rendering. That licence is between you and Remotion; nothing here grants it.

`python3 .claude/skills/studio-setup/scripts/doctor.py` reports what is
reachable right now, including which optional keys are unset.

## The orchestrator skills

Two entry points. Pick by the **shape of the output**, not the topic.

| Ask | Skill |
|---|---|
| Research a niche, a competitor, why a video went viral; shorts/Reels/TikTok ideas or scripts | `shorts-factory` |
| A 10–20 minute video essay | `longform-factory` |
| Anything Handsel promotion or content | `handsel-growth-office` (first, always) |

### `longform-factory`

Owns `episodes/`. Fifteen phases from script lock to analytics, with the
priority order that follows from its organising claim — that the competitive
core is not "an AI avatar talks" but *a philosophical structure converted into a
visual form*:

```
Script → Red Team → Storyboard → Remotion → Avatar
```

An episode is **25–35% avatar, 65–75% motion graphics**, and every generative
pass has an adversarial counterpart run separately: `philosophy-script` ↔
`theology-red-team`, `storyboard-director` ↔ `video-red-team`, `remotion-video`
↔ `subtitle-qc`.

`storyboard.json` is imported directly by the Remotion composition, so a
storyboard edit is a video edit. Phases needing a **CUDA GPU** (MuseTalk 1.5 /
EchoMimicV2 lip-sync) or a **TTS credential** are isolated: without them the
motion-graphics cut still renders, times and reviews correctly.

First episode: `episodes/ai-baptism` — *AI가 세례를 받으려 한다면?*, 11:50, 14
scenes, 157 beats, 26.1% avatar.

### `shorts-factory`

`.claude/skills/shorts-factory/` is the entry point for any short-form
research or scripting request. It owns the nine-stage pipeline, the ask-to-skill
routing table (`references/routing.md`), the cost gate on paid APIs, and the
run-mode rule: **API mode** when keys are set, **open mode** when they are not.
Open mode runs stages 1–2 from public web sources and stages 6–9 at full
strength — missing keys degrade a run, they do not block it.

Example output: `research/ai-tools-automation-2026-08-27/report.md`.

Do not route a longform ask through `shorts-factory` — its nine stages are built
around a 30-second artifact, and its routing table has no phase for a storyboard,
a claim map or a cut review.

## Verification

`scripts/verify_skills.py` checks every skill for a valid `SKILL.md`, parsable
frontmatter with `name` and `description`, a name matching its directory, every
relative `scripts/` `references/` `assets/` path resolving inside the folder, no
path escaping the folder, and that bundled Python parses. Current state: **73
skills, 0 errors**, and every bundled script runs `--help` offline.

`scripts/verify_storyboard.py <storyboard.json>` validates a longform storyboard:
required fields, contiguous non-overlapping scenes, **beats summing exactly to
their scene's duration**, beat durations inside the 3–14s band, and the avatar
share inside its declared target band.

`scripts/subtitle_qc.py` transcribes final narration with `faster-whisper` and
diffs it against the canonical script — guarded lines verbatim, no missing
sentences, timing drift inside threshold. It reports `SKIPPED` rather than
passing when narration does not exist yet; an unrun check is never a pass.

## China platform coverage — NOT SUPPORTED

No installed skill can search or collect from **抖音 (Douyin)**, **小红书
(Xiaohongshu / RED)** or **哔哩哔哩 (Bilibili)**. A grep for every name and
alias across all 43 skills returns nothing.

Do not read TikTok support as Douyin support. They are separate apps on
separate infrastructure with separate catalogues and a separate ranking system;
the ScrapeCreators TikTok endpoints do not reach Douyin. The same holds for
Instagram vs. Xiaohongshu and YouTube vs. Bilibili.

What *is* transferable: everything downstream of collection. `hook-anatomy`,
`trend-radar`, `content-autopsy`, `read-the-room`, `voice-matching`,
`viral-hooks` and the scripting skills analyse text and structure, not
platforms, so they work on Chinese short-form the moment something feeds them
data — with the caveat that their platform-specific numbers (retention curves,
CTA conventions) are calibrated on TikTok/Reels/Shorts.

### Adding a platform

Each skill is a self-contained folder, so a new platform is a new folder rather
than an edit to an existing one:

1. Add `douyin-research` / `xiaohongshu-research` / `bilibili-research`,
   modelled on `.claude/skills/scrapecreators-api/SKILL.md` — that skill is the
   reference shape for an API-backed data layer.
2. Register the credential in `.env.example`.
3. Add `.claude/context/<platform>-accounts.md` matching the existing shape.
4. Leave stages 6–9 of the pipeline alone; they are platform-agnostic. Add a
   `viral-douyin-content`-style skill only where the ranking system differs
   enough to change the writing — for Douyin it does.
5. Re-run `python3 scripts/verify_skills.py`.

Access reality per platform, worth checking before you build: Bilibili has an
official open API; Douyin requires the Douyin Open Platform or a third-party
data provider; Xiaohongshu publishes no public API, so it needs a commercial
provider. Use `skill-creator` to scaffold and `mcp-builder` if a platform is
better served as an MCP server than as curl inside a skill.

## Licences

Each skill keeps its upstream licence. ScrapeCreators and scrollmark are MIT;
`anthropics/skills` is Apache 2.0 for `mcp-builder`. See each source repository.
