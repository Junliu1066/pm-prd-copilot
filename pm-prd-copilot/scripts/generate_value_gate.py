#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from pipeline_common import (
    build_value_gate,
    build_evidence_snapshot,
    default_value_gate_materials,
    project_paths,
    read_json,
    read_text,
    validate_schema,
    value_gate_owner_decision_markdown,
    value_gate_owner_summary_markdown,
    value_gate_markdown,
    build_prd_agent_input_package,
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
        help="V0 is rule-based. llm/auto are accepted for pipeline compatibility.",
    )
    parser.add_argument(
        "--fetch-evidence",
        action="store_true",
        help="Fetch public source URLs for evidence reachability and excerpts. Does not save raw snapshots.",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    paths = project_paths(base_dir, args.project)
    raw_text = read_text(paths["raw_input"])
    if not raw_text.strip():
        raise SystemExit(f"Missing raw input: {paths['raw_input']}")

    materials = read_json(paths["value_gate_materials_json"])
    if not materials:
        materials = default_value_gate_materials(args.project)
        write_json(paths["value_gate_materials_json"], materials)
    material_errors = validate_schema(base_dir / "shared" / "schemas" / "value_gate_materials.schema.json", materials)
    if material_errors:
        raise SystemExit(f"Value gate materials validation failed: {material_errors}")

    value_gate = build_value_gate(
        args.project,
        raw_text,
        seed=read_json(paths["value_gate_json"]),
        materials_payload=materials,
        fetch_external_evidence=args.fetch_evidence,
    )
    errors = validate_schema(base_dir / "shared" / "schemas" / "value_gate.schema.json", value_gate)
    if errors:
        raise SystemExit(f"Value gate validation failed: {errors}")

    write_json(paths["value_gate_json"], value_gate)
    write_text(paths["value_gate_md"], value_gate_markdown(value_gate))
    write_json(paths["value_gate_prd_input_json"], build_prd_agent_input_package(value_gate))
    write_text(paths["value_gate_owner_decision_md"], value_gate_owner_decision_markdown(value_gate))
    write_text(paths["value_gate_owner_summary_md"], value_gate_owner_summary_markdown(value_gate))
    write_json(paths["value_gate_evidence_snapshot_json"], build_evidence_snapshot(value_gate))
    print(paths["value_gate_json"])
    print(paths["value_gate_md"])
    print(paths["value_gate_materials_json"])
    print(paths["value_gate_prd_input_json"])
    print(paths["value_gate_owner_decision_md"])
    print(paths["value_gate_owner_summary_md"])
    print(paths["value_gate_evidence_snapshot_json"])


if __name__ == "__main__":
    main()
