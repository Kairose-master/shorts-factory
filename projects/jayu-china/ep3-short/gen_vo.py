"""EP3 「자유중국의 진보는 왜 시장을 원했나」 — 제작 원칙 v1.0 고정 70초 포맷.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 진보가 민영화·개방·언론자유를 '시장의 언어'로 주장한다.
② 그것을 만든 인과: 기존 질서=국가(국영기업·중앙집권·검열) → 바꾸려는 쪽은 그 반대말을
   들 수밖에 없음 → 시장개혁·분권·언론자유가 개혁의 언어 → 1980년대 민주화 연합으로 결집
   → 진보=시장. 역으로 국영기업 노조는 지킬 것이 있어 보수 편에 섬.
③ 다음 편에서 깨뜨릴 상식: "한국 보수는 반중, 진보는 친중" → 이 세계에선 정반대. (EP4)
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[  # (id, 구간, text)
 ("s1","WTF 0-2","이 세계의 진보는 민영화를 주장합니다."),
 ("s2","전제 2-7","국민당이 내전에서 이긴 세계, 자유중국이니까요."),
 ("s3","약속","모순 같지만, 역사를 보면 필연입니다."),
 ("s4","원인A 7-20","이 세계의 기존 질서는 국가였습니다. 국영기업, 중앙집권, 그리고 신문 검열."),
 ("s5","원인A2","바꾸려는 쪽은 반대말을 들 수밖에 없습니다. 시장개혁, 지방분권, 언론자유."),
 ("s6","원인B 20-35","1980년대 민주화 연합이 그렇게 모였습니다. 국영 신문을 그만둔 기자 쉬리핑 씨도, 시장자유파 옆에 섰습니다."),
 ("s7","원인B2","개혁의 언어가, 시장이 된 겁니다."),
 ("s8","Second Hook 35-45","그런데 더 이상한 일이 벌어집니다. 국영기업 노동조합이, 보수 편에 섭니다. 지킬 것이 그쪽에 있으니까요."),
 ("s9","Payoff 45-60","진보가 시장을 사랑한 게 아닙니다. 기존 질서를 바꿀 말이 시장뿐이었던 겁니다. 무엇이 진보인지는, 무엇이 기존 질서인지가 정합니다."),
 ("s10","확장 60-67","그리고 국경 밖에선 이 뒤집힘이 더 큽니다."),
 ("s11","다음 모순 67-70","이 세계의 한국은, 보수가 친중이고 진보가 반중입니다."),
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
