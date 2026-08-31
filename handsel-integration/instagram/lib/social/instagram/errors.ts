/**
 * Instagram Graph API error classification.
 *
 * The one decision this file exists to make: is a failed call worth retrying?
 * Getting it wrong in either direction costs real things — retrying a
 * permission error burns publishing quota (25 posts/24h) and can trip Meta's
 * abuse heuristics; NOT retrying a transient 5xx abandons a post that would
 * have gone out on the next tick. So classification is explicit, by Meta's
 * documented codes, and everything unknown defaults to permanent: the failure
 * mode of a wrong "permanent" is a human glancing at the queue, while the
 * failure mode of a wrong "transient" is an 8-attempt hammer on a call that
 * can never succeed. lib/retry.ts's isTransientLlmError is deliberately NOT
 * reused here — Graph error semantics live in codes, not messages.
 */

import type { IgErrorBody } from './types'

export type IgErrorClass = 'transient' | 'permanent' | 'auth'

export class InstagramApiError extends Error {
  readonly status: number
  readonly code?: number
  readonly subcode?: number
  readonly fbtraceId?: string
  readonly classification: IgErrorClass

  constructor(message: string, opts: {
    status: number
    code?: number
    subcode?: number
    fbtraceId?: string
  }) {
    super(message)
    this.name = 'InstagramApiError'
    this.status = opts.status
    this.code = opts.code
    this.subcode = opts.subcode
    this.fbtraceId = opts.fbtraceId
    this.classification = classifyIgError(opts.status, opts.code, opts.subcode)
  }
}

/** Graph codes that mean "the token is the problem" — never retried. */
const AUTH_CODES = new Set([102, 190])

/**
 * Graph codes documented as retryable: 1/2 (unknown/service), 4/17/32/613
 * (throttling tiers), 341 (temporary application block).
 */
const TRANSIENT_CODES = new Set([1, 2, 4, 17, 32, 341, 613])

/** error_subcode 2207003: media still processing — transient by definition. */
const TRANSIENT_SUBCODES = new Set([2207003, 2207027])

export function classifyIgError(
  status: number,
  code?: number,
  subcode?: number,
): IgErrorClass {
  if (code !== undefined && AUTH_CODES.has(code)) return 'auth'
  if (subcode !== undefined && TRANSIENT_SUBCODES.has(subcode)) return 'transient'
  if (code !== undefined && TRANSIENT_CODES.has(code)) return 'transient'
  if (status === 429 || status >= 500) return 'transient'
  return 'permanent'
}

/** Parse a Graph error response body into a typed error. Never throws. */
export function igErrorFromBody(status: number, body: unknown): InstagramApiError {
  const e = (body as IgErrorBody | null)?.error
  const message = e?.message
    ? `graph ${status}: ${String(e.message).slice(0, 300)}`
    : `graph ${status}: unrecognized error body`
  return new InstagramApiError(message, {
    status,
    code: typeof e?.code === 'number' ? e.code : undefined,
    subcode: typeof e?.error_subcode === 'number' ? e.error_subcode : undefined,
    fbtraceId: typeof e?.fbtrace_id === 'string' ? e.fbtrace_id : undefined,
  })
}

/**
 * "Already published" shows up when a publish retry races a success that we
 * failed to record (crash between media_publish and the DB write). It must be
 * treated as success-shaped, not failure-shaped, or the retry loop publishes
 * a duplicate through a fresh container. Meta signals it inconsistently, so
 * both the documented subcode and the message text are checked.
 */
export function looksAlreadyPublished(err: InstagramApiError): boolean {
  if (err.subcode === 2207032) return true
  return /already.{0,20}publish/i.test(err.message)
}
