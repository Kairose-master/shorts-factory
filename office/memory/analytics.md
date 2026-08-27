# Analytics

No published content, so no analytics.

## What this Office can and cannot measure today

Zapier MCP is not connected and no platform-analytics connector is wired.

| Metric | Available? | How |
|---|---|---|
| views, likes, comments, shares | yes | public / ScrapeCreators — `api` |
| saves | rarely | usually `unmeasured` |
| watch time, completion rate, retention @3s, skip rate | **no** | native insights only — a human types them in |
| CTR, followers gained | **no** | as above |

**This is the Office's single biggest capability gap.** The learning loop runs on
`api` metrics and human-entered `native-insights`; every hook experiment is
therefore judged on views-per-follower against the account's own baseline rather
than on 3-second retention, which is the metric that would actually answer the
question.

Closing it needs one of: Zapier MCP with the platform analytics actions, a direct
platform API connector, or a standing human routine that reads native insights at
a fixed interval after each post.

**Until then: `unmeasured` is written, never estimated.** A guessed retention
number poisons every lesson derived from it, and lessons are the only thing this
Office accumulates.
