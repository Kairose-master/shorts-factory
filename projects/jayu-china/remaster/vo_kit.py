"""vo_kit — edge-tts 재생성 + WordBoundary 실측 캡처.

lines.json v2 스키마: [{id, seg, dur, text, words:[[word, t, dur], ...]}]
t는 해당 라인 오디오 내 시작초. 칩 스케줄은 chips_from_words()로 산출.
"""
import edge_tts, asyncio, os, wave, json, subprocess
import imageio_ffmpeg

EXE = imageio_ffmpeg.get_ffmpeg_exe()
V = "ko-KR-HyunsuMultilingualNeural"


async def _gen_line(sid, text, outdir, rate="+13%", pitch="-8Hz"):
    mp3 = f"{outdir}/{sid}.mp3"; wav = f"{outdir}/{sid}.wav"
    t = edge_tts.Communicate(text, V, rate=rate, pitch=pitch,
                             boundary="WordBoundary",
                             proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(mp3, "wb") as f:
        async for chunk in t.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append([chunk["text"], round(chunk["offset"]/1e7, 3),
                              round(chunk["duration"]/1e7, 3)])
    subprocess.run([EXE, "-y", "-loglevel", "error", "-i", mp3,
                    "-ar", "24000", "-ac", "1", wav], check=True)
    os.remove(mp3)
    with wave.open(wav) as w:
        dur = w.getnframes()/w.getframerate()
    return round(dur, 2), words


def generate(LINES, outdir):
    """LINES: [(sid, seg, text)] → wav + lines.json(v2). 총 길이 반환."""
    os.makedirs(outdir, exist_ok=True)
    async def run():
        plan = []
        for sid, seg, text in LINES:
            dur, words = await _gen_line(sid, text, outdir)
            plan.append({"id": sid, "seg": seg, "dur": dur, "text": text, "words": words})
            print(f"{sid} {dur:5.2f}s w{len(words)} [{seg}] {text[:30]}")
        json.dump(plan, open(f"{outdir}/lines.json", "w"), indent=1, ensure_ascii=False)
        total = sum(p["dur"] for p in plan)
        print(f"narration {total:.1f}s")
        return total
    return asyncio.run(run())


def chips_from_words(entry, max_chars=15, tail=0.35):
    """lines.json 항목 → [(chip_text, start, dur)] — WordBoundary 실측 타이밍.

    단어를 max_chars 이하 구로 묶되 문장부호(쉼표/마침표/물음표) 뒤에서 우선 절단.
    각 칩 시작 = 첫 단어 offset, 길이 = 다음 칩 시작(또는 마지막 단어 끝+tail)까지.
    """
    words = entry.get("words") or []
    if not words:                       # 폴백: 글자수 비례 (v1 방식)
        return None
    groups, cur, cur_len = [], [], 0
    for w, t, dur in words:
        pause = cur and (t - (cur[-1][1] + cur[-1][2])) > 0.22
        if cur and (cur_len + len(w) + 1 > max_chars or pause or
                    cur[-1][0][-1:] in ".,?!…"):
            groups.append(cur); cur, cur_len = [], 0
        cur.append((w, t, dur)); cur_len += len(w) + 1
    if cur: groups.append(cur)
    sched = []
    for gi, g in enumerate(groups):
        start = g[0][1]
        end = (groups[gi+1][0][1] if gi+1 < len(groups)
               else g[-1][1] + g[-1][2] + tail)
        txt = " ".join(w for w, _, _ in g)
        sched.append((txt, round(start, 3), round(end-start, 3)))
    return sched
