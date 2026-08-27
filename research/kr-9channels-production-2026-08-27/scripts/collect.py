#!/usr/bin/env python3
"""Collect Shorts listings for the nine tracked Korean channels."""
import json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

KEY = os.environ["SCRAPECREATORS_API_KEY"]
BASE = "https://api.scrapecreators.com/v1"
OUT = Path(__file__).resolve().parent
HANDLES = ["romantoon", "효잉-ing", "read-y", "wonjaewoo", "dangmolee",
           "궁금소", "moon_couple", "내손내싼", "제로비ZeroB"]

def get(path, **params):
    url = f"{BASE}{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"x-api-key": KEY})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read())
        except Exception as exc:
            if attempt == 2:
                print(f"  ERR {path} {params}: {exc}", file=sys.stderr)
                return None
            time.sleep(2 ** attempt)

data = {}
for h in HANDLES:
    prof = get("/youtube/channel", handle=h)
    if not prof or not prof.get("success"):
        print(f"  FAIL profile {h}")
        continue
    shorts, token, pages = [], None, 0
    while pages < 2:
        p = {"handle": h}
        if token:
            p["continuationToken"] = token
        r = get("/youtube/channel/shorts", **p)
        if not r:
            break
        shorts += r.get("shorts") or []
        token = r.get("continuationToken")
        pages += 1
        if not token:
            break
    data[h] = {"profile": {k: prof.get(k) for k in
                           ("name", "handle", "channelId", "subscriberCount",
                            "videoCount", "viewCount", "description")},
               "shorts": shorts}
    print(f"  {h:<14} subs {prof.get('subscriberCount'):>9,}  shorts {len(shorts):>3}  "
          f"credits left {r.get('credits_remaining') if r else '?'}")

(OUT / "channels.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
print(f"\nwrote {OUT / 'channels.json'}")
