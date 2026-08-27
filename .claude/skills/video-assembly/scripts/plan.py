#!/usr/bin/env python3
"""Turn measured narration into the render plan.

Takes ``timing.json`` from ``narrate.py`` and pads, and writes ``plan.json``:
the scene start/duration table that the renderer draws against and that
``qc.py`` later checks the finished file against. One file, one truth.

    python3 plan.py --timing project/vo/timing.json --out project/plan.json \
        --lead 0.25 --gap 0.18 --tail 0.6

Per-scene overrides live in the lines file and are carried through here:
``{"id": "s3", "extra": 1.2}`` buys a scene 1.2s of silence after its narration
(for a beat that needs to land), and ``{"id": "s3", "gap": 0.0}`` removes the
gap after it (for a hard cut into the next line).

Each scene also carries the TTS word boundaries, so a renderer can place a
reveal on the word it belongs to:

    def word_at(scene, needle):
        for w in scene["words"]:
            if w["text"].strip(".,'").lower() == needle:
                return w["t"]
"""
import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timing", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lines", help="optional lines.json carrying per-scene extra/gap")
    ap.add_argument("--lead", type=float, default=0.25, help="silence before the first word")
    ap.add_argument("--gap", type=float, default=0.18, help="default silence between scenes")
    ap.add_argument("--tail", type=float, default=0.6, help="silence after the last word")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    args = ap.parse_args()

    timing = json.loads(Path(args.timing).read_text(encoding="utf-8"))
    over = {}
    if args.lines:
        over = {i["id"]: i for i in json.loads(Path(args.lines).read_text(encoding="utf-8"))}

    scenes, cur = [], args.lead
    for k, t in enumerate(timing):
        o = over.get(t["id"], {})
        extra = float(o.get("extra", 0.0))
        gap = args.gap if k < len(timing) - 1 else 0.0
        gap = float(o.get("gap", gap))
        dur = t["seconds"] + extra + gap
        scenes.append({
            "id": t["id"], "start": round(cur, 3), "dur": round(dur, 3),
            "vo": t["wav"], "vo_seconds": t["seconds"], "text": t["text"],
            "words": t.get("words_timed", []),
        })
        cur += dur

    total = round(cur + args.tail, 3)
    plan = {"fps": args.fps, "width": args.width, "height": args.height,
            "lead": args.lead, "tail": args.tail, "duration": total, "scenes": scenes}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(plan, indent=2, ensure_ascii=False))

    for s in scenes:
        print(f"  {s['id']:>4}  {s['start']:6.2f} → {s['start'] + s['dur']:6.2f}  ({s['dur']:5.2f}s)")
    print(f"\n  total {total:.2f}s   wrote {args.out}")
    if total > 60:
        print("  WARN: over 60s — not a Short on YouTube, and past the Reels sweet spot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
