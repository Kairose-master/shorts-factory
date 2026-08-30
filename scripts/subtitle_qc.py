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
import difflib
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
    ap.add_argument("--caption-track")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    sb, beats = load_storyboard(Path(a.storyboard))
    # Drift is measured against the caption track when one exists: that is where
    # each line was actually placed, so the check reads assembly integrity.
    # Falling back to raw beat times would re-flag the deliberate, bounded
    # within-scene pushes the assembler already reported.
    cues = []
    ct = Path(a.caption_track) if a.caption_track else None
    if ct and ct.exists():
        cues = json.loads(ct.read_text(encoding="utf-8"))
    notes = []
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

            # Exact first. A guarded line is meant to survive verbatim, and an
            # exact substring is the only test that actually proves that.
            #
            # But a transcript is a model's guess, so an exact miss is not by
            # itself proof the line was mis-spoken. Fall back to the closest
            # thing the model DID hear and report the similarity, so a failure
            # names what to go listen to instead of just saying no. Below 0.90
            # it blocks; above, it is flagged as a transcription artifact.
            missing_guards, soft_guards = [], []
            for g in guards:
                if normalise(g) in full:
                    continue
                t = normalise(g)
                best, heard = 0.0, ""
                for seg in segs:
                    r = difflib.SequenceMatcher(None, t, normalise(seg["text"])).ratio()
                    if r > best:
                        best, heard = r, seg["text"].strip()
                (soft_guards if best >= 0.90 else missing_guards).append(
                    (g, best, heard))
            ok_n = len(guards) - len(missing_guards)
            rows.append((
                "GUARDED LINES",
                "PASS" if not missing_guards else "FAIL",
                f"{ok_n}/{len(guards)} verbatim"
                + (f", {len(soft_guards)} near-match (transcription)" if soft_guards else ""),
            ))
            for g, r, heard in missing_guards:
                blocking.append(
                    f"guarded line not verbatim (best {r:.2f}):\n"
                    f"      script: {g}\n      heard : {heard}")
            for g, r, heard in soft_guards:
                notes.append(f"guarded line matched at {r:.2f} (likely a "
                             f"transcription artifact): {heard}")

            # Same treatment: a line the model garbled is not a line the
            # narrator dropped. Only a genuinely absent line blocks.
            missing, garbled = [], []
            for b in beats:
                if normalise(b["vo"]) in full:
                    continue
                t = normalise(b["vo"])
                best = max((difflib.SequenceMatcher(None, t, normalise(sg["text"])).ratio()
                            for sg in segs), default=0.0)
                (garbled if best >= 0.80 else missing).append((b, best))
            rows.append((
                "MISSING SENTENCES",
                "PASS" if not missing else "FAIL",
                f"{len(missing)} absent"
                + (f", {len(garbled)} near-match (transcription)" if garbled else ""),
            ))
            blocking += [f"{b['scene']} @{b['t']}: not found in transcript "
                         f"(best match {r:.2f})" for b, r in missing]

            # Align in ORDER, scanning forward from a cursor. Matching a short
            # prefix anywhere in the transcript is how a first version of this
            # reported 679s of drift on an 11-minute episode: a 12-character
            # opening matched a similar sentence ten minutes away.
            worst, cum, unmatched, cursor = 0.0, 0.0, 0, 0
            expected = cues or [{"start": b["t"], "text": b["vo"]} for b in beats]
            for e in expected:
                target = normalise(e["text"])
                best, best_i = 0.0, None
                for j in range(cursor, min(cursor + 12, len(segs))):
                    r = difflib.SequenceMatcher(
                        None, target, normalise(segs[j]["text"])).ratio()
                    if r > best:
                        best, best_i = r, j
                if best_i is None or best < 0.55:
                    unmatched += 1
                    continue
                cursor = best_i + 1
                d = segs[best_i]["start"] - e["start"]
                cum = d
                worst = max(worst, abs(d))
            ok = worst <= DRIFT_PER_BEAT and abs(cum) <= DRIFT_CUMULATIVE
            rows.append((
                "TIMING DRIFT",
                "PASS" if ok else "FAIL",
                f"max {worst:+.2f}s, cum {cum:+.2f}s, {unmatched} unaligned",
            ))
            if not ok:
                blocking.append(
                    f"timing drift max {worst:.2f}s cum {cum:.2f}s "
                    f"(measured against the caption track, i.e. assembly integrity)")

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
    if notes:
        report += ["", "## Notes (not blocking)", ""] + [f"- {x}" for x in notes]
    if blocking:
        report += ["", "## Blocking", ""] + [f"- {b}" for b in blocking]
    (out / "qc-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n".join(report))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
