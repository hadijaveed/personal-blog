#!/usr/bin/env bash
#
# render.sh — headless Chrome screenshot helper for claude-design-diagram.
#
# Reads HTML files from docs/assets/diagrams/src/ and writes 1600x900 PNGs
# to docs/assets/diagrams/.
#
# Usage:
#   ./render.sh <slug>        # render a single diagram (e.g. "01-breadth")
#   ./render.sh --all         # render every .html in src/
#   ./render.sh <path/to.html> # render an arbitrary HTML file in place
#
# Requires Google Chrome installed at the standard macOS path.

set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then
  echo "error: Google Chrome not found at $CHROME" >&2
  exit 1
fi

# Resolve repo root from this script's location.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/../../.." && pwd )"
SRC_DIR="$REPO_ROOT/docs/assets/diagrams/src"
OUT_DIR="$REPO_ROOT/docs/assets/diagrams"
PROFILE_BASE="${TMPDIR:-/tmp}/claude-design-diagram-profiles"

mkdir -p "$OUT_DIR" "$PROFILE_BASE"

render_one() {
  local html_path="$1"
  local out_path="$2"
  local slug
  slug="$(basename "$html_path" .html)"
  local profile="$PROFILE_BASE/$slug-$$"

  echo "rendering $slug → $out_path"
  "$CHROME" \
    --headless=new \
    --disable-gpu \
    --hide-scrollbars \
    --window-size=1600,900 \
    --user-data-dir="$profile" \
    --screenshot="$out_path" \
    "file://$html_path" >/dev/null 2>&1

  rm -rf "$profile"
}

if [ $# -eq 0 ]; then
  echo "usage: $0 <slug> | --all | <path/to.html>" >&2
  exit 1
fi

if [ "$1" = "--all" ]; then
  shopt -s nullglob
  files=("$SRC_DIR"/*.html)
  if [ ${#files[@]} -eq 0 ]; then
    echo "no html files in $SRC_DIR" >&2
    exit 1
  fi
  for f in "${files[@]}"; do
    slug="$(basename "$f" .html)"
    render_one "$f" "$OUT_DIR/$slug.png"
  done
else
  arg="$1"
  if [ -f "$arg" ]; then
    # arbitrary path
    slug="$(basename "$arg" .html)"
    render_one "$arg" "$OUT_DIR/$slug.png"
  elif [ -f "$SRC_DIR/$arg.html" ]; then
    render_one "$SRC_DIR/$arg.html" "$OUT_DIR/$arg.png"
  elif [ -f "$SRC_DIR/$arg" ]; then
    slug="$(basename "$arg" .html)"
    render_one "$SRC_DIR/$arg" "$OUT_DIR/$slug.png"
  else
    echo "error: could not find HTML for '$arg'" >&2
    echo "  tried: $arg" >&2
    echo "  tried: $SRC_DIR/$arg.html" >&2
    echo "  tried: $SRC_DIR/$arg" >&2
    exit 1
  fi
fi

echo "done."
