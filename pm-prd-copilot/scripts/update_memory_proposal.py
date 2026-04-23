#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def build_proposal(diff_summary: dict) -> str:
    return "\n".join(
        [
            f"# Memory Proposal - {datetime.utcnow().strftime('%Y-%m-%d')}",
            "",
            "This proposal was generated from a reviewed draft/final diff.",
            "",
            "## Source",
            f"- Generated: `{diff_summary['generated_path']}`",
            f"- Final: `{diff_summary['final_path']}`",
            "",
            "## Observed edit signal",
            f"- Added lines: {diff_summary['additions']}",
            f"- Deleted lines: {diff_summary['deletions']}",
            "",
            "## Candidate long-term preferences",
            "- Confirm whether the user prefers shorter summaries or more explicit scope.",
            "- Confirm whether more explicit acceptance criteria were added.",
            "- Confirm whether risk or dependency sections were strengthened.",
            "",
            "## Diff excerpt",
            "```diff",
            *diff_summary["diff_excerpt"],
            "```",
            "",
            "## Review decision",
            "- [ ] Accept into `memory/`",
            "- [ ] Keep as one-off change",
            "- [ ] Reject",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a reviewable memory proposal")
    parser.add_argument("--diff-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    diff_summary = json.loads(Path(args.diff_summary).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{datetime.utcnow().strftime('%Y-%m-%dT%H%M%SZ')}-memory-proposal.md"
    output_path.write_text(build_proposal(diff_summary) + "\n", encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
