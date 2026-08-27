# SOP — Quality control

QC runs **after render, before packaging**. QC's verdict is written to
`office/production/<id>/qc.md` whether it passes or fails. A rejected render is
logged in `office/memory/rejected.md` with the reason in plain words.

**QC never publishes and never renders.** Its only power is the veto, and the
veto is absolute.

## The nine gates

Score each 0–5. **Any gate below 3 blocks.** Total below 30/45 blocks.

| # | Gate | Fails when |
|---|---|---|
| 1 | **Hook** | the first 1–2s could be skipped without losing anything; it opens with "Hi guys" / "Today I'll explain" / a logo |
| 2 | **Clarity** | a viewer who has never heard of Handsel cannot say what happened |
| 3 | **Pacing** | any shot holds past its information; dead air before 0:03 |
| 4 | **Visual quality** | upscaled assets, mismatched fonts, captions under the platform UI, text outside safe area |
| 5 | **Factual accuracy** | any claim not traceable to `research/handsel-model.md`, or anything in the DO NOT CLAIM ledger |
| 6 | **Handsel relevance** | the video would work identically for any other product |
| 7 | **Retention risk** | the payoff arrives after the average drop-off; the interesting part is at the end |
| 8 | **Cringe risk** | see below |
| 9 | **Platform nativeness** | reads as an ad; wrong aspect; visible watermark from another platform; caption written for the wrong platform |

## Gate 5 is checked line by line

Read the script against `research/handsel-model.md`. For every factual sentence,
name the source line. No source, no sentence. This is the gate that would end the
project if it failed publicly — a project whose entire thesis is *independent
verification* cannot ship an unverified claim about itself.

## Gate 8 — cringe, for a developer audience specifically

Automatic fail:

- A synthetic avatar presenting as a person.
- "Web3", "revolutionary", "game-changing", "the future of X", rocket emoji.
- Money-flex framing. Handsel moves $1–$5 bounties; implying riches is both false
  and repellent to the audience that would actually use it.
- Fake urgency, fake scarcity, fake countdowns.
- A meme format more than ~3 weeks past peak (check `trend-radar`).
- AI-generated humans with hand or eye artifacts, at any duration.
- Explaining a joke on screen.

Developers forgive rough production. They do not forgive being sold to.

## Verdict format

```
IDEA        HS-000
RENDER      renders/final.mp4  (0:31, 1080x1920)
GATES       hook 4 · clarity 5 · pacing 3 · visual 4 · accuracy 5
            relevance 5 · retention 3 · cringe 5 · native 4    = 38/45
VERDICT     PASS | REVISE | REJECT
BLOCKERS    <gate, what specifically, timecode>
NOTES       <what to keep if this is re-cut>
```

`REVISE` names the specific fix and returns to the owning role. `REJECT` retires
the concept and writes to `memory/rejected.md` — including what was worth keeping,
because a rejected video usually contains one good shot or one good line.
