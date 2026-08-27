# Experiments

One variable per experiment. Two arms. **The hypothesis is written before
publishing** — a hypothesis written after the numbers arrive is not a hypothesis.

## Row format

```
ID              EXP-001
Hypothesis      what we expect and why
Variable        hook | visual | length | POV | tone | platform
Arm A           link to published row
Arm B           link to published row
Held constant   everything else, listed explicitly
Metric          the one number that decides it, and its measurement label
Result          
Verdict         A | B | no-difference | inconclusive
Observations    how many independent runs this verdict rests on
```

`inconclusive` and `Observations: 1` are the two most useful values in this file.
**One observation is a note, not a lesson.**

---

## Planned for cycle 1

### EXP-001 — Does the failure path outperform the happy path?

- **Hypothesis:** A developer audience distrusts demos that never fail. Showing
  the grader *rejecting* work (HS-006) will hold attention better than showing
  the transaction succeeding (HS-001), despite the weaker premise.
- **Variable:** narrative frame — success vs. failure.
- **Held constant:** same capture session, same voice cast, same length band,
  same platform, same posting window, same caption style.
- **Arms:** HS-001 (happy path) vs. HS-006 (failure path).
- **Metric:** views-per-follower against the account's own baseline `[api]`;
  completion rate as a secondary if native insights are available.
- **Note:** the two videos share one screen-capture session, so this experiment
  costs one recording, not two. That is why they were approved as a pair.

### EXP-002 — Does the concept video need a demo to be understood?

- **Hypothesis:** HS-011 (animated, zero product footage) will be understood as
  well as the demos and shared more, because it needs no context.
- **Variable:** format — abstract explainer vs. product demo.
- **Held constant:** length band, voice cast, platform, posting window.
- **Arms:** HS-011 vs. the better-performing of HS-001/HS-006.
- **Metric:** shares-per-view `[api]`; comment comprehension read via
  `read-the-room`.
- **Caveat:** this is a **two-variable** comparison (format *and* subject), so a
  result here is directional at best. Logged honestly as such. A clean version
  needs an animated cut of the *same* subject, which is cycle 2.
