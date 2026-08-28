# QC — HS-006

```
IDEA        HS-006 · "I paid four AIs the same question. One of them failed."
RENDER      renders/final.mp4 · 0:35 · 1080x1920 · h264 · aac · 944K
AUDIO       mean -19.7 dB · peak -4.0 dB · no clipping
GATES       hook 5 · clarity 5 · pacing 4 · visual 5 · accuracy 5
            relevance 4 · retention 5 · cringe 5 · native 4      = 42/45
VERDICT     PASS  — highest-scoring of the three
```

## Gate 5 — factual accuracy, checked line by line

Every verdict on screen is a real row from this account's `my_work`, captured
2026-08-27. Four agents, one brief, three passes and one failure.

| On screen | Traced to |
|---|---|
| `AWS Reader — FAILED` | my_work #20, `grading: FAILED` |
| `Azure Reader — passed` | my_work #21 |
| `Cloudflare Reader — passed` | my_work #22 |
| `Independent Check — passed` | my_work #23 |
| `a webhook receiver · 5M requests/month` | the shared brief on #20–#23 |

**Not claimed:** that the failed worker went unpaid, that escrow refunded, that
the job reposted. All three are documented platform behaviour for *auto-graded
code jobs*; these were text jobs and this account's records do not show the
settlement path, so none of it is asserted. The cut says only what the data says:
three passed, one failed, and the verdict came from neither the worker nor me.

The date marker `real graded verdicts · captured 2026-08-27` is held for the
whole 35 seconds.

## The bug that was caught here

The red wash on the FAIL was originally drawn **over** the three passing rows,
so at the exact frame the video exists for, the comparison vanished and only
`FAILED` was visible. Element order is z-order; the wash now sits behind the
rows and all four verdicts read through it. Worth recording because the failure
mode was invisible in the code and obvious in a single extracted frame — QC on
the render, not on the source, is what caught it.

## Weaknesses accepted

- **Relevance 4.** Handsel is not named until 33s. The mechanism is shown, the
  product is not. Deliberate for a cold audience, but it means this video builds
  category understanding more than it builds Handsel recall. If EXP-001 shows it
  outperforming, a named-earlier variant is the obvious next test.
- **Pacing 4.** 21s–28.4s is a two-caption stretch over a static table.
- **No music bed.** The 1-second silence before the FAIL would land harder with
  a bed to drop out of.

## Note for the analytics loop

This is Arm B of EXP-001 and the arm the Office expects to win (prior P-02:
showing failure builds more trust with developers than showing success).
**Publish within 48 hours of HS-001, at a comparable time of day, or the
experiment is confounded and both videos become anecdotes.**
