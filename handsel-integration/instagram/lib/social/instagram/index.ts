/**
 * Public surface of the Instagram provider. Callers outside lib/social/
 * import from here; the module files behind it are implementation detail.
 */
export { instagramPublisher, getPublishQuota, getMediaInsights } from './publish-server'
export { isInstagramConfigured, NOT_CONFIGURED_REASON, maskToken } from './auth-server'
export {
  validateCaption,
  validateAssets,
  buildPreview,
  publishBusinessKey,
  MAX_CAPTION_CHARS,
  MAX_HASHTAGS,
} from './core'
export { InstagramApiError, classifyIgError } from './errors'
export { enqueueSocialJob, claimSocialJobs, recordAdvance, getQueueRow } from './queue-server'
export type { QueryPort, QueueRow } from './queue-server'
export { drainSocialQueue } from './drain-server'
export { describeSocialJob, isDue, rowStatusAfterAdvance } from './queue'
export {
  parseCommentWebhook,
  verifyWebhookSignature,
  triageComment,
  renderDmTemplate,
  dmDedupeKey,
  isCommentFresh,
} from './dm-core'
export type { CommentEvent, DmCampaign } from './dm-core'
export { handleCommentEvent, isDmAutomationEnabled } from './dm-server'
