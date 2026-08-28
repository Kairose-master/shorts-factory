# QC — HS-034

```
IDEA        HS-034 · "The company, running." — floor simulation
RENDER      renders/final.mp4 · 0:37 · 1080x1920 · h264 · aac · 14 SFX cues
AUDIO       mean -20.1 dB · no clipping
GATES       hook 4 · clarity 5 · pacing 5 · visual 5 · accuracy 5
            relevance 5 · retention 5 · cringe 5 · native 4      = 43/45
VERDICT     PASS
```

## What is new here

Every previous cut *argued*. This one *shows*. Same real run as HS-032
(`dlg-AJin4S4WA4` — $7.00 escrowed, $7.00 paid, six roles), rendered as a floor
you watch rather than a list you read:

- six desks, each with a screen that **flickers while that worker is thinking**
- a status light per desk: grey → amber while busy → green on finish
- **work packets physically travel** the wires from the four researchers to the
  Architect, then from the Architect to the Red team
- a **treasury bar that drains** $7.00 → $0.00 as coins fly out and land, each
  desk rimming gold as it is paid

The screen flicker is deterministic — a hash of the frame index, not randomness —
so the render stays reproducible.

## Gate 5

Identical source to HS-032 and the same traceability. The choreography encodes
the real dependency graph: four parallel reads with no dependency on each other,
one synthesis that waits on all four, one review of that synthesis. Nothing on
screen asserts a figure that is not in
`../PILOT-10/capture/run-2026-08-27.md`.

**Not claimed:** that the product's own UI looks like this. It is a
visualisation of a real run, not a screen recording, and it shows no Handsel
chrome that could be mistaken for one.

## Why hook 4, and why that is fine

"This is an A.I. company" is a slower opening than HS-031's "four of them could
not afford to start." It buys the slowness back immediately — by 5s four screens
are flickering at once, which is a thing no other cut in the library can do.

Ranked for a cold audience: **HS-032 leads on clarity, HS-034 leads on
watchability.** They are the same story and the natural A/B — same run, same
facts, one told in cards and one told as a place. That is a genuinely
single-variable experiment, which is rarer than it sounds.

## Two layout bugs caught on the render

1. **Wires were invisible.** Drawn at `DIM` they read as smudges at phone scale,
   so packets appeared to drift through empty space. Raised to a dedicated
   `WIRE` tone and 4px.
2. **The end card stacked into the caption band.** `$7.00` at 140pt runs to
   ~1470 and captions live at 1500, so the URL sat underneath the caption. The
   URL now uses the caption slot as its own final beat instead of stacking a
   third line.

Both were invisible in the source and obvious in one extracted frame — L-02
again.

## Weaknesses accepted

- **Native 4.** Still no music bed. This is the cut that would benefit most: a
  floor with 14 SFX cues and no bed has audible gaps between events.
- Render is ~2 min for 37s, roughly double the card-based cuts. Acceptable, but
  the floor is not free.
