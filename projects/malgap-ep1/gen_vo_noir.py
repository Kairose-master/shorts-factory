"""No.1 시그니처 — Ledger Noir 판 내레이션. No.2와 동일 보이스로 연작 통일."""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo-noir")
EXE=imageio_ffmpeg.get_ffmpeg_exe()
LINES=[
 ("s1","단어 하나가 얼마짜리인지, 재 본 적 있으세요?"),
 ("s2","시그니처."),
 ("s3","이건, 요거트에 토핑 세 개입니다."),
 ("s4","삼만 원이 넘습니다."),
 ("s5","재료값을 빼면, 남는 건 단어입니다."),
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
