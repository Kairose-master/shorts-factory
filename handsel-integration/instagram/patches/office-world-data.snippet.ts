/**
 * PATCH → lib/office-world-data.ts, growth-studio template (~line 1336).
 *
 * The audit's finding: growth-studio's `distributor` role already "packages
 * the approved copy per channel" but stops short of publishing. Instagram
 * publishing extends that seam instead of inventing a parallel social office.
 * Department: market (market.gate 🌐 — the boundary with the outside
 * economy); glyph exists at /public/dept/market.png; avatar accessory
 * headset/accent per lib/office-avatar-kit.ts.
 *
 * 1) Add ONE role after `distributor` in growth-studio's roles[]:
 */
export const publisherRole = {
  id: 'publisher',
  name: 'Publisher',
  blurb:
    'Takes the approved, packaged asset from the Distribution Planner and files the Instagram publish job — container, poll, publish — through the social queue. Never publishes anything the approval gate has not stamped READY.',
  colorIndex: 4,
  customInstructions:
    'You may only enqueue content whose queue row is READY. Refuse DRAFT and APPROVAL_REQUIRED rows and say why. Always dry-run (preview) first and attach the call plan to the job record. Check publishing quota before enqueueing more than one item.',
  mcpHint: 'instagram-publisher skill / lib/social/instagram',
}

/**
 * 2) Add ONE pipeline step after the distributor step:
 *    (bountyWeight small — publishing is mechanical; the thinking was paid
 *    upstream. reviewOfRoleId stays unset: the human approval gate, not a
 *    paid reviewer, is the control for public content.)
 */
export const publishStep = {
  roleId: 'publisher',
  title: 'Publish the approved Instagram asset',
  brief:
    'Take the Distribution Planner\'s Instagram-packaged asset (media URL, caption, alt text, campaign). Verify the content-queue row is READY. Dry-run the publish, attach the preview, then enqueue the social job and report the queue business key and, once drained, the media id and permalink.',
  acceptanceCriteria:
    'Queue row exists with status done; Instagram media id and permalink recorded; preview attached; no publish attempted for any row not READY.',
  dependsOnRoleIds: ['distributor'],
  bountyWeight: 1,
}

/**
 * Existing role ids in growth-studio map onto the requested crew:
 *   Social Scout   → positioning (Exa-connected scout; finds the opportunity)
 *   Content Agent  → copywriter (+ shorts-factory Office for video assets)
 *   [approval]     → claim-check + the human READY gate
 *   Publisher      → publisher (this patch)
 *   Analyst        → add later re-using getMediaInsights; do NOT add a role
 *                    until there is real published media to analyze — the
 *                    office file's invariant is that nothing invents activity.
 */
