#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
from datetime import datetime, timezone
from pathlib import Path


def extract_feedback(generated_path: Path, final_path: Path) -> dict:
    generated = generated_path.read_text(encoding="utf-8").splitlines()
    final = final_path.read_text(encoding="utf-8").splitlines()
    diff = list(difflib.unified_diff(generated, final, fromfile=str(generated_path), tofile=str(final_path), lineterm=""))
    additions = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    return {
        "generated_path": str(generated_path),
        "final_path": str(final_path),
        "generated_lines": len(generated),
        "final_lines": len(final),
        "additions": additions,
        "deletions": deletions,
        "diff_excerpt": diff[:80],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a simple edit summary")
    parser.add_argument("--generated", required=True)
    parser.add_argument("--final", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    summary = extract_feedback(Path(args.generated), Path(args.final))
    Path(args.output).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
