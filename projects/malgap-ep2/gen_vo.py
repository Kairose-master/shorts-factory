"""No.2 「정통」 내레이션 — edge-tts, 건조한 다큐 톤 단일 보이스."""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
EXE=imageio_ffmpeg.get_ffmpeg_exe()
LINES=[
 ("s1","냉면 한 그릇이 만육천 원입니다."),
 ("s2","정통은, 이렇게 만들어집니다."),
 ("s3","먼저, 오래된 간판이 필요합니다."),
 ("s4","다음은, 줄입니다."),
 ("s5","육수는, 고기를 물에 잠시 담근 농도라는 비판을 받기도 했습니다."),
]
async def gen():
    plan=[]
    for sid,text in LINES:
        mp3=f"{OUT}/{sid}.mp3"; wav=f"{OUT}/{sid}.wav"
        t=edge_tts.Communicate(text,"ko-KR-InJoonNeural",rate="-12%",pitch="-15Hz",
                               proxy=os.environ.get("HTTPS_PROXY"))
        await t.save(mp3)
        subprocess.run([EXE,"-y","-loglevel","error","-i",mp3,"-ar","24000","-ac","1",wav],check=True)
        os.remove(mp3)
        with wave.open(wav) as w: dur=w.getnframes()/w.getframerate()
        plan.append({"id":sid,"dur":round(dur,2),"text":text})
        print(f"{sid} {dur:5.2f}s | {text}")
    json.dump(plan,open(f"{OUT}/lines.json","w"),indent=2,ensure_ascii=False)
asyncio.run(gen())
