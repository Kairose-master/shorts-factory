# 「The Bill」 — production record

A 44.6s vertical motion-graphics Short. Zero paid API calls. The video's subject
is the cost that AI-tool videos do not disclose, and its own bill is the payoff
card — which is only usable as a hook because it is checkable.

| | |
|---|---|
| **Built from** | `research/ai-tools-automation-2026-08-27-api/report.md` (API-mode run, posted to Slack #유튜브-리서치 2026-08-27) |
| **Idea** | §7 idea 1 — *"The real monthly bill for a 'one-prompt' AI video"*, called "the strongest opportunity in this dataset" |
| **Skills** | `motion-graphics` (frames), `video-assembly` (narration → clock → mux → gate) |
| **Format** | Kinetic-type / data card sequence, no footage, no subject |
| **Duration** | 44.63s — the 30–60s Shorts band (`viral-youtube-shorts` target ≥50% APV) |
| **Voice** | edge-tts `en-US-AndrewNeural`, `+0%` except s4 `-4%` and s6 `-8%` |
| **Spend** | **$0.00.** No generation credits, no stock licence, no key. ~35s wall clock per render |

## Why this idea and not the other nine

§4b of the research counts **nine separate cost complaints across five videos**,
on both platforms, and §3 counts **0 of 16 top-performing hooks that mention
price**. That is the largest measured gap between what the audience asks for and
what the niche supplies, in a dataset where every other idea competes with
existing supply.

The report's own Script A left the cost as `$[YOUR NUMBER]`, on the grounds that
inventing a figure would reproduce the dishonesty §4c documents. This video
resolves that differently: it does not estimate anyone else's bill, it publishes
its own, and its own is verifiable because the pipeline that made it is in this
repository.

## Scenes — measured, not storyboarded

Durations come from `vo/timing.json`; every reveal is anchored to a TTS word
boundary carried in `plan.json`. Nothing here was estimated.

| # | In → out | Narration | On screen | Evidence |
|---|---|---|---|---|
| s1 | 0.25 → 8.18 | "Python and ffmpeg drew every frame of this video. Zero credits. That number is the part nobody shows you." | tool telemetry running from frame 0; **ZERO CREDITS** pops on the word "Zero" (4.13s) | §3 shape: flat declarative, named tool in sentence one, hard number, no question. §6.3: the tool visibly *working*, not a brand mark |
| s2 | 8.18 → 15.14 | "Sixteen top AI tool videos, ranked against their own baselines. Not one mentions cost." | 16 tiles build, then dim; **0 / 16 — mention what it costs** | §3 hook table (16 verbatim openings); §4b "Zero of the 16 hooks mention price" |
| s3 | 15.14 → 20.78 | "Their comment sections do. Quote: they always forget to mention the cost of credits." | the comment, verbatim, in a quote card | §4b, quoted exactly |
| s4 | 20.78 → 29.97 | "The top video credits a model for the motion. A commenter says it just called a paid generator. Like praising McDonald's for discovering potatoes." | three-chip chain: the video → the model → **a paid generator** | §4d, the McDonald's/potatoes reply; §1 the 20.59× top performer |
| s5 | 29.97 → 38.69 | "So, this video's bill. Voice, free. Frames, a script. Footage, none. Credits, zero." | itemised receipt builds per word; **TOTAL $0.00** | this repository |
| s6 | 38.69 → 44.02 | "Ask the next person selling you a one-prompt workflow what their number was." | instruction close, accent rule sweeps through the tail | §5 identity/instruction close; `viral-captions-and-ctas`: no generic follow CTA |

**Where the shape deviates from the measured pattern, on purpose:** 11 of 16
measured hooks name a *product*. This one names two tools (Python, ffmpeg) that
are not the subject — the subject is the absence of a bill. It keeps the
declarative form and the hard number, which are the two properties present in
15/16 and 6/16 respectively.

## Claims audit

Everything on screen, and whether it is defensible:

- **"20.59× — the strongest hook in the set"** — §1, TubeLab `averageViewsRatio`.
- **"16 outlier openings · Shorts + TikTok · 2026-08-27"** — §3. The TikTok four
  are a *plays ÷ followers* proxy, not the same measure as the YouTube twelve
  (§2 says so explicitly), which is why the tiles are **uniform**: charting them
  at proportional heights would have manufactured a comparison the data does not
  support.
- **The two quoted comments** — verbatim from §4b and §4d, attributed on screen.
- **"a paid generator / billed per generation"** — carried as the commenter's
  claim in the narration, not asserted as fact.
- **"$300 per 10 minutes" is NOT in this video.** §4b flags it as a commenter's
  unverified assertion. It would have been the punchiest number available and it
  is the one number that could not be stood behind.
- **"~35 s of render time"** — wall clock of this exact script on this machine:
  36.4s, 35.0s, 35.0s across three renders. The tilde is doing real work.

## QC

`video-assembly/scripts/qc.py`, 9 checks, 0 failures:

```
[ok  ] plan         6 scenes, 44.62s, no overlap
[ok  ] container    44.63s 1080x1920 30.0fps
[ok  ] duration     44.63s vs plan 44.62s (+0.01s)
[ok  ] resolution   1080x1920      [ok  ] fps  30.0
[ok  ] loudness     -15.2 LUFS vs target -14.0 (-1.2)
[ok  ] black tail   peak luma 255 in the last 0.45s
[ok  ] frozen end   moving
```

Audio placement verified separately by per-scene RMS: silence in the 0.25s lead
and the 0.6s tail, speech energy at all six scene starts.

**Loudness lands 1.2 LUFS under target** even after the analysis pass, because
the file is roughly 12% silence and `linear=true` backs off against the -1.5
dBTP ceiling. Inside tolerance and on the safe side of clipping; the platforms
normalise to about -14 on ingest regardless.

**What QC cannot see and a person checked:** the contact sheet
(`contact-sheet.jpg`). Two bugs it caught that the exit code did not — the s2
heading overflowing the safe area on one line, and `0 / 16` colliding with the
credits chip.

## Rebuild

```bash
S=.claude/skills/video-assembly/scripts
python3 $S/narrate.py --lines projects/the-bill/lines.json --out projects/the-bill/vo
python3 $S/plan.py --timing projects/the-bill/vo/timing.json --lines projects/the-bill/lines.json \
    --out projects/the-bill/plan.json
python3 projects/the-bill/render.py --out projects/the-bill/silent.mp4 --cpu-seconds 35
python3 $S/mux.py --video projects/the-bill/silent.mp4 --plan projects/the-bill/plan.json \
    --out projects/the-bill/the-bill.mp4
python3 $S/qc.py --video projects/the-bill/the-bill.mp4 --plan projects/the-bill/plan.json \
    --sheet projects/the-bill/contact-sheet.jpg
```

`silent.mp4` is gitignored — it rebuilds in 35 seconds. The narration wavs and
the finished mp4 are committed, because a TTS endpoint is not guaranteed to
return identical audio next month and the file is the record of what shipped.

## Publishing notes

**Title** — What this video cost
**Caption** — 16 top AI-tool hooks. Zero of them mention price. Here's this one's bill, itemised. What was your last month?
**Pinned comment** — the full pipeline: edge-tts for voice, Python + PIL for frames, ffmpeg to encode. Repo link. Invite people to post their real number.

**Before publishing commercially, change the voice.** edge-tts drives the
endpoint behind Edge's read-aloud feature: free, keyless, and licensed for that
feature rather than for your channel. Swapping it changes `lines.json` and
nothing else in the pipeline.
