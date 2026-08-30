---
name: thumbnail-director
description: Generate and choose a longform thumbnail that is legible at phone size, understandable without reading the title, and honest about what the episode actually argues. Use when packaging an episode, when a thumbnail concept frames the thesis wrongly, or when deciding between candidates.
---

# thumbnail-director

Three constraints, in priority order. The third is the one that gets skipped.

1. **Readable at phone size.** Roughly 320×180 in a feed.
2. **Understandable without the title.** The title may be truncated, translated
   or absent depending on surface.
3. **Honest about the thesis.** A thumbnail that sells a different argument than
   the episode makes is a failure even when it wins clicks.

## Why the third one matters most

Consider two candidates for an episode arguing that AI-vs-human similarity is
the *wrong* frame:

| Candidate | Verdict |
|---|---|
| "인간이랑 뭐가 달라?" | **Reject.** Frames the episode as a human-similarity argument — the exact reading it spends eleven minutes refusing. Viewers arrive expecting that debate and leave when it does not happen. |
| "저도 믿는데요?" | **Use.** Puts the claim in the AI's mouth and leaves judgement to the viewer. Same curiosity, correct thesis, and it is a line the episode actually contains. |

The first would probably out-click the second. It would also raise the exit rate
in the first minute and mistrain the audience about what the channel does. For a
channel whose returning viewers are the whole business, a thumbnail that
oversells costs more than it earns.

Retention is downstream of the promise. Fix the promise.

## Generate at least six concepts

Force spread across approaches:

| Approach | Shape |
|---|---|
| **Scene** | the episode's own image — the situation |
| **Quote** | a line from the episode, in the speaker's mouth |
| **Confrontation** | two things facing each other |
| **Question** | the question, typeset large |
| **Anomaly** | one element that should not be there |
| **Contrast pair** | the two things the episode separates |

## Craft rules

- **Three to seven Korean characters** in the primary line. Anything longer is
  unreadable in feed.
- **One idea.** A second line only as a small subordinate, never competing.
- **Extreme contrast.** Test by shrinking to 320px wide and squinting.
- **Face or figure large**, in the right third; text in the left two-thirds.
- **One accent colour** against a dark ground. The episode's warm accent, so
  the channel accumulates a recognisable look.
- **No arrows, no red circles, no shock faces.** Wrong register for an essay
  channel, and they promise a video this is not.
- **Never render the face of a religious figure.** Never grotesque or
  sensational religious imagery.
- One cue that the figure is not human — a single cold-coloured detail does more
  than any amount of chrome or circuitry.

## Building it

Cheapest reliable path: a `<Still>` in the same Remotion project as the episode.
It inherits the palette, the fonts and the visual language automatically, it
renders in seconds, and it stays consistent across a series without a separate
brand file.

```bash
npx remotion still src/index.ts Thumbnail "$EPISODE/thumbnail/thumbnail.png"
```

Generative image models are for the *scene* behind the type, when one is needed.
The type itself should be laid out in the composition — a model asked to render
Korean text will produce plausible-looking nonsense.

## Choose

Shrink every candidate to 320px, view them in a row, and pick the one that is
still legible **and** still honest. Record the rejected concepts and the reason —
"rejected: frames the thesis as similarity" is exactly the note that stops the
same mistake on episode four.
