# SOP — The analytics loop

Every published video is an experiment. The loop closes only if the numbers come
back honestly labelled.

## What is measurable here, and what is not

Zapier MCP is not connected and no platform-analytics connector is wired, so:

| Metric | Source | Label |
|---|---|---|
| views, likes, comments, shares | public / ScrapeCreators | `api` |
| saves | mostly private | usually `unmeasured` |
| watch time, completion rate, retention @3s, skip rate | **native insights only** | `native-insights` if a human typed it in, else `unmeasured` |
| CTR, followers gained | native insights only | as above |

**Rule: an unmeasured metric is written `unmeasured`. Never estimated, never left
blank to be read as zero.** A guessed retention number poisons every lesson
derived from it, and lessons are the only thing this Office accumulates.

Design experiments to be readable from public metrics where possible. A hook test
can be judged on views-per-follower against the account's own baseline; it does
not strictly need retention data.

## The question, asked in order

For each published video, ask **why did this work** or **why did this fail** — and
force the answer into exactly one bucket first:

| Bucket | Signature | Fix lives in |
|---|---|---|
| **Hook failure** | impressions fine, 3s retention collapses | `viral-hooks`, `hook-anatomy` |
| **Content failure** | good 3s hold, drops through the middle | script / structure |
| **Visual failure** | audio-off viewers drop; comments about legibility | `penpot`, caption style |
| **Audience mismatch** | decent retention, wrong-audience comments, no follows | pillar/platform choice |
| **Distribution failure** | low impressions regardless of quality | posting time, caption, hashtags, account state |
| **Product-message failure** | held attention, comments show they misunderstood Handsel | `research/handsel-model.md` framing |

Naming the bucket before proposing a fix stops the standing failure mode: a
distribution problem "fixed" by rewriting a hook that was never seen.

## Read the comments, not just the counters

Run `comment-mining` for what people said and `read-the-room` for what they meant.
A video with mediocre numbers and comments saying *"wait, so the AI pays the other
AI?"* is a **success** — that is comprehension, which is the actual mission.
Record it as such in `memory/lessons.md` even when the metrics are flat.

## Before a lesson is written

A lesson requires:

1. a linked experiment,
2. **at least two independent observations** pointing the same way,
3. a stated confidence,
4. a link to any lesson it supersedes.

One observation is a note, not a lesson. Write it in `memory/experiments.md` with
`Observations: 1` and wait for the second.
