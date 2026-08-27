# QC — HS-001

```
IDEA        HS-001 · "I gave an AI $5 and told it to hire someone"
RENDER      renders/final.mp4 · 0:30 · 1080x1920 · h264 · aac · 860K
AUDIO       mean -19.1 dB · peak -3.9 dB · no clipping
GATES       hook 5 · clarity 5 · pacing 4 · visual 4 · accuracy 5
            relevance 5 · retention 4 · cringe 5 · native 4      = 41/45
VERDICT     PASS
```

## Gate 5 — factual accuracy, checked line by line

Every string on screen is verbatim from the real `plan_delegation` response
`dlg-S711y4gs3O` (2026-08-27), logged in `_source/captured-2026-08-27.md`.

| On screen | Traced to |
|---|---|
| `total $5.00` | the call's stated budget |
| `write the explainer  $4.00` | subtask 1 price |
| `review the explainer  $1.00` | subtask 2 price |
| `a different agent. checks the first one.` | subtask 2's stated purpose |
| `Verdict is clearly APPROVE or REVISE` | subtask 2 acceptance criteria, verbatim |

**Not claimed anywhere in the cut:** that money moved, that anyone was paid,
that work was delivered, that the plan was executed. `plan_delegation` is free
and escrows nothing, so an on-screen marker — `real output · plan only · nothing
escrowed` — is held for the entire 30 seconds. It is not fine print; it is
legible at phone scale, and it is the reason this video can make its claim at all.

## Weaknesses accepted

- **Pacing 4.** 4.3s–9.4s is a low-information stretch (`planning...`) carried
  by narration alone. It survives because the line under it is the setup for
  the turn, but it is the first thing to cut if a 25s version is wanted.
- **Visual 4.** Text-on-black throughout. Legible and dev-native, not striking.
  The Penpot kit does not exist yet; when it does, this is the video to re-cut.
- **No music bed.** Narration over silence. Common and acceptable in dev
  explainer content, but untested for this account — see the note in
  `../HS-011/qc.md`.

## Not fixed, deliberately

The turn lands at 12.3s (the $1.00 reviewer row). That is late for a 30s cut and
a shorter setup would move it earlier — but the surprise only works once the
viewer has accepted "it wrote a plan" as the whole story. Moving it earlier
trades the payoff for the pace. Logged as a hypothesis, not a defect: a
faster-turn variant is a clean single-variable follow-up.
