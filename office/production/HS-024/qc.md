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

---

# QC — HS-024 v2 (hs024-v2.mp4) · 2026-08-31

```
RENDER      renders/hs024-v2.mp4 · 0:49.5 · 1080x1920 · h264 · aac · 23.2MB
AUDIO       mean -20.3 dB · peak -4.5 dB (unchanged narration/music)
METHOD      9-frame contact sheet + hook-frame recheck after one fix
VERDICT     DRAFT PASS — awaiting human approval; publishing NOT authorized
```

## What changed vs draft 2, and the evidence behind each change

Reference set grew to 4 downloaded viral videos (milesreevesai 592K,
sophia.designsthings 541K, alyvibecodes 280K — TikTok; amigoscode top reel —
Instagram, via a fresh Apify reel pull). Gemini format teardown of the two
new ones agreed on the #1 native-feel factor: **handheld phone footage of a
physical screen** (glare, drift, reflections), not clean digital captures.

1. Static screenshots replaced with REAL screen recordings of the live
   product (Playwright video through the local bridge): home scroll with the
   dark office diorama and the honest "AGENTS ON THE PLATFORM: n/a" stats,
   and the /live dashboard with its real zeros.
2. Handheld phone-cam treatment applied in post (2-axis sway, ±0.6°
   breathing rotation, soft glare, fine grain, vignette) — directly encoding
   the references' top authenticity signal.
3. Captions reformatted to the reference grammar: 3 words per page,
   lowercase (numerals/$ kept), bottom-third pill, word-by-word highlight.
4. Hook rebuilt as a top-left persistent banner ("$100. steal it, it's
   yours.") over footage — the alyvibecodes hook pattern; the v2-draft-1
   center hero overlay read as a watermark and was rejected on the contact
   sheet.

## Unchanged and still true

Factual chain identical to draft 2 (all on-screen strings from live
`get_job` queries 2026-08-31; not-audited candour beat intact; no traction
claims — the n/a and zero stats on screen are the honest state, shown on
purpose).
