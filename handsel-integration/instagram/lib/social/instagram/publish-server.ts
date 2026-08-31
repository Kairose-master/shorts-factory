/**
 * Instagram publishing orchestration — the provider behind SocialPublisher.
 *
 * Design decision worth stating: advance() performs AT MOST ONE remote
 * mutation per call and returns the updated job for the queue to persist.
 * The alternative — a single publishJob() that loops create→poll→publish
 * internally — was rejected because a serverless function dying mid-loop
 * leaves no record of which step happened; with one-step advancement every
 * state transition is durably recorded before the next remote call, which is
 * what makes retries idempotent instead of duplicate-producing.
 *
 * Idempotency ladder (checked in order):
 *   1. job.remoteMediaId set        -> PUBLISHED, no calls made
 *   2. job.containerId set          -> poll it; publish only on FINISHED
 *   3. neither                      -> create container(s)
 * Meta's "already published" error at step 2/3 races is mapped to success by
 * errors.ts#looksAlreadyPublished — never to a fresh container.
 */

import type { PublishPreview, SocialJob, SocialPublisher } from '../types'
import {
  buildPreview,
  carouselParentParams,
  containerNextAction,
  containerParamsFor,
  normalizeContainerStatus,
  parseQuota,
  validateAssets,
  validateCaption,
} from './core'
import { InstagramApiError, looksAlreadyPublished } from './errors'
import { graphCall } from './client-server'
import { isInstagramConfigured, NOT_CONFIGURED_REASON, resolveInstagramConfig } from './auth-server'
import type {
  IgContainerResponse,
  IgMediaInsights,
  IgPublishResponse,
  IgQuota,
  IgStatusResponse,
} from './types'

function failed(job: SocialJob, status: SocialJob['status'], error: string): SocialJob {
  return { ...job, status, error }
}

function fromIgError(job: SocialJob, e: unknown): SocialJob {
  if (e instanceof InstagramApiError) {
    if (looksAlreadyPublished(e)) {
      return { ...job, status: 'PUBLISHED', publishedAt: new Date().toISOString(), error: undefined }
    }
    if (e.classification === 'auth') return failed(job, 'NEEDS_AUTH', e.message)
    if (e.classification === 'permanent') return failed(job, 'FAILED', e.message)
    // transient errors that exhausted client-side retries: keep status, let the
    // queue's attempt counter and run_after decide whether to try again
    return { ...job, error: e.message }
  }
  return failed(job, 'FAILED', String((e as Error)?.message ?? e).slice(0, 300))
}

export const instagramPublisher: SocialPublisher = {
  platform: 'instagram',
  isConfigured: isInstagramConfigured,

  preview(job: SocialJob): PublishPreview {
    // Account id in previews is cosmetic; a placeholder keeps preview() sync
    // and callable with zero configuration (dry-run must never need a token).
    return buildPreview(job, process.env.INSTAGRAM_ACCOUNT_ID || '<ig-account-id>')
  },

  async advance(job: SocialJob): Promise<SocialJob> {
    const cfg = await resolveInstagramConfig()
    if (!cfg) return failed(job, 'NEEDS_AUTH', NOT_CONFIGURED_REASON)

    // 1. Already published: terminal no-op.
    if (job.remoteMediaId) {
      return { ...job, status: 'PUBLISHED' }
    }

    // Validation is re-checked on every advance — media can be swapped in the
    // DB between ticks, and a swapped-after-approval asset must not ride an
    // approval it never received (the queue compares asset hashes upstream;
    // this is the second gate).
    const capV = validateCaption(job.caption)
    const assetV = validateAssets(job.contentType, job.assets)
    if (!capV.ok || !assetV.ok) {
      return failed(job, 'FAILED', [...capV.problems, ...assetV.problems].join('; '))
    }

    try {
      // 2. Container exists: poll, then publish when ready.
      if (job.containerId) {
        const statusBody = await graphCall<IgStatusResponse>(cfg, {
          method: 'GET',
          path: `/${job.containerId}`,
          params: { fields: 'status_code' },
        })
        const status = normalizeContainerStatus(statusBody.status_code)
        if (!status) return failed(job, 'FAILED', `unrecognized container status: ${String(statusBody.status_code)}`)

        switch (containerNextAction(status)) {
          case 'wait':
            return { ...job, status: 'PROCESSING' }
          case 'fail':
            return failed(job, 'FAILED', `container ${job.containerId} reported ERROR`)
          case 'recreate':
            // Meta expired the unpublished container; clear it so the next
            // advance creates a fresh one from the same (still-stored) media.
            return { ...job, status: 'EXPIRED', containerId: undefined, error: 'container expired; will recreate' }
          case 'already-published':
            return { ...job, status: 'PUBLISHED', publishedAt: new Date().toISOString() }
          case 'publish': {
            const published = await graphCall<IgPublishResponse>(cfg, {
              method: 'POST',
              path: `/${cfg.accountId}/media_publish`,
              params: { creation_id: job.containerId },
            })
            return {
              ...job,
              status: 'PUBLISHED',
              remoteMediaId: published.id,
              publishedAt: new Date().toISOString(),
              error: undefined,
            }
          }
        }
      }

      // 3. No container yet: create one (carousel = children first, then parent).
      if (job.contentType === 'carousel') {
        const childIds: string[] = []
        for (const asset of job.assets) {
          const child = await graphCall<IgContainerResponse>(cfg, {
            method: 'POST',
            path: `/${cfg.accountId}/media`,
            params: containerParamsFor(job, asset, { carouselItem: true }),
          })
          childIds.push(child.id)
        }
        const parent = await graphCall<IgContainerResponse>(cfg, {
          method: 'POST',
          path: `/${cfg.accountId}/media`,
          params: carouselParentParams(job, childIds),
        })
        return { ...job, status: 'PROCESSING', containerId: parent.id, error: undefined }
      }

      const container = await graphCall<IgContainerResponse>(cfg, {
        method: 'POST',
        path: `/${cfg.accountId}/media`,
        params: containerParamsFor(job, job.assets[0]),
      })
      return { ...job, status: 'PROCESSING', containerId: container.id, error: undefined }
    } catch (e) {
      return fromIgError(job, e)
    }
  },
}

/** GET the account's publishing quota. Null when unconfigured or unparsable. */
export async function getPublishQuota(): Promise<IgQuota | null> {
  const cfg = await resolveInstagramConfig()
  if (!cfg) return null
  try {
    const body = await graphCall<unknown>(cfg, {
      method: 'GET',
      path: `/${cfg.accountId}/content_publishing_limit`,
      params: { fields: 'config,quota_usage' },
    })
    return parseQuota(body)
  } catch {
    return null
  }
}

/** Basic engagement metrics for a published media id. Null when unavailable. */
export async function getMediaInsights(mediaId: string): Promise<IgMediaInsights | null> {
  const cfg = await resolveInstagramConfig()
  if (!cfg) return null
  try {
    const body = await graphCall<{ data?: Array<{ name?: string; values?: Array<{ value?: number }> }> }>(cfg, {
      method: 'GET',
      path: `/${mediaId}/insights`,
      params: { metric: 'reach,likes,comments,saved,shares,views' },
    })
    const metrics: Record<string, number> = {}
    for (const row of body.data ?? []) {
      const v = row.values?.[0]?.value
      if (typeof row.name === 'string' && typeof v === 'number') metrics[row.name] = v
    }
    return { mediaId, metrics }
  } catch {
    return null
  }
}
