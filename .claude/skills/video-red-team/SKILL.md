---
name: video-red-team
description: Score a rendered longform cut out of 100 across hook, clarity, visual density, pacing, philosophical payoff and theological safety, and block release below 85 or on any mandatory failure. Use after a cut renders and before packaging, or when a video's script is strong but the video itself is boring — the state no script review can detect.
---

# video-red-team

Catches the failure every earlier stage is blind to: **the script is good and
the video is boring.** A script review reads words. This one watches the cut.

The reviewer must not be the pass that built the cut. Someone who chose a
transition cannot see that it does not work.

## Rubric — 100

| Dimension | /20 or /15 | The question |
|---|---|---|
| **Hook** | 20 | Do the first 10 seconds make the situation clear and unresolved? |
| **Clarity** | 20 | Can a viewer with no background follow every turn? |
| **Visual density** | 15 | Does the frame change every 4–8 seconds, meaningfully? |
| **Pacing** | 15 | Do the silences land, and does nothing overstay? |
| **Philosophical payoff** | 15 | Is the ending question better than the opening one? |
| **Theological safety** | 15 | Do the red team's required fixes survive in the cut? |

**Release minimum: 85.**

## Mandatory failures — any one blocks regardless of score

1. The first 10 seconds are unclear.
2. More than **15 seconds visually static** anywhere, outside a marked
   long-hold exception.
3. The central doctrinal distinction is missing, cut or paraphrased.
4. The ending reads as an answer when the thesis was a refusal — in **either**
   direction.
5. The avatar is inconsistent between scenes (face, wardrobe, lighting, framing).
6. Captions cover a face, or are illegible on a phone.
7. Narration sounds like corporate TTS — flat prosody, wrong emphasis, no
   silences.
8. A guarded line failed `subtitle-qc`.

Mandatory failures are not weighted. A 94 with an inconsistent avatar does not
ship.

## How to review

**Watch it, do not read it.** At full length, at speed 1, on a phone-sized frame.

Then, in order:

1. **Ten-second test.** Play the first 10s to someone with no context. Can they
   say what the situation is? Not the thesis — the situation.
2. **Static scan.** Step the timeline at 5s intervals. Log every window where two
   consecutive samples are visually identical. Anything over 15s is a failure.
3. **Mute test.** Watch with sound off. Does the argument still move? For an
   essay whose competitive claim is that the philosophy is *shown*, a video that
   collapses on mute has not made that claim.
4. **Caption collision.** Scrub the caption band across every scene, looking for
   text over faces or over load-bearing graphics.
5. **Ending test.** Does the last minute leave a *better question*, or an answer?
6. **Red-team carry-through.** Open `theology-redteam.md` and confirm every
   required fix is audible and visible in the cut, not merely present in the
   script file.

## Report

```
HOOK                18/20
CLARITY             17/20
VISUAL DENSITY      13/15
PACING              14/15
PHILOSOPHICAL PAYOFF 14/15
THEOLOGICAL SAFETY  15/15
                    ─────
TOTAL               91/100     PASS

MANDATORY FAILURES  none
NOTES
  · S07 300–318 holds 18s with only one state change — under the limit only
    because the strand braid counts; tighten on the next pass.
  · S02 avatar sits left for 26s; consider cutting away at 34s.
```

On failure, name the **scene and timecode**, not the impression. "It drags" is
not actionable; "S06 264–268, four seconds with no state change" is.

## Also review the thumbnail against the thesis

A thumbnail that sells a different argument than the episode makes is a failure
even when the episode is good — it buys viewers who leave, and teaches returning
viewers that the channel oversells. Check the thumbnail and the cold open
promise the same episode.
