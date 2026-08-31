/**
 * PATCH → lib/ops-cycle.ts
 * Append to OPS_STEPS (order: after 'settlementQueue' is fine; anywhere works
 * — steps are independent). Deliberately NOT fast:true — ops-cycle defines
 * fast as visitor-safe money movement; a social publish must never ride
 * visitor traffic, and a 5-minute cadence is tighter than any scheduled post
 * needs. vercel.json's existing cron picks this up with zero config.
 */
export const socialDrainStep = {
  name: 'socialDrain',
  run: async () => {
    const { drainSocialQueue } = await import('@/lib/social/instagram/drain-server')
    const { pool } = await import('@/lib/db')
    return drainSocialQueue(pool)
  },
}
