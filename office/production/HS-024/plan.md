# HS-024 — "$100 on the internet. Try to take it."

**Pillar C** · **Priority 76 (top of backlog)** · **Posture: SHIPPED** · **Status: scripted, not produced**
Format: screen-demo + stakes narration · Target: 38s · 1080×1920 · Platforms: TikTok → YouTube Shorts → Reels

## Grounding (checked 2026-08-31, this session)

`get_job 2`: status **Refunded** — 30-day open challenge, nobody extracted it.
`get_job 3`: status **Refunded** — the second run has now ALSO settled refunded.
Both are $100 real USDC in `LaborMarketV2` escrow on Base mainnet; the task text
itself says "The chain is the only judge." Incident I-02, updated this date.

Audience evidence (coding-niche sweep 2026-08-31): stakes-first first-person
hooks with a number carried the largest video in the sample (5.9M plays), and the
niche's comment sections reward candour about what could go wrong over polish.

## Hypothesis

A real-money challenge framed as a bounty story (proven short-form genre) with a
checkable on-chain artefact will out-perform any capability explainer. One
variable vs. HS-001's flat-premise arm: the hook leads with the stake, not the actor.

## Hook

**Selected:** *"There's a hundred dollars sitting on the open internet, and the
rules say: steal it and it's yours."*
Variants and reasoning: `../../memory/hooks.md` (HS-024 section).

## Script — 38s

| t | On screen | Audio (NARRATOR) | Caption (burned) |
|---|---|---|---|
| 0.0–3.5 | BaseScan: the escrow address, $100 USDC balance visible | "There's a hundred dollars sitting on the open internet — and the rules say: steal it and it's yours." | `$100. real USDC. public chain.` |
| 3.5–9.0 | the job page / `get_job 2` output scrolling: "This job is not work." | "It's locked in a smart-contract escrow as an open challenge. No claim form. No judge. The chain decides." | `no claim form. the chain is the judge.` |
| 9.0–15.0 | highlight the task line: only the accepting agent can submit — and it won't | "There's no work to do. The only way to win is to break the contract itself." | `the only way in: break the contract` |
| 15.0–21.0 | status field: **Refunded** — hold on the word | "Thirty days ran out. Status: refunded. Nobody managed it." | `30 days. nobody.` |
| 21.0–26.0 | `get_job 3` beside it: **Refunded** again | "So we ran it again. Another thirty days. Refunded again." | `we ran it twice.` |
| 26.0–33.0 | plain slate, small text | "That is not proof it's secure. These contracts have never been audited. It's just the only kind of evidence we can actually give you — the kind you can check yourself." | `not audited. just checkable.` |
| 33.0–38.0 | BaseScan URL + job numbers on screen, cut to black | "Job two and job three. Go check I'm not lying." | `job #2 · job #3 · base mainnet` |

The turn is at **15.0s** (the word *Refunded*); the candour beat at 26.0s is
mandatory — it is the DO NOT CLAIM ledger's audit line spoken out loud, and per
the sweep it is also the part the audience rewards.

## Shot list

| # | Shot | Dur | Source | MUST CONTAIN |
|---|---|---|---|---|
| s01 | BaseScan balance | 3.5 | browser capture | the USDC amount and the address |
| s02 | job #2 task text | 5.5 | MCP client capture | "This job is not work." verbatim |
| s03 | submit-restriction line | 6.0 | same capture | the sentence about the accepting agent |
| s04 | job #2 status | 6.0 | same capture | the word `Refunded` |
| s05 | job #3 status | 5.0 | same capture | `Refunded`, visibly a different job number |
| s06 | candour slate | 7.0 | title card (penpot/brand-kit) | "not audited" legible at phone scale |
| s07 | end card | 5.0 | title card | both job numbers + chain name |

## May NOT claim (from the ledger)

- "secure" / "audited" — the 26.0s beat exists to pre-empt this.
- Any live traction number not on screen in the same frame.
- That a third run exists or is planned — unverified at scripting time.

## Captions/CTA (viral-captions-and-ctas)

Caption: `We left $100 of real money where anyone could take it. Twice. Here's
what happened.` CTA is a **send/check CTA**, not a follow-beg: "Go check I'm not
lying" + job numbers. Pinned comment: link to the escrow address and both jobs,
plus one line: "Not audited. Start with amounts you'd shrug at — that's our own
docs talking."
