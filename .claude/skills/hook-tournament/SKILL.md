---
name: hook-tournament
description: Generate ten cold opens for one longform topic, score them on a fixed rubric, and keep the strongest three before choosing one. Use when an episode needs its opening 20 seconds, when a draft open is suspected of being the first idea rather than the best, or when an open is accurate but not compelling (or compelling but not accurate).
---

# hook-tournament

A longform cold open is not a short-form hook. A Short's hook survives three
seconds; an essay's open has to survive **eleven minutes of payoff** — it must
still be true at minute ten. Openers that outperform on the first metric and
lose on the second are how essay channels train an audience to distrust them.

Ten candidates, scored, top three kept, one chosen. Ten because the first is
almost never the best and the third is where writers usually stop.

## Rubric — 100 points

| Criterion | /20 | The question it answers |
|---|---|---|
| **Immediate comprehension** | 20 | Does a viewer with no context understand the situation in one sentence? |
| **Surprise** | 20 | Is there a turn they did not see coming? |
| **Curiosity** | 20 | Do they *need* the next line? |
| **Accuracy** | 20 | Is it still true after the payoff lands? |
| **Payoff compatibility** | 20 | Does the episode actually deliver on what this promises? |

**Accuracy and payoff compatibility are hard gates.** A candidate scoring below
14 on either is eliminated regardless of total. A 92 that misrepresents the
thesis is worse than a 78 that does not — it buys the wrong viewers, who leave,
and teaches the returning ones that the channel oversells.

## Generate across archetypes, not variations

Ten rephrasings of one idea is one candidate. Force spread:

| Archetype | Shape |
|---|---|
| **Scene** | drop the viewer into a moment, no framing |
| **Direct question** | ask the viewer the thing, immediately |
| **Stipulation** | "이런 조건이라면" — hand them the premise up front |
| **Reversal** | state the obvious answer, then break it |
| **Confession** | a character admits the uncertainty the essay explores |
| **Concrete anomaly** | a small fact that should not be true |
| **Refused frame** | name the question everyone asks, then decline it |

At least five distinct archetypes among the ten.

## Scene opens win longform, usually

For an essay, the strongest open is normally a **scene** — a situation the
viewer parses instantly and cannot resolve. It needs no context, it dramatises
the question rather than stating it, and it gives the ending something to call
back to. A closing callback to the opening scene is the cheapest and most
effective structural payoff available to an essay.

Prefer a scene when: the question has a natural human situation, and the essay
ends by returning to it.
Prefer a direct question when: the situation is abstract enough that staging it
would be more confusing than asking.

## Output

```
1. [archetype] "text"
   comprehension 18 · surprise 17 · curiosity 19 · accuracy 20 · payoff 19 = 93
   note: one line on what it risks
```

Then: the three survivors, the choice, and **one sentence on what the choice
gives up**. Every open trades something. Naming the trade is how the next
episode's tournament gets better.

Hand the winner to `storyboard-director` as SCENE 01, and tell `thumbnail-director`
what it promises — the thumbnail and the open must sell the same episode.
