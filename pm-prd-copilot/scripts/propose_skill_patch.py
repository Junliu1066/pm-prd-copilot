#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a weekly skill-upgrade proposal")
    parser.add_argument("--base-dir", default=".")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    proposals_dir = base_dir / "pm-prd-copilot" / "proposals" / "memory"
    patch_dir = base_dir / "pm-prd-copilot" / "proposals" / "skill-patches"
    patch_dir.mkdir(parents=True, exist_ok=True)
    proposal_files = sorted(proposals_dir.glob("*.md"))

    lines = [
        f"# Skill Upgrade Proposal - {datetime.utcnow().strftime('%Y-%m-%d')}",
        "",
        "This file is a reviewed change proposal. It must not be applied automatically.",
        "",
        "## Inputs considered",
    ]
    if proposal_files:
        lines.extend(f"- `{path.name}`" for path in proposal_files[-10:])
    else:
        lines.append("- No memory proposals found.")

    lines.extend(
        [
            "",
            "## Suggested stable-layer changes",
            "- Consider tightening default structure for requirement summaries.",
            "- Consider expanding explicit risk prompts if accepted repeatedly.",
            "- Consider updating templates only if the same edit appears across multiple approved proposals.",
            "",
            "## Required checks before merge",
            "- [ ] Regression passed",
            "- [ ] Schema compatibility unchanged",
            "- [ ] Human review completed",
            "",
        ]
    )

    output_path = patch_dir / f"{datetime.utcnow().strftime('%Y-%m-%d')}-skill-upgrade-proposal.md"
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
