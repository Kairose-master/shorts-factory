#!/usr/bin/env bash
# Rebuild the Tier 0 render toolchain in a fresh container.
#
# The remote container is recycled every session, so ffmpeg, yt-dlp and the
# Korean font are gone each time you start. This script puts them back.
# It is idempotent — safe to re-run.
#
#   bash scripts/setup_render_env.sh
#
# What it does NOT do: install whisper.cpp. See docs/environment-constraints.md —
# the model weights are hosted on huggingface.co, which this environment's
# egress policy blocks. Transcription backend is selected by sermon_shorts.py.
set -euo pipefail

say() { printf '\033[1m==> %s\033[0m\n' "$*"; }

FONT_DIR=${FONT_DIR:-/usr/local/share/fonts}

# ---------------------------------------------------------------- ffmpeg ----
# apt is unusable here (archive.ubuntu.com serves 404s for several deps), and
# johnvansickle.com is blocked. The imageio-ffmpeg wheel on PyPI ships the same
# static johnvansickle build, and PyPI is reachable, so that is the way in.
say "ffmpeg"
if ! command -v ffmpeg >/dev/null 2>&1; then
  pip3 install --quiet imageio-ffmpeg
  FF=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
  ln -sf "$FF" /usr/local/bin/ffmpeg
fi
ffmpeg -hide_banner -version | head -1

# ---------------------------------------------------------------- yt-dlp ----
say "yt-dlp"
command -v yt-dlp >/dev/null 2>&1 || pip3 install --quiet yt-dlp
yt-dlp --version

# ------------------------------------------------------------ Korean font ----
# ffmpeg here is a static build without libfreetype, so drawtext is unavailable
# and subtitles must go through libass. libass needs a real TTF/OTF on disk;
# the container ships no CJK face at all, so Korean would burn in as tofu.
#
# Google Fonts (fonts.gstatic.com) is blocked, but the npm registry is not, and
# @fontsource/noto-sans-kr ships the Korean subset — as woff2. fontTools
# converts woff2 back to TTF, which libass can read.
say "Korean font (Noto Sans KR)"
if [ ! -f "$FONT_DIR/NotoSansKR-Regular.ttf" ]; then
  pip3 install --quiet fonttools brotli
  work=$(mktemp -d)
  ( cd "$work"
    npm pack @fontsource/noto-sans-kr@5 >/dev/null 2>&1
    tar xzf fontsource-noto-sans-kr-*.tgz )
  mkdir -p "$FONT_DIR"
  python3 - "$work" "$FONT_DIR" <<'PY'
import sys
from fontTools.ttLib import TTFont
work, out = sys.argv[1], sys.argv[2]
for weight, name in (("400", "Regular"), ("700", "Bold")):
    src = f"{work}/package/files/noto-sans-kr-korean-{weight}-normal.woff2"
    f = TTFont(src)
    f.flavor = None
    f.save(f"{out}/NotoSansKR-{name}.ttf")
    print(f"  wrote {out}/NotoSansKR-{name}.ttf")
PY
  rm -rf "$work"
fi
ls -1 "$FONT_DIR"/NotoSansKR-*.ttf

say "Done. Render layer ready."
echo "Font dir for ffmpeg: $FONT_DIR  (FontName=Noto Sans KR)"
