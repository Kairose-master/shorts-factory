# Lessons Learned

**A lesson requires evidence.** No linked experiment → it is an opinion; store it
marked `speculative` and never let it override an evidenced lesson.

## Row format

```
ID          L-001
Lesson      stated as an actionable rule
Evidence    link to experiments.md — REQUIRED
Confidence  speculative | directional | established
Supersedes  link to a previous lesson, if any
Date        
```

`established` requires **two or more independent observations** pointing the same
way. One observation is a note.

---

## Priors — carried in from outside, not yet tested here

These are `speculative` by definition: they come from the installed skills and
from the Handsel repo, not from this Office's own published results. They are
written down so cycle 1 can **falsify** them rather than quietly assume them.

| ID | Prior | Source | Confidence |
|---|---|---|---|
| P-01 | A flat literal statement out-hooks a question for a cold dev audience | `viral-hooks` archetypes | speculative |
| P-02 | Showing the failure path builds more trust with developers than the happy path | product intuition + audience-signal-2026-08-27 (the highest-discussion thread in a 30-day sweep is an agent-failure confession) — **EXP-001 still tests it** | **directional** |
| P-03 | Burned-in captions are mandatory; most viewing is muted | `viral-captions-and-ctas` | directional |
| P-04 | Synthetic-realistic avatar voices read as cringe to a dev audience; deliberately robotic ones do not | `voicebox` casting notes | speculative |
| P-05 | The honesty assets (`/market-health`, `failure-modes.md`) are a distribution advantage, not a liability | positioning judgement | speculative |
| P-06 | Handsel's education content compounds: explainers make every demo legible | pillar design | speculative |

**P-02 and P-05 are the two worth being wrong about.** Both are bets that
candour outperforms polish. If cycle 1 falsifies them, the Office's whole tone
needs rethinking — which is exactly why they are written down before publishing
rather than after.

---

## Cycle 1 — production lessons (process, not audience)

These come from making the videos, not from publishing them, so they are about
the Office's own machinery. They are `established` because each was observed
directly and fixed, not inferred from metrics.

| ID | Lesson | Evidence | Confidence |
|---|---|---|---|
| L-01 | QC the **render**, never the source. The red wash in HS-006 was painted over the three passing rows — invisible in the code, obvious in one extracted frame. | HS-006/qc.md | established |
| L-02 | Extract a contact sheet of 5–7 frames before accepting any render. Every layout defect found in cycle 1 was found this way and none was found by reading the build script. | all three qc.md | established |
| L-03 | Pad the narration track to full runtime. FFmpeg's `-shortest` silently truncates the video to the last spoken word and the closing beat disappears without an error. | HS-011/qc.md | established |
| L-04 | Measure the gap between boxes before trusting an arrow. A 42px arrow is invisible at phone scale even though it is plainly there in the source. | HS-011/qc.md | established |
| L-05 | Monospace does not wrap. Any mono line over ~48 characters at 36px runs past the right safe edge and clips mid-word. | HS-001/qc.md | established |
| L-06 | The real data was better than the planned script. HS-006 was written around a staged failure; a real one already existed in `my_work`, and a real failure is the only kind that proves anything about a grader. **Check what actually happened before inventing what should happen.** | _source/captured-2026-08-27.md | established |

**L-06 is the one that generalises beyond video.** The Office's instinct was to
construct a demonstration. The account's own history already contained a better,
truer one. Look first.

---

## Cycle 1 addendum — the first audience-grounded lesson

| ID | Lesson | Evidence | Confidence |
|---|---|---|---|
| L-07 | **The Office's backlog was generated from the product, not the audience — and it showed.** A 30-day sweep of Reddit and HN surfaced a framing (agent debt and failure) that outranks the invented top idea's framing (agent success), on the same theme, with the same audience. Generate from evidence first, product second. | research/audience-signal-2026-08-27.md; HS-021 vs HS-001 | directional |

**Why only `directional`:** one sweep, 23 items, two sources, and GitHub failed
during it. It is one pointer, not two. It becomes `established` if a second
monthly sweep says the same thing — which is exactly the discipline
`analytics-loop.md` demands of every other claim, and the Office does not get to
exempt a lesson about itself.

This is also the first time a prior moved on outside evidence rather than the
Office's own opinion: **P-02 goes speculative → directional.**

---

## Cycle 1, second addendum — the Lawbook correction

| ID | Lesson | Evidence | Confidence |
|---|---|---|---|
| L-08 | **Tracing a claim to a source is not verifying it.** HS-006 scored 42/45 on QC because its central claim traced cleanly to a surface I had already read — and that surface did not mean what I assumed. Where a claim rests on a system's own status string, query a second and third surface before publishing. | production/HS-006/qc-correction-2026-08-27.md | **established** |
| L-09 | **Never publish an untyped verdict.** One word that collapses outcome, cause, attribution and settlement is not a verdict, it is a guess wearing a verdict's clothes. This is the Lawbook's whole thesis and the Office broke it in a video *about verification*. | research/verification-lawbook.md; the same correction | **established** |
| L-10 | **A missing glyph ships silently.** Pillow does not raise, and `font.getmask(ch).getbbox()` is truthy even for tofu, because the tofu box is itself drawn — so my first check was worthless. Only the font's cmap is authoritative. `✓` and `↳` are absent from every font in the kit. The render engine now refuses to start when any element's text would draw tofu. | _engine/render.py `check_glyphs`; HS-006b's first cut | **established** |

**L-08 and L-09 are `established` on one observation each**, which the Office's
own bar normally forbids. The exception is deliberate and narrow: these are not
claims about how audiences behave, where one observation really is a coincidence.
They are a demonstrated defect in a process, reproduced and fixed. A process bug
you have seen once and understood is not a sample of size one.

**The uncomfortable part.** The document that caught this arrived from outside the
Office. Nothing in the Office's own QC would have found it — the gate was passed,
the claim was sourced, the video was scored highest of the three. What found it
was someone handing over a framework built specifically to name this failure mode.
That is worth remembering the next time the Office reports a clean QC pass.
