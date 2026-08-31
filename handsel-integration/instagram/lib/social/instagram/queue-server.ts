/**
 * social_publish_queue — durable, self-migrating Postgres queue.
 *
 * Copied structurally from lib/callback/settlement-queue.ts, including the
 * parts that look paranoid on purpose: CREATE TABLE IF NOT EXISTS on first
 * touch, a partial index on pending rows, tableReady memoization that
 * un-memoizes on failure, and claim-by-UPDATE...RETURNING so two drains on
 * two instances can never take the same row.
 *
 * Portability: every function takes a QueryPort instead of importing the
 * pool. In the Handsel repo this is `pool` from lib/db (PORTING.md); in the
 * standalone build it lets the module typecheck with zero dependencies. The
 * indirection costs one argument and buys a compile-anywhere queue.
 *
 * The business-key UNIQUE (platform:content_id) is the duplicate-publish
 * guard: application code cannot enqueue the same content twice no matter how
 * many times an approval handler retries.
 */

import type { SocialJob } from '../types'
import { hasGivenUp, nextRunAfter, rowStatusAfterAdvance } from './queue'
import { publishBusinessKey } from './core'

export interface QueryPort {
  query(sql: string, params?: unknown[]): Promise<{ rows: Array<Record<string, unknown>> }>
}

export interface QueueRow {
  id: string
  businessKey: string
  job: SocialJob
  status: 'pending' | 'done' | 'abandoned'
  attempts: number
  runAfter: Date
  lastError: string | null
}

const LOCK_TIMEOUT_MS = 6 * 60_000

let tableReadyPromise: Promise<void> | null = null

async function ensureTable(db: QueryPort): Promise<void> {
  if (!tableReadyPromise) {
    tableReadyPromise = (async () => {
      await db.query(`CREATE TABLE IF NOT EXISTS social_publish_queue (
        id text PRIMARY KEY,
        business_key text NOT NULL UNIQUE,
        job jsonb NOT NULL,
        status text NOT NULL DEFAULT 'pending',
        attempts integer NOT NULL DEFAULT 0,
        run_after timestamptz NOT NULL DEFAULT now(),
        locked_at timestamptz,
        last_error text,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now()
      )`)
      await db.query(
        `CREATE INDEX IF NOT EXISTS social_publish_queue_due_idx
         ON social_publish_queue (run_after) WHERE status = 'pending'`,
      )
    })()
  }
  try {
    await tableReadyPromise
  } catch (e) {
    tableReadyPromise = null // un-memoize: next caller retries the migration
    throw e
  }
}

function rowFromDb(r: Record<string, unknown>): QueueRow {
  return {
    id: String(r.id),
    businessKey: String(r.business_key),
    job: r.job as SocialJob,
    status: r.status as QueueRow['status'],
    attempts: Number(r.attempts),
    runAfter: new Date(String(r.run_after)),
    lastError: r.last_error === null ? null : String(r.last_error),
  }
}

/**
 * Idempotent enqueue: the UNIQUE business key turns a duplicate into a no-op
 * (ON CONFLICT DO NOTHING). Returns whether a new row was created.
 */
export async function enqueueSocialJob(db: QueryPort, job: SocialJob): Promise<boolean> {
  await ensureTable(db)
  const runAfter = job.scheduledAt ? new Date(job.scheduledAt) : new Date()
  const { rows } = await db.query(
    `INSERT INTO social_publish_queue (id, business_key, job, run_after)
     VALUES ($1, $2, $3, $4)
     ON CONFLICT (business_key) DO NOTHING
     RETURNING id`,
    [job.id, publishBusinessKey(job), JSON.stringify(job), runAfter],
  )
  return rows.length > 0
}

/** Claim up to n due rows; skips rows locked within LOCK_TIMEOUT_MS. */
export async function claimSocialJobs(db: QueryPort, n: number): Promise<QueueRow[]> {
  await ensureTable(db)
  const { rows } = await db.query(
    `UPDATE social_publish_queue SET locked_at = now(), updated_at = now()
     WHERE id IN (
       SELECT id FROM social_publish_queue
       WHERE status = 'pending'
         AND run_after <= now()
         AND (locked_at IS NULL OR locked_at < now() - ($2 || ' milliseconds')::interval)
       ORDER BY run_after ASC
       LIMIT $1
       FOR UPDATE SKIP LOCKED
     )
     RETURNING *`,
    [n, String(LOCK_TIMEOUT_MS)],
  )
  return rows.map(rowFromDb)
}

/** Persist the outcome of one advance() step and reschedule or settle the row. */
export async function recordAdvance(db: QueryPort, row: QueueRow, advanced: SocialJob): Promise<QueueRow> {
  await ensureTable(db)
  const attempts = row.attempts + 1
  const gaveUp = hasGivenUp(attempts) && advanced.status !== 'PUBLISHED'
  const status = rowStatusAfterAdvance(advanced, attempts, gaveUp)
  const finalJob: SocialJob = gaveUp && status === 'abandoned' && advanced.status !== 'FAILED' && advanced.status !== 'NEEDS_AUTH'
    ? { ...advanced, status: 'FAILED', error: advanced.error ?? `gave up after ${attempts} attempts`, retryCount: attempts }
    : { ...advanced, retryCount: attempts }
  const runAfter = status === 'pending' ? nextRunAfter(attempts) : row.runAfter
  const { rows } = await db.query(
    `UPDATE social_publish_queue
     SET job = $2, status = $3, attempts = $4, run_after = $5,
         locked_at = NULL, last_error = $6, updated_at = now()
     WHERE id = $1
     RETURNING *`,
    [row.id, JSON.stringify(finalJob), status, attempts, runAfter, finalJob.error ?? null],
  )
  return rowFromDb(rows[0])
}

export async function getQueueRow(db: QueryPort, businessKey: string): Promise<QueueRow | null> {
  await ensureTable(db)
  const { rows } = await db.query(
    `SELECT * FROM social_publish_queue WHERE business_key = $1`,
    [businessKey],
  )
  return rows.length ? rowFromDb(rows[0]) : null
}
