/**
 * Comment-triggered DM sending — the server sibling of dm-core.ts.
 *
 * Flow: comments webhook -> triage (pure) -> guardrails -> ONE private reply
 * via POST /{ig-user-id}/messages with recipient {comment_id} -> durable log.
 * The social_dm_log table's UNIQUE dedupe key is the anti-spam mechanism the
 * code cannot bypass; the hourly counter is checked in the same table so the
 * limit survives restarts and multiple instances.
 *
 * Feature gating follows the repo's kill-switch convention: the feature runs
 * only when INSTAGRAM_DM_ENABLED=true, and INSTAGRAM_DM_DISABLED=true always
 * wins. Enabling the flag is the standing human approval for the *mechanism*;
 * each campaign's template is separately approved through the prompt gate
 * (prompts/dm-reply-generation.md) before it enters the campaigns table.
 */

import type { QueryPort } from './queue-server'
import { resolveInstagramConfig } from './auth-server'
import { graphCall } from './client-server'
import {
  dmDedupeKey,
  isCommentFresh,
  MAX_DMS_PER_HOUR,
  renderDmTemplate,
  triageComment,
  type CommentEvent,
  type DmCampaign,
} from './dm-core'

export function isDmAutomationEnabled(): boolean {
  if (process.env.INSTAGRAM_DM_DISABLED === 'true') return false
  return process.env.INSTAGRAM_DM_ENABLED === 'true'
}

export type DmResult =
  | { sent: true; commentId: string; campaignId: string }
  | { sent: false; reason: string }

let tableReadyPromise: Promise<void> | null = null

async function ensureTable(db: QueryPort): Promise<void> {
  if (!tableReadyPromise) {
    tableReadyPromise = db
      .query(
        `CREATE TABLE IF NOT EXISTS social_dm_log (
          dedupe_key text PRIMARY KEY,
          from_id text NOT NULL,
          from_username text,
          campaign_id text NOT NULL,
          comment_id text NOT NULL,
          media_id text,
          verdict text NOT NULL,
          sent boolean NOT NULL DEFAULT false,
          error text,
          created_at timestamptz NOT NULL DEFAULT now()
        )`,
      )
      .then(() => void 0)
  }
  try {
    await tableReadyPromise
  } catch (e) {
    tableReadyPromise = null
    throw e
  }
}

async function sentInLastHour(db: QueryPort): Promise<number> {
  const { rows } = await db.query(
    `SELECT count(*)::int AS n FROM social_dm_log
     WHERE sent = true AND created_at > now() - interval '1 hour'`,
  )
  return Number(rows[0]?.n ?? 0)
}

/**
 * Handle one webhook comment event end to end. Every non-send is a structured
 * reason (logged rows included), never a throw — the webhook route must
 * always 200 fast or Meta suspends the subscription.
 */
export async function handleCommentEvent(
  db: QueryPort,
  event: CommentEvent,
  campaigns: DmCampaign[],
): Promise<DmResult> {
  if (!isDmAutomationEnabled()) return { sent: false, reason: 'dm automation disabled (INSTAGRAM_DM_ENABLED)' }
  const cfg = await resolveInstagramConfig()
  if (!cfg) return { sent: false, reason: 'instagram not configured' }

  const triage = triageComment(event, campaigns, cfg.accountId)
  if (triage.verdict !== 'reply' || !triage.campaign) {
    if (triage.verdict === 'human') {
      await ensureTable(db)
      await db.query(
        `INSERT INTO social_dm_log (dedupe_key, from_id, from_username, campaign_id, comment_id, media_id, verdict, sent)
         VALUES ($1,$2,$3,$4,$5,$6,'human',false) ON CONFLICT (dedupe_key) DO NOTHING`,
        [`human:${event.commentId}`, event.fromId, event.fromUsername, 'none', event.commentId, event.mediaId],
      )
    }
    return { sent: false, reason: triage.reason }
  }
  if (!isCommentFresh(event)) return { sent: false, reason: 'comment older than the private-reply window' }

  const { text, problems } = renderDmTemplate(triage.campaign, event)
  if (problems.length) return { sent: false, reason: `template rejected: ${problems.join('; ')}` }

  await ensureTable(db)
  if ((await sentInLastHour(db)) >= MAX_DMS_PER_HOUR) {
    return { sent: false, reason: `hourly DM ceiling (${MAX_DMS_PER_HOUR}) reached` }
  }

  // Claim the dedupe key BEFORE sending: a crash after send leaves a claimed
  // key (no duplicate later); a crash before send leaves sent=false with an
  // error for the ops report. The reverse order risks double-sending.
  const key = dmDedupeKey(event.fromId, triage.campaign.id)
  const { rows } = await db.query(
    `INSERT INTO social_dm_log (dedupe_key, from_id, from_username, campaign_id, comment_id, media_id, verdict, sent)
     VALUES ($1,$2,$3,$4,$5,$6,'reply',false)
     ON CONFLICT (dedupe_key) DO NOTHING
     RETURNING dedupe_key`,
    [key, event.fromId, event.fromUsername, triage.campaign.id, event.commentId, event.mediaId],
  )
  if (rows.length === 0) return { sent: false, reason: 'already messaged for this campaign (dedupe)' }

  try {
    await graphCall(cfg, {
      method: 'POST',
      path: `/${cfg.accountId}/messages`,
      params: {
        recipient: JSON.stringify({ comment_id: event.commentId }),
        message: JSON.stringify({ text }),
      },
    })
    await db.query(`UPDATE social_dm_log SET sent = true WHERE dedupe_key = $1`, [key])
    return { sent: true, commentId: event.commentId, campaignId: triage.campaign.id }
  } catch (e) {
    const msg = String((e as Error)?.message ?? e).slice(0, 300)
    await db.query(`UPDATE social_dm_log SET error = $2 WHERE dedupe_key = $1`, [key, msg])
    return { sent: false, reason: msg }
  }
}
