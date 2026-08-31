#!/usr/bin/env python3
"""EXP-E04 전용 — @churchsoulmate(팔로워 171,610) 레퍼런스 릴스를 실측해
   그대로 흉내 낸 실험 렌더러. build_short.py(기본 포맷, 풀블리드 크롭 +
   노란 자막)를 대체하지 않는다 — 이 오피스의 기본값은 여전히 build_short.py다.

   레퍼런스: churchsoulmate "아직도 들으면 눈물이 흐르는 하용조 목사님의
   생전 마지막 설교 말씀" (72초, 1,168,878회 재생, 33,795 좋아요, 2023-08
   게시 — 이 계정 최근 게시물 대비 약 4~20배 재생, 명백한 아웃라이어).

   실측한 레이아웃 차이(기존 포맷 대비):
     1. 풀블리드 크롭이 아니라 어두운 캔버스(#1A2631) 위에 둥근 모서리
        박스로 영상을 인셋한다.
     2. 자막이 노란색이 아니라 흰색이고, 박스 하단(영상 위)에 겹친다.
     3. 훅이 인용부호로 감싼 실제 발화 한 줄 + 출처 한 줄(2행) 구조다.
     4. 박스 하단 자막 아래 작은 회색 출처 표기가 항상 떠 있다
        ("故하용조 목사 | 온누리교회").
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

OFFICE = Path(__file__).resolve().parents[2]
FONT = "Noto Sans CJK KR"
W, H = 1080, 1920
BG = "0x1A2631"                 # 레퍼런스 배경 실측(RGB 26,38,49)
BOX_X, BOX_Y, BOX_W, BOX_H = 72, 407, 936, 1123   # 레퍼런스 비율 실측
HOOK_SIZE, HOOK_MARGIN_TOP = 62, 130
CAP_SIZE, CAP_MARGIN_BOTTOM = 52, 470
ATTR_SIZE, ATTR_MARGIN_BOTTOM = 30, 400
CAP_SIDE = BOX_X + 60           # 자막을 박스 안쪽으로 제한
WHITE, GRAY, BLACK = "&H00FFFFFF", "&H00AAAAAA", "&H00000000"


def die(msg):
    sys.exit(f"오류: {msg}")


def parse_tc(s):
    s = str(s).strip()
    if re.fullmatch(r"\d+", s):
        return int(s)
    m = re.fullmatch(r"(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)", s)
    if not m:
        die(f"타임코드를 읽을 수 없음: {s!r}")
    h, mm, ss = m.group(1) or 0, m.group(2), m.group(3)
    return int((int(h) * 3600 + int(mm) * 60 + float(ss)) * 1000)


def ass_time(ms):
    ms = max(0, int(ms))
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, cs = divmod(r, 1000)
    return f"{h}:{m:02d}:{s:02d}.{cs // 10:02d}"


def wrap(text, width, max_lines=2):
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


def read_caption_tsv(path):
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            die(f"{path}:{i}: 탭 3개 필드 필요")
        s, e = int(parts[0]), int(parts[1])
        txt = "\t".join(parts[2:]).strip()
        if txt:
            out.append((s, e, txt))
    return out


def build_ass(hook_lines, cues, duration_ms, attribution):
    hook = r"\N".join(hook_lines)
    head = f"""[Script Info]
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HOOK,{FONT},{HOOK_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,4,2,8,60,60,{HOOK_MARGIN_TOP},1
Style: CAP,{FONT},{CAP_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,5,2,2,{CAP_SIDE},{CAP_SIDE},{CAP_MARGIN_BOTTOM},1
Style: ATTR,{FONT},{ATTR_SIZE},{GRAY},{GRAY},{BLACK},{BLACK},0,0,0,0,100,100,0,0,1,3,0,2,{CAP_SIDE},{CAP_SIDE},{ATTR_MARGIN_BOTTOM},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 0,{ass_time(0)},{ass_time(duration_ms)},HOOK,,0,0,0,,{hook}",
          f"Dialogue: 0,{ass_time(0)},{ass_time(duration_ms)},ATTR,,0,0,0,,{attribution}"]
    for s, e, t in cues:
        ev.append(f"Dialogue: 1,{ass_time(s)},{ass_time(e)},CAP,,0,0,0,,{wrap(t, 17)}")
    return head + "\n".join(ev) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shorts-id", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--in", dest="tin", required=True)
    ap.add_argument("--out", dest="tout", required=True)
    ap.add_argument("--hook", required=True, help="'인용|출처' 2행")
    ap.add_argument("--attribution", required=True)
    ap.add_argument("--captions", required=True)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--frames", default="")
    a = ap.parse_args()

    start, end = parse_tc(a.tin), parse_tc(a.tout)
    dur_ms = end - start
    dur_s = dur_ms / 1000
    hook_lines = [x.strip() for x in a.hook.split("|") if x.strip()]

    base = OFFICE / "production" / a.shorts_id
    outdir, capdir = base / "renders", base / "captions"
    outdir.mkdir(parents=True, exist_ok=True)
    capdir.mkdir(parents=True, exist_ok=True)

    cues = read_caption_tsv(Path(a.captions))
    out_ms = int(dur_ms / a.speed)
    ass = capdir / "captions.ass"
    ass.write_text(build_ass(hook_lines, cues, out_ms, a.attribution), encoding="utf-8")

    target = outdir / "final.mp4"
    # 소스를 박스 비율(936:1123 ≈ 0.833)로 중앙 크롭한 뒤 박스 크기로 스케일하고,
    # 어두운 캔버스 위 (BOX_X,BOX_Y)에 얹는다. 레퍼런스는 둥근 모서리 + 그림자를
    # 쓰지만 ffmpeg 순정 필터로는 비용이 커서 이번 실험에서는 생략한다.
    box_ratio = BOX_W / BOX_H
    speed_v = f"setpts=PTS/{a.speed}" if a.speed != 1.0 else "setpts=PTS-STARTPTS"
    vf = (
        f"crop=ih*{box_ratio}:ih:(iw-ih*{box_ratio})/2:0,"
        f"scale={BOX_W}:{BOX_H}:flags=lanczos,{speed_v},"
        f"pad={W}:{H}:{BOX_X}:{BOX_Y}:color={BG},"
        f"subtitles='{ass}':fontsdir=/usr/share/fonts"
    )
    af, rem = "", a.speed
    while rem > 2.0:
        af += "atempo=2.0,"; rem /= 2.0
    while rem < 0.5:
        af += "atempo=0.5,"; rem /= 0.5
    af += f"atempo={rem:.4f},loudnorm=I=-14:TP=-1.5:LRA=11"

    cmd = ["ffmpeg", "-hide_banner", "-y", "-ss", f"{start/1000:.3f}",
           "-t", f"{dur_s:.3f}", "-i", a.source, "-vf", vf, "-af", af,
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
           "-t", f"{dur_s / a.speed:.3f}",
           "-movflags", "+faststart", str(target)]
    print("렌더:", target)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        die("ffmpeg 실패\n" + r.stderr[-2000:])

    if a.frames:
        for sec in [x.strip() for x in a.frames.split(",") if x.strip()]:
            f = outdir / f"preview-{sec.replace('.', '_')}s.png"
            subprocess.run(["ffmpeg", "-hide_banner", "-y", "-ss", sec, "-i", str(target),
                            "-frames:v", "1", str(f)], capture_output=True)
            print("  프레임:", f)
    print(f"\n  {dur_s:.1f}초 → {dur_s/a.speed:.1f}초 (x{a.speed}) · {len(cues)}큐 · {W}x{H}")


if __name__ == "__main__":
    main()
