# Instagram Content Publishing API — operating reference

Verified against Meta's official sample (`fbsamples/reels_publishing_apis`,
insta_reels sample, last commit 2026-06) and the Graph API docs. Base:
`https://graph.facebook.com/{version}` — version from `INSTAGRAM_API_VERSION`
(unset = unversioned, Meta serves the default).

## The publishing flow

```
media asset (local render)
  ↓ upload to blob store            → public https URL
POST /{ig-user-id}/media           → container id            (UPLOADING)
  image_url | video_url, media_type=REELS|STORIES|CAROUSEL, caption,
  cover_url, share_to_feed, alt_text, is_carousel_item, children
  ↓
GET /{container-id}?fields=status_code                        (PROCESSING)
  IN_PROGRESS → poll again (queue backoff: 15s → 10min cap)
  FINISHED    → publish
  ERROR       → FAILED (permanent; inspect media specs)
  EXPIRED     → recreate container (~24h lifetime)
  PUBLISHED   → already done (crash-recovery path)
  ↓
POST /{ig-user-id}/media_publish?creation_id=<container>      (PUBLISHING)
  → media id                                                  (PUBLISHED)
  ↓
GET /{media-id}?fields=permalink       (record, show in Local Jobs)
GET /{ig-user-id}/content_publishing_limit?fields=config,quota_usage
```

Carousel: children first (`is_carousel_item=true`, no caption), then parent
(`media_type=CAROUSEL`, `children=id1,id2,...`, caption on the parent).
Images inside a container are usually ready immediately; video containers
take seconds-to-minutes.

## Auth model

- IG **professional (Business/Creator) account** linked to a Facebook Page.
- Meta app with **Instagram Graph API** product; token needs
  `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`
  (+ `instagram_manage_insights` for insights).
- Use a **long-lived token** (60d) or a System User token (Business Manager,
  non-expiring); store server-side (platform_secrets), rotate on `NEEDS_AUTH`.

## Error classes (see lib/social/instagram/errors.ts)

| class | codes | handling |
|---|---|---|
| auth | 102, 190 | park row as NEEDS_AUTH; human rotates token |
| transient | 1, 2, 4, 17, 32, 341, 613; HTTP 429/5xx; subcode 2207003/2207027 | client retries ×3, then queue backoff |
| permanent | everything else (100 validation, 10/200 permission…) | FAILED immediately; never retried |
| already-published | subcode 2207032 / message match | mapped to success |

## Hard limits worth engineering around

- **~25 API publishes per rolling 24h** per IG account (`content_publishing_limit`).
- Caption ≤ 2200 chars, ≤ 30 hashtags; alt text ≤ 1000.
- Feed image aspect 0.80(4:5)–1.91:1 enforced server-side; Reels/Stories 9:16 recommended.
- Reels ≤ 1GB / length limits per current docs; container expires unpublished after ~24h.
- Stories: image/video only via API — **no polls, stickers, links, music**.
- Media must be fetchable by Meta's crawler: public URL, no auth, no redirects to private hosts.

## What the API cannot do (known limitations)

- No true scheduled publish server-side — scheduling is ours (queue `run_after`).
- No editing a published caption via this surface; no deleting via publish API.
- No personal (non-professional) accounts.
- Insights metrics vary by media type; absent metrics return an API error per
  metric, which is why `getMediaInsights` returns null rather than throwing.
