#!/usr/bin/env python3
"""Re-pull comments with engagement.likes, which the first pass dropped."""
import json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

KEY = os.environ["SCRAPECREATORS_API_KEY"]
OUT = Path(__file__).resolve().parent

def get(url):
    req = urllib.request.Request(url, headers={"x-api-key": KEY})
    for a in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except Exception as exc:
            if a == 2:
                print(f"  ERR {exc}", file=sys.stderr)
                return None
            time.sleep(2 ** a)

CACHE = OUT / "comments.json"
have = json.loads(CACHE.read_text()) if CACHE.exists() else {}
deep = json.loads((OUT / "deep.json").read_text())

for h, vids in deep.items():
    for v in vids:
        if v["id"] in have:
            continue
        r = get("https://api.scrapecreators.com/v1/youtube/video/comments?url="
                + urllib.parse.quote(v["url"], safe=""))
        cs = []
        for c in (r or {}).get("comments") or []:
            cs.append({"text": (c.get("content") or "").strip(),
                       "likes": (c.get("engagement") or {}).get("likes") or 0,
                       "replies": (c.get("engagement") or {}).get("replies") or 0,
                       "is_creator": bool((c.get("author") or {}).get("isCreator"))})
        cs = [c for c in cs if c["text"]]
        have[v["id"]] = sorted(cs, key=lambda c: -c["likes"])
        CACHE.write_text(json.dumps(have, ensure_ascii=False, indent=1))
        top = have[v["id"]][0]["likes"] if have[v["id"]] else 0
        print(f"  {h:<12} {v['id']}  {len(cs):>3} comments, top {top:,} likes")

for h, vids in deep.items():
    for v in vids:
        v["comments"] = have.get(v["id"], [])
(OUT / "deep.json").write_text(json.dumps(deep, ensure_ascii=False, indent=1))
print("\nmerged into deep.json")
