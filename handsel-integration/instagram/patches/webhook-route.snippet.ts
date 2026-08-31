/**
 * PATCH → app/api/webhooks/instagram/route.ts (new file in the Handsel repo).
 *
 * Meta's comments webhook. Two contracts to honor:
 *  - GET: subscription verification handshake (hub.challenge echo).
 *  - POST: MUST return 200 fast, always — repeated non-200s get the
 *    subscription disabled. So: verify signature, parse, handle inline (the
 *    work is one small DB roundtrip + at most one Graph call), and never
 *    throw past the try/catch.
 * Campaigns: load from the social_dm_campaigns table (or a config module) —
 * a campaign row is created only after its template passed the
 * dm-reply-generation approval gate.
 */
import { NextRequest, NextResponse } from 'next/server'
import { parseCommentWebhook, verifyWebhookSignature } from '@/lib/social/instagram/dm-core'
import { handleCommentEvent, isDmAutomationEnabled } from '@/lib/social/instagram/dm-server'
import { pool } from '@/lib/db'
import { loadDmCampaigns } from '@/lib/social/instagram/dm-campaigns-server' // your campaign source

export async function GET(request: NextRequest) {
  const url = new URL(request.url)
  const mode = url.searchParams.get('hub.mode')
  const token = url.searchParams.get('hub.verify_token')
  const challenge = url.searchParams.get('hub.challenge')
  if (mode === 'subscribe' && token && token === process.env.INSTAGRAM_WEBHOOK_VERIFY_TOKEN) {
    return new NextResponse(challenge ?? '', { status: 200 })
  }
  return new NextResponse('forbidden', { status: 403 })
}

export async function POST(request: NextRequest) {
  const raw = await request.text()
  const secret = process.env.META_APP_SECRET
  if (!secret || !verifyWebhookSignature(secret, raw, request.headers.get('x-hub-signature-256'))) {
    return new NextResponse('bad signature', { status: 401 })
  }
  try {
    if (isDmAutomationEnabled()) {
      const events = parseCommentWebhook(JSON.parse(raw))
      const campaigns = await loadDmCampaigns(pool)
      for (const event of events) {
        // sequential + structured results; a failure is a log line, not a 500
        await handleCommentEvent(pool, event, campaigns)
      }
    }
  } catch {
    // swallow: Meta retries on non-200; our own errors are in social_dm_log
  }
  return NextResponse.json({ ok: true })
}
