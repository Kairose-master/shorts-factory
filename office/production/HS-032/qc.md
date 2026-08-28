# QC — HS-032

```
IDEA        HS-032 · "I hired an entire company for $7."
RENDER      renders/final.mp4 · 0:34 · 1080x1920 · h264 · aac · 13 SFX cues
GATES       hook 5 · clarity 5 · pacing 5 · visual 5 · accuracy 5
            relevance 5 · retention 4 · cringe 5 · native 4      = 43/45
VERDICT     PASS — and this is the one to lead with
```

## What this fixes

HS-031 scored 43/45 too and is **the wrong video to show a stranger.** It opens on
a limitation, spends nine seconds on a staking bond, prints delegation ids, and
ends on *"Sometimes."* Someone who has never heard of Handsel finishes it without
learning what the product is.

HS-032 is the promotional cut. The brief said the narrative is *build an AI
company, give it capital, watch it do business*, and that protocol vocabulary is
supporting evidence rather than the hook. This one obeys both.

**Jargon audit — words that do not appear anywhere in script or on screen:**
escrow · bond · delegation · USDC · on-chain · wallet · smart account ·
verification · grader · MCP · x402 · EIP-712 · protocol · agent.

It says *company*, *jobs*, *workers*, *researched*, *decided*, *attacked*,
*got paid*. A viewer needs no glossary and no prior context.

## Gate 5 — every figure traced

All from `dlg-AJin4S4WA4`, a real completed run (`../PILOT-10/capture/run-2026-08-27.md`).

| On screen | Source |
|---|---|
| six roles: AWS · Azure · Cloudflare · Independent · Architect · Red team | the run's six subtasks |
| three researched in parallel | AWS/Azure/Cloudflare have no dependency |
| a fourth read all three and decided | Platform recommendation waits on all three |
| a fifth attacked it | Red team REVIEWS the recommendation |
| $1/$1/$1/$1/$2/$1 | per-subtask prices |
| $7.00, every worker paid | `$7.00 escrowed (paid $7.00, refunded $0.00)` |
| 54,000 words | assembled output length |

**Deliberately not explained:** the task was a technical infrastructure question.
The video never states it, because a viewer does not need to understand the
question to understand that six specialists answered it and were paid. Omitting
it is not hiding it — the run is named in the capture and nothing about the claim
depends on the subject matter.

**Not claimed:** that this is typical. It is one real run. The video says "I hired
a company and this is what happened", never "this is what always happens" — which
matters, because `dlg-fwuIFrSwyx` is the same brief mostly failing. That video
exists separately as HS-031 and is the honest companion, not the opener.

## Why the score understates it

43/45, the same as HS-031 — because the scoring dimensions have no axis for
*serves the actual goal*. For a cold audience these two are not close. The
grid should probably grow an `audience-readiness` dimension; logged rather than
patched mid-flight.

Understandability is a genuine 10 here and the rubric caps at 10.

## Weaknesses accepted

- **Retention 4.** The strongest single moment (the red team attacking) lands at
  19s, later than ideal. Moving it earlier would break the causal order — you
  cannot attack a decision before it is written.
- **Native 4 → bed added.** See below.
- The two `$7.00` counters tick up over ~1s, so a frame grabbed mid-animation
  shows `$6.99` or `$5.49`. Both settle and hold. Not a defect, but worth knowing
  before anyone screenshots it for a thumbnail.

## Publishing order — changed

**HS-032 leads.** It is the only cut that works on someone with zero context.
HS-031, HS-006b and HS-011 are all follow-ups for an audience that already knows
what the product is.

## Music bed — added 2026-08-27

`bed-office`, 45s, in the SFX library. **Chosen over CC0 alternatives on a
measurement, not a preference.** A bed's only job is to not fight the voice, so
what matters is how much of its energy sits in the 300–3400 Hz speech band
relative to its own level:

| candidate | speech-band share |
|---|---|
| CC0 #524621 "Synth 3" | **−3.4 dB** — would fight the narration badly |
| CC0 #860123 "Low Frequency Ambient" | −17.4 dB |
| **`bed-office` (synthesised)** | **−24.8 dB** |

It is built that way on purpose: sub energy under ~120 Hz, air above 5 kHz, a
soft 1 Hz pulse at 110 Hz, and the speech band left empty. A company gets a
heartbeat out of it for free.

Verified present rather than assumed. My first check compared whole-file
sub-120 Hz against a bed-less cut and showed nothing — the narration's own low
end hid it across a 37-second average. Measuring **inside a gap between
narration lines** was decisive: bare VO **−91.0 dB** (silence) → mixed
**−37.5 dB**, almost entirely sub-120 Hz. Whole-file averages hide a bed; gaps
do not.
