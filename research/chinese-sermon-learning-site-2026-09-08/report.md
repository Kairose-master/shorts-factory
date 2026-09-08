# 새오름교회 설교 → 중국어 학습 사이트 · 요약 영상 — 제작 기록

**Method.** Mode: API (GEMINI_API_KEY only; ScrapeCreators/Apify/TubeLab deliberately unused — no
audience research was requested and none would change an internal church learning asset). Sources: five
worship decks uploaded by the user (2026-08-02, 08-17 유치부, 08-23, 08-30, 09-06), bolls.life Bible
API (和合本 CUNPS, 개역한글 KRV). Sample: 4 adult sermons (48–83 paragraphs each, ko/zh parallel) +
1 children's lesson (ko only). Date: 2026-09-08. Not checked: any performance data — nothing has been
published yet, so no view/retention claims are made anywhere.

## What was built (lives in `kairose-master/Chinese-pastor`, branch `claude/chinese-sermon-learning-site-8hrbv3`)

- `pipeline/` — PPTX → structured sermon JSON → Gemini enrichment (summary, outline, 8 verbatim key
  sentences, 24 zh words + 12 ko words with in-sermon examples, 4 grammar patterns, 10-question quiz,
  video beats) → 9:16 MP4 (Pillow cards + Gemini TTS + ffmpeg) with VTT/SRT.
- Static site: series timeline, summary, scripture (deck text vs CUNPS/KRV diff), parallel reader
  with hide-and-reveal, vocabulary with browser TTS, Leitner flashcards, quiz, video with clickable
  cue list, global vocabulary ranked by recurrence, in-browser PPTX/JSON import (optional Gemini key).
- 5 rendered videos, 100–124 s each, 5.9–7.1 MB.

## Skills used and how

| Skill | Used for |
|---|---|
| `shorts-factory` | this Method block and the hard rules (cite or drop, no virality promise) |
| `video-formats` | Explainer grammar: one idea per card, card carries the short form, voice the sentence |
| `viral-short-form` / `viral-youtube-shorts` | hook = the week's greeting line (question/imperative), loop the close back to the hook, no logo/intro frame |
| `remotion-captions` | cue JSON shape (`start/end/text`) mirrored in `<id>.script.json` |

Video hooks, quoted verbatim (Chinese narration, Korean subtitle on card):

- 08-02 「与神的爱是无法隔绝的！」
- 08-17 「遇到喜欢的人，我们会怎么做？」
- 08-23 「看着教会里空着的座位，你是否感到空落落的？」
- 08-30 「让我们一起撒下盼望的种子。」
- 09-06 「我们都是被差遣的人。」

## Findings worth carrying into the next run

1. The greeting line the pastor makes the congregation say to each other is the natural hook and the
   natural memorise-this sentence; it appears in every adult deck.
2. The four adult sermons are one series (vacation → new semester → sending). Series navigation
   matters more than a flat list.
3. Deck hygiene issues found (church name differs on 08-30, a benediction typo repeated three weeks,
   two Chinese slips in 08-02) are listed in `IMPROVEMENTS.md` in the site repo.
4. Gemini `gemini-2.5-pro` is closed to this key (404); `gemini-3.1-pro-preview` was used.

## Cost

6 Gemini text calls (~30k input tokens each), 71 TTS calls, 0 paid scraping calls.
