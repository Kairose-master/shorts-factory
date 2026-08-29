#!/usr/bin/env python3
"""나레이션 쇼츠 렌더러 (기둥 A·B·C·D·F).

소스 영상이 필요 없다. 대본 · Piper 한국어 TTS · 텍스트 모션만으로 완성한다.
기둥 E(설교 클립)는 build_short.py 가 맡는다.

색 문법은 build_short.py 와 같고, 그 이유도 같다:

  흰색   EDITORIAL · RECONSTRUCTED  — 오피스의 목소리
  노란색 QUOTE                      — 목사님이 실제로 한 말

**RECONSTRUCTED 가 흰색인 것은 실수가 아니다.** 설교자의 논증을 오피스가
자기 말로 옮긴 것이므로 화면에서 말하는 주체는 오피스다. 노란색은 음성 대조를
통과한 실제 발화에만 쓴다. 이 대본에 QUOTE 줄이 있는데 음성 대조 증거가
없으면 렌더를 거부한다.

사용법:
  python3 build_narration.py --shorts-id SS-001 \
      --hook "3천 년 전 이스라엘이|가장 듣기 싫었을 명령"
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OFFICE = ROOT / "sermon-office"

W, H = 1080, 1920
FONT = "Noto Sans CJK KR"
WHITE, YELLOW, BLACK = "&H00FFFFFF", "&H0000E0FF", "&H00000000"

HOOK_SIZE, HOOK_MARGIN_TOP, HOOK_OUTLINE = 104, 155, 7
BODY_SIZE, BODY_OUTLINE = 76, 6
BODY_LINE_CHARS, BODY_MAX_LINES = 15, 4
BODY_Y = 900             # 본문 세로 중심
CITE_SIZE, CITE_Y = 62, 1250
ATTR_SIZE, ATTR_Y = 40, 1400
DISC_SIZE, DISC_Y = 34, 1452
# 유튜브 UI 가 81.7%(y=1568) 아래를 덮는다. 모든 요소가 그 위에 있어야 한다.
UI_SAFE_BOTTOM = 1568
PROGRESS_Y, PROGRESS_W, PROGRESS_H = 1500, 756, 8
END_LEAD_SIZE, END_MAIN_SIZE, END_SUB_SIZE = 50, 76, 50
END_Y = 880
GAP_MS = 260              # 문장 사이 숨
LEAD_IN_MS = 350          # 첫 문장 전 여백

VOICE_DIR = Path(__file__).resolve().parent / "voices"


def die(m):
    sys.exit(f"오류: {m}")


def ass_time(ms):
    ms = max(0, int(ms)); h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000); s, cs = divmod(r, 1000)
    return f"{h}:{m:02d}:{s:02d}.{cs // 10:02d}"


def wrap(text, width, max_lines):
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if len(cand) <= width or not cur:
            cur = cand
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines - 1] + [" ".join(lines[max_lines - 1:])]
    return r"\N".join(lines)


def parse_script(path):
    """'## 대본' 절에서 [등급 · 근거] 문장 을 읽는다.

    verify_sermon_office.py 가 강제하는 형식과 같다. 형식이 하나뿐이어야
    검증기와 렌더러가 같은 것을 본다.
    """
    if not path.is_file():
        die(f"대본이 없습니다: {path}")
    out, inside = [], False
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## 대본"):
            inside = True; continue
        if inside and line.startswith("## "):
            break
        s = line.strip()
        if not inside or not s or s.startswith(("|", ">", "-", "#", "`")):
            continue
        m = re.match(r"\[(QUOTE|RECONSTRUCTED|EDITORIAL)([^\]]*)\]\s*(.+)", s)
        if not m:
            die(f"{path}:{i}: 자세 등급이 없는 대본 줄 — 근거 없는 주장")
        out.append({"posture": m.group(1), "ref": m.group(2).strip(" ·"),
                    "text": m.group(3).strip(), "line": i})
    if not out:
        die(f"{path}: '## 대본' 절을 찾지 못했습니다")
    return out


def make_endcard(sermon_id, seconds):
    """엔드카드 내용을 설교 meta.json 에서 만든다. build_short.py 와 같은 규칙."""
    if seconds <= 0 or not sermon_id:
        return None
    mp = OFFICE / "sermons" / sermon_id / "meta.json"
    if not mp.is_file():
        die(f"엔드카드를 만들 meta.json 이 없습니다: {mp}")
    m = json.loads(mp.read_text(encoding="utf-8"))
    date = m.get("date") or ""
    if date:
        y, mo, d = date.split("-")
        date = f"{y}년 {int(mo)}월 {int(d)}일"
    main = " ".join(x for x in (date, m.get("service_type") or "") if x) or m.get("title_raw", "")
    sub = " · ".join(x for x in (m.get("scripture"), m.get("preacher")) if x)
    return {"ms": int(seconds * 1000), "main": main, "sub": sub, "church": "방배동 예심교회"}


def wav_ms(p):
    with wave.open(str(p)) as w:
        return int(w.getnframes() / w.getframerate() * 1000)


def synth(lines, outdir, model, length_scale=1.0):
    """문장마다 WAV 하나. 길이가 곧 그 문장의 화면 체류 시간이 된다."""
    wavs = []
    for i, ln in enumerate(lines):
        p = outdir / f"n{i:02d}.wav"
        r = subprocess.run([sys.executable, "-m", "piper", "--model", str(model),
                            "--length-scale", f"{length_scale}", "--output_file", str(p)],
                           input=ln["text"], text=True, capture_output=True)
        if r.returncode != 0 or not p.is_file():
            die("Piper 합성 실패\n" + r.stderr[-800:])
        wavs.append(p)
        ln["dur"] = wav_ms(p)
    return wavs


def build_ass(hook_lines, lines, total_ms, attribution="", disclosure="", endcard=None):
    hook = r"\N".join(hook_lines)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HOOK,{FONT},{HOOK_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,-1,0,1,{HOOK_OUTLINE},4,8,60,60,{HOOK_MARGIN_TOP},1
Style: BODY,{FONT},{BODY_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,{BODY_OUTLINE},3,5,110,110,0,1
Style: BODYQ,{FONT},{BODY_SIZE},{YELLOW},{YELLOW},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,{BODY_OUTLINE},3,5,110,110,0,1
Style: CITE,{FONT},{CITE_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,3,0,1,5,2,5,110,110,0,1
Style: ENDLEAD,{FONT},{END_LEAD_SIZE},&H30FFFFFF,&H30FFFFFF,{BLACK},{BLACK},0,0,0,0,100,100,2,0,1,4,0,5,90,90,0,1
Style: ENDMAIN,{FONT},{END_MAIN_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,6,3,5,90,90,0,1
Style: ENDSUB,{FONT},{END_SUB_SIZE},&H18FFFFFF,&H18FFFFFF,{BLACK},{BLACK},0,0,0,0,100,100,1,0,1,4,0,5,90,90,0,1
Style: ATTR,{FONT},{ATTR_SIZE},&H80FFFFFF,&H80FFFFFF,{BLACK},{BLACK},0,0,0,0,100,100,1,0,1,3,0,5,80,80,0,1
Style: DISC,{FONT},{DISC_SIZE},&HA0FFFFFF,&HA0FFFFFF,{BLACK},{BLACK},0,0,0,0,100,100,1,0,1,3,0,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 0,{ass_time(0)},{ass_time(total_ms)},HOOK,,0,0,0,,"
          f"{{\\fad(220,0)}}{hook}"]
    if attribution:
        ev.append(f"Dialogue: 0,{ass_time(600)},{ass_time(total_ms)},ATTR,,0,0,0,,"
                  f"{{\\pos(540,{ATTR_Y})\\fad(500,0)}}{attribution}")
    if disclosure:
        # DO NOT CLAIM 9 — 합성 나레이션을 목사님 음성인 것처럼 제시하지 않는다.
        # 출처에 설교자 이름이 있으면 시청자는 들리는 목소리를 그 사람으로 읽는다.
        ev.append(f"Dialogue: 0,{ass_time(600)},{ass_time(total_ms)},DISC,,0,0,0,,"
                  f"{{\\pos(540,{DISC_Y})\\fad(500,0)}}{disclosure}")
    if endcard:
        es, ee = total_ms, total_ms + endcard["ms"]
        ev.append(f"Dialogue: 3,{ass_time(es)},{ass_time(ee)},ENDLEAD,,0,0,0,,"
                  f"{{\\pos(540,{END_Y - 130})\\fad(300,0)}}원본 설교 전체는 채널에 있습니다")
        ev.append(f"Dialogue: 3,{ass_time(es + 120)},{ass_time(ee)},ENDMAIN,,0,0,0,,"
                  f"{{\\pos(540,{END_Y})\\fad(300,0)}}{endcard['main']}")
        ev.append(f"Dialogue: 3,{ass_time(es + 240)},{ass_time(ee)},ENDSUB,,0,0,0,,"
                  f"{{\\pos(540,{END_Y + 120})\\fad(300,0)}}{endcard['sub']}")
        ev.append(f"Dialogue: 3,{ass_time(es + 240)},{ass_time(ee)},ENDSUB,,0,0,0,,"
                  f"{{\\pos(540,{END_Y + 200})\\fad(300,0)}}{endcard['church']}")
    t = LEAD_IN_MS
    for ln in lines:
        end = t + ln["dur"]
        style = "BODYQ" if ln["posture"] == "QUOTE" else "BODY"
        body = wrap(ln["text"], BODY_LINE_CHARS, BODY_MAX_LINES)
        ev.append(f"Dialogue: 1,{ass_time(t)},{ass_time(end)},{style},,0,0,0,,"
                  f"{{\\pos(540,{BODY_Y})\\fad(160,160)}}{body}")
        # 성경 장·절이 문장에 나오면 하단에 인용 표시를 띄운다. 시청자가
        # 확인할 수 있어야 한다(제작 SOP 기본값).
        cite = re.search(r"(에스겔|겔)\s*\d+장?\s*\d+절?", ln["text"])
        if cite:
            ev.append(f"Dialogue: 2,{ass_time(t)},{ass_time(end + 900)},CITE,,0,0,0,,"
                      f"{{\\pos(540,{CITE_Y})\\fad(200,300)}}{cite.group(0)}")
        t = end + GAP_MS
    return head + "\n".join(ev) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shorts-id", required=True)
    ap.add_argument("--hook", required=True, help="상단 훅. '|' 로 줄바꿈, 최대 2줄")
    ap.add_argument("--model", default=str(VOICE_DIR / "ko_KR-kss-medium.onnx"))
    ap.add_argument("--sermon", default="", help="설교 id. 비우면 plan.md 에서 찾는다")
    ap.add_argument("--endcard", type=float, default=3.5,
                    help="끝에 붙일 원본 설교 안내 카드 길이(초). 0 이면 끄기")
    ap.add_argument("--length-scale", type=float, default=1.0,
                    help="Piper 발화 길이. 1.0 미만이면 빨라진다 (0.9 권장 하한)")
    ap.add_argument("--attribution", default="", help="하단 출처 표기. 비우면 meta.json 에서 생성")
    ap.add_argument("--disclosure", default="나레이션은 AI 합성 음성입니다 · 방배동 예심교회",
                    help="합성 음성 고지. DO NOT CLAIM 9. 비우려면 명시적으로 빈 문자열")
    ap.add_argument("--frames", default="", help="미리보기 프레임 초 (쉼표 구분)")
    a = ap.parse_args()

    if not shutil.which("ffmpeg"):
        die("ffmpeg 가 없습니다")
    model = Path(a.model)
    if not model.is_file():
        die(f"Piper 음성 모델이 없습니다: {model}\n"
            f"       ko_KR-kss-medium 을 {VOICE_DIR} 에 두세요.")

    hook_lines = [x.strip() for x in a.hook.split("|") if x.strip()]
    if not 1 <= len(hook_lines) <= 2:
        die("훅은 1–2줄입니다")

    base = OFFICE / "production" / a.shorts_id
    lines = parse_script(base / "script.md")

    # QUOTE 줄이 있으면 음성 대조 증거를 요구한다.
    if any(l["posture"] == "QUOTE" for l in lines):
        if not (base / "captions" / "captions-verified.json").is_file():
            die("대본에 QUOTE 줄이 있는데 captions/captions-verified.json 이 없습니다.\n"
                "       음성 대조 전에는 목사님의 말이라고 화면에 주장할 수 없습니다.")

    outdir = base / "renders"; outdir.mkdir(parents=True, exist_ok=True)
    audio = outdir / "narration"; audio.mkdir(exist_ok=True)
    capdir = base / "captions"; capdir.mkdir(exist_ok=True)

    print(f"나레이션 합성 — {len(lines)}문장")
    wavs = synth(lines, audio, model, a.length_scale)
    total = LEAD_IN_MS + sum(l["dur"] + GAP_MS for l in lines) + 700

    attribution = a.attribution
    if not attribution:
        refs = [l["ref"] for l in lines if l["ref"]]
        sermon = refs[0].split()[0] if refs else ""
        meta_p = None
        for d in (OFFICE / "sermons").glob("*/meta.json"):
            meta_p = d
            try:
                m = json.loads(d.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if m.get("sermon_id") and m["sermon_id"] in (base / "plan.md").read_text(
                    encoding="utf-8"):
                attribution = (f"{m.get('preacher','')} 설교 「{m.get('scripture','')}」"
                               f" {m.get('date','')} 에서 재구성")
                break
    sermon_id = a.sermon
    if not sermon_id:
        plan = (base / "plan.md").read_text(encoding="utf-8")
        for d in sorted((OFFICE / "sermons").iterdir()):
            if d.is_dir() and d.name in plan:
                sermon_id = d.name
                break
    endcard = make_endcard(sermon_id, a.endcard)
    ass = capdir / "narration.ass"
    ass.write_text(build_ass(hook_lines, lines, total, attribution, a.disclosure, endcard),
                   encoding="utf-8")

    # 문장 사이 무음을 넣어 이어붙인다
    concat = audio / "concat.txt"
    sil = audio / "gap.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-f", "lavfi", "-t", f"{GAP_MS/1000}",
                    "-i", "anullsrc=r=22050:cl=mono", str(sil)], capture_output=True)
    lead = audio / "lead.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-f", "lavfi", "-t", f"{LEAD_IN_MS/1000}",
                    "-i", "anullsrc=r=22050:cl=mono", str(lead)], capture_output=True)
    parts = [lead]
    for w in wavs:
        parts += [w, sil]
    concat.write_text("\n".join(f"file '{p.name}'" for p in parts) + "\n", encoding="utf-8")
    voice = audio / "voice.wav"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(concat), "-ar", "44100", "-ac", "1", str(voice)],
                       capture_output=True, text=True, cwd=str(audio))
    if r.returncode != 0:
        die("오디오 결합 실패\n" + r.stderr[-800:])

    # 배경: 짙은 남색 그라디언트에 아주 느린 확대. 첫 500ms 안에 움직임이 있어야
    # 한다(제작 SOP 기본값) — 훅의 페이드인과 이 확대가 그 역할을 한다.
    dur_s = (total + (endcard["ms"] if endcard else 0)) / 1000
    body_s = total / 1000
    bg = (f"gradients=s={W}x{H}:c0=0x2A4A7F:c1=0x0B1020:c2=0x1A2C4E:"
          f"x0=200:y0=0:x1=900:y1={H}:nb_colors=3:d={dur_s:.2f}:speed=0.015:r=30,"
          f"format=yuv420p")
    # 진행바는 흰색이다. 노란색은 QUOTE 전용이므로 장식에 쓰지 않는다.
    px = (W - PROGRESS_W) // 2
    # gradients 를 30fps 로 만들고 zoompan 도 30fps 로 둔다. 소스가 25fps 이면
    # zoompan 이 프레임 수를 그대로 두고 fps 만 바꿔 영상이 짧아진다.
    vf = (f"zoompan=z='min(zoom+0.00018,1.08)':d=1:s={W}x{H}:fps=30,"
          f"drawbox=x={px}:y={PROGRESS_Y}:w={PROGRESS_W}:h={PROGRESS_H}:"
          f"color=white@0.16:t=fill,"
          f"drawbox=x={px}:y={PROGRESS_Y}:w='{PROGRESS_W}*min(t/{body_s:.3f},1)':"
          f"h={PROGRESS_H}:color=white@0.5:t=fill,"
          + (f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill:"
             f"enable='gte(t,{body_s:.3f})'," if endcard else "")
          +
          f"subtitles='{ass}':fontsdir=/usr/share/fonts")

    target = outdir / "final.mp4"
    cmd = ["ffmpeg", "-hide_banner", "-y",
           "-f", "lavfi", "-t", f"{dur_s:.3f}", "-i", bg,
           "-i", str(voice), "-vf", vf, "-af",
           (f"apad=pad_dur={a.endcard}" if endcard else "anull"), "-r", "30",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-t", f"{dur_s:.3f}",
           "-movflags", "+faststart", str(target)]
    print("렌더:", target)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        die("ffmpeg 실패\n" + r.stderr[-1800:])

    for sec in [x.strip() for x in a.frames.split(",") if x.strip()]:
        f = outdir / f"preview-{sec.replace('.', '_')}s.jpg"
        subprocess.run(["ffmpeg", "-hide_banner", "-y", "-ss", sec, "-i", str(target),
                        "-frames:v", "1", "-q:v", "3", str(f)], capture_output=True)
        print("  프레임:", f)

    (capdir / "narration-manifest.json").write_text(json.dumps(
        {"shorts_id": a.shorts_id, "engine": "build_narration",
         "voice": model.name, "length_scale": a.length_scale,
         "total_ms": total, "sentences": len(lines),
         "postures": sorted({l["posture"] for l in lines}),
         "attribution": attribution, "disclosure": a.disclosure,
         "lines": [{"line": l["line"], "posture": l["posture"], "ref": l["ref"],
                    "dur_ms": l["dur"], "text": l["text"]} for l in lines]},
        ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\n  길이 {dur_s:.1f}초 · {len(lines)}문장 · {W}x{H}")
    print(f"  음성 {model.name} (합성). 목사님 음성이 아니며 그렇게 제시하지 않는다.")


if __name__ == "__main__":
    main()
