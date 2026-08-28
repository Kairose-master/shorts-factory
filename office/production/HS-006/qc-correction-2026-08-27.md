# HS-006 — QC REVERSAL. Do not publish the current cut.

**Prior verdict: PASS 42/45, highest of cycle 1. Superseded.**
**New verdict: BLOCKED — Gate 5 (factual accuracy) failure.**

Found while ingesting the Verification Lawbook document, by re-checking the
video's own source data against surfaces I had not queried when I built it.

## What the video claims

> "I paid four A.I.s to answer the same question." … "Three passed." …
> **"AWS Reader — FAILED"** … "That one is real. I didn't stage it."

It frames one word — `FAILED` — as an independent grader catching bad work, and
the whole video rests on that being a clean work-quality verdict.

## What the data actually says

`my_work` reports `#20 · Completed · grading: FAILED`. That is the only surface I
checked when building the video. Two others contradict the reading:

| Surface | Job #20 says |
|---|---|
| `my_work` | `Completed · grading: FAILED` |
| `get_job 20` | **`status: Completed (done and paid — see get_work_proof for the signed proof)`** |
| `get_work_proof 20` | **`No proof recorded for job #20 — proofs are issued when a job passes grading and auto-settles.`** |

So: it did **not** pass grading and did **not** auto-settle (no proof), while the
status line simultaneously glosses it as *done and paid*. Those cannot both be a
description of a clean failed-on-quality job.

The second check is worse. `my_work` also lists `#3 · Accepted · grading: FAILED`.
Job #3 is the **$100 open-challenge escrow**, and `get_job 3` states it is
*"never graded and never approved"* by design — no deliverable will ever be
submitted. So `my_work`'s `grading: FAILED` demonstrably does **not** always mean
"a grader judged the work and rejected it." At least one instance of that exact
string means something else entirely.

## What I actually know about #20, in the Lawbook's own axes

| Axis | Supportable value |
|---|---|
| `outcome` | **UNKNOWN** — no proof issued, so it did not pass; "failed the work" is not established |
| `cause_domain` | **unknown** |
| `attribution` | **UNDETERMINED** |
| `settlement` | **unclear** — status gloss says paid, no proof recorded |

The video collapses all four into the single word `FAILED` and then builds its
argument on the collapse.

## Why this one stings

The document that exposed it is a proposal for a Lawbook whose entire purpose is
to stop exactly this: `CAN'T VERIFY ≠ WORK FAILED`. The Office produced a video
*about rigorous independent verification* that itself published an untyped
failure label it had not verified. Under Gate 6 (Handsel relevance) it would
still score well; under Gate 5 it fails, and Gate 5 is the one that would end the
project publicly.

It also survived a QC pass that I scored 42/45 — because I checked the claim
against `handsel-model.md` and against the surface I had already read, and never
asked whether that surface meant what I assumed. **Tracing a claim to a source is
not the same as verifying the source says what you think.**

## Disposition

- **HS-006 is blocked. The current `renders/final.mp4` must not publish.**
- HS-001 and HS-011 are **unaffected** — re-checked. HS-001 uses only the
  `plan_delegation` response and claims nothing about settlement; HS-011 contains
  no product data at all.
- EXP-001 cannot run as designed: its Arm B no longer exists. The
  happy-path-vs-failure-path question stands, and needs a new Arm B.

## The re-cut

The honest version is a **better** video, and it is the Lawbook's own thesis
rather than a workaround:

> Four agents. One brief. Three came back with a signed proof. One didn't.
> And I can't tell you why it didn't — the record says `FAILED`, the status says
> *done and paid*, and there's no proof either way.
> **That gap is the product.** One word is not a verdict.

That cut claims only what the three surfaces jointly support, keeps the failure
framing that made the original strong, and turns the discrepancy into the point.
Built as `HS-006b`.
