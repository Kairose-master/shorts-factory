---
name: theology-red-team
description: Separate what a script asserts as Christian doctrine from what it uses as philosophical analogy or thought experiment, and block production when the two collapse. Use before producing any video touching Christian theology — incarnation, baptism, salvation, personhood — or when checking whether a metaphor's literal reading commits a claim the script does not intend. Not a heresy detector; it adjudicates nothing between traditions.
---

# theology-red-team

**This is not a heresy detector.** It does not decide who is right. It does one
thing: separate what the script *asserts as doctrine* from what it *uses as a
device*, and stop production when those two registers collapse into each other.

The failure mode is almost never an unusual opinion. It is a thought experiment
stated in the grammar of a confession — where the script did not intend a claim,
and a viewer has no way to tell.

## Run order

1. **Split every claim.** Tag each sentence:
   `[THEOLOGY]` · `[PHILOSOPHY]` · `[THOUGHT EXPERIMENT]` · `[RHETORIC]` ·
   `[OPEN QUESTION]`. Emit `script/claim-map.json`.
2. **Read each `[THEOLOGY]` line literally.** Not charitably — literally. What
   does the sentence commit to if a viewer takes it at face value?
3. **Read each metaphor literally too.** This is the step most reviews skip.
4. **Check the blocking conditions.**
5. **Emit** `script/theology-redteam.md` with a verdict and required fixes.

## Blocking conditions

Production stops until each is cleared.

| # | Condition |
|---|---|
| **B1** | The incarnation is described as divinity *becoming* finite |
| **B2** | AI personhood is asserted |
| **B3** | Baptism eligibility for AI is asserted — **in either direction** |
| **B4** | Relation is treated as sufficient proof of personhood |
| **B5** | Mature personal profession is assumed to be a universal baptismal condition |
| **B6** | A thought experiment is presented in the register of doctrine |
| **B7** | AI is asserted to receive salvation, the Spirit, or baptism |

### B1 — the incarnation

Say: *the Son assumed human nature and entered concrete human history.*
Never say: *the divine nature became finite / shrank / was contained.*

A "specific coordinates" style metaphor is where this usually breaks. Watch the
grammatical subject: if **God** is what takes on a bounded location, the sentence
circumscribes the divine nature no matter what disclaimer surrounds it. Move the
finite verb onto the *meeting*, the *action*, or the *history*, and the metaphor
keeps everything the essay needs — particularity, non-substitutability, a
specific place — while dropping the claim it did not intend.

Relevant background: Chalcedon's "without confusion, without change"; the
*extra Calvinisticum*. The script does not have to cite either. It has to not
contradict them accidentally.

### B3 — both directions

A confident "of course not" fails this gate exactly as a confident "yes" does.
If the episode's thesis is that the question is premature, an ending that leans
either way is a content failure, not a safety improvement.

### B5 — baptismal conditions

Traditions differ. Some require a credible personal profession; traditions
practising infant baptism baptize candidates who cannot profess anything. A
script that silently assumes the first has narrowed Christianity to one wing
without noticing — and its whole argument runs on that assumption.

Test: **would an infant pass the test this script applies?** If not, and the
script does not acknowledge that, B5 is hit.

Fixing it is usually not a disclaimer. Paedobaptist practice already refuses a
checklist reading of baptism — it asks who this one is and inside whose covenant
the act happens. For an essay arguing that identity and history matter more than
attribute scores, that is corroboration from inside church practice. Add the
beat; do not adjudicate between the traditions.

## A metaphor label does not repair a metaphor

If the literal reading of an analogy is a forbidden claim, `※ 비유입니다` does not
fix it — it makes the claim deniable while still making it. **Change what the
metaphor says.** Then hold the label on screen for the metaphor's full duration;
a flashed disclaimer is not a disclaimer.

## Verdict

Emit one of:

- `THEOLOGY_PASS`
- `THEOLOGY_PASS WITH REQUIRED FIXES (n)` — production continues only once the
  fixes are in the script *and* the rendered cut
- `THEOLOGY_BLOCK` — a blocking condition with no fix the script will accept

Required fixes carry through to `subtitle-qc`, which compares them **verbatim**
against final narration. A narrator paraphrasing a required line back toward the
original wording fails the render.

## Explicitly out of scope

- Adjudicating between traditions. Name that they differ; stop.
- Deciding the episode's question. If refusing to answer is the thesis, protect
  the refusal in both directions.
- The philosophy. Numerical identity, haecceity, the memory/participation
  distinction — that is `philosophy-script`'s territory, and a theology review
  that wanders into it will start rewriting arguments it was not asked to judge.
