# AI가 세례를 받으려 한다면?

11:50 · 16:9 · 1920×1080 · 30fps · Korean
The first episode built with `longform-factory`.

## What this is

An essay that refuses to answer its own title. It takes the question *"can an AI
be baptized?"*, shows that the intuitive answers depend on a word — 믿는다 — that
turns out to be doing unexamined work, walks through duplication and
non-substitutability into the incarnation's historical particularity, and comes
back to AI holding a different question than it started with:

> 그래서 너와 바로 그 하나님 사이에는 무슨 일이 있었는데?

It does **not** conclude that AI can be baptized. It does not conclude that it
cannot. `video-red-team` fails a cut that reads as either.

## Structure

14 scenes · 157 beats · 26.1% avatar / 73.9% motion graphics.

| | Scene | | | Scene |
|---|---|---|---|---|
| S01 | 0:00 cold open | | S08 | 5:55 성육신 |
| S02 | 0:20 첫 번째 반사 | | S09 | 7:15 예수의 복제본 |
| S03 | 0:55 10년 | | S10 | 8:08 다시 AI |
| S04 | 1:40 우리는 무엇을 보고 믿음을 인정하는가 | | S11 | 9:16 AI의 대답 |
| S05 | 2:30 질문을 바꾼다 | | S12 | 10:24 결론 |
| S05B | 3:08 세례는 누구의 행위인가 | | S13 | 11:24 END |
| S06 | 3:33 완벽한 복제 | | | |
| S07 | 4:51 함께 통과한 시간 | | | |

**S05B did not exist in the submitted draft.** The theology red team added it —
see below.

## What the red team changed

Two required fixes. Full reasoning in `script/theology-redteam.md`.

**RT-01 · the incarnation metaphor.** The draft said 무한한 하나님이 유한한 역사
속에서 **특정한 좌표를 취하셨습니다**. Two sentences earlier it correctly denies that
the divine nature became finite — and then this line makes *God* the thing that
acquires a bounded location, which is the same claim by another route. Labelling
it 비유 does not repair a metaphor whose literal reading is the forbidden claim;
it only makes the claim deniable. Rewritten so the finite verb governs the
**meeting**, not the essence, keeping the particularity the argument needs.

**RT-02 · the baptismal frame.** From S03 onward the draft ran on an unstated
premise: that the church's question about a candidate is *"does this one
credibly and personally believe?"* Traditions practising infant baptism baptize
candidates who cannot profess anything — on the draft's framing an infant fails
every test it applies to the AI. Fixing it turned out to *strengthen* the thesis,
because paedobaptist practice already refuses the checklist reading of baptism.
That is the episode's own conclusion arriving early, from inside church practice
rather than philosophy. Hence S05B.

## Build state

| | |
|---|---|
| Script | **LOCKED** v1.1 |
| Claim map | 21 claims · 4 guarded lines |
| Theology red team | **PASS** (2 required fixes applied) |
| Storyboard | **VALID** — beats sum exactly, avatar share inside band |
| Remotion composition | **BUILDS AND RENDERS** — typecheck clean |
| Narration | **MISSING** — no TTS credential in this environment |
| Avatar lip-sync | **MISSING** — no CUDA GPU in this environment |
| Cut review | pending final audio |
| Publish | **BLOCKED** — human approval required |

The current render is a complete, correctly-timed motion-graphics cut with
**placeholder avatar plates and no audio**. Right artifact for reviewing
structure, pacing, typography and density — the 74% that carries the argument.
Wrong artifact for judging hook strength, narration or the avatar.

## Running it

```bash
cd remotion && npm install

# review a single scene as a still — seconds, not minutes
npx remotion still src/index.ts Scene-S08 /tmp/s08.png --frame=1900

# the whole cut
npx remotion render src/index.ts Episode ../export/final.mp4 --concurrency=2

# the thumbnail
npx remotion still src/index.ts Thumbnail ../thumbnail/thumbnail.png

# interactive
npx remotion studio src/index.ts
```

Validate the storyboard after any timing change — it is the only timing source,
so an edit there is an edit to the video:

```bash
python3 ../../scripts/verify_storyboard.py storyboard/storyboard.json
```

## To finish it

1. **Narration.** Two distinct voices — narrator and the AI character. See
   `audio/manifest.json` for direction and options. A human read removes the
   corporate-TTS mandatory failure outright and is the strongest choice for an
   essay channel.
2. **Subtitle QC.** `python3 scripts/subtitle_qc.py` — the four guarded lines
   must come back verbatim.
3. **Avatar** (optional). Needs a CUDA box. `avatar/<sceneId>.mp4`, then
   `node remotion/scripts/sync-avatar.mjs`. Shipping at 0% avatar with graphics
   carrying every scene is a legitimate choice for a topic this abstract, not a
   degraded one.
4. **Cut review.** `video-red-team`, ≥85 and no mandatory failure.
5. **Approval.** A human, every time.

## Reuse

The Remotion primitives (`src/theme.ts`, `src/lib/`, `src/components/`), the
storyboard schema, the red-team blocking conditions and the QA rubric are all
episode-independent. `.claude/skills/longform-factory/references/reuse.md`
covers bootstrapping the next one — and the trap of running the same argumentative
movement over four different nouns and calling it a series.
