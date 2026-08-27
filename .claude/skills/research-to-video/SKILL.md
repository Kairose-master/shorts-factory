---
name: research-to-video
description: Turn a finished research report into a rendered video file on this machine. Use when a report, outlier table, hook analysis or script exists and the next step is an actual MP4 — deciding whether the idea is buildable at all, which assets it needs and where they can legally come from, then running narration, render, mux and QC. Also use when asked whether a faceless format is producible here, or when a Korean-language short needs burned captions.
---

# research → video

The join between `shorts-factory` (research, stages 1–9) and a file on disk.
It ends at a **checked MP4**, not at a handoff.

```
shorts-factory  →  [ research-to-video ]  →  projects/<slug>/<slug>.mp4
report.md          tier · assets · script     video-assembly + motion-graphics
                   · evidence carried         + web-media-getter
```

## Rule 0 — route on the ASSET, not on the face

The obvious question is "does this need a camera". It is the wrong question.

Measured on the nine tracked Korean Shorts channels, 2026-08-27
(`research/kr-9channels-production-2026-08-27/report.md` §4):

- **8 of 9 never show the creator's face.**
- **0 of 9 could be rebuilt from code alone.** Every one leans on footage an
  agent cannot make: broadcast clips, archival video, licensed stock, specific
  photographs, custom illustration, or the creator's own hands on a table.

**Faceless is not assetless.** Sort by where the pixels come from:

| Tier | Assets | Cost | Buildable here | Looks like |
|---|---|---|---|---|
| **A** | code-drawn graphics + TTS | **$0** | ✅ today | data cards, receipts, rankings, kinetic type, process explainers |
| **B** | public-domain / CC archive + code | **$0** | ✅ today | stock-led explainers, historical, science |
| **C** | broadcast / film / news clips | rights work | ❌ decide quotation scope first | clip-commentary, celebrity, politics |
| **D** | custom illustration or original shooting | production budget | ❌ | webtoon animation, tabletop demo, presenter |

Say the tier out loud before writing a storyboard. Promising a C-tier idea on a
free pipeline is the single most expensive mistake available here, because the
whole script gets written before anyone notices.

**A C-tier idea is not dead — it is re-shot at A or B.** The strongest engine in
that dataset is a cost-breakdown format whose *video* is D-tier (the creator's
hands) and whose *structure* is A-tier. Its most-endorsed comment (67,000 likes)
praises the **rigour of the calculation**, not the footage. Take the structure,
rebuild the screen.

## Rule 1 — carry the evidence or drop the shot

Every scene cites the research line it came from. A scene with no citation is
one somebody invented during the handoff, and that is precisely where
research-grounded video turns back into generic video.

| Storyboard field | Comes from | If missing |
|---|---|---|
| hook shape | stage 4 verbatim transcripts | **stop** — do not invent one |
| format / scene grammar | stage 6 + the measured visual analysis | fall back to a plain card sequence and say so |
| on-screen numbers | stage 3 outlier table | leave the placeholder, do not fill it |
| audience language | stage 5 comment mining | write plainer, do not guess at slang |

**Placeholders survive the handoff.** If the research left `$[YOUR NUMBER]`, it
stays. Filling it fabricates the one thing the research deliberately refused to.

**Numbers a viewer could screenshot do not get animated counters.** A roll from
0 to 915 puts "784" on screen for four frames. Roll a headline number if the
roll is the reveal; fade a factual one in at its final value.

## Rule 2 — captions are the entry fee, not a garnish

**9 of 9 measured channels burn full captions.** No exceptions, across every
format, every subject, every publish date. A Korean short without burned
captions does not resemble anything in that niche.

`motion-graphics/scripts/captions.py` does this from the TTS word boundaries
already in `plan.json`:

```python
cards = captions.chunk(scene["words"], max_chars=18)     # once, outside the loop
font  = captions.fit(probe, cards, kf, COL - 40)         # sized to the LONGEST card
captions.draw(d, cards, t, font, y, L, R, highlight=ACCENT, stroke=7)
```

Size to the longest card, never the average — the overflow that ruins the read
is always on the one long line. Stroke, not a plate: a caption box hides the
picture and a plate-less white caption vanishes on light footage.

## Rule 3 — Korean runs on the same path as English

The earlier routing (`research-to-production`, if present) sends Korean to
Gemini TTS and then warns about lost word timings, a separate caption pass, and
a 12 dB level mismatch. **That detour is unnecessary.** Measured 2026-08-27:

| | |
|---|---|
| Korean voices in edge-tts | `ko-KR-InJoonNeural`, `ko-KR-SunHiNeural`, `ko-KR-HyunsuMultilingualNeural` |
| Word boundaries | **yes** — `boundary="WordBoundary"` returns per-word offsets in Korean |
| Speaking rate | **3.90 chars/s** at `+0%` (192 chars / 49.34s, InJoon, measured) |
| Level | same engine as English, so no cross-engine normalisation |

A 60s Korean short therefore holds about **230 characters** of narration — not
the ~330 the old note assumed from 5.5 chars/s. That is a 40% budget error, and
it is the difference between a script that fits and one that gets cut on the
render day. Check the character count at step 1, not after.

**Korean also needs a Korean font, and PIL will not tell you.** Ask DejaVu for
한글 and you get tofu, silently, through a render that exits 0. Use
`motion-graphics/scripts/fonts.py`: `fonts.korean(700)`. It prefers a real
Korean face, downloads Noto Sans KR (OFL) if the machine has none, and only
falls back to a pan-CJK font — which *covers* Hangul but was not *designed* for
it — with a warning you must repeat in the report.

## The run

```bash
S=.claude/skills/video-assembly/scripts
P=projects/<slug>

python3 .claude/skills/motion-graphics/scripts/selfcheck.py --out /tmp/mg   # 10s, do it first
python3 $S/narrate.py --lines $P/lines.json --out $P/vo                     # measure the read
python3 $S/plan.py --timing $P/vo/timing.json --lines $P/lines.json --out $P/plan.json
python3 $P/render.py                                                        # draw against plan.json
python3 $S/mux.py  --video $P/silent.mp4 --plan $P/plan.json --out $P/<slug>.mp4
python3 $S/qc.py   --video $P/<slug>.mp4  --plan $P/plan.json --sheet $P/contact-sheet.jpg
```

Narration is synthesised and **measured** before a frame is drawn; the
measurement is the scene clock. `video-assembly` owns that rule and the reasons
behind it.

**For B-tier assets**, `web-media-getter` fans out over Openverse, Wikimedia,
Internet Archive, Library of Congress and NASA with no key, and tags a licence
per result:

```bash
python3 .agents/skills/web-media-getter/webmedia.py "rocket launch" --type video --count 5
python3 .agents/skills/web-media-getter/webmedia.py "diamond crystal" --download --out $P/clips
```

Two things it will not do for you: relevance ranking is weak on Internet Archive
(a "rocket launch" query returns game speedruns), and a licence **tag** is not a
licence **check**. Open the item page for anything that ships.

## Anti-patterns

- **Writing the script before naming the tier.** The tier decides whether the
  script is buildable; discovering it afterwards wastes the script.
- **Calling a C-tier plan "free".** Clip-based commentary is not free, it is
  unresolved. Say "rights work required", never "$0".
- **Sizing captions to the average card.** The longest card is the one that
  breaks, and it breaks in the feed, not in the contact sheet.
- **Naming channels on screen because the data has them.** The finding is
  usually about the distribution. Naming a competitor — especially one whose
  subject matter is a brand risk — buys nothing and costs something.
- **Shipping on `qc.py` exit 0.** It proves the file is not broken. Open the
  contact sheet; two layout bugs in this repo's own runs got past a clean exit.
- **Reporting a render as free without saying what was spent upstream.**
  Research credits and render cost are separate budgets and both belong in the
  report.

## Worked examples

Two complete runs, both A-tier, both with their evidence recorded:

- `projects/the-bill/` — English, 44.6s, cost-breakdown argument from the
  AI-tools research (§7 idea 1).
- `projects/gijunseon/` — Korean, 55.7s, burned captions, baseline-vs-subscriber
  data from the nine-channel research (§1).

`references/tier-playbook.md` has the per-tier scene grammars and the asset
checklist.
