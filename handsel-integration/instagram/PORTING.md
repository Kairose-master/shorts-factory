# Porting this integration into Kairose-master/handsel

## Why it is staged here

This session's permission layer denied attaching `Kairose-master/handsel`
(read and push both blocked by the auto-mode classifier), so the integration
was built against a public clone's conventions and staged in this directory.
Everything compiles and 47 tests pass standalone (`npm run gates` here).
To let a session work on the Handsel repo directly, grant it repository
access (claude.ai → admin settings → Claude GitHub app repo allowlist), then
this directory transplants in under an hour.

## File map (staged path → target path)

| Here | Handsel repo |
|---|---|
| `lib/social/types.ts` | `lib/social/types.ts` |
| `lib/social/instagram/*.ts` | `lib/social/instagram/*.ts` |
| `docs/social/instagram-brand.md` | `docs/social/instagram-brand.md` |
| `skills/instagram-publisher/**` | `skills/instagram-publisher/**` |
| `tests/instagram.test.ts` | `tests/instagram.test.ts` |
| `tests/instagram.e2e.test.ts` | `tests/instagram.e2e.test.ts` |
| `patches/env.example.snippet` | append to `.env.example` |
| `patches/ops-cycle.snippet.ts` | fold into `lib/ops-cycle.ts` OPS_STEPS |
| `patches/office-world-data.snippet.ts` | fold into `lib/office-world-data.ts` (growth-studio) |

## Required edits after copying (each is 1-3 lines)

1. **Token source** — `lib/social/instagram/auth-server.ts`, the marked line:
   ```ts
   const accessToken = (await getPlatformSecret('instagram_token')) || process.env.INSTAGRAM_ACCESS_TOKEN || null
   ```
   (import from `@/lib/platform-secret`).
2. **QueryPort** — callers pass `pool` from `@/lib/db`; `pg.Pool` satisfies
   the interface as-is. Nothing in queue-server imports the DB directly, so
   no edit inside the module.
3. **Retry helper (optional)** — client-server carries its own bounded retry
   to stay dependency-free; if you prefer one policy repo-wide, swap the loop
   for `withRetry` from `@/lib/retry` with a Graph-aware `retryable`
   predicate (`(e) => e instanceof InstagramApiError && e.classification === 'transient'`).
4. **Ops step** — append the snippet's step object to `OPS_STEPS`. Not
   `fast: true` (see snippet header).
5. **Import paths** — tests here use relative imports; switch to the repo's
   `@/` alias when moving into `/tests`.
6. **Media URL gate** — before enqueueing, run asset URLs through
   `validateSourceUrl()` (`@/lib/media-recipe`) and the
   `.public.blob.vercel-storage.com` allowlist (`@/lib/artifacts`). The
   staged code lints https-only; the repo has the stronger SSRF gate.

## Local Jobs surface (Phase 7)

No new dashboard. The queue's `describeSocialJob` lines surface through the
ops-cycle report (like every other step), and a `social_publish_queue` row is
the durable job record: `{ id, business_key, job(jsonb: SocialJob — content
type, media, caption, alt text, scheduled time, campaign, container id, media
id, retry count, created/published at, error), status, attempts, run_after }`.
If a UI row is wanted on `/jobs`, render pending/abandoned queue rows with
the existing compact-row pattern; `EVENT_ICON`-style mapping:
QUEUED/PREPARING→Rocket, UPLOADING/PROCESSING→Wrench, PUBLISHED→CheckCircle2,
FAILED/NEEDS_AUTH→XCircle.

## Meta configuration required from you (one-time, ~30 min)

1. Instagram account → **Professional (Business)**, linked to a Facebook Page.
2. Meta developer app (Business type) → add **Instagram Graph API** product.
3. In Business Manager, create a **System User**, grant it the Page + IG
   account, generate a token with scopes: `instagram_basic`,
   `instagram_content_publish`, `pages_read_engagement`,
   `instagram_manage_insights`. (System-user tokens don't expire; a normal
   long-lived user token needs 60-day rotation.)
4. Read the ig-user-id: `GET /me/accounts` → page id →
   `GET /{page-id}?fields=instagram_business_account`.
5. App review: `instagram_content_publish` requires Advanced Access for
   accounts outside the app's roles — for the official Handsel account owned
   by the app's own Business, Standard Access on a live app suffices.
6. Set `INSTAGRAM_ACCESS_TOKEN` + `INSTAGRAM_ACCOUNT_ID` (Vercel env or
   `platform_secrets`), optionally pin `INSTAGRAM_API_VERSION=v21.0`.

## Exact commands

- Local test (here): `cd handsel-integration/instagram && npm install && npm run gates`
- Local test (after porting): `npm run gates` at the Handsel repo root
  (typecheck + lint + test + build), lockfile via
  `pnpm install --lockfile-only && pnpm install --frozen-lockfile` — though
  no new runtime dependency is added, so package.json should not change.
- **Live verification (the single next step once credentials exist):**
  upload one 4:5 image to the blob store, build a SocialJob from
  `skills/instagram-publisher/examples/job.post.json` with that URL,
  `enqueueSocialJob(pool, job)`, run one ops cycle (or call
  `drainSocialQueue(pool)` twice ~15s apart), and confirm the row reaches
  `done` with a media id + permalink. Until that succeeds, publishing is
  implemented and tested against a faithful local fake — **not claimed to
  work live**.

## Dependency decisions (Phase 5)

| Candidate | Verdict | Why |
|---|---|---|
| `fbsamples/reels_publishing_apis` (Meta) | **reference only** | Express demo, not a library; used to verify the container/status/publish/quota flow and param names. Active (2026-06). |
| `Inoue-AI/Inoue-AI-Instagram-SDK` | rejected | MIT, active, but Python+Go — wrong language for a TS/Next repo; adds a runtime for zero fetches saved. |
| `mcpware/instagram-mcp` | rejected (noted as optional) | MIT, active TS MCP server with publish+insights — but it's a *server process* with its own auth config; Handsel needs an in-process lib wired to its own queue/ops/approval. Could later be offered as a verified connector for *external* offices. |
| `MatthieuThib/pystagram` | rejected | Python; last commit 2024-03; leans on the deprecated Basic Display API. |
| **Chosen: direct Graph API, zero new runtime deps** | ✔ | The whole surface is 4 endpoints; global fetch + the repo's own retry/queue conventions cover it. Smallest reliable stack. |
