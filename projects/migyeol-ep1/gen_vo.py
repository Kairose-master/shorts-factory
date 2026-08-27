"""「미결」 No.1 가드너 미술관 — 궁금소 171x 과정 서술 문법. 전 사실 FBI/미술관 공식 출처."""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
EXE=imageio_ffmpeg.get_ffmpeg_exe()
LINES=[
 ("s1","1990년 새벽 보스턴. 경찰복을 입은 두 남자가 미술관 벨을 눌렀습니다."),
 ("s2","경비원들은 지하실에 묶였습니다. 81분."),
 ("s3","베르메르, 렘브란트. 열세 점, 5억 달러어치가 사라졌습니다."),
 ("s4","현상금 천만 달러. 범인은 아직 없습니다."),
 ("s5","미술관은 그 자리에 빈 액자를 그대로 걸어 뒀습니다."),
 ("s6","액자는 지금도 비어 있습니다."),
]
async def gen():
    plan=[]
    for sid,text in LINES:
        mp3=f"{OUT}/{sid}.mp3"; wav=f"{OUT}/{sid}.wav"
        t=edge_tts.Communicate(text,"ko-KR-InJoonNeural",rate="+4%",pitch="-10Hz",
                               proxy=os.environ.get("HTTPS_PROXY"))
        await t.save(mp3)
        subprocess.run([EXE,"-y","-loglevel","error","-i",mp3,"-ar","24000","-ac","1",wav],check=True)
        os.remove(mp3)
        with wave.open(wav) as w: dur=w.getnframes()/w.getframerate()
        plan.append({"id":sid,"dur":round(dur,2),"text":text})
        print(f"{sid} {dur:5.2f}s | {text}")
    json.dump(plan,open(f"{OUT}/lines.json","w"),indent=2,ensure_ascii=False)
    print(f"narration total {sum(p['dur'] for p in plan):.1f}s")
asyncio.run(gen())
