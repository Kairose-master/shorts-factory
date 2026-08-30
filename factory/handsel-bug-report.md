# Handsel MCP — bug report: job status contradicts grading verdict

한 줄 요약: `get_job`이 **채점에 실패해 지급되지 않은 잡을 "done and paid"로 표시**하고,
존재하지 않는 작업증명을 보라고 안내합니다. 그리고 `claim_job`이 "예약됨"이라며 거부한
잡을 같은 계정의 auto-mine 워커가 나중에 스스로 클레임했습니다.

Reported: 2026-08-30 · Server: `Handsel` MCP (mainnet/real-USDC instance, not `Handsel-test`)
Account: 17 agents, Office 1 = "Due Diligence Desk" template, all 14 roles `auto-mine`.

---

## Bug 1 — `get_job` reports a FAILED, unpaid job as "Completed (done and paid)" (high)

Three tools disagree about the same job, and the one an operator is most likely to
read is the one that is wrong.

**Job #20** — "AWS read — A webhook receiver taking 5M requests a month…", bounty $1,
worker `AWS Reader` (`0xC3ECF5FE7a80d18e68B9D7A4442cB651F631FC78`).

| Tool | What it returns |
|---|---|
| `my_work` | `#20 · … · Completed · grading: FAILED · agent: AWS Reader` |
| `get_job(20)` | `status: Completed (done and paid — see get_work_proof for the signed proof)` |
| `get_work_proof(20)` | `No proof recorded for job #20 — proofs are issued when a job passes grading and auto-settles.` |

`get_job` asserts two things that are both false: that the job is paid, and that a
signed proof exists to look at. The proof endpoint's own wording ("proofs are issued
when a job passes grading") is the proof that #20 did not pass.

Independent confirmation that no money moved: `list_my_agents` shows `AWS Reader` at
**$0.06 USDC** — its seed balance, unchanged. Every agent that actually passed a job
carries its bounty (`Independent Check` $2.13, `Researcher` $2.00, `Red Team` $1.25,
`Editor` $1.10, `Fact Checker` $1.00, `Architect` $0.72, `Cloudflare Reader` $0.50).

**Expected:** a terminal state that failed grading should read as failed/settled-unpaid
(e.g. `Failed (graded not-passed — escrow returned to requester)`), and must not point
the operator at a `get_work_proof` that cannot exist.

**Why it matters:** an operator reconciling earnings from `get_job` alone will book
revenue that never arrived, and will not notice a worker that is silently failing.

### Reproduce
1. Have a worker agent claim and `submit_work` on a job whose deliverable misses the
   acceptance criteria, so the independent grader returns not-passed.
2. `my_work` → the row shows `grading: FAILED`.
3. `get_job(<id>)` → status line reads `Completed (done and paid …)`.
4. `get_work_proof(<id>)` → `No proof recorded`.
5. `list_my_agents` → the worker's USDC balance is unchanged.

---

## Bug 2 — `get_job` says "awaiting grading" for a job `my_work` has already graded FAILED (medium)

**Job #31** — "Investment committee memo — 유튜브 Shorts 채널 @Cost_Of_말 운영 전략…",
bounty $3.33, requester `0x984DBbaEb54702f82e0BDE18f0d97e0AAEEdddB0` (a third party),
worker `My Research Agent` (`0x4dA326C5AFe0F5adF3b7c988D001B2408a7fFf33`).

| Tool | What it returns |
|---|---|
| `my_work` | `#31 · … · Submitted · grading: FAILED · agent: My Research Agent` |
| `get_job(31)` | `status: Submitted (submitted — awaiting independent grading / settlement)` |
| `get_work_proof(31)` | `No proof recorded for job #31` |

Both calls were re-issued back-to-back in one turn and still disagreed, so this is not a
stale-read artifact of one snapshot. Either the grader has run (and `get_job`'s
explanatory text is wrong) or it has not (and `my_work` is showing a verdict that does
not exist yet). From the client side the two are indistinguishable, which is itself the
problem: there is no single tool an operator can trust for "has this been graded".

If the intended semantics are *graded but not yet settled*, the status string should say
so — "awaiting independent grading" is actively misleading once a verdict exists.

---

## Bug 3 — a job `claim_job` refuses as reserved is later claimed by auto-mine on the same account (medium)

Same job #31, earlier the same day.

Manual `claim_job(31)` was refused, repeatedly, with:

> This job is reserved for a different hired worker (an office pipeline step)
> — it is not open to anyone else.

Diagnosis at the time (recorded in `factory/office-report.md`): the requester
`0x984D…ddB0` is not one of our 17 agents and the reserved worker is not on this
account — a third party had stood up an office from the same *Due Diligence Desk*
template. The refusal looked correct.

Hours later, with no operator action, `my_work` shows job #31 **claimed and submitted by
our own `My Research Agent`** via auto-mine.

So one of these is true, and the client cannot tell which:

- **(a)** the reservation is enforced in the `claim_job` path but not in the auto-mine
  claim path — auto-mine bypasses a gate that manual claiming respects; or
- **(b)** the reservation legitimately lapsed (timeout / the reserved worker released it)
  and the job became open — but that transition is invisible: nothing in `get_job`,
  `browse_open_jobs` or any notification records that a reserved job reopened.

If (a), it is a permissions hole. If (b), it is missing observability — the operator
learns their agent took an outside job only by reading `my_work` afterwards.

---

## Bug 4 — `my_work` recommends a `set_auto_mine` parameter the tool does not accept (medium)

**Update 2026-08-30 11:11 UTC.** `my_work` output changed between the 10:11 and 11:11 calls.
It now annotates third-party jobs and closes with:

> 2 of these are an outside job — posted by another account, with your agent's bond and
> credit score staked on it. `set_auto_mine` with `scope:"own"` keeps a worker to work
> your own agents posted.

The annotation is a real improvement. The advice is not callable. The `set_auto_mine`
schema exposes exactly three properties — `agent_id`, `agent_name`, `enabled` — with
`additionalProperties: false`, so a call carrying `scope` is rejected by input validation
before it reaches the server. The tool tells the operator to do the one thing that would
contain this problem, and the parameter to do it with does not exist.

Either ship `scope` on `set_auto_mine` or stop advertising it.

Still requested alongside it:
1. A capability or role filter, so a generic "platform agent" does not claim a job whose
   acceptance criteria are written for a specific specialist lens (job #31 requires one
   of five named role lenses; the claimer was a generic research agent).
2. Some surfaced signal at the time an auto-mine worker claims, submits, or fails a job —
   the new `my_work` annotation is after-the-fact, and only if the operator looks.

### What the new annotation exposed

The flag reveals that **#19 was also an outside job** — "Legal & regulatory read — 유튜브
Shorts 채널 @Cost_Of_말…", worked by `Independent Check`, graded `passed`. So this account
had been working the third party's pipeline in at least two places, one of them paid, and
until the 11:11 tool change there was no field anywhere in `my_work`, `get_job` or
`office_roster` that distinguished an own-delegation job from an outside one. Operators
who ran auto-mine before this change could not have known.

## Not verified (stated as unknown, not as fact)

- Whether the bond for #31 was slashed. `My Research Agent` still reports credit 433.00
  and $3.24 USDC after the FAILED verdict; whether settlement is merely pending or the
  failure carries no bond penalty is not observable from the client.
- Whether the third party's "shared source" for #31 contains anything non-public. The
  channel's view counts and titles are public, so a third party collecting them needs no
  access to our material; no evidence of a leak, and none is claimed here.

## Environment

- Tools used: `my_work`, `get_job`, `get_work_proof`, `list_my_agents`, `office_roster`,
  `claim_job` (earlier).
- All observations above are verbatim tool output captured 2026-08-30 01:10–09:20 UTC.
- Job ids referenced: #20 (bug 1), #31 (bugs 2–4), #19 (outside job, passed). Control cases that behave correctly:
  #19, #21, #24, #25, #27, #28, #29, #30 — all `passed`, all paid.
