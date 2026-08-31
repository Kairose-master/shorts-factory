/**
 * Instagram Graph API domain types.
 *
 * Everything here mirrors what graph.facebook.com actually returns for the
 * Content Publishing API, narrowed to the fields this integration reads.
 * Kept separate from ../types.ts on purpose: SocialJob must never grow an
 * Instagram-shaped field, and these types must never leak past the provider.
 */

export const IG_CONTAINER_STATUSES = [
  'IN_PROGRESS',
  'FINISHED',
  'ERROR',
  'EXPIRED',
  'PUBLISHED',
] as const
export type IgContainerStatus = (typeof IG_CONTAINER_STATUSES)[number]

/** POST /{ig-user-id}/media media_type values this integration uses. */
export type IgMediaType = 'IMAGE' | 'REELS' | 'STORIES' | 'CAROUSEL'

export interface IgContainerResponse {
  id: string
}

export interface IgStatusResponse {
  id?: string
  status_code?: string
  status?: string
}

export interface IgPublishResponse {
  id: string
}

export interface IgQuota {
  quotaTotal: number
  quotaUsage: number
  remaining: number
}

export interface IgErrorBody {
  error?: {
    message?: string
    type?: string
    code?: number
    error_subcode?: number
    fbtrace_id?: string
  }
}

export interface IgInsightValue {
  name: string
  values: Array<{ value: number }>
}

export interface IgMediaInsights {
  mediaId: string
  metrics: Record<string, number>
}
