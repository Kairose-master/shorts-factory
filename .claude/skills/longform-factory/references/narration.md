# Narration — engines, fitting, and what actually goes wrong

Everything here was learned by generating a full episode, not by reading docs.

## Engine choice

| Engine | Key | Korean | Throughput | Verdict |
|---|---|---|---|---|
| **Edge TTS** (`edge-tts`) | none | 3 neural voices (InJoon · SunHi · HyunsuMultilingual) | ~1–2s per line, no quota seen | **Default.** |
| Gemini TTS | `GEMINI_API_KEY` | good, takes a Korean style prompt | **10 requests/day/model on free tier** | Unusable for longform |
| Piper / eSpeak | none | weak or robotic Korean | fast | Timing drafts only |
| ElevenLabs / Qwen3-TTS | paid | excellent | fine | When budget exists |

**The Gemini trap.** Gemini TTS follows direction better than anything else free
— you hand it a paragraph of Korean describing the delivery. It is also capped
at **10 generate-requests per day per model** on the free tier. Three TTS models
is ~30 calls; an eleven-minute episode needs ~120. Verify the quota before
planning around it:

```bash
# the 429 body names the exact limit
#   quota: GenerateRequestsPerDayPerProjectPerModel-FreeTier  value: 10
```

**Never mix engines within an episode.** Same rule as the avatar: one voice, one
source. A scene generated on a different model is a timbre change mid-episode.

### edge-tts behind a proxy

`edge-tts` opens a **direct** websocket with a `certifi`-only SSL context, so in
a proxied container it both bypasses `HTTPS_PROXY` and fails to trust the
proxy's CA. Point it at both — extending trust to the configured CA, never
disabling verification:

```python
import ssl, os, edge_tts.communicate as C
C._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
proxy = os.environ.get("HTTPS_PROXY")
await edge_tts.Communicate(text, voice, proxy=proxy).save(path)
```

## One file per beat

Generate **per beat**, never per scene. The storyboard is the pipeline's single
timing source, so each line can be laid down at its own `t` and drift becomes
impossible by construction rather than merely small. It also makes a single
re-record a single call.

## Fitting: what goes wrong and in what order

Measured on the first episode: **47 of 118 lines overran their beats.** The
overall ratio was only 1.05x — the excess was concentrated in a few over-written
sentences. Fix in this order, and stop as soon as it fits:

1. **Trim the script.** A line that will not fit its beat is over-written. This
   is a script improvement, not a workaround — shorter lines are better spoken
   Korean, and most offenders carry two clauses where one would do.
2. **Move the beat grid** — only where no graphic depends on the boundary, and
   check the scene component before touching it.
3. **Time-compress the scene**, up to ~1.10–1.15x. Past **1.25x** speech starts
   to sound hurried; a scene needing more than that is telling you to go back
   to step 1.

**Guarded lines are never trimmed to make a scene fit.** When a red-team
required line cannot fit its slot, the *beat grid* moves. On this episode C-04
alone needed 4.6s in a 3s slot, so SCENE 04's tail was re-timed and its graphic
window moved with it.

## Placement rules

- **Reset at every scene boundary.** Without this a long sentence in scene four
  drags scene thirteen's audio out of sync with its graphics. A first pass here
  accumulated **14 seconds** of drift by the end.
- **Consecutive spoken lines pack**; a line preceded by a *non-spoken* beat is
  anchored to its own mark. Authored gaps — a silence, a UI sequence, a held
  graphic — are content, and speech must not creep into them. Anchoring *every*
  line instead strands the slack a congested run needs, which is what forces
  unnecessary compression.
- Decide compression from **where the last line actually lands**, not from the
  scene's total load. A scene can sit at 92% of capacity and still overrun,
  because a 19-second mid-scene gap is unusable by the lines after it.

## The music bed

Synthesise it. The bed has to fall to *complete* silence for named scenes and
return without a swell; cutting a found track to that shape is harder than
generating one, and a generated bed is unambiguously yours to publish. Duck it
under speech so the pad never competes with a consonant.

A bed that builds toward the conclusion tells the viewer the episode reached
one. If the essay refuses to answer, the music has to refuse too.
