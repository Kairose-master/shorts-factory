#!/usr/bin/env python3
"""The Office's standing voice cast, built on Piper + FFmpeg.

Three machine voices that must not sound alike, because the one idea every
Handsel video exists to convey is *who is talking to whom*. If the hirer, the
worker and the grader sound identical, the fact that grading is done by a third
party is invisible on the audio track.

Free and offline: Piper for the reads, FFmpeg for the timbre. No key, no cost.
"""
from __future__ import annotations
import subprocess, tempfile
from pathlib import Path

VOICES = Path(__file__).resolve().parents[3] / "vendor" / "voices"
LESSAC = VOICES / "en_US-lessac-medium.onnx"
ALAN   = VOICES / "en_GB-alan-medium.onnx"
SR     = 22050

# role -> (piper model, piper length_scale, ffmpeg filter chain)
# length_scale > 1 is slower.
CAST = {
    # The only voice allowed to make a claim. Dry, close, mid-pace.
    "NARRATOR": (LESSAC, 1.02, "loudnorm=I=-15:TP=-1.5:LRA=11"),

    # The agent that posts the job. Telephone band + a fast tremolo that reads
    # as a carrier tone. Deliberately synthetic — a near-human agent voice is
    # uncanny; an obviously machine one is legible.
    "AGENT_A": (ALAN, 0.95,
                f"asetrate={SR}*1.06,aresample={SR},atempo=1/1.06,"
                "highpass=f=320,lowpass=f=3200,tremolo=f=72:d=0.30,"
                "loudnorm=I=-16:TP=-1.5:LRA=11"),

    # The agent that claims and delivers. Same family, different register, so
    # the two are separable in one listen.
    "AGENT_B": (LESSAC, 0.92,
                f"asetrate={SR}*0.94,aresample={SR},atempo=1/0.94,"
                "highpass=f=300,lowpass=f=3000,tremolo=f=95:d=0.34,"
                "loudnorm=I=-16:TP=-1.5:LRA=11"),

    # The independent verdict. Slower, lower, colder. Never friendly — warmth
    # would undercut the one thing it represents.
    "GRADER": (ALAN, 1.22,
               f"asetrate={SR}*0.86,aresample={SR},atempo=1/0.86,"
               "lowpass=f=2400,tremolo=f=42:d=0.22,"
               "loudnorm=I=-15:TP=-1.5:LRA=11"),
}


def say(role: str, text: str, out: Path) -> Path:
    """Render one line in one voice."""
    model, length, chain = CAST[role]
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        raw = Path(tf.name)
    subprocess.run(["piper", "-m", str(model), "-f", str(raw),
                    "--length-scale", str(length)],
                   input=text.encode(), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                    "-af", chain, "-ar", str(SR), "-ac", "1", str(out)],
                   check=True)
    raw.unlink(missing_ok=True)
    return out


def duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def build_track(lines, total: float, out: Path, workdir: Path) -> Path:
    """lines: [(start_seconds, role, text)] -> one mixed WAV of length `total`.

    Each line is placed at its exact timecode rather than concatenated, so the
    audio stays locked to the visual beats even when a read comes out short.
    Returns the track and prints any line that overruns its slot.
    """
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    out = Path(out)
    clips = []
    for i, (start, role, text) in enumerate(lines):
        p = say(role, text, workdir / f"line{i:02d}.wav")
        d = duration(p)
        clips.append((start, p, d))
        nxt = lines[i + 1][0] if i + 1 < len(lines) else total
        if start + d > nxt + 0.05:
            print(f"  ! line {i} ({role}) runs {start + d - nxt:.2f}s into the "
                  f"next beat: {text[:48]}...")
    if not clips:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                        "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(total),
                        str(out)], check=True)
        return out

    args, filt = [], []
    for i, (start, p, _d) in enumerate(clips):
        args += ["-i", str(p)]
        filt.append(f"[{i}:a]adelay={int(start*1000)}|{int(start*1000)}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(clips)))
    filt.append(f"{mix}amix=inputs={len(clips)}:normalize=0[mixed]")
    # A final limiter: the mix is sparse, so amix without normalisation is the
    # right call, but two overlapping lines must not clip.
    # apad before -t so the track is padded to the full runtime rather than
    # ending with the last line — otherwise ffmpeg's -shortest truncates the
    # video to the final word and the closing beat is lost.
    filt.append("[mixed]alimiter=limit=0.95,loudnorm=I=-14:TP=-1.0:LRA=11,apad[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args,
                    "-filter_complex", ";".join(filt), "-map", "[out]",
                    "-t", str(total), "-ar", str(SR), "-ac", "2", str(out)],
                   check=True)
    return out


LIB = Path(__file__).resolve().parents[2] / "asset-library" / "sfx"


def mix_sfx(voice_track: Path, cues, total: float, out: Path,
            bed: str = None, bed_db: float = -26.0) -> Path:
    """Lay SFX cues over a finished narration track.

    cues: [(start_seconds, name, gain_db)] where `name` is a file stem in
    office/asset-library/sfx (either the synthesised .wav or a fetched .mp3).

    `bed` lays a music bed under everything for the full runtime, with its own
    fades. It is handled separately from the cues because a bed trimmed by -t
    stops mid-level, and an abrupt cut at the end of a video is audible in a way
    a missing sound effect is not.

    Voice is never ducked here — the cues are chosen to sit in gaps and the
    gains are set well under the read. A limiter catches the occasional overlap.
    """
    out = Path(out)
    args = ["-i", str(voice_track)]
    filt = ["[0:a]aformat=sample_fmts=fltp:sample_rates=%d:channel_layouts=stereo[v]" % SR]
    labels = ["[v]"]
    n = 1
    for start, name, gain in cues:
        src = None
        for ext in (".wav", ".mp3"):
            cand = LIB / f"{name}{ext}"
            if cand.is_file():
                src = cand
                break
        if src is None:
            print(f"  ! sfx not found, skipped: {name}")
            continue
        args += ["-i", str(src)]
        filt.append(
            f"[{n}:a]aformat=sample_fmts=fltp:sample_rates={SR}:channel_layouts=stereo,"
            f"volume={gain}dB,adelay={int(start*1000)}|{int(start*1000)}[s{n}]")
        labels.append(f"[s{n}]")
        n += 1
    if bed:
        src = None
        for ext in (".wav", ".mp3"):
            cand = LIB / f"{bed}{ext}"
            if cand.is_file():
                src = cand
                break
        if src is None:
            print(f"  ! bed not found, skipped: {bed}")
        else:
            args += ["-i", str(src)]
            fade_out = max(total - 2.0, 0.1)
            filt.append(
                f"[{n}:a]aformat=sample_fmts=fltp:sample_rates={SR}:channel_layouts=stereo,"
                f"atrim=0:{total},volume={bed_db}dB,"
                f"afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out:.2f}:d=2.0[bed]")
            labels.append("[bed]")
            n += 1

    if n == 1:
        return voice_track
    filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0[m]")
    filt.append("[m]alimiter=limit=0.95,loudnorm=I=-14:TP=-1.0:LRA=11,apad[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args,
                    "-filter_complex", ";".join(filt), "-map", "[out]",
                    "-t", str(total), "-ar", str(SR), "-ac", "2", str(out)],
                   check=True)
    print(f"  mixed {n-1} layers" + (f" (incl. bed {bed})" if bed else ""))
    return out
