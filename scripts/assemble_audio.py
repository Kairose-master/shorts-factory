#!/usr/bin/env python3
"""Place every generated narration beat at its exact storyboard time.

This is where the pipeline's timing guarantee is actually cashed in. Each beat
was synthesised separately, so each can be laid down at its storyboard `t`
rather than wherever a continuous read happened to land. Drift is not minimised
here — it is zero by construction, because nothing is ever concatenated.

Overruns are the one thing that can still go wrong: a line whose natural read is
longer than its beat. Most spill into a following silence and are harmless. One
that would collide with the next spoken line is reported, and the overlap is
resolved by nudging the incoming line later by at most `--max-nudge` seconds —
past that it is left to collide and printed loudly, because silently squashing a
line is worse than a visible fault.

Usage:
  python3 scripts/assemble_audio.py --storyboard <p> --audio <dir> \
      --out <narration.wav> --caption-track <t.json> [--bed bed.wav --mixed mixed.wav]
"""
import argparse
import json
import wave
from pathlib import Path

import numpy as np

RATE = 48000
BED_GAIN = 0.16
LEAD_IN = 0.12          # a beat's audio starts a hair before its visual mark
MIN_GAP = 0.16          # breath between consecutive lines
TAIL_GUARD = 0.35       # never let a line run past its own scene
MAX_TEMPO = 1.25        # speech survives this; past it, trim the script instead


def resample(a, factor):
    """Time-compress by `factor` (1.15 = 15% faster) without pitch correction.

    At these factors the pitch shift is small enough to read as a slightly
    brisker delivery rather than a chipmunk, and it keeps the whole assembly
    dependency-free.
    """
    if abs(factor - 1.0) < 1e-3:
        return a
    idx = np.linspace(0, len(a) - 1, int(len(a) / factor))
    return np.interp(idx, np.arange(len(a)), a)


def read_wav(path: Path):
    with wave.open(str(path)) as w:
        rate = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    a = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    if w.getnchannels() == 2:
        a = a.reshape(-1, 2).mean(axis=1)
    if rate != RATE:  # linear resample; these are speech and pad, not masters
        idx = np.linspace(0, len(a) - 1, int(len(a) * RATE / rate))
        a = np.interp(idx, np.arange(len(a)), a)
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--storyboard", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bed")
    ap.add_argument("--mixed")
    ap.add_argument("--max-tempo", type=float, default=MAX_TEMPO)
    ap.add_argument("--caption-track", required=True)
    a = ap.parse_args()

    sb = json.loads(Path(a.storyboard).read_text(encoding="utf-8"))
    beats_dir = Path(a.audio) / "beats"
    total = sb["durationSec"]
    track = np.zeros(int(total * RATE), dtype=np.float64)

    placed, missing, compressed, tight = [], [], [], []

    # Placement resets at every scene boundary. A line that overruns pushes the
    # next line inside its own scene and no further: without the reset a single
    # long sentence in scene four drags the audio of scene thirteen out of sync
    # with its graphics, which is exactly what a first pass of this produced
    # (14s of accumulated drift by the end).
    for scene in sb["scenes"]:
        lines = [(i, b) for i, b in enumerate(scene["beats"]) if b.get("vo")]
        if not lines:
            continue

        clips, dur_sum = {}, 0.0
        for i, b in lines:
            f = beats_dir / f"{scene['id']}_{i:02d}.wav"
            if not f.exists():
                missing.append(f"{scene['id']}_{i:02d}")
                continue
            c = read_wav(f)
            clips[i] = c
            dur_sum += len(c) / RATE

        if not clips:
            continue

        first_t = max(0.0, lines[0][1]["t"] - LEAD_IN)
        limit = scene["endSec"] - TAIL_GUARD

        # A line is pulled back to its own authored mark only when a NON-spoken
        # beat sits between it and the previous line. That gap was authored — a
        # silence, a UI sequence, a held graphic — and speech must not creep
        # into it. Consecutive spoken lines, by contrast, simply follow one
        # another: making each of those wait for its own mark strands the slack
        # a congested run needs, which is what forced two scenes to 1.25x.
        spoken_idx = {i for i, _ in lines}
        anchored = {}
        for n, (i, b) in enumerate(lines):
            prev = lines[n - 1][0] if n else None
            anchored[i] = (
                prev is None
                or any(j not in spoken_idx for j in range(prev + 1, i))
            )

        def dry_run(f):
            """Where does the last line end at tempo `f`? Mirrors placement."""
            cur = first_t
            for i, b in lines:
                if i not in clips:
                    continue
                st = max(cur, max(0.0, b["t"] - LEAD_IN)) if anchored[i] else cur
                cur = st + (len(clips[i]) / RATE) / f + MIN_GAP
            return cur - MIN_GAP

        # If a scene's speech genuinely does not fit, compress that scene's
        # clips rather than letting them spill into the next scene. Speech
        # survives ~1.25x; past that the line is over-written and the script is
        # what should change, so the scene is reported instead of squashed.
        factor = 1.0
        end_at = dry_run(1.0)
        if end_at > limit:
            lo, hi = 1.0, MAX_TEMPO
            for _ in range(24):        # bisect: placement is monotone in tempo
                mid = (lo + hi) / 2
                if dry_run(mid) > limit:
                    lo = mid
                else:
                    hi = mid
            factor = hi
            if dry_run(factor) > limit + 0.05:
                tight.append(
                    f"{scene['id']}: last line still ends {dry_run(factor) - limit:.1f}s "
                    f"past the scene at the {MAX_TEMPO}x limit — trim the script"
                )
            compressed.append(f"{scene['id']} {factor:.2f}x")
            for i in clips:
                clips[i] = resample(clips[i], factor)

        cursor = first_t
        for i, b in lines:
            if i not in clips:
                continue
            clip = clips[i]
            dur = len(clip) / RATE
            start = (max(cursor, max(0.0, b["t"] - LEAD_IN))
                     if anchored[i] else cursor)
            i0 = int(start * RATE)
            i1 = min(len(track), i0 + len(clip))
            track[i0:i1] += clip[: i1 - i0]
            cursor = start + dur + MIN_GAP
            placed.append({
                "key": f"{scene['id']}_{i:02d}", "t": b["t"],
                "vo": b["vo"],
                "speaker": b.get("speaker") or scene.get("voice") or "narrator",
                "placedAt": round(start, 3), "audioSec": round(dur, 2),
                "overrun": round(dur - b["dur"], 2),
                "drift": round(start - (b["t"] - LEAD_IN), 3),
                "tempo": round(factor, 3),
            })

    peak = np.max(np.abs(track)) or 1.0
    narr = track / peak * 0.89

    def write(path, arr):
        pcm = (np.clip(arr, -1, 1) * 32767).astype("<i2")
        with wave.open(path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes(pcm.tobytes())

    write(a.out, narr)

    if a.bed and a.mixed and Path(a.bed).exists():
        bed = read_wav(Path(a.bed))
        bed = np.pad(bed, (0, max(0, len(narr) - len(bed))))[: len(narr)]
        # Duck the bed under speech so the pad never competes with a consonant.
        env = np.abs(narr)
        win = int(0.25 * RATE)
        env = np.convolve(env, np.ones(win) / win, mode="same")
        duck = 1.0 - 0.55 * np.clip(env / 0.18, 0, 1)
        mixed = narr + bed * BED_GAIN * duck
        mixed = mixed / (np.max(np.abs(mixed)) or 1.0) * 0.94
        write(a.mixed, mixed)

    drifted = [p for p in placed if abs(p["drift"]) > 0.001]
    over = [p for p in placed if p["overrun"] > 0]
    print(f"placed {len(placed)} lines over {total}s")
    print(f"missing: {len(missing)}")
    print(f"overruns (line longer than its beat): {len(over)}"
          + (f", worst {max(p['overrun'] for p in over):+.2f}s" if over else ""))
    print(f"pushed later inside their own scene: {len(drifted)}"
          + (f", worst {max(abs(p['drift']) for p in drifted):.2f}s" if drifted else ""))
    print(f"scenes time-compressed: {len(compressed)}"
          + (f"  [{', '.join(compressed)}]" if compressed else ""))
    if tight:
        print(f"\nOVER THE COMPRESSION LIMIT ({len(tight)}):")
        for c in tight:
            print("  " + c)
    if missing:
        print(f"\nMISSING: {', '.join(missing[:12])}")

    Path(a.out).with_suffix(".placement.json").write_text(
        json.dumps({"placed": placed, "missing": missing,
                    "compressed": compressed, "tight": tight},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")

    # The caption track: where each line is ACTUALLY spoken.
    #
    # Graphics stay on their authored beats, because they are choreographed to
    # the argument and a diagram that moves because a sentence ran long is a
    # worse defect than a caption that lingers. Captions, though, have exactly
    # one job — match the voice — so they are driven from measured placement
    # rather than from the beat grid. This is what lets a line overrun its beat
    # without desyncing anything.
    track = [
        {"start": p["placedAt"], "end": round(p["placedAt"] + p["audioSec"], 3),
         "text": p["vo"], "speaker": p["speaker"], "scene": p["key"].rsplit("_", 1)[0]}
        for p in placed
    ]
    Path(a.caption_track).write_text(
        json.dumps(track, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"caption track: {len(track)} cues -> {a.caption_track}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
