#!/usr/bin/env node
/**
 * Offline dry-run for a SocialJob JSON: prints the exact Graph call sequence
 * and validation findings. Zero network, zero token — safe to run anywhere.
 *
 *   node scripts/preview.mjs path/to/job.json
 *
 * Standalone by design (plain fetch-free mirror of core.ts's buildPreview):
 * the skill must be able to preview on a machine with no toolchain. Keep in
 * sync with lib/social/instagram/core.ts — tests/instagram.test.ts pins the
 * canonical sequence.
 */
import { readFileSync } from 'node:fs'

const path = process.argv[2]
if (!path) {
  console.error('usage: preview.mjs <job.json>')
  process.exit(1)
}
const job = JSON.parse(readFileSync(path, 'utf8'))
const igUserId = process.env.INSTAGRAM_ACCOUNT_ID || '<ig-account-id>'

const warnings = []
if ((job.caption ?? '').length > 2200) warnings.push('caption over 2200 chars')
const tags = ((job.caption ?? '').match(/#[\p{L}\p{N}_]+/gu) ?? []).length
if (tags > 30) warnings.push(`${tags} hashtags (max 30)`)
for (const [i, a] of (job.assets ?? []).entries()) {
  if (!/^https:\/\//.test(a.url ?? '')) warnings.push(`asset ${i}: URL must be https`)
}
if (job.contentType === 'reel' && !(job.campaign ?? '').length) {
  warnings.push('reel without campaign metadata — reference-format citation required by policy')
}

const calls = []
const containerParams = (asset, extra = {}) => ({
  ...(asset.kind === 'video' ? { video_url: asset.url } : { image_url: asset.url }),
  ...(job.caption && !extra.is_carousel_item && job.contentType !== 'story' ? { caption: job.caption } : {}),
  ...extra,
})

if (job.contentType === 'carousel') {
  for (const asset of job.assets) {
    calls.push({ method: 'POST', path: `/${igUserId}/media`, params: containerParams(asset, { is_carousel_item: 'true' }) })
  }
  calls.push({ method: 'POST', path: `/${igUserId}/media`, params: { media_type: 'CAROUSEL', children: '<child-ids>', caption: job.caption } })
} else {
  const extra = job.contentType === 'reel' ? { media_type: 'REELS', ...(job.shareToFeed !== undefined ? { share_to_feed: String(job.shareToFeed) } : {}) }
    : job.contentType === 'story' ? { media_type: 'STORIES' } : {}
  calls.push({ method: 'POST', path: `/${igUserId}/media`, params: containerParams(job.assets[0], extra) })
}
calls.push({ method: 'GET', path: '/<container-id>', params: { fields: 'status_code' } })
calls.push({ method: 'POST', path: `/${igUserId}/media_publish`, params: { creation_id: '<container-id>' } })

console.log(JSON.stringify({ dryRun: true, platform: 'instagram', contentType: job.contentType, warnings, calls }, null, 2))
console.log('\nNo network calls were made. access_token never appears in previews.')
