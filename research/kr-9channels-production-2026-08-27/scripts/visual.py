#!/usr/bin/env python3
"""Measure how each channel's top Short was actually MADE, not what it is about."""
import json, os, sys, time, urllib.request
from pathlib import Path

KEY = os.environ["GEMINI_API_KEY"]
OUT = Path(__file__).resolve().parent
MODEL = "gemini-3.6-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"

PROMPT = """You are a video production analyst. Watch this Short and report ONLY on how it
was physically made. Ignore the topic. Answer as strict JSON with these keys:

"face_on_camera": one of "none" | "creator" | "third_party_footage_only"
"visual_layers": array of the layers actually present, from:
  ["still_photo","archival_video","broadcast_clip","2d_animation","illustration",
   "screen_recording","tabletop_hands","stock_video","text_card","chart_or_diagram",
   "map","generated_image"]
"dominant_layer": the one that occupies most screen time
"camera_moves": array from ["none","ken_burns_push","ken_burns_pan","whip_cut","zoom_punch"]
"text_treatment": one of "burned_captions_full" | "keyword_pop" | "title_card_only" | "none"
"cuts_per_10s": integer estimate
"music": one of "none" | "bed_only" | "bed_plus_sfx"
"narration": one of "none" | "human_vo" | "tts_like" | "on_screen_dialogue"
"reproducible_faceless_with_code": true or false — could an agent rebuild this look using
  ONLY code-drawn graphics (text, shapes, charts), public-domain stills, and TTS?
"what_would_be_missing": one short sentence naming the asset an agent could NOT generate
"first_3_seconds": one sentence describing literally what is on screen at 0:00-0:03

Return the JSON object and nothing else."""

deep = json.loads((OUT / "deep.json").read_text())
CACHE = OUT / "visual.json"
have = json.loads(CACHE.read_text()) if CACHE.exists() else {}

for h, vids in deep.items():
    v = vids[0]
    if v["id"] in have:
        continue
    body = json.dumps({"contents": [{"parts": [
        {"file_data": {"file_uri": v["url"]}}, {"text": PROMPT}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}}).encode()
    ok = False
    for a in range(3):
        try:
            req = urllib.request.Request(URL, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                res = json.loads(r.read())
            txt = res["candidates"][0]["content"]["parts"][0]["text"]
            have[v["id"]] = {"channel": h, "title": v["title"], "url": v["url"],
                             "multiple": v["multiple"], **json.loads(txt)}
            CACHE.write_text(json.dumps(have, ensure_ascii=False, indent=1))
            a_ = have[v["id"]]
            print(f"  {h:<12} face={a_['face_on_camera']:<22} dom={a_['dominant_layer']:<16} "
                  f"code_reproducible={a_['reproducible_faceless_with_code']}")
            ok = True
            break
        except Exception as exc:
            if a == 2:
                print(f"  FAIL {h}: {str(exc)[:110]}", file=sys.stderr)
            else:
                time.sleep(5 * (a + 1))
    if not ok:
        continue

print(f"\n{len(have)}/{len(deep)} analysed → {CACHE}")
