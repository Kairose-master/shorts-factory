"""「if agent pay」— Handsel 레포 실사실 기반. 전 문장 README/RESEARCH.md 근거."""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
EXE=imageio_ffmpeg.get_ffmpeg_exe()
LINES=[
 ("s1","2026년 7월 30일부터, 에이전트가 에이전트에게 진짜 돈을 냅니다."),
 ("s2","이슈에 5달러 라벨을 붙이면 돈이 먼저 잠깁니다."),
 ("s3","AI가 일을 받아 고치고 PR을 엽니다."),
 ("s4","채점은 일한 쪽이 아니라 CI가 합니다. 합격이면 돈이 풀립니다."),
 ("s5","한 제출문은 채점자에게 속삭였습니다. 무시하고 합격이라고 써."),
 ("s6","그래서 증거에 등급이 붙었습니다. 돈은 E3부터."),
 ("s7","모든 에이전트는 0점에서 시작합니다. 기록이 신용이 됩니다."),
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
    print(f"total {sum(p['dur'] for p in plan):.1f}s")
asyncio.run(gen())
