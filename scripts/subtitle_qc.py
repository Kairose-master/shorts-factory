#!/usr/bin/env python3
"""Transcribe final narration and diff it against the canonical script.

The last place a red-team required fix can silently disappear. A fix agreed in
the script is worth nothing if the narrator paraphrased it, so guarded lines are
compared verbatim and a near-match fails.

Checks:
  * guarded lines present verbatim          (blocking)
  * every script sentence present            (blocking)
  * per-beat and cumulative timing drift     (blocking over threshold)
  * distinct voice where the script stages two speakers  (reported; needs --voices)
  * low-confidence tokens on domain terms    (advisory)

Emits final.srt and qc-report.md. Exit code is non-zero when a blocking check
fails, so a render pipeline can gate on it.

Usage:
  python3 scripts/subtitle_qc.py --audio A.wav --script canonical.md \
      --storyboard storyboard.json --out subtitles/ [--model large-v3]

Requires faster-whisper (`pip install faster-whisper`). Without it the script
still writes an SRT skeleton from the storyboard and reports SKIPPED rather
than passing — an unrun check is never a pass.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

DRIFT_PER_BEAT = 0.6
DRIFT_CUMULATIVE = 1.5
DOMAIN_TERMS = ["성육신", "세례", "신앙고백", "유아", "귀속", "고유성"]

MAX_CUE_CHARS = 26
MIN_CUE_SEC = 1.0
MAX_CUE_SEC = 6.0
CUE_GAP_SEC = 0.08


def normalise(s: str) -> str:
    """Whitespace- and punctuation-insensitive, but not word-insensitive.

    Guarded lines must survive punctuation and spacing changes from TTS, and
    must NOT survive a rewording — that is the whole point of the check.
    """
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[.,!?…·\"'“”‘’\-——–()]", "", s)
    return re.sub(r"\s+", "", s).strip()


def load_storyboard(path: Path):
    sb = json.loads(path.read_text(encoding="utf-8"))
    beats = []
    for scene in sb["scenes"]:
        for b in scene["beats"]:
            if b.get("vo"):
                beats.append({
                    "scene": scene["id"],
                    "t": b["t"],
                    "dur": b["dur"],
                    "vo": b["vo"],
                    "speaker": b.get("speaker", "narrator"),
                    "guard": b.get("guard"),
                })
    return sb, beats


GUARD_RE = re.compile(r"\*\*\[GUARD\]\*\*(.*?)(?:\n\n|\Z)", re.S)


def script_guards(script_path: Path):
    """Lines the canonical script marks as uncuttable, plus storyboard guards."""
    text = script_path.read_text(encoding="utf-8")
    out = []
    for m in GUARD_RE.finditer(text):
        chunk = m.group(1)
        for q in re.findall(r"[\"“](.+?)[\"”]", chunk):
            out.append(q.strip())
    return out


def transcribe(audio: Path, model_name: str):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None, "faster-whisper not installed"
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(
        str(audio), language="ko", word_timestamps=True, vad_filter=True
    )
    segs = []
    for s in segments:
        segs.append({
            "start": s.start,
            "end": s.end,
            "text": s.text.strip(),
            "words": [
                {"w": w.word, "start": w.start, "end": w.end, "p": w.probability}
                for w in (s.words or [])
            ],
        })
    return segs, None


def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrap(text: str, limit: int = MAX_CUE_CHARS):
    if len(text) <= limit:
        return [text]
    words = text.split(" ")
    if len(words) == 1:
        return [text]
    best, best_delta = 1, float("inf")
    for i in range(1, len(words)):
        a = len(" ".join(words[:i]))
        b = len(" ".join(words[i:]))
        delta = abs(a - b) + max(0, max(a, b) - limit) * 3
        if delta < best_delta:
            best_delta, best = delta, i
    return [" ".join(words[:best]), " ".join(words[best:])]


def write_srt(beats, out: Path):
    lines = []
    for i, b in enumerate(beats, 1):
        start = b["t"]
        end = min(b["t"] + b["dur"], b["t"] + MAX_CUE_SEC)
        end = max(end, start + MIN_CUE_SEC) - CUE_GAP_SEC
        lines.append(str(i))
        lines.append(f"{ts(start)} --> {ts(end)}")
        lines.extend(wrap(b["vo"]))
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio")
    ap.add_argument("--script", required=True)
    ap.add_argument("--storyboard", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="large-v3")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    sb, beats = load_storyboard(Path(a.storyboard))
    guards = script_guards(Path(a.script)) + [
        b["vo"] for b in beats if b.get("guard")
    ]

    write_srt(beats, out / "final.srt")

    rows, blocking = [], []

    if not a.audio or not Path(a.audio).exists():
        rows.append(("TRANSCRIPT", "SKIPPED", "no narration audio yet"))
        rows.append(("GUARDED LINES", "SKIPPED", f"{len(guards)} to verify"))
        rows.append(("MISSING SENTENCES", "SKIPPED", ""))
        rows.append(("TIMING DRIFT", "SKIPPED", ""))
        verdict = "SUBTITLE_SKIPPED"
        note = (
            "Narration has not been generated, so nothing was verified. This is "
            "not a pass: an unrun check never counts as a passing one. Re-run "
            "once audio/narration.wav exists."
        )
    else:
        segs, err = transcribe(Path(a.audio), a.model)
        if segs is None:
            rows.append(("TRANSCRIPT", "FAIL", err))
            blocking.append(err)
            verdict = "SUBTITLE_FAIL"
            note = "Install faster-whisper and re-run."
        else:
            full = normalise(" ".join(s["text"] for s in segs))

            missing_guards = [g for g in guards if normalise(g) not in full]
            rows.append((
                "GUARDED LINES",
                "PASS" if not missing_guards else "FAIL",
                f"{len(guards) - len(missing_guards)}/{len(guards)} verbatim",
            ))
            if missing_guards:
                blocking += [f"guarded line not verbatim: {g}" for g in missing_guards]

            missing = [b for b in beats if normalise(b["vo"]) not in full]
            rows.append((
                "MISSING SENTENCES",
                "PASS" if not missing else "FAIL",
                str(len(missing)),
            ))
            if missing:
                blocking += [
                    f"{b['scene']} @{b['t']}: not found in transcript" for b in missing
                ]

            # Align each beat to the transcript segment that best contains it.
            worst, cum = 0.0, 0.0
            for b in beats:
                hit = next(
                    (s for s in segs if normalise(b["vo"])[:12] in normalise(s["text"])),
                    None,
                )
                if hit:
                    d = hit["start"] - b["t"]
                    cum = d
                    worst = max(worst, abs(d))
            ok = worst <= DRIFT_PER_BEAT and abs(cum) <= DRIFT_CUMULATIVE
            rows.append((
                "TIMING DRIFT",
                "PASS" if ok else "FAIL",
                f"max {worst:+.2f}s, cum {cum:+.2f}s",
            ))
            if not ok:
                blocking.append(f"timing drift max {worst:.2f}s cum {cum:.2f}s")

            flagged = [
                w["w"]
                for s in segs
                for w in s["words"]
                if w["p"] < 0.6 and any(t in w["w"] for t in DOMAIN_TERMS)
            ]
            rows.append((
                "PRONUNCIATION",
                "REVIEW" if flagged else "PASS",
                ", ".join(flagged[:8]) or "clean",
            ))

            speakers = {b["speaker"] for b in beats}
            rows.append((
                "SPEAKER SEPARATION",
                "REVIEW" if len(speakers) > 1 else "PASS",
                f"{len(speakers)} speaker(s) in script — verify by ear",
            ))

            verdict = "SUBTITLE_FAIL" if blocking else "SUBTITLE_PASS"
            note = ""

    report = ["# subtitle-qc", "", f"episode: `{sb['episodeId']}`", ""]
    width = max(len(r[0]) for r in rows)
    report.append("```")
    for name, status, detail in rows:
        report.append(f"{name:<{width}}  {status:<8} {detail}")
    report.append(f"{'VERDICT':<{width}}  {verdict}")
    report.append("```")
    if note:
        report += ["", note]
    if blocking:
        report += ["", "## Blocking", ""] + [f"- {b}" for b in blocking]
    (out / "qc-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n".join(report))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
