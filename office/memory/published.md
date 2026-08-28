# Published Content

Nothing published. **The Office has never published and will not publish without
explicit human approval** — see the autonomy boundary in `../CHARTER.md`.

## Row format

Every metric carries a measurement label. **`unmeasured` is a valid, required
value. A blank is not, and an estimate is never.**

```
ID              HS-000-yt-01
Backlog ID      HS-000
Platform        youtube-shorts | tiktok | instagram-reels
URL             
Published at    
Hook used       verbatim, the line as it aired
Length          seconds
Experiment      link to memory/experiments.md, if this is an arm

views              n     [api]
watch time         —     [unmeasured]
completion rate    —     [unmeasured]
retention @3s      —     [unmeasured]
likes              n     [api]
comments           n     [api]
shares             n     [api]
saves              —     [unmeasured]
CTR                —     [unmeasured]
followers gained   —     [unmeasured]
```

Labels: `api` (public/ScrapeCreators) · `native-insights` (a human read it off the
platform's own dashboard) · `unmeasured`.

Without a platform analytics connector, watch time, completion rate, retention
and CTR are **only** available as `native-insights`. Design experiments to be
readable from `api` metrics where possible — see `../sop/analytics-loop.md`.
