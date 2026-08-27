# The Verification Lawbook — Office digest

**Source:** *"Handsel 쇼츠 공장과 Verification Lawbook"* (.docx, supplied 2026-08-27).
246 paragraphs, 14 tables, 40 external citations.

---

## ⚠️ Status: this is a DESIGN PROPOSAL, not shipped product

The document says so about itself, twice:

> "현재 정식 제품 명세·고객 데이터가 제공되지 않았으므로 아래는 … positioning 작업
> 가정이다."

> "rulesetVersion, verifierVersion, evidenceHash 같은 필드가 실제로 구현되지 않았다면
> concept mockup임을 표시하거나 구현 후 촬영한다."

**Binding consequence for the Office:** none of the codes below may appear on a
Handsel screen in a published video as though the product emits them. Doing so
would fabricate a feature — the exact thing `CHARTER.md` rule 1 forbids, and
doubly indefensible for a project whose pitch is verifiability. If a Lawbook code
appears at all, it is labelled `CONCEPT` on screen.

Verify against `handsel-model.md` (built from the repo) before scripting. Where
the two disagree, **the repo wins.**

---

## The core idea

A flat failure enum is not enough:

```
FAIL_PERMISSION  FAIL_TIMEOUT  FAIL_ATTACK  FAIL_WORK
```

On one axis this still mixes up *what happened*, *who is responsible*, *whether
it is even judgeable*, *what money should do*, and *what to retry*. The proposal
is to split a verdict into **five orthogonal axes**:

| Axis | Example values | The question it answers |
|---|---|---|
| `outcome` | SUCCESS · FAILED · UNKNOWN · NOT_EXECUTED | Was the contracted work achieved? |
| `cause_domain` | WORKER · POLICY · EVIDENCE · VERIFIER · SYSTEM · SECURITY | Where did the problem occur? |
| `attribution` | WORKER · REQUESTER · VERIFIER · PLATFORM · EXTERNAL · **UNDETERMINED** | Is there a basis to assign responsibility? |
| `retry` | NO · IMMEDIATE · BACKOFF · AFTER_FIX · REVERIFY · APPEAL | What happens next? |
| `settlement` | RELEASE · HOLD · REFUND · PARTIAL · ESCALATE | What does the money do? |

The judgment pipeline: `Observation → Evidence collection → Evidence validation →
Diagnosis → Attribution → Judgment → Remedy/Settlement`.

### The three separations that carry the whole argument

```
Evidence integrity  ≠  Claim truth  ≠  Contract satisfaction
```

A correct screenshot hash means the screenshot was not tampered with. It does not
mean the website is good. (Grounded in C2PA: a valid manifest attests provenance,
not that the content is true.)

```
CAN'T VERIFY  ≠  WORK FAILED
SECURITY_BLOCKED  ≠  MALICIOUS_WORKER_CONFIRMED
```

Containment is not a guilt finding.

## Lawbook v0.1 — 16 proposed codes

| Code | outcome | default attribution | remedy | settlement |
|---|---|---|---|---|
| `WORK_FAILED` | FAILED | worker possible | revise / appeal | refund/slash per contract |
| `POLICY_BLOCKED` | UNKNOWN / NOT_EXECUTED | none | policy review | **no worker penalty** |
| `AUTHENTICATION_REQUIRED` | UNKNOWN | requester side | fix credentials | hold |
| `AUTHORIZATION_DENIED` | UNKNOWN | situational | fix permission | hold |
| `EVIDENCE_MISSING` | UNKNOWN / FAILED | per contract | resubmit | no immediate blame |
| `EVIDENCE_INACCESSIBLE` | UNKNOWN | verifier / requester / platform | restore access → reverify | **no worker penalty** |
| `EVIDENCE_INVALID` | UNKNOWN / FAILED | situational | regenerate evidence | per contract |
| `EVIDENCE_TAMPERED` | UNKNOWN | undetermined | quarantine + adjudication | hold |
| `VERIFIER_UNAVAILABLE` | UNKNOWN | verifier / platform | backoff retry | **no worker penalty** |
| `VERIFIER_DISAGREEMENT` | UNKNOWN | none | second verifier / appeal | hold |
| `VERIFICATION_INCONCLUSIVE` | UNKNOWN | none | more evidence / escalate | hold / partial |
| `FAILED_PRECONDITION` | NOT_EXECUTED | situational | fix state, retry | hold |
| `RESOURCE_EXHAUSTED` | UNKNOWN | provider / platform | capacity/budget fix | **no worker blame** |
| `DEADLINE_EXCEEDED` | UNKNOWN | undetermined | **check state first** | prevent double payout |
| `SECURITY_BLOCKED` | UNKNOWN | undetermined | contain → investigate | hold, **no automatic guilt** |
| `ADJUDICATION_REVERSED` | replaced by new verdict | prior verdict corrected | restore / compensate | credit + settlement correction |

Prior art the document leans on: gRPC status codes (why `UNAUTHENTICATED`,
`PERMISSION_DENIED`, `RESOURCE_EXHAUSTED`, `FAILED_PRECONDITION`,
`DEADLINE_EXCEEDED` are deliberately distinct), RFC 9457 for the wire format
(stable `type` + per-occurrence `instance`), C2PA on provenance ≠ truth, W3C
PROV-O for provenance-of-provenance, NIST SP 800-61r3 for
violation → containment → review → attribution → restriction → remediation →
restoration.

`DEADLINE_EXCEEDED` is singled out: gRPC warns a state-changing operation may
have *succeeded* even after its deadline passed. For a payout or bounty claim,
that means **check state before retrying** or risk paying twice.

## Messaging the document proposes

> **Agents can delegate work. Handsel makes the outcome provable.**
> **Blocked is not failed. Unverified is not failed. We record why.**
>
> Delegate. Prove. Verify. Settle.
> Money moves after evidence, not promises.
> Don't trust the score. Inspect the proof.
> Do not parse error strings. Branch on typed failure semantics.

**"Don't trust Handsel. Inspect it."** is the strongest line in the document and
is a better articulation of the positioning than anything the Office had written.

It also warns against leading with "AI marketplace": the category explains but
creates no tension. Lead with the anomaly and let Handsel be the thing that
*names* it.

## Why this is a content engine, not just a spec

> "failure-code lawbook이 커질수록 콘텐츠 backlog도 자동으로 커진다."

**One incident = one code = one short.** 16 codes is 16 videos with a built-in
structure, which is a better idea generator than the Office's current ad-hoc
ideation. The proposed loop:

```
PRODUCT → (real incident) → LAWBOOK → (names it) → SHORT
   ↑                                                  ↓
   └──────── COMMENTS / DATA ←────────────────────────┘
```

Marketing stops being a department that wraps the product and becomes an
evaluator of whether the protocol is comprehensible to humans.

## What the Office should adopt, and what it should not

**Adopt now:**
- The five axes as a *writing discipline*. Never label an event with one word
  that conflates outcome, cause, attribution and settlement.
- "Don't trust the score. Inspect the proof." as a standing line.
- One incident → one code → one short as the backlog generator.
- The template split: `HSL_DEMO_V1` (UI 70% / host 30%, big status codes) and
  `HSL_INCIDENT_V1` (red error → 0.3s silence → reversal → correct code → remedy).
- The "no fake social proof" rule — use *protocol proof* instead until real
  customer proof exists. This matches the Office's cold-start honesty.

**Do not adopt:**
- The codes as product facts. They are proposed. See the status warning above.
- The document's KPI gates (3s survival 45%+, completion 25%+, CTA 0.7%+) as
  *targets*. The document itself says to switch to relative uplift against the
  account's own median after ~10 videos, and the Office has **no median yet**.
  Treat them as the document's suggested acceptance criteria, not as measurements.
- The published case-study numbers in its Table 2 as benchmarks. The document is
  explicit that organic and paid performance are mixed there and that they are
  not causal.
- LEET as a source. The document itself retires it as a discovery heuristic.
