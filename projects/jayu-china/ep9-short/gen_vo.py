"""EP9 「대만독립이 없는 세계의 대만 정치」 — 원칙 v1.0 고정 70초 포맷. ACT III 마지막.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 대만 선거의 최대 쟁점이 독립·통일이 아니다.
② 그것을 만든 인과 (정본 §5 EP9: 대만 지역주의·연방주의 + 홍콩 constitutional
   autonomy = 영토정치의 다른 가능성): 공산 혁명이 없는 세계→대만은 자유중국의 한 성
   →분리 공포도 병합 위협도 없음→존재를 묻는 질문 자체가 부재→정치의 축은 난징과의
   거리(세금·항만·교과서)→홍콩도 같은 문법→영토정치가 안보의 언어에서 회계의 언어로 번역.
③ 다음 편에서 깨뜨릴 상식: "보수=시장" → 2080년 대학생에겐 낯선 문장 (정본 EP10 훅).
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","이 세계 대만 선거의 최대 쟁점은, 독립이 아닙니다."),
 ("s2","전제 2-7","국민당이 이긴 세계, 대만은 자유중국의 한 성이니까요."),
 ("s3","약속","그럼 무엇으로 싸울까요?"),
 ("s4","원인A 7-20","이 세계엔 분리의 공포도, 병합의 위협도 없습니다. 존재를 묻는 질문이 애초에 없는 겁니다."),
 ("s5","원인A2","질문이 사라지면, 그 자리를 채우는 건 생활입니다."),
 ("s6","원인B 20-35","그래서 쟁점은 난징과의 거리입니다. 세금을 얼마나 남길지, 항만을 누가 운영할지, 교과서를 어디서 정할지."),
 ("s7","원인B2","가오슝 항만 노동자 린원제 씨의 투표 기준은, 국기가 아니라 하역료 배분입니다."),
 ("s8","Second Hook 35-45","그런데 바다 건너 홍콩이 같은 걸 요구합니다. 두 섬의 공통 구호는 통일도 독립도 아닌, 자치입니다."),
 ("s9","Payoff 45-60","영토의 정치가 사라진 게 아닙니다. 안보의 언어에서 회계의 언어로 번역됐을 뿐입니다. 존재를 안 물으면, 예산을 묻습니다."),
 ("s10","확장 60-67","이제 이 지형 위에서, 표를 던질 차례입니다."),
 ("s11","다음 모순 67-70","2080년 대학생에게, 보수는 시장이 아닙니다."),
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
