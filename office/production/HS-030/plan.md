# HS-030 — "Don't trust the score. Inspect the proof."

**Pillar E** · **Priority 67** · **Posture: SHIPPED** · **Status: scripted, not produced**
Format: negative-imperative practica (numbered) · Target: 42s · 1080×1920 · Platforms: YouTube Shorts → TikTok → Reels

## Grounding

Incident I-01 (live queries, 2026-08-27): one job, three surfaces, three
readings — `my_work` → `FAILED`; `get_job` → `Completed (done and paid)`;
`get_work_proof` → `No proof recorded`. On our own account.
EIP-712-signed proofs at `/proof/<id>` are SHIPPED (model file §4/§6).

Audience evidence (sweep 2026-08-31): the negative-imperative + count hook is a
proven pattern in this niche ("Don't use Claude Code unless you've installed
these five plugins" — 592K plays), and AI-trust/verification is the sweep's
identified content gap (51K-view video carrying 1,036 comments, nobody serving
it in short-form).

## Hypothesis

A practica-format video (the niche's tool-tip genre) whose "tool" is a
verification habit will ride existing search/format demand while landing the
Office's core thesis. One variable: practica framing vs. HS-011's conceptual framing.

## Hook

**Selected:** *"Don't trust an AI agent's status report until you've checked
three surfaces."*
Variants and reasoning: `../../memory/hooks.md` (HS-030 section).

## Script — 42s

| t | On screen | Audio (NARRATOR) | Caption (burned) |
|---|---|---|---|
| 0.0–3.5 | terminal, a one-word status glowing: `FAILED` | "Don't trust an AI agent's status report until you've checked three surfaces." | `one word is not a verdict` |
| 3.5–9.5 | `my_work` capture, the row highlighted | "Surface one: the worker's own history. This job of ours says FAILED. Case closed?" | `1 · the worker's story` |
| 9.5–16.0 | `get_job` capture on the same job | "Surface two: the market's record of the same job — 'Completed. Done and paid.' Same job. Opposite word." | `2 · the market's story` |
| 16.0–22.5 | `get_work_proof`: "No proof recorded" | "Surface three: the signed proof. There isn't one. Three surfaces, three answers." | `3 · the proof — missing` |
| 22.5–29.0 | plain slate | "A missing proof is information. It means every word you just read was somebody's report — not evidence." | `a missing proof IS the finding` |
| 29.0–36.0 | `/proof/<id>` page of a job that HAS one: the signature block | "When the work did pass a grader, there's a cryptographically signed proof anyone can verify — without trusting the platform, or us." | `signed. checkable. not ours to edit.` |
| 36.0–42.0 | the three commands stacked on screen | "We found this mess on our own account. That's why the habit exists. Score is a claim. Proof is the evidence." | `don't trust the score. inspect the proof.` |

The turn is at **9.5s** (the contradiction) and the payoff at 22.5s ("a missing
proof is information"). The 36.0s beat keeps the candour register: the confusion
is ours, on screen, undisguised.

## Shot list

| # | Shot | Dur | Source | MUST CONTAIN |
|---|---|---|---|---|
| s01 | FAILED close-up | 3.5 | MCP capture | the single word, phone-legible |
| s02 | my_work row | 6.0 | MCP capture | job number + FAILED in one frame |
| s03 | get_job same job | 6.5 | MCP capture | **the same job number** + "Completed" |
| s04 | get_work_proof | 6.5 | MCP capture | "No proof recorded" verbatim |
| s05 | insight slate | 6.5 | title card | ≤8 words |
| s06 | a real proof page | 7.0 | browser capture | the signature block of a job that has one |
| s07 | three-command stack | 6.0 | title card | the three tool names, correct spelling |

## May NOT claim (from the ledger)

- That `FAILED` means a grader rejected the work — the whole point; the script
  never asserts what job #20's true state is, only that the surfaces disagree.
- Any Verification Lawbook code on a Handsel screen — typed verdicts are
  CONCEPT; this script deliberately uses only the three real, shipped surfaces.
- "Audited" / "secure" anywhere near the proof beat; "signed" and "verifiable"
  are the ledger-safe words.

## Captions/CTA

Caption: `Your agent's dashboard is a story. Here's how to check it.` CTA is a
save-driving practica CTA: "Save this before your agent handles real money."
Pinned comment: the three commands as copyable text + the /proof link format.
