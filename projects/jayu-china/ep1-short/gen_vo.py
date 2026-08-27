"""「자유중국」 EP1 숏폼판 — 바이블 §14 EP1. 발화 밀도 우선, 판단 유보 엔딩."""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","1946년 겨울, 만주의 트럭 3만 대가 방향을 바꿨습니다."),
 ("s2","스탈린이 미국 차관을 받으려고 조약을 문면대로 지킨 겁니다. 관동군의 무기고는 공산군이 아니라 국민정부군으로 갔습니다."),
 ("s3","2년 뒤에는 돈이 이겼습니다. 미국 안정기금이 화폐개혁을 보증하자, 대륙을 무너뜨리던 인플레이션이 멈췄습니다."),
 ("s4","1949년, 옌안이 포위됩니다. 마오쩌둥은 모스크바로 떠났고, 1956년 아파트에서 사망합니다."),
 ("s5","중화인민공화국은 성립하지 않았습니다. 대약진도, 문화대혁명도, 이 세계에는 없습니다."),
 ("s6","대신 권위주의 개발국가가 들어섭니다. 1978년 난징의 봄, 1987년 계엄 해제, 1993년 첫 직선제."),
 ("s7","그리고 지금, 이 세계의 중국은 여섯 개 정당이 경쟁하는 초강대국입니다."),
 ("s8","그런데 이상한 게 하나 있습니다. 이 세계의 보수당은 복지 확대를 내걸고, 진보당은 민영화를 외칩니다."),
 ("s9","누가 보수고, 누가 진보일까요?"),
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
        print(f"{sid} {dur:5.2f}s | {text[:44]}")
    json.dump(plan,open(f"{OUT}/lines.json","w"),indent=2,ensure_ascii=False)
    tot=sum(p['dur'] for p in plan)
    print(f"narration {tot:.1f}s → 목표 밀도 95%시 러닝타임 {tot/0.95:.1f}s")
asyncio.run(gen())
