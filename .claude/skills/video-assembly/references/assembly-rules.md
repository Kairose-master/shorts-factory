# Assembly rules

The failure modes this pipeline actually hits, and what each one looks like
before you know what it is.

## Timing

**Symptom: the picture is right but the words land late.** Almost always a
scene whose measured narration exceeded its storyboarded slot, absorbed by
pushing everything after it. `plan.py` cannot see this — it derives starts from
measurements, so the plan is correct and the *storyboard* was wrong. Compare
`vo/timing.json` against the storyboard before blaming the renderer.

**Symptom: the hook feels rushed.** Check `wpm` in `timing.json`. Synthetic
voices run 155–180 wpm at `+0%`; a hook above 180 is a rewrite, not a rate
change. Slowing the whole line with `rate` flattens the delivery — cut words
instead.

**The 29% rule.** In practice the opening line overruns its storyboard slot far
more than any other, because hooks get written to a word count and read to a
rhythm. Budget the hook last, from its measurement.

## Audio

- **Mono, 16-bit, matching sample rate.** `mux.py` mixes samples in Python and
  refuses anything else rather than silently producing noise. `narrate.py`
  already writes 24 kHz mono; a hand-added wav usually does not.
- **Normalise once.** `loudnorm` at mux, and nowhere else. A file normalised at
  export and again on ingest pumps on every consonant.
- **-14 LUFS with -1.5 dBTP.** True peak matters more than it looks: AAC
  encoding overshoots sample peak, and a file that peaked at 0 dBFS before
  encoding clips after it.
- **A bed under narration sits around -22 dB** and fades out over the last
  1.2s. Louder and the voice loses intelligibility on a phone speaker, which is
  where this is watched.

## Picture

- **Never end on a held frame.** `qc.py` fails it. Shorts loops straight back to
  frame 0, so a frozen tail reads as a stall in the loop rather than an ending.
- **Never end on black.** Same reason, worse — it reads as a broken file.
- **`-c:v copy` at mux.** The picture was already encoded at step 4; re-encoding
  it to attach audio costs quality and minutes for nothing.
- **yuv420p, always.** rgb24 or yuv444p files play locally and fail to decode on
  a phone.

## QC

`qc.py` answers exactly six questions: is the plan self-consistent, does the
container match it, is the resolution and fps right, is there audio near -14
LUFS, does it end black, does it end frozen. That is a floor.

What it cannot see, and a person must:

- whether the on-screen text is inside the platform's safe area *in the feed*,
- whether the reveal outruns the read,
- whether the hook still filters after the rewrite,
- whether any claim on screen is one you can stand behind.

Pass `--sheet` and look at the sheet. "It rendered" and "it is correct" are
different claims, and only one of them is in the exit code.

## Reproducibility

Commit `lines.json`, `plan.json`, `render.py` and the storyboard. The wavs and
the mp4 are derived, but commit the final mp4 anyway if it ships — a voice
endpoint's output is not guaranteed identical next month, and the file is the
record of what was published.

State in the report: the voice id, the rate, the total narration seconds, the
render wall-clock, and the money spent. For this pipeline that last number is
zero, which is only worth saying because it is checkable.
