---
name: longform-factory
description: Orchestrate a 10–20 minute Korean longform YouTube essay end to end — lock a script, red-team its claims, tournament the cold open, break it into a machine-readable storyboard, budget the avatar against motion graphics, render it in Remotion, QC the subtitles and the cut, and package it for publish behind a human gate. Use when the ask is a longform video essay rather than a short, when a philosophical or theological topic needs to become a watchable episode, or to decide which of the twelve longform skills to run for a given ask. The companion to shorts-factory, which owns short-form.
---

# longform-factory

`shorts-factory` owns short-form research and scripting. This owns the other
shape: one **10–20 minute essay** where the argument, not the clip, is the unit.

The competitive claim of this pipeline is deliberately **not** "an AI avatar
talks." It is *a philosophical structure converted into a visual form*. Priority
order follows from that, and it is the opposite of the order tools get installed
in:

```
Script → Red Team → Storyboard → Remotion → Avatar
```

MuseTalk moves a mouth. Remotion makes the video. **Deciding which question to
show, in which order, is a separate capability from both** — and it is the only
one a competitor cannot install.

## The avatar ratio

An episode is **25–35% avatar, 65–75% motion graphics**. Not a style preference:

- A held synthetic face is the single strongest "this was generated" signal a
  viewer gets. Reducing its share reduces the AI smell more than improving the
  face would.
- Abstract subjects — duplication, identity, time, particularity — have no
  natural footage. Graphics are not a substitute for footage here; they are the
  only way to *show* the argument at all.
- Never hold a static talking avatar longer than **12 seconds** unless the scene
  is carrying emotional weight that needs the hold (see `avatar-director`).
- Change visual state every **4–8 seconds**.

`avatar-director` enforces the budget; `video-red-team` fails the cut if it drifts.

## Writer and Reviewer are never the same pass

Every generative skill here has an adversarial counterpart, and they must run as
separate passes with separate context:

| Writer | Reviewer |
|---|---|
| `philosophy-script` | `theology-red-team` |
| `storyboard-director` · `visual-metaphor` | `video-red-team` |
| `remotion-video` (assembly) | `subtitle-qc` |
| `thumbnail-director` | `video-red-team` (thumbnail/thesis match) |

The writer is the worst judge of whether the thing should ship. If one pass both
writes and approves, the review did not happen.

## The twelve phases

| # | Phase | Skill | Gate |
|---|---|---|---|
| 1 | Script lock | `philosophy-script` | — |
| 2 | Claim separation + red team | `theology-red-team` | **THEOLOGY_PASS** |
| 3 | Cold open tournament | `hook-tournament` | — |
| 4 | Storyboard | `storyboard-director` | beats must sum to scene duration |
| 5 | Avatar budget | `avatar-director` | share inside 25–35% |
| 6 | Visual metaphors | `visual-metaphor` | — |
| 7 | Assets | `media-acquisition`, `asset-hunter` | licence recorded |
| 8 | Narration | `voicebox`, `references/narration.md` | distinct voice per speaker; every line fits its beat |
| 9 | Lip-sync | `avatar-director` → MuseTalk / EchoMimicV2 | **needs CUDA** |
| 10 | Assembly | `remotion-video` | typecheck + still review |
| 11 | Subtitles + QC | `subtitle-qc` | guarded lines verbatim |
| 12 | Cut review | `video-red-team` | **≥85/100** |
| 13 | Thumbnail | `thumbnail-director` | readable without the title |
| 14 | Publish | `youtube-publisher` | **human approval, every time** |
| 15 | Learn | `analytics-review` | — |

Phases 1–6 and 10–13 need no GPU and no paid key. Run them first, always. A
missing key is a reason to name the variable and continue, never to stall.

## Reality check before planning a run

```bash
node -v; python3 -V
command -v ffmpeg || ls /opt/pw-browsers/ffmpeg-*/ 2>/dev/null
command -v nvidia-smi >/dev/null && nvidia-smi -L || echo "NO GPU — lip-sync unavailable"
for k in GEMINI_API_KEY ELEVENLABS_API_KEY DASHSCOPE_API_KEY YOUTUBE_API_KEY; do
  printf '%-24s %s\n' "$k" "$(printenv "$k" >/dev/null && echo SET || echo unset)"
done
```

State the result **before** planning, in one line. The two facts that most often
change a plan: whether there is a CUDA GPU (phase 9), and whether a TTS
credential exists (phase 8). Neither blocks phases 1–6 or 10–13.

## Output layout

```
episodes/<episode-id>/
├── script/      canonical.md · claim-map.json · theology-redteam.md
├── storyboard/  storyboard.json          ← the machine-readable driver
├── prompts/     image + narration prompts
├── audio/       manifest.json  (WAVs gitignored)
├── avatar/      manifest + clips (gitignored)
├── remotion/    the composition — src/, public/
├── subtitles/   final.srt · qc-report.md
├── thumbnail/   concepts + chosen still
├── qa/          rubric + scored review
└── export/      final.mp4 · metadata.json   (mp4 gitignored)
```

`storyboard.json` is the contract between phases 4 and 10. Beat times are
**absolute episode seconds**; every scene's beats must sum exactly to that
scene's duration. `remotion-video` reads it directly, so a storyboard edit is a
video edit — there is no second place to change a timing.

## Reference

- `references/pipeline.md` — what each phase consumes and emits, and the exact
  failure mode each gate exists to catch.
- `references/narration.md` — TTS engine choice, the Gemini free-tier trap, and
  the fitting loop that reconciles a measured read with an authored beat grid.
- `references/reuse.md` — running the stack on the next episode.

## The reuse claim

This stack is built for one episode and reused for the series. `references/reuse.md`
walks the next four: *AI가 죄를 지을 수 있을까* · *AI가 기도하면 하나님은 들으실까* ·
*기억을 복제하면 과거도 복제될까* · *AI에게 용서를 구할 수 있을까*. Each reuses the
storyboard schema, the Remotion primitives, the red-team blocking conditions and
the QA rubric unchanged. What changes per episode is the script and the scene
components — roughly a day of work against a week for the first.
