"""EP8 「친미는 좌파인가 우파인가?」 — 원칙 v1.0 고정 70초 포맷.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: '친미'가 좌우의 고정 표식이 아니다 — 1950년엔 보수의
   말, 2050년엔 진보의 말로, 같은 세계 안에서 자리를 옮긴다.
② 그것을 만든 인과 (정본 §5 EP8: 미중관계 변화에 따라 친미가 보수→자유주의 진보로
   이동): 1950년 미국=반공 질서의 축→친미=질서 수호=보수 / 세기가 지나며 동아시아
   기존 질서의 중심이 자유중국으로→그 질서에 도전하는 쪽에게 미국은 균형추·개혁의
   지렛대→친미=진보. 축이 움직이면 같은 방향도 반대편이 된다.
③ 다음 편에서 깨뜨릴 상식: "대만 선거의 최대 쟁점은 독립" → 이 세계에선 아니다
   (정본 EP9 훅 그대로).
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","1950년의 친미는 보수였고, 2050년의 친미는 진보입니다."),
 ("s2","전제 2-7","국민당이 이긴 세계의 동아시아입니다."),
 ("s3","약속","같은 친미가 왜 자리를 옮겼을까요?"),
 ("s4","원인A 7-20","1950년, 미국은 반공 질서의 축이었습니다. 미국 편에 서는 게 질서를 지키는 일, 보수의 말이었죠."),
 ("s5","원인A2","그때의 반미는 반질서, 급진의 말이었습니다."),
 ("s6","원인B 20-35","그런데 세기가 지나며 지역의 중심이 바뀝니다. 동아시아의 기존 질서는 이제, 자유중국입니다."),
 ("s7","원인B2","이 질서에 도전하려는 쪽에게 미국은 균형추가 됩니다. 개혁의 지렛대요."),
 ("s8","Second Hook 35-45","그래서 2050년의 어느 집회에선 자유무역과 미국과 개혁을 한 깃발이 외칩니다. 그 깃발의 색은, 진보입니다."),
 ("s9","Payoff 45-60","친미가 이념인 적은 없습니다. 미국이 변한 게 아니라 질서의 중심이 옮겨간 겁니다. 축이 움직이면, 같은 방향도 반대편이 됩니다."),
 ("s10","확장 60-67","그리고 이 질문을 가장 낯설게 받는 곳이 있습니다."),
 ("s11","다음 모순 67-70","이 세계 대만 선거의 최대 쟁점은, 독립이 아닙니다."),
]
async def gen():
    plan=[]
    for sid,seg,text in LINES:
        mp3=f"{OUT}/{sid}.mp3"; wav=f"{OUT}/{sid}.wav"
        t=edge_tts.Communicate(text,V,rate="+13%",pitch="-8Hz",
                               proxy=os.environ.get("HTTPS_PROXY"))
        await t.save(mp3)
        subprocess.run([EXE,"-y","-loglevel","error","-i",mp3,"-ar","24000","-ac","1",wav],check=True)
        os.remove(mp3)
        with wave.open(wav) as w: dur=w.getnframes()/w.getframerate()
        plan.append({"id":sid,"seg":seg,"dur":round(dur,2),"text":text})
        print(f"{sid} {dur:5.2f}s [{seg}] {text[:34]}")
    json.dump(plan,open(f"{OUT}/lines.json","w"),indent=2,ensure_ascii=False)
    print(f"narration {sum(p['dur'] for p in plan):.1f}s")
asyncio.run(gen())
