# instagram-publisher

Skill wrapper over `lib/social/instagram/` — the Handsel Instagram publishing
integration. See `SKILL.md` for the operating contract and
`references/graph-api.md` for the API reference.

## Setup (operator)

1. Meta side (one-time): see "Meta configuration" in `../../PORTING.md`.
2. Set env vars (`.env`, never committed):
   `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_ACCOUNT_ID`,
   optional `INSTAGRAM_API_VERSION` (e.g. `v21.0`).
3. Verify: quota call succeeds →
   the account is connected and publish-capable.

## Quick dry run

```bash
node scripts/preview.mjs examples/job.post.json
```

## Local tests

```bash
npm run gates   # typecheck + 47 unit/e2e tests, no credentials needed
```
