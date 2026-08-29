"""evo_kit — edge-tts 구(句) 단위 합성 내레이션 (무료·무제한).

편집장 결정(2026-08-29): Gemini TTS는 무료 등급이 모델당 하루 10콜이라 시즌
제작에 못 쓴다 → edge-tts로 복귀하되 "AI 티"와 느린 속도를 구조로 잡는다.

한 줄을 통째로 합성하지 않고 구 단위로 쪼개 각각 합성한 뒤 이어붙인다:
  ① edge가 문장 끝마다 자동으로 넣는 0.4~0.6초 정적을 제거 → 체감 속도 급상승
  ② 구마다 rate/pitch를 결정적으로 미세하게 흔들어 평탄한 억양을 깬다
  ③ 각 구의 시작·길이를 정확히 알게 되므로 자막 칩이 추정이 아니라 실측이 된다
"""
import asyncio, json, os, subprocess, wave
import numpy as np
import edge_tts
import imageio_ffmpeg

EXE = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = "ko-KR-HyunsuMultilingualNeural"
BASE_RATE = int(os.environ.get("EVO_RATE", "32"))     # %
BASE_PITCH = -8                                        # Hz
SR = 24000
GAP_IN = 0.05      # 문장 안 구 사이
GAP_END = 0.15     # 문장 끝 뒤
TAIL = 0.25        # 마지막 칩이 남는 시간


def phrases(text, max_chars=15):
    """대본 → 자막 칩 단위 구 리스트 (문장부호 우선 절단)."""
    parts, cur = [], ""
    for tok in text.replace("…", "… ").split(" "):
        if not tok:
            continue
        if cur and (len(cur) + len(tok) + 1 > max_chars or cur[-1] in ".,?!…"):
            parts.append(cur); cur = tok
        else:
            cur = (cur + " " + tok).strip()
    if cur:
        parts.append(cur)
    out = []
    for c in parts:
        while len(c) > max_chars + 8 and " " in c:
            idx = [i for i, ch in enumerate(c) if ch == " "]
            cut = min(idx, key=lambda i: abs(i - len(c) // 2))
            out.append(c[:cut].strip()); c = c[cut:].strip()
        out.append(c)
    return [c for c in out if c]


def _trim(a, thresh=0.012):
    """앞뒤 무음 제거 — edge가 붙이는 패딩을 잘라 붙임새를 타이트하게."""
    if len(a) == 0:
        return a
    e = np.abs(a) / 32768.0
    win = 240
    m = len(e) // win
    if m < 2:
        return a
    r = np.sqrt((e[:m*win].reshape(m, win) ** 2).mean(axis=1))
    on = np.where(r > thresh)[0]
    if len(on) == 0:
        return a
    return a[max(0, (on[0]-1))*win: min(m, on[-1]+2)*win]


async def _one(text, rate, pitch, path):
    c = edge_tts.Communicate(text, VOICE, rate=f"{rate:+d}%", pitch=f"{pitch:+d}Hz",
                             proxy=os.environ.get("HTTPS_PROXY"))
    await c.save(path)


def synth_line(text, wav_path, seed=0):
    """한 줄을 구 단위로 합성·접합. (총초, [(칩, 시작, 길이)]) 반환."""
    ph = phrases(text)
    tmp = wav_path + ".part"
    segs, sched, t = [], [], 0.0
    for i, p in enumerate(ph):
        # 결정적 미세 변주 — 같은 대본이면 항상 같은 결과
        j = (seed * 7 + i * 13) % 5
        rate = BASE_RATE + (j - 2) * 3          # ±6%
        pitch = BASE_PITCH + ((j % 3) - 1)      # ±1Hz
        asyncio.run(_one(p, rate, pitch, tmp + ".mp3"))
        subprocess.run([EXE, "-y", "-loglevel", "error", "-i", tmp + ".mp3",
                        "-ar", str(SR), "-ac", "1", tmp + ".wav"], check=True)
        with wave.open(tmp + ".wav") as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        a = _trim(a.astype(np.float32))
        d = len(a) / SR
        sched.append((p, round(t, 3), round(d + (GAP_IN if i < len(ph)-1 else TAIL), 3)))
        segs.append(a)
        gap = GAP_END if p[-1:] in ".?!…" else GAP_IN
        if i < len(ph) - 1:
            segs.append(np.zeros(int(SR * gap), np.float32))
            t += d + gap
        else:
            t += d
    for ext in (".mp3", ".wav"):
        if os.path.exists(tmp + ext):
            os.remove(tmp + ext)
    out = np.concatenate(segs) if segs else np.zeros(1, np.float32)
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.clip(out, -32000, 32000).astype(np.int16).tobytes())
    return round(t, 2), sched


def generate(LINES, outdir):
    """LINES: [(sid, seg, text)] → wav + lines.json(v3 스키마: chips 포함)."""
    os.makedirs(outdir, exist_ok=True)
    plan, total = [], 0.0
    for i, (sid, seg, text) in enumerate(LINES):
        dur, sched = synth_line(text, f"{outdir}/{sid}.wav", seed=i)
        plan.append({"id": sid, "seg": seg, "dur": dur, "text": text,
                     "chips": [[c, s, d] for c, s, d in sched]})
        total += dur
        print(f"{sid} {dur:5.2f}s c{len(sched)} [{seg}] {text[:26]}")
    json.dump(plan, open(f"{outdir}/lines.json", "w"), indent=1, ensure_ascii=False)
    print(f"narration {total:.1f}s (edge {BASE_RATE:+d}% 구 단위)")
    return total
