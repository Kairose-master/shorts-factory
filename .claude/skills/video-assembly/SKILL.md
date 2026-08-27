---
name: video-assembly
description: Use to actually build a short-form video file on this machine — synthesising narration, deriving scene timing from it, rendering, muxing, normalising loudness and gating the result — or when a render finished and you need to know whether it is publishable. Runs end to end with no paid API and no editor.
---

# Video Assembly

**The narration is the clock.** Write the lines, synthesise them, measure them,
and only then decide how long a scene is. Every other order produces a video
whose words and pictures disagree, and you find out at the render.

This skill owns everything that is not drawing. `motion-graphics` draws.

## The order, and why it is that order

| # | Step | Command | Produces |
|---|---|---|---|
| 1 | Write the lines | — | `lines.json` |
| 2 | Synthesise and **measure** | `scripts/narrate.py` | `vo/*.wav`, `vo/timing.json` |
| 3 | Turn measurements into the plan | `scripts/plan.py` | `plan.json` |
| 4 | Draw against `plan.json` | project `render.py` + `motion-graphics` | `silent.mp4` |
| 5 | Place audio, normalise, mux | `scripts/mux.py` | `final.mp4` |
| 6 | Gate it | `scripts/qc.py --sheet …` | verdict + contact sheet |

```bash
S=.claude/skills/video-assembly/scripts
python3 $S/narrate.py --lines p/lines.json --out p/vo
python3 $S/plan.py    --timing p/vo/timing.json --lines p/lines.json --out p/plan.json
python3 p/render.py                                  # reads plan.json, writes p/silent.mp4
python3 $S/mux.py     --video p/silent.mp4 --plan p/plan.json --out p/final.mp4
python3 $S/qc.py      --video p/final.mp4  --plan p/plan.json --sheet p/sheet.jpg
```

Steps 2 and 3 are cheap and steps 4–6 are not. A line that runs 29% over its
storyboarded slot is a rewrite at step 2 and a re-render at step 4.

## Requires

`pip install edge-tts pillow numpy imageio-ffmpeg`. No key, no account, no
system ffmpeg — `imageio-ffmpeg` brings its own binary and every script falls
back to it.

**Behind an egress proxy**, `narrate.py` forwards `HTTPS_PROXY` into edge-tts,
which otherwise connects direct and fails TLS verification. If TTS still fails
on certificates, the CA bundle has to reach `certifi`, not just the environment.

> **The voice is free, and that is a licensing fact, not just a price.**
> edge-tts drives the endpoint behind Edge's read-aloud feature. It costs
> nothing and needs no key, which makes it right for drafts, timing passes and
> internal cuts. Before publishing commercially, move to a voice you have a
> licence for — the pipeline does not change, only `lines.json`'s `voice` field
> and the synthesiser behind `narrate.py`. Say which voice shipped.

## plan.json is the contract

`plan.py` writes it, `render.py` reads it, `mux.py` places audio by it and
`qc.py` checks the finished file against it. One file, four consumers, so a
timing change cannot be applied in three places and missed in the fourth.

```json
{"fps": 30, "width": 1080, "height": 1920, "duration": 41.2,
 "scenes": [{"id": "s1", "start": 0.25, "dur": 5.35, "vo": "p/vo/s1.wav",
             "vo_seconds": 5.17, "text": "..."}]}
```

`dur` is always ≥ `vo_seconds`; the difference is the beat after the line. Buy a
scene more room with `"extra"` in `lines.json`, and cut hard into the next line
with `"gap": 0`. Never by editing `plan.json` by hand — it is regenerated.

## Hard rules

- **Never re-time by trimming narration.** If the hook needs 5.2s and the slot
  is 4.0s, the slot is wrong. Cutting the hook to fit removes the line that was
  doing the filtering.
- **Take the time back from the middle.** Scenes that came in under their
  storyboard are where an over-running hook is paid for.
- **-14 LUFS, once, at mux.** All three platforms normalise there. Normalising
  twice pumps; not normalising ships something audibly quieter than the video
  before it in the feed, which is a retention problem before it is an audio one.
- **Audio is placed at `start`, never concatenated.** Concatenation lets picture
  and voice drift apart the moment a scene duration changes.
- **`qc.py` exit 0 is a floor, not a verdict.** It proves the file is not
  broken. Pass `--sheet` and open the sheet; a render can be technically perfect
  and unreadable.
- **Say what the run cost.** This pipeline's answer is usually "nothing, plus
  CPU" — state it either way, with the same specificity you would want from
  someone else's video.

The failure modes worth knowing before the first render — the drift, the tail,
the loudness trap, the mono-wav requirement — are in
`references/assembly-rules.md`.

## Where this sits

`video-formats` picks the scene grammar and `motion-graphics` draws the frames;
this skill sequences them and gates the output. Upstream `video-production`
covers the same territory for a paid Remotion engine with sourced footage and a
preview editor — reach for that when the video needs stock, a subject or a human
editor downstream, and this one when it has to exist tonight for nothing.

## Anti-patterns

- **Storyboarding durations, then making the voice fit.** Backwards. The read
  is a measurement, not a preference.
- **Rendering before hearing the wavs.** A mispronounced product name is a
  three-second fix at step 2 and a full re-render at step 5.
- **`-shortest` hiding a mistake.** If the audio bed is longer than the picture,
  ffmpeg silently truncates and QC reports a duration mismatch, not a cause.
  Check `plan.json` totals first.
- **Shipping without stating the voice and the tooling.** Whoever picks this up
  next has to reproduce it.
