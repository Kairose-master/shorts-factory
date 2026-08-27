"""Dialogue TTS for 「말갑」 EP1 cartoon — edge-tts (no key, no quota).
Needs: SSL_CERT_FILE=/root/.ccr/ca-bundle.crt and HTTPS_PROXY set (agent proxy)."""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg

OUT = os.path.join(os.path.dirname(__file__), "vo")
EXE = imageio_ffmpeg.get_ffmpeg_exe()
# id, speaker, voice, rate/pitch tweak (emotion), line
LINES = [
 ("l1","dahye", "ko-KR-SunHiNeural", "+8%", "+20Hz", "사장님, 요거트 하나에 3만 원이요?"),
 ("l2","sajang","ko-KR-InJoonNeural","-5%", "-10Hz", "시그니처니까요."),
 ("l3","dahye", "ko-KR-SunHiNeural", "+10%","+0Hz",  "뭐가 다른데요?"),
 ("l4","sajang","ko-KR-InJoonNeural","-8%", "-15Hz", "저희만의 큐레이션입니다."),
 ("l5","dahye", "ko-KR-SunHiNeural", "+0%", "-15Hz", "토핑 세 개잖아요."),
 ("l6","sajang","ko-KR-InJoonNeural","+5%", "+5Hz",  "프리미엄 토핑이죠."),
 ("l7","dahye", "ko-KR-SunHiNeural", "-5%", "-20Hz", "재료값은 얼마인데요?"),
 ("l8","sajang","ko-KR-InJoonNeural","-15%","-20Hz", "그건… 영업 비밀입니다."),
]

async def gen():
    plan = []
    for lid, spk, voice, rate, pitch, text in LINES:
        mp3 = f"{OUT}/{lid}.mp3"; wav = f"{OUT}/{lid}.wav"
        t = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch,
                                 proxy=os.environ.get("HTTPS_PROXY"))
        await t.save(mp3)
        subprocess.run([EXE,"-y","-loglevel","error","-i",mp3,
                        "-ar","24000","-ac","1",wav], check=True)
        os.remove(mp3)
        with wave.open(wav) as w: dur = w.getnframes()/w.getframerate()
        plan.append({"id":lid,"spk":spk,"dur":round(dur,2),"text":text})
        print(f"{lid} {spk:<6} {dur:5.2f}s | {text}")
    json.dump(plan, open(f"{OUT}/lines.json","w"), indent=2, ensure_ascii=False)
    print(f"\ntotal dialogue {sum(p['dur'] for p in plan):.2f}s")

asyncio.run(gen())
