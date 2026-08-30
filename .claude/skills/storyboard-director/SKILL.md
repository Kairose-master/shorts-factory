---
name: storyboard-director
description: Break a locked longform script into a machine-readable storyboard of scenes and 3–14 second beats that a Remotion composition can render directly. Use after a script passes theology red team and before any assembly, or when timings stated in prose have drifted from what the video actually does.
---

# storyboard-director

Turns `script/canonical.md` into `storyboard/storyboard.json` — the single
timing source for the rest of the pipeline. Prose timings and render timings
diverge the moment either is edited; this file removes the second place to be
wrong. **`remotion-video` reads it directly, so a storyboard edit is a video edit.**

## Structure

```json
{
  "episodeId": "...", "fps": 30, "width": 1920, "height": 1080,
  "durationSec": 710, "durationInFrames": 21300,
  "budget": {"avatarSec": 185, "avatarShare": 0.261,
             "targetBand": [0.25,0.35], "maxStaticSec": 12,
             "visualStateChangeEverySec": [4,8]},
  "design": {"bg":"#0A0A0C","ink":"#F2EFE9","warm":"#C9A227","cold":"#4A7FB5"},
  "emphasisKeywords": ["세례","믿음","바로 그 사람"],
  "scenes": [{
    "id":"S01", "title":"...", "component":"ColdOpenChurch",
    "startSec":0, "endSec":20, "avatarSec":8, "avatarRole":"ai",
    "audioNote":"...", "transitionOut":"hard-cut",
    "beats":[{"t":0,"dur":5,"kind":"visual","vo":null,
              "onScreen":null,"visual":"..."}]
  }]
}
```

### Beat fields

| Field | Meaning |
|---|---|
| `t` | **absolute episode seconds**, not scene-local |
| `dur` | seconds; beats in a scene must sum exactly to its duration |
| `kind` | `visual` · `narration` · `avatar` · `quote` · `graphic` · `ui` · `title` · `cut` · `silence` |
| `vo` | spoken line, or `null` for a beat with no narration |
| `speaker` | when more than one voice exists |
| `onScreen` | text that appears; `\n` is a hard line break |
| `visual` | prose direction for whoever builds the component |
| `emphasis` · `marker` · `markerHold` | rendering flags |
| `guard` | this line may not be cut or paraphrased |
| `theology` | `doctrine` \| `analogy`, carried from the claim map |

Extra numeric fields (`zoom`, `converge`, `station`, `stat`, `event`) are scene
keyframes read by that scene's component.

## Hard rules

**Beats sum exactly.** Validate before handing on:

```bash
python3 ./scripts/verify_storyboard.py episodes/<id>/storyboard/storyboard.json
```

**Absolute times.** Beat `t` is episode-absolute so a scene can be reasoned
about in isolation without recomputing offsets. Scene components convert to
scene-local themselves.

**3–14 seconds per beat.** Under 3 and the render cannot land a state change;
over 14 and the frame is static past the tolerable limit. A beat that wants to
be 20 seconds is two beats.

**Size a spoken beat from its character count, not by feel.** This is the single
most expensive mistake available at this stage, because it is invisible until
narration has been generated and by then the beat grid is baked into every scene
component. Korean neural TTS at a contemplative rate reads roughly **4.5–5.5
characters per second** including its own pauses:

```
minimum beat seconds ≈ len(line) / 5 + 0.5
```

A 40-character sentence needs ~8.5s. Giving it 4.5s does not make it faster; it
makes the assembly stage compress it, push the line late, or both. On this
pipeline's first episode 47 of 118 lines overran their beats and one scene came
out 60% over, all from estimating rather than counting.

**Corollary: a line that will not fit is a line that is too long.** Split the
sentence or cut it at the script stage. Two beats of 5s beat one beat of 10s
anyway — the extra boundary is a free visual state change.

**Silence is a beat.** `kind: "silence"`, `vo: null`, a real duration. If it is
not in the storyboard it will get filled.

**Every scene names a component.** One component per scene, so a single scene can
be re-rendered and reviewed without a full pass.

## Pacing

Change visual state every **4–8 seconds** — a new element, a transformation, a
value change, a reframe. Not necessarily a cut; a timeline lighting its next
station counts.

**Never exceed 12 static seconds**, with one class of exception: a scene whose
content *is* the hold — a face admitting uncertainty, a silence after a question
the viewer must sit with. Take the exception rarely, mark it in the scene's
comment, and give the frame a slow drift so it reads as held rather than frozen.

## Scene lengths

35–85 seconds is the workable band. Under 25 and the essay feels like a
slideshow; over 90 and the beat structure inside the scene stops being legible
as one movement. The exceptions are the cold open (~20s) and the ending (~26s),
which are short on purpose.

## Then

`avatar-director` sets `avatarSec` per scene and checks the total share.
`visual-metaphor` fills the `visual` fields for abstract concepts.
`remotion-video` builds one component per scene.
