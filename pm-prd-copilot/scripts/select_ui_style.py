#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STYLE_KEYWORDS = {
    "swiss_utility": ["后台", "管理", "审批", "crm", "dashboard", "finance", "财务", "合规", "运营", "工作台", "表格"],
    "refined_saas": ["saas", "协作", "平台", "工作流", "productivity", "analytics", "分析", "pm"],
    "concrete_editorial": ["水泥", "混凝土", "cement", "concrete", "industrial", "建筑", "硬件", "基础设施", "studio"],
    "brutalist_product": ["brutalist", "anti", "独立", "实验", "developer", "创意工具"],
    "glass_depth": ["glass", "玻璃", "沉浸", "media", "premium", "consumer"],
    "ai_lab_dark": ["ai", "agent", "模型", "prompt", "eval", "评测", "developer", "console"],
    "editorial_magazine": ["内容", "文章", "研究", "品牌故事", "portfolio", "publication"],
    "bauhaus_grid": ["教育", "workshop", "设计系统", "几何", "课程"],
    "minimal_luxury": ["奢侈", "精品", "高端", "venue", "gallery", "commerce"],
    "warm_humanist": ["教练", "学习", "健康", "社区", "家庭", "wellness"],
    "retro_terminal": ["cli", "terminal", "安全", "日志", "命令行"],
    "neo_clay": ["儿童", "游戏化", "habit", "轻量", "playful"],
    "data_newsroom": ["报告", "市场", "投资", "情报", "research", "source", "来源"],
}

OPERATIONAL_KEYWORDS = {"后台", "管理", "审批", "财务", "合规", "运营", "crm", "dashboard", "表格", "内部"}
EXPRESSIVE_STYLE_IDS = {"concrete_editorial", "brutalist_product", "glass_depth", "bauhaus_grid", "minimal_luxury", "neo_clay"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> Any:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def normalize(text: str) -> str:
    return text.lower()


def flatten_json(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten_json(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten_json(item) for item in value)
    return str(value)


def load_catalog(base_dir: Path) -> dict[str, Any]:
    path = base_dir / "pm-prd-copilot" / "ui-design" / "data" / "visual_style_catalog.json"
    catalog = read_json(path)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("styles"), list):
        raise SystemExit(f"Invalid style catalog: {path}")
    return catalog


def collect_project_text(base_dir: Path, project: str) -> str:
    project_dir = base_dir / "projects" / project
    if not project_dir.exists():
        raise SystemExit(f"Project not found: {project_dir}")
    parts = [
        flatten_json(read_json(project_dir / "01_requirement_brief.json")),
        flatten_json(read_json(project_dir / "02_prd.generated.json")),
        read_text(project_dir / "00_raw_input.md"),
        read_text(project_dir / "02_prd.final.md"),
        read_text(project_dir / "06_review_merge.md"),
    ]
    return normalize(" ".join(parts))


def style_by_id(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {style["id"]: style for style in catalog["styles"] if isinstance(style, dict) and "id" in style}


def find_explicit_style(catalog: dict[str, Any], requested_style: str) -> str:
    requested = normalize(requested_style)
    if not requested:
        return ""
    for style in catalog["styles"]:
        aliases = [style.get("id", ""), style.get("name", ""), *style.get("aliases", [])]
        if any(normalize(alias) == requested or requested in normalize(alias) for alias in aliases):
            return style["id"]
    raise SystemExit(f"Requested style not found in catalog: {requested_style}")


def score_styles(catalog: dict[str, Any], project_text: str) -> list[tuple[int, str]]:
    scores: list[tuple[int, str]] = []
    for style in catalog["styles"]:
        style_id = style["id"]
        keywords = STYLE_KEYWORDS.get(style_id, [])
        aliases = style.get("aliases", [])
        best_for = style.get("best_for", [])
        score = 0
        for keyword in [*keywords, *aliases, *best_for]:
            key = normalize(str(keyword))
            if key and key in project_text:
                score += 3 if key in {normalize(alias) for alias in aliases} else 1
        scores.append((score, style_id))
    return sorted(scores, key=lambda item: (-item[0], item[1]))


def choose_style(catalog: dict[str, Any], project_text: str, requested_style: str) -> tuple[str, list[str], list[str]]:
    explicit = find_explicit_style(catalog, requested_style)
    warnings: list[str] = []
    scores = score_styles(catalog, project_text)
    operational = any(keyword in project_text for keyword in OPERATIONAL_KEYWORDS)

    if explicit:
        if operational and explicit in EXPRESSIVE_STYLE_IDS:
            warnings.append(
                "Explicit expressive style selected for an operational product. Keep dense workflows in restrained utility surfaces."
            )
        backups = [style_id for _score, style_id in scores if style_id != explicit][:3]
        return explicit, backups, warnings

    if operational:
        backups = [style_id for _score, style_id in scores if style_id not in {"swiss_utility", "refined_saas"}][:3]
        return "swiss_utility", ["refined_saas", *backups[:2]], warnings

    top = scores[0][1] if scores and scores[0][0] > 0 else "refined_saas"
    backups = [style_id for _score, style_id in scores if style_id != top][:3]
    return top, backups, warnings


def build_payload(catalog: dict[str, Any], project: str, selected_id: str, backup_ids: list[str], warnings: list[str]) -> dict[str, Any]:
    styles = style_by_id(catalog)
    selected = styles[selected_id]
    backups = [styles[style_id] for style_id in backup_ids if style_id in styles]
    return {
        "schema_version": "ui_style_direction.v1",
        "project_id": project,
        "generated_at": utc_now(),
        "selected_style": selected,
        "backup_styles": [
            {
                "id": style["id"],
                "name": style["name"],
                "description": style["description"],
                "best_for": style.get("best_for", []),
                "avoid_for": style.get("avoid_for", [])
            }
            for style in backups
        ],
        "warnings": warnings,
        "human_approval_required": True,
        "next_steps": [
            "Review whether the selected style matches the product task and target users.",
            "Approve or override the style before generating high-fidelity UI.",
            "Use the selected tokens and quality gates during screenshot review."
        ]
    }


def build_markdown(payload: dict[str, Any]) -> str:
    style = payload["selected_style"]
    tokens = style["tokens"]
    lines = [
        f"# UI Style Direction - {payload['project_id']}",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        "- Status: draft for human review",
        f"- Selected style: `{style['id']}` / {style['name']}",
        f"- Category: {style['category']}",
        f"- Description: {style['description']}",
        "",
        "## Tokens",
        f"- Palette: {', '.join(tokens['palette'])}",
        f"- Typography: {tokens['typography']}",
        f"- Radius: {tokens['radius']}",
        f"- Density: {tokens['density']}",
        f"- Texture: {tokens['texture']}",
        f"- Layout: {tokens['layout']}",
        f"- Motion: {tokens['motion']}",
        "",
        "## Component Bias",
        *[f"- {item}" for item in style.get("component_bias", [])],
        "",
        "## Best For",
        *[f"- {item}" for item in style.get("best_for", [])],
        "",
        "## Avoid For",
        *[f"- {item}" for item in style.get("avoid_for", [])],
        "",
        "## Quality Gates",
        *[f"- [ ] {item}" for item in style.get("quality_gates", [])],
        "",
        "## Warnings",
    ]
    lines.extend(f"- {warning}" for warning in payload.get("warnings", [])) if payload.get("warnings") else lines.append("_None._")
    lines.extend(["", "## Backup Styles"])
    for backup in payload.get("backup_styles", []):
        lines.append(f"- `{backup['id']}` / {backup['name']}: {backup['description']}")
    lines.extend(
        [
            "",
            "## Approval",
            "- [ ] Approve this style direction.",
            "- [ ] Override style direction.",
            "- [ ] Request a more restrained variant.",
            "- [ ] Request a more expressive variant.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_style_direction(base_dir: Path, project: str, requested_style: str = "") -> dict[str, Path]:
    base_dir = base_dir.resolve()
    catalog = load_catalog(base_dir)
    project_text = collect_project_text(base_dir, project)
    selected_id, backup_ids, warnings = choose_style(catalog, project_text, requested_style)
    payload = build_payload(catalog, project, selected_id, backup_ids, warnings)
    output_dir = base_dir / "projects" / project / "prototype"
    outputs = {
        "json": output_dir / "ui_style_direction.json",
        "markdown": output_dir / "ui_style_direction.md"
    }
    write_json(outputs["json"], payload)
    write_text(outputs["markdown"], build_markdown(payload))
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Select a supervised UI style direction for a project prototype.")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--project", required=True)
    parser.add_argument("--style", default="", help="Optional explicit style alias, e.g. concrete, swiss, glass, 水泥风.")
    args = parser.parse_args()

    outputs = generate_style_direction(Path(args.base_dir), args.project, requested_style=args.style)
    print("UI style direction generated:")
    for label, path in outputs.items():
        print(f"- {label}: {path}")


if __name__ == "__main__":
    main()
