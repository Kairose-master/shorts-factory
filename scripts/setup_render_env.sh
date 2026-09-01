#!/usr/bin/env bash
# Install the Tier 0 render toolchain: ffmpeg, yt-dlp, a Korean font, and
# optionally whisper.cpp. Idempotent — safe to re-run.
#
#   bash scripts/setup_render_env.sh                 render tools only
#   bash scripts/setup_render_env.sh --with-whisper  also build whisper.cpp
#
# Works on macOS and Linux. On macOS it uses Homebrew, which is both simpler
# and better than the workarounds below it: those exist only because this
# project's cloud container has a broken apt and a blocked CDN.
#
# whisper.cpp needs huggingface.co for the model, which the cloud container
# blocks — there, transcription falls back to Gemini. On your own machine
# whisper is free, unlimited, and its timings do not drift.
# See docs/porting-to-your-claude.md.
set -euo pipefail

say()  { printf '\033[1m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[33m    %s\033[0m\n' "$*"; }

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# Fonts live in the repo, not the system. libass is pointed at this directory
# explicitly, so the render looks identical on every machine and nothing has
# to be installed with admin rights.
FONT_DIR=${FONT_DIR:-$REPO_ROOT/assets/fonts}
WITH_WHISPER=0
[ "${1:-}" = "--with-whisper" ] && WITH_WHISPER=1

case "$(uname -s)" in
  Darwin) OS=mac ;;
  *)      OS=linux ;;
esac
say "platform: $OS"

# pip on a system Python is often marked externally managed (PEP 668), which
# is a refusal rather than a failure — retry into the user site instead.
pip_install() {
  python3 -m pip install --quiet "$@" 2>/dev/null \
    || python3 -m pip install --quiet --user "$@" 2>/dev/null \
    || python3 -m pip install --quiet --break-system-packages "$@"
}

# ---------------------------------------------------------------- ffmpeg ----
say "ffmpeg"
if ! command -v ffmpeg >/dev/null 2>&1; then
  if [ "$OS" = mac ]; then
    command -v brew >/dev/null 2>&1 || {
      echo "Homebrew is required. Install it first:"
      echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
      exit 1; }
    brew install ffmpeg
  else
    # apt is unusable in the cloud container and the static-build host is
    # blocked there, but PyPI is not: the imageio-ffmpeg wheel carries the
    # same static build.
    pip_install imageio-ffmpeg
    FF=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
    ln -sf "$FF" /usr/local/bin/ffmpeg
  fi
fi
ffmpeg -hide_banner -version | head -1

# ---------------------------------------------------------------- yt-dlp ----
say "yt-dlp"
if ! command -v yt-dlp >/dev/null 2>&1; then
  if [ "$OS" = mac ]; then brew install yt-dlp; else pip_install yt-dlp; fi
fi
yt-dlp --version

# ------------------------------------------------------------ Korean font ----
# Without a CJK face libass burns Korean as tofu. Google Fonts is blocked in
# the cloud container but the npm registry is not, and @fontsource ships the
# Korean subset as woff2, which fontTools converts back to TTF.
say "Korean font (Noto Sans KR) → $FONT_DIR"
if [ ! -f "$FONT_DIR/NotoSansKR-Regular.ttf" ]; then
  command -v npm >/dev/null 2>&1 || {
    echo "npm is required to fetch the font."
    [ "$OS" = mac ] && echo "  brew install node" || echo "  install Node.js first"
    exit 1; }
  pip_install fonttools brotli
  mkdir -p "$FONT_DIR"
  work=$(mktemp -d)
  ( cd "$work"
    npm pack @fontsource/noto-sans-kr@5 >/dev/null 2>&1
    tar xzf fontsource-noto-sans-kr-*.tgz )
  python3 - "$work" "$FONT_DIR" <<'PY'
import sys
from fontTools.ttLib import TTFont
work, out = sys.argv[1], sys.argv[2]
for weight, name in (("400", "Regular"), ("700", "Bold")):
    f = TTFont(f"{work}/package/files/noto-sans-kr-korean-{weight}-normal.woff2")
    f.flavor = None
    f.save(f"{out}/NotoSansKR-{name}.ttf")
    print(f"  wrote {out}/NotoSansKR-{name}.ttf")
PY
  rm -rf "$work"
fi
ls -1 "$FONT_DIR"/NotoSansKR-*.ttf

# ---------------------------------------------------------- whisper.cpp ----
if [ "$WITH_WHISPER" = 1 ]; then
  say "whisper.cpp + large-v3"
  if [ "$OS" = mac ]; then
    command -v cmake >/dev/null 2>&1 || brew install cmake
  else
    command -v cmake >/dev/null 2>&1 || warn "cmake not found — install it and re-run"
  fi
  WHISPER_DIR=${WHISPER_DIR:-$HOME/whisper.cpp}
  [ -d "$WHISPER_DIR" ] || git clone --depth 1 https://github.com/ggml-org/whisper.cpp "$WHISPER_DIR"
  ( cd "$WHISPER_DIR"
    cmake -B build -DCMAKE_BUILD_TYPE=Release >/dev/null
    cmake --build build -j --config Release >/dev/null
    # large-v3, never a *.en model — those are English-only and cannot read Korean.
    [ -f models/ggml-large-v3.bin ] || bash ./models/download-ggml-model.sh large-v3 )
  echo
  echo "Add these two lines to ~/.zshrc, then open a new terminal:"
  echo "  export PATH=\"$WHISPER_DIR/build/bin:\$PATH\""
  echo "  export WHISPER_MODEL=\"$WHISPER_DIR/models/ggml-large-v3.bin\""
fi

say "Done."
echo "Font dir: $FONT_DIR  (FontName=Noto Sans KR)"
[ "$WITH_WHISPER" = 1 ] || echo "Transcription: add --with-whisper for the free offline route."
