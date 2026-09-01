#!/usr/bin/env python3
"""EXP-E07 전용 — "서장훈 팩폭" 류 명언/동기부여 쇼츠 실측 스타일.
   레퍼런스: YouTube "서장훈 팩폭 다 뻥입니다"(4.1M회, 출처: 청춘페스티벌
   강연) — 다운로드해 프레임 단위로 확인.

   레퍼런스와 다른 점(자세 등급 색상 규칙 보존, brand/shorts-format.md):
   레퍼런스는 훅·자막 둘 다 흰색이지만, 이 오피스는 **노란 자막 = QUOTE**
   라는 색상 규칙이 위조 방지 장치다(§자세 등급). 그래서 자막은 노란색을
   그대로 유지하고, 레퍼런스의 구조적 아이디어만 가져온다:
     1. 풀블리드 크롭이 아니라 **레터박스**(원본 종횡비 유지, 검정 바탕) —
        crop-x 재실측 부담이 줄어든다(L-15/L-20 문제 완화).
     2. 자막 아래 **상시 출처 표기**(지금은 엔드카드에만 있음).

   1차 렌더는 훅에 청록색 네온 외곽선을 넣었으나, 채널 소유자가
   "제목 폰트가 너무구려"라고 반려 — 작은 68pt 글자에 Outline=7의
   밝은 청록 외곽선이 붙으니 글자 형태가 뭉개져 싸구려 밈 폰트처럼
   보였다. build_short.py가 이미 쓰는 검정 외곽선(글자 크기 대비
   ~6% 비율)으로 되돌렸다 — 폰트 자체(Noto Sans CJK KR Bold)는
   그대로다, 문제는 외곽선 색·두께였다.
"""
import argparse, re, subprocess, sys
from pathlib import Path

OFFICE = Path(__file__).resolve().parents[2]
FONT = "Noto Sans CJK KR"
W, H = 1080, 1920
HOOK_BAND_H = 230       # 상단 검정 밴드
VIDEO_H = 1350          # 4:5 비율 영상 (1080x1350)
VIDEO_Y = HOOK_BAND_H
HOOK_SIZE = 68
HOOK_OUTLINE, HOOK_SHADOW = 4, 3   # build_short.py와 같은 비율(외곽선/글자크기 ≈6%)
CAP_SIZE, CAP_MARGIN_BOTTOM = 56, 220
ATTR_SIZE, ATTR_MARGIN_BOTTOM = 30, 130
WHITE, YELLOW, GRAY, BLACK = "&H00FFFFFF", "&H0000E0FF", "&H00AAAAAA", "&H00000000"


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
    # HOOK: Alignment=2(하단 중앙 정렬) 기준으로 상단 밴드 중앙에 오도록 역산.
    # 2줄 블록 높이 근사(폰트 크기 x 1.35 x 2줄)를 상단 밴드(HOOK_BAND_H) 중앙에 맞춘다.
    block_h = int(HOOK_SIZE * 1.35 * max(len(hook_lines), 1))
    hook_margin_v = H - ((HOOK_BAND_H - block_h) // 2 + block_h)
    head = f"""[Script Info]
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HOOK,{FONT},{HOOK_SIZE},{WHITE},{WHITE},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,{HOOK_OUTLINE},{HOOK_SHADOW},2,60,60,{hook_margin_v},1
Style: CAP,{FONT},{CAP_SIZE},{YELLOW},{YELLOW},{BLACK},{BLACK},1,0,0,0,100,100,0,0,1,5,2,2,80,80,{CAP_MARGIN_BOTTOM},1
Style: ATTR,{FONT},{ATTR_SIZE},{GRAY},{GRAY},{BLACK},{BLACK},0,0,0,0,100,100,0,0,1,3,0,2,80,80,{ATTR_MARGIN_BOTTOM},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 0,{ass_time(0)},{ass_time(duration_ms)},HOOK,,0,0,0,,{hook}",
          f"Dialogue: 0,{ass_time(0)},{ass_time(duration_ms)},ATTR,,0,0,0,,{attribution}"]
    for s, e, t in cues:
        ev.append(f"Dialogue: 1,{ass_time(s)},{ass_time(e)},CAP,,0,0,0,,{wrap(t, 15)}")
    return head + "\n".join(ev) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shorts-id", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--in", dest="tin", required=True)
    ap.add_argument("--out", dest="tout", required=True)
    ap.add_argument("--hook", required=True, help="'1행|2행'")
    ap.add_argument("--attribution", required=True)
    ap.add_argument("--captions", required=True)
    ap.add_argument("--crop-x", type=float, default=0.5)
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
    video_ratio = W / VIDEO_H  # 1080:1350 = 0.8
    speed_v = f"setpts=PTS/{a.speed}" if a.speed != 1.0 else "setpts=PTS-STARTPTS"
    cx = "(iw-ow)/2" if a.crop_x == 0.5 else f"(iw-ow)*{a.crop_x}"
    vf = (
        f"crop=ih*{video_ratio}:ih:{cx}:0,"
        f"scale={W}:{VIDEO_H}:flags=lanczos,{speed_v},"
        f"pad={W}:{H}:0:{VIDEO_Y}:color=black,"
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
