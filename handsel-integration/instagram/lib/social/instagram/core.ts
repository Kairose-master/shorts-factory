/**
 * Pure Instagram publishing logic — no fetch, no DB, no env.
 *
 * Everything a test can pin without a network lives here: caption and media
 * validation, the container-status state machine, the poll/backoff schedule,
 * quota math and the dry-run preview builder. The repo convention (CLAUDE.md:
 * pure X.ts + X-server.ts siblings; see lib/clawhub.ts vs its fetch) is the
 * reason this file exists as a separate module: the -server siblings stay
 * thin enough that not unit-testing them costs nothing.
 */

import type {
  PublishPreview,
  PublishPreviewCall,
  SocialJob,
  SocialMediaAsset,
} from '../types'
import type { IgContainerStatus, IgMediaType, IgQuota } from './types'

// ---------------------------------------------------------------------------
// Caption / media validation
// ---------------------------------------------------------------------------

export const MAX_CAPTION_CHARS = 2200
export const MAX_HASHTAGS = 30
export const MAX_ALT_TEXT_CHARS = 1000
export const MAX_CAROUSEL_CHILDREN = 10
export const MIN_CAROUSEL_CHILDREN = 2

export interface ValidationResult {
  ok: boolean
  problems: string[]
  warnings: string[]
}

export function countHashtags(caption: string): number {
  return (caption.match(/#[\p{L}\p{N}_]+/gu) ?? []).length
}

export function validateCaption(caption: string): ValidationResult {
  const problems: string[] = []
  const warnings: string[] = []
  if (caption.length > MAX_CAPTION_CHARS) {
    problems.push(`caption is ${caption.length} chars; Instagram caps at ${MAX_CAPTION_CHARS}`)
  }
  const tags = countHashtags(caption)
  if (tags > MAX_HASHTAGS) {
    problems.push(`caption carries ${tags} hashtags; Instagram caps at ${MAX_HASHTAGS}`)
  }
  // eslint-disable-next-line no-control-regex
  if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/.test(caption)) {
    problems.push('caption contains control characters')
  }
  if (caption.trim().length === 0) warnings.push('caption is empty')
  return { ok: problems.length === 0, problems, warnings }
}

/**
 * Aspect linting is advisory (warnings), except where Meta hard-rejects:
 * feed images outside 4:5..1.91:1 fail at container creation, so those are
 * problems, not warnings. Reels/stories are lint-only — Meta crops.
 */
export function validateAssets(
  contentType: SocialJob['contentType'],
  assets: SocialMediaAsset[],
): ValidationResult {
  const problems: string[] = []
  const warnings: string[] = []

  if (assets.length === 0) problems.push('no media assets')

  if (contentType === 'carousel') {
    if (assets.length < MIN_CAROUSEL_CHILDREN || assets.length > MAX_CAROUSEL_CHILDREN) {
      problems.push(`carousel needs ${MIN_CAROUSEL_CHILDREN}-${MAX_CAROUSEL_CHILDREN} items, got ${assets.length}`)
    }
  } else if (contentType === 'post') {
    if (assets.length !== 1) problems.push(`post takes exactly one asset, got ${assets.length}`)
  } else if (assets.length !== 1) {
    problems.push(`${contentType} takes exactly one asset, got ${assets.length}`)
  }

  for (const [i, a] of assets.entries()) {
    if (!/^https:\/\//.test(a.url)) problems.push(`asset ${i}: URL must be https`)
    if (contentType === 'reel' && a.kind !== 'video') {
      problems.push(`asset ${i}: a reel needs a video asset`)
    }
    if (a.altText && a.altText.length > MAX_ALT_TEXT_CHARS) {
      problems.push(`asset ${i}: alt text over ${MAX_ALT_TEXT_CHARS} chars`)
    }
    if (a.width && a.height) {
      const ratio = a.width / a.height
      if (contentType === 'post' || contentType === 'carousel') {
        if (a.kind === 'image' && (ratio < 0.8 - 1e-9 || ratio > 1.91 + 1e-9)) {
          problems.push(`asset ${i}: image ratio ${ratio.toFixed(2)} outside Instagram's 0.80-1.91 feed range`)
        } else if (Math.abs(ratio - 0.8) > 0.01) {
          warnings.push(`asset ${i}: ratio ${ratio.toFixed(2)} — 4:5 (0.80) is the preferred feed format`)
        }
      }
      if ((contentType === 'reel' || contentType === 'story') && Math.abs(ratio - 9 / 16) > 0.02) {
        warnings.push(`asset ${i}: ratio ${ratio.toFixed(2)} — 9:16 (0.5625) is the ${contentType} format`)
      }
    }
  }
  return { ok: problems.length === 0, problems, warnings }
}

// ---------------------------------------------------------------------------
// Container state machine
// ---------------------------------------------------------------------------

export type ContainerAction = 'wait' | 'publish' | 'fail' | 'recreate' | 'already-published'

/**
 * One place answers "the container says X — now what". EXPIRED maps to
 * recreate (Meta expires unpublished containers after ~24h; the media is
 * still in blob storage, so a fresh container is cheap and safe). PUBLISHED
 * maps to already-published so a crashed-after-publish retry becomes a no-op
 * instead of a duplicate.
 */
export function containerNextAction(status: IgContainerStatus): ContainerAction {
  switch (status) {
    case 'FINISHED': return 'publish'
    case 'IN_PROGRESS': return 'wait'
    case 'ERROR': return 'fail'
    case 'EXPIRED': return 'recreate'
    case 'PUBLISHED': return 'already-published'
  }
}

export function normalizeContainerStatus(raw: string | undefined): IgContainerStatus | null {
  if (!raw) return null
  const s = raw.toUpperCase()
  return (['IN_PROGRESS', 'FINISHED', 'ERROR', 'EXPIRED', 'PUBLISHED'] as const).find(v => v === s) ?? null
}

// ---------------------------------------------------------------------------
// Backoff — same shape as lib/callback/settlement-queue.ts, faster base
// ---------------------------------------------------------------------------

export const MAX_PUBLISH_ATTEMPTS = 8
export const BASE_BACKOFF_MS = 15_000
export const MAX_BACKOFF_MS = 10 * 60_000

export function backoffMs(attempts: number): number {
  const ms = BASE_BACKOFF_MS * 2 ** Math.max(0, attempts - 1)
  return Math.min(ms, MAX_BACKOFF_MS)
}

export function nextRunAfter(attempts: number, now: Date = new Date()): Date {
  return new Date(now.getTime() + backoffMs(attempts))
}

export function hasGivenUp(attempts: number): boolean {
  return attempts >= MAX_PUBLISH_ATTEMPTS
}

// ---------------------------------------------------------------------------
// Quota
// ---------------------------------------------------------------------------

/** Parse GET /{ig-user-id}/content_publishing_limit?fields=config,quota_usage */
export function parseQuota(body: unknown): IgQuota | null {
  const row = (body as { data?: Array<{ config?: { quota_total?: number }; quota_usage?: number }> })
    ?.data?.[0]
  if (!row || typeof row.quota_usage !== 'number') return null
  const total = row.config?.quota_total
  if (typeof total !== 'number') return null
  return { quotaTotal: total, quotaUsage: row.quota_usage, remaining: Math.max(0, total - row.quota_usage) }
}

// ---------------------------------------------------------------------------
// Graph call plans (pure) — executed by publish-server, shown by preview
// ---------------------------------------------------------------------------

const IG_MEDIA_TYPE_BY_CONTENT: Record<SocialJob['contentType'], IgMediaType | null> = {
  post: null, // image posts pass no media_type
  reel: 'REELS',
  story: 'STORIES',
  carousel: 'CAROUSEL',
}

export function containerParamsFor(job: SocialJob, asset: SocialMediaAsset, opts?: {
  carouselItem?: boolean
}): Record<string, string> {
  const params: Record<string, string> = {}
  const mediaType = IG_MEDIA_TYPE_BY_CONTENT[job.contentType]

  if (opts?.carouselItem) {
    params.is_carousel_item = 'true'
    if (asset.kind === 'video') params.media_type = 'VIDEO'
  } else if (job.contentType === 'story') {
    params.media_type = 'STORIES'
  } else if (mediaType && job.contentType !== 'carousel') {
    params.media_type = mediaType
  }

  if (asset.kind === 'video') params.video_url = asset.url
  else params.image_url = asset.url

  if (!opts?.carouselItem && job.contentType !== 'story') {
    if (job.caption) params.caption = job.caption
  }
  if (asset.altText) params.alt_text = asset.altText
  if (asset.kind === 'video' && asset.coverUrl) params.cover_url = asset.coverUrl
  if (job.contentType === 'reel' && job.shareToFeed !== undefined) {
    params.share_to_feed = String(job.shareToFeed)
  }
  return params
}

export function carouselParentParams(job: SocialJob, childIds: string[]): Record<string, string> {
  const params: Record<string, string> = {
    media_type: 'CAROUSEL',
    children: childIds.join(','),
  }
  if (job.caption) params.caption = job.caption
  return params
}

/**
 * Dry-run preview: the exact call sequence advance() will make, with the
 * access token never present (previews get logged and pasted into approvals).
 */
export function buildPreview(job: SocialJob, igUserId: string): PublishPreview {
  const calls: PublishPreviewCall[] = []
  const capV = validateCaption(job.caption)
  const assetV = validateAssets(job.contentType, job.assets)
  const warnings = [...capV.problems, ...capV.warnings, ...assetV.problems, ...assetV.warnings]

  if (job.contentType === 'carousel') {
    for (const asset of job.assets) {
      calls.push({ method: 'POST', path: `/${igUserId}/media`, params: containerParamsFor(job, asset, { carouselItem: true }) })
    }
    calls.push({ method: 'POST', path: `/${igUserId}/media`, params: carouselParentParams(job, job.assets.map((_, i) => `<child-${i + 1}>`)) })
  } else {
    calls.push({ method: 'POST', path: `/${igUserId}/media`, params: containerParamsFor(job, job.assets[0]) })
  }
  calls.push({ method: 'GET', path: '/<container-id>', params: { fields: 'status_code' } })
  calls.push({ method: 'POST', path: `/${igUserId}/media_publish`, params: { creation_id: '<container-id>' } })

  return { platform: 'instagram', contentType: job.contentType, calls, warnings }
}

// ---------------------------------------------------------------------------
// Idempotency
// ---------------------------------------------------------------------------

/**
 * The queue's UNIQUE business key. One content row publishes to one platform
 * at most once — the DB constraint, not application logic, is what makes a
 * double-enqueue harmless (copied from settlement_queue's UNIQUE task_id).
 */
export function publishBusinessKey(job: Pick<SocialJob, 'contentId' | 'platform'>): string {
  return `${job.platform}:${job.contentId}`
}
