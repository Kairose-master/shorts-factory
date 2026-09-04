# HS-AD3 — QC record: five independent reviews, not delivery-authorized

The `motion-graphics` gate requires an INDEPENDENT critic (a clean subagent
that inspects the actual media, not the builder's account of it) to score eight
axes; delivery needs every axis ≥8 and an average ≥8.5. Five versions were
built and five reviews run. **None reached the bar.** No version was delivered
as authorized, and none is approved to publish.

Recording this in full because the Office's standing rule is to log the
rejects, and because the pattern across five reviews is the actual finding.

## What every review agreed on — the clip is real

| Axis | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| research_fidelity | 9 | 7 | 9 | 7 | **9** |
| product_authenticity | 9 | 8 | 9 | 7 | **9** |
| material_restraint | 8 | 8 | 8 | 8 | **9** |
| concept_specificity | 7 | 8 | 9 | 8 | **8** |
| reference_fidelity | 3 | 3 | 7 | 6 | 5 |
| composition | 5 | 3 | 7 | 5 | 4 |
| motion_causality | 3 | 4 | 7 | 5 | 4 |
| mobile_readability | 8 | 4 | 8 | 4 | **3** |

Verified by the round-5 critic against the sources, by measurement rather than
assertion: beat 1 is pixel-identical to the office screen recording (mean RGB
delta 1.31, one pixel above threshold — codec noise); beat 2 matches the
captured certificate row for row; every on-screen value traces to job #30. It
found **no invented metric, verdict, name, surface or effect anywhere**, and no
neon, glow, bloom, gradient wash or glassmorphism.

## What it never fixed, and why

Two defects survived every rewrite, and they are properties of the material
rather than of the edit:

1. **No dominant value.** The reference mechanism earns its motion by returning
   to the same product cards and showing `98 / 97 / 96` become `42 / 39 / 36` —
   one huge changing number per hold. Handsel's proof surfaces are legal-style
   documents: a certificate table and a JSON body, every character the same
   size by design. `"verdict":"pass"` cannot be made larger than the signature
   beside it without either cropping the line or annotating it — and annotating
   an already-settled value is exactly what got v1 rejected as "a static object
   with rows appearing".
2. **The product's own detail card is 8px tall.** It is the line that ties the
   clicked agent to the certificate, and at 1080 wide the product renders it at
   8px cap height. Enlarging it enough to read (≈3.7x) crops the sentence in
   half. v4 tried a punch-in; the round-5 critic measured the card identical
   across frames 45-98 and called the punch-in nonexistent — correctly, because
   the office camera behind it scaled while the card is a fixed screen-space
   HUD element.

Under the honesty rules there was no legitimate way through: the page has no
hover state (captured hovered and unhovered — identical to the pixel), so the
press cannot be given a product response without inventing UI, and no value can
be emphasised without annotating a state that was never unresolved.

## What was fixed along the way

- v1 → v2: dropped the brackets over already-resolved rows (the banned
  "static object + rows appearing" pattern).
- v2 → v3: stopped laying pages on a charcoal ground; captured them full-bleed
  at phone proportions so the frame is edge-to-edge product. Added the real
  office recording. Both of v2's hard failures cleared.
- v3 → v4: cut the office beat to open in motion; removed the unevidenced
  "BOUNTY $1 USDC · PAID" headline (neither page displays a payment); hid the
  Next.js dev badge that was occluding the outcome line.
- v4 → v5: removed the bottom URL strip that read as fabricated browser chrome
  for a page it was not the address of; gave beat 2 a real camera move from the
  certificate's own verified banner out to the record.

## Verdict

`hsad3-v5-draft.mp4` (10.5s, 1080x1920) is factually clean and usable as a hero
insert in front of an existing cut. It is **not** gate-authorized and is
**not** approved to publish. Publishing anything from this Office still needs
explicit human approval, separately.

Full evidence in `evidence/`: the research brief, the reference observations,
the render brief and the round-5 critic JSON.
