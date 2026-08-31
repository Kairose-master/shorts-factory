/**
 * Pure scheduling and row logic for the social publish queue.
 *
 * Modeled 1:1 on lib/callback/settlement-queue.ts: the pure functions
 * (backoff schedule, give-up policy, describe) live here where a unit test
 * can pin them; the SQL lives in queue-server.ts. Queue rows track a
 * SocialJob attempt-chain; the UNIQUE business key (platform:content_id)
 * on the table — not application code — is what makes enqueue idempotent
 * and duplicate publishes structurally impossible.
 */

import type { SocialJob, SocialJobStatus } from '../types'
export { backoffMs, nextRunAfter, hasGivenUp, MAX_PUBLISH_ATTEMPTS } from './core'

export const QUEUE_ROW_STATUSES = ['pending', 'done', 'abandoned'] as const
export type QueueRowStatus = (typeof QUEUE_ROW_STATUSES)[number]

/** Terminal job statuses: the queue row leaves 'pending' on these. */
const TERMINAL: ReadonlySet<SocialJobStatus> = new Set(['PUBLISHED', 'FAILED', 'NEEDS_AUTH'])

/**
 * After an advance() step, what happens to the queue row?
 *  - PUBLISHED           -> done
 *  - FAILED / NEEDS_AUTH -> abandoned (a human looks; retrying cannot help)
 *  - anything else       -> pending, rescheduled by backoff
 * EXPIRED is deliberately non-terminal: advance() clears the container id and
 * the next tick recreates it, so an expired container costs one extra cycle,
 * not the post.
 */
export function rowStatusAfterAdvance(job: SocialJob, attempts: number, gaveUp: boolean): QueueRowStatus {
  if (job.status === 'PUBLISHED') return 'done'
  if (job.status === 'FAILED' || job.status === 'NEEDS_AUTH') return 'abandoned'
  if (gaveUp) return 'abandoned'
  return 'pending'
}

export function isTerminal(status: SocialJobStatus): boolean {
  return TERMINAL.has(status)
}

/** One human-readable line for the Local Jobs UI / ops report. */
export function describeSocialJob(job: SocialJob, attempts: number): string {
  const base = `${job.platform} ${job.contentType} ${job.contentId}`
  switch (job.status) {
    case 'PUBLISHED':
      return `${base}: published as ${job.remoteMediaId ?? '(id unrecorded)'}`
    case 'NEEDS_AUTH':
      return `${base}: needs re-authentication — ${job.error ?? 'token rejected'}`
    case 'FAILED':
      return `${base}: failed after ${attempts} attempt(s) — ${job.error ?? 'unknown error'}`
    case 'PROCESSING':
      return `${base}: container ${job.containerId ?? '?'} processing (attempt ${attempts})`
    case 'EXPIRED':
      return `${base}: container expired; recreating`
    default:
      return `${base}: ${job.status.toLowerCase()} (attempt ${attempts})`
  }
}

/**
 * Scheduled content: a job whose scheduled_at is in the future is not due,
 * regardless of run_after. Pure so the "is it time yet" decision is testable
 * against fixed clocks instead of the DB's now().
 */
export function isDue(job: Pick<SocialJob, 'scheduledAt'>, runAfter: Date, now: Date = new Date()): boolean {
  if (runAfter.getTime() > now.getTime()) return false
  if (job.scheduledAt && new Date(job.scheduledAt).getTime() > now.getTime()) return false
  return true
}
