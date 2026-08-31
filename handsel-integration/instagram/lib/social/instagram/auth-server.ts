/**
 * Instagram credential resolution. The only file allowed to touch the token.
 *
 * Conventions inherited from lib/email.ts / lib/hf-image.ts:
 *  - optional-env: unconfigured is a structured no-op, never a throw;
 *  - two-tier secret read: the shared platform secret store first, env second
 *    (PORTING.md swaps the marked line for getPlatformSecret when this file
 *    lands in the Handsel repo — the standalone build has no DB);
 *  - the token never appears whole in logs or results: maskToken keeps last 4.
 *
 * Env vars (documented in .env.example, never committed with values):
 *   INSTAGRAM_ACCESS_TOKEN   long-lived Page/system-user token with
 *                            instagram_basic + instagram_content_publish
 *   INSTAGRAM_ACCOUNT_ID     the IG professional account's ig-user-id
 *   INSTAGRAM_API_VERSION    optional, e.g. v21.0; unset = unversioned path
 *   INSTAGRAM_GRAPH_ORIGIN   optional override (tests point it at localhost)
 */

export interface InstagramConfig {
  accessToken: string
  accountId: string
  apiVersion: string | null
  graphOrigin: string
}

export async function resolveInstagramConfig(): Promise<InstagramConfig | null> {
  // PORTING: prefix with `(await getPlatformSecret('instagram_token')) ||`
  const accessToken = process.env.INSTAGRAM_ACCESS_TOKEN || null
  const accountId = process.env.INSTAGRAM_ACCOUNT_ID || null
  if (!accessToken || !accountId) return null
  return {
    accessToken,
    accountId,
    apiVersion: process.env.INSTAGRAM_API_VERSION || null,
    graphOrigin: process.env.INSTAGRAM_GRAPH_ORIGIN || 'https://graph.facebook.com',
  }
}

export async function isInstagramConfigured(): Promise<boolean> {
  return (await resolveInstagramConfig()) !== null
}

export const NOT_CONFIGURED_REASON =
  'instagram not configured (INSTAGRAM_ACCESS_TOKEN / INSTAGRAM_ACCOUNT_ID)'

/** Last-4 display form; safe for logs, UI and error strings. */
export function maskToken(token: string): string {
  if (token.length <= 4) return '****'
  return `…${token.slice(-4)}`
}
