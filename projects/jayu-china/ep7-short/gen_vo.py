"""EP7 「일본 좌파가 재무장을 주장한 이유」 — 원칙 v1.0 고정 70초 포맷. ACT III 진입.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 일본 좌파가 재무장·자주국방을 주장한다.
② 그것을 만든 인과 (정본 §5 EP7: 대미 자율성을 요구하는 세력이 자주국방과 재무장을
   동시에 주장): 이 세계 일본의 기존 질서 = 미군 주둔·대미 종속 안보 → 우파는 동맹
   질서를 수호 → 좌파의 원칙은 '자율'(기지 반대·주권 회복) → 미군이 줄면 방위 공백
   → 자율의 값 = 자주국방 → 좌파 = 기지 축소 + 재무장 동시 주장.
③ 다음 편에서 깨뜨릴 상식: "친미는 보수" → 1950년의 친미 보수와 2050년의 친미
   진보가 동시에 존재 (정본 EP8 훅 그대로).
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","미군기지를 줄이자. 일본군을 키우자. 같은 사람의 말입니다."),
 ("s2","전제 2-7","국민당이 이긴 세계, 이 세계의 일본입니다."),
 ("s3","약속","말한 쪽은 좌파입니다. 왜일까요?"),
 ("s4","원인A 7-20","이 세계 일본의 기존 질서는 미군이었습니다. 기지, 안보 우산, 그리고 그 아래의 정치."),
 ("s5","원인A2","우파는 그 질서를 지킵니다. 동맹이 곧 국익이니까요."),
 ("s6","원인B 20-35","좌파의 말은 언제나 자율이었습니다. 기지 반대, 주권 회복, 대미 자립."),
 ("s7","원인B2","그런데 미군이 나가면 방위엔 공백이 생깁니다. 자율의 값은, 자주국방입니다."),
 ("s8","Second Hook 35-45","그래서 도쿄의 평화 집회에서 군비 증강 서명을 받습니다. 반전과 재무장이 같은 부스에 있습니다."),
 ("s9","Payoff 45-60","좌파가 변한 게 아닙니다. 자율이라는 원칙이 이 세계에선 재무장이라는 결론을 낳았을 뿐입니다. 원칙이 같아도, 질서가 다르면 결론이 뒤집힙니다."),
 ("s10","확장 60-67","그럼 이 세계에서 친미는, 보수일까요?"),
 ("s11","다음 모순 67-70","1950년의 친미 보수와, 2050년의 친미 진보가, 동시에 존재합니다."),
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
