/**
 * End-to-end provider tests against a REAL local HTTP server standing in for
 * graph.facebook.com — the repo's convention for network coverage (see
 * tests/mcp-client.e2e.test.ts): no fetch mocks, ever. The fake implements
 * just enough Graph surface to exercise every lifecycle branch: container
 * creation, status polling, publish, quota, and each documented error class.
 */
import { afterAll, afterEach, beforeAll, describe, expect, it } from 'vitest'
import { createServer, type Server } from 'node:http'
import type { AddressInfo } from 'node:net'

import { instagramPublisher, getPublishQuota } from '../lib/social/instagram/publish-server'
import type { SocialJob } from '../lib/social/types'

interface Scenario {
  /** container status_code sequence returned by successive polls */
  statuses: string[]
  /** error body to return on the next media (container-create) call, if any */
  createError?: { status: number; body: unknown }
  publishError?: { status: number; body: unknown }
}

let server: Server
let origin: string
let scenario: Scenario
let requests: Array<{ method: string; path: string }>
let pollIndex: number

function resetScenario(s: Partial<Scenario> = {}) {
  scenario = { statuses: ['FINISHED'], ...s }
  requests = []
  pollIndex = 0
}

beforeAll(async () => {
  server = createServer((req, res) => {
    const url = new URL(req.url ?? '/', 'http://x')
    requests.push({ method: req.method ?? 'GET', path: url.pathname })
    const send = (status: number, body: unknown) => {
      res.writeHead(status, { 'content-type': 'application/json' })
      res.end(JSON.stringify(body))
    }

    if (req.method === 'POST' && url.pathname.endsWith('/media')) {
      if (scenario.createError) return send(scenario.createError.status, scenario.createError.body)
      return send(200, { id: `container-${requests.length}` })
    }
    if (req.method === 'POST' && url.pathname.endsWith('/media_publish')) {
      if (scenario.publishError) return send(scenario.publishError.status, scenario.publishError.body)
      return send(200, { id: 'media-777' })
    }
    if (req.method === 'GET' && url.pathname.includes('content_publishing_limit')) {
      return send(200, { data: [{ config: { quota_total: 25 }, quota_usage: 5 }] })
    }
    if (req.method === 'GET' && url.searchParams.get('fields') === 'status_code') {
      const status = scenario.statuses[Math.min(pollIndex, scenario.statuses.length - 1)]
      pollIndex++
      return send(200, { id: url.pathname.slice(1), status_code: status })
    }
    return send(404, { error: { message: 'unknown route', code: 803 } })
  })
  await new Promise<void>(r => server.listen(0, '127.0.0.1', r))
  origin = `http://127.0.0.1:${(server.address() as AddressInfo).port}`
  process.env.INSTAGRAM_GRAPH_ORIGIN = origin
  process.env.INSTAGRAM_ACCESS_TOKEN = 'test-token-not-a-secret'
  process.env.INSTAGRAM_ACCOUNT_ID = '17841400000000000'
  process.env.INSTAGRAM_API_VERSION = 'v21.0'
})

afterAll(async () => {
  delete process.env.INSTAGRAM_GRAPH_ORIGIN
  delete process.env.INSTAGRAM_ACCESS_TOKEN
  delete process.env.INSTAGRAM_ACCOUNT_ID
  delete process.env.INSTAGRAM_API_VERSION
  await new Promise<void>(r => server.close(() => r()))
})

afterEach(() => resetScenario())

const job = (over: Partial<SocialJob> = {}): SocialJob => ({
  id: 'sj-e2e',
  contentId: 'c-e2e',
  platform: 'instagram',
  contentType: 'post',
  assets: [{ url: 'https://x.public.blob.vercel-storage.com/a.png', kind: 'image' }],
  caption: 'e2e #handsel',
  status: 'QUEUED',
  retryCount: 0,
  createdAt: new Date().toISOString(),
  ...over,
})

describe('image publish lifecycle', () => {
  it('creates a container, waits while processing, then publishes', async () => {
    resetScenario({ statuses: ['IN_PROGRESS', 'FINISHED'] })

    const step1 = await instagramPublisher.advance(job())
    expect(step1.status).toBe('PROCESSING')
    expect(step1.containerId).toBeDefined()

    const step2 = await instagramPublisher.advance(step1)
    expect(step2.status).toBe('PROCESSING') // IN_PROGRESS -> wait

    const step3 = await instagramPublisher.advance(step2)
    expect(step3.status).toBe('PUBLISHED')
    expect(step3.remoteMediaId).toBe('media-777')
    expect(step3.publishedAt).toBeDefined()
  })
})

describe('duplicate-publish prevention', () => {
  it('a job with a recorded media id makes zero network calls', async () => {
    resetScenario()
    const done = await instagramPublisher.advance(job({ remoteMediaId: 'media-1', status: 'PUBLISHING' }))
    expect(done.status).toBe('PUBLISHED')
    expect(requests.length).toBe(0)
  })

  it('an already-published race maps to success, not a fresh container', async () => {
    resetScenario({
      statuses: ['FINISHED'],
      publishError: { status: 400, body: { error: { message: 'Media is already published', code: 100 } } },
    })
    const withContainer = job({ containerId: 'container-race', status: 'PROCESSING' })
    const out = await instagramPublisher.advance(withContainer)
    expect(out.status).toBe('PUBLISHED')
    expect(requests.filter(r => r.method === 'POST' && r.path.endsWith('/media')).length).toBe(0)
  })
})

describe('failure classes', () => {
  it('auth failure (code 190) -> NEEDS_AUTH after a single attempt', async () => {
    resetScenario({ createError: { status: 400, body: { error: { message: 'token expired', code: 190 } } } })
    const out = await instagramPublisher.advance(job())
    expect(out.status).toBe('NEEDS_AUTH')
    expect(requests.length).toBe(1) // permanent-class: never retried
  })

  it('validation failure (code 100) -> FAILED after a single attempt', async () => {
    resetScenario({ createError: { status: 400, body: { error: { message: 'Invalid parameter', code: 100 } } } })
    const out = await instagramPublisher.advance(job())
    expect(out.status).toBe('FAILED')
    expect(requests.length).toBe(1)
  })

  it('container ERROR -> FAILED', async () => {
    resetScenario({ statuses: ['ERROR'] })
    const out = await instagramPublisher.advance(job({ containerId: 'container-x', status: 'PROCESSING' }))
    expect(out.status).toBe('FAILED')
    expect(out.error).toMatch(/ERROR/)
  })

  it('EXPIRED container clears the id for recreation', async () => {
    resetScenario({ statuses: ['EXPIRED'] })
    const out = await instagramPublisher.advance(job({ containerId: 'container-old', status: 'PROCESSING' }))
    expect(out.status).toBe('EXPIRED')
    expect(out.containerId).toBeUndefined()
  })

  it('invalid local content fails before any network call', async () => {
    resetScenario()
    const out = await instagramPublisher.advance(job({ caption: 'x'.repeat(3000) }))
    expect(out.status).toBe('FAILED')
    expect(requests.length).toBe(0)
  })
})

describe('carousel', () => {
  it('creates children then a parent container', async () => {
    resetScenario()
    const twoUp = job({
      contentType: 'carousel',
      assets: [
        { url: 'https://x.public.blob.vercel-storage.com/1.png', kind: 'image' },
        { url: 'https://x.public.blob.vercel-storage.com/2.png', kind: 'image' },
      ],
    })
    const out = await instagramPublisher.advance(twoUp)
    expect(out.status).toBe('PROCESSING')
    expect(requests.filter(r => r.method === 'POST').length).toBe(3) // 2 children + parent
  })
})

describe('quota', () => {
  it('reads and parses content_publishing_limit', async () => {
    resetScenario()
    const q = await getPublishQuota()
    expect(q).toEqual({ quotaTotal: 25, quotaUsage: 5, remaining: 20 })
  })
})

describe('unconfigured environment', () => {
  it('is a structured NEEDS_AUTH, never a throw', async () => {
    const token = process.env.INSTAGRAM_ACCESS_TOKEN
    delete process.env.INSTAGRAM_ACCESS_TOKEN
    try {
      const out = await instagramPublisher.advance(job())
      expect(out.status).toBe('NEEDS_AUTH')
      expect(out.error).toMatch(/INSTAGRAM_ACCESS_TOKEN/)
    } finally {
      process.env.INSTAGRAM_ACCESS_TOKEN = token
    }
  })
})
