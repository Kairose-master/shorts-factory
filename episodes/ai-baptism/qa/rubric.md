# QA — `ai-baptism`

Three gates before the cut can go to a human. Each names the failure it prevents.

## Gate 1 · THEOLOGY_PASS

Owned by `theology-red-team`. **Status: PASS WITH REQUIRED FIXES (2)** — both
present in script v1.1. See `script/theology-redteam.md`.

Carry-through is re-verified at Gate 2: a fix that lives only in the script file
and not in the delivered audio has not happened.

## Gate 2 · SUBTITLE_PASS

Owned by `subtitle-qc`. **Status: SKIPPED — no narration audio exists.**

An unrun check is not a pass. Re-run once `audio/narration.wav` exists:

```bash
python3 ../../scripts/subtitle_qc.py \
  --audio audio/narration.wav --script script/canonical.md \
  --storyboard storyboard/storyboard.json --out subtitles/
```

The four guarded lines it must find verbatim:

| Claim | Line | Why guarded |
|---|---|---|
| C-04 | 이건 인간과 AI가 같다는 얘기가 아닙니다. | blocks the equivalence inference the scene invites |
| C-12 | 하나님이 신성을 버리고 유한한 존재가 되었다는 뜻이 아닙니다. | the denial that makes S08 safe |
| C-13 | 하나님의 아들이 인간 본성을 취하여 역사 속 특정한 시간과 장소에 오셨다고 고백합니다. | the positive confession |
| C-14 | 무한하신 하나님이 작아지신 것이 아니라, 유한한 역사 안의 바로 그 자리에서 우리를 만나셨다는 것입니다. | RT-01's replacement; a paraphrase drifting back toward "좌표를 취하셨습니다" fails |

## Gate 3 · VIDEO_QA_PASS

Owned by `video-red-team`. **Status: PENDING — requires a cut with final audio.**

Minimum 85/100, and no mandatory failure. Episode-specific readings of the
mandatory list:

| # | Mandatory failure | Where it would show up here |
|---|---|---|
| 1 | First 10s unclear | S01 — the AI must be legible as *not a person* before it speaks |
| 2 | >15s visually static | S06 264–268 (4s silence) and S11 (68s hold) are the candidates. S11 is a **marked exception**: the content is the hold. S06's silence is inside the limit. |
| 3 | Central doctrinal distinction missing | S08 383–398, C-12/C-13 |
| 4 | Ending reads as an answer | S12–S13 — fails in **either** direction |
| 5 | Avatar inconsistent between scenes | S01/S02/S04/S05/S06/S07/S10/S11/S12/S13 all use it; one reference image drives all |
| 6 | Captions cover a face | S11 is the risk — the face is centre-frame for 68s |
| 7 | Narration sounds like corporate TTS | the whole episode; the strongest mitigation is a human read |
| 8 | Guarded line failed subtitle-qc | Gate 2 |

## Current build status

| | |
|---|---|
| Script | **LOCKED** v1.1 |
| Claim map | 21 claims · 4 guarded |
| Theology red team | PASS (2 required fixes applied) |
| Storyboard | **VALID** — 14 scenes, 157 beats, beats sum exactly, avatar 26.1% |
| Remotion composition | **BUILDS AND RENDERS** — 14 scene components, typecheck clean |
| Narration | **MISSING** — no TTS credential in this environment |
| Avatar lip-sync | **MISSING** — no CUDA GPU in this environment |
| Subtitles | SRT generated from storyboard; QC skipped pending audio |
| Thumbnail | concept chosen, renders as a Remotion Still |
| Cut review | pending final audio |
| Publish | **BLOCKED** — human approval required, and two gates are not yet run |

## What the current render actually is

A complete, correctly-timed 11:50 motion-graphics cut with **placeholder avatar
plates and no audio**. It is the right artifact for reviewing structure, pacing,
typography and visual density — the 74% of the episode that carries the argument.

It is **not** a reviewable cut for hook strength, narration quality or the
avatar. Do not score Gate 3 against it; those dimensions are not present to be
scored, and a score computed against absent inputs is worse than no score.
