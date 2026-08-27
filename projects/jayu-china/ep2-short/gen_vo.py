"""EP2 「자유중국의 보수는 누구인가」 — canon §10 비트 시트 준거."""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","한 정당의 공약입니다. 국영 반도체 투자 확대, 복지연금 유지, 국방비 증액, 지방정부 권한 제한."),
 ("s2","좌파일까요, 우파일까요? 이 세계의 집권 보수당, 국민당의 공약입니다."),
 ("s3","이유는 역사에 있습니다. 이 세계의 국민당은 통일과 반공과 산업화를 국가의 손으로 해냈습니다."),
 ("s4","그래서 국가주도 개발국가 그 자체가, 보수가 지켜야 할 기존 질서가 됐습니다."),
 ("s5","복지도 마찬가지입니다. 전 국민 보험은 이 당이 만들었습니다. 자기 유산을 지키는 게 보수니까요."),
 ("s6","물론 하나가 아닙니다. 국가개발보수, 시장보수, 유교보수, 주권주의. 우파 안에서도 넷이 싸웁니다."),
 ("s7","더 이상한 사실 하나. 작은 정부를 원하는 시장자유파는, 1980년대에 진보 연합에 서 있었습니다."),
 ("s8","난징의 63살 천젠궈 씨는 말합니다. 우리 부모 세대가 이 나라 산업을 만들었다고. 24살 린샤오 씨는 그걸 낡은 기득권이라 부릅니다."),
 ("s9","보수의 내용이 이상한 게 아닙니다. 무엇이 기존 질서였는지가, 달랐던 겁니다."),
 ("s10","그럼 이 세계의 진보는, 누구일까요?"),
]
async def gen():
    plan=[]
    for sid,text in LINES:
        mp3=f"{OUT}/{sid}.mp3"; wav=f"{OUT}/{sid}.wav"
        t=edge_tts.Communicate(text,V,rate="+13%",pitch="-8Hz",
                               proxy=os.environ.get("HTTPS_PROXY"))
        await t.save(mp3)
        subprocess.run([EXE,"-y","-loglevel","error","-i",mp3,"-ar","24000","-ac","1",wav],check=True)
        os.remove(mp3)
        with wave.open(wav) as w: dur=w.getnframes()/w.getframerate()
        plan.append({"id":sid,"dur":round(dur,2),"text":text})
        print(f"{sid} {dur:5.2f}s | {text[:40]}")
    json.dump(plan,open(f"{OUT}/lines.json","w"),indent=2,ensure_ascii=False)
    print(f"narration {sum(p['dur'] for p in plan):.1f}s")
asyncio.run(gen())
