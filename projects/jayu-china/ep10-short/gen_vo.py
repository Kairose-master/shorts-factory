"""EP10 「자유중국의 20대는 누구를 보수라 부를까」 — 원칙 v1.0 고정 70초 포맷. ACT IV 시작.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 2080년 대학생에게 "보수=시장"은 낯선 문장이다.
② 그것을 만든 인과 (정본 §5 EP10: 세대별 기억이 정치 성향 묶음을 정한다):
   국가개발을 살아낸 세대→국가가 만든 질서를 지키는 것이 보수→2080년 20대는
   그 복지를 공기로 알고 태어남→기존 질서=국가 복지→그걸 허물자는 시장 개혁이
   오히려 급진의 자리→보수·진보는 내용이 아니라 위치.
③ 다음 편에서 깨뜨릴 상식: "정치인은 좌우로 깔끔히 분류된다" → EP11 분류 게임
   (이 사람은 좌파입니까, 우파입니까?).
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","2080년 대학생에게, 보수는 시장이 아닙니다."),
 ("s2","전제 2-7","국민당이 이긴 세계, 번영을 만든 건 시장이 아니라 국가였으니까요."),
 ("s3","약속","그럼 이 세계 20대의 보수는 뭘까요?"),
 ("s4","원인A 7-20","할아버지 세대는 국가가 깐 철도와 공단, 연금 위에서 자랐습니다. 그걸 지키자는 게 보수가 됐죠."),
 ("s5","원인A2","정치 성향은 논리가 아니라, 세대의 기억이 묶습니다."),
 ("s6","원인B 20-35","2080년의 20대는 그 복지를 공기처럼 마시며 태어났습니다. 그들에게 복지는 이념이 아니라, 원래 있던 질서입니다."),
 ("s7","원인B2","난징대 2학년 천위팅 씨에게 보수 아저씨란, 연금에 손대지 말라는 사람입니다."),
 ("s8","Second Hook 35-45","그러니 여러분의 상식은 여기서 뒤집힙니다. 복지를 줄이고 시장에 맡기자 — 이 캠퍼스에선 급진파의 구호입니다."),
 ("s9","Payoff 45-60","보수와 진보는 내용이 아니라 위치입니다. 지키면 보수, 바꾸면 진보. 무엇이 먼저 와 있었느냐가 정할 뿐입니다."),
 ("s10","확장 60-67","그래서 이 세계에선, 라벨만 보고는 아무것도 알 수 없습니다."),
 ("s11","다음 모순 67-70","다음 편, 정치인 한 명을 놓고 묻습니다. 좌파일까요, 우파일까요?"),
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
