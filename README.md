# shorts-factory

A short-form video research and scripting workspace for Claude Code.

43 Agent Skills from five upstream repositories, installed under
`.claude/skills/` and left byte-identical to upstream. `CLAUDE.md` holds the
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

Provenance and content hashes live in `skills-lock.json`, written by the
official `skills` CLI. `npx skills update` upgrades in place.

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

Nothing here ships a key, and no skill should invent one. Copy `.env.example`
to `.env` and fill in what you need — every variable is documented there with
its provider and cost model.

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

## Verification

`scripts/verify_skills.py` checks every skill for a valid `SKILL.md`, parsable
frontmatter with `name` and `description`, a name matching its directory, every
relative `scripts/` `references/` `assets/` path resolving inside the folder, no
path escaping the folder, and that bundled Python parses. Current state: **43
skills, 0 errors**, and every bundled script runs `--help` offline.

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
