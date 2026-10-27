#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -x "$ROOT/.venv/bin/sphinx-build" ]]; then
  SPHINX_BUILD="$ROOT/.venv/bin/sphinx-build"
elif command -v sphinx-build >/dev/null 2>&1; then
  SPHINX_BUILD="$(command -v sphinx-build)"
else
  echo "[docs] 未找到 sphinx-build。请先执行：python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 127
fi

# 1) Rebuild the searchable error-code table from checked-in manual data.
python3 scripts/generate_error_codes.py

# 2) Rebuild the two independent language sites into one publishable tree.
HTML_OUTPUT="$ROOT/build/html"
if [[ "$HTML_OUTPUT" != "$ROOT/build/html" || "$HTML_OUTPUT" == "/" ]]; then
  echo "[docs] 非法 HTML 输出目录: $HTML_OUTPUT" >&2
  exit 2
fi
rm -rf -- "$HTML_OUTPUT"
rm -rf -- "$ROOT/build/doctrees/zh_CN" "$ROOT/build/doctrees/en"

"$SPHINX_BUILD" -b html -W --keep-going -c docs/zh_CN -d "$ROOT/build/doctrees/zh_CN" docs/zh_CN "$HTML_OUTPUT"
"$SPHINX_BUILD" -b html -W --keep-going -c docs/en -d "$ROOT/build/doctrees/en" docs/en "$HTML_OUTPUT/en"

test -s "$HTML_OUTPUT/index.html"
test -s "$HTML_OUTPUT/en/index.html"
