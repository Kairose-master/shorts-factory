# Handsel Short-Form Growth Office

An autonomous short-form content factory for growing awareness and adoption of
Handsel. Not a campaign — **a learning machine** that should be better at this
after every production cycle.

## Read in this order

| File | What |
|---|---|
| `CHARTER.md` | mission, roles, autonomy boundary, pillars, hard rules |
| `research/handsel-model.md` | the verified product model + **the DO NOT CLAIM ledger** |
| `memory/backlog.md` | 20 scored hypotheses; three approved |
| `sop/production-pipeline.md` | the 14 steps |
| `sop/quality-control.md` | the nine gates and the veto |
| `sop/analytics-loop.md` | how a result becomes a lesson |

## Layout

```
office/
├── CHARTER.md
├── research/handsel-model.md
├── memory/          backlog · hooks · published · rejected · experiments · analytics · lessons
├── sop/             production-pipeline · quality-control · analytics-loop
└── production/<idea-id>/
    ├── plan.md  script.md  hooks.md
    ├── narration.wav  refs/  renders/final.mp4
    ├── aicron-brief.md   (only when a HUMAN generation step is needed)
    └── qc.md
```

`office/` is committed — it is the Office's memory and must survive the
container. Rendered `.mp4` files are gitignored; commit the plan, the script and
the QC verdict, not the binary.

## Start a cycle

Invoke the **`handsel-growth-office`** skill. It routes to the other 49.

## Status

- **Published: 0.** Nothing publishes without explicit human approval.
- **Approved and ready to produce:** HS-001, HS-006, HS-011 — all $0 to make.
- **Blocking capability gap:** no retention/completion analytics. See
  `memory/analytics.md`.
