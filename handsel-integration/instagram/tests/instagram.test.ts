/**
 * Pure-function tests for the Instagram provider, per the repo convention:
 * test the response→domain mappers and decision functions, never the fetch
 * (tests/clawhub.test.ts is the exemplar; the network path is covered by
 * instagram.e2e.test.ts with a real local HTTP server).
 */
import { describe, expect, it } from 'vitest'

import {
  backoffMs,
  buildPreview,
  containerNextAction,
  containerParamsFor,
  carouselParentParams,
  countHashtags,
  hasGivenUp,
  MAX_CAPTION_CHARS,
  MAX_PUBLISH_ATTEMPTS,
  normalizeContainerStatus,
  parseQuota,
  publishBusinessKey,
  validateAssets,
  validateCaption,
} from '../lib/social/instagram/core'
import { classifyIgError, igErrorFromBody, looksAlreadyPublished } from '../lib/social/instagram/errors'
import { describeSocialJob, isDue, rowStatusAfterAdvance } from '../lib/social/instagram/queue'
import type { SocialJob } from '../lib/social/types'

const baseJob = (over: Partial<SocialJob> = {}): SocialJob => ({
  id: 'sj-1',
  contentId: 'c-1',
  platform: 'instagram',
  contentType: 'post',
  assets: [{ url: 'https://x.public.blob.vercel-storage.com/a.png', kind: 'image', width: 1080, height: 1350 }],
  caption: 'Two robots agreed on a price. #handsel',
  status: 'QUEUED',
  retryCount: 0,
  createdAt: new Date().toISOString(),
  ...over,
})

describe('caption validation', () => {
  it('accepts a normal caption', () => {
    expect(validateCaption('hello #one #two').ok).toBe(true)
  })
  it('rejects over-length captions', () => {
    const v = validateCaption('x'.repeat(MAX_CAPTION_CHARS + 1))
    expect(v.ok).toBe(false)
    expect(v.problems[0]).toMatch(/2200/)
  })
  it('rejects more than 30 hashtags', () => {
    const caption = Array.from({ length: 31 }, (_, i) => `#t${i}`).join(' ')
    expect(countHashtags(caption)).toBe(31)
    expect(validateCaption(caption).ok).toBe(false)
  })
  it('rejects control characters', () => {
    expect(validateCaption('bad\u0007caption').ok).toBe(false)
  })
  it('counts unicode hashtags', () => {
    expect(countHashtags('#코딩 #ai_에이전트 plain')).toBe(2)
  })
})

describe('asset validation', () => {
  it('flags a 16:9 image on a feed post as a hard problem beyond 1.91', () => {
    const v = validateAssets('post', [{ url: 'https://a/b.png', kind: 'image', width: 2000, height: 1000 }])
    expect(v.ok).toBe(false)
  })
  it('prefers 4:5 with only a warning for square', () => {
    const v = validateAssets('post', [{ url: 'https://a/b.png', kind: 'image', width: 1080, height: 1080 }])
    expect(v.ok).toBe(true)
    expect(v.warnings.join(' ')).toMatch(/4:5/)
  })
  it('requires video for reels', () => {
    const v = validateAssets('reel', [{ url: 'https://a/b.png', kind: 'image' }])
    expect(v.problems.join(' ')).toMatch(/video/)
  })
  it('enforces carousel child count', () => {
    expect(validateAssets('carousel', [{ url: 'https://a/1.png', kind: 'image' }]).ok).toBe(false)
    const eleven = Array.from({ length: 11 }, (_, i) => ({ url: `https://a/${i}.png`, kind: 'image' as const }))
    expect(validateAssets('carousel', eleven).ok).toBe(false)
  })
  it('rejects http URLs', () => {
    expect(validateAssets('post', [{ url: 'http://a/b.png', kind: 'image' }]).ok).toBe(false)
  })
})

describe('container state machine', () => {
  it('maps each status to exactly one action', () => {
    expect(containerNextAction('FINISHED')).toBe('publish')
    expect(containerNextAction('IN_PROGRESS')).toBe('wait')
    expect(containerNextAction('ERROR')).toBe('fail')
    expect(containerNextAction('EXPIRED')).toBe('recreate')
    expect(containerNextAction('PUBLISHED')).toBe('already-published')
  })
  it('normalizes case and rejects junk', () => {
    expect(normalizeContainerStatus('finished')).toBe('FINISHED')
    expect(normalizeContainerStatus('NOPE')).toBeNull()
    expect(normalizeContainerStatus(undefined)).toBeNull()
  })
})

describe('backoff schedule', () => {
  it('doubles from 15s and caps at 10min', () => {
    expect(backoffMs(1)).toBe(15_000)
    expect(backoffMs(2)).toBe(30_000)
    expect(backoffMs(3)).toBe(60_000)
    expect(backoffMs(10)).toBe(10 * 60_000)
  })
  it('gives up at the attempt ceiling', () => {
    expect(hasGivenUp(MAX_PUBLISH_ATTEMPTS - 1)).toBe(false)
    expect(hasGivenUp(MAX_PUBLISH_ATTEMPTS)).toBe(true)
  })
})

describe('quota parsing', () => {
  it('parses the documented shape', () => {
    const q = parseQuota({ data: [{ config: { quota_total: 25 }, quota_usage: 3 }] })
    expect(q).toEqual({ quotaTotal: 25, quotaUsage: 3, remaining: 22 })
  })
  it('returns null for malformed bodies', () => {
    expect(parseQuota({})).toBeNull()
    expect(parseQuota({ data: [{}] })).toBeNull()
    expect(parseQuota(null)).toBeNull()
  })
})

describe('container params', () => {
  it('builds a reel container with share_to_feed and cover', () => {
    const job = baseJob({
      contentType: 'reel',
      shareToFeed: true,
      assets: [{ url: 'https://a/v.mp4', kind: 'video', coverUrl: 'https://a/c.jpg' }],
    })
    const p = containerParamsFor(job, job.assets[0])
    expect(p.media_type).toBe('REELS')
    expect(p.video_url).toBe('https://a/v.mp4')
    expect(p.cover_url).toBe('https://a/c.jpg')
    expect(p.share_to_feed).toBe('true')
  })
  it('stories get STORIES and no caption', () => {
    const job = baseJob({ contentType: 'story' })
    const p = containerParamsFor(job, job.assets[0])
    expect(p.media_type).toBe('STORIES')
    expect(p.caption).toBeUndefined()
  })
  it('carousel items are marked and the parent carries children', () => {
    const job = baseJob({ contentType: 'carousel' })
    const child = containerParamsFor(job, job.assets[0], { carouselItem: true })
    expect(child.is_carousel_item).toBe('true')
    const parent = carouselParentParams(job, ['1', '2'])
    expect(parent).toMatchObject({ media_type: 'CAROUSEL', children: '1,2' })
  })
  it('plain image post passes no media_type', () => {
    const p = containerParamsFor(baseJob(), baseJob().assets[0])
    expect(p.media_type).toBeUndefined()
    expect(p.image_url).toBeDefined()
  })
})

describe('preview (dry run)', () => {
  it('lists container -> poll -> publish and never a token', () => {
    const preview = buildPreview(baseJob(), '17841400000000000')
    expect(preview.calls.map(c => c.path)).toEqual([
      '/17841400000000000/media',
      '/<container-id>',
      '/17841400000000000/media_publish',
    ])
    expect(JSON.stringify(preview)).not.toMatch(/access_token/)
  })
  it('surfaces validation warnings', () => {
    const bad = baseJob({ caption: 'x'.repeat(3000) })
    expect(buildPreview(bad, 'id').warnings.length).toBeGreaterThan(0)
  })
})

describe('error classification', () => {
  it('classifies auth codes', () => {
    expect(classifyIgError(400, 190)).toBe('auth')
    expect(classifyIgError(400, 102)).toBe('auth')
  })
  it('classifies throttling and 5xx as transient', () => {
    expect(classifyIgError(400, 4)).toBe('transient')
    expect(classifyIgError(503)).toBe('transient')
    expect(classifyIgError(429)).toBe('transient')
  })
  it('defaults unknown 4xx to permanent', () => {
    expect(classifyIgError(400, 100)).toBe('permanent')
    expect(classifyIgError(400)).toBe('permanent')
  })
  it('parses Graph error bodies', () => {
    const e = igErrorFromBody(400, { error: { message: 'Invalid parameter', code: 100, error_subcode: 2207005, fbtrace_id: 'F' } })
    expect(e.code).toBe(100)
    expect(e.classification).toBe('permanent')
    expect(e.message).toMatch(/Invalid parameter/)
  })
  it('detects already-published by subcode and by message', () => {
    expect(looksAlreadyPublished(igErrorFromBody(400, { error: { code: 100, error_subcode: 2207032 } }))).toBe(true)
    expect(looksAlreadyPublished(igErrorFromBody(400, { error: { message: 'Media is already published' } }))).toBe(true)
    expect(looksAlreadyPublished(igErrorFromBody(400, { error: { message: 'nope' } }))).toBe(false)
  })
})

describe('queue row transitions', () => {
  it('published -> done', () => {
    expect(rowStatusAfterAdvance(baseJob({ status: 'PUBLISHED' }), 1, false)).toBe('done')
  })
  it('failed and needs-auth -> abandoned', () => {
    expect(rowStatusAfterAdvance(baseJob({ status: 'FAILED' }), 1, false)).toBe('abandoned')
    expect(rowStatusAfterAdvance(baseJob({ status: 'NEEDS_AUTH' }), 1, false)).toBe('abandoned')
  })
  it('processing stays pending until give-up', () => {
    expect(rowStatusAfterAdvance(baseJob({ status: 'PROCESSING' }), 3, false)).toBe('pending')
    expect(rowStatusAfterAdvance(baseJob({ status: 'PROCESSING' }), 8, true)).toBe('abandoned')
  })
  it('expired container stays pending (recreate is cheap)', () => {
    expect(rowStatusAfterAdvance(baseJob({ status: 'EXPIRED' }), 2, false)).toBe('pending')
  })
})

describe('scheduling', () => {
  const now = new Date('2026-09-01T12:00:00Z')
  it('future scheduled_at is not due even when run_after passed', () => {
    expect(isDue({ scheduledAt: '2026-09-02T00:00:00Z' }, new Date('2026-09-01T00:00:00Z'), now)).toBe(false)
  })
  it('due when both gates passed', () => {
    expect(isDue({ scheduledAt: '2026-09-01T00:00:00Z' }, new Date('2026-09-01T00:00:00Z'), now)).toBe(true)
    expect(isDue({}, new Date('2026-09-01T00:00:00Z'), now)).toBe(true)
  })
  it('future run_after is not due', () => {
    expect(isDue({}, new Date('2026-09-02T00:00:00Z'), now)).toBe(false)
  })
})

describe('idempotency key + description', () => {
  it('one content row maps to one business key per platform', () => {
    expect(publishBusinessKey({ platform: 'instagram', contentId: 'c-9' })).toBe('instagram:c-9')
  })
  it('describes terminal states with the interesting fact first', () => {
    expect(describeSocialJob(baseJob({ status: 'PUBLISHED', remoteMediaId: '18001' }), 2)).toMatch(/18001/)
    expect(describeSocialJob(baseJob({ status: 'NEEDS_AUTH', error: 'graph 400: bad token' }), 1)).toMatch(/re-auth/)
  })
})
