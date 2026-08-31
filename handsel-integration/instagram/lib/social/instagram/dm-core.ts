/**
 * Pure logic for comment-triggered Instagram DMs (Private Replies).
 *
 * Policy this file enforces by construction, not by convention:
 *
 *  1. COMMENT-TRIGGERED ONLY. There is no code path that produces a DM to a
 *     user who did not comment on our own media. Cold outreach is not a
 *     feature we chose not to use; it is a feature this module cannot do —
 *     the send call requires a comment_id, and comment ids only arrive via
 *     the comments webhook.
 *  2. ONE DM PER PERSON PER CAMPAIGN, EVER. The dedupe key is (user, campaign)
 *     with no expiry. A person who commented on five posts gets one DM.
 *  3. FRESHNESS. Meta rejects private replies to comments older than 7 days;
 *     we stop at 6 to never race the boundary.
 *  4. HONESTY. Templates must self-identify as the Handsel account team and
 *     contain no claim outside the model file; the campaign-approval prompt
 *     (prompts/dm-reply-generation.md) is the editorial gate, and campaigns —
 *     not individual DMs — are what a human approves.
 *  5. NEGATIVE/COMPLAINT COMMENTS GO TO A HUMAN. Triage routes them out of
 *     the promo path entirely; a promo DM under an angry comment is how a
 *     brand account earns a screenshot.
 */

import { createHmac, timingSafeEqual } from 'node:crypto'

// ---------------------------------------------------------------------------
// Webhook payload normalization
// ---------------------------------------------------------------------------

export interface CommentEvent {
  commentId: string
  mediaId: string
  text: string
  fromId: string
  fromUsername: string
  /** epoch ms of the comment (webhook entry time when field-level ts absent) */
  timestampMs: number
}

/**
 * Normalize a Meta comments-webhook POST body into CommentEvents.
 * Unknown shapes yield [] — a webhook must never 500 over a payload we don't
 * recognize (Meta disables endpoints that error repeatedly).
 */
export function parseCommentWebhook(body: unknown): CommentEvent[] {
  const out: CommentEvent[] = []
  const root = body as { object?: string; entry?: unknown[] } | null
  if (!root || root.object !== 'instagram' || !Array.isArray(root.entry)) return out
  for (const entry of root.entry) {
    const e = entry as { time?: number; changes?: unknown[] }
    for (const change of e.changes ?? []) {
      const c = change as {
        field?: string
        value?: {
          id?: string
          media?: { id?: string }
          text?: string
          from?: { id?: string; username?: string }
          timestamp?: number | string
        }
      }
      if (c.field !== 'comments' || !c.value) continue
      const v = c.value
      if (!v.id || !v.from?.id) continue
      const ts = typeof v.timestamp === 'string' ? Date.parse(v.timestamp) : v.timestamp
      out.push({
        commentId: v.id,
        mediaId: v.media?.id ?? '',
        text: v.text ?? '',
        fromId: v.from.id,
        fromUsername: v.from.username ?? '',
        timestampMs: Number.isFinite(ts) && ts! > 0 ? Number(ts) : (e.time ? e.time * 1000 : Date.now()),
      })
    }
  }
  return out
}

/**
 * X-Hub-Signature-256 verification. Constant-time compare; a missing or
 * malformed header is a plain false, never a throw — the route turns false
 * into 401 and logs nothing attacker-controlled.
 */
export function verifyWebhookSignature(appSecret: string, rawBody: string, signatureHeader: string | null): boolean {
  if (!signatureHeader?.startsWith('sha256=')) return false
  const expected = createHmac('sha256', appSecret).update(rawBody, 'utf8').digest('hex')
  const given = signatureHeader.slice('sha256='.length)
  if (given.length !== expected.length) return false
  try {
    return timingSafeEqual(Buffer.from(given, 'hex'), Buffer.from(expected, 'hex'))
  } catch {
    return false
  }
}

// ---------------------------------------------------------------------------
// Triage + trigger matching
// ---------------------------------------------------------------------------

export interface DmCampaign {
  id: string
  /** case-insensitive whole-word triggers, e.g. ['handsel', 'link', 'proof'] */
  triggers: string[]
  /** approved template; {{username}} and {{link}} are the only variables */
  template: string
  link: string
  /** true = any comment on the campaign's media qualifies, triggers ignored */
  anyComment?: boolean
  /** restrict to specific media ids; empty = all account media */
  mediaIds?: string[]
}

export type TriageVerdict = 'reply' | 'human' | 'ignore'

const NEGATIVE_MARKERS = /\b(scam|fraud|rug|stolen|refund|lawsuit|report(?:ed|ing)?|hate|angry|broken|doesn'?t work|worst)\b/i

/**
 * Route a comment: negative/complaint -> human, matching trigger -> reply,
 * everything else -> ignore. "Promote to everyone who commented" is expressed
 * as a campaign with anyComment=true — still comment-triggered, still deduped,
 * still triaged for negativity first.
 */
export function triageComment(event: CommentEvent, campaigns: DmCampaign[], selfAccountId: string): {
  verdict: TriageVerdict
  campaign?: DmCampaign
  reason: string
} {
  if (event.fromId === selfAccountId) return { verdict: 'ignore', reason: 'own comment (echo)' }
  if (!event.text.trim()) return { verdict: 'ignore', reason: 'empty comment' }
  if (NEGATIVE_MARKERS.test(event.text)) return { verdict: 'human', reason: 'negative/complaint marker — human review' }

  for (const campaign of campaigns) {
    if (campaign.mediaIds?.length && !campaign.mediaIds.includes(event.mediaId)) continue
    if (campaign.anyComment) return { verdict: 'reply', campaign, reason: 'campaign accepts any comment' }
    const words = event.text.toLowerCase()
    if (campaign.triggers.some(t => new RegExp(`(?:^|\\W)${escapeRegExp(t.toLowerCase())}(?:$|\\W)`).test(words))) {
      return { verdict: 'reply', campaign, reason: `trigger matched (${campaign.id})` }
    }
  }
  return { verdict: 'ignore', reason: 'no campaign matched' }
}

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

// ---------------------------------------------------------------------------
// Freshness, dedupe, rate limit, template
// ---------------------------------------------------------------------------

/** Meta's private-reply window is 7 days; we stop a day early. */
export const MAX_COMMENT_AGE_MS = 6 * 24 * 60 * 60 * 1000
/** Per-hour outbound DM ceiling — far under Meta's limits, deliberately. */
export const MAX_DMS_PER_HOUR = 20

export function isCommentFresh(event: Pick<CommentEvent, 'timestampMs'>, now: number = Date.now()): boolean {
  return now - event.timestampMs <= MAX_COMMENT_AGE_MS
}

/** UNIQUE key in social_dm_log: one DM per person per campaign, forever. */
export function dmDedupeKey(fromId: string, campaignId: string): string {
  return `${campaignId}:${fromId}`
}

export const DM_MAX_CHARS = 1000

export function renderDmTemplate(campaign: DmCampaign, event: CommentEvent): { text: string; problems: string[] } {
  const problems: string[] = []
  const text = campaign.template
    .replaceAll('{{username}}', event.fromUsername || 'there')
    .replaceAll('{{link}}', campaign.link)
  if (/\{\{[^}]+\}\}/.test(text)) problems.push('template contains an unknown variable')
  if (text.length > DM_MAX_CHARS) problems.push(`rendered DM is ${text.length} chars (max ${DM_MAX_CHARS})`)
  // Self-identification must live in the words, not smuggled in via the link
  // URL — check the template body with the link variable blanked out.
  if (!/handsel/i.test(campaign.template.replaceAll('{{link}}', ''))) {
    problems.push('DM must self-identify as Handsel')
  }
  return { text, problems }
}
