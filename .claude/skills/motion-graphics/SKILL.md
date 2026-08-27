---
name: motion-graphics
description: Use when a short needs animation rather than footage — kinetic type, an animated receipt or counter, a chart that builds, a card sequence, a title treatment — or when a generated-video budget has run out and the shot still has to exist. Draws every frame from code, so a render costs nothing and repeats exactly.
---

# Motion Graphics

**A frame is a pure function of time.** `frame(t, i) -> Image`. No timeline
state, no layer stack, no credits. That single constraint is what makes a render
free, deterministic, diffable and re-runnable at 3 a.m. without a card on file.

Use this when the shot is *information* — a number, a list, a quote, a
comparison, a process. Use footage (`media-acquisition`) when the shot is
*a thing in the world*. A talking head with a chart behind it needs both.

## Requires

`pip install pillow numpy imageio-ffmpeg` — that is the whole dependency list,
and `imageio-ffmpeg` carries its own ffmpeg binary, so no system package is
needed. Run `scripts/selfcheck.py` first; it renders three seconds and a contact
sheet in about ten, and it fails on a missing font *now* rather than at minute
forty of a render.

```bash
python3 .claude/skills/motion-graphics/scripts/selfcheck.py --out /tmp/mg
```

## The engine

`scripts/mg.py` is imported, not run. Add its directory to `sys.path` from the
project's `render.py` and call `mg.render(frame_fn, duration, path)`.

| Group | What it gives you |
|---|---|
| Canvas | `W`, `H`, `FPS`, `SAFE`, `canvas()`, palette constants, `font()` |
| Easing | `ease_out` (default), `ease_in`, `ease_in_out`, `ease_out_back`, `linear` |
| Scheduling | `seg(t, start, dur, ease)` → local 0‑1 progress · `hold()` · `caret()` |
| Text | `wrap`, `fit_font`, `text_block`, `reveal_words`, `typewriter` |
| Marks | `rule` (self-drawing line), `panel`, `progress_bar`, `counter`, `mix` |
| Output | `render`, `Encoder`, `contact_sheet`, `duration_of` |

`seg` is the one to understand. Every element is written against the **scene
clock**, and `seg` converts that clock into one element's own 0‑to‑1 progress:

```python
p = mg.seg(t, 0.6, 0.4)          # starts at 0.6s, runs 0.4s, eased, clamped
y = 900 - int(40 * (1 - p))      # slide up into place
d.text((x, y), line, font=f, fill=mg.mix(bg, mg.INK, p))   # and fade in
```

Nothing accumulates, so scrubbing to any `t` is exact and a re-render of one
scene cannot drift from the others.

## Non-negotiables

- **Safe area.** `mg.SAFE` reserves 96px sides, 260px top, 380px bottom. The
  bottom is the big one: TikTok's caption block and the Reels UI eat far more
  than people expect, and text that clears it in the editor still gets covered
  in the feed.
- **Legibility beats motion.** A line must be readable while it is moving. If
  the reveal is faster than the read, the motion cost you the words.
- **One overshoot per video.** `ease_out_back` on the single element that
  matters. Every element bouncing reads as a template.
- **Fixed-width numbers.** Animate a counter with `mono` and a padded format
  (`"{:>7,.2f}"`) or the digits jitter as the string width changes.
- **Deterministic randomness.** Seed per scene *and* per hold group
  (`random.Random(scene * 733 + i // hold)`), never per frame, or the texture
  strobes at 30 Hz.

The timing tables, the motion budget, and the anti-patterns that survive a
render but not a viewer are in `references/animation-rules.md`. Read it before
storyboarding, not after the first render disappoints.

## Where this sits

`video-formats` chooses the scene grammar. This skill draws it.
`video-assembly` owns narration, timing, mux and the QC gate — including the
rule that **narration is synthesised before frames are drawn**, because measured
narration duration is the scene clock this engine renders against. Ignore that
order and every `seg()` offset in the file is a guess.

`brand-kit` supplies the palette and type once so they are not re-decided per
video; override `mg.INK`, `mg.PAPER`, `mg.ACCENT` and `mg.FONT_FILES` at the top
of `render.py` rather than editing the engine.

## Anti-patterns

- **Rendering PNGs to a scratch directory, then encoding.** `mg.Encoder` pipes
  raw RGB into libx264 directly. The scratch pass costs minutes and disk and
  buys nothing.
- **Calling a paid generator for something that is text on a background.** A
  card, a quote, a receipt, a bar chart and a countdown are all cheaper, sharper
  and re-editable as code. Reach for generation when the shot needs the world.
- **Declaring a render correct from the exit code.** `contact_sheet()` exists
  because ffmpeg exits 0 on twelve identical blank frames. Look at the sheet.
- **Animating everything at once.** If three things move in the same 300 ms the
  eye picks one and misses two. Stagger by 120–200 ms.
