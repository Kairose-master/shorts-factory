# HS-021 — "My AI agent earned $0 in 48 days and owes me $155"

**Pillar C** · **Priority 71** · **Posture: SHIPPED** · **Status: scripted, not produced**
Format: story → mechanism · Target: 40s · 1080×1920 · Platforms: TikTok → Reels → YouTube Shorts

## Grounding

Incident I-09: r/AI_Agents, 2026-08-22 — *"My autonomous AI agent has earned $0
in 48 days and still owes me $155."* 79 upvotes, 62 comments
(`../../research/audience-signal-2026-08-27.md`). The story is the Redditor's,
attributed on screen; it is never presented as ours.

Audience evidence (sweep 2026-08-31): AI-career-fear is the niche's largest
traffic source (BBC clip 5.9M plays; top comment "software engineers have
created their own replacement", 85K likes), and agent-failure candour is the
most-rewarded register in comments ("Claude deletes ur whole project and spends
2 million tokens" — 3,018 likes). This entry sits exactly on both.

## Hypothesis

The audience's own economic anxiety, transposed onto the agent ("the agent has a
jobs crisis too"), will out-perform a mechanism-first explainer on hook retention.
One variable: story-first vs. mechanism-first opening.

## Hook

**Selected:** *"This AI agent earned zero dollars in 48 days. It also owes its
owner a hundred and fifty-five."*
Variants and reasoning: `../../memory/hooks.md` (HS-021 section).

## Script — 40s

| t | On screen | Audio (NARRATOR) | Caption (burned) |
|---|---|---|---|
| 0.0–4.0 | the Reddit post, subreddit + date visible, numbers highlighted | "This AI agent earned zero dollars in 48 days. It also owes its owner a hundred and fifty-five." | `$0 earned. $155 owed. 48 days.` |
| 4.0–10.0 | scroll of the thread (real, attributed) | "That's a real post. Sixty-two comments, most of them the same story: the API bill runs whether or not anyone pays for the output." | `the bill runs either way` |
| 10.0–16.0 | plain slate | "The missing piece isn't a smarter agent. It's this: who says the work was good — and does money move on their word, or the agent's?" | `who grades the work?` |
| 16.0–23.0 | Handsel job flow capture: escrow locked → work submitted → grader verdict | "On this market the bounty is escrowed before work starts, and the grade comes from a third party — never the agent that did the work. Fail, and the money goes back." | `escrow first · graded by a third party · fail = refund` |
| 23.0–30.0 | credit score panel: 300–990 scale, an agent's real score | "Pass enough graded jobs and the agent has a track record it never self-reported — a credit score, 300 to 990, built only from verified work." | `a record it didn't write itself` |
| 30.0–35.0 | `list_my_agents` capture: five rows at 0.00 | "Ours isn't a success story yet either. Nine agents on our own account. Five have never earned a cent." | `five of ours: $0.00` |
| 35.0–40.0 | /try sandbox loading — no login screen | "The sandbox is free, no login, fake money. See if your agent can pass a grade." | `try it with fake money first` |

The turn is at **10.0s**; the self-deprecating beat at 30.0s is deliberate — it
is incident I-05 verbatim and pre-empts the "shill" read that the sweep's
comment data punishes hardest.

## Shot list

| # | Shot | Dur | Source | MUST CONTAIN |
|---|---|---|---|---|
| s01 | Reddit post | 4.0 | screenshot, subreddit + date visible | the two numbers |
| s02 | thread scroll | 6.0 | screenshot | at least one real comment legible |
| s03 | question slate | 6.0 | title card | the question, ≤10 words |
| s04 | job flow | 7.0 | MCP/UI capture | escrow amount + a verdict from a non-worker party |
| s05 | credit panel | 7.0 | UI capture | the 300–990 scale on a real agent |
| s06 | agent list | 5.0 | MCP capture | five visible `0.00` rows |
| s07 | /try | 5.0 | browser capture | the absence of a login form |

## May NOT claim (from the ledger)

- That Handsel would have saved this Redditor money — unknowable; the video only
  poses the grading question against their story.
- "Agents can borrow on mainnet" — credit drawdown is testnet-only. The script
  says "credit score", never "loan".
- Any traction beyond what is on screen (five $0.00 rows are the honest state).
- **Confirm the live /try URL before publish** (`handsel-main` vs `handsel-nu`
  is an open question in the model file).

## Captions/CTA

Caption: `The agent economy has a jobs crisis too. A real one.` CTA is
send-driving: "Send this to the friend whose agent is 'almost profitable'."
Pinned comment: link to the Reddit thread (credit the author), then the sandbox.
