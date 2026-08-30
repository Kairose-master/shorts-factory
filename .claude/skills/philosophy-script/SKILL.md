---
name: philosophy-script
description: Write a Korean longform video essay that walks an argument instead of teaching a conclusion — thought experiment, intuition, counterexample, conceptual fracture, deeper question. Use when a philosophical, ethical or theological question has to become a 10–20 minute script, when an existing draft resolves too early or reads like a lecture, or when a script needs restructuring so a video agent can decompose it into scenes.
---

# philosophy-script

Writes the script an essay channel lives on. The job is **not** to explain a
position. It is to take a question the viewer thinks is simple, show them why
their first answer does not survive contact, and leave them holding a better
question than the one they arrived with.

## The five-movement shape

```
사고실험  →  직관  →  반례  →  개념 균열  →  더 깊은 질문
```

| Movement | What it does | Failure if skipped |
|---|---|---|
| **사고실험** | a concrete scenario, not an abstract framing | the viewer has nothing to have an intuition *about* |
| **직관** | name the answer the viewer already has, sympathetically | they feel argued at, and defend instead of thinking |
| **반례** | add one condition that makes that answer uncomfortable | the essay has no engine; nothing is at stake |
| **개념 균열** | show *which word* was doing unexamined work | it becomes an opinion piece rather than analysis |
| **더 깊은 질문** | relocate the question, do not resolve it | the last two minutes are unnecessary; retention collapses |

The fracture is where an essay earns its length. Locate the one word the
question was leaning on — 믿는다, 같다, 사람, 기억한다 — and show that the word was
never as simple as the question assumed.

## Rules

**Do not resolve.** An essay that answers its own title is a two-minute video
padded to twelve. The ending relocates: *this was the wrong first question, and
here is the one that comes before it.*

**One condition at a time.** Each new stipulation gets its own beat and its own
silence. Stacking three conditions in one paragraph loses the viewer at the
first.

**Concrete before abstract, always.** "완벽하게 복제된 사람이 사랑해라고 말합니다"
lands; "수적 동일성과 질적 동일성의 구분" does not. If a technical term is
unavoidable, translate it into ordinary Korean in the same breath, then never
use it again.

**Write the silences.** Mark them in the script with a duration. A three-second
hold after a question is a structural element, and if it is not written down the
production stage will fill it.

**Steelman before you fracture.** The objection you break must be the strongest
version, stated in the viewer's own words. Breaking a weak version teaches them
you are not arguing in good faith, and they leave.

**Never sneer at the intuition.** The viewer holds it. Contempt for the first
answer is contempt for the person watching.

## Spoken-Korean register

- Natural spoken Korean, `-습니다` throughout for the narrator. Not a sermon
  register, not an announcer register.
- Short sentences. One clause per line where the line is a beat.
- Direct address (여러분) at the turns, not continuously.
- No academic jargon without immediate translation.
- No "구독 좋아요" ask. It costs the ending, which is the only part anyone quotes.

## Length budget

For a 10–12 minute episode: roughly **1,500–1,900 spoken Korean syllables per
minute of finished video** is far too fast — target instead **~210–240 spoken
characters per minute**, with silence budgeted separately. Practically: write
the beats with durations, sum them, and let the sum decide the runtime rather
than writing to a word count.

Reserve 8–12% of total runtime for silence. On an eleven-minute essay that is
roughly one minute of deliberate nothing, and it is the difference between an
essay and a podcast.

## Output

`script/canonical.md`, with:

- a header carrying episode id, runtime, avatar share, script-lock version
- scenes with explicit time ranges
- narration as quoted blocks, speaker-attributed where more than one voice
- `**ON-SCREEN**` blocks for text that appears rather than is spoken
- `**[GUARD]**` on any line that may not be cut or paraphrased downstream
- inline `[THEOLOGY]` / `[THOUGHT EXPERIMENT]` tags where register changes

Hand straight to `theology-red-team`. Do not storyboard an unreviewed script —
a required fix at phase 2 can change scene count, and re-timing a storyboard
costs more than waiting for the review.
