#!/usr/bin/env python3
"""longform2shorts — 롱폼에서 말 밀도 최대의 숏폼을 자동으로 잘라내는 도구.

파이프라인:
  1. ffmpeg  : 오디오 추출 (16k mono)
  2. whisper : 단어 타임스탬프 전사 (faster-whisper, 로컬·무API)
  3. 무음 제거: 발화 블록 사이 갭 > --max-gap 을 점프컷 → "말이 끊기지 않는" 편집
  4. 하이라이트 스코어링: 숫자·질문·훅 어휘·발화 밀도 가중
  5. 창 선택 : 발화시간 기준 --target 초의 비중복 상위 N개
  6. 렌더    : 세로 1080x1920 (블러 확장 배경 — 9채널 썸네일 실측 관행),
              구간별 자막 PNG 오버레이(원어 verbatim), 점프컷 concat, loudnorm -14

사용:
  python3 tools/longform2shorts/l2s.py --input long.mp4 --outdir out/ \
      [--clips 2] [--target 30] [--max-gap 0.4] [--model small]

출처 표기: 자막은 전사 원문 그대로(verbatim). 지어내는 문장 없음.
"""
import argparse, json, os, subprocess, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

EXE = imageio_ffmpeg.get_ffmpeg_exe()
FONT_BOLD = os.path.join(os.path.dirname(__file__), "..", "..",
                         "projects", "malgap-ep1", "NotoSansKR-Bold.ttf")

HOOK_WORDS = ["돈", "원", "달러", "$", "%", "비밀", "처음", "마지막", "진짜", "충격",
              "money", "dollar", "usdc", "pay", "paid", "escrow", "free", "first",
              "never", "real", "live", "actually", "secret", "why", "how"]

def run(cmd): subprocess.run(cmd, check=True)

def transcribe(inp, workdir, model_size):
    wav = f"{workdir}/audio16k.wav"
    run([EXE, "-y", "-loglevel", "error", "-i", inp, "-ar", "16000", "-ac", "1", wav])
    from faster_whisper import WhisperModel
    m = WhisperModel(model_size, device="cpu", compute_type="int8")
    segs, info = m.transcribe(wav, word_timestamps=True, vad_filter=True)
    words = []
    for s in segs:
        for w in (s.words or []):
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
    print(f"  lang={info.language} p={info.language_probability:.2f} words={len(words)}")
    return words, info.language

def speech_blocks(words, max_gap):
    """단어들을 갭<=max_gap 로 이어붙인 발화 블록. 갭은 전부 점프컷 대상."""
    blocks = []
    cur = None
    for w in words:
        if cur and w["s"] - cur["e"] <= max_gap:
            cur["e"] = w["e"]; cur["words"].append(w)
        else:
            if cur: blocks.append(cur)
            cur = {"s": w["s"], "e": w["e"], "words": [w]}
    if cur: blocks.append(cur)
    for b in blocks:
        b["text"] = "".join((" " if i and not b["words"][i]["w"].startswith("'") else "") + x["w"]
                            for i, x in enumerate(b["words"])).strip()
        b["dur"] = b["e"] - b["s"]
    return [b for b in blocks if b["dur"] >= 0.25]

def score_block(b):
    t = b["text"].lower()
    sc = len(b["words"]) / max(b["dur"], 0.3)                # 발화 밀도(말 많음) 최우선
    sc += 2.2 * sum(t.count(k) for k in HOOK_WORDS)
    sc += 2.5 * sum(c.isdigit() for c in t) / max(len(t), 1) * 10
    sc += 1.6 * t.count("?")
    return sc

def pick_windows(blocks, target, n_clips):
    """연속 블록 슬라이스 중 발화합≈target 를 만들고 점수순·비중복 상위 n개."""
    cands = []
    for i in range(len(blocks)):
        talk, j = 0.0, i
        while j < len(blocks) and talk < target:
            talk += blocks[j]["dur"]; j += 1
        if talk < target * 0.6: break
        win = blocks[i:j]
        cands.append({"i": i, "j": j, "talk": talk,
                      "score": sum(score_block(b) * b["dur"] for b in win) / talk,
                      "s": win[0]["s"], "e": win[-1]["e"]})
    cands.sort(key=lambda c: -c["score"])
    picked = []
    for c in cands:
        if all(c["j"] <= p["i"] or c["i"] >= p["j"] for p in picked):
            picked.append(c)
        if len(picked) == n_clips: break
    return sorted(picked, key=lambda c: c["s"])

def caption_png(text, path, width=1080):
    """당몰이/제로비 실측 스타일: 흰 고딕 + 먹 스트로크, 최대 2줄."""
    f = ImageFont.truetype(FONT_BOLD, 58)
    words, lines, cur = text.split(), [], ""
    tmp = Image.new("RGB", (10, 10)); td = ImageDraw.Draw(tmp)
    for w in words:
        t = (cur + " " + w).strip()
        if td.textbbox((0, 0), t, font=f)[2] > width - 160 and cur:
            lines.append(cur); cur = w
        else: cur = t
    lines.append(cur); lines = lines[-2:]
    H = len(lines) * 78 + 30
    im = Image.new("RGBA", (width, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, ln in enumerate(lines):
        d.text((width/2, 8 + k*78), ln, font=f, fill=(242, 233, 220),
               stroke_width=7, stroke_fill=(20, 17, 15), anchor="ma")
    im.save(path)
    return H

def render_clip(inp, win, blocks, outp, workdir, idx):
    """점프컷 concat + 세로 블러패드 + 자막 오버레이 + loudnorm."""
    segs = blocks[win["i"]:win["j"]]
    # --- 1) 점프컷: 발화 블록만 이어붙인 중간본
    parts, fc = [], []
    for k, b in enumerate(segs):
        fc.append(f"[0:v]trim=start={b['s']:.3f}:end={b['e']:.3f},setpts=PTS-STARTPTS[v{k}];"
                  f"[0:a]atrim=start={b['s']:.3f}:end={b['e']:.3f},asetpts=PTS-STARTPTS[a{k}];")
        parts.append(f"[v{k}][a{k}]")
    fc.append("".join(parts) + f"concat=n={len(segs)}:v=1:a=1[vc][ac];")
    # --- 2) 세로 변환: 블러 배경 + 원본 중앙 (9채널 실측 관행)
    fc.append("[vc]split[v1][v2];"
              "[v1]scale=1080:1920:force_original_aspect_ratio=increase,"
              "crop=1080:1920,boxblur=22:2[bg];"
              "[v2]scale=1080:-2[fg];"
              "[bg][fg]overlay=(W-w)/2:(H-h)/2[base];")
    # --- 3) 자막: 블록별 PNG, 점프컷 이후의 새 타임라인에 매핑
    t, ov_in, layer = 0.0, [], "base"
    for k, b in enumerate(segs):
        png = f"{workdir}/cap_{idx}_{k}.png"
        caption_png(b["text"], png)
        ov_in.append(png)
        nxt = f"cap{k}"
        fc.append(f"[{layer}][{len(ov_in)}:v]overlay=0:1520:"
                  f"enable='between(t,{t:.3f},{t + b['dur']:.3f})'[{nxt}];")
        layer = nxt; t += b["dur"]
    graph = "".join(fc)[:-1].rsplit(f"[{layer}]", 1)[0] + f"[{layer}]"
    cmd = [EXE, "-y", "-loglevel", "error", "-i", inp]
    for p in ov_in: cmd += ["-i", p]
    cmd += ["-filter_complex", graph, "-map", f"[{layer}]", "-map", "[ac]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
            "-af_", "anull"]
    cmd.remove("-af_"); cmd.remove("anull")
    cmd += ["-c:a", "aac", "-ar", "48000", "-b:a", "160k", "-movflags", "+faststart", outp]
    run(cmd)
    # --- 4) loudnorm
    tmp = outp + ".norm.mp4"
    run([EXE, "-y", "-loglevel", "error", "-i", outp, "-c:v", "copy",
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
         "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp])
    os.replace(tmp, outp)
    return t

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--clips", type=int, default=2)
    ap.add_argument("--target", type=float, default=30.0, help="목표 발화 시간(초)")
    ap.add_argument("--max-gap", type=float, default=0.40, help="이보다 긴 무음은 점프컷")
    ap.add_argument("--model", default="small")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    wd = os.path.join(a.outdir, "_work"); os.makedirs(wd, exist_ok=True)

    print("[1/4] transcribe")
    words, lang = transcribe(a.input, wd, a.model)
    print("[2/4] speech blocks (silence jump-cut)")
    blocks = speech_blocks(words, a.max_gap)
    talk = sum(b["dur"] for b in blocks)
    span = (blocks[-1]["e"] - blocks[0]["s"]) if blocks else 0
    print(f"  blocks={len(blocks)} talk={talk:.1f}s / span={span:.1f}s "
          f"→ 말 밀도 {100*talk/max(span,1e-9):.0f}%에서 100%로")
    print("[3/4] pick windows")
    wins = pick_windows(blocks, a.target, a.clips)
    report = {"input": a.input, "language": lang, "blocks": len(blocks),
              "talk_seconds": round(talk, 1), "clips": []}
    print("[4/4] render")
    for i, wsel in enumerate(wins, 1):
        outp = os.path.join(a.outdir, f"short_{i}.mp4")
        dur = render_clip(a.input, wsel, blocks, outp, wd, i)
        segs = blocks[wsel["i"]:wsel["j"]]
        report["clips"].append({
            "file": outp, "source_range": [round(wsel["s"], 1), round(wsel["e"], 1)],
            "duration": round(dur, 1), "score": round(wsel["score"], 2),
            "transcript": " ".join(b["text"] for b in segs)})
        print(f"  {outp}  {dur:.1f}s (원본 {wsel['s']:.0f}–{wsel['e']:.0f}s 구간, "
              f"점프컷 {len(segs)}블록)")
    json.dump(report, open(os.path.join(a.outdir, "report.json"), "w"),
              indent=2, ensure_ascii=False)
    print("done → report.json")

if __name__ == "__main__":
    main()
