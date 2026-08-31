#!/usr/bin/env python3
"""EXP-E06 전용 — 예심교회 실제 본당 사진(SS-016 정지화면에서 로고·워터마크
   제외하고 추출) 위에, 설교 영상을 실제 스크린 자리에 합성한다.
   "영화관에서 보는 것처럼" 템플릿을 이 교회 자신의 예배당으로 재현 —
   외부 스톡·생성 이미지 없이 우리 채널의 진짜 공간이다.
"""
import argparse, re, subprocess, sys
from pathlib import Path

OFFICE = Path(__file__).resolve().parents[2]
ASSETS = Path(__file__).with_name("assets")
FONT = "Noto Sans CJK KR"
W, H = 1080, 1920
# church-cinema-bg.png 제작 스크립트(build_church_cinema_bg.py)가 계산한 스크린 좌표
SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H = 570, 349, 311, 183
HOOK_SIZE, HOOK_MARGIN_TOP = 52, 60
CAP_SIZE, CAP_MARGIN_BOTTOM = 46, 760
ATTR_SIZE, ATTR_MARGIN_BOTTOM = 26, 700
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
Style: HOOK,{FONT},{HOOK_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,0,0,3,0,0,8,50,50,{HOOK_MARGIN_TOP},1
Style: CAP,{FONT},{CAP_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,5,2,2,90,90,{CAP_MARGIN_BOTTOM},1
Style: ATTR,{FONT},{ATTR_SIZE},{GRAY},{GRAY},{BLACK},{BLACK},0,0,0,0,100,100,0,0,1,3,0,2,90,90,{ATTR_MARGIN_BOTTOM},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # HOOK 스타일 BorderStyle=3(불투명 박스) — 천장 위에서도 읽히도록
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
    ap.add_argument("--hook", required=True)
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

    bg = ASSETS / "church-cinema-bg.png"
    target = outdir / "final.mp4"
    speed_v = f"setpts=PTS/{a.speed}" if a.speed != 1.0 else "setpts=PTS-STARTPTS"
    screen_ratio = SCREEN_W / SCREEN_H
    vf_video = (
        f"crop=ih*{screen_ratio}:ih:(iw-ih*{screen_ratio})/2:0,"
        f"scale={SCREEN_W}:{SCREEN_H}:flags=lanczos,{speed_v}"
    )
    filter_complex = (
        f"[0:v]{vf_video}[vid];"
        f"[1:v][vid]overlay={SCREEN_X}:{SCREEN_Y}:shortest=1[comp];"
        f"[comp]subtitles='{ass}':fontsdir=/usr/share/fonts[out]"
    )
    af, rem = "", a.speed
    while rem > 2.0:
        af += "atempo=2.0,"; rem /= 2.0
    while rem < 0.5:
        af += "atempo=0.5,"; rem /= 0.5
    af += f"atempo={rem:.4f},loudnorm=I=-14:TP=-1.5:LRA=11"

    cmd = ["ffmpeg", "-hide_banner", "-y",
           "-ss", f"{start/1000:.3f}", "-t", f"{dur_s:.3f}", "-i", a.source,
           "-loop", "1", "-i", str(bg),
           "-filter_complex", filter_complex, "-map", "[out]", "-map", "0:a",
           "-af", af,
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
