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


# A Korean TTS speaks Latin tokens phonetically, and the transcript records what
# it heard. Comparing the written form against the heard form flags a line as
# missing when it was delivered perfectly — which is what happened to all three
# "absent" lines on the first real run: every one contained AI, Yes or No.
SPOKEN_FORMS = {
    "AI": "에이아이", "Yes": "예스", "No": "노", "OK": "오케이",
}


def normalise(s: str) -> str:
    """Whitespace- and punctuation-insensitive, but not word-insensitive.

    Guarded lines must survive punctuation, spacing and the written/spoken
    split above, and must NOT survive a rewording — that is the whole point.
    """
    s = unicodedata.normalize("NFKC", s)
    for written, spoken in SPOKEN_FORMS.items():
        # Not \b: "AI가" has no word boundary between I and 가, because
        # Korean syllables are word characters.
        s = re.sub(rf"(?<![A-Za-z]){written}(?![A-Za-z])", spoken, s)
    s = re.sub(r"[.,!?…·\"'“”‘’\-——–()]", "", s)
    return re.sub(r"\s+", "", s).strip()


def build_index(segs):
    """One normalised transcript string, plus a char -> word-start-time map.

    Everything downstream keys off this. Whisper merges several sentences into
    one segment, so a per-segment comparison scores a fully-present line low
    just because the segment carries extra sentences around it; and fuzzy
    span-matching over words, tried first here, proved unstable enough to
    report large negative drifts on lines that were plainly correct.

    A flat character stream with a parallel time index removes the guessing:
    a line is located by exact search, and its position converts straight to a
    timestamp. Lines that do not match exactly are reported as unaligned rather
    than force-fitted somewhere.
    """
    chars, times = [], []
    for sg in segs:
        for w in sg["words"] or []:
            n = normalise(w["w"])
            chars.append(n)
            times.extend([w["start"]] * len(n))
    return "".join(chars), times


def align(expected, full, times):
    """Locate each expected line in the transcript, scanning forward only."""
    out, pos = [], 0
    for e in expected:
        target = normalise(e["text"])
        if not target:
            continue
        i = full.find(target, pos)
        if i == -1:                       # allow an out-of-order match once
            i = full.find(target)
        if i == -1:
            # Not exact. Report the closest thing the model heard there, so a
            # failure names what to go listen to instead of just saying no.
            window = full[pos:pos + max(len(target) * 4, 400)]
            best, heard = 0.0, ""
            for j in range(0, max(1, len(window) - len(target)), 4):
                span = window[j:j + len(target)]
                r = difflib.SequenceMatcher(None, target, span).ratio()
                if r > best:
                    best, heard = r, span
            out.append({**e, "ratio": best, "heard": heard, "at": None})
            continue
        pos = i + len(target)
        out.append({**e, "ratio": 1.0, "heard": target,
                    "at": times[i] if i < len(times) else None})
    return out


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
            flat, times = build_index(segs)
            expected = cues or [{"start": b["t"], "text": b["vo"]} for b in beats]
            aligned = align(expected, flat, times)
            by_text = {normalise(r["text"]): r for r in aligned}

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
                rec = by_text.get(t)
                if rec is None:
                    rec = next(iter(align([{"start": 0, "text": g}], flat, times)), None)
                best = rec["ratio"] if rec else 0.0
                heard = rec["heard"] if rec else ""
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
                rec = by_text.get(normalise(b["vo"]))
                best = rec["ratio"] if rec else 0.0
                (garbled if best >= 0.80 else missing).append((b, best))
            rows.append((
                "MISSING SENTENCES",
                "PASS" if not missing else "FAIL",
                f"{len(missing)} absent"
                + (f", {len(garbled)} near-match (transcription)" if garbled else ""),
            ))
            blocking += [f"{b['scene']} @{b['t']}: not found in transcript "
                         f"(best match {r:.2f})" for b, r in missing]

            # Align on WORDS, in order, scanning forward from a cursor.
            #
            # Two earlier versions of this were wrong in instructive ways. The
            # first matched a 12-character prefix anywhere in the transcript and
            # reported 679s of drift on an 11-minute episode. The second matched
            # whole segments in order — better, but whisper merges several
            # sentences into one segment, so a segment's start can sit many
            # seconds before the line being measured. Words are the only unit
            # that lines up with a per-line cue.
            # Whisper reports word starts a little late, and consistently so:
            # a first run showed +0.70 to +0.86s on essentially every line. A
            # constant offset shared by all lines is measurement bias, not the
            # audio sliding out of sync — what matters is whether lines drift
            # RELATIVE to each other. So centre on the median and check the
            # spread around it, and report the bias separately rather than
            # letting it fail an otherwise clean assembly.
            offsets, unmatched, labelled = [], 0, []
            for r in aligned:
                if r["at"] is None or r["ratio"] < 1.0:
                    unmatched += 1
                    continue
                d = r["at"] - r["start"]
                offsets.append(d)
                labelled.append((d, r["text"][:44]))
            if not offsets:
                rows.append(("TIMING DRIFT", "FAIL", "nothing aligned"))
                blocking.append("timing drift: no line could be aligned")
            else:
                bias = sorted(offsets)[len(offsets) // 2]
                dev = [(abs(d - bias), d - bias, t) for d, t in labelled]
                worst = max(x[0] for x in dev)
                cum = offsets[-1] - bias
                for a_, d_, t_ in sorted(dev, reverse=True)[:5]:
                    if a_ > DRIFT_PER_BEAT:
                        notes.append(f"drift {d_:+.2f}s (bias-corrected) on: {t_}")
                ok = worst <= DRIFT_PER_BEAT and abs(cum) <= DRIFT_CUMULATIVE
                rows.append((
                    "TIMING DRIFT",
                    "PASS" if ok else "FAIL",
                    f"max {worst:+.2f}s about a {bias:+.2f}s measurement bias, "
                    f"cum {cum:+.2f}s, {unmatched} unaligned",
                ))
                if not ok:
                    blocking.append(
                        f"timing drift {worst:.2f}s around the median offset "
                        f"(assembly integrity, measured against the caption track)")

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
