# QC — HS-024 draft 2 (hs024-draft2.mp4)

```
IDEA        HS-024 · "$100 on the internet. Try to take it."
RENDER      renders/hs024-draft2.mp4 · 0:49.5 · 1080x1920 · h264 · aac · 12.3MB
AUDIO       mean -20.3 dB · peak -4.5 dB · no clipping · narration loudnorm I=-16
METHOD      contact sheet, 6 frames (L-02) · draft-1 rejected on 3 defects
VERDICT     DRAFT PASS — awaiting human approval; publishing NOT authorized
```

## Draft-1 defects found by frame extraction (all fixed in draft 2)

1. Captions rendered with no inter-word spaces — trailing space inside an
   inline-block span does not render; separator moved between spans
   (CaptionOverlay.tsx local patch).
2. Terminal scenes empty — `typeSpeed` is seconds-per-char; props passed
   chars-per-sec (18 → ~162s of typing). Props corrected to 0.045–0.05.
3. Hook frame weak — light-mode homepage screenshot under a small green
   overlay; replaced with a bold `$100` stat card matching the reference's
   bold-text first frame.

## Gate 5 — factual accuracy, line by line

| On screen | Traced to |
|---|---|
| "OPEN CHALLENGE - $100 escrow, deliberately locked" | `get_job 2` title, live query 2026-08-31 |
| "This job is not work." / "Take it and it is yours - no claim form, no adjudication." | sealed task text, same query |
| "status: Refunded (refunded to the requester)" | `get_job 2` status field, verbatim |
| job #3 · Refunded | `get_job 3`, live query 2026-08-31 (second window closed) |
| "not audited. … amounts you would shrug at." | DO NOT CLAIM ledger / repo's own docs |
| /live dashboard zeros | real page capture, 2026-08-31 (cold start shown, not hidden) |

Not claimed anywhere: security, audit, traction, a third run.

## Known limitations (acceptable for draft, revisit before approval)

- Narration is Gemini TTS (Charon); Typecast swap possible once integrated.
- Music is a synthesized ambient bed, deliberately at −16 dB under narration.
- Section-title overlay at ~41s slightly overlaps the page headline.
- Reference format (milesreevesai) followed for pacing/captions; no talking head
  (Office rule: no synthetic presenter).
