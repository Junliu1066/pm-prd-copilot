#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from pipeline_common import (
    build_value_gate,
    project_paths,
    read_json,
    read_text,
    validate_schema,
    value_gate_markdown,
    write_json,
    write_text,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate product value gate before PRD generation")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--project", required=True)
    parser.add_argument(
        "--mode",
        default="rule",
        choices=["rule", "llm", "auto"],
        help="V0 is rule-based. llm/auto are accepted for pipeline compatibility but do not fetch evidence.",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    paths = project_paths(base_dir, args.project)
    raw_text = read_text(paths["raw_input"])
    if not raw_text.strip():
        raise SystemExit(f"Missing raw input: {paths['raw_input']}")

    value_gate = build_value_gate(args.project, raw_text, seed=read_json(paths["value_gate_json"]))
    errors = validate_schema(base_dir / "shared" / "schemas" / "value_gate.schema.json", value_gate)
    if errors:
        raise SystemExit(f"Value gate validation failed: {errors}")

    write_json(paths["value_gate_json"], value_gate)
    write_text(paths["value_gate_md"], value_gate_markdown(value_gate))
    print(paths["value_gate_json"])
    print(paths["value_gate_md"])


if __name__ == "__main__":
    main()
