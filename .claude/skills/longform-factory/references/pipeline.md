# The longform pipeline — contracts and gates

Each phase's **input**, **output**, and the specific failure it exists to catch.
A gate that cannot name the failure it prevents is ceremony; every gate below
earns its place by naming one.

## 1 · Script lock — `philosophy-script`

**In** a question. **Out** `script/canonical.md`.

Structure: 사고실험 → 직관 → 반례 → 개념 균열 → 더 깊은 질문. The essay does not
resolve; it relocates the question. A longform essay that answers its own title
in the first two minutes has no reason to run eleven.

**Catches** the explainer failure — a script that teaches a conclusion instead of
walking an argument, and therefore has no retention structure after minute three.

## 2 · Claim separation + red team — `theology-red-team`

**In** `canonical.md`. **Out** `claim-map.json`, `theology-redteam.md`, verdict.

Every sentence is tagged `[THEOLOGY]`, `[PHILOSOPHY]`, `[THOUGHT EXPERIMENT]`,
`[RHETORIC]` or `[OPEN QUESTION]`. Blocking conditions are listed in that skill.

**Catches** register collapse — a thought experiment stated in the grammar of a
confession. This is the failure mode, not unusual opinions. A metaphor whose
literal reading is a forbidden claim is not repaired by labelling it a metaphor;
the metaphor has to change.

**Gate** `THEOLOGY_PASS`. Required fixes must be present in the *rendered cut*,
not merely agreed to — `subtitle-qc` re-verifies them against final narration.

## 3 · Cold open tournament — `hook-tournament`

**In** the locked script. **Out** 10 opens scored, top 3, one chosen.

**Catches** first-hook attachment. The first cold open a writer produces is
almost never their best, and never their most accurate.

## 4 · Storyboard — `storyboard-director`

**In** script + chosen open. **Out** `storyboard/storyboard.json`.

Scenes carry `startSec`/`endSec`; beats carry absolute `t` and `dur`. **Every
scene's beats must sum exactly to its duration** — validate before continuing:

```bash
python3 scripts/verify_storyboard.py episodes/<id>/storyboard/storyboard.json
```

**Catches** drift. Timing stated in prose diverges from timing in the render the
moment either is edited. One machine-readable source removes the second place to
be wrong.

## 5 · Avatar budget — `avatar-director`

**In** storyboard. **Out** per-scene `avatarSec`, total share.

**Gate** share inside 25–35%; no static avatar hold over 12s.

**Catches** the talking-head default — where the avatar quietly becomes the
whole video because it is the cheapest thing to fill time with.

## 6 · Visual metaphors — `visual-metaphor`

**In** abstract concepts from the script. **Out** a concrete visual per concept.

**Catches** stock B-roll and "AI cyberpunk" filler — footage that decorates the
words without carrying the argument.

## 7 · Assets — `media-acquisition`, `asset-hunter`

Licence and provenance recorded per asset. For an episode this abstract, most
"assets" are drawn in Remotion rather than sourced; that is cheaper and more
consistent than searching for footage that does not exist.

## 8 · Narration — `voicebox`

**Out** one continuous WAV per speaker plus `audio/manifest.json`.

Each distinct speaker gets a distinct voice. Where an episode stages a second
speaker (an AI, a quoted person), a single-voice render is a **content** failure,
not a cosmetic one — the argument depends on hearing two.

## 9 · Lip-sync — MuseTalk 1.5 / EchoMimicV2

**Needs CUDA.** MuseTalk for close-up mouth work; EchoMimicV2 when upper-body
gesture materially improves a scene. Output goes to `avatar/<sceneId>.mp4`.

Absent a GPU this phase is skipped and `remotion-video` falls back to the
designed avatar plate. The episode still renders, times and reviews correctly —
only the avatar beats are placeholders. Say so plainly rather than implying the
cut is final.

## 10 · Assembly — `remotion-video`

**In** storyboard + audio + avatar clips. **Out** `export/final.mp4`.

**Catches** nothing by itself; it is the build. Review stills per scene before
committing to a full render — a full pass is minutes, a still is seconds.

## 11 · Subtitles + QC — `subtitle-qc`

`faster-whisper` transcribes the final narration and diffs it against
`canonical.md`.

**Catches** the drift that matters most: a narrator paraphrasing a line the red
team required verbatim. Guarded lines are compared exactly; a paraphrase of a
guarded line fails the render.

## 12 · Cut review — `video-red-team`

Scored /100 across hook, clarity, visual density, pacing, payoff, safety.

**Catches** "the script is good but the video is boring" — the state no
script-level review can see.

**Gate** ≥85, with mandatory failures that override the score.

## 13 · Thumbnail — `thumbnail-director`

**Catches** a thumbnail that sells a different thesis than the episode argues —
which costs more than a weak thumbnail, because it buys the wrong viewers and
they leave.

## 14 · Publish — `youtube-publisher`

**Gate** explicit human approval, every time. A successful render is not an
approval, and neither is a passing QA score.

## 15 · Learn — `analytics-review`

Retention curve read against the storyboard, so a drop is attributed to a
*named scene* rather than a vague minute.
