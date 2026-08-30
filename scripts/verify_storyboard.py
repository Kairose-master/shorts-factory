#!/usr/bin/env python3
"""Validate a longform storyboard against the contract in storyboard-director.

Checks, per storyboard:
  * required top-level fields, and durationInFrames == durationSec * fps
  * scenes are contiguous and non-overlapping from 0 to durationSec
  * every scene's beats sum EXACTLY to that scene's duration
  * beats are contiguous, in order, and inside their scene
  * beat durations sit in the 3-14s band (over 14s is an error, under 3s a warn)
  * avatar share sits inside the declared target band
  * every scene names a component, and every beat a known kind

Exit code is non-zero if any ERROR is reported. WARNs do not fail the run.
Usage: python3 scripts/verify_storyboard.py <storyboard.json> [--json]
"""
import json
import sys
from pathlib import Path

KINDS = {
    "visual", "narration", "avatar", "quote", "graphic",
    "ui", "title", "cut", "silence",
}
EPS = 1e-6
MAX_BEAT = 14.0
MIN_BEAT = 3.0


def check(path: Path):
    errors, warnings = [], []
    try:
        sb = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read {path}: {exc}"], [], {}

    for key in ("episodeId", "fps", "durationSec", "durationInFrames", "scenes"):
        if key not in sb:
            errors.append(f"missing top-level field: {key}")
    if errors:
        return errors, warnings, {}

    fps, total = sb["fps"], sb["durationSec"]
    expect = round(total * fps)
    if sb["durationInFrames"] != expect:
        errors.append(
            f"durationInFrames {sb['durationInFrames']} != durationSec*fps ({expect})"
        )

    scenes = sb["scenes"]
    if not scenes:
        errors.append("no scenes")
        return errors, warnings, {}

    avatar = 0.0
    cursor = 0.0
    for s in scenes:
        sid = s.get("id", "<unnamed>")
        if not s.get("component"):
            errors.append(f"{sid}: no component named")

        start, end = s["startSec"], s["endSec"]
        dur = end - start
        if dur <= 0:
            errors.append(f"{sid}: non-positive duration {dur}")
            continue
        if abs(start - cursor) > EPS:
            errors.append(
                f"{sid}: starts at {start} but previous scene ended at {cursor} "
                "(scenes must be contiguous)"
            )
        cursor = end

        av = s.get("avatarSec", 0)
        if av > dur + EPS:
            errors.append(f"{sid}: avatarSec {av} exceeds scene duration {dur}")
        avatar += av

        beats = s.get("beats") or []
        if not beats:
            errors.append(f"{sid}: no beats")
            continue

        bsum = sum(b["dur"] for b in beats)
        if abs(bsum - dur) > 0.01:
            errors.append(
                f"{sid}: beats sum to {bsum:.2f}s but scene is {dur:.2f}s "
                "(they must match exactly)"
            )

        bcur = start
        for i, b in enumerate(beats):
            tag = f"{sid} beat {i} @{b.get('t')}"
            if b.get("kind") not in KINDS:
                errors.append(f"{tag}: unknown kind {b.get('kind')!r}")
            if abs(b["t"] - bcur) > EPS:
                errors.append(
                    f"{tag}: starts at {b['t']} but previous beat ended at {bcur} "
                    "(beats must be contiguous; t is episode-absolute)"
                )
            bcur = b["t"] + b["dur"]
            if b["dur"] > MAX_BEAT + EPS:
                errors.append(
                    f"{tag}: {b['dur']}s exceeds the {MAX_BEAT}s ceiling — split it"
                )
            elif b["dur"] < MIN_BEAT - EPS:
                warnings.append(f"{tag}: {b['dur']}s is under the {MIN_BEAT}s floor")
        if abs(bcur - end) > 0.01:
            errors.append(f"{sid}: beats end at {bcur} but scene ends at {end}")

    if abs(cursor - total) > EPS:
        errors.append(f"scenes end at {cursor} but durationSec is {total}")

    share = avatar / total if total else 0.0
    band = (sb.get("budget") or {}).get("targetBand")
    if band and not (band[0] - 1e-4 <= share <= band[1] + 1e-4):
        errors.append(
            f"avatar share {share:.3f} is outside the target band "
            f"{band[0]}–{band[1]}"
        )

    stats = {
        "scenes": len(scenes),
        "beats": sum(len(s.get("beats") or []) for s in scenes),
        "durationSec": total,
        "avatarSec": avatar,
        "avatarShare": round(share, 4),
    }
    return errors, warnings, stats


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv[1:]
    if not args:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    path = Path(args[0])
    errors, warnings, stats = check(path)

    if as_json:
        print(json.dumps(
            {"ok": not errors, "errors": errors, "warnings": warnings, "stats": stats},
            ensure_ascii=False, indent=2,
        ))
        return 1 if errors else 0

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if stats:
        print(
            f"\n{stats['scenes']} scenes · {stats['beats']} beats · "
            f"{stats['durationSec']}s · avatar {stats['avatarSec']}s "
            f"({stats['avatarShare']:.1%})"
        )
    print("FAIL" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
