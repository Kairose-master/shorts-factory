/**
 * Queue drain — the OpsStep body.
 *
 * Mirrors lib/callback/settlement-drain.ts: a SMALL batch, strictly
 * sequential (never Promise.all — the settlement drain learned that under
 * nonce contention; here the concern is Meta's per-account rate ceiling),
 * and a one-line report per row. Wired into lib/ops-cycle.ts as a normal
 * step, NOT fast:true — ops-cycle defines fast as "money that should have
 * moved", and a social post must never ride visitor traffic.
 *
 * Scheduled content: isDue() re-checks scheduled_at at claim time, so a
 * post scheduled for tomorrow sits in the queue untouched even though its
 * row is pending.
 */

import { claimSocialJobs, recordAdvance, type QueryPort } from './queue-server'
import { describeSocialJob, isDue } from './queue'
import { instagramPublisher } from './publish-server'

const DRAIN_BATCH = 3

export interface SocialDrainReport {
  claimed: number
  published: number
  advanced: number
  abandoned: number
  lines: string[]
}

export async function drainSocialQueue(db: QueryPort): Promise<SocialDrainReport | string> {
  let rows
  try {
    rows = await claimSocialJobs(db, DRAIN_BATCH)
  } catch (e) {
    return `social queue unreadable: ${String((e as Error)?.message ?? e).slice(0, 200)}`
  }

  const report: SocialDrainReport = { claimed: rows.length, published: 0, advanced: 0, abandoned: 0, lines: [] }

  for (const row of rows) {
    if (!isDue(row.job, row.runAfter)) {
      // claimed but not due (scheduled_at in the future): release untouched
      await recordAdvance(db, { ...row, attempts: row.attempts - 1 }, row.job)
      continue
    }
    const advanced = await instagramPublisher.advance(row.job)
    const updated = await recordAdvance(db, row, advanced)
    if (updated.status === 'done') report.published++
    else if (updated.status === 'abandoned') report.abandoned++
    else report.advanced++
    report.lines.push(describeSocialJob(updated.job, updated.attempts))
  }
  return report
}
