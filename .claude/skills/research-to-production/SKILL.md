---
name: research-to-production
description: |
  Turn a finished research report into an actual video production run. Use when a
  shorts-factory research report, an outlier table, a hook analysis or a script
  draft exists and the next step is building the video — mapping measured findings
  onto a video-formats format, writing the storyboard, and handing off to
  video-production. Also use when asked whether this machine can actually render
  what the research recommends, or to plan a faceless/no-camera format from
  research evidence.

  Triggers: "make the video", "리서치 결과로 영상 만들어", "produce this script",
  "which format for this idea", "can we actually render this", "faceless format",
  "브릿지", "research to video"
---

# research-to-production

The connector between the research pipeline (`shorts-factory`, stages 1–9) and the
production pipeline (`video-production`, steps 0–9). Both existed; nothing joined
them. This skill is that join and nothing else — it does not render, source, or
re-research.

## Where this sits

```
shorts-factory  →  [ research-to-production ]  →  video-production
stages 1-9         format pick · storyboard        steps 0-9
report.md          · evidence carry-forward        render
```

**It writes one artifact**: a storyboard the `video-production` interview can take
as given, with every shot traceable to a line in the research.

## Rule 0: check the machine before promising a format

Run `studio-setup`'s doctor **first**, every time:

```bash
python3 .claude/skills/studio-setup/scripts/doctor.py
```

Recommending a format the machine cannot render wastes the user's whole run. Read
the output and say plainly which of the formats below are reachable **today**.

The engine (`video-studio`), `ffmpeg`, and local TTS are separate installs from
the skills. A skills tree that verifies clean does **not** mean a machine that can
render. These are different claims — never merge them.

## Step 1: carry the evidence forward, or drop the shot

Every scene in the storyboard cites the research line it came from. A shot with no
citation is a shot somebody invented during the handoff, and it is exactly where
research-grounded video quietly turns into generic video.

| Storyboard field | Comes from | If missing |
|---|---|---|
| hook line | stage 4 verbatim transcript | **stop** — do not write one from scratch |
| format choice | stage 6 hook analysis + measured visual | fall back to `explainer` and say so |
| scene beats | stage 9 script | the script step was skipped; go run it |
| on-screen numbers | stage 3 outlier table | leave the placeholder in, do not invent |
| audience language | stage 5 comment mining | write plainer, do not guess at slang |

**Placeholders survive the handoff.** If the research left `$[YOUR NUMBER]`, it
stays `$[YOUR NUMBER]` in the storyboard and the user fills it. Filling it for
them fabricates the one thing the research deliberately refused to fabricate.

## Step 2: pick the format from measured production, not from vibes

`video-formats` ships ten formats in `references/formats/`. Map by **how the
outlier was actually made**, which stage 4's visual analysis measured — not by
subject matter.

| Measured visual source | Format | Camera needed |
|---|---|---|
| still images + slow push | `explainer`, `timeline-explainer` | none |
| illustration + narration | `explainer` | none |
| archival / broadcast clips | `boil`, `titled-video` | none (rights required) |
| 2D animation / webtoon | `pip-story` | none |
| screen recording | `pointer-popups` | none |
| product tabletop + hands | `product-launch` | phone only |
| presenter to camera | `talking-head` | camera |

Only `talking-head` needs a face. **Faceless is the default, not the exception** —
seven of ten formats never need a camera.

When the visual analysis did not run (quota, cost, a skipped stage), say the
format choice is **inferred** and name what would confirm it. Do not present an
inferred format as a measured one.

## Step 3: write the storyboard

Follow the chosen format's grammar in `references/formats/<name>.md` exactly — that
file, not this one, defines the scene shapes. Add one column the formats do not
have:

```
| scene | layer | source | EVIDENCE |
|-------|-------|--------|----------|
| s1    | vo    | prompt:…| report.md §3, 50.68x hook, verbatim |
```

Source prefixes are `video-production`'s contract, not this skill's invention:
`prompt:` generate · `find:` licensed search · `url:` user link · `file:` user path.
Use them verbatim or `build_props` will not resolve the shot.

## Step 4: hand off

Say exactly this to the user, then stop:

> Storyboard ready at `<path>`. `video-production` takes it from step 3
> (sourcing). Blocked on: `<doctor output, or "nothing">`.

Do **not** start the render. `video-production` owns steps 0–9 including the cost
gate, the placeholder preview, and the frame check. Skipping into it from here
bypasses the preview that exists to catch layout errors before anyone spends money.

## Cost honesty

The research pipeline and the production pipeline bill separately. A user who
approved a research budget has **not** approved a render budget. Quote generation
cost fresh, before the first paid production call, even if they just approved
research spend an hour ago.

Cheapest complete path, and it is genuinely cheap: still images from a
public-domain archive + local TTS + burned-in captions. Zero API cost once the
engine and `ffmpeg` are installed. Reach for paid generation only when the format
actually needs motion that no archive can supply.

## What this skill will not do

- Re-run research. If the report is thin, go back to `shorts-factory`.
- Invent a hook. Stage 4 supplies it or the run stops.
- Render. That is `video-production`.
- Promise a format the doctor says is unreachable.
