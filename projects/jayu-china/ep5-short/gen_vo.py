"""EP5 「"중국 자본을 막아라" — 한국 진보의 탄생」 — 원칙 v1.0 고정 70초 포맷.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 중국 자본 규제·반중 구호가 진보의 것이다.
② 그것을 만든 인과 (정본 §5 EP5): 대륙 통합의 수혜는 재계·보수에 집중, 청구서는
   노동에 감 → 산업주권·노동·문화자율·외교다변화를 이유로 의존을 비판 → 그 비판은
   기존 질서(=중국과의 통합)와의 싸움 → 싸우는 쪽의 이름이 진보. (EP3 논리의 한국판)
③ 다음 편에서 깨뜨릴 상식: "정치가 반중이면 청년도 반중" → 청년에겐 중국이 생활 —
   중국 유학이 미국 유학만큼 자연스럽다 (정본 EP6).
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","중국 자본 규제를 외치는 쪽은, 진보당입니다."),
 ("s2","전제 2-7","국민당이 이긴 세계, 수출길이 대륙인 한국이니까요."),
 ("s3","약속","누가, 왜 막자는 걸까요?"),
 ("s4","원인A 7-20","통합은 공짜가 아니었습니다. 항만과 플랫폼을 중국 자본이 사들이고, 공장은 대륙 내륙으로 떠납니다."),
 ("s5","원인A2","수혜는 재계로, 청구서는 노동으로 갔습니다. 인천 용접공 박성호 씨의 조선소가 닫혔습니다."),
 ("s6","원인B 20-35","그래서 네 가지 말이 나옵니다. 산업주권, 노동, 문화자율, 외교다변화."),
 ("s7","원인B2","이걸 외치면 기존 질서와 싸우는 겁니다. 그쪽의 이름이, 진보입니다."),
 ("s8","Second Hook 35-45","그래서 이상한 장면이 나옵니다. 노조 집회에 주권 깃발이 걸리고, 재계 신문은 개방을 사설로 씁니다."),
 ("s9","Payoff 45-60","반중은 보수의 유전자가 아닙니다. 의존을 만든 쪽이 지키고, 청구서를 받는 쪽이 저항할 뿐입니다."),
 ("s10","확장 60-67","그런데 정당들이 싸우는 동안, 청년들은 다르게 움직입니다."),
 ("s11","다음 모순 67-70","이 세계의 대학생에겐, 중국 유학이 미국 유학만큼 자연스럽습니다."),
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
