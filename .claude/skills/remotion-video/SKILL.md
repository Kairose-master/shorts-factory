---
name: remotion-video
description: Build and render a longform 16:9 Remotion composition from a storyboard JSON — beat clock, burned-in Korean captions, self-hosted fonts, one component per scene, per-scene compositions for review. Use when assembling an episode, adding a scene, debugging tofu glyphs or timing drift, or rendering a full cut. The longform counterpart to the upstream remotion-* skills, which cover generic Remotion usage.
---

# remotion-video

Assembly. The upstream `remotion-create`, `remotion-markup`, `remotion-captions`
and `remotion-render` skills cover Remotion generally; this covers **how this
pipeline uses it** — the storyboard contract, the Korean text problem, and the
review loop.

## The contract

`storyboard/storyboard.json` is imported directly by the composition. Scene
`startSec`/`endSec` become `<Sequence>` bounds; beat `t`/`dur` drive everything
inside. **There is no second place to change a timing** — editing the storyboard
edits the video.

```
remotion/
├── package.json  remotion.config.ts  tsconfig.json
├── public/fonts/            self-hosted Korean webfont
├── public/audio/ public/avatar/      (gitignored)
└── src/
    ├── index.ts  Root.tsx  Episode.tsx  Thumbnail.tsx
    ├── theme.ts             palette + font loading
    ├── lib/beats.ts         storyboard reader + scene clock
    ├── lib/anim.ts          riseIn · settle · draw · breathe · holdEnvelope
    ├── components/          Frame · Caption · AvatarPlate · Type
    └── scenes/              one file per scene
```

## Korean text will render as tofu unless you fix it

Render containers routinely ship **no Korean font** — check before assuming:

```bash
fc-list | grep -iE "noto|nanum|pretendard|cjk" | head
```

If nothing comes back, self-host. Do not rely on a Google Fonts URL: it needs
network at render time and fails silently, producing a full render of empty
boxes that only a still review catches.

```bash
npm pack pretendard --pack-destination /tmp
tar xzf /tmp/pretendard-*.tgz --strip-components=5 -C public/fonts \
  package/dist/web/static/woff2/Pretendard-{Regular,Medium,Bold,ExtraBold}.woff2
```

Load with `FontFace` + `delayRender`/`continueRender` so frames wait for the
font. Call the loader from the shared `Frame` component, not only from the root
composition — each scene is also its own composition, and a standalone scene
render must still have the font. Pretendard is SIL OFL 1.1; keep the licence
beside the files.

## The scene clock

Beat times are episode-absolute; inside a `<Sequence>` the frame counter is
scene-local. `useSceneClock(scene)` converts once and returns `absSec`,
`localSec`, the current `beat`, `beatProgress` and an `at()` helper. A scene
component never computes its own offset — which is also why mounting a scene
alone at frame 0 gives exactly the frames it occupies in the episode, and why
per-scene compositions work without extra plumbing.

## Captions

Burned in, because this audience watches muted on a phone.

- 1–2 lines, never a paragraph. Balance the break by length, not word count.
- Highlight **only** semantic keywords, from the storyboard's `emphasisKeywords`.
  Highlighting everything highlights nothing.
- A gradient scrim behind the band, in the shared component, so no scene has to
  solve legibility locally.
- Distinct styling per speaker where the episode has more than one voice.
- Captions never cover a face — a mandatory failure in `video-red-team`.

## Per-scene compositions

Register `Scene-<id>` for every scene alongside `Episode`. A still is seconds; a
full pass is minutes. **Review stills before every full render.**

```bash
npx remotion still src/index.ts Scene-S06 /tmp/s06.png --frame=1500
npx remotion render src/index.ts Episode "$EPISODE/export/final.mp4" --concurrency=2
```

Pick still frames *inside a visually loaded moment*, not at a scene boundary —
a still at frame 0 of a fade tells you nothing.

## Audio

Attach at episode level, not per scene. The narration is one continuous WAV that
the storyboard was timed against; splitting it per scene lets drift accumulate at
every seam. Music at ~0.16 gain under narration.

## Avatar fallback

Avatar clips are looked up through a manifest. When a scene has no clip — which
is the normal state until a GPU has run phase 9 — render a **designed plate**,
not a grey box: a lit portrait vignette that composes correctly and is obviously
a placeholder. A bad generated face is worse than no face, which is the same
reason the episode is 65–75% graphics in the first place.

## Failure modes

| Symptom | Cause |
|---|---|
| Empty boxes for Korean | font not loaded, or loaded without `delayRender` |
| Text collapsing multiple spaces | HTML whitespace; use separate elements or `pre` |
| An element stretched out of proportion | `preserveAspectRatio="none"` on a non-matching viewBox |
| A frame that reads as broken | a `scaleY` collapse; drop and fade instead |
| Element off frame | SVG coordinates written against a different baseline than the layout |
| Timing right in prose, wrong on screen | something read a duration from somewhere other than the storyboard |

## Settings

1920×1080, 30fps, H.264. `--concurrency=2` on a small container; higher
concurrency on a 2-core box thrashes and renders slower.
