# Publishing packages — cycle 1

**Target: English-speaking internet.** Three videos, three platforms each.

**Status: NOT PUBLISHED. Awaiting explicit human approval.** Nothing below has
been posted, scheduled, or sent anywhere.

Copy is written **native per platform** — never one caption cross-posted. First
lines are written to survive each platform's truncation point.

---

## Publishing order and timing — this is load-bearing

1. **HS-001** first.
2. **HS-006** within 48 hours, at a comparable time of day. These two are the
   arms of EXP-001; publish them far apart or at different times of day and the
   experiment is confounded and both become anecdotes.
3. **HS-011** at least 48 hours after HS-006, so EXP-002 does not contaminate
   EXP-001's posting window.

Everything held constant between arms: same account, same caption style, same
length band, same hashtag strategy, same posting window.

---

## HS-001 — "I gave an AI $5 and told it to hire someone" · 0:30

### YouTube Shorts
**Title** (58 chars) — `I gave an AI $5 and told it to hire someone`
**Description**
```
It didn't do the work. It wrote a plan, priced every piece, and hired
a second agent for $1 to check the first one's work.

Nobody told it to do that.

This is a real planner output — nothing was escrowed, no money moved.
handsel-main.vercel.app

#shorts #ai #aiagents #softwareengineering
```

### TikTok
**Caption**
```
it hired a second AI to check the first AI's work. nobody asked it to.
real output, nothing escrowed 👀
```
`#ai #aiagents #tech #programming #startup`

### Instagram Reels
**Caption** — first line must survive the cutoff
```
It hired a checker for the checker.

I gave an AI a $5 budget and told it to hire someone. It didn't do the
work — it wrote a plan, put a price on every piece, and spent $1 of the
$5 on a second agent whose only job was to review the first one.

Nobody told it to do that.

Real planner output. Nothing escrowed, no money moved.
```
`#ai #aiagents #buildinpublic #softwareengineering #tech`

### Pinned comment
> The $1 reviewer is the part I didn't expect. I asked for one thing to get
> written — it decided on its own that somebody had to check it.

---

## HS-006 — "I paid four AIs the same question. One failed." · 0:35

### YouTube Shorts
**Title** (57 chars) — `I paid 4 AIs the same question. One of them failed.`
**Description**
```
Same brief. Same grader. None of them graded their own work.

Three passed. One failed. I never read any of it — the verdict came
from something that wasn't the worker and wasn't me.

Real graded verdicts, captured 2026-08-27.
handsel-main.vercel.app

#shorts #ai #aiagents #softwareengineering
```

### TikTok
**Caption**
```
every AI demo shows you the part that works.
this is the part that has to. 3 passed, 1 failed, I checked none of it
```
`#ai #aiagents #tech #programming #devtools`

### Instagram Reels
**Caption**
```
Three passed. One failed. I never read any of it.

Four AI agents, one brief, one grader — and none of them graded their
own work. The one that failed, failed for real. I didn't stage it and
I didn't catch it.

Every AI demo shows you the part that works. This is the part that
has to.

Real graded verdicts, captured 2026-08-27.
```
`#ai #aiagents #buildinpublic #softwareengineering #devtools`

### Pinned comment
> The tests failed. Nobody had to notice.
> *(Hook variant C from the batch — it was the better comment than opener.)*

---

## HS-011 — "An AI grading its own homework is not a reputation" · 0:35

### YouTube Shorts
**Title** (56 chars) — `An AI grading its own homework is not a reputation`
**Description**
```
An AI that is confidently wrong looks exactly like one that is right.
Which is why you still read every output yourself.

Unless the grading isn't done by the worker — and the answer is
generated with the problem, so the solver never sees it.

handsel-main.vercel.app

#shorts #ai #aiagents #machinelearning #softwareengineering
```

### TikTok
**Caption**
```
this AI says it did a great job. it's also the one that graded it.
that's not a score, that's a claim about a claim
```
`#ai #aiagents #tech #programming #ailiteracy`

### Instagram Reels
**Caption**
```
It graded its own homework and gave itself a 98.

An AI that is confidently wrong looks exactly like one that is right.
That's why you still read every output yourself — the score is a claim
about a claim.

Unless the grading isn't done by the worker. And the answer is generated
with the problem, so the solver never sees it.

Now the score is worth something. It was never yours to give.
```
`#ai #aiagents #ailiteracy #buildinpublic #softwareengineering`

### Pinned comment
> The line I couldn't fit: an agent that's confidently wrong and one that's
> right produce the same confident output. Nothing about the output tells
> you which one you got.

---

## Standing rules applied to all of the above

- **No engagement bait.** No "comment X", no "follow for part 2", no fake
  urgency. The CTA is a URL on the end card and nothing more.
- **No virality promise, no traction claim.** Handsel is at a cold start and
  none of this copy says otherwise.
- **AI disclosure.** All three use synthetic narration (Piper/eSpeak, offline).
  Where a platform's AI-disclosure toggle applies to synthetic voice, set it.
  TikTok's regime is the strictest — see `viral-tiktok-content`.
- Hashtags are small, specific, and audience-shaped. Broad tags
  (#viral #fyp #foryou) are omitted on purpose: they buy impressions from an
  audience that will never install a developer tool, which suppresses the
  follow-through signals that actually matter here.

## What to record after posting

Per `../sop/analytics-loop.md`, into `../memory/published.md`. Public metrics
carry `[api]`; watch time, completion rate, retention @3s and CTR are
`native-insights` if a human reads them off the dashboard and **`unmeasured`
otherwise — never estimated.**
