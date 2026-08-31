---
name: instagram-publisher
description: >
  Publish approved content to the official Handsel Instagram account through
  the Instagram Content Publishing API (Graph API) — single-image posts,
  carousels, Reels and Stories — with dry-run previews, scheduling, quota
  checks, publish-status polling and media insights. Use when asked to post,
  publish, schedule or preview Instagram content, turn screenshots into a
  carousel, share a Reel to the feed, put something on the Story, check
  publishing quota, or read performance of a published post. Never publishes
  without an approved content-queue row; dry-run first is the default for any
  new content.
---

# instagram-publisher

Wraps `lib/social/instagram/` (SocialJob queue + InstagramPublisher provider).
Everything observable goes through the same Local Jobs surface as any other
Handsel work — there is no separate social dashboard.

## Non-negotiables (mirror of the module policy)

1. **Nothing publishes without approval.** A content row must be `READY`
   (human-approved) before `enqueue`. Generation finishing is not approval.
2. **Dry-run first.** For any content not previously previewed, run the
   preview and show the exact Graph calls before enqueueing.
3. **Never print a token.** Configuration checks report configured/missing
   and last-4 only (`maskToken`).
4. **Reference-driven content only** for Reels: the queue row must cite its
   reference-format teardown and demand cluster (see
   `docs/social/instagram-brand.md`). Refuse to enqueue a Reel without them.
5. **Respect quota.** Check `get_quota` before bulk scheduling; stop at 80%.

## Conceptual operations → implementation

| Operation | Call |
|---|---|
| `instagram.publish_post` | build SocialJob `{contentType:'post'}` → `enqueueSocialJob` |
| `instagram.publish_carousel` | SocialJob `{contentType:'carousel', assets:[2..10]}` → enqueue |
| `instagram.publish_reel` | SocialJob `{contentType:'reel', shareToFeed}` → enqueue |
| `instagram.publish_story` | SocialJob `{contentType:'story'}` → enqueue |
| `instagram.get_publish_status` | `getQueueRow(db, businessKey)` → `describeSocialJob` |
| `instagram.get_quota` | `getPublishQuota()` |
| `instagram.get_media_insights` | `getMediaInsights(mediaId)` |
| dry-run / preview | `instagramPublisher.preview(job)` — zero network, zero token |

The queue is drained by the ops cycle (`social.drain` step) every 5 minutes;
`scheduled_at` in the future holds a row untouched until due.

## Natural-language mapping

- "Post this image to Handsel Instagram." → validate 4:5, upload to blob,
  preview, confirm approval state, `publish_post`.
- "Publish this as a Reel and share it to the feed." → `publish_reel` with
  `shareToFeed: true`; demand the reference-format citation first.
- "Put this release image on the Handsel Story." → `publish_story` (9:16).
- "Turn these four screenshots into an Instagram carousel." → 4 assets,
  4:5 lint, alt text per image, `publish_carousel`.
- "Schedule this launch content for tomorrow." → same, with `scheduled_at`.

## Media prerequisites

Graph API fetches media from a **public https URL**. Upload local files to
the blob store first (`/api/upload` or the worker direct-to-blob route) and
use the returned `*.public.blob.vercel-storage.com` URL. Validate with the
artifact host allowlist before handing any URL to Meta.

## Failure handling the operator should know

- `NEEDS_AUTH`: token expired/revoked — re-issue the long-lived token; the
  row is parked, never retried (retrying burns quota).
- `EXPIRED`: Meta expired an unpublished container (~24h); the queue
  recreates it automatically from the same blob media.
- Quota exhausted: transient; the row retries with backoff.
- Full status vocabulary and the lifecycle diagram: `references/graph-api.md`.

## Scripts

- `scripts/preview.mjs <job.json>` — offline dry-run: prints the exact call
  sequence and validation warnings for a SocialJob JSON. No token needed.
