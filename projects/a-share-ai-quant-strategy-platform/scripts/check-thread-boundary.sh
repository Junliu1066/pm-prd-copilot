#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

THREAD_NAME="${THREAD:-}"
if [[ -z "$THREAD_NAME" ]]; then
  THREAD_NAME="$(git -C "$ROOT" branch --show-current 2>/dev/null || true)"
fi

if [[ -z "$THREAD_NAME" || "$THREAD_NAME" != codex/* ]]; then
  echo "check-thread-boundary skipped: set THREAD=codex/<branch> to enforce file boundaries"
  exit 0
fi

matches_any() {
  local file="$1"
  shift
  local pattern
  for pattern in "$@"; do
    if [[ "$file" == $pattern ]]; then
      return 0
    fi
  done
  return 1
}

case "$THREAD_NAME" in
  codex/p0-docs)
    allowed_patterns=(
      "AGENTS.md"
      "*.md"
      "automation/**"
      "tasks/**"
      "scripts/**"
      "Makefile"
    )
    ;;
  codex/p0-spring-api)
    allowed_patterns=(
      "backend/pom.xml"
      "backend/mvnw"
      "backend/mvnw.cmd"
      "backend/.mvn/**"
      "backend/common/**"
      "backend/auth/**"
      "backend/user/**"
      "backend/config/**"
      "backend/src/main/java/com/aquant/AQuantApplication.java"
      "backend/src/main/java/com/aquant/common/**"
      "backend/src/main/java/com/aquant/auth/**"
      "backend/src/main/java/com/aquant/user/**"
      "backend/src/main/resources/application*.yml"
      "backend/src/test/java/com/aquant/common/**"
      "backend/src/test/java/com/aquant/auth/**"
      "backend/src/test/java/com/aquant/user/**"
      "api/**"
      "tests/backend/**"
      "08_backend_engineering_spec.md"
    )
    ;;
  codex/p0-quant-engine)
    allowed_patterns=(
      "backend/marketdata/**"
      "backend/indicator/**"
      "backend/strategyengine/**"
      "backend/backtest/**"
      "backend/risk/**"
      "backend/src/main/java/com/aquant/marketdata/**"
      "backend/src/main/java/com/aquant/indicator/**"
      "backend/src/main/java/com/aquant/strategyengine/**"
      "backend/src/main/java/com/aquant/backtest/**"
      "backend/src/main/java/com/aquant/risk/**"
      "backend/src/test/java/com/aquant/marketdata/**"
      "backend/src/test/java/com/aquant/indicator/**"
      "backend/src/test/java/com/aquant/strategyengine/**"
      "backend/src/test/java/com/aquant/backtest/**"
      "backend/src/test/java/com/aquant/risk/**"
      "tests/quant/**"
    )
    ;;
  codex/p0-points)
    allowed_patterns=(
      "backend/points/**"
      "backend/src/main/java/com/aquant/points/**"
      "backend/src/test/java/com/aquant/points/**"
      "tests/points/**"
    )
    ;;
  codex/p0-web-prototype)
    allowed_patterns=(
      "prototype/html/**"
      "02_prototype_layer.md"
    )
    ;;
  codex/p0-miniapp-frontend)
    allowed_patterns=(
      "miniapp/**"
      "tests/miniapp/**"
    )
    ;;
  codex/p0-web-frontend)
    allowed_patterns=(
      "web/**"
      "tests/web/**"
    )
    ;;
  codex/p0-admin)
    allowed_patterns=(
      "admin/**"
      "backend/admin/**"
      "backend/src/main/java/com/aquant/admin/**"
      "backend/src/test/java/com/aquant/admin/**"
      "tests/admin/**"
    )
    ;;
  codex/ai-compliance)
    allowed_patterns=(
      "backend/ai/**"
      "backend/risk/**"
      "backend/src/main/java/com/aquant/ai/**"
      "backend/src/main/java/com/aquant/risk/**"
      "backend/src/test/java/com/aquant/ai/**"
      "backend/src/test/java/com/aquant/risk/**"
      "prompts/**"
      "tests/ai/**"
      "tests/compliance/**"
    )
    ;;
  codex/p1-arena)
    allowed_patterns=(
      "backend/arena/**"
      "backend/src/main/java/com/aquant/arena/**"
      "backend/src/test/java/com/aquant/arena/**"
      "arena/**"
      "tests/arena/**"
    )
    ;;
  codex/qa-gates)
    allowed_patterns=(
      "scripts/**"
      "tests/**"
      "Makefile"
      "10_test_plan.md"
      "19_merge_review_checklist.md"
    )
    ;;
  *)
    echo "unknown THREAD for boundary check: $THREAD_NAME" >&2
    echo "add this branch to scripts/check-thread-boundary.sh before using it" >&2
    exit 1
    ;;
esac

if ! git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "check-thread-boundary skipped: not inside a git worktree"
  exit 0
fi

changed_files=()
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  path="${line:3}"
  if [[ "$path" == *" -> "* ]]; then
    path="${path##* -> }"
  fi
  path="${path#\"}"
  path="${path%\"}"
  path="${path#./}"
  project_prefix="projects/a-share-ai-quant-strategy-platform/"
  path="${path#$project_prefix}"
  changed_files+=("$path")
done < <(git -C "$ROOT" status --short --untracked-files=all -- .)

if [[ "${#changed_files[@]}" -eq 0 ]]; then
  echo "check-thread-boundary passed: no changed files"
  exit 0
fi

violations=()
for file in "${changed_files[@]}"; do
  if ! matches_any "$file" "${allowed_patterns[@]}"; then
    violations+=("$file")
  fi
done

if [[ "${#violations[@]}" -ne 0 ]]; then
  echo "file boundary violations for $THREAD_NAME:" >&2
  printf '  %s\n' "${violations[@]}" >&2
  if ! git -C "$ROOT" ls-files --error-unmatch AGENTS.md >/dev/null 2>&1; then
    echo "hint: AGENTS.md is not tracked, so the project may not have a git baseline yet" >&2
    echo "hint: create the initial baseline commit before enforcing thread-specific boundaries" >&2
  fi
  echo "allowed patterns:" >&2
  printf '  %s\n' "${allowed_patterns[@]}" >&2
  exit 1
fi

echo "check-thread-boundary passed for $THREAD_NAME"
