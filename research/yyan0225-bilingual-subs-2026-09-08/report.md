# @yyan0225 (새오름교회) — 한중 이중 자막 재구성 run

## Method

| | |
|---|---|
| **Run mode** | **API** — `APIFY_TOKEN` (video download), `GEMINI_API_KEY` (clean-up + translation). `SCRAPECREATORS_API_KEY`, `TUBELAB_API_KEY` set but not needed |
| **Date** | 2026-09-08 |
| **Source** | YouTube channel [@yyan0225](https://www.youtube.com/@yyan0225) — 새오름교회 (기독교대한감리회, 한국에 온 중국인 이주민을 위한 교회). The channel has exactly **2 public videos**, both processed |
| **Transcription** | faster-whisper `large-v3-turbo`, CPU int8, VAD on, word timestamps, run locally (free) |
| **Translation** | Gemini `gemini-3.5-flash`, ~23 requests total (50 cues per request, plus retries). One request per batch does light ASR correction **and** translation |
| **Render** | ffmpeg 6 + libass, Noto Sans CJK KR / SC, 1920×1080 30 fps, x264 CRF 21, AAC 160k, EBU R128 loudnorm to −16 LUFS |
| **Paid calls** | Apify `streamers/youtube-video-downloader`: **$0.45** (2 videos, 720p). Gemini: ~23 requests. Nothing else metered |
| **Not checked** | The translations were **not reviewed by a human**. Scripture quotations follow 和合本 / 개역개정 wording only as far as Gemini reproduced them; verify before publishing |

**Why Apify.** yt-dlp from this container hit YouTube's "Sign in to confirm you're
not a bot" on every player client (web, mweb, tv, ios, android, embedded), with
and without a PO-token provider, and headless Chromium got its connection reset.
The Apify actor downloads from its own infrastructure and returned both files in
about 3 minutes.

**What "재구성" meant here.** Both source videos are a **static title slide over
audio** (checked at 30 s / 400 s / 900 s — identical frames). There was nothing to
cut, so the visual was rebuilt instead: a blurred, text-free crop of the church's
own slide art as the background, an intro card, a persistent bilingual header,
large centred bilingual subtitles, a progress bar and a clock. The original slide
typography is not reused; every word on screen comes from the transcript or the
slide's own title/scripture/date/church lines.

---

## The two videos

Same sermon, two languages. Title, scripture and date come from the slide the
church uploaded, verbatim.

| | Korean service | Chinese service |
|---|---|---|
| Video | [OY3yK3gOdbo](https://www.youtube.com/watch?v=OY3yK3gOdbo) "2026 09 06 새오름교회 주일예배" | [-0PbFLRiDmM](https://www.youtube.com/watch?v=-0PbFLRiDmM) "2026 09 06 主日礼拜" |
| Length | 27:19 | 19:14 |
| Spoken | Korean (live sermon, ad-libs, congregation Q&A) | Mandarin (read delivery, close to a script) |
| Title on slide | 보내는 사람들, 그리고 보냄받은 사람들 | 差遣的人，与被差遣的人 |
| Scripture | 사도행전 13장 1-3절 | 使徒行传13章1-3节 |
| Church name on slide | 새오름교회 | 言盐教会 |
| Whisper segments → cues | 263 → **452** | 518 → **524** |
| Cues Gemini edited (ASR fix / punctuation) | 140 | 97 |
| Cues hidden as unintelligible | 0 | 0 |
| Subtitle layout | 한국어 (white) over 中文 (gold) | 中文 (white) over 한국어 (gold) |
| Output | `renders/OY3yK3gOdbo_juilyebae_ko-zh_1080p.mp4` | `renders/-0PbFLRiDmM_zhuriliba_zh-ko_1080p.mp4` |

| 1080p master | 74.9 MB | 54.1 MB |
| 720p delivery copy (mono 64k AAC) | 29.8 MiB | 21.8 MiB |

The 1080p masters exceed the 30 MiB file-delivery limit of this session, so the
720p copies were what went out; they are transcodes of the masters, not
re-renders. Both masters were checked frame-by-frame at four points (intro card,
early, middle, end) and measured at −16 LUFS integrated.

Renders are gitignored (`*.mp4`). Everything needed to regenerate them is
committed: the pipeline script, the corrected transcripts with timings
(`subtitles/*/bilingual.json`), the styled `.ass`, and the three `.srt` files per
video (source language, translation, both).

## Terminology decisions

- **하나님 → 神, not 上帝.** The church's own Chinese sermon says 神 21 times and
  上帝 never (counted in the Whisper transcript of -0PbFLRiDmM), so the Korean→
  Chinese pass was pinned to 神. Result: 神 ×20, 上帝 ×0.
- Names follow each Bible's convention: 안디옥/安提阿, 바나바/巴拿巴, 사울/扫罗,
  바울/保罗, 성령님/圣灵, 사도행전/使徒行传.
- 보내는 사람들 / 보냄받은 사람들 ↔ 差遣的人 / 被差遣的人 — the slide's own pairing.

## Known ASR errors that were corrected (examples, verbatim)

| Video | Whisper heard | Corrected to |
|---|---|---|
| zh | 题目《拆派的人》以及《蒙拆遣的人》 | 题目《差遣的人》以及《蒙差遣的人》 |
| zh | 安提亚 | 安提阿 |
| zh | 填补了空胃 | 填补了空位 |
| ko | 성냥님께서 말씀하실 때 | 성령님께서 말씀하실 때 |
| ko | 보낸받는 | 보냄받는 |
| ko | 저희 집이서가 만들어줬습니다 | 저희 집사님이 만들어줬습니다 |

The last one is a contextual guess by the model (a 집사님 is the plausible
speaker being credited). If a person's title matters, check it against the audio
at 0:39.

## What to review before publishing

1. **Scripture quotes** — Acts 13:1-3 is read aloud in both services; the
   translation line should match the church's Bible edition, not a paraphrase.
2. **The two hidden-cue thresholds are conservative** (nothing was hidden). If a
   hymn or prayer segment reads as garbage on screen, drop it in
   `bilingual.json` (`"garbled": true`) and re-run `build` + `render`.
3. **Loudness** — both audio tracks were normalised to −16 LUFS with a 70 Hz
   high-pass. The Korean service has room noise; nothing else was touched.

## Reproduce

```bash
python3 scripts/bilingual_subtitles.py run SRC.mp4 --lang ko --out work/ko \
  --reconstruct --bg-crop 640:360:640:360 \
  --title-src "보내는 사람들, 그리고 보냄받은 사람들" --title-dst "差遣的人，与被差遣的人" \
  --meta "사도행전 13:1-3 · 使徒行传 13:1-3  ｜  2026. 9. 6 주일예배 · 主日礼拜" \
  --badge "한국어 설교 · 中文字幕" --church "새오름교회 · 言盐教会" \
  --glossary "하나님=神 (never 上帝), 안디옥=安提阿, 바나바=巴拿巴, ..." \
  --mp4 renders/OY3yK3gOdbo_juilyebae_ko-zh_1080p.mp4
```

Swap `--lang zh` and the titles for the Chinese service. `--bg-crop` points at
the text-free bottom-right quarter of the 1280×720 slide. Stages are resumable:
delete `whisper_raw.json` to re-transcribe, `bilingual.json` to re-translate.
