# Reusing the stack

The first episode pays for the machinery. From the second on, most of the
pipeline is untouched.

## What is fixed across episodes

| Fixed | Where |
|---|---|
| Storyboard schema | `storyboard-director` |
| Beat clock, caption engine, theme tokens | `remotion-video` primitives |
| Frame · Safe · Vignette · Grain · Statement · Readout · markers | `remotion/src/components/` |
| Red-team blocking conditions | `theology-red-team` |
| QA rubric and mandatory failures | `video-red-team` |
| Avatar budget rule | `avatar-director` |
| Publish gate | `youtube-publisher` |

## What is new per episode

- `script/canonical.md` and its claim map
- the scene components (`remotion/src/scenes/*.tsx`)
- image prompts and the thumbnail
- narration WAV

## Bootstrapping episode N+1

```bash
cp -r episodes/<done>/remotion episodes/<new>/remotion
rm -rf episodes/<new>/remotion/src/scenes/*
# keep: src/theme.ts, src/lib/, src/components/, public/fonts/
```

Then run phases 1–6, write the new scene components against the new storyboard,
and continue from phase 10.

## The planned series

Each reuses the same movement — a checklist reading of some phenomenon is
displaced by a question about history, attribution and relation — so the visual
grammar built for `ai-baptism` carries over directly.

| Episode | Question | Reuses |
|---|---|---|
| `ai-sin` | AI가 죄를 지을 수 있을까? | agency vs. attribution; the stat-sheet disassembly |
| `ai-prayer` | AI가 기도하면 하나님은 들으실까? | the addressed-party frame; the incarnation zoom |
| `memory-copy` | 기억을 복제하면 과거도 복제될까? | the duplication scene and the 기억 ≠ 당사자 graphic, near-verbatim |
| `ai-forgiveness` | AI에게 용서를 구할 수 있을까? | the event timeline; the relation network |

`memory-copy` is the cheapest second episode — it is the S06/S07 argument
promoted from a segment to a full essay, and those two scene components port
with only copy changes.

## The trap

Reuse is a property of the *machinery*, not the *argument*. Four episodes that
run the same movement over four nouns is one episode published four times.
Each needs a genuinely different second half — a different place the question
gets relocated to — or the series reads as a template, which is exactly the
"AI smell" the whole avatar ratio exists to avoid.
