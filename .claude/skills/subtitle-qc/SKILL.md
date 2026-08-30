---
name: subtitle-qc
description: Transcribe final narration with faster-whisper, diff it against the canonical script, and fail the render when a guarded line was paraphrased, a sentence was dropped, or timing has drifted. Use after narration is generated and before a cut is approved, or when producing the Korean SRT for upload.
---

# subtitle-qc

The last place a required fix can silently disappear.

A red-team fix agreed in the script is worth nothing if the narrator paraphrased
it. TTS drops clauses; a human read improvises; a re-recorded line reverts to the
phrasing the writer had in their head. This stage compares what was **actually
said** to what was **required**.

## Run

```bash
pip install faster-whisper
python3 ./scripts/subtitle_qc.py \
  --audio episodes/<id>/audio/narration.wav \
  --script episodes/<id>/script/canonical.md \
  --storyboard episodes/<id>/storyboard/storyboard.json \
  --out episodes/<id>/subtitles/
```

Emits `final.srt`, `qc-report.md`, and an exit code — non-zero fails the render.

Use `large-v3` for the QC pass; a smaller model's Korean errors produce false
diffs that cost more time than the model saves.

## What it checks

### 1 · Guarded lines — verbatim, blocking

Any beat carrying `guard` in the storyboard, and any line marked `**[GUARD]**`
in the canonical script, is compared **exactly** (after normalising whitespace
and punctuation). Near-matches fail.

These are red-team required fixes. The whole point of RT-class fixes is that a
specific sentence is present in the delivered audio. "Close enough" is precisely
the failure this exists to catch — a paraphrase that drifts back toward the
wording the red team rejected reads to a viewer as the rejected claim.

### 2 · Missing sentences — blocking

Every script sentence must appear in the transcript. TTS silently dropping a
clause is common and invisible without this check.

### 3 · Timing drift — blocking over threshold

Compare each beat's transcript timestamp to its storyboard `t`. Report per-beat
drift; fail above **±0.6s**, or cumulative drift above **±1.5s**.

Beyond that, captions detach from speech and graphics land on the wrong words —
which is worse than either error alone, because the viewer sees a video that is
subtly out of sync without knowing why.

### 4 · Speaker separation — blocking when the script stages two voices

If the script assigns lines to a second speaker, verify the audio for those beats
came from a different voice. A single-voice render of a two-voice script is a
**content** failure: the argument depends on hearing a second speaker.

### 5 · Pronunciation — advisory

Flag low-confidence tokens on domain terms (성육신, 세례, proper nouns). Advisory,
because whisper's confidence on Korean theological vocabulary is unreliable —
but a human should listen to what it flags.

## SRT rules

- 1–2 lines, ≤ ~26 Korean characters per line
- minimum 1.0s, maximum 6.0s per cue
- ≥ 80ms gap between cues
- break at clause boundaries, never mid-word
- no speaker labels in the SRT itself — styling carries that in the burned-in
  captions, and an uploaded SRT with `[AI]` prefixes reads badly in the player

## Report

```
GUARDED LINES     3/3 verbatim              PASS
MISSING SENTENCES 0                          PASS
TIMING DRIFT      max +0.31s, cum +0.44s     PASS
SPEAKER SEPARATION S11 distinct              PASS
PRONUNCIATION     2 flagged (성육신 ×2)       REVIEW
VERDICT           SUBTITLE_PASS
```

A `REVIEW` does not block. A `FAIL` does, and it names the line.
