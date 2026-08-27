# Animation rules

Craft notes for `mg.py`. Numbers are starting points that survive contact with a
feed, not laws.

## Timing

| Move | Duration | Ease |
|---|---|---|
| Text fade + 40px slide in | 0.35–0.45s | `ease_out` |
| Rule / underline sweep | 0.4–0.6s | `ease_out` |
| Counter roll | 1.0–1.6s | `ease_out` |
| Card swap (out then in) | 0.2s + 0.3s | `ease_in` then `ease_out` |
| The one hero element | 0.5s | `ease_out_back` |
| Cut (no transition) | 0 | — |

**Stagger** related elements 120–200 ms apart. Below 100 ms they read as
simultaneous; above 300 ms the second one feels like a mistake.

**Hold.** A line needs roughly `0.35s + 0.06s per word` on screen after it
finishes animating. Anything shorter is decoration, not communication.

## The scene clock

Scene duration comes from measured narration, never from a guess (`video-assembly`
owns this). Inside a scene, place elements against the words they belong to:

```python
# narration: "Sixteen of the best videos this month. Not one mentions price."
p_head = mg.seg(t, 0.10, 0.40)   # "Sixteen of the best videos"
p_turn = mg.seg(t, 2.30, 0.40)   # lands on "Not one"
```

Get those offsets from the TTS word timings when the engine gives them, and from
listening to the wav when it does not. An offset that is 300 ms late reads as a
technical fault; 300 ms early reads as a spoiler.

## Legibility

- **Minimum size** on a 1080×1920 canvas: 44px body, 64px for anything a viewer
  is expected to read in passing, 88–120px for a hook card.
- **Contrast** at least 4.5:1 against what is *behind the text at that frame* —
  which during a fade is not the final background. `mg.mix(bg, INK, p)` fades
  the ink toward the background rather than compositing alpha, so contrast is
  exact at every frame instead of approximately right at the end.
- **Line length** 20–30 characters at hook size, up to 42 at body size.
  `mg.wrap` takes a pixel width; pick it from `SAFE`, not by eye.
- **Never centre a paragraph.** Centre one or two lines; anything longer gets a
  ragged left edge that the eye has to re-find every line.

## Motion budget

One video, one idea about movement. Pick a primary axis — vertical for lists and
receipts, horizontal for timelines and comparisons — and keep everything on it.
Diagonal drift, rotation and scale pulses are individually fine and collectively
noise.

Backgrounds do not move. A moving background under moving text halves the
readability of both and is the single most common tell of a template.

## Colour

Two colours and one accent. The accent marks exactly one class of thing — the
money, the verdict, the delta — and never decorates. If the accent appears on
three unrelated element types the viewer stops reading it as a signal.

Set them once at the top of `render.py`:

```python
mg.INK, mg.PAPER, mg.ACCENT = (20, 20, 22), (243, 239, 230), (198, 58, 46)
```

## Anti-patterns

- **The reveal that outruns the read.** Word-by-word at 20 words/second is a
  strobe. Match `reveal_words` to the narration, or cut and hold instead.
- **Typewriter for long text.** Charming for eight characters, exhausting for a
  sentence. `reveal_words` above ~5 words.
- **Easing everything with `ease_in_out`.** It is the slowest-feeling curve;
  used everywhere the video reads as sluggish. Default to `ease_out`.
- **Symmetric layouts.** A centred stack of centred lines has no reading order.
  Anchor to the left safe edge and let length vary.
- **A frozen last second.** The final frame held for 30 frames looks like a
  crash and, on Shorts, reads as a failed loop. End on the last motion or cut
  0.3s after it. `video-assembly`'s QC gate fails a render for this.
- **Colour-only encoding.** Red vs green for up vs down is invisible to part of
  the audience and to anyone watching at 200 nits in daylight. Pair with a sign,
  a position or a word.
