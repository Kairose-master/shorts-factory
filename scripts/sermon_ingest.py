#!/usr/bin/env python3
"""예심교회 설교 수집 — 신규 감지, 제목 파싱, 자막 확보, 설교 시작 추정.

sermon-office/sop/ingest.md 의 공정을 실행한다.

과금 호출은 --fetch 없이는 절대 일어나지 않는다. 기본은 dry-run이다.
  channel-videos 1회 = 1 credit,  transcript 1편 = 1 credit.

사용법:
  python3 scripts/sermon_ingest.py --selftest          # 무과금, 파서 회귀 테스트
  python3 scripts/sermon_ingest.py --list              # 1 credit, 신규만 표시
  python3 scripts/sermon_ingest.py --fetch --limit 3   # 1 + 3 credits
  python3 scripts/sermon_ingest.py --fetch --video Y1ABPz8B7kw   # 1 credit
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERMONS = ROOT / "sermon-office" / "sermons"
API = "https://api.scrapecreators.com"
HANDLE = "@yeshim1126"
CHANNEL_ID = "UCycXcRJIzo4slTU9sNcwAhQ"

# 예배 종류. 긴 것부터 매칭한다.
SERVICE_TYPES = [
    "새벽기도회", "새벽기도", "수요예배", "금요기도회", "금요철야", "주일예배",
    "유치아동부예배", "유치아동부", "청소년부", "청년예배", "교육부",
    "여름수련회", "수련회", "위임식", "특별새벽", "DTS", "성경공부",
]

# 개역개정 표준 약어 + 전체 이름 → 3글자 코드. 긴 키부터 매칭한다(요일/요이/요삼 대 요).
BOOKS = {
    "창세기": "GEN", "창": "GEN", "출애굽기": "EXO", "출": "EXO",
    "레위기": "LEV", "레": "LEV", "민수기": "NUM", "민": "NUM",
    "신명기": "DEU", "신": "DEU", "여호수아": "JOS", "수": "JOS",
    "사사기": "JDG", "삿": "JDG", "룻기": "RUT", "룻": "RUT",
    "사무엘상": "1SA", "삼상": "1SA", "사무엘하": "2SA", "삼하": "2SA",
    "열왕기상": "1KI", "왕상": "1KI", "열왕기하": "2KI", "왕하": "2KI",
    "역대상": "1CH", "대상": "1CH", "역대하": "2CH", "대하": "2CH",
    "에스라": "EZR", "스": "EZR", "느헤미야": "NEH", "느": "NEH",
    "에스더": "EST", "에": "EST", "욥기": "JOB", "욥": "JOB",
    "시편": "PSA", "시": "PSA", "잠언": "PRO", "잠": "PRO",
    "전도서": "ECC", "전": "ECC", "아가": "SNG", "아": "SNG",
    "이사야": "ISA", "사": "ISA", "예레미야애가": "LAM", "애": "LAM",
    "예레미야": "JER", "렘": "JER", "에스겔": "EZK", "겔": "EZK",
    "다니엘": "DAN", "단": "DAN", "호세아": "HOS", "호": "HOS",
    "요엘": "JOL", "욜": "JOL", "아모스": "AMO", "암": "AMO",
    "오바댜": "OBA", "옵": "OBA", "요나": "JON", "욘": "JON",
    "미가": "MIC", "미": "MIC", "나훔": "NAM", "나": "NAM",
    "하박국": "HAB", "합": "HAB", "스바냐": "ZEP", "습": "ZEP",
    "학개": "HAG", "학": "HAG", "스가랴": "ZEC", "슥": "ZEC",
    "말라기": "MAL", "말": "MAL",
    "마태복음": "MAT", "마": "MAT", "마가복음": "MRK", "막": "MRK",
    "누가복음": "LUK", "눅": "LUK", "요한복음": "JHN", "요": "JHN",
    "사도행전": "ACT", "행": "ACT", "로마서": "ROM", "롬": "ROM",
    "고린도전서": "1CO", "고전": "1CO", "고린도후서": "2CO", "고후": "2CO",
    "갈라디아서": "GAL", "갈": "GAL", "에베소서": "EPH", "엡": "EPH",
    "빌립보서": "PHP", "빌": "PHP", "골로새서": "COL", "골": "COL",
    "데살로니가전서": "1TH", "살전": "1TH", "데살로니가후서": "2TH", "살후": "2TH",
    "디모데전서": "1TI", "딤전": "1TI", "디모데후서": "2TI", "딤후": "2TI",
    "디도서": "TIT", "딛": "TIT", "빌레몬서": "PHM", "몬": "PHM",
    "히브리서": "HEB", "히": "HEB", "야고보서": "JAS", "약": "JAS",
    "베드로전서": "1PE", "벧전": "1PE", "베드로후서": "2PE", "벧후": "2PE",
    "요한일서": "1JN", "요일": "1JN", "요한이서": "2JN", "요이": "2JN",
    "요한삼서": "3JN", "요삼": "3JN", "유다서": "JUD", "유": "JUD",
    "요한계시록": "REV", "계": "REV",
}
BOOK_KEYS = sorted(BOOKS, key=len, reverse=True)

# 자막에서 찬송/음악 구간을 표시하는 마커
MUSIC_MARKERS = ("[노래]", "[음악]", "[박수]", "[Music]", "[Applause]")
# 본문 봉독이 끝나가는 신호
READING_CUES = ("말씀입니다", "절까지", "절 말씀", "아멘", "말씀을 봉독")


def parse_scripture(raw):
    """'겔47:13-23' → ('EZK', '겔 47:13-23'). 못 읽으면 (None, 원문)."""
    s = raw.strip().strip("[]").strip()
    if not s:
        return None, None
    compact = s.replace(" ", "")
    for key in BOOK_KEYS:
        if compact.startswith(key):
            rest = compact[len(key):].lstrip(" .")
            if rest and rest[0].isdigit():
                return BOOKS[key], f"{key} {rest}"
    return None, s


def parse_date(title):
    """제목에서 설교 날짜를 뽑는다. YYYY-M-D, YYYY.M.D, YYYYMMDD 모두 처리."""
    m = re.search(r"(20\d{2})[-.\s]\s?(\d{1,2})[-.\s](\d{1,2})", title)
    if m:
        y, mo, d = (int(x) for x in m.groups())
        if 1 <= mo <= 12 and 1 <= d <= 31:
            return f"{y:04d}-{mo:02d}-{d:02d}"
    m = re.search(r"\b(20\d{2})(\d{2})(\d{2})\b", title)
    if m:
        y, mo, d = (int(x) for x in m.groups())
        if 1 <= mo <= 12 and 1 <= d <= 31:
            return f"{y:04d}-{mo:02d}-{d:02d}"
    return None


def parse_title(title):
    """실측 제목 규약을 구조로 바꾼다. 모르는 형태는 조용히 틀리지 않고 None으로 둔다."""
    out = {
        "title_raw": title,
        "date": parse_date(title),
        "scripture": None,
        "book_code": None,
        "service_type": "기타",
        "preacher": None,
        "subject": None,
    }

    m = re.search(r"\[([^\]]+)\]", title)
    if m and "예심교회" not in m.group(1):
        code, ref = parse_scripture(m.group(1))
        out["book_code"], out["scripture"] = code, ref
    if out["scripture"] is None:
        # 대괄호가 없는 형태: '/ 빌 3:10-12 /'
        for seg in re.split(r"[/|]", title):
            code, ref = parse_scripture(seg)
            if code:
                out["book_code"], out["scripture"] = code, ref
                break

    for st in SERVICE_TYPES:
        if st in title:
            out["service_type"] = st
            break

    m = re.search(r"([가-힣]{2,4})\s*(목사|전도사|사모|강도사|장로)", title)
    if m:
        out["preacher"] = f"{m.group(1)} {m.group(2)}"

    # 남은 것 중 사람이 붙인 설교 제목
    subj = title
    for pat in (r"\[[^\]]*\]", r"20\d{2}[-.\s]?\d{1,2}[-.\s]?\d{1,2}", r"\b20\d{6}\b"):
        subj = re.sub(pat, " ", subj)
    if out["preacher"]:
        subj = subj.replace(out["preacher"], " ")
        subj = re.sub(r"[가-힣]{2,4}\s*(목사|전도사|사모|강도사|장로)", " ", subj)
    if out["service_type"] != "기타":
        subj = subj.replace(out["service_type"], " ")
    subj = re.sub(r"[/|]+", " ", subj)
    subj = re.sub(r"\s+", " ", subj).strip(" -·.")
    out["subject"] = subj or None
    return out


def sermon_id(meta, video_id):
    """S-YYYYMMDD-<본문코드+장>. 날짜나 본문이 없으면 video_id로 떨어진다."""
    date = (meta.get("date") or "").replace("-", "")
    ref = meta.get("scripture") or ""
    m = re.search(r"(\d+)", ref.split(":")[0][::-1])
    chap = m.group(1)[::-1] if m else ""
    code = meta.get("book_code")
    if date and code:
        return f"S-{date}-{code}{chap}"
    if date:
        return f"S-{date}-{video_id}"
    return f"S-unknown-{video_id}"


def estimate_sermon_start(cues):
    """찬송/기도 구간을 건너뛰고 강해가 시작되는 지점을 추정한다.

    확정값이 아니다. 호출자는 반드시 추정치로 라벨링한다
    (sermon-office/research/channel-model.md §6).
    """
    if not cues:
        return None, "자막 없음"
    by_min = {}
    for c in cues:
        minute = int(c["startMs"]) // 60000
        hit = any(mk in c["text"] for mk in MUSIC_MARKERS)
        got, tot = by_min.get(minute, (0, 0))
        by_min[minute] = (got + (1 if hit else 0), tot + 1)

    last_music = -1
    for minute in sorted(by_min):
        got, tot = by_min[minute]
        if tot and got / tot >= 0.15:
            last_music = minute
    floor_ms = (last_music + 1) * 60000 if last_music >= 0 else 0

    for c in cues:
        if int(c["startMs"]) < floor_ms:
            continue
        if any(cue in c["text"] for cue in READING_CUES):
            return int(c["startMs"]), f"봉독 신호 '{c['text'][:24]}' (음악 종료 {last_music+1}분 이후)"
    if last_music >= 0:
        return floor_ms + 60000, f"음악 종료 {last_music+1}분 + 60초 (봉독 신호 없음)"
    return 0, "음악 구간·봉독 신호 모두 없음 — 0으로 둠"


def api_get(path, **params):
    key = os.environ.get("SCRAPECREATORS_API_KEY")
    if not key:
        sys.exit("SCRAPECREATORS_API_KEY 가 설정되지 않았습니다. "
                 "자격증명을 지어내지 않습니다 — 키를 설정하거나 --selftest 만 실행하세요.")
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"x-api-key": key})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode())


def known_ids():
    if not SERMONS.is_dir():
        return set()
    out = set()
    for meta in SERMONS.glob("*/meta.json"):
        try:
            out.add(json.loads(meta.read_text(encoding="utf-8"))["video_id"])
        except Exception:
            pass
    return out


def cmd_list(args):
    """1 credit. 최신 영상 목록과 파싱 결과, 신규 여부를 보여준다."""
    data = api_get("/v1/youtube/channel-videos", handle=HANDLE, sort=args.sort)
    seen = known_ids()
    print(f"credits 잔여 {data.get('credits_remaining')} · 청구 {data.get('credits_charged')}\n")
    print(f"{'신규':<4}{'설교ID':<22}{'예배':<10}{'설교자':<10}{'조회':>5}  제목")
    for v in data.get("videos", [])[: args.limit or 30]:
        meta = parse_title(v["title"])
        sid = sermon_id(meta, v["id"])
        new = "  " if v["id"] in seen else "NEW"
        print(f"{new:<4}{sid:<22}{meta['service_type']:<10}"
              f"{(meta['preacher'] or '-'):<10}{v.get('viewCountInt', 0):>5}  {v['title'][:48]}")
    return 0


def ingest_video(video):
    """자막을 가져와 sermons/<id>/ 를 만든다. 1 credit."""
    meta = parse_title(video["title"])
    sid = sermon_id(meta, video["id"])
    tr = api_get("/v1/youtube/video/transcript", url=video["url"])
    cues = tr.get("transcript") or []
    start_ms, why = estimate_sermon_start(cues)

    d = SERMONS / sid
    d.mkdir(parents=True, exist_ok=True)
    (d / "transcript.json").write_text(
        json.dumps({"videoId": video["id"], "language": tr.get("language"),
                    "captionTracks": tr.get("captionTracks"), "transcript": cues},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    record = {
        "sermon_id": sid,
        "video_id": video["id"],
        "url": video["url"],
        **meta,
        "published_time": video.get("publishedTime"),
        "length_seconds": video.get("lengthSeconds"),
        "view_count_at_ingest": video.get("viewCountInt"),
        "ingested_at": "2026-08-29",
        "caption_kind": (tr.get("captionTracks") or [{}])[0].get("kind"),
        "caption_cues": len(cues),
        "sermon_start_ms_estimated": start_ms,
        "sermon_start_basis": why,
        "quote_audio_verified": False,
    }
    (d / "meta.json").write_text(json.dumps(record, ensure_ascii=False, indent=1),
                                 encoding="utf-8")
    mm, ss = divmod((start_ms or 0) // 1000, 60)
    print(f"  ✓ {sid}  큐 {len(cues)}개 · 설교 시작 추정 {mm}:{ss:02d} ({why})")
    return sid


def fetch_video(video_id):
    """채널 목록 밖의 영상 하나를 직접 조회한다. 1 credit."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    d = api_get("/v1/youtube/video", url=url)
    if not d.get("success", True) or not d.get("title"):
        sys.exit(f"{video_id} 조회 실패")
    return {
        "id": d.get("id") or video_id,
        "url": url,
        "title": d["title"],
        "publishedTime": d.get("publishDate"),
        "lengthSeconds": (d.get("durationMs") or 0) // 1000,
        "viewCountInt": d.get("viewCountInt"),
    }


def cmd_fetch(args):
    data = api_get("/v1/youtube/channel-videos", handle=HANDLE, sort=args.sort)
    vids = data.get("videos", [])
    if args.video:
        found = [v for v in vids if v["id"] == args.video]
        # 최신 30편 밖의 과거 영상은 목록에 없다. 채널이 1,268편이므로 흔한 경우다.
        # 그럴 때는 영상 엔드포인트로 직접 메타데이터를 가져온다 (+1 credit).
        vids = found or [fetch_video(args.video)]
    else:
        seen = known_ids()
        vids = [v for v in vids if v["id"] not in seen][: args.limit]
    if not vids:
        print("신규 설교 없음.")
        return 0
    print(f"{len(vids)}편 수집 — 자막 {len(vids)} credits 청구 예정\n")
    for v in vids:
        ingest_video(v)
    return 0


# ─────────────────────────── 회귀 테스트 ───────────────────────────
# 2026-08-29 채널에서 실제로 관측된 제목들. 형태가 바뀌면 여기가 먼저 깨진다.
CASES = [
    ("2026-8-28[겔47:13-23]/새벽기도/장선기 목사",
     {"date": "2026-08-28", "book_code": "EZK", "scripture": "겔 47:13-23",
      "service_type": "새벽기도", "preacher": "장선기 목사"}),
    ("2026-8-26 [마태복음 8:10-22] 치유하시는 예수님 / 김지훈 목사",
     {"date": "2026-08-26", "book_code": "MAT", "scripture": "마태복음 8:10-22",
      "service_type": "기타", "preacher": "김지훈 목사", "subject": "치유하시는 예수님"}),
    ("2023-6-1 새벽기도 [눅17:7-19]/ 불편하면 기도하라/ 장선기 목사",
     {"date": "2023-06-01", "book_code": "LUK", "scripture": "눅 17:7-19",
      "service_type": "새벽기도", "preacher": "장선기 목사", "subject": "불편하면 기도하라"}),
    ("[예심교회] / 빌 3:10-12 / 수요예배 / 이승일 목사 / 20230322",
     {"date": "2023-03-22", "book_code": "PHP", "scripture": "빌 3:10-12",
      "service_type": "수요예배", "preacher": "이승일 목사"}),
    ("2024-8-7[롬2:17-29]/다른 사람을 가르치는 네가 하는 일을 보라/장선기 목사",
     {"date": "2024-08-07", "book_code": "ROM", "scripture": "롬 2:17-29",
      "preacher": "장선기 목사", "subject": "다른 사람을 가르치는 네가 하는 일을 보라"}),
    ("20260823 유치아동부예배",
     {"date": "2026-08-23", "book_code": None, "service_type": "유치아동부예배",
      "preacher": None}),
    ("예심 DTS 제자도1 오실환 목사",
     {"date": None, "book_code": None, "service_type": "DTS",
      "preacher": "오실환 목사"}),
    ("2023-08-29 [요일 4:7-12] 새벽기도 / 장선기 목사",
     {"book_code": "1JN", "scripture": "요일 4:7-12"}),
    ("2024-1-2[살전5:16-18]/새벽기도/장선기 목사",
     {"book_code": "1TH", "scripture": "살전 5:16-18"}),
    ("2023-5-24 새벽기도 [눅15:1-10]/ 잃어버린 양들이여/ 장선기 목사",
     {"book_code": "LUK", "scripture": "눅 15:1-10", "service_type": "새벽기도"}),
    ("2026-7-29[겔33:1-9]/새벽기도/장선기 목사",
     {"date": "2026-07-29", "book_code": "EZK", "scripture": "겔 33:1-9"}),
    ("2023-08-29 [욘 1:1-3] 새벽기도 / 장선기 목사",
     {"book_code": "JON", "scripture": "욘 1:1-3"}),
    ("2023-08-29 [욜 2:28-32] 새벽기도 / 장선기 목사",
     {"book_code": "JOL", "scripture": "욜 2:28-32"}),
    ("2023-08-29 [요 4:34-38] 수요예배 / 오묘희 전도사",
     {"book_code": "JHN", "scripture": "요 4:34-38", "preacher": "오묘희 전도사"}),
]

ID_CASES = [
    ("2026-8-28[겔47:13-23]/새벽기도/장선기 목사", "abc123", "S-20260828-EZK47"),
    ("20260823 유치아동부예배", "vid999", "S-20260823-vid999"),
    ("예심 DTS 제자도1 오실환 목사", "zzz", "S-unknown-zzz"),
]


def cmd_selftest(_args):
    fails = 0
    for title, expect in CASES:
        got = parse_title(title)
        for k, want in expect.items():
            if got[k] != want:
                fails += 1
                print(f"FAIL  {title[:44]!r}\n      {k}: {got[k]!r} != {want!r}")
    for title, vid, want in ID_CASES:
        got = sermon_id(parse_title(title), vid)
        if got != want:
            fails += 1
            print(f"FAIL  id  {title[:36]!r}: {got!r} != {want!r}")

    cues = ([{"startMs": str(i * 3000), "text": "찬양 [노래]"} for i in range(20)]
            + [{"startMs": str(60000 + i * 3000), "text": "기도합니다"} for i in range(60)]
            + [{"startMs": "300000", "text": "23절까지의 말씀입니다."}]
            + [{"startMs": str(303000 + i * 3000), "text": "강해"} for i in range(50)])
    ms, why = estimate_sermon_start(cues)
    if ms != 300000:
        fails += 1
        print(f"FAIL  설교 시작 추정: {ms} != 300000 ({why})")
    if estimate_sermon_start([])[0] is not None:
        fails += 1
        print("FAIL  빈 자막이 None 을 반환하지 않음")

    total = len(CASES) + len(ID_CASES) + 2
    print(f"\n{'FAILED' if fails else 'OK'}  {total - fails}/{total} 통과")
    return 1 if fails else 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="최신 목록 표시 (1 credit)")
    p.add_argument("--fetch", action="store_true", help="자막까지 수집 (1 + N credits)")
    p.add_argument("--selftest", action="store_true", help="파서 회귀 테스트 (무과금)")
    p.add_argument("--video", help="특정 video id 하나만")
    p.add_argument("--limit", type=int, default=5, help="최대 편수 (기본 5)")
    p.add_argument("--sort", default="latest", choices=["latest", "popular"])
    a = p.parse_args()

    if a.selftest:
        return cmd_selftest(a)
    if a.fetch:
        return cmd_fetch(a)
    if a.list:
        return cmd_list(a)
    p.print_help()
    print("\n과금 호출은 --list 또는 --fetch 를 명시할 때만 일어납니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
