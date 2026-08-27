#!/usr/bin/env python3
"""Transcripts + comments for the top 3 Shorts of each channel (recent window where possible)."""
import json, os, statistics as st, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

KEY = os.environ["SCRAPECREATORS_API_KEY"]
BASE = "https://api.scrapecreators.com/v1"
OUT = Path(__file__).resolve().parent
NOW = datetime(2026, 8, 27, tzinfo=timezone.utc)

def get(path, **params):
    url = f"{BASE}{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"x-api-key": KEY})
    for a in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except Exception as exc:
            if a == 2:
                print(f"    ERR {path}: {exc}", file=sys.stderr)
                return None
            time.sleep(2 ** a)

def age(s):
    return (NOW - datetime.fromisoformat(s["publishDate"]).astimezone(timezone.utc)).days \
        if s.get("publishDate") else 9999

def flatten_transcript(r):
    if not r:
        return ""
    for k in ("transcript", "text", "transcript_only_text"):
        if isinstance(r.get(k), str) and r[k].strip():
            return r[k].strip()
    for k in ("segments", "items"):
        v = r.get(k)
        if isinstance(v, list) and v:
            parts = []
            for seg in v:
                if isinstance(seg, dict):
                    for ev in seg.get("events", []) or []:
                        if ev.get("text"):
                            parts.append(ev["text"])
                    if seg.get("text"):
                        parts.append(seg["text"])
            if parts:
                return " ".join(parts).strip()
    return ""

def comments_of(r):
    if not r:
        return []
    for k in ("comments", "data", "items"):
        v = r.get(k)
        if isinstance(v, list):
            out = []
            for c in v:
                if not isinstance(c, dict):
                    continue
                out.append({"text": (c.get("commentText") or c.get("text") or
                                     c.get("content") or "").strip(),
                            "likes": c.get("likeCountInt") or c.get("likes") or
                                     c.get("voteCount") or 0})
            return [c for c in out if c["text"]]
    return []

CACHE = OUT / "deep.jsonl"
done = {}
if CACHE.exists():
    for ln in CACHE.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            r = json.loads(ln)
            done[r["id"]] = r
    print(f"  resuming: {len(done)} videos already fetched")

data = json.load(open(OUT / "channels.json"))
deep = {}
for h, v in data.items():
    sh = [s for s in v["shorts"] if s.get("viewCountInt")]
    if not sh:
        continue
    med = st.median([s["viewCountInt"] for s in sh])
    recent = [s for s in sh if age(s) <= 365]
    pool = recent if len(recent) >= 5 else sh
    top = sorted(pool, key=lambda s: -s["viewCountInt"])[:3]
    deep[h] = []
    for s in top:
        if s["id"] in done:
            deep[h].append(done[s["id"]])
            continue
        tr = get("/youtube/video/transcript", url=s["url"])
        cm = get("/youtube/video/comments", url=s["url"])
        cs = sorted(comments_of(cm), key=lambda c: -(c["likes"] or 0))[:25]
        rec = {"id": s["id"], "url": s["url"], "title": s["title"],
               "views": s["viewCountInt"], "likes": s.get("likeCountInt"),
               "multiple": round(s["viewCountInt"] / med, 2), "age_days": age(s),
               "seconds": (s.get("durationMs") or 0) / 1000,
               "transcript": flatten_transcript(tr), "comments": cs}
        deep[h].append(rec)
        with open(CACHE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"  {h:<12} {s['id']}  {rec['multiple']:>6.1f}x  "
              f"transcript {len(rec['transcript']):>5} chars  comments {len(cs):>3}")

(OUT / "deep.json").write_text(json.dumps(deep, ensure_ascii=False, indent=1))
print(f"\nwrote {OUT / 'deep.json'}")
