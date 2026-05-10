#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

required_files=(
  "prototype/html/index.html"
  "prototype/html/styles.css"
  "prototype/html/app.js"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "missing prototype file: $file" >&2
    exit 1
  fi
done

node --check prototype/html/app.js >/dev/null

echo "check-prototype passed"

