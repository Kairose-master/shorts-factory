#!/usr/bin/env python3
"""설교 클립 → 9:16 쇼츠 렌더러 (기둥 E).

레이아웃 규격: sermon-office/brand/shorts-format.md
갓피플TV(@GODpeopleTV) 벤치마크 실측과 레퍼런스 스크린샷 좌표 측정에서 나왔다.

  상단  대형 흰색 훅 2줄 (EDITORIAL — 제작자의 목소리)
  중앙  설교 영상 풀블리드 9:16 크롭
  하단  노란 자막 (QUOTE — 목사님의 말, 음성 대조 필요)

두 층의 색이 다른 것은 디자인이 아니라 **자세 등급의 시각적 구현**이다.
흰 글씨는 오피스가 쓴 것이고, 노란 글씨는 목사님이 말한 것이다.

사용법:
  # 본편 렌더
  python3 sermon-office/production/_engine/build_short.py \
      --sermon S-20260828-EZK47 --shorts-id SS-004 \
      --in 41:33.04 --out 42:32.12 \
      --hook "먼저 믿은 게|우월이 되는 순간" \
      --source /path/to/sermon.mp4

  # 음성 대조용 클립 (사람이 60초 듣고 자막이 맞는지 확인)
  python3 ... --verify

  # 소스 영상 없이 레이아웃만 확인 (정지화면)
  python3 ... --still /path/to/frame.jpg
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OFFICE = ROOT / "sermon-office"

W, H = 1080, 1920
FONT = "Noto Sans CJK KR"

# ── 레이아웃 상수. 전부 sermon-office/brand/shorts-format.md 의 실측에서 온다.
HOOK_SIZE = 116          # 레퍼런스 제목 글자 높이 5.4% × 1920, 한글 자면 보정
HOOK_MARGIN_TOP = 155    # 8.1% — 레퍼런스 제목 1행 상단 8.7% 보다 살짝 위
HOOK_OUTLINE = 7
HOOK_SHADOW = 4
CAP_SIZE = 64
CAP_MARGIN_BOTTOM = 422  # 자막 하단이 78% 지점. 유튜브 채널행(81.7%) 위
CAP_MARGIN_SIDE = 130    # 좌우 12% — 우측 액션 버튼 열을 피한다
CAP_OUTLINE = 6
STATUS_SIZE, STATUS_MARGIN = 34, 352   # 자막 검수 상태 라벨, 자막 위
CAP_LINE_CHARS = 17      # 한글 기준 한 줄 최대 글자수
CAP_GROUP_CHARS = 36     # 자막 한 덩어리 최대 글자수 (17자 × 2줄)
CAP_GROUP_MS = 5000      # 자막 한 덩어리 최대 지속
CAP_MAX_LINES = 2

# ASS 색상은 &HAABBGGRR. 노란색 #FFE000 → BGR 00E0FF
YELLOW = "&H0000E0FF"
WHITE = "&H00FFFFFF"
BLACK = "&H00000000"


def die(msg):
    sys.exit(f"오류: {msg}")


def parse_tc(s):
    """'41:33.04' 또는 '2493040'(ms) 또는 '41:33' → ms"""
    s = str(s).strip()
    if re.fullmatch(r"\d+", s):
        return int(s)
    m = re.fullmatch(r"(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)", s)
    if not m:
        die(f"타임코드를 읽을 수 없음: {s!r} (예: 41:33.04, 1:02:15, 2493040)")
    h, mm, ss = m.group(1) or 0, m.group(2), m.group(3)
    return int((int(h) * 3600 + int(mm) * 60 + float(ss)) * 1000)


def ass_time(ms):
    ms = max(0, int(ms))
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, cs = divmod(r, 1000)
    return f"{h}:{m:02d}:{s:02d}.{cs // 10:02d}"


def wrap(text, width=CAP_LINE_CHARS, max_lines=CAP_MAX_LINES):
    """어절 단위로 감싼다. 줄 수를 넘으면 뒤를 버리지 않고 마지막 줄에 몰아넣는다."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if len(cand) <= width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines - 1] + [" ".join(lines[max_lines - 1:])]
    return r"\N".join(lines)


def clean_cue(text):
    """ASR 마커를 지운다. 화면에 [목을 가다듬음] 이 나가면 안 된다."""
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = text.replace(">>", " ")
    return re.sub(r"\s+", " ", text).strip()


def load_cues(sermon_id, start_ms, end_ms):
    p = OFFICE / "sermons" / sermon_id / "transcript.json"
    if not p.is_file():
        die(f"자막이 없음: {p}")
    cues = json.loads(p.read_text(encoding="utf-8"))["transcript"]
    out = []
    for c in cues:
        s, e = int(c["startMs"]), int(c["endMs"])
        if e <= start_ms or s >= end_ms:
            continue
        t = clean_cue(c["text"])
        if t:
            out.append((max(s, start_ms) - start_ms, min(e, end_ms) - start_ms, t))
    # ASR 큐는 서로 겹친다. 다음 큐가 시작하면 앞 큐를 끝낸다.
    for i in range(len(out) - 1):
        out[i] = (out[i][0], min(out[i][1], out[i + 1][0]), out[i][2])
    out = [(s, e, t) for s, e, t in out if e - s > 200]
    return group_cues(out)


def group_cues(cues):
    """ASR 큐를 어절 단위로 잘라 문장에 가깝게 다시 묶는다.

    원본 큐는 2초 단위로 기계적으로 끊겨서 '사람들은 믿음 안 가진 사람들 / 보면'
    처럼 문장 중간에서 갈라진다. 화면에 그대로 나가면 읽기 어렵고, 무엇보다
    잘린 조각이 인용처럼 보인다. 문장부호와 길이로 다시 묶는다.
    """
    groups, buf = [], None
    for s, e, t in cues:
        if buf is None:
            buf = [s, e, t]
            continue
        merged = f"{buf[2]} {t}".strip()
        # 종결은 문장부호로만 판단한다. '믿었다고 해' 의 '해' 처럼 어간이
        # 문장 끝처럼 보이는 경우가 많아, 음절로 판단하면 문장을 더 잘게 부순다.
        ends = buf[2].rstrip().endswith((".", "?", "!"))
        too_long = len(merged) > CAP_GROUP_CHARS or (e - buf[0]) > CAP_GROUP_MS
        if ends or too_long:
            groups.append(tuple(buf))
            buf = [s, e, t]
        else:
            buf = [buf[0], e, merged]
    if buf:
        groups.append(tuple(buf))
    return groups


def write_caption_tsv(path, cues):
    """사람이 고칠 자막 초안. 시작ms · 종료ms · 텍스트, 탭 구분.

    ASR 원문에는 실언과 반복이 그대로 남는다("이게 참 이게 참 되게에 참").
    벤치마크 채널의 자막이 깨끗한 것은 사람이 다듬기 때문이다. 이 파일을
    고쳐서 --captions 로 되돌려 주면 그때 QUOTE 등급이 된다.
    """
    lines = ["# 시작ms\t종료ms\t자막  — 고친 뒤 --captions 로 넘기세요.",
             "# 음성을 들으면서 고칩니다. 그 행위가 곧 음성 대조입니다.",
             "# 지울 행은 텍스트를 비우지 말고 행 전체를 지우세요."]
    lines += [f"{s}\t{e}\t{t}" for s, e, t in cues]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_caption_tsv(path):
    if not path.is_file():
        die(f"자막 파일이 없습니다: {path}")
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            die(f"{path}:{i}: 탭으로 구분된 3개 필드가 필요합니다")
        try:
            s, e = int(parts[0]), int(parts[1])
        except ValueError:
            die(f"{path}:{i}: 시작/종료가 정수 ms 가 아닙니다")
        txt = "\t".join(parts[2:]).strip()
        if txt:
            out.append((s, e, txt))
    return out


def scale_cues(cues, speed):
    """배속을 걸면 자막 타이밍도 같은 비율로 당겨야 한다."""
    if speed == 1.0:
        return cues
    return [(int(s / speed), int(e / speed), t) for s, e, t in cues]


def build_ass(hook_lines, cues, duration_ms, verify=False, status=""):
    hook = r"\N".join(hook_lines)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HOOK,{FONT},{HOOK_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,-1,0,1,{HOOK_OUTLINE},{HOOK_SHADOW},8,60,60,{HOOK_MARGIN_TOP},1
Style: CAP,{FONT},{CAP_SIZE},{YELLOW},{YELLOW},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,{CAP_OUTLINE},2,2,{CAP_MARGIN_SIDE},{CAP_MARGIN_SIDE},{CAP_MARGIN_BOTTOM},1
Style: STATUS,{FONT},{STATUS_SIZE},&H90FFFFFF,&H90FFFFFF,{BLACK},{BLACK},0,0,0,0,100,100,1,0,1,3,0,2,{CAP_MARGIN_SIDE},{CAP_MARGIN_SIDE},{STATUS_MARGIN},1
Style: VERIFY,{FONT},44,&H0000FFFF,&H0000FFFF,{BLACK},{BLACK},0,0,0,0,100,100,0,0,1,4,0,7,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    if not verify:
        ev.append(f"Dialogue: 0,{ass_time(0)},{ass_time(duration_ms)},HOOK,,0,0,0,,{hook}")
        if status:
            # 자막이 아직 음성 대조를 통과하지 못했다는 표시. 노란 글씨는 "목사님이
            # 이렇게 말했다"는 주장이므로, 검수 전에는 그 주장에 단서를 단다.
            ev.append(f"Dialogue: 0,{ass_time(0)},{ass_time(duration_ms)},STATUS,,0,0,0,,{status}")
    for s, e, t in cues:
        ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},CAP,,0,0,0,,{wrap(t)}")
        if verify:
            ev.append(f"Dialogue: 1,{ass_time(s)},{ass_time(e)},VERIFY,,0,0,0,,"
                      f"{ass_time(s)}  자막이 실제 발화와 같은가?")
    return head + "\n".join(ev) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sermon", required=True, help="설교 id, 예: S-20260828-EZK47")
    ap.add_argument("--shorts-id", required=True, help="쇼츠 id, 예: SS-004")
    ap.add_argument("--in", dest="tin", required=True, help="시작 타임코드")
    ap.add_argument("--out", dest="tout", required=True, help="종료 타임코드")
    ap.add_argument("--hook", default="", help="상단 훅. '|' 로 줄바꿈")
    ap.add_argument("--source", help="원본 설교 mp4")
    ap.add_argument("--still", help="소스 영상 대신 정지화면")
    ap.add_argument("--audio-from", help="정지화면 렌더에 이 파일의 해당 구간 오디오를 쓴다")
    ap.add_argument("--captions", help="사람이 교정한 자막 TSV. 주면 QUOTE 등급으로 렌더")
    ap.add_argument("--verify", action="store_true",
                    help="음성 대조용 클립 — 훅 없이 자막과 타임코드만")
    ap.add_argument("--source-crop", default="",
                    help="9:16 으로 채우기 전에 소스에서 잘라낼 영역 W:H:X:Y")
    ap.add_argument("--crop-x", type=float, default=0.5,
                    help="9:16 크롭의 가로 위치. 0.0 왼쪽 · 0.5 가운데 · 1.0 오른쪽")
    ap.add_argument("--no-loudnorm", dest="loudnorm", action="store_false",
                    help="음량 정규화를 끈다 (기본은 켬, 목표 -14 LUFS)")
    ap.add_argument("--scrim", type=float, default=0.0,
                    help="글자 가독성을 위한 검은 명암막 불투명도 0.0-0.6")
    ap.add_argument("--speed", type=float, default=1.0,
                    help="배속. 1.45 면 88초가 61초가 된다. 음높이는 유지된다")
    ap.add_argument("--frames", default="", help="미리보기 프레임을 뽑을 초 (쉼표 구분)")
    a = ap.parse_args()

    if not shutil.which("ffmpeg"):
        die("ffmpeg 가 없습니다. apt-get install -y ffmpeg")
    if not a.source and not a.still:
        die("--source 또는 --still 중 하나가 필요합니다.\n"
            "       이 컨테이너는 YouTube 다운로드가 차단되어 있습니다. 원본 파일은\n"
            "       채널 소유자가 YouTube Studio 에서 내려받아 --source 로 넘겨주세요.")

    start, end = parse_tc(a.tin), parse_tc(a.tout)
    if end <= start:
        die("--out 이 --in 보다 뒤여야 합니다")
    dur_ms = end - start
    dur_s = dur_ms / 1000

    hook_lines = [x.strip() for x in a.hook.split("|") if x.strip()] or ["", ""]
    if len(hook_lines) > 2:
        die("훅은 최대 2줄입니다 (레퍼런스 실측). 지금 %d줄" % len(hook_lines))

    base = OFFICE / "production" / a.shorts_id
    outdir = base / "renders"        # 바이너리 — gitignore
    capdir = base / "captions"       # 텍스트 증거 — 커밋된다
    outdir.mkdir(parents=True, exist_ok=True)
    capdir.mkdir(parents=True, exist_ok=True)

    if a.captions:
        cues, verified = read_caption_tsv(Path(a.captions)), True
    else:
        cues, verified = load_cues(a.sermon, start, end), False
        draft = capdir / "captions-draft.tsv"
        write_caption_tsv(draft, cues)
    if not cues:
        die("해당 구간에 자막 큐가 없습니다")
    ass = capdir / ("verify.ass" if a.verify else "captions.ass")
    status = "" if (verified or a.verify) else "자동 자막 · 검수 전"
    out_ms = int(dur_ms / a.speed)
    ass.write_text(build_ass(hook_lines, scale_cues(cues, a.speed), out_ms, a.verify, status),
                   encoding="utf-8")

    target = outdir / ("verify.mp4" if a.verify else "final.mp4")
    # 16:9 → 9:16: 높이에 맞춰 키운 뒤 가운데를 잘라낸다. 인물이 중앙에 있는
    # 강단 영상이라 가운데 크롭이 곧 인물 크롭이다.
    speed_v = f"setpts=PTS/{a.speed}," if a.speed != 1.0 else ""
    # 교회 업로드에는 흰 여백·워터마크 띠가 붙는 경우가 많다. 9:16 로 채우기 전에
    # 먼저 실제 화면 영역만 잘라낸다.
    pre = f"crop={a.source_crop}," if a.source_crop else ""
    # 9:16 크롭 위치. 0.5 가 가운데, 0.0 이 왼쪽 끝.
    cx = "(iw-ow)/2" if a.crop_x == 0.5 else f"(iw-ow)*{a.crop_x}"
    scrim = (f",drawbox=x=0:y=0:w=iw:h=ih:color=black@{a.scrim}:t=fill"
             if a.scrim > 0 else "")
    vf = (f"{pre}scale=-2:{H}:flags=lanczos,crop={W}:{H}:{cx}:0{scrim},{speed_v}"
          f"subtitles='{ass}':fontsdir=/usr/share/fonts")
    # atempo 는 0.5–2.0 만 받는다. 그 밖은 연쇄한다.
    af, rem = "", a.speed
    while rem > 2.0:
        af += "atempo=2.0,"; rem /= 2.0
    while rem < 0.5:
        af += "atempo=0.5,"; rem /= 0.5
    af += f"atempo={rem:.4f}"
    # 설교 녹음은 대개 조용하다. 쇼츠 피드에서 다른 영상과 음량이 맞아야 한다.
    if a.loudnorm:
        af += ",loudnorm=I=-14:TP=-1.5:LRA=11"

    if a.still:
        cmd = ["ffmpeg", "-hide_banner", "-y", "-loop", "1", "-t", f"{dur_s:.3f}",
               "-i", a.still]
        if a.audio_from:
            cmd += ["-ss", f"{start/1000:.3f}", "-t", f"{dur_s:.3f}", "-i", a.audio_from]
        cmd += ["-vf", vf, "-r", "30", "-c:v", "libx264",
                "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p"]
        if a.audio_from:
            cmd += ["-af", af, "-c:a", "aac", "-b:a", "160k", "-map", "0:v", "-map", "1:a",
                    "-shortest"]
        cmd += ["-movflags", "+faststart", str(target)]
    else:
        cmd = ["ffmpeg", "-hide_banner", "-y", "-ss", f"{start/1000:.3f}",
               "-t", f"{dur_s:.3f}", "-i", a.source, "-vf", vf, "-af", af,
               "-c:v", "libx264", "-preset", "medium", "-crf", "20",
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
               "-movflags", "+faststart", str(target)]

    print("렌더:", target)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        die("ffmpeg 실패\n" + r.stderr[-1500:])

    if a.frames:
        for sec in [x.strip() for x in a.frames.split(",") if x.strip()]:
            f = outdir / f"preview-{sec.replace('.', '_')}s.png"
            subprocess.run(["ffmpeg", "-hide_banner", "-y", "-ss", sec, "-i", str(target),
                            "-frames:v", "1", str(f)], capture_output=True)
            print("  프레임:", f)

    print(f"\n  원본 {dur_s:.1f}초 → 출력 {dur_s/a.speed:.1f}초 (x{a.speed}) · "
          f"자막 {len(cues)}큐 · {W}x{H}")
    if a.still and not a.audio_from:
        print("  ⚠ 정지화면 렌더입니다. 레이아웃 확인용이며 게시물이 아닙니다.")
    elif a.still and a.audio_from:
        print("  ℹ 화면은 정지 이미지, 소리는 설교 원본입니다.")
    if a.verify:
        return
    if verified:
        print("  ✅ 자막 등급 QUOTE — 사람이 교정한 파일에서 렌더했습니다.")
        print(f"     출처: {a.captions}")
        (capdir / "captions-verified.json").write_text(json.dumps(
            {"shorts_id": a.shorts_id, "sermon": a.sermon,
             "source_tsv": str(a.captions), "in_ms": start, "out_ms": end,
             "cue_count": len(cues), "posture": "QUOTE"},
            ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        print("  ⚠ 자막 등급 RECONSTRUCTED — 자동(ASR) 원문 그대로입니다.")
        print(f"     초안: {capdir / 'captions-draft.tsv'}")
        print("     다음 단계: --verify 클립을 들으면서 초안을 고치고,")
        print("     --captions <고친파일> 로 다시 렌더하면 QUOTE 가 됩니다.")


if __name__ == "__main__":
    main()
