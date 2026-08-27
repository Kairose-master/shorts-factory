"""EP6 「미국보다 중국이 더 가까운 한국」 — 원칙 v1.0 고정 70초 포맷.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 한국 청년에게 중국 유학·취업·문화가 미국만큼 자연스럽다.
② 그것을 만든 인과 (정본 §5 EP6: 중국어·철도·유학·취업·문화소비의 생활사):
   대륙 종단 철도가 생활권을 만듦 → 언어(중국어 정규 과목)·취업(대륙 지사=승진 코스)·
   문화(상하이 밴드·항저우 로케)가 노선을 따라감 → 정치의 반중/친중과 무관하게
   생활이 먼저 통합. "정치는 진영을 나누지만 생활은 노선을 따라간다."
③ 다음 편에서 깨뜨릴 상식: "좌파는 군축" → 이 세계 일본에선 좌파가 재무장을 주장 (정본 EP7).

연속성: EP5의 박성호(41, 인천 용접공·규제 집회) 가족을 재등장 — 딸 박지은(24)의
난징 면접. 세대 층위 반박(EP5 적대 검수에서 유보한 것)을 이 편이 회수한다.
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","이 세계 청년에겐, 중국 유학이 미국 유학만큼 자연스럽습니다."),
 ("s2","전제 2-7","국민당이 이긴 세계, 밤기차 하나로 난징인 한국이니까요."),
 ("s3","약속","정치는 싸우는데, 생활은 왜 이럴까요?"),
 ("s4","원인A 7-20","국경이 아니라 노선입니다. 부산발 대륙 열차가 매일 밤 떠나고, 방학이면 좌석이 동납니다."),
 ("s5","원인A2","언어도 노선을 따랐습니다. 중국어는 제2외국어가 아니라 초등학교 정규 과목입니다."),
 ("s6","원인B 20-35","일자리도 그렇습니다. 대륙 지사 발령은 좌천이 아니라 승진 코스입니다."),
 ("s7","원인B2","차트엔 상하이 밴드가 있고, 주말 드라마는 항저우에서 찍습니다."),
 ("s8","Second Hook 35-45","그래서 이런 저녁이 있습니다. 아버지 박성호 씨는 규제 집회에 다녀오고, 딸 지은 씨는 난징 면접을 준비합니다. 같은 식탁에서요."),
 ("s9","Payoff 45-60","청년이 친중이라서가 아닙니다. 정치는 진영을 나누지만, 생활은 노선을 따라갑니다. 지도가 바뀌면 일상이 먼저 바뀝니다."),
 ("s10","확장 60-67","그런데 같은 지도를 받은 나라가, 정반대로 움직였습니다."),
 ("s11","다음 모순 67-70","이 세계의 일본에선, 좌파가 재무장을 외칩니다."),
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
