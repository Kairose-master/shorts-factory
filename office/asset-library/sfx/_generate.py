#!/usr/bin/env python3
"""Synthesise the Office's core UI sound pack. No key, no network, no licence.

Why this exists: the CC0 path (sfx-mcp -> Freesound) is blocked on
FREESOUND_API_KEY, and most of what a Handsel short needs is not "a sound
somebody recorded" — it is a 40ms tick, a counter blip, an error buzz. Those are
cheaper to synthesise than to search for, and a sound we generated is
licence-clean by construction, which is a stronger position than CC0.

Freesound stays the right source for texture that cannot be synthesised —
room tone with character, real mechanical noise, anything with a performance in
it. This pack is the deterministic half, not a replacement.

Every sound is a pure function of its parameters, so the pack is reproducible:
delete the directory, re-run, get byte-identical files.

Usage: python3 office/asset-library/sfx/_generate.py
"""
from __future__ import annotations
import json, hashlib, wave
from pathlib import Path
import numpy as np

SR = 48_000
HERE = Path(__file__).resolve().parent
RNG_SEED = 20260827          # fixed: the noise must be reproducible


def _env(n, attack=0.002, decay=0.06, curve=3.0):
    """Percussive envelope. Attack removes the click that a raw start makes."""
    a = int(SR * attack)
    d = max(n - a, 1)
    return np.concatenate([
        np.linspace(0, 1, a) ** 0.5,
        (np.linspace(1, 0, d) ** curve),
    ])[:n]


def _sine(f, n, phase=0.0):
    return np.sin(2 * np.pi * f * np.arange(n) / SR + phase)


def _noise(n, rng):
    return rng.standard_normal(n)


def _lowpass(x, cutoff):
    """One-pole lowpass. Crude on purpose — it is a UI blip, not a mixdown."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = a * acc + (1 - a) * v
        y[i] = acc
    return y


def _sweep_lowpass(x, f0, f1):
    """Lowpass whose cutoff glides f0 -> f1 with the filter state carried across.

    Doing this blockwise resets the state every block, which averages out into a
    swell rather than a sweep. One continuous pass is the correct construction,
    though at 0.38s the audible and spectral difference is modest — checked
    against a before/after spectrogram, not assumed.
    """
    n = len(x)
    cutoff = np.geomspace(f0, f1, n)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty(n)
    acc = 0.0
    for i in range(n):
        acc = a[i] * acc + (1 - a[i]) * x[i]
        y[i] = acc
    return y


def _highpass(x, cutoff):
    return x - _lowpass(x, cutoff)


def _norm(x, peak=0.89):
    m = np.max(np.abs(x))
    return x * (peak / m) if m > 0 else x


def _fade_edges(x, ms=3):
    """No sound ends on a discontinuity; a hard cut is an audible click."""
    n = int(SR * ms / 1000)
    if len(x) > 2 * n:
        x[:n] *= np.linspace(0, 1, n)
        x[-n:] *= np.linspace(1, 0, n)
    return x


def write(name: str, x: np.ndarray, note: str, catalogue: list):
    x = _fade_edges(_norm(np.asarray(x, dtype=np.float64)))
    pcm = (x * 32767).astype("<i2")
    path = HERE / f"{name}.wav"
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    catalogue.append({
        "asset_id": f"sfx-{name}",
        "type": "sfx",
        "local_path": f"office/asset-library/sfx/{name}.wav",
        "source": "synthesised",
        "source_url": None,
        "creator": "Handsel Growth Office",
        "license": "proprietary-owned",
        "attribution": None,
        "commercial_use": True,
        "duration": round(len(x) / SR, 3),
        "reason_selected": note,
        "content_hash": "sha256:" + hashlib.sha256(pcm.tobytes()).hexdigest()[:32],
        "used_in": [],
    })
    print(f"  {name:22} {len(x)/SR:5.3f}s  {note}")


def build():
    rng = np.random.default_rng(RNG_SEED)
    cat: list = []

    # --- click: the counter tick. Short, dry, no pitch of its own.
    n = int(SR * 0.045)
    click = _highpass(_noise(n, rng), 1400) * _env(n, 0.0008, 0.045, 5.0)
    write("click", click, "counter tick, UI step", cat)

    # --- tick: softer sibling for rapid sequences, so repeats don't fatigue.
    n = int(SR * 0.035)
    tick = (_sine(2200, n) * 0.6 + _highpass(_noise(n, rng), 2000) * 0.4) * _env(n, 0.0006, 0.035, 6.0)
    write("tick", tick, "fast counter, used in runs", cat)

    # --- payment: a coin-ish two-partial pluck. Money arriving.
    n = int(SR * 0.30)
    pay = (_sine(1180, n) + 0.7 * _sine(1770, n) + 0.35 * _sine(2640, n)) * _env(n, 0.001, 0.30, 3.2)
    write("payment", pay, "money moves, escrow release", cat)

    # --- cash: heavier, lower, for a treasury change rather than one payment.
    n = int(SR * 0.42)
    cash = (_sine(720, n) + 0.6 * _sine(1090, n) + 0.3 * _sine(1460, n)) * _env(n, 0.0015, 0.42, 2.6)
    write("cash", cash, "treasury change, larger sum", cat)

    # --- success: rising major third. Resolved, not triumphant.
    n = int(SR * 0.34)
    t = np.arange(n) / SR
    f = 660 + (880 - 660) * np.clip(t / 0.16, 0, 1)
    success = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.004, 0.34, 2.2)
    write("success", success, "PASS, verified, settled", cat)

    # --- failure: falling, slightly detuned. Flat, never comic.
    n = int(SR * 0.40)
    t = np.arange(n) / SR
    f = 420 - 160 * np.clip(t / 0.30, 0, 1)
    failure = (np.sin(2 * np.pi * np.cumsum(f) / SR)
               + 0.45 * np.sin(2 * np.pi * np.cumsum(f * 1.012) / SR)) * _env(n, 0.003, 0.40, 2.0)
    write("failure", failure, "FAILED verdict — deliberately unfunny", cat)

    # --- warning: two clipped beeps. For REVISE / INCONCLUSIVE, not failure.
    n1 = int(SR * 0.075)
    beep = np.clip(_sine(900, n1) * 1.6, -1, 1) * _env(n1, 0.002, 0.075, 2.0)
    gap = np.zeros(int(SR * 0.055))
    write("warning", np.concatenate([beep, gap, beep]), "REVISE / INCONCLUSIVE", cat)

    # --- notification: soft two-tone. A card appearing.
    n1 = int(SR * 0.13)
    a = _sine(1046, n1) * _env(n1, 0.003, 0.13, 2.4)
    b = _sine(1568, n1) * _env(n1, 0.003, 0.13, 2.4)
    write("notification", np.concatenate([a, b * 0.85]), "card appears, agent activates", cat)

    # --- impact: low thud for a hard cut or a stamp landing.
    n = int(SR * 0.26)
    t = np.arange(n) / SR
    f = 150 * np.exp(-t * 12) + 45
    impact = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.001, 0.26, 2.8)
    impact += _lowpass(_noise(n, rng), 220) * _env(n, 0.001, 0.10, 5.0) * 0.5
    write("impact", impact, "stamp lands, hard cut", cat)

    # --- whoosh: a real sweep. Cutoff glides 300 -> 7000 Hz in one continuous
    # pass, so the brightness genuinely travels instead of just swelling.
    n = int(SR * 0.38)
    out = _sweep_lowpass(_noise(n, rng), 300, 7000)
    out = _highpass(out, 200)
    env = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    write("whoosh", out * env, "movement between states; sweep is subtle at 0.38s — reads mostly as a swell", cat)

    # --- transition: whoosh with a pitched tail, for a scene change.
    n = int(SR * 0.45)
    tr = np.concatenate([out[: int(SR * 0.30)], np.zeros(n - int(SR * 0.30))])
    tail = _sine(520, n) * np.concatenate([np.zeros(int(SR * 0.26)), _env(n - int(SR * 0.26), 0.004, 0.19, 2.5)])
    write("transition", tr * 0.9 + tail * 0.5, "scene change", cat)

    # --- typing: six irregular clicks. Irregular or it reads as a machine gun.
    parts = []
    for i in range(6):
        m = int(SR * 0.030)
        k = _highpass(_noise(m, rng), 1800) * _env(m, 0.0005, 0.030, 6.0)
        parts.append(k * (0.75 + 0.25 * rng.random()))
        parts.append(np.zeros(int(SR * (0.055 + 0.035 * rng.random()))))
    write("typing", np.concatenate(parts), "prompt being typed", cat)

    # --- digital: bit-crushed blips. Machine speech without words.
    n = int(SR * 0.22)
    d = _sine(1400, n) * _env(n, 0.001, 0.22, 3.0)
    d = np.round(d * 6) / 6                      # crude quantisation = grit
    write("digital", d, "agent thinking, machine event", cat)

    # --- office-ambience: 6s loopable pink-ish bed. Sits far under everything.
    n = int(SR * 6.0)
    amb = _lowpass(_noise(n, rng), 900) + 0.4 * _lowpass(_noise(n, rng), 220)
    x = int(SR * 0.35)                           # equal-power crossfade to loop
    head, tail = amb[:x].copy(), amb[-x:].copy()
    f = np.linspace(0, 1, x)
    amb[:x] = head * np.sqrt(f) + tail * np.sqrt(1 - f)
    amb = amb[: n - x]
    write("office-ambience", amb * 0.30, "loopable bed, -30dB under VO", cat)

    (HERE / "sfx-manifest.json").write_text(
        json.dumps({"assets": cat,
                    "note": "Synthesised by _generate.py. Reproducible from seed "
                            f"{RNG_SEED}. Owned outright — no attribution required, "
                            "no third-party licence."}, indent=2) + "\n")
    print(f"\n{len(cat)} sounds -> {HERE}")


if __name__ == "__main__":
    build()
