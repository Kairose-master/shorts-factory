#!/usr/bin/env python3
"""MASTER-PROMPT §13 OBSERVE 단계 — 발행 영상 성과 스냅샷 (LLM 토큰 0).

queue.json의 PUBLISHED 항목을 ScrapeCreators로 조회해 analytics.jsonl에
타임스탬프 스냅샷을 append한다. 24H/72H/7D 시점에 실행.
비용: 영상당 1 크레딧. 사용: python3 factory/analytics.py
"""
import json, os, sys, time, urllib.request, ssl
ROOT = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("SCRAPECREATORS_API_KEY")
if not KEY:
    sys.exit("SCRAPECREATORS_API_KEY unset — 실행 불가 (자격증명 발명 금지 원칙)")

ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt") \
    if os.path.exists("/root/.ccr/ca-bundle.crt") else ssl.create_default_context()
opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.ProxyHandler({"https": os.environ.get("HTTPS_PROXY", "")})
    if os.environ.get("HTTPS_PROXY") else urllib.request.HTTPSHandler(context=ctx))

q = json.load(open(f"{ROOT}/queue.json"))
pub = [it for it in q["items"] if it.get("status") == "PUBLISHED" and it.get("videoId")]
now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
out = open(f"{ROOT}/analytics.jsonl", "a")
for it in pub:
    url = (f"https://api.scrapecreators.com/v1/youtube/video"
           f"?url=https://www.youtube.com/watch?v={it['videoId']}")
    req = urllib.request.Request(url, headers={"x-api-key": KEY})
    try:
        j = json.load(opener.open(req, timeout=60))
    except Exception as e:
        print(f"{it['id']}: FETCH FAIL {e}"); continue
    snap = {"ts": now, "id": it["id"], "videoId": it["videoId"],
            "views": j.get("viewCountInt"), "likes": j.get("likeCountInt"),
            "comments": j.get("commentCountInt"),
            "title": j.get("title")}
    out.write(json.dumps(snap, ensure_ascii=False) + "\n")
    print(f"{it['id']:14} views={snap['views']} likes={snap['likes']} comments={snap['comments']}")
out.close()
print(f"snapshot @ {now} — {len(pub)} videos, ~{len(pub)} credits")
