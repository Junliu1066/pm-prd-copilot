#!/usr/bin/env bash
set -u

BASE_DIR="."
PROJECT=""
MODE="advisory"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --base-dir)
      BASE_DIR="${2:-.}"
      shift 2
      ;;
    --project)
      PROJECT="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-advisory}"
      shift 2
      ;;
    -h|--help)
      echo "Usage: harness/run_validation.sh [--base-dir .] [--project demo-project] [--mode advisory|strict]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

cd "$BASE_DIR" || exit 2

if [ -x ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
else
  PYTHON="python3"
fi

echo "== Runtime validation =="
echo "Base dir: $(pwd)"
echo "Python: $PYTHON"

"$PYTHON" - <<'PY'
import importlib.util
import sys

missing = [name for name in ("yaml", "jsonschema") if importlib.util.find_spec(name) is None]
if missing:
    print("Missing Python dependencies: " + ", ".join(missing))
    print("Install dependencies with: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt")
    sys.exit(2)
print("Dependency check: ok")
PY
dep_status=$?
if [ "$dep_status" -ne 0 ]; then
  exit "$dep_status"
fi

"$PYTHON" - <<'PY'
from pathlib import Path
import sys
import yaml

paths = [
    Path("registry/artifacts.yaml"),
    Path("registry/skills.yaml"),
    Path("registry/stewards.yaml"),
    Path("registry/mcps.yaml"),
    Path("registry/plugins.yaml"),
    Path("governance/efficiency_policy.yaml"),
    Path("governance/teaching_policy.yaml"),
    Path("governance/random_audit_policy.yaml"),
    Path("governance/steward_scaling_policy.yaml"),
    Path("governance/steward_operating_rules.yaml"),
    Path("governance/runtime/triggers.yaml"),
    Path("governance/runtime/artifact_controls/control_manifest.yaml"),
]

failed = False
for path in paths:
    if not path.exists():
        print(f"YAML missing: {path}")
        failed = True
        continue
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"YAML invalid: {path}: {exc}")
        failed = True
    else:
        print(f"YAML ok: {path}")

sys.exit(1 if failed else 0)
PY
yaml_status=$?
if [ "$yaml_status" -ne 0 ]; then
  exit "$yaml_status"
fi

"$PYTHON" - <<'PY'
from pathlib import Path
import sys

required = [
    Path("governance/runtime/index.md"),
    Path("governance/runtime/triggers.yaml"),
    Path("governance/runtime/document_boundaries.md"),
    Path("governance/runtime/artifact_controls/index.md"),
    Path("pm-prd-copilot/templates/codex_development_document_template.md"),
]

missing = [str(path) for path in required if not path.exists()]
if missing:
    print("Required runtime files missing:")
    for path in missing:
        print(f"- {path}")
    sys.exit(1)

template = Path("pm-prd-copilot/templates/codex_development_document_template.md").read_text(encoding="utf-8")
pointer = "<!-- codex-runtime: apply governance/runtime/artifact_controls/index.md when updating this artifact -->"
if pointer not in template:
    print("Template missing runtime pointer.")
    sys.exit(1)

print("Runtime file check: ok")
PY
runtime_status=$?
if [ "$runtime_status" -ne 0 ]; then
  exit "$runtime_status"
fi

if [ -z "$PROJECT" ]; then
  if [ -d "projects/demo-project" ]; then
    PROJECT="demo-project"
  else
    echo "No project specified and projects/demo-project is missing; skipping full harness."
    exit 0
  fi
fi

echo "Running governance harness for project: $PROJECT"
"$PYTHON" harness/run_harness.py --base-dir . --project "$PROJECT" --mode "$MODE"
