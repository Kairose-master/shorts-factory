"""gtts_kit — Gemini TTS 내레이션 생성 + 무음 기반 자막 정렬.

편집장 확정(2026-08-29): 음성 Orus, 말투 '몰아붙임'(urgent), 속도는 그 상태 그대로.
edge-tts 대비 같은 대본에서 약 38% 짧아진다 — AI 티(평탄한 억양·늘어지는 문말)의
원인이 속도가 아니라 억양 통제 부재였기 때문. 말투 지시로 해결.

Gemini TTS는 WordBoundary를 주지 않으므로 자막 칩은 이렇게 맞춘다:
  ① 대본을 구(句) 단위로 먼저 쪼갠다(문장부호 + 길이).
  ② 오디오에서 무음 구간(RMS 저점)을 찾는다.
  ③ 각 구의 기대 시작 시각(글자수 비례)에 가장 가까운 무음을 경계로 채택,
     없으면 기대값을 그대로 쓴다.
"""
import base64, json, os, re, time, wave
import urllib.request
import numpy as np

MIN_INTERVAL = float(os.environ.get("GTTS_INTERVAL", "22"))  # 무료 티어 RPM 회피
_last_call = [0.0]

MODEL = os.environ.get("GTTS_MODEL", "gemini-3.1-flash-tts-preview")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
VOICE = "Orus"
STYLE = ("숨가쁘게 몰아붙이는 유튜브 쇼츠 내레이션. 아주 빠르게, 힘 있게, "
         "리듬을 타면서 읽어줘:")


def synth(text, path, voice=VOICE, style=STYLE, retries=6):
    """Gemini TTS 1콜 → 24kHz mono wav. 길이(초) 반환."""
    key = os.environ["GEMINI_API_KEY"]
    body = {"contents": [{"parts": [{"text": f"{style} {text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    last = None
    for attempt in range(retries):
        wait = max(0.0, MIN_INTERVAL - (time.time() - _last_call[0]))
        if attempt:
            wait = max(wait, MIN_INTERVAL * (1.6 ** attempt))     # 429 백오프
        if wait:
            time.sleep(wait)
        _last_call[0] = time.time()
        try:
            req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.load(r)
            part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
            pcm = base64.b64decode(part["data"])
            m = re.search(r"rate=(\d+)", part["mimeType"])
            rate = int(m.group(1)) if m else 24000
            a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32)
            if rate != 24000:                      # 파이프라인 표준 24k로 리샘플
                a = np.interp(np.linspace(0, len(a), int(len(a)*24000/rate)),
                              np.arange(len(a)), a)
            a = np.clip(a, -32000, 32000).astype(np.int16)
            with wave.open(path, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
                w.writeframes(a.tobytes())
            return len(a) / 24000
        except Exception as e:                     # 429/일시 오류는 재시도
            last = e
    raise RuntimeError(f"gemini tts failed: {last}")


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
    for c in parts:                                # 과장 구는 중앙 공백에서 한 번 더
        while len(c) > max_chars + 8 and " " in c:
            idx = [i for i, ch in enumerate(c) if ch == " "]
            cut = min(idx, key=lambda i: abs(i - len(c) // 2))
            out.append(c[:cut].strip()); c = c[cut:].strip()
        out.append(c)
    return [c for c in out if c]


def silences(wav_path, win=0.02, thresh_ratio=0.16, min_gap=0.09):
    """무음 구간 [(start, end)] — RMS가 전체 중앙값 대비 낮은 연속 구간."""
    with wave.open(wav_path) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    n = int(sr * win)
    m = len(a) // n
    if m < 3:
        return []
    rms = np.sqrt((a[:m*n].reshape(m, n) ** 2).mean(axis=1))
    thr = max(rms.max() * thresh_ratio, np.median(rms) * 0.35)
    quiet = rms < thr
    out, i = [], 0
    while i < m:
        if quiet[i]:
            j = i
            while j < m and quiet[j]:
                j += 1
            if (j - i) * win >= min_gap:
                out.append((i * win, j * win))
            i = j
        else:
            i += 1
    return out


def chips(text, wav_path, dur, tail=0.30):
    """구 + 무음 정렬 → [(칩 텍스트, 시작초, 길이초)]."""
    ph = phrases(text)
    if len(ph) == 1:
        return [(ph[0], 0.0, dur)]
    gaps = [g for g in silences(wav_path) if 0.25 < g[0] < dur - 0.25]
    total = sum(len(p) for p in ph)
    bounds, acc = [], 0
    for p in ph[:-1]:                              # 각 구의 끝 = 다음 구 시작
        acc += len(p)
        exp = dur * acc / total
        cand = [g for g in gaps if abs((g[0]+g[1])/2 - exp) < 0.75]
        if cand:
            g = min(cand, key=lambda g: abs((g[0]+g[1])/2 - exp))
            bounds.append(round((g[0] + g[1]) / 2, 3))
            gaps = [x for x in gaps if x[0] > g[1]]
        else:
            bounds.append(round(exp, 3))
    bounds = sorted(set(bounds))
    while len(bounds) < len(ph) - 1:               # 중복 제거로 모자라면 기대값 보충
        bounds.append(round(dur * (len(bounds) + 1) / len(ph), 3))
        bounds = sorted(set(bounds))
    starts = [0.0] + bounds[:len(ph)-1]
    ends = bounds[:len(ph)-1] + [min(dur + tail, dur + tail)]
    return [(ph[i], round(starts[i], 3), round(ends[i] - starts[i], 3)) for i in range(len(ph))]


def generate(LINES, outdir):
    """LINES: [(sid, seg, text)] → wav + lines.json(v3, chips 포함). 총 초 반환."""
    os.makedirs(outdir, exist_ok=True)
    plan = []
    for sid, seg, text in LINES:
        wav = f"{outdir}/{sid}.wav"
        if os.path.exists(wav):                    # 중단 지점부터 이어서
            with wave.open(wav) as w:
                dur = round(w.getnframes() / w.getframerate(), 2)
        else:
            dur = round(synth(text, wav), 2)
        cs = chips(text, wav, dur)
        plan.append({"id": sid, "seg": seg, "dur": dur, "text": text,
                     "chips": [[c, s, d] for c, s, d in cs]})
        print(f"{sid} {dur:5.2f}s c{len(cs)} [{seg}] {text[:28]}")
    json.dump(plan, open(f"{outdir}/lines.json", "w"), indent=1, ensure_ascii=False)
    total = sum(p["dur"] for p in plan)
    print(f"narration {total:.1f}s  (Gemini TTS {len(LINES)}콜)")
    return total
