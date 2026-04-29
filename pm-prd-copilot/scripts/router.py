#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from closeout_project import generate_closeout_package
from select_ui_style import generate_style_direction


PROJECT_FILES = [
    "00_raw_input.md",
    "01_requirement_brief.json",
    "01_requirement_brief.md",
    "01_requirement_brief.meta.json",
    "02_prd.generated.json",
    "02_prd.generated.md",
    "02_prd.generated.meta.json",
    "02_prd.final.md",
    "03_user_stories.generated.json",
    "03_user_stories.generated.md",
    "03_user_stories.generated.meta.json",
    "03_user_stories.final.md",
    "04_risk_check.generated.json",
    "04_risk_check.md",
    "04_risk_check.generated.md",
    "04_risk_check.generated.meta.json",
    "05_tracking_plan.generated.json",
    "05_tracking_plan.md",
    "05_tracking_plan.generated.md",
    "05_tracking_plan.generated.meta.json",
    "06_review_merge.md",
]


def init_project(base_dir: Path, project: str, title: str) -> None:
    project_dir = base_dir / "projects" / project
    project_dir.mkdir(parents=True, exist_ok=True)
    for filename in PROJECT_FILES:
        target = project_dir / filename
        if target.exists():
            continue
        if filename.endswith(".json"):
            if filename.endswith(".meta.json"):
                target.write_text("{}\n", encoding="utf-8")
                continue
            target.write_text(
                json.dumps(
                    {
                        "project_id": project,
                        "title": title,
                        "status": "draft",
                        "facts": [],
                        "assumptions": [],
                        "open_questions": [],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        else:
            target.write_text(f"# {title}\n\n", encoding="utf-8")


def show_status(base_dir: Path, project: str) -> None:
    project_dir = base_dir / "projects" / project
    if not project_dir.exists():
        raise SystemExit(f"Project not found: {project_dir}")
    for filename in PROJECT_FILES:
        target = project_dir / filename
        state = "present" if target.exists() else "missing"
        print(f"{state:7} {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PM PRD Copilot project router")
    parser.add_argument("--base-dir", default=".", help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-project")
    init_parser.add_argument("--project", required=True)
    init_parser.add_argument("--title", required=True)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--project", required=True)

    closeout_parser = subparsers.add_parser("closeout")
    closeout_parser.add_argument("--project", required=True)
    closeout_parser.add_argument("--run-id", default="")
    closeout_parser.add_argument(
        "--output-dir",
        default="",
        help="Optional closeout output directory. Defaults to projects/<project>/closeout.",
    )

    ui_style_parser = subparsers.add_parser("ui-style")
    ui_style_parser.add_argument("--project", required=True)
    ui_style_parser.add_argument(
        "--style",
        default="",
        help="Optional explicit style alias, e.g. concrete, swiss, glass, 水泥风.",
    )

    args = parser.parse_args()
    base_dir = Path(args.base_dir).resolve()

    if args.command == "init-project":
        init_project(base_dir, args.project, args.title)
    elif args.command == "status":
        show_status(base_dir, args.project)
    elif args.command == "closeout":
        output_dir = Path(args.output_dir).resolve() if args.output_dir else None
        outputs = generate_closeout_package(base_dir, args.project, run_id=args.run_id, output_dir=output_dir)
        print("Closeout dry-run package generated:")
        for label, path in outputs.items():
            print(f"- {label}: {path}")
    elif args.command == "ui-style":
        outputs = generate_style_direction(base_dir, args.project, requested_style=args.style)
        print("UI style direction generated:")
        for label, path in outputs.items():
            print(f"- {label}: {path}")


if __name__ == "__main__":
    main()
