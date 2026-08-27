# QC — HS-011

```
IDEA        HS-011 · "An AI grading its own homework is not a reputation"
RENDER      renders/final.mp4 · 0:35 · 1080x1920 · h264 · aac · 1.0M
AUDIO       mean -19.0 dB · peak -4.0 dB · no clipping
GATES       hook 4 · clarity 5 · pacing 4 · visual 4 · accuracy 5
            relevance 4 · retention 4 · cringe 5 · native 4      = 39/45
VERDICT     PASS
```

## Gate 5 — factual accuracy

No product data appears in this video at all, by design. The two factual claims:

| On screen / spoken | Traced to |
|---|---|
| "confidently wrong looks exactly like right" | `handsel-model.md` §2, quoted from the repo |
| "the answer is generated with the problem; the solver never sees it" | §4, Proving Ground |

`98 / 100` is illustrative of *any* self-reported score and is captioned "a claim
about a claim". It is not attributed to Handsel and is not a Handsel number.

**Deliberately cut:** the four grader modalities, evidence classes E0–E4, and
everything about credit. All true, all one idea too many for 35 seconds. Evidence
classes are HS-012; credit is HS-014.

## The composition fixes QC forced

1. **The detach arrow was 42px long** and invisible at phone scale — the single
   beat the whole video turns on did not read. Boxes were separated and
   narrowed; the arrow is now unmistakable.
2. **The self-grading loop was still on screen** during the "so you check all of
   it" beat, competing with the accumulating rows. The loop now retires when the
   aphorism lands, so the checking beat owns the frame.
3. **The render was truncated to 32.7s** because FFmpeg's `-shortest` cut the
   video to the last spoken word, losing the closing beat. The narration track is
   now `apad`-ed to full runtime. Fixed in the shared engine, so it cannot recur.

## Weaknesses accepted

- **Hook 4.** The opening visual is a box drawing itself — modest movement for
  the first 400ms, where the standing rule is *movement inside 500ms*. The line
  carries it; the frame does not help much. Lowest hook score of the three.
- **Relevance 4.** Handsel appears only on the end card. This is the compounding
  video — it makes the other two legible — but on its own it markets the
  *category*, not the product.
- **Visual 4.** Minimal by choice: a video arguing for verifiable process should
  not be made of unverifiable generated imagery. That choice costs visual
  richness and it is the right trade.

## Open item across all three — no music bed

None of the three renders has a music bed; narration sits over silence. This is
common and defensible in dev-explainer short-form, and it is **untested for this
account**. It is logged as an open production question, not scored as a defect —
adding a bed is one line in the engine once there is a reason to think it helps.
