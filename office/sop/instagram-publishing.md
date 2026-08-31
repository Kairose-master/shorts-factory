# SOP — Publishing to Instagram (the handsel Social Desk)

Where a render goes AFTER step 13 of `production-pipeline.md` approves it.
This Office produces content; it does not hold Instagram credentials and it
does not publish. Publishing belongs to the handsel repo's Social Desk,
which owns the official-API integration, the approval gate, scheduling,
retries and duplicate-publish prevention.

## The route

1. **Step 13 approval happens here** as always: render + QC verdict +
   caption + target account + publish time, then stop and wait.
2. Host the approved asset on a **public https URL** (the handsel
   deployment uses Vercel Blob). Reels: MP4 9:16 1080×1920. Posts: JPEG,
   4:5. Stories: 9:16, plain media only — the API cannot attach polls,
   stickers or music, so no story concept may depend on them.
3. Create the job in the handsel Social Desk (`/social` on the deployment,
   or `createSocialJob()` / the `instagram-publisher` skill in that repo).
   The job enters as `APPROVAL_REQUIRED` — the handsel-side approve click
   is the second, mechanical half of the approval this Office already gave;
   it fingerprints the exact media + caption, so a silent swap after
   approval is refused at publish time.
4. The queue publishes on schedule and records the media id + permalink on
   the job card.
5. **Log the publish in `memory/published.md`** with the permalink, and
   read performance back per `analytics-loop.md` (the Social Desk exposes
   `get_media_insights`; reach/likes/comments/saves/shares per media id).

## Rules that carry over

- Nothing publishes without explicit human approval — now enforced twice
  (this Office's step 13 AND the Social Desk's approval gate).
- Every factual Handsel claim in a caption traces to
  `research/handsel-model.md` or it is cut — same ledger, same rule.
- Editorial spec for the account (bio, palettes, highlight system, content
  types): `docs/social/instagram-brand.md` in the handsel repo.
