"""Burned-in captions driven by TTS word boundaries.

Every one of the nine Korean Shorts channels measured on 2026-08-27 burns full
captions — 9 of 9, no exceptions. In that niche captions are not a style choice,
they are the entry fee, and they are what a muted feed actually reads.

    import captions
    chunks = captions.chunk(scene["words"], max_chars=16)   # once, outside the loop
    captions.draw(d, chunks, tl, font, y=1180, ...)         # once per frame

`chunk` groups word timings into caption cards; `draw` paints the card that is
live at time `tl` and tints the word currently being spoken.
"""
from __future__ import annotations

# Characters per caption card. Korean packs ~2x the meaning per character of
# English, so a Korean card holds fewer characters and stays on screen longer.
DEFAULTS = {"korean": 16, "latin": 34}


def is_cjk(s: str) -> bool:
    return any("　" <= c <= "鿿" or "가" <= c <= "힯" for c in s)


def chunk(words, max_chars: int | None = None, max_gap: float = 0.45,
          min_dur: float = 0.7, tail: float = 0.35):
    """Group `words` (from plan.json) into caption cards.

    Splits on three things, in priority order: a pause longer than `max_gap`,
    a card that would exceed `max_chars`, and sentence-final punctuation. Each
    card carries its own words so the live word can be highlighted.
    """
    if not words:
        return []
    if max_chars is None:
        max_chars = DEFAULTS["korean"] if is_cjk("".join(w["text"] for w in words)) \
            else DEFAULTS["latin"]

    cards, cur = [], []
    for i, w in enumerate(words):
        gap = w["t"] - (words[i - 1]["t"] + words[i - 1].get("dur", 0)) if i else 0
        text_len = sum(len(x["text"]) + 1 for x in cur) + len(w["text"])
        if cur and (gap > max_gap or text_len > max_chars):
            cards.append(cur)
            cur = []
        cur.append(w)
        if w["text"].rstrip()[-1:] in ".?!。？！":
            cards.append(cur)
            cur = []
    if cur:
        cards.append(cur)

    out = []
    for k, c in enumerate(cards):
        start = c[0]["t"]
        last_end = c[-1]["t"] + (c[-1].get("dur") or 0.3)
        nxt = cards[k + 1][0]["t"] if k + 1 < len(cards) else last_end + tail
        out.append({"start": start,
                    "end": max(nxt, start + min_dur) if k + 1 < len(cards)
                           else last_end + tail,
                    "text": " ".join(w["text"] for w in c),
                    "words": c})
    return out


def active(cards, t: float):
    for c in cards:
        if c["start"] <= t < c["end"]:
            return c
    return None


def draw(d, cards, t: float, font, y: int, left: int, right: int,
         fill=(255, 255, 255), highlight=None, shadow=(0, 0, 0),
         align: str = "center", stroke: int = 6):
    """Paint the live caption card. Returns the card, or None.

    A stroke rather than a plate: a caption box hides the picture, and on a
    light background a white caption with no outline disappears entirely. The
    stroke costs nothing and survives any footage under it.
    """
    card = active(cards, t)
    if not card:
        return None

    if highlight is None:
        x = left if align == "left" else \
            right - d.textlength(card["text"], font=font) if align == "right" else \
            left + (right - left - d.textlength(card["text"], font=font)) / 2
        d.text((x, y), card["text"], font=font, fill=fill,
               stroke_width=stroke, stroke_fill=shadow)
        return card

    # word-level tint: measure the whole card, then lay words out one by one
    parts = [w["text"] for w in card["words"]]
    space = d.textlength(" ", font=font)
    widths = [d.textlength(p, font=font) for p in parts]
    total = sum(widths) + space * (len(parts) - 1)
    x = left if align == "left" else \
        right - total if align == "right" else left + (right - left - total) / 2
    for w, p, wd in zip(card["words"], parts, widths):
        live = w["t"] <= t < w["t"] + max(w.get("dur") or 0.25, 0.18)
        d.text((x, y), p, font=font, fill=highlight if live else fill,
               stroke_width=stroke, stroke_fill=shadow)
        x += wd + space
    return card


def fit(d, cards, font_for, max_width: int, start: int = 64, min_size: int = 36):
    """Largest size at which EVERY card fits on one line. Call once, not per frame.

    Sizing to the average card and letting the longest one overflow is the
    caption bug that survives QC and ruins the read.
    """
    size = start
    while size > min_size:
        f = font_for(size)
        if all(d.textlength(c["text"], font=f) <= max_width for c in cards):
            return f
        size -= 2
    return font_for(min_size)
