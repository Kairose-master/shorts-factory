---
name: avatar-director
description: Decide where an AI avatar appears in a longform video and where graphics carry the scene instead, hold the avatar share inside 25–35%, and drive MuseTalk 1.5 or EchoMimicV2 to produce the lip-synced clips. Use when planning avatar placement, when a cut feels like a talking head, or when deciding whether a machine can run lip-sync at all.
---

# avatar-director

Two jobs: **decide where the avatar appears**, and **produce the clips**. The
first matters more, and it is the one most pipelines skip.

## The budget

**25–35% of runtime.** Everything else is motion graphics.

This is not a style preference. A held synthetic face is the strongest "this was
generated" signal a viewer receives — stronger than script, pacing or voice.
Below 25% the episode loses its human anchor; above 35% it starts reading as an
avatar video regardless of how good the face is. The cheapest way to make a
video look less synthetic is to show less synthetic face.

**No static avatar hold over 12 seconds**, except a scene whose content *is* the
hold (see below).

## Where the avatar earns its place

| Use it | Why |
|---|---|
| Cold open dialogue | a character speaking is a scene; a graphic is not |
| Turns and hand-offs | "이제 …를 내려놓겠습니다" — a person changes subject better than a title card |
| Direct address | 여러분 lands from a face |
| A confession or admission | the whole point is that someone is saying it |
| The closing callback | it pays off the open |

| Do not use it | Instead |
|---|---|
| Explaining a structure | show the structure |
| Timelines, comparisons, scoring | build the graphic |
| Abstract concepts | `visual-metaphor` |
| Anything with a diagram on screen | the diagram; a face beside it splits attention and wins nothing |
| Narration over a continuous visual movement | let the movement run |

## The long-hold exception

One scene per episode may hold the avatar well past 12 seconds — where the
content *is* the hold. A face admitting it cannot verify its own interior, held
for a minute, is doing work no cut could do; cutting away lets the viewer off
the hook the scene exists to set.

Take it once. Mark it in the storyboard. Give the frame a slow drift — a
breathing scale, a drifting key light — so it reads as held, not frozen.

## Voice

Each distinct speaker gets a distinct voice. Where an episode stages an AI
character alongside a narrator, a single-voice render is a **content** failure:
the argument depends on the viewer hearing a second speaker. Flag it to
`subtitle-qc` as a QA condition, not a note.

## Producing the clips

### Requirements

Both engines need **CUDA**. Check first, and say the result plainly:

```bash
command -v nvidia-smi >/dev/null && nvidia-smi -L || echo "NO GPU — lip-sync unavailable"
```

No GPU means phase 9 is skipped. `remotion-video` falls back to a designed
avatar plate; the episode still renders, times and reviews correctly, and only
the avatar beats are placeholders. **Say that, rather than presenting the cut as
final.** Options: run this phase on a GPU box, rent one, or ship the episode at
0% avatar with graphics carrying every scene — which for an abstract topic is a
legitimate choice, not a degraded one.

### Choosing an engine

| | MuseTalk 1.5 | EchoMimicV2 |
|---|---|---|
| Scope | mouth region on an existing clip | half-body, audio-driven, with gesture |
| Use for | close-ups, the confession, the callback | a presenter whose hands matter |
| Input | driving video + audio | reference image + audio (+ pose) |
| Cost | cheaper, faster | heavier |

Default to MuseTalk. Reach for EchoMimicV2 only when upper-body gesture
materially improves a scene — which for an essay is rare, because the avatar is
usually cut away from within a few seconds anyway.

### Consistency

Same face, same wardrobe, same lighting, same framing across every scene. An
avatar that changes between scenes is a mandatory failure in `video-red-team`,
and it is the most common defect when clips are generated scene by scene.
Generate the reference **once**, store it, and drive every clip from it.

### Output contract

`avatar/<sceneId>.mp4`, at the composition's resolution and fps, exactly the
length of that scene's avatar window. Register it in the manifest that
`remotion-video` reads; an unregistered clip is silently ignored.

## Reporting

Always report the achieved share, per scene and total, against the 25–35% band —
and against how much of it is real lip-sync versus placeholder.
