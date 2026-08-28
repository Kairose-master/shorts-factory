# Attaching capabilities to Handsel office agents

Done live 2026-08-27 on office 1. Everything below is a real call and a real
result, not documentation of an intent.

## What "attaching a skill" actually is

A Handsel agent is a worker. By default it is a **platform agent** — it has the
runtime and nothing else. Wiring points it at one **MCP server + one tool**, and
from then on that tool is called whenever the agent is dispatched a job.

```
test_mcp_connector  →  wire_office_agent  →  office_roster
     (verify)              (attach)            (confirm)
```

`browse_capabilities` reads the **ClawHub** directory of published skills — real
listings with install counts and stars. It is read-only and is for deciding
*what* to wire, not for wiring.

## The one decision that matters: `assisted` vs `proxy`

The tool's own warning, and it is not a style preference:

> Prefer `assisted` for a search-shaped server: in `proxy` the tool's raw output
> becomes the deliverable, which fails any acceptance criterion about quoting
> sources however good the retrieval was.

- **`assisted`** — the agent *writes* its deliverable from what the tool returned.
  Correct for anything search-shaped, because a search server returns a result
  dump, and a result dump is not work.
- **`proxy`** — the tool's output *is* the submission. Correct only when the
  server on the other end is itself an agent that writes finished work.

Getting this wrong does not error. It produces a worker that retrieves well and
fails grading, which is a much more expensive kind of wrong.

## What was wired

```
test_mcp_connector https://mcp.exa.ai/mcp · web_search_exa
  → reachable · job arrives in "query" · single string · works as a worker
```

| Agent | Was | Now |
|---|---|---|
| Commercial Analyst | platform agent, no tool | `web_search_exa` · assisted |
| Financial Reviewer | platform agent, no tool | `web_search_exa` · assisted |
| Legal & Compliance Reader | platform agent, no tool | `web_search_exa` · assisted |

**Partner and Red Team were deliberately left unwired.** The Partner synthesises
the three reads and the office's structure already feeds it their output; giving
it a search tool would have it go looking instead of reading what it was handed.
A capability is not automatically an upgrade — it changes what the role does.

Confirmed against `office_roster` rather than assumed from the call's reply.

## The shared source

`set_office_source` appends one document to **every** role's brief at hire time,
so several agents genuinely read the same thing through different tools.

Office 1's source is now the Handsel verified-facts block **and the DO NOT CLAIM
ledger** (2,602 chars) — so any office hired into slot 1 inherits the same
factual floor the Growth Office holds itself to, including "never collapse
outcome, cause, attribution and settlement into one word", which is the rule
HS-006 broke.

**It applies at hire time only.** It does not rewrite an already-hired office,
because a brief that changed under a posted job would move the target its worker
is graded against. That is a correctness property, not a limitation.

## Gotcha

`wire_office_agent` matches `agent_name` literally. `Legal & Compliance Reader`
failed as `Legal &amp; Compliance Reader` — an ampersand that got HTML-escaped in
transit. **Use `agent_id`**; it is the documented preference and it has no
escaping surface.

## Why this matters to the Office

A Handsel office is not a fixed template. The roles, their tools and their shared
brief are all editable after hiring, which means "build an AI company" is closer
to literal than the phrase suggests — and it is a content pillar in itself:
*I gave one of my AI employees a new skill, and it changed what it delivered.*
