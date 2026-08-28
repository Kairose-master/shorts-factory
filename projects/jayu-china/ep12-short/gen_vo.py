"""EP12 「2080 자유중국 총선 — 당신이라면 누구를 찍겠습니까?」 — 원칙 v1.0 고정 70초 포맷. 시즌1 피날레.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 이 세계 총선에서 유권자의 5표(이슈별 한 표)는
   한 정당에 모이지 않는다 — 좌우 한 줄 투표가 애초에 불가능하다.
② 그것을 만든 인과 (시즌 전체의 결산): 1946 이후 134년의 다른 역사가 이슈마다
   다른 동맹을 만들었다 — 복지=보수(EP2), 민영화=진보(EP3), 반중=진보(EP5),
   영토=회계(EP9), 세대=위치(EP10). 정당들은 좌우 축이 아니라 이슈 축 위에 있다.
③ 다음 편(시즌2)에서 깨뜨릴 상식: "좌우가 이상한 건 이 세계가 이상해서다"
   → 시즌2 「자유중국의 철학」: 왜 우리는 자꾸 한 줄로 세우려 했는가를 묻는다.
   (정본 §13: 결과를 보여준 뒤 질문만 남긴다 — "좌우는 허구다"라고 가르치지 않는다.)
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","당신에게 5표가 주어졌습니다. 현실의 좌우 자는, 버리고 오세요."),
 ("s2","전제 2-7","2080년 자유중국 총선 — 국민당이 이긴 세계의 선거판입니다."),
 ("s3","약속","이슈는 다섯 — 경제, 외교, 복지, 지역, 기술."),
 ("s4","원인A 7-20","경제, 국영 지주회사를 지킬까요 쪼갤까요? 외교, 미국과 손잡을까요 다툴까요?"),
 ("s5","원인A2","여기까지 두 표. 벌써 다른 당을 찍고 있을지도 모릅니다."),
 ("s6","원인B 20-35","복지 — 연금은 성역인가 개혁인가. 지역 — 세금은 난징인가 성인가. 기술 — 인공지능은 누가 규제하나."),
 ("s7","원인B2","다섯 표를 다 던졌다면 세어 보세요. 몇 개의 당에 흩어졌나요?"),
 ("s8","Second Hook 35-45","이 세계 유권자의 표도 똑같이 흩어집니다. 승자는 정당이 아니라 연합입니다."),
 ("s9","Payoff 45-60","134년의 다른 역사가 이슈마다 다른 동맹을 만들었습니다. 좌우 한 줄은 애초에 이 판의 축이 아니었죠."),
 ("s10","확장 60-67","시즌 내내 분류가 실패한 이유가, 이 한 장의 선거판에 있습니다."),
 ("s11","다음 모순 67-70","그런데 왜 우리는 자꾸 한 줄로 세우려 했을까요? 시즌 2에서 그 질문을 엽니다."),
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
