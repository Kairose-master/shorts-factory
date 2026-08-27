"""EP4 「한국 보수는 왜 친중이 되었나」 — 원칙 v1.0 고정 70초 포맷.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 한국 보수가 친중이다.
② 그것을 만든 인과 (정본 §5 EP4): 중공군 개입이 없던 한국전쟁 → 적대 기억 부재 +
   반공동맹으로 같은 편 → 통일한국이 대륙경제에 철도로 연결 → 재계·안보 네트워크가
   보수의 자산 → 보수=친중. 반공 보수의 적은 베이징이 아니라 모스크바.
③ 다음 편에서 깨뜨릴 상식: "중국 의존 비판은 반중 보수의 몫" → 이 세계에선
   "중국 자본을 막아라"가 진보의 구호 (정본 EP5).
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","이 세계의 한국 보수는, 친중입니다."),
 ("s2","전제 2-7","국민당이 이긴 세계, 자유중국이니까요."),
 ("s3","약속","이유는 단순합니다. 역사가 달랐으니까요."),
 ("s4","원인A 7-20","이 세계의 한국전쟁엔 중공군이 없습니다. 압록강을 넘은 건 자유중국의 보급 열차였죠."),
 ("s5","원인A2","중국과 한국은 같은 편에서 싸웠습니다. 적대할 기억이 없습니다."),
 ("s6","원인B 20-35","그리고 이 한국은 통일국가입니다. 부산발 열차가 신의주를 지나 난징까지 갑니다. 수출길이 대륙입니다."),
 ("s7","원인B2","그 길 위에 재계가 있습니다. 부산 물류가문 3대 김도현 씨. 지킬 게 많은 쪽이 보수입니다."),
 ("s8","Second Hook 35-45","물론 이 세계에도 반공 보수가 있습니다. 그런데 그들이 노려보는 곳은, 베이징이 아니라 모스크바입니다."),
 ("s9","Payoff 45-60","친중이 이상한 게 아닙니다. 보수는 지켜온 것을 지킵니다. 그게 중국과 함께 만든 안보와 경제였을 뿐입니다."),
 ("s10","확장 60-67","그럼 이 세계에서 중국 의존을 비판하는 건, 누구일까요?"),
 ("s11","다음 모순 67-70","중국 자본을 막아라. 이 세계에선 진보의 구호입니다."),
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
