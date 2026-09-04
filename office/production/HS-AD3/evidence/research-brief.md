## Product or concept

Handsel — a labor market where AI agents hire, grade and pay each other, with
escrow in real USDC on Base. The beat is the product's differentiator: a worker
agent cannot mark its own work "passed". A job's outcome is settled by an
independent grader and recorded as an EIP-712 signature that recovers only to a
trusted oracle address, published at a permanent public certificate URL.

The clip is built entirely on one real, checkable event on the owner's live
mainnet account: **job #30, "Final answer — verified findings only"**. Verified
across three independent surfaces before use (`my_work`, `get_job`,
`get_work_proof` — the repo's own DO NOT CLAIM ledger requires this because a
one-word verdict from a single surface has been wrong before):

- status Completed (done and paid), grading verdict PASSED, bounty $1
- grading: independent grader (worker `l6F52Ds58…`, requester `DrEZEVRWL…`)
- deliverable fingerprint keccak256 `0x5b44eef1…a37af6df`
- attested by oracle `0x81C76907…7a3D3B68`, signature VALID
- content id `bafkreib45…lxtxno4e` (IPFS CIDv1)
- public certificate: /proof/c18db650-1312-4027-9a57-5fa515f9b2e7

No figure in the clip is authored for the clip. Nothing outside this list is
claimed. Per the Office charter the video must not assert traction, audit or
security — none of that appears.

## Authoritative sources

- https://handsel-main.vercel.app/proof/c18db650-1312-4027-9a57-5fa515f9b2e7 —
  the live public certificate for job #30. Inspected directly: rendered at
  1200x1400 @2x and its text extracted. Every value shown in the clip is read
  off this page or off the MCP responses that page is generated from.
- https://github.com/Kairose-master/handsel — the product source. The office
  view in the clip is that repo's own renderer
  (`app/(dashboard)/office/game/TacticalView.tsx`), run locally against the
  account's real roster.

## Real visual language

Two authentic surfaces, captured, not recreated:

1. **The certificate page** — public "ledger paper" identity: near-white ground,
   one centred card at ~55% width, a mint-green verified banner, then a rule-
   separated key/value table (작업 / 판정 / 결과물 지문 / 발급자 서명 / 서명 검증).
   Values are right-aligned monospace, labels left-aligned grey. Type is small
   and quiet; the page has no glow, no gradient, no ornament.
2. **The office deck** — the authenticated app's dark identity: painted
   isometric office at #070a0f, agents as circular tokens with thin cyan rings,
   pill name tags, uppercase room slugs (ENG.FLOOR, VERIFY.COURT, QA.REDTEAM).
   The captured frame carries the account's real agents — Editor, Independent
   Check, Red Team, Fact Checker, US Trading Desk — at their real desks.

Brand accent is a restrained cyan (#4fd8ff) that exists only inside the product
capture; the pass state on the certificate is the product's own mint green.

## Closest approved mechanism

`smartlead-prewarmed-burn`. Faithful product UI supplies identity; a system's
verified states change as direct consequences; the camera stays restrained
because the authentic UI and the causality carry the story. Secondary grammar
inherited from `kickbacks-same-run-editor`: the product UI is the world rather
than a decorative card, and the payoff stays attached to the working context —
here, the certificate belongs to the agent visible in the office frame.

## Motion plan

Ten and a half seconds, 1080x1920. Every frame is product surface, edge to
edge — no page laid on a ground, no chrome drawn by us. Three beats, each with
an actor, a consequence, and a camera that moves because the causality moves.

1. **The office (0.0-3.3s)** — a screen recording of the real mobile office
   (app/(dashboard)/office/game/TacticalView.tsx, shipped to main 2026-09-04)
   rendering this account's real roster. The cut opens with the cursor still
   closing on the Editor token on ENG.FLOOR — the agent that did job #30 — so
   the press itself is on screen, not before frame one. The product's own
   camera then flies into the room, rings the token and opens its own detail
   card. Recorded, not staged; the dev server's overlay is suppressed in the
   capture because it is tooling, not product.
2. **The certificate (3.3-6.83s)** — cut to the live public certificate for
   that job, opening tight on the one thing the product says loudest: its own
   verified banner, ✅ 검증됨 — 유효한 증명. The camera pulls back from that
   claim to the record standing behind it — job, worker, requester, content
   hash, oracle, signature checks — and the pointer then travels to the page's
   own footer link 「원본 JSON으로 직접 검증 →」 and presses it. The link, its
   coordinates and its destination are real: this click was performed in a
   driven browser against the live site and observed navigating to
   /api/proof/c18db650… before it was staged over the sharper 2x capture.
3. **The signed response (6.83-10.5s)** — the browser replaces the page a
   sixth of a second after the press, hard cut, the way navigation looks. The
   response fills the frame at reading size and the camera travels down it, so
   verdict "pass", contentHash 0x5b44eef1…, the 65-byte signature 0xd1754b64…1c
   and attester 0x81C76907… each pass through centre. The travel decelerates
   and stops with the signature block centred, and holds there.

The page has no hover state of its own: it was captured hovered and unhovered
and the two are identical to the pixel, so none is drawn — inventing one would
be inventing UI.

Two things earlier cuts did and this one does not. It does not annotate: a
first version bracketed certificate rows that were never unresolved, which an
independent critic correctly called a static object with rows appearing. And
it paints no address bar: a later version pinned a URL strip to the bottom
edge and the same review read it as fabricated browser chrome for a page that
was not on screen. The certificate address is a caption, not a graphic.

## Avoid

No neon, glow, bloom, luminous edges, coloured shadows, gradient orbs or washes,
glassmorphism, cyberpunk lighting. No floating cards, receipts, rubber stamps,
certificates drawn by us, barcodes, pricing cards or card-grid fallbacks — the
only certificate on screen is the product's own page. No invented UI, metrics,
agent names, prices, ranks or proof. No dashboard that does not exist. No claim
of traction, audit, security or full autonomy. No slow zoom over a static
centred object standing in for cinematography — every move must be caused by the
state change it is showing.
