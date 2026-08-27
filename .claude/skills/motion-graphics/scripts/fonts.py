"""Resolve a font that can actually draw the script's language.

PIL does not fall back: ask DejaVu for 한글 and you get tofu boxes, silently, all
the way through a render that exits 0. This module fails loudly instead, and
fetches an OFL font when the machine has none.

    import fonts
    f = fonts.korean(700)          # a path, guaranteed to carry Hangul
    mg.FONT_FILES["kr-bold"] = f
"""
from __future__ import annotations

import os
import re
import ssl
import sys
import urllib.request
from pathlib import Path

CACHE = Path(os.environ.get("MG_FONT_CACHE",
                            Path.home() / ".cache" / "motion-graphics-fonts"))
CSS = "https://fonts.googleapis.com/css2?family={fam}:wght@{w}"

#: Scripts we check coverage for, by a few characters that must be present.
PROBES = {
    "korean": "원가값의",
    "japanese": "原価円",
    "chinese": "原价值",
    "latin": "Ag1",
}


def has_glyphs(path: str | Path, probe: str) -> bool:
    """True only if every probe character has a real glyph in the cmap."""
    try:
        from fontTools.ttLib import TTCollection, TTFont
    except ImportError:  # fontTools is the only reliable check; say so
        print("  WARN: pip install fonttools to verify glyph coverage", file=sys.stderr)
        return True
    p = str(path)
    try:
        fs = TTCollection(p).fonts if p.lower().endswith(".ttc") else \
            [TTFont(p, fontNumber=0, lazy=True)]
        for f in fs:
            cm = f.getBestCmap()
            if all(ord(c) in cm for c in probe):
                return True
    except Exception:
        return False
    return False


def _ctx():
    bundle = os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt"
    if Path(bundle).is_file():
        return ssl.create_default_context(cafile=bundle)
    return ssl.create_default_context()


def google_font(family: str = "Noto Sans KR", weight: int = 700) -> Path:
    """Download one static TTF from Google Fonts into the cache. OFL licensed.

    Google serves woff2 to modern user agents and TTF to older ones; PIL reads
    TTF, so this deliberately does not set a browser UA.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"{family.replace(' ', '')}-{weight}.ttf"
    if out.is_file() and out.stat().st_size > 100_000:
        return out
    url = CSS.format(fam=family.replace(" ", "+"), w=weight)
    css = urllib.request.urlopen(url, timeout=120, context=_ctx()).read().decode()
    m = re.search(r"https://[^)\s]+\.ttf", css)
    if not m:
        raise RuntimeError(f"Google Fonts returned no TTF for {family} {weight}. "
                           f"Fetch it manually into {CACHE}.")
    data = urllib.request.urlopen(m.group(0), timeout=300, context=_ctx()).read()
    out.write_bytes(data)
    print(f"  fetched {family} {weight} → {out} ({len(data) / 1e6:.1f} MB, OFL)")
    return out


#: System families that are genuinely designed for each script. A font can
#: carry a script's codepoints and still be the wrong typeface for it — WenQuanYi
#: has Hangul because it is a pan-CJK face, and its 한글 reads as foreign to a
#: Korean viewer. Coverage is not suitability.
NATIVE = {
    "korean": ("notosanskr", "notoserifkr", "nanum", "malgun", "pretendard",
               "spoqa", "gothica1", "blackhansans"),
    "japanese": ("notosansjp", "notoserifjp", "ipa", "meiryo", "yugothic"),
    "chinese": ("notosanssc", "notosanstc", "wqy", "sourcehansans"),
    "latin": ("dejavu", "liberation", "noto", "free"),
}


def resolve(script: str = "korean", weight: int = 700,
            family: str = "Noto Sans KR") -> str:
    """A font path that really draws `script`, in a face meant for it.

    Order: cache → a *native* system family → OFL download → any covering font
    with a warning. Coverage alone is the last resort, never the first choice.
    """
    probe = PROBES[script]
    native = NATIVE.get(script, ())

    cached = CACHE / f"{family.replace(' ', '')}-{weight}.ttf"
    if cached.is_file() and has_glyphs(cached, probe):
        return str(cached)

    import glob
    system = sorted(glob.glob("/usr/share/fonts/**/*.tt[cf]", recursive=True) +
                    glob.glob("/usr/share/fonts/**/*.otf", recursive=True))
    for p in system:
        stem = Path(p).stem.lower().replace("-", "").replace("_", "")
        if any(n in stem or n in p.lower() for n in native) and has_glyphs(p, probe):
            print(f"  native system font for {script}: {p}")
            return p

    try:
        return str(google_font(family, weight))
    except Exception as exc:
        for p in system:
            if has_glyphs(p, probe) and "unifont" not in p.lower():
                print(f"  WARN: no {script} face and the OFL download failed "
                      f"({exc}). Falling back to {p}, which covers the script "
                      f"but was not designed for it — say so in the report.",
                      file=sys.stderr)
                return p
        raise RuntimeError(
            f"No font on this machine draws {script} ({probe!r}) and the OFL "
            f"download failed: {exc}\nInstall one, or drop a TTF into {CACHE}."
        ) from exc


def korean(weight: int = 700) -> str:
    return resolve("korean", weight, "Noto Sans KR")


if __name__ == "__main__":
    for w in (400, 700, 900):
        p = korean(w)
        print(f"  korean {w}: {p}  hangul={has_glyphs(p, PROBES['korean'])}")
