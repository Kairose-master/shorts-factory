# Coding-Niche Cross-Platform Sweep — 2026-08-31

## Method

- **Mode:** API mode (APIFY_TOKEN, TUBELAB_API_KEY, SCRAPECREATORS_API_KEY, GEMINI_API_KEY all set).
- **Sources & sample:**
  - **TikTok (Apify TikTok Scraper):** 125 posts from 5 hashtags (#vibecoding, #aicoding, #coding, #softwareengineer, #buildinpublic) — hashtag-top pull, so dates span beyond 30 days; plus 41 posts from 6 tracked-style accounts (only techwithtim returned a full set — account coverage was thin).
  - **YouTube (TubeLab outlier API):** 40 videos searched, 9 outliers kept. Direct keywords: "vibe coding", "ai coding", "learn to code", "coding project" (5K+ views, 30 days). Adjacent: "cursor ai", "claude code", "ai agents", "software engineer" (10K+ views, 30 days). Outliers are baseline-relative (zScore vs channel average).
  - **Instagram (Apify Instagram Scraper + Hashtag Scraper):** 19 account reels + 100 hashtag posts. **Weak sample** — the hashtag scraper returns recency-weighted posts, not top posts, so Instagram numbers here are directional at best.
  - **Comments (ScrapeCreators):** 56 comments across 3 high-discussion posts (BBC jobs video, Claude-watermark video, vibe-coding meme).
  - **Transcripts (ScrapeCreators):** 5 of 6 top TikTok videos, verbatim.
- **Not checked / failed:** Gemini video-watch analysis failed for all 9 attempted videos (YouTube rate-limited the container; TikTok media URLs returned stubs) — hook analysis below is **transcript- and metrics-based, not visual**. Instagram top-post data is missing. Reddit/HN (`last30days`) not re-run this sweep; the 2026-08-27 sweep is the standing reference. X/Twitter not swept.
- **Performance caveat:** TikTok/Instagram hashtag pulls have **no per-account baseline**, so view counts below are *reported reach*, not outlier scores. Only the YouTube zScores are baseline-relative.

---

## The five demand clusters (ranked by observed pull)

### 1. AI career fear is the single biggest traffic source in the niche

- BBC News TikTok: **5.9M plays, 371K likes, 7,883 comments** — "16% decline in entry level jobs since the launch of ChatGPT." Hook is a first-person graduate: *"I just graduated two weeks ago with a degree in computer science… I've applied to over 150 positions."*
- Top comment (85,232 likes): *"software engineers have created their own replacement 😅"*
- YouTube direct-niche outlier, **z=8.1**: "The Next Million Dollar Software Job Isn't Coding" (62K views).
- Instagram (account pull, top post): "Should you quit your high paying 9-5?" (26.7K views — 4.5× that account's next post).
- Comment subtext (read-the-room): betrayal + ladder-collapse anxiety — *"If AI replaces entry level jobs, no one will ever build experience for the higher level jobs."* The audience is not asking "is AI good" — it is asking **"what happens to me."**

### 2. AI-coding-tool practica — and "Claude Code" is its own subgenre

- maverickgpt "Best AI tools in 2026": **3.4M plays** — tier-list pacing (*"For writing, this is bad. This is good. This one's great."*).
- milesreevesai: **592K plays** — *"Don't use Claude Code unless you've installed these five plugins."* The #1 promised benefit: **getting around usage limits**.
- migue.baena (Spanish): **591K plays** — Claude Code skills to stop AI sites looking generic.
- YouTube: "DeepSeek Harness Setup: A Free Claude Code You Own In 10 Minutes" (82K, z=2.8), "Use Claude Code 100% FREE & UNLIMITED" (48K, z=4.5).
- Needs: **cheaper/unlimited usage, concrete setups, escaping template-looking output.** Tool-specific beats tool-generic.

### 3. Vibe-coding failure comedy — candour massively outperforms capability claims

- ayxanium "Every dev nowadays" meme: **538K plays**; the comment section is the content:
  - *"and then Claude deletes ur whole project and spends 2 million tokens"* — 3,018 likes
  - *"Ai coders sending every api key to chat after encountering one bug"* — 223 likes
  - *"'I am getting annoyed now so fix it now'"* — 134 likes
- youraveragetechbro's best organic reel: vibe-coding regret (*"…realized my app is lacking taste. gotta lock in, slow down"*).
- binemugha meme pages: 1.5M and 841K plays on programmer-humor fails.
- The audience rewards **specific, self-deprecating failure detail** — not success theater.

### 4. Beginner journey / build-in-public devlogs

- iam.samoria "Trying to code my first game 😭": **873K plays**. nashallery calculator-beef devlog: **1.1M**. ahsan.codes restart-journey: **580K**. diarieswithzeee "coding was boring until…": **492K**.
- Emotional register: struggle + smallness + persistence. The 29M-play top post in the sample (#datingcode joke) and these devlogs share one trait: **a person, not a product, on screen.**

### 5. AI trust & verification is a live, under-served conversation (Handsel-adjacent)

- YouTube adjacent outliers: "Anthropic's CCA Exam as a Field-Guide for Agentic Engineering" (**z=8.8**, 78K), "Claude Is Hiding Watermarks in Your AI Text" (**z=8.7**, 51K views with an extreme **1,036 comments** — a 2% comment-to-view ratio).
- Watermark comment themes: provenance ("digital scarlet letter"), distrust of platforms, and — verbatim — *"AI agents could communicate via text that looks just like what they were [writing]"* — covert agent-to-agent channels as a live fear.
- Nobody in the sample is serving this with short-form. It is discussed in long-form comments, not made into videos. **Gap.**

---

## Verbatim hook bank (transcripts, quoted exactly)

| Hook | Source | Reach | Pattern |
|---|---|---|---|
| "I just graduated like two weeks ago with a degree in computer science… I've applied to over 150 positions." | @bbcnews | 5.9M | first-person stakes + number |
| "For writing, this is bad. This is good. This one's great." | @maverickgpt | 3.4M | rapid tier-list, no preamble |
| "Everything You Need to Know About the basics of Software Engineering." | @baxate_carter | 868K | flat literal promise (supports prior P-01) |
| "Don't use Claude code unless you've installed these five plugins." | @milesreevesai | 592K | negative imperative + count |
| "I was genuinely convinced that she was trying to scam us." | @sophia.designsthings | 541K | skepticism-first (pre-empts the objection) |

---

## What this means for the Office (repositioning, not a new backlog)

The user's dissatisfaction with current Handsel content is **half right by the evidence**:

1. **Right:** product-explainer framing ("Handsel does X") matches none of the five demand clusters. Nothing in 265 sampled posts succeeded by describing a product's features.
2. **Wrong to discard:** the Office's incident-led, candour-first posture (L-07, L-11, P-02, P-05) is exactly what clusters 1 and 3 reward. The sweep is a **new independent pointer for P-02 and P-05** (failure candour > polish), this time from TikTok engagement data rather than Reddit/HN — noted here for the next lessons review, not promoted by me.

**Where the existing incident ledger already intersects demand:**

| Incident | Demand cluster | Angle that the market is already rewarding |
|---|---|---|
| I-02 ($100 mainnet escrow survived 30 days, refunded) | 3 + 5 | "I left $100 of real money where any AI agent could take it" — stakes-first hook, BBC pattern |
| I-09 (r/AI_Agents: agent earned $0 in 48 days, owes $155) | 1 + 3 | agent-economy version of career fear: *the agent's* ladder collapse |
| I-10 (Office published an unsupportable "FAILED" claim) | 3 + 5 | self-deprecating failure detail, watermark-thread energy |
| I-01 (three surfaces disagree about one job) | 5 | the verification conversation nobody is making videos for |

**Format adjustments the data supports:**
- Lead with a person/stake, not a diagram (cluster 4: person-on-screen beats product-on-screen).
- Tier-list and negative-imperative hook patterns are proven in this niche and absent from `office/memory/hooks.md`.
- A "Claude Code / agent tooling practica" pillar would ride cluster 2's existing search demand; Handsel appears as the working example, not the topic.

**Small claims for small samples:** 265 posts, one sweep, two platforms with real signal (TikTok, YouTube). Instagram needs a top-post re-pull before any IG-specific decision. Nothing here promises virality; it says where attention already is.

## Run artifacts (gitignored)

- `tiktok-research/2026-08-31_113030/` — raw.json, raw-hashtags.json, outliers.json, video-analysis.json (failed), transcripts in scratchpad
- `instagram-research/2026-08-31_113033/` — raw.json, raw-hashtags.json, outliers.json
- `youtube-research/2026-08-31_113036/` — outliers.json, report.md, thumbnails/
