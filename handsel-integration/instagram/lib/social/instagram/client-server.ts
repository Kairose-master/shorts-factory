/**
 * The one fetch wrapper for the Instagram Graph API.
 *
 * Every outbound call in this integration goes through graphCall so that
 * retry policy, timeouts, error typing and token handling exist in exactly
 * one place. Retries follow lib/retry.ts's shape (bounded attempts,
 * exponential backoff) but with Graph-native classification from errors.ts —
 * a permanent Graph error (validation, permission) is NEVER retried, because
 * hammering those burns the 25-posts/24h publishing quota and cannot succeed.
 *
 * The access token travels as a query param per Meta's samples; it is
 * appended after preview/log serialization so no log line ever carries it.
 */

import { igErrorFromBody, InstagramApiError } from './errors'
import type { InstagramConfig } from './auth-server'

const CALL_TIMEOUT_MS = 30_000
const RETRIES = 3
const RETRY_BASE_MS = 2_000

export interface GraphCallInput {
  method: 'GET' | 'POST'
  /** Path without version prefix, e.g. `/12345/media`. */
  path: string
  params?: Record<string, string>
}

function buildUrl(cfg: InstagramConfig, input: GraphCallInput, withToken: boolean): string {
  const version = cfg.apiVersion ? `/${cfg.apiVersion}` : ''
  const url = new URL(`${cfg.graphOrigin}${version}${input.path}`)
  for (const [k, v] of Object.entries(input.params ?? {})) url.searchParams.set(k, v)
  if (withToken) url.searchParams.set('access_token', cfg.accessToken)
  return url.toString()
}

const sleep = (ms: number) => new Promise<void>(r => setTimeout(r, ms))

/**
 * Executes one Graph call with bounded retries on transient failures only.
 * Throws InstagramApiError (typed, classified) on a final failure; network
 * failures (fetch throw / abort) are wrapped as transient status-0 errors.
 */
export async function graphCall<T>(cfg: InstagramConfig, input: GraphCallInput): Promise<T> {
  let lastError: InstagramApiError | null = null

  for (let attempt = 0; attempt <= RETRIES; attempt++) {
    if (attempt > 0) await sleep(RETRY_BASE_MS * 2 ** (attempt - 1))
    let res: Response
    try {
      res = await fetch(buildUrl(cfg, input, true), {
        method: input.method,
        signal: AbortSignal.timeout(CALL_TIMEOUT_MS),
      })
    } catch (e) {
      lastError = new InstagramApiError(
        `graph network failure: ${String((e as Error)?.message ?? e).slice(0, 200)}`,
        { status: 0, code: 1 }, // code 1 => transient per errors.ts
      )
      continue
    }

    let body: unknown = null
    try { body = await res.json() } catch { body = null }

    if (res.ok) return body as T

    const err = igErrorFromBody(res.status, body)
    if (err.classification !== 'transient') throw err
    lastError = err
  }

  throw lastError ?? new InstagramApiError('graph call failed with no response', { status: 0 })
}

/** Preview-safe URL (no token) for logs and dry-run output. */
export function describeCall(cfg: InstagramConfig, input: GraphCallInput): string {
  return `${input.method} ${buildUrl(cfg, input, false)}`
}
