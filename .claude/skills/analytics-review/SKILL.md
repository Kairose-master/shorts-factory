---
name: analytics-review
description: Read a published longform episode's retention curve against its storyboard so every drop is attributed to a named scene and beat, and turn that into specific changes for the next episode. Use when analytics exist for a published episode, or when deciding what to change about a format.
---

# analytics-review

Closes the loop. The point is not "retention was 42%." It is **which scene lost
them, and why that scene.**

## Why the storyboard makes this work

Retention is reported by time. The storyboard maps time to *named scenes and
beats*. So a drop at 4:38 is not "somewhere in the middle" — it is `S06`, beat
`264`, the four-second silence after "원래 그 사람이 없어져도 괜찮을까요?".

That is the difference between a guess and a finding. Always resolve a drop to a
beat before interpreting it.

```
retention timestamp → storyboard scene + beat → what that beat asked the viewer to do
```

## Read in this order

**1 · First 30 seconds.** The steepest drop in any video. Compare against the
channel's own baseline, never against a published benchmark — audience, topic
and surface all move it.

**2 · Named drops.** Every fall steeper than the local trend. For each: which
scene, which beat, and which of these it is —
- a **question the viewer could not parse** (clarity)
- a **hold that outstayed** (pacing)
- a **turn they did not want to take** (the argument lost them)
- a **promise the thumbnail made that this scene contradicted** (packaging)

Only the last is a packaging problem. The first three are production problems,
and the fix is in a different skill each time.

**3 · Recoveries.** More informative than drops and almost never examined. A
rising curve means a scene *won people back*. Find what it did — usually a
concrete scenario after an abstract stretch — and put more of it earlier.

**4 · The ending.** For an essay, how many reached the final question is the
metric that matters most. It is the part that gets quoted, shared and argued
with. A strong ending seen by 8% of viewers is a structural failure upstream,
not a weak ending.

**5 · Comments as evidence of comprehension.** Run `read-the-room`. Are people
arguing with the argument the episode made, or with one it did not? Widespread
misreading of the thesis is a *script* finding, and often traces to a specific
beat where two claims were compressed into one.

## Rules

**Never optimise from one episode.** A single retention curve is one
observation. Two episodes make a line, not a trend. Write the hypothesis down
and wait.

**Separate the format from the topic.** A topic that under-performs does not
mean the format failed. Change one variable per episode, and say which one
before publishing.

**Do not chase the average.** A niche essay channel wins on the people who
finish and return, not on the median viewer who never would have. Watch
returning-viewer share and the ending-reach number over raw retention.

**Report avatar share alongside retention.** The 25–35% band is a hypothesis,
not a law. Across five or six episodes it becomes testable — and if the data
says something different for this channel, change the band and say why.

## Output

Append to the episode's `qa/` folder and to the Office lessons file:

```
EPISODE   ai-baptism
RETENTION 30s 71% · 50% at 6:12 (S08 성육신) · ending reach 19%
DROPS     S06 264 (−4.1pp) four-second silence — the longest hold in the cut
          S08 380 (−3.3pp) three-second silence on 성육신
RECOVERY  S09 459 (+1.2pp) the "똑같네" quote
READING   Both named drops are silences. The silences are doing what they were
          designed to do at the level of the argument and costing viewers at the
          level of retention. Next episode: keep them, cut each by one second,
          and add a visual state change inside the hold so the frame moves while
          the voice does not.
CHANGE    one variable: silence length. Everything else held.
```
