"""EP11 「이 정치인은 좌파입니까, 우파입니까?」 — 원칙 v1.0 고정 70초 포맷. 참여형 분류 게임.

제작 전 세 문장 (원칙 게이트):
① 현실과 가장 반대되는 사실: 이 세계 정치인의 공약 묶음은 현실의 좌우 자로
   10초 안에 분류되지 않는다 (네 명 전원이 반씩 걸친다).
② 그것을 만든 인과 (정본 §5 EP11 + 부록B: '그냥 좌우가 반대인 세계' 금지 —
   역사적으로 다른 coalition이 생성됐다는 점이 핵심): 공약을 묶는 건 이념
   논리가 아니라 역사(전쟁·동맹·산업·세대)→1946 이후 다른 역사가 다른
   동맹 묶음을 낳음→현실 나침반이 고장 나는 이유.
③ 다음 편에서 깨뜨릴 상식: "분류가 안 되면 투표도 못 한다" → EP12 2080
   총선, 당신에게 5표 (정본 엔딩: "분류 말고 실제로 투표하면 어떻게 될까?").
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg
OUT=os.path.join(os.path.dirname(__file__),"vo")
os.makedirs(OUT,exist_ok=True)
EXE=imageio_ffmpeg.get_ffmpeg_exe()
V="ko-KR-HyunsuMultilingualNeural"
LINES=[
 ("s1","WTF 0-2","복지 확대, 시장 개방, 군비 증강. 좌파일까요, 우파일까요?"),
 ("s2","전제 2-7","국민당이 이긴 세계의 선거판, 현실의 나침반은 여기서 고장 납니다."),
 ("s3","약속","정치인 네 명, 직접 분류해 보세요."),
 ("s4","원인A 7-20","1번은 국영 철도를 지키면서 무역 개방을 밀어붙입니다. 2번은 민영화를 외치며 외국 자본 규제를 요구합니다."),
 ("s5","원인A2","벌써 헷갈리죠? 아직 두 명 남았습니다."),
 ("s6","원인B 20-35","3번은 복지 확대와 군비 증강을 같이 공약합니다. 4번은 감세를 주장하면서 재벌 해체를 요구합니다."),
 ("s7","원인B2","네 명 모두, 현실의 좌우 자로는 반씩 걸칩니다."),
 ("s8","Second Hook 35-45","속임수가 아닙니다. 이 조합들은 이 세계에선 전부 자연스러운 동맹입니다."),
 ("s9","Payoff 45-60","공약을 묶는 건 이념의 논리가 아니라 역사입니다. 전쟁과 동맹과 산업이 다르면, 묶음도 다르게 태어납니다."),
 ("s10","확장 60-67","분류가 안 되는 건 여러분 잘못이 아닙니다. 자가, 다른 세계의 자일 뿐이죠."),
 ("s11","다음 모순 67-70","분류 말고, 투표를 해보죠. 다음 편 2080 총선 — 당신에게 5표가 주어집니다."),
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
