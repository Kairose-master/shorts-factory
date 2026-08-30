# THEOLOGY RED TEAM — `ai-baptism`

Pass 1 · script v1.0 → v1.1 · verdict **PASS WITH REQUIRED FIXES (2)**

The red team is **not** a heresy detector. Its single job is to separate two
things the draft mixes: what the script *asserts as Christian doctrine* from what
it *uses as a philosophical device*. A thought experiment stated in the register
of a confession is the failure mode here, not an unusual opinion.

## Blocking conditions checked

| # | Blocking condition | Result |
|---|---|---|
| B1 | Incarnation described as divinity becoming finite | **HIT → RT-01** |
| B2 | AI personhood asserted | pass |
| B3 | AI baptism eligibility asserted (either direction) | pass |
| B4 | Relation treated as sufficient proof of personhood | pass (guard added, RT-04) |
| B5 | Mature personal profession assumed universal for baptism | **HIT → RT-02** |
| B6 | Thought experiment presented as doctrine | pass (markers added, RT-03/05) |
| B7 | AI asserted to receive salvation / the Spirit / baptism | pass |

---

## RT-01 — REQUIRED — SCENE 08

**Draft line**

> 무한한 하나님이 유한한 역사 속에서 특정한 좌표를 취하셨습니다.

**Why it fails.** The draft does the right thing two sentences earlier — it
explicitly denies that the divine nature became finite. Then this line undoes it.
"무한한 하나님이 … 좌표를 취하셨습니다" makes *God* the thing that acquires a
coordinate. A coordinate is a location in a bounded frame; a subject that takes
one is circumscribed by it. Read plainly, the sentence says the infinite became
locatable — which is exactly ABSOLUTE RULE 7. It also cuts against the classical
claim (the *extra Calvinisticum*, and Chalcedon's "without confusion, without
change") that the Son is not contained by the human nature assumed.

The draft labels it 비유. A metaphor label does not repair a metaphor whose
literal reading is the forbidden claim — it just makes the forbidden claim
deniable. The fix has to change what the metaphor *says*, not how it is framed.

**Replacement (shipped in v1.1)**

> 조금 철학적인 비유를 쓰자면 —
> 무한하신 하나님이 작아지신 것이 아니라,
> 유한한 역사 안의 바로 그 자리에서 우리를 만나셨다는 것입니다.

The subject of the finite verb is now the **meeting**, not the essence. It
denies the shrinking reading out loud rather than relying on the earlier
sentence to hold. And it keeps everything the episode actually needs from the
line — historical particularity, non-substitutability, a specific place — which
is what feeds SCENE 09 and SCENE 12.

**Also required:** the on-screen marker `※ 비유입니다 — 교리 정식이 아닙니다` holds in
the lower third for the entire metaphor, not as a flash.

---

## RT-02 — REQUIRED — new SCENE 05B

**What the draft assumes.** From SCENE 03 onward the episode runs on one
implicit premise: that the church's question about a baptismal candidate is
*"does this one credibly and personally believe?"* Ten years of behaviour, the
FAITH DETECTOR, "진짜 믿는다" — all of it is built on a credible-profession test.

That is a real and widely held position. It is not the only one. Traditions
practising infant baptism baptize candidates who cannot profess anything at all.
On the draft's framing, an infant fails every test the episode applies to the
AI — which should have been the tell that the framing was doing more work than
it was licensed to do.

**Why this is not merely a disclaimer.** Fixing it *makes the thesis stronger*.
Paedobaptist practice already refuses the checklist reading of baptism: it asks
who this particular one is, and inside whose covenant and community the act
happens — not what the candidate scores. That is the episode's own conclusion,
arriving one act early and from inside church practice rather than from
philosophy. Cutting it costs the argument its best corroboration.

**Shipped as** a 25-second scene between 05 and 06, descriptive only, adjudicating
nothing between traditions, ending on `세례는 공동체가 행하는 사건`.

---

## RT-03 — ADVISORY — SCENE 09

The Jesus-duplicate hypothetical is the episode's sharpest device and its most
misquotable twenty seconds. Christian theology does not hold that a duplicate of
the incarnate Son is possible — the hypostatic union is not a property list that
a second bearer could satisfy. The scene's payoff already says this. The risk is
a clip circulating without the payoff.

**Shipped:** an on-screen `사고실험` marker held for the whole scene, and the
never-render-the-face rule for the silhouette.

## RT-04 — ADVISORY — SCENE 10

The event-network beat replaces a scoring frame with a relational one, and could
be read as: *relation is what makes a person, so a sufficiently related AI is a
person.* The episode must not carry that. **Shipped:** every line in the beat is
interrogative, and a `[GUARD]` in the canonical script forbids resolving them in
any edit pass. Relation is offered as an *additional* axis of inquiry, never as
a sufficient condition.

## RT-05 — ADVISORY — SCENE 06

The duplication scenario is a device for probing numerical identity, not a
technical forecast. **Shipped:** a `[THOUGHT EXPERIMENT]` tag in the canonical
script, and the visual language stays editorial rather than sci-fi so the frame
does not read as prediction.

---

## What the red team explicitly did **not** do

- It did not adjudicate credobaptism vs. paedobaptism. RT-02 names that the
  traditions differ and stops.
- It did not decide whether an AI could be baptized. The episode's refusal to
  answer is the thesis, not an evasion, and the red team protects that refusal
  in both directions — a "clearly not" ending would fail QA exactly as a
  "clearly yes" ending would.
- It did not check the philosophy. Numerical identity, haecceity and the
  memory/participation distinction are `philosophy-script`'s territory.

## Verdict

`THEOLOGY_PASS` — conditional on RT-01 and RT-02 being present in the rendered
cut. Both are in v1.1. `subtitle-qc` re-checks the RT-01 replacement line
verbatim against the final narration; if the narrator paraphrases it back toward
"좌표를 취하셨습니다", the render fails QA.
