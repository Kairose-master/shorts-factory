"""TTS 비교 프로브 — Gemini TTS 음성/말투 후보 vs 현행 edge-tts.

목표: ① AI 티(평탄한 억양·기계적 문말 처리) 제거 ② 훨씬 빠른 발화.
결과는 out/tts/*.wav + 길이 로그. 무료 아님 — 호출 수를 세어 출력한다.
"""
import base64, json, os, struct, subprocess, sys, wave
import urllib.request

KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-2.5-flash-preview-tts"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "tts")
os.makedirs(OUT, exist_ok=True)

TEXT = ("이 세계의 한국 보수는, 친중입니다. 국민당이 이긴 세계, 자유중국이니까요. "
        "이유는 단순합니다. 역사가 달랐으니까요.")

# 말투 지시 = AI 티를 없애는 핵심 레버
STYLES = {
    "doc_fast": "빠르고 단호한 다큐멘터리 내레이션으로, 문장 끝을 늘어뜨리지 말고 딱 끊어서 읽어줘. 쉼표에서만 짧게 숨을 쉬고, 핵심 단어에 강세를 줘:",
    "urgent": "숨가쁘게 몰아붙이는 유튜브 쇼츠 내레이션. 아주 빠르게, 힘 있게, 리듬을 타면서 읽어줘:",
}
VOICES = ["Charon", "Orus", "Alnilam", "Rasalgethi", "Iapetus"]

calls = 0


def gemini_tts(text, voice, style_key):
    global calls
    body = {
        "contents": [{"parts": [{"text": f"{STYLES[style_key]} {text}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
        },
    }
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    calls += 1
    part = d["candidates"][0]["content"]["parts"][0]
    pcm = base64.b64decode(part["inlineData"]["data"])
    mime = part["inlineData"]["mimeType"]          # audio/L16;codec=pcm;rate=24000
    rate = int(mime.split("rate=")[-1]) if "rate=" in mime else 24000
    path = f"{OUT}/gem_{voice}_{style_key}.wav"
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(pcm)
    return path, len(pcm) / 2 / rate


def edge(rate_pct, tag):
    import asyncio, edge_tts
    import imageio_ffmpeg
    mp3 = f"{OUT}/edge_{tag}.mp3"; wav = f"{OUT}/edge_{tag}.wav"
    async def go():
        t = edge_tts.Communicate(TEXT, "ko-KR-HyunsuMultilingualNeural",
                                 rate=rate_pct, pitch="-8Hz",
                                 proxy=os.environ.get("HTTPS_PROXY"))
        await t.save(mp3)
    asyncio.run(go())
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([exe, "-y", "-loglevel", "error", "-i", mp3, "-ar", "24000", "-ac", "1", wav],
                   check=True)
    os.remove(mp3)
    with wave.open(wav) as w:
        return wav, w.getnframes() / w.getframerate()


if __name__ == "__main__":
    rows = []
    for v in VOICES:
        try:
            p, d = gemini_tts(TEXT, v, "doc_fast")
            rows.append((f"gemini {v} / doc_fast", d, p))
            print(f"{v:12s} doc_fast {d:5.2f}s")
        except Exception as e:
            print(f"{v} FAIL {str(e)[:120]}")
    for v in VOICES[:2]:
        try:
            p, d = gemini_tts(TEXT, v, "urgent")
            rows.append((f"gemini {v} / urgent", d, p))
            print(f"{v:12s} urgent   {d:5.2f}s")
        except Exception as e:
            print(f"{v} urgent FAIL {str(e)[:120]}")
    for r in ("+13%", "+30%"):
        p, d = edge(r, r.replace("%", "").replace("+", "p"))
        rows.append((f"edge Hyunsu {r} (현행)" if r == "+13%" else f"edge Hyunsu {r}", d, p))
        print(f"edge {r:5s}       {d:5.2f}s")
    print(f"\nGemini 호출 {calls}회")
    json.dump([[n, d, p] for n, d, p in rows], open(f"{OUT}/index.json", "w"), ensure_ascii=False, indent=1)
