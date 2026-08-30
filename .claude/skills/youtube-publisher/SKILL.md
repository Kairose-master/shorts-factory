---
name: youtube-publisher
description: Package a finished longform episode for YouTube — title candidates, description, tags, chapters, end screen, SRT upload — and gate the actual publish behind explicit human approval every time. Use when an episode has passed QA and needs metadata and upload, or when writing the videos.insert call.
---

# youtube-publisher

Packaging and upload. **The publish itself is never automatic.**

## The gate

A publish requires all four, plus a human:

```
SCRIPT_PASS      philosophy-script produced a locked script
THEOLOGY_PASS    theology-red-team, required fixes present in the cut
VIDEO_QA_PASS    video-red-team ≥85, no mandatory failure
THUMBNAIL_PASS   thumbnail-director, thesis-honest
       ↓
HUMAN APPROVAL   explicit, per episode, every time
```

**A successful render is not an approval. A passing QA score is not an
approval.** Neither is a previous episode's approval — permission does not carry
forward. Present the four verdicts, the cut, the thumbnail and the metadata, and
ask. For a channel touching religious subject matter, an unreviewed publish is
not a process slip; it is the whole risk.

## Metadata

### Title

Three candidates minimum. For an essay:

- Put the **question** in the title, not the answer.
- The specific noun beats the category noun — a concrete situation reads as a
  story; a topic reads as a lecture.
- 25–45 Korean characters. Front-load the distinctive part; mobile truncates.
- No manufactured urgency, no "충격", no "논란".

### Description

First two lines are what shows before "더보기" — make them do work. Then:

- one paragraph on what the episode actually argues
- **an explicit statement that the episode is a thought experiment, not a
  doctrinal declaration**, where the subject matter warrants it
- chapters
- sources or further reading
- no keyword stuffing

### Chapters

From the storyboard's scene boundaries — they already are the structure.
`00:00` first, minimum three, ≥10s apart, named for the *turn* rather than the
topic ("완벽한 복제", not "복제에 대하여").

### Tags

10–15, specific over broad. Broad tags on a niche essay put it in a pool it
cannot win.

## Uploading

Requires `YOUTUBE_API_KEY` plus an OAuth client — an API key alone cannot upload,
which is a common and time-wasting misreading of the docs. `videos.insert` with
`part=snippet,status`, resumable upload for a file this size.

**Always upload as `private`.** Never `public` directly from a script. Let a
human flip it in Studio after they have watched the processed video — processing
occasionally damages a file in ways no local check catches.

Then: `captions.insert` for the Korean SRT (do not rely on auto-captions for
Korean theological vocabulary), and `thumbnails.set`.

If the credential is missing, say which variable is unset and what it would
enable, and hand back the finished bundle for manual upload. Never invent a
credential, and never fall back to some other route to get the file onto the
platform.

## The bundle

```
export/
├── final.mp4
├── thumbnail.png
├── subtitles.srt
└── metadata.json     title candidates · description · tags · chapters · gate verdicts
```

`metadata.json` carries the four gate verdicts alongside the metadata, so the
approval request and the evidence for it are one artifact.
