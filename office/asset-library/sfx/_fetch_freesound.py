#!/usr/bin/env python3
"""Fetch CC0 texture from Freesound into the Office SFX library.

Deliberately narrow. The synthesised pack already covers every UI event —
clicks, ticks, counters, verdicts. What synthesis cannot produce is texture with
a *performance* in it: a real room, real mechanical noise, something that sounds
like a place rather than an event. That is the only thing fetched here.

Auth reality (checked against Freesound's resource docs, not assumed):
  /sounds/<id>/download/  requires OAuth2 — unavailable with a plain token.
  previews (mp3/ogg)      work with `Authorization: Token`.
So this pulls the HQ mp3 preview. At ~128kbps, under narration in a 30s vertical
video, that is inaudible from the master — and it is the only path a token opens.

Every query hard-filters `license:"Creative Commons 0"` at the source. Nothing
that is not CC0 can enter the library through this script.

Usage: python3 office/asset-library/sfx/_fetch_freesound.py
"""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys, tempfile
import urllib.error, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
API = "https://freesound.org/apiv2"

# slug -> (queries tried in order, max seconds, why synthesis cannot do it)
WANTED = {
    "amb-server-room": (
        ["server room ambience", "computer room hum", "data center ambience",
         "computer fan hum room"], 30,
        "a real room's hum — synthesis gives pink noise, not a place"),
    "amb-office": (
        ["office ambience quiet", "office room tone", "workplace ambience quiet"], 30,
        "room tone with people in it"),
    "keys-mechanical": (
        ["mechanical keyboard typing", "keyboard typing close", "typing keys mechanical"], 12,
        "real key travel and rattle; synthesised clicks read as UI, not hands"),
    "coins-handling": (
        ["coins handling", "coin drop metal", "coins jingle"], 8,
        "actual metal — a synthesised coin is a bell"),
    "paper-handle": (
        ["paper shuffle", "paper handling document", "paper page turn"], 8,
        "a document being physically handled"),
}


def key() -> str:
    k = os.environ.get("FREESOUND_API_KEY")
    if not k:
        env = ROOT / ".env"
        if env.is_file():
            for line in env.read_text().splitlines():
                if line.startswith("FREESOUND_API_KEY="):
                    k = line.split("=", 1)[1].strip()
    if not k:
        sys.exit("BLOCKED: FREESOUND_API_KEY_REQUIRED — see office/skills/freesound-setup.md")
    return k


def get(url: str, k: str, raw=False):
    req = urllib.request.Request(url, headers={"Authorization": f"Token {k}"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read() if raw else json.load(r)


def search(q: str, maxdur: int, k: str) -> list:
    params = urllib.parse.urlencode({
        "query": q,
        "filter": f'license:"Creative Commons 0" duration:[1 TO {maxdur}]',
        "fields": "id,name,duration,license,username,previews,url,samplerate",
        "sort": "rating_desc",
        "page_size": 5,
    })
    try:
        return get(f"{API}/search/text/?{params}", k).get("results", [])
    except urllib.error.HTTPError as e:
        print(f"    search failed ({e.code}) for {q!r}")
        return []


def mean_dbfs(blob: bytes) -> float:
    """Measure a candidate before accepting it.

    The first version of this script took the top-rated search hit and wrote it
    straight to disk. One of the five came back at -61.7 dBFS — effectively
    silence — because Freesound's rating says nothing about whether a clip is
    loud enough to use. Rating is a popularity signal, not a level check.
    """
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
        tf.write(blob)
        path = tf.name
    try:
        r = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", path,
             "-af", "volumedetect", "-f", "null", "/dev/null"],
            capture_output=True, text=True)
        m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
        return float(m.group(1)) if m else -99.0
    finally:
        os.unlink(path)


USABLE_DBFS = -38.0     # quieter than this needs so much gain the noise floor comes with it


def main():
    k = key()
    mf = HERE / "sfx-manifest.json"
    data = json.loads(mf.read_text()) if mf.is_file() else {"assets": []}
    have = {a["asset_id"] for a in data["assets"]}
    hashes = {a.get("content_hash") for a in data["assets"]}
    added = 0

    for slug, (queries, maxdur, why) in WANTED.items():
        aid = f"sfx-{slug}"
        if aid in have:
            print(f"{slug:20} already in library — skipped")
            continue
        # Gather candidates across every query, then pick on measured level.
        cands, seen_ids = [], set()
        for q in queries:
            for r in search(q, maxdur, k):
                if r["id"] not in seen_ids:
                    seen_ids.add(r["id"])
                    cands.append((r, q))
            if len(cands) >= 6:
                break
        if not cands:
            print(f"{slug:20} NO CC0 MATCH after {len(queries)} queries")
            continue

        best = None
        for r, q in cands[:6]:
            u = r["previews"].get("preview-hq-mp3") or r["previews"].get("preview-hq-ogg")
            try:
                b = get(u, k, raw=True)
            except urllib.error.HTTPError:
                continue
            lvl = mean_dbfs(b)
            if best is None or lvl > best[2]:
                best = (r, q, lvl, b)
            if lvl >= USABLE_DBFS:
                break
        if best is None:
            print(f"{slug:20} candidates unreadable")
            continue
        hit, used_q, level, blob = best
        if level < USABLE_DBFS:
            print(f"{slug:20} REJECTED — best of {len(cands)} is {level:.1f} dBFS, "
                  f"below the {USABLE_DBFS:.0f} dBFS floor")
            continue
        h = "sha256:" + hashlib.sha256(blob).hexdigest()[:32]
        if h in hashes:
            print(f"{slug:20} duplicate content — skipped")
            continue
        path = HERE / f"{slug}.mp3"
        path.write_bytes(blob)
        hashes.add(h)
        data["assets"].append({
            "asset_id": aid,
            "type": "sfx",
            "local_path": f"office/asset-library/sfx/{slug}.mp3",
            "source": "freesound",
            "source_url": hit["url"],
            "freesound_id": hit["id"],
            "creator": hit["username"],
            "license": "CC0-1.0",
            "attribution": None,          # CC0 requires none; creator kept anyway
            "commercial_use": True,
            "duration": round(hit["duration"], 2),
            "original_resolution": f'{hit.get("samplerate","?")} Hz (preview: HQ mp3)',
            "reason_selected": f"{why} · matched query {used_q!r}",
            "content_hash": h,
            "used_in": [],
            "mean_dbfs": round(level, 1),
            "note": "HQ mp3 preview — original download needs OAuth2, unavailable with a token key",
        })
        added += 1
        print(f"{slug:20} #{hit['id']:<9} {hit['duration']:5.1f}s  {level:6.1f} dBFS  "
              f"by {hit['username'][:16]:16} {len(blob)//1024:4d} KB  (best of {len(cands)})")

    mf.write_text(json.dumps(data, indent=2) + "\n")
    bad = [a for a in data["assets"] if a["license"] in (None, "UNKNOWN")]
    print(f"\n{added} fetched · {len(data['assets'])} assets in library · "
          f"{len(bad)} with UNKNOWN licence (must be 0)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
