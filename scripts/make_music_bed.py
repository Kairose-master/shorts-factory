#!/usr/bin/env python3
"""Synthesise the episode's music bed from the storyboard.

Why synthesised rather than sourced: the audio manifest specifies one sustained
pad, no melody, no percussion, that can fall to *complete* silence for the
incarnation and the confession and return without a swell. Cutting a found track
to that shape is harder than generating it, the envelope has to line up with
named scenes anyway, and the result is unambiguously ours to publish.

A bed that builds toward the conclusion would tell the viewer the episode
reached one. It does not. So the envelope never rises at the end.

Usage: python3 scripts/make_music_bed.py --storyboard <path> --out <bed.wav>
"""
import argparse
import json
import math
import wave
from pathlib import Path

import numpy as np

RATE = 44100

# Per-scene gain. Silence is authored, not an absence.
SCENE_GAIN = {
    "S01": 0.00,   # room tone only; the cold open has no music
    "S02": 0.55,
    "S03": 0.60,
    "S04": 0.50,
    "S05": 0.40,
    "S05B": 0.30,  # a footnote spoken out loud, not a reveal
    "S06": 0.45,
    "S07": 0.62,   # warmest bed in the episode
    "S08": 0.10,   # near-stop: sub only
    "S09": 0.22,
    "S10": 0.48,
    "S11": 0.00,   # the confession carries no music at all
    "S12": 0.52,
    "S13": 0.30,   # cuts on the door
}

# Two fifths and an octave over a low root — a drone, not a chord progression.
ROOT = 55.0  # A1
PARTIALS = [
    (1.0, 0.50), (2.0, 0.26), (3.0, 0.11),
    (4.0, 0.07), (6.0, 0.04), (8.0, 0.025),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--storyboard", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    sb = json.loads(Path(a.storyboard).read_text(encoding="utf-8"))
    total = sb["durationSec"]
    n = int(total * RATE)
    t = np.arange(n) / RATE

    # The drone. Slight detune per partial so it breathes instead of sitting
    # perfectly still, which is what makes a synth pad sound synthetic.
    sig = np.zeros(n, dtype=np.float64)
    for mult, amp in PARTIALS:
        detune = 1.0 + 0.0007 * math.sin(mult * 1.7)
        lfo = 1.0 + 0.06 * np.sin(2 * np.pi * (0.031 + 0.004 * mult) * t)
        sig += amp * lfo * np.sin(2 * np.pi * ROOT * mult * detune * t)

    # A slow filter sweep, done as a gentle tilt rather than a real filter.
    sig *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.008 * t)

    # Scene envelope, with 1.2s ramps at every boundary so nothing steps.
    env = np.zeros(n, dtype=np.float64)
    for s in sb["scenes"]:
        g = SCENE_GAIN.get(s["id"], 0.4)
        i0, i1 = int(s["startSec"] * RATE), int(s["endSec"] * RATE)
        env[i0:i1] = g
    ramp = int(1.2 * RATE)
    kernel = np.ones(ramp) / ramp
    env = np.convolve(env, kernel, mode="same")

    out = sig * env

    # Head and tail fades: the episode opens on room tone and ends on nothing.
    fade = int(2.0 * RATE)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)

    peak = np.max(np.abs(out)) or 1.0
    out = out / peak * 0.30          # bed sits well under narration
    pcm = (out * 32767).astype("<i2")

    with wave.open(a.out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())

    silent = [k for k, v in SCENE_GAIN.items() if v == 0.0]
    print(f"wrote {a.out}: {total}s @ {RATE}Hz")
    print(f"fully silent scenes: {', '.join(silent)}")


if __name__ == "__main__":
    main()
