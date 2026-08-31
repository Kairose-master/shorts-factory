/**
 * SocialJob — the platform-agnostic social publishing abstraction.
 *
 * Why an abstraction at all: the queue, the Local Jobs surface and the Office
 * only ever see a SocialJob. Instagram is one provider behind it. When a
 * second network arrives (X, LinkedIn), it implements SocialPublisher and
 * reuses the queue, the statuses and the approval gate unchanged — the
 * alternative (an instagram_posts table with instagram-shaped columns) was
 * rejected because it forces a rewrite the day platform #2 shows up.
 *
 * Policy boundary, stated once and loudly: Handsel has never published to a
 * third-party network before. lib/email.ts is transactional-only by policy and
 * lib/mail-desk.ts is inbound-only by policy. This module inherits the same
 * posture: nothing in this file or its providers publishes without a content
 * row that has passed the approval gate (APPROVAL_REQUIRED -> READY is a human
 * or explicit-policy transition, never an automatic one).
 */

export const SOCIAL_PLATFORMS = ['instagram'] as const
export type SocialPlatform = (typeof SOCIAL_PLATFORMS)[number]

export const SOCIAL_CONTENT_TYPES = ['post', 'carousel', 'reel', 'story'] as const
export type SocialContentType = (typeof SOCIAL_CONTENT_TYPES)[number]

/**
 * Content-queue status. DRAFT/READY/APPROVAL_REQUIRED are editorial states;
 * SCHEDULED..PUBLISHED are machine states. The editorial->machine boundary is
 * the approval gate.
 */
export const SOCIAL_CONTENT_STATUSES = [
  'DRAFT',
  'APPROVAL_REQUIRED',
  'READY',
  'SCHEDULED',
  'PUBLISHING',
  'PUBLISHED',
  'FAILED',
] as const
export type SocialContentStatus = (typeof SOCIAL_CONTENT_STATUSES)[number]

/**
 * Publishing-job lifecycle (one attempt-chain against one provider).
 * QUEUED -> PREPARING -> UPLOADING -> PROCESSING -> PUBLISHING -> PUBLISHED,
 * with FAILED / EXPIRED / NEEDS_AUTH as terminal failure states. NEEDS_AUTH is
 * separate from FAILED because retrying an expired token burns quota and
 * cannot succeed — it needs a human, not a backoff.
 */
export const SOCIAL_JOB_STATUSES = [
  'QUEUED',
  'PREPARING',
  'UPLOADING',
  'PROCESSING',
  'PUBLISHING',
  'PUBLISHED',
  'FAILED',
  'EXPIRED',
  'NEEDS_AUTH',
] as const
export type SocialJobStatus = (typeof SOCIAL_JOB_STATUSES)[number]

export interface SocialMediaAsset {
  /** Publicly reachable https URL (blob-store URL in production). */
  url: string
  kind: 'image' | 'video'
  /** Declared pixel dimensions, when known — used for aspect-ratio linting. */
  width?: number
  height?: number
  /** Alt text travels with the asset, not the caption. */
  altText?: string
  /** Reel/story cover image URL (video assets only). */
  coverUrl?: string
}

export interface SocialJob {
  id: string
  contentId: string
  platform: SocialPlatform
  contentType: SocialContentType
  assets: SocialMediaAsset[]
  caption: string
  campaign?: string
  scheduledAt?: string // ISO-8601; absent = publish at next drain
  status: SocialJobStatus
  /** Provider-side container/creation id once one exists. */
  containerId?: string
  /** Provider-side media id once published — presence makes retries no-ops. */
  remoteMediaId?: string
  retryCount: number
  createdAt: string
  publishedAt?: string
  error?: string
  /** Reel-only: also surface on the main feed grid. */
  shareToFeed?: boolean
}

/** What a provider needs to expose. Everything else lives in the queue. */
export interface SocialPublisher {
  platform: SocialPlatform
  isConfigured(): Promise<boolean>
  /** Executes exactly one drain step for the job; returns the updated job. */
  advance(job: SocialJob): Promise<SocialJob>
  /** Dry run: the exact provider calls advance() would make, without making them. */
  preview(job: SocialJob): PublishPreview
}

export interface PublishPreviewCall {
  method: 'GET' | 'POST'
  path: string
  params: Record<string, string>
}

export interface PublishPreview {
  platform: SocialPlatform
  contentType: SocialContentType
  calls: PublishPreviewCall[]
  warnings: string[]
}
