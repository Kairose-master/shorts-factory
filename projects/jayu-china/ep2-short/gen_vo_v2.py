"""EP2 v2 — Shorts 제작 원칙 v1.0 고정 70초 포맷.

제작 전 세 문장 (원칙 최종 규칙):
① 현실과 가장 반대되는 사실: 보수가 복지와 국영기업을 지키고, 진보가 민영화를 주장한다.
② 그것을 만든 역사적 인과: 국민당 승리 → 반공 개발국가 → 국가주도 산업화·전민보험 제도화
   → 민주화 후에도 기존 질서=국가개입 → 지킬 것이 많은 쪽이 보수가 됨 → 개혁세력이 시장화 요구.
③ 다음 편에서 깨뜨릴 상식: "한국 보수는 반중이다" → 이 세계에선 친중. (정본 파일럿 순서 EP1→EP2→EP4)
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo2")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[  # (id, 구간, text)
 ("s1","WTF 0-2","이 세계의 보수는 복지를 지킵니다."),
 ("s2","전제 2-7","1946년 국민당이 내전에서 이긴 세계니까요."),
 ("s3","약속","왜 그런지 역사가 답합니다."),
 ("s4","원인A 7-20","국민당은 반공을 위해 국가를 키웠습니다. 국영 철강과 반도체, 철도와 항만까지."),
 ("s5","원인A2","통일과 반공과 산업화를 해낸 당. 그게 집권 보수당입니다."),
 ("s6","원인B 20-35","그리고 제도가 됐습니다. 전 국민 보험도 이 당이 만들었고, 국영기업에서 평생 일한 천젠궈 씨 세대가 유권자입니다."),
 ("s7","원인B2","민주화가 와도 질서는 남았습니다. 지킬 게 많은 쪽이 보수가 되니까요."),
 ("s8","Second Hook 35-45","그런데 여기서 정치가 뒤집힙니다. 작은 정부를 원하던 시장자유파가 1980년대엔 진보 연합에 있었습니다."),
 ("s9","Payoff 45-60","보수가 이상한 게 아닙니다. 이 세계의 기존 질서가 국가개입이었을 뿐. 그래서 개혁을 외치는 진보가 민영화를 주장합니다."),
 ("s10","확장 60-67","이 뒤집힘은 중국에서 끝나지 않습니다."),
 ("s11","다음 모순 67-70","이 세계의 한국 보수는, 친중입니다."),
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
