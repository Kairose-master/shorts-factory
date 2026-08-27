# AI Tools & Automation — short-form research run (API mode)

Companion to `research/ai-tools-automation-2026-08-27/report.md` (open mode).
Where the two disagree, §6 names the disagreement explicitly.

## Method

| | |
|---|---|
| **Run mode** | **API** — all four keys live and validated |
| **Date** | 2026-08-27 |
| **Stages run** | 1–5 measured · 6–9 analytic |
| **YouTube source** | TubeLab `/v1/search/outliers` (`type=short`) + `/v1/video/transcript` |
| **TikTok source** | ScrapeCreators `/v1/tiktok/search/keyword`, `/video/transcript`, `/video/comments` |
| **Comments** | ScrapeCreators `/v1/youtube/video/comments` |
| **Visual** | Gemini `gemini-flash-latest`, native YouTube URL input |
| **Spend** | 21 ScrapeCreators credits (2100 → 2079), ~30 TubeLab calls, 6 Gemini calls. Cap was 400 credits |

**Sample.**

| Layer | n |
|---|---|
| YouTube Shorts outliers returned | 33 unique (25 direct + 25 adjacent, deduped) |
| …of which on-niche (AI tooling/automation, not AI-as-entertainment) | **15** |
| YouTube transcripts fetched | **14 of 15** |
| YouTube comment sets | 8 videos / **103 comments** |
| TikTok videos returned | 86 unique across 3 queries |
| TikTok transcripts + comment sets | 5 videos / **75 comments** |

**What was NOT run, and why it matters.**

- **Gemini visual analysis: 1 of 5 succeeded.** The other four returned `503
  UNAVAILABLE` (model overload) across two retry passes with backoff. This is a
  transient capacity failure, not a data or key problem. Every visual claim below
  rests on the single successful analysis and is labelled as such.
- **Apify was not used.** `APIFY_TOKEN` is valid but on the **FREE** plan, and
  `.claude/context/tiktok-accounts.md` still contains the placeholder `@example`
  row — `tiktok-research` fans out over *tracked accounts*, so it had nothing
  real to fan out over. TikTok was collected through ScrapeCreators keyword
  search instead, which is cheaper and needs no account list. Consequence: the
  TikTok leg has **no per-creator baseline** (see the caveat in §2).
- **Instagram and X were not collected.** Out of the scope you set.
- **The `youtube-research` skill could not produce this data as shipped.** Two
  defects, both worked around without touching the skills tree:
  1. `find_outliers.py` hardcodes `type=video`. Its first run returned **zero
     Shorts** — 9 long-form videos from 763s to 17,562s.
  2. Its transcript parser reads `data["segments"]`; the API now returns
     `items[].events`. It reported "Fetched 0 transcripts" while the endpoint was
     returning HTTP 200 the whole time.
  Both are logged in §7 as follow-up work.

---

## 1. Stage 3 — outliers, measured against each creator's own baseline

TubeLab returns `averageViewsRatio` (this video ÷ that channel's average) and a
`zScore`. Both are **channel-relative**, which is the measure that matters. Raw
view counts are shown only so you can see how badly they mislead.

**On-niche Shorts, ranked by baseline multiple:**

| × baseline | z | Views | Subs | Len | Channel | Title |
|---|---|---|---|---|---|---|
| **20.59×** | 5.19 | 127,836 | 20.4K | 63s | Sanji Nai-Chien | Don't sleep on this AI motion tool |
| **13.05×** | 8.49 | 136,240 | 411K | 61s | David Ondrej | AI Coding Agents tier list |
| **12.14×** | 3.60 | 1,158,789 | 70.8K | 63s | Eric Tech | The AI CRM That Actually Does the Work for You |
| **9.78×** | 7.58 | **6,251** | 18.9K | 52s | Quinn Nolan | Sell THIS Simple Automation To Local Businesses |
| 4.42× | 1.82 | 139,764 | 12.1K | 37s | AnimAItion Studio | AI today really only needs one prompt… |
| 3.84× | 2.00 | 40,804 | 411K | 34s | David Ondrej | Bad Claude Code Habits |
| 3.63× | 2.92 | 164,876 | 361K | 75s | Matt Pocock | AI Coding is exhausting |
| 3.48× | 2.95 | 44,176 | 263K | 41s | Jack Roberts | The FREE GitHub skill that deletes every AI tell. |
| 2.99× | 2.20 | 135,715 | 361K | 98s | Matt Pocock | Claude Code's system tools are SO BLOATED |
| 2.98× | 2.92 | 31,393 | 368K | 31s | Sabrina Ramonov | The Blotato DM Automation Behind My $120K ARR Reel |
| 2.69× | 2.01 | 34,295 | 263K | 39s | Jack Roberts | 89,000 AI skills for you to steal |
| 2.58× | 2.02 | 27,971 | 317K | 32s | Nate B Jones | Why does everything look the same now? |
| 2.50× | 2.21 | 26,634 | 368K | 26s | Sabrina Ramonov | Which AI Tool Should You Use for Each Task? |

**Read the 4th row before anything else.** Quinn Nolan's Short has **6,251
views** — the lowest number in the table — and is the **4th strongest performer
in the set** at 9.78× his own baseline with a z of 7.58. Ranked by raw views it
would sit dead last of thirteen. This is the entire argument for baseline-relative
scoring in one row, and it is exactly the row the open-mode run could not see.

**The inverse case.** Eric Tech's 1.16M views is the biggest number in the
table and only 12.14× — while Sabrina Ramonov's 26,634-view Short is 2.50× on a
368K-subscriber channel. Large channels post large numbers on ordinary videos.

### The discovery-surface finding

Only **15 of 33** returned Shorts were about AI tooling at all. The other 18 —
including the two highest ratios in the whole pull, `#animation` at **43.65×**
and `LAMBORGHINI HURACÁN KEY TRANSFORMATION` at **23.96×** — are AI-*generated
entertainment*: animation, acting skits, car edits, storytelling.

On the Shorts surface, "AI agent" and "AI automation" as queries return
**entertainment made with AI**, not education about AI. The tooling niche is a
minority tenant of its own keywords. Open mode could not detect this, because it
never saw the ranked field.

---

## 2. TikTok — reach relative to follower count

**Caveat, and it is a real one.** ScrapeCreators keyword search returns no
per-creator average, so the ratio below is **plays ÷ followers**, not
plays ÷ that creator's median. It is a reach proxy, **not** the same measurement
as §1 and not comparable to it. Treated as directional only.

| plays/followers | Plays | Followers | Len | Account | Description |
|---|---|---|---|---|---|
| 21.36× | 572,714 | 26.8K | 169s | @rickbenn.ai | build a real ai agent in under 60 seconds |
| 23.21× | 182,446 | 7.9K | 35s | @lwazi.ai | Comment "AI" and I'll send you everything… |
| 12.82× | 110,190 | 8.6K | 33s | @liamjohnston.ai | Stop wasting time manually building automations |
| 11.82× | 202,645 | 17.1K | 59s | @oliver.merrick | How to make n8n flows 10x faster! |
| **10.44×** | 458,779 | 43.9K | 117s | **@trystring** | **the copy/paste n8n bros only trying to make money** |
| 0.70× | 574,740 | 817.8K | 92s | @sabrina_ramonov | Top seven AI tools to build AI agent teams |
| 0.15× | 121,789 | 817.9K | 34s | @sabrina_ramonov | Build your FIRST AI Automation in n8n |
| 0.14× | 116,047 | 817.9K | 51s | @sabrina_ramonov | is n8n dead? Here's my take |

**The cross-platform inversion.** Sabrina Ramonov is the one creator present in
both datasets. On YouTube Shorts she runs **2.50× and 2.98× above her own
baseline**. On TikTok the same subject matter reaches **0.14×–0.70× of her
follower count** — three separate videos, all under 1×. n8n instruction is
travelling on Shorts and stalling on her TikTok. n=3 on one creator, so this is
an observation to test, not a pattern.

---

## 3. Stage 4 — verbatim hooks

Every line below is transcript text, quoted exactly. Timestamps are the API's.

**20.59× — Sanji Nai-Chien**
> "Claude can now generate entire motion graphics videos, and I don't think people realize how fast motion design is changing."

**13.05× — David Ondrej**
> "Claude code right now eight year. The OG CLI agent it's still amazing, but table is getting removed from the…"
*(ASR is mangled — "eight year" is almost certainly "A-tier". The structure survives: verdict first, no preamble.)*

**12.14× — Eric Tech**
> "Most CRMs are just a place to track contacts, you never look at again. Attio goes beyond that. It's the AI CRM that…"

**9.78× — Quinn Nolan**
> "Here's a $99 per month automation that you can sell to home service businesses. After they complete an appointment, we're going to send their customers a…"

**3.84× — David Ondrej**
> "Running one tab all day. >> Yeah, that's not optimal at all because you're going to be wasting your limits…"

**3.63× — Matt Pocock**
> "Our coding feels exhausting." *(ASR for "AI coding feels exhausting")*

**3.48× — Jack Roberts**
> "This is one of the most slept on GitHub repos right now because this skill deletes AI slop from your writing."

**2.99× — Matt Pocock**
> "Most harnesses, but especially Claude Code, ship with a ton of bloat in the system prompt."

**2.98× — Sabrina Ramonov**
> "This is the one thing that made me a hundred twenty thousand dollars. I got forty-one point nine million views last month, but this one reel made me a…"

**2.69× — Jack Roberts**
> "Stop building AI skills from scratch because this free MCP gives your AI more than 80,000 skills to choose from."

**2.58× — Nate B Jones**
> "Here's something strange that everyone using AI is noticing right around the same time. The tools keep getting…"

**2.50× — Sabrina Ramonov**
> "Studying? Use this. For business? Definitely use this. Make AI videos? This is way cheaper than Pictory."

**TikTok, same treatment:**

- **@trystring (10.44×)** — "if you're thinking of starting an AI automation business, pause, because I'm gonna tell you w[hy]…"
- **@oliver.merrick (11.82×)** — "If I was a beginner in automations, I would just have AI create them for me where I just ask…"
- **@liamjohnston.ai (12.82×)** — "Claude Code can build a complete Nathan workflow from a single prompt and you can sell it to businesses right away." *(ASR: "Nathan" = "n8n")*
- **@rickbenn.ai (21.36×)** — "so let me show you how to build an AI agent with no code in about 30 seconds"

### What the hooks actually share

Counting across all 16 verbatim openings:

| Property | Count | Note |
|---|---|---|
| Declarative statement, no question | 15/16 | only @trystring uses an imperative interrupt ("pause") |
| Names a specific product in the first sentence | 11/16 | Claude, Attio, n8n, Higgsfield, Blotato, Pictory, GitHub |
| Contains a hard number | 6/16 | $99/mo, $120K, 41.9M, 80,000, 89,000, 30 seconds |
| Opens with a negative or a complaint | 5/16 | exhausting, bloated, slop, "Most CRMs are just…", "Stop…" |
| First-person "I built…" framing | **0/16** | see §6 |

**The shape that wins here is: flat declarative claim → named tool → number.**
No curiosity gap, no withheld payoff, no question. The single highest performer
in the on-niche set states a capability and then states that people are
underrating it. That is the whole hook.

**Visual (n=1, Gemini).** The 20.59× winner opens **split-screen**: the Claude
interface running a prompt on top, the creator at a mic below, overlay text
`CLAUDE MOTION IS INSANE`, one cut inside the first three seconds, face on
screen. The tool UI is on screen at 0:00 — doing something, not sitting there as
a logo.

---

## 4. Stage 5 — comment mining

### 4a. A caveat that has to come first: this niche's comments are contaminated

Three separate TikTok videos carry near-identical unsolicited plugs for the same
product:

> "i've been using **workbeaver ai** for that vibe, no setup, no config. i just show it once and it takes over." (525 likes)
> "i had a smoother experience with **workbeaver** since it works through…" (340 likes)
> "I tried the Claude+n8n combo but it felt like overkill for me. I use **WorkBeaver** now." (96 likes)

And @lwazi.ai's comments are dominated by testimonial spam in one voice:

> "Started AI dropshipping out of pain now I'm making over 10k monthly and helping my family" (272 likes)
> "The same person who used to worry about rent now runs an AI dropshipping store making 8K weekly."

**Treat like-counts in this niche as unreliable.** The findings below are drawn
from comments that argue with the video's substance — the pattern astroturfing
does not imitate.

### 4b. Objection 1: cost. The dominant objection, and no hook addresses it

This is the single most repeated theme across both platforms:

> "They always 'forget' to mention the part about the COST of CREDITS."
> "It cost $300 per 10 minutes video"
> "Yeah… You lost me as soon as you mentioned Higgsfield. 🙄 That sh*t is hella expensive."
> "No one shows the iterations and credits it takes."
> "n8n costs :(" · "You forgot to mention the llm api is paid" · "How much a month?"
> "Do i need a n8n subscription for this?" · "Do I need a Claude Subscription for this?"
> "n8n automation price"

Nine separate cost complaints across five videos. **Zero of the 16 hooks mention
price.** Quinn Nolan's 9.78× hook is the only one that puts a dollar figure up
front — and it is a figure the viewer *earns* ($99/mo revenue), not one they pay.

### 4c. Objection 2: undisclosed sponsorship and sameness

> "This is the 5th creator I've seen pushing Higgsfield, they must be paying big money for referrals."
> "You are the 10th person to make the sane exact video, same exact graphics, same exact samurai etc…😶"
> "these guys get sponsored by Higgsfield, so they just come here and act like it's just one prompt… No one shows the iterations and credits it takes."

The audience is tracking cross-creator repetition and reading it as paid. Note
this is on the **20.59× top performer** — overperformance and audience distrust
coexist in the same comment section.

### 4d. Objection 3: technical misattribution

> "saying Claude can generate motion, while actually it's just talking to Higgsfield via MCP is the same as praising McDonald's for discovering potatoes"

> "There is very little overhead in having 12 MCP servers installed. Only the tool definitions go into the context."
> "But can't claude contextually load MCP servers as it requires them to avoid bloat? Hasn't that been an option for quite some time now?"

A technically literate subgroup fact-checks claims in the replies. On David
Ondrej's MCP video the correction is *more specific* than the video.

### 4e. Objection 4: "it's not that easy"

> "its not that easy bro, you still gotta build 80-90% of the automation"
> "How many hours of Refactoring did you go through that you didn't mention?"
> "Why in the hell would I want to harass my customers?"

### 4f. The format finding: ranking content farms "what about X"

David Ondrej's tier list (13.05×) drew almost entirely omission callouts:

> "No OpenCode and Hermes Agent being here is diabolical"
> "I'd love to know why you've forgotten about OpenCode?" · "what about hermess agent"
> "What about cline? I use it with VS and get very good results." · "What about Deepcode CLI?"
> "So cursor is high a tier or s tier, just curious" · "Pi lets you use existing SUBSCRIPTIONS???"

A ranking with a *defensible verdict* generates argument automatically, because
every omission is a grievance. That is a structural engagement property of the
format, not a function of the script.

### 4g. The richest audience language is emotional, not technical

Matt Pocock's "AI Coding is exhausting" (3.63×) produced the most quotable
material in the entire pull:

> "It takes the joy out of it. It's like being full time code reviewer and full time product owner, and never doing actual development anymore."
> "Coding used to be like driving, once you laid the design foundations you're on autopilot"
> "Exhausted, exhilarated, and overwhelmed."
> "We all need a holiday. I'm cooked man"
> "I liked the autocomplete stage, not a fan of this phase, and almost certainly will hate the next one when I'm a barista."
> "There's a 1983 paper called 'Ironies of Automation' that describes exactly this problem. Automation removes the easy stuff and leaves the hard stuff."
> "Additionally I find myself doing more things in parallel, jumping between agents as one is working. So the added context shift exhausts me on top"

And the sharpest business insight in the set came from @trystring's comments —
the top-liked substantive comment across all 178 mined:

> "Upper managment still doesnt know how to find outllook on their computer" (816 likes)
> "Look how easy it is to build websites these days, yet business owners still pays thousands for websites simply because t[hey can't]" (248 likes)
> "Many businesses owners still using fax, and you spect them to be up to date with the latest open ai update?" (28 likes)
> "There are still businesses that pay $500/month for a Wordpress website built 25 years ago when that was the hype." (169 likes)

The audience's own thesis: **the moat is not technical difficulty, it is buyer
ignorance.** Nobody in the dataset has built a hook on that.

Also worth noting — @trystring's own audience caught the contradiction:
> "So Ai sales is cooked and a scam but you're selling Ai successfully? I'm confused" (471 likes)

---

## 5. Stage 6–7 — hook and trend read, now evidence-backed

**Hook patterns that measurably work here**, ordered by evidence strength:

1. **Flat capability declaration + "people don't realize"** — 20.59×. No loop.
   States a fact, then states that the fact is underrated.
2. **Ranked verdict** — 13.05×, and it farms argument in the replies (§4f).
3. **Problem-first, then name the product** — 12.14×. The tool arrives at 1.84s,
   *after* the pain is stated. Not a logo cold open; a complaint cold open.
4. **Revenue-specific offer** — 9.78× on 6,251 views. "$99 per month automation
   you can sell to home service businesses" names buyer, price and mechanism in
   one sentence.
5. **Named-emotion complaint** — 3.63×, 3.84×, 2.99×. Lowest ratios but by far
   the highest-quality comment sections.

**Trend read.** The open-mode run called this "late Growth, entering Peak" with
backlash "not yet dominant." The measured data moves that: backlash content is
already here **and already overperforming** — @trystring at 10.44×, Matt Pocock
at 3.63× and 2.99×, David Ondrej at 3.84×, Nate B Jones at 2.58×. Five of the
sixteen top hooks are complaints about the niche itself.

Revised verdict: **at Peak, with the critical lane already open and paying.**
Instructional "here's how to build an agent" content is the crowded lane; the
uncrowded one is the honest cost-and-limits account. Both the highest-liked
comments and several strong ratios sit there.

---

## 6. Where the open-mode report was wrong

Four explicit corrections. The old §4 was inference; this is transcript.

**1. "I built an AI agent that…" is NOT the strongest surviving pattern.**

> Previous report, §4: *"'I built an AI agent that…' — still works, because the
> loop is genuinely open… This is the strongest surviving pattern in the niche."*

**Measured: 0 of 16 outlier hooks use first-person build framing.** Not one. The
winning frame is second- or third-person and declarative — "Claude can now…",
"Most CRMs are…", "Here's a $99 per month automation *you* can sell". The
previous report predicted the single pattern that does not appear in the data at
all.

**2. List and ranking formats were called dead. They are among the strongest.**

> Previous report, §4: *"'Top 5 AI tools you need in 2026' — a list promise. The
> viewer can guess the contents. Fails question 2: eminently scrollable."*

**Measured: the tier list is the 2nd-highest on-niche performer at 13.05×**, and
Sabrina Ramonov's rapid-fire task→tool list runs 2.50×. What the old report got
right is narrower than what it claimed: a *numbered countdown* is guessable, but
a **ranking with a verdict** is not — the viewer stays to find out whether they
agree, and then argues in the comments (§4f). The list wasn't the problem; the
absence of a defensible opinion was.

**3. "Tool-logo cold open — anti-pattern to kill on sight" is too broad.**

> Previous report, §4: *"A Short that starts on a product logo has spent its
> first second on a brand the viewer has no reason to care about."*

**Measured: the 20.59× top performer opens with the Claude interface on screen at
0:00** (Gemini, n=1) and names the product in word one of the script. The
12.14× video names "Attio" at 1.84s. The real distinction is not logo-vs-no-logo
but **static brand mark vs. tool visibly doing something**, and whether a stated
problem precedes it. Refined, not reversed — but as written the old rule would
have vetoed the best video in the set.

**4. The backlash timing was called early.**

> Previous report, §3: *"'Enough of this' commentary ⚠️ not yet dominant."*

**Measured: five of sixteen top hooks are backlash**, including a 10.44× TikTok
whose entire thesis is that the niche is a grift. Not merely present — it is one
of the better-performing lanes. See §5.

**What the old report got right**, and the data supports: supply-side saturation
is real ("You are the 10th person to make the sane exact video"); proof is the
scarce good (§4b–4e are all demands for proof); identity call-outs work
(@trystring, @oliver.merrick, Quinn Nolan all filter in the first line).

**Untested.** The old report's §1 — AI-label mechanics, permanent disclosures,
the Mohan letter figures — is platform-policy sourcing that this run neither
confirms nor contradicts. It does not touch per-video performance and stands as
it was.

---

## 7. Stage 8 — content ideas, from measured gaps

Ranked by evidence, with the finding each rests on.

| # | Idea | Hook shape | Evidence |
|---|---|---|---|
| 1 | The real monthly bill for a "one-prompt" AI video — credits, retries, API | Flat declarative + number | §4b, 9 cost complaints, 0 of 16 hooks address it |
| 2 | Your buyer still can't find Outlook. That's the whole business. | Contrarian | 816-like comment, the top substantive comment in the set |
| 3 | "Claude generated this" — no it didn't, it called Higgsfield via MCP | Correction | The McDonald's/potatoes comment, §4d |
| 4 | The $99/mo automation, priced out end to end | Revenue-specific | Quinn Nolan 9.78× on 6,251 views |
| 5 | AI coding tier list — with the omissions argued for on purpose | Ranked verdict | 13.05× + §4f comment mechanics |
| 6 | "Full-time code reviewer, never developing" — the exhaustion nobody sells | Named emotion | §4g, richest comment section in the pull |
| 7 | Ironies of Automation (1983) explains your 2026 workflow | Contrarian + authority | Surfaced by a commenter, unclaimed |
| 8 | Why the same samurai clip is in 10 different creators' videos | Callout | §4c, audience already sees it |
| 9 | The 80% of the automation nobody films | Proof | "you still gotta build 80-90%" |
| 10 | Searching "AI agent" on Shorts returns cartoons, not tools | Data | §1, our own pull |

**Idea 1 is the strongest opportunity in this dataset.** It is the most repeated
audience objection across both platforms and it appears in none of the sixteen
top-performing hooks.

---

## 8. Stage 9 — scripts

Built to `viral-youtube-shorts`: under 30s → ~65%+ APV; 30–60s → ~50%+. Both
target 30–45s. Both use the measured shape from §3: **declarative open, named
tool, hard number, no question.**

### Script A — "What the one-prompt video actually costs" (41s)

> Idea 1. Evidence: §4b. Target 50%+ APV.

| Time | Visual | Audio / on-screen |
|---|---|---|
| 0:00–0:04 | Split-screen: tool UI mid-generation, creator at mic | **"One prompt made this video. It also cost `$[YOUR NUMBER]`, and nobody shows you that part."** |
| 0:04–0:10 | Credit balance draining, counter overlay | "Not the subscription. The credits. Every retry is a fresh charge." |
| 0:10–0:20 | Receipt-style list building on screen | "`[N]` generations before one that's usable. Plus the LLM API behind it. Plus the n8n plan if you're wiring it up." |
| 0:20–0:30 | Two columns: Advertised vs Actual | "Advertised: one prompt. Actual: `$[YOUR NUMBER]` and `[YOUR TIME]` for sixty seconds of footage." |
| 0:30–0:41 | Creator to camera, no cut | "It's still cheaper than a motion designer. I just think you should know the number before you budget the month, because nobody selling you the tool is going to say it." |

> **Fill the bracketed values from your own billing before shooting.** They are
> deliberately left blank: the entire premise of this script is a real measured
> cost, and inventing one would reproduce the dishonesty §4c documents. The only
> figure this dataset supplies is an audience claim — *"It cost $300 per 10
> minutes video"* — which is a commenter's assertion about Higgsfield, not a
> verified price, and should not be quoted as fact.

**Retention design.** The split-screen open with the tool *working* is the 20.59×
pattern (§3, Gemini n=1). The number lands at 0:02 — no withheld payoff, matching
15 of 16 measured hooks. The 0:20 turn is the re-hook. The close concedes the
tool is worth it, which keeps it from reading as anti-AI and holds the pro-tool
half of the audience through the last third.

**Title:** What the "one prompt" video actually costs
**Caption:** Credits, retries, API, plan. The real monthly number. What's yours been?
**Pinned comment:** full cost breakdown, itemised.

---

### Script B — "Your buyer can't find Outlook" (36s)

> Idea 2. Evidence: §4g, 816-like comment. Identity call-out.

| Time | Visual | Audio / on-screen |
|---|---|---|
| 0:00–0:04 | Creator to camera, hard cut in | **"If you're stuck picking an automation niche, you're solving the wrong problem."** |
| 0:04–0:11 | Screen: n8n canvas, then a fax machine | "The build isn't the moat. Anyone can copy your workflow in an afternoon." |
| 0:11–0:21 | Split: slick dashboard vs. someone hunting a desktop icon | "The moat is that your buyer still can't find Outlook on their own computer. There are businesses paying five hundred a month for a WordPress site built in 2001." |
| 0:21–0:30 | Invoice, line item reading "setup + monthly" | "They're not paying for difficulty. They're paying to not think about it. That's a service business, not a tech business." |
| 0:30–0:36 | Creator, hold, no CTA card | "So stop optimising the workflow. Go find the person still using fax." |

**Retention design.** Identity call-out at 0:00 filters hard and holds the
survivors — the §5 pattern. Every claim is a real comment from §4g, so the
specifics are audience language rather than invented detail. No follow prompt:
`viral-captions-and-ctas` treats generic follow CTAs as reach-suppressing, and
the closing instruction is more re-watchable than an ask.

> **Measured against a real voice.** Script B's narration was synthesised with
> Kokoro (`am_michael`, speed 1.0) and timed per scene. The storyboard above is
> an estimate; these are the numbers.
>
> | scene | storyboard | measured | delta |
> |---|---|---|---|
> | s1 hook | 4.0s | **5.17s** | +1.17 |
> | s2 | 7.0s | 5.40s | −1.60 |
> | s3 | 10.0s | **11.15s** | +1.15 |
> | s4 | 9.0s | 7.38s | −1.62 |
> | s5 | 6.0s | 5.45s | −0.55 |
> | **total** | 36.0s | **34.55s** | −1.45 |
>
> The total is close, which hides the problem: **the hook needs 5.17s, not 4.0s
> — 29% over its slot.** Cutting it to fit would mean cutting the identity
> call-out that §5 says does the filtering. The fix is to take the 1.6s back
> from s2 and s4, both of which came in under. `audio-acquisition` states the
> rule this demonstrates: measured narration duration is the scene clock, so
> narration is synthesised *before* footage, never after.

**Title:** Your buyer can't find Outlook
**Caption:** The moat isn't technical. Who's the least technical client you've closed?

---

## 9. Follow-up: two defects in `youtube-research`

Both blocked this run and were worked around outside the skills tree, since
`CLAUDE.md` requires it stay byte-identical to upstream.

1. **`find_outliers.py` cannot return Shorts.** `type=video` is hardcoded at the
   search-params list. The API accepts `type=short` (verified, HTTP 200, returns
   12–72s videos). As shipped, a Shorts research run returns long-form only —
   the first pass here gave 9 videos of 763s–17,562s and zero Shorts.
2. **The transcript parser is out of date with the API.** It reads
   `data["segments"]`; the endpoint returns `{"items":[{"events":[{"startMs","text"}]}]}`.
   It fails silently — printing "Fetched 0 transcripts" on HTTP 200 responses —
   which reads as "no transcripts exist" rather than "parser mismatch."

Both should go upstream to `ScrapeCreators/social-media-research-skills` rather
than be patched locally.

---

## Sources

All performance figures: TubeLab `/v1/search/outliers` and ScrapeCreators, pulled
2026-08-27. Run artifacts in `youtube-research/2026-08-27_083911/`
(`shorts-outliers.json`, `comments.json`, `tiktok-raw.json`, `tiktok-deep.json`,
`video-analysis.json`) — gitignored; regenerate from the scripts noted above.

Videos cited, in ratio order: [Lt1jJmG3l_k](https://www.youtube.com/shorts/Lt1jJmG3l_k) ·
[H-MU1gXsf2U](https://www.youtube.com/shorts/H-MU1gXsf2U) ·
[QC3ChcrKHu4](https://www.youtube.com/shorts/QC3ChcrKHu4) ·
[_aT_SVlxmJk](https://www.youtube.com/shorts/_aT_SVlxmJk) ·
[8oLkAlk2AbY](https://www.youtube.com/shorts/8oLkAlk2AbY) ·
[Z1NTwYuuvvw](https://www.youtube.com/shorts/Z1NTwYuuvvw) ·
[e-pFrQ_Rh0s](https://www.youtube.com/shorts/e-pFrQ_Rh0s) ·
[dUHpFuUIyi0](https://www.youtube.com/shorts/dUHpFuUIyi0) ·
[oLx4yCbeklQ](https://www.youtube.com/shorts/oLx4yCbeklQ) ·
[KdWdEq9rnIc](https://www.youtube.com/shorts/KdWdEq9rnIc) ·
[h8e334CiG1M](https://www.youtube.com/shorts/h8e334CiG1M) ·
[nYL2tunaHxA](https://www.youtube.com/shorts/nYL2tunaHxA) ·
[ioni7VijCdM](https://www.youtube.com/shorts/ioni7VijCdM)

TikTok: [@rickbenn.ai](https://www.tiktok.com/@rickbenn.ai/video/7488433859810364694) ·
[@lwazi.ai](https://www.tiktok.com/@lwazi.ai/video/7627605980838153493) ·
[@trystring](https://www.tiktok.com/@trystring/video/7555625844241190199) ·
[@oliver.merrick](https://www.tiktok.com/@oliver.merrick/video/7513519539708120338) ·
[@liamjohnston.ai](https://www.tiktok.com/@liamjohnston.ai/video/7607192428428201223)
