#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional local dependency
    yaml = None


PROTECTED_ROOTS = [
    ".github/",
    "ai-intel/",
    "docs/",
    "governance/",
    "harness/",
    "plugins/",
    "pm-prd-copilot/",
    "registry/",
    "shared/",
    "skills/",
    "stewards/",
    "teaching/",
    "workflow/",
]

TEMP_PARTS = {"cache", ".cache", "tmp", "temp"}
LEGACY_PRD_TERMS = {
    "centralized_visual_layer": "PRD 可视化层",
    "old_prototype_wireframe": "原型图 / 线框图",
    "ai_model_selection": "AI 模型选型",
    "export_domain_bleed": "导出",
    "excel_domain_bleed": "Excel",
    "async_export_bleed": "异步导出",
}
FINAL_PRD_REQUIRED_TERMS = {
    "page_specs": "页面说明",
    "page_flow": "页面跳转关系",
    "prototype_layer": "原型图层",
}
LEGACY_SIGNAL_LABELS = {
    "centralized_visual_layer": "旧集中式 PRD 可视化层",
    "old_prototype_wireframe": "旧原型图 / 线框图口径",
    "ai_model_selection": "非 AI 项目默认 AI 模型选型",
    "export_domain_bleed": "导出场景污染",
    "excel_domain_bleed": "Excel 场景污染",
    "async_export_bleed": "异步导出场景污染",
}
FINAL_REQUIRED_LABELS = {
    "page_specs": "页面说明",
    "page_flow": "页面跳转关系",
    "prototype_layer": "原型图层",
}
ACTION_LABELS = {
    "archive_sensitive_input": "敏感输入先归档，暂不删除",
    "archive_then_cleanup_after_distillation": "沉淀后归档，再考虑清理",
    "delete_after_approval": "归档和审批后可清理候选",
    "manual_review": "需要人工审核",
    "manual_review_project_memory": "项目偏好缓存需要人工审核",
    "retain_closeout_record": "保留收口审计记录",
    "retain_project_record": "保留项目状态记录",
    "retain_until_distilled": "保留到经验沉淀完成",
}
RUN_EVIDENCE_FILES = {
    "manifest.json",
    "trace.json",
    "harness_report.json",
    "random_audit_report.json",
    "efficiency_report.json",
    "eval_suite_report.json",
    "real_output_eval_status.json",
    "skill_generalization_audit.json",
}


@dataclass
class FileRecord:
    path: str
    root: str
    kind: str
    bytes: int
    modified_at: str
    registered_artifact: str | None
    cleanup_action: str
    rationale: str
    symlink: bool
    safe_to_delete_after_approval: bool


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def validate_project_id(project: str) -> None:
    if not project or project in {".", ".."}:
        raise SystemExit("Project id is required.")
    if "/" in project or "\\" in project:
        raise SystemExit("Project id must be a single directory name, not a path.")


def read_json(path: Path) -> Any:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def repo_relative(base_dir: Path, path: Path) -> str:
    return path.relative_to(base_dir).as_posix()


def detect_kind(path: Path, registered_kind: str | None) -> str:
    if registered_kind:
        return registered_kind
    suffixes = "".join(path.suffixes)
    if suffixes.endswith(".meta.json"):
        return "metadata"
    if path.suffix == ".json":
        return "json"
    if path.suffix == ".md":
        return "markdown"
    if path.suffix == ".html":
        return "html"
    if path.suffix in {".png", ".jpg", ".jpeg", ".svg"}:
        return "visual"
    return path.suffix.lstrip(".") or "file"


def load_registered_artifacts(base_dir: Path, project: str) -> dict[str, dict[str, str]]:
    registry_path = base_dir / "registry" / "artifacts.yaml"
    if not registry_path.exists():
        return {}
    raw_text = registry_path.read_text(encoding="utf-8")
    if yaml is None:
        return parse_registered_artifacts(raw_text, project)
    data = yaml.safe_load(raw_text) or {}
    artifacts = data.get("artifacts", {})
    if not isinstance(artifacts, dict):
        return {}

    registered: dict[str, dict[str, str]] = {}
    for artifact_key, spec in artifacts.items():
        if not isinstance(spec, dict):
            continue
        pattern = spec.get("path_pattern")
        if not isinstance(pattern, str) or "{date}" in pattern:
            continue
        rel_path = pattern.format(project=project)
        registered[rel_path] = {
            "artifact": str(artifact_key),
            "kind": str(spec.get("type", "")),
            "owner_stage": str(spec.get("owner_stage", "")),
        }
    return registered


def parse_registered_artifacts(raw_text: str, project: str) -> dict[str, dict[str, str]]:
    registered: dict[str, dict[str, str]] = {}
    current_key = ""
    current_spec: dict[str, str] = {}

    def flush() -> None:
        if not current_key:
            return
        pattern = current_spec.get("path_pattern", "")
        if not pattern or "{date}" in pattern:
            return
        registered[pattern.format(project=project)] = {
            "artifact": current_key,
            "kind": current_spec.get("type", ""),
            "owner_stage": current_spec.get("owner_stage", ""),
        }

    for line in raw_text.splitlines():
        if line.startswith("  ") and not line.startswith("    ") and line.strip().endswith(":"):
            flush()
            current_key = line.strip().rstrip(":")
            current_spec = {}
            continue
        if not current_key or not line.startswith("    "):
            continue
        stripped = line.strip()
        if ": " not in stripped:
            continue
        key, value = stripped.split(": ", 1)
        current_spec[key] = value.strip().strip('"').strip("'")
    flush()
    return registered


def classify_file(rel_path: str, root_label: str, symlink: bool, registered_artifact: str | None) -> tuple[str, str, bool]:
    path = Path(rel_path)
    name = path.name
    parts = set(path.parts)

    if symlink:
        return (
            "manual_review",
            "检测到符号链接，清理工具不能自动跟随或删除链接目标。",
            False,
        )
    if "/closeout/" in rel_path:
        return ("retain_closeout_record", "收口产物是本轮审计记录，必须保留。", False)
    if name == "project_state.json":
        return ("retain_project_record", "项目状态文件是本地生命周期指针，必须保留。", False)
    if root_label == "memory_cache":
        return (
            "manual_review_project_memory",
            "项目偏好缓存会影响后续工作，清除前必须人工审核。",
            False,
        )
    if parts & TEMP_PARTS or name.endswith((".tmp", ".temp", ".bak")):
        return ("delete_after_approval", "临时或缓存类文件，删除仍需明确审批。", True)
    if name.endswith(".meta.json"):
        return ("delete_after_approval", "生成元数据通常可复现，核心产物归档后可列为清理候选。", True)
    if "runs" in parts:
        if name in RUN_EVIDENCE_FILES:
            return (
                "archive_then_cleanup_after_distillation",
                "治理运行证据应保留到学习沉淀和审计复核完成。",
                True,
            )
        return ("delete_after_approval", "运行过程产物，删除前需要复核。", True)
    if name in {"00_raw_input.md"}:
        return (
            "archive_sensitive_input",
            "原始输入可能包含项目特定或敏感上下文，只能在监督下归档。",
            False,
        )
    if name.endswith("_review_notes.md") or name.startswith("00_test_review_notes"):
        return (
            "retain_until_distilled",
            "项目评审笔记包含高价值纠错证据，应保留到架构沉淀完成。",
            False,
        )
    if name.endswith(".final.md"):
        return (
            "retain_until_distilled",
            "人工修订后的 final 产物是高价值学习证据，应保留到沉淀完成。",
            False,
        )
    if name.endswith((".generated.md", ".generated.json")):
        return (
            "archive_then_cleanup_after_distillation",
            "生成产物应保留到有用经验提取完成后再考虑归档清理。",
            True,
        )
    if registered_artifact:
        return (
            "archive_then_cleanup_after_distillation",
            "已注册工作流产物，任何清理前都必须先归档。",
            True,
        )
    if parts & {"analysis", "prototype", "delivery", "ai", "review"}:
        return (
            "archive_then_cleanup_after_distillation",
            "项目过程产物应先审核归档，再考虑清理。",
            True,
        )
    return ("manual_review", "未注册文件，任何清理决定前都需要人工审核。", False)


def iter_project_files(base_dir: Path, project: str) -> list[FileRecord]:
    registered = load_registered_artifacts(base_dir, project)
    roots = [
        ("project", base_dir / "projects" / project),
        ("memory_cache", base_dir / "memory-cache" / "projects" / project),
    ]
    records: list[FileRecord] = []

    for root_label, root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() and not path.is_symlink():
                continue
            if "closeout" in path.parts:
                continue
            rel_path = repo_relative(base_dir, path)
            reg = registered.get(rel_path)
            artifact_key = reg["artifact"] if reg else None
            registered_kind = reg["kind"] if reg else None
            stat = path.lstat()
            action, rationale, safe_to_delete = classify_file(rel_path, root_label, path.is_symlink(), artifact_key)
            records.append(
                FileRecord(
                    path=rel_path,
                    root=root_label,
                    kind=detect_kind(path, registered_kind),
                    bytes=stat.st_size,
                    modified_at=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(timespec="seconds"),
                    registered_artifact=artifact_key,
                    cleanup_action=action,
                    rationale=rationale,
                    symlink=path.is_symlink(),
                    safe_to_delete_after_approval=safe_to_delete,
                )
            )
    return records


def summarize_records(records: list[FileRecord]) -> dict[str, Any]:
    by_action: dict[str, int] = {}
    by_root: dict[str, int] = {}
    total_bytes = 0
    for record in records:
        by_action[record.cleanup_action] = by_action.get(record.cleanup_action, 0) + 1
        by_root[record.root] = by_root.get(record.root, 0) + 1
        total_bytes += record.bytes
    return {
        "file_count": len(records),
        "total_bytes": total_bytes,
        "by_action": dict(sorted(by_action.items())),
        "by_root": dict(sorted(by_root.items())),
    }


def first_heading(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def project_title(project_dir: Path, project: str) -> str:
    brief = read_json(project_dir / "01_requirement_brief.json")
    if isinstance(brief, dict) and brief.get("title"):
        return str(brief["title"])
    for candidate in ["02_prd.final.md", "02_prd.generated.md", "01_requirement_brief.md", "00_raw_input.md"]:
        heading = first_heading(project_dir / candidate)
        if heading:
            return heading
    return project


def diff_signal(generated_path: Path, final_path: Path) -> dict[str, Any] | None:
    if not generated_path.exists() or not final_path.exists():
        return None
    generated = generated_path.read_text(encoding="utf-8").splitlines()
    final = final_path.read_text(encoding="utf-8").splitlines()
    diff = list(
        difflib.unified_diff(
            generated,
            final,
            fromfile=generated_path.name,
            tofile=final_path.name,
            lineterm="",
        )
    )
    additions = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    return {
        "generated_path": generated_path.name,
        "final_path": final_path.name,
        "generated_lines": len(generated),
        "final_lines": len(final),
        "additions": additions,
        "deletions": deletions,
        "diff_excerpt": diff[:40],
    }


def latest_run_id(project_dir: Path) -> str:
    state = read_json(project_dir / "project_state.json")
    if isinstance(state, dict) and state.get("last_run_id"):
        return str(state["last_run_id"])
    run_root = project_dir / "runs"
    if not run_root.exists():
        return ""
    runs = sorted([path.name for path in run_root.iterdir() if path.is_dir()])
    return runs[-1] if runs else ""


def collect_review_notes(project_dir: Path) -> tuple[list[str], list[str]]:
    candidates = sorted(
        path
        for path in project_dir.glob("*.md")
        if "review" in path.name.lower() or "notes" in path.name.lower() or "评审" in path.name
    )
    review_lines: list[str] = []
    review_files: list[str] = []
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        extracted = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped.startswith(("- ", "|")):
                continue
            if "---" in stripped or "问题 |" in stripped or "检查项 |" in stripped:
                continue
            if stripped.startswith("- "):
                stripped = stripped[2:].strip()
            extracted.append(stripped)
        if extracted:
            review_files.append(path.name)
            review_lines.extend(extracted)
    return review_lines, review_files


def scan_text_terms(path: Path, terms: dict[str, str]) -> dict[str, bool]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    return {key: value in text for key, value in terms.items()}


def collect_prd_quality_signals(project_dir: Path) -> dict[str, Any]:
    generated_md = project_dir / "02_prd.generated.md"
    generated_json = project_dir / "02_prd.generated.json"
    final_md = project_dir / "02_prd.final.md"
    generated_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [generated_md, generated_json]
        if path.exists()
    )
    final_text = final_md.read_text(encoding="utf-8") if final_md.exists() else ""
    legacy_generated = {
        key: term in generated_text
        for key, term in LEGACY_PRD_TERMS.items()
    }
    legacy_final = {
        key: term in final_text
        for key, term in LEGACY_PRD_TERMS.items()
    }
    final_required = {
        key: term in final_text
        for key, term in FINAL_PRD_REQUIRED_TERMS.items()
    }
    final_removed_old_visual_layer = bool(final_text) and "PRD 可视化层" not in final_text
    final_removed_old_prototype = bool(final_text) and "原型图 / 线框图" not in final_text
    final_omits_non_ai_model_selection = bool(final_text) and "AI 模型选型" not in final_text
    return {
        "generated_legacy_terms": legacy_generated,
        "final_legacy_terms": legacy_final,
        "final_required_terms": final_required,
        "final_removed_old_visual_layer": final_removed_old_visual_layer,
        "final_removed_old_prototype": final_removed_old_prototype,
        "final_omits_non_ai_model_selection": final_omits_non_ai_model_selection,
        "final_is_prd_structure_golden_candidate": all(final_required.values())
        and final_removed_old_visual_layer
        and final_removed_old_prototype
        and final_omits_non_ai_model_selection,
    }


def collect_project_context(base_dir: Path, project: str, run_id: str = "") -> dict[str, Any]:
    project_dir = base_dir / "projects" / project
    selected_run_id = run_id or latest_run_id(project_dir)
    run_dir = project_dir / "runs" / selected_run_id if selected_run_id else project_dir / "runs"
    brief = read_json(project_dir / "01_requirement_brief.json")
    prd = read_json(project_dir / "02_prd.generated.json")
    stories = read_json(project_dir / "03_user_stories.generated.json")
    harness = read_json(run_dir / "harness_report.json")
    efficiency = read_json(run_dir / "efficiency_report.json")
    manifest = read_json(run_dir / "manifest.json")

    review_lines, review_files = collect_review_notes(project_dir)
    raw_input_text = (project_dir / "00_raw_input.md").read_text(encoding="utf-8") if (project_dir / "00_raw_input.md").exists() else ""
    is_test_project = any(token in raw_input_text for token in ["测试目的", "测试样例", "测试输入"])

    return {
        "project_id": project,
        "title": project_title(project_dir, project),
        "run_id": selected_run_id,
        "brief": brief if isinstance(brief, dict) else {},
        "prd": prd if isinstance(prd, dict) else {},
        "story_count": len(stories) if isinstance(stories, list) else 0,
        "harness": harness if isinstance(harness, dict) else {},
        "efficiency": efficiency if isinstance(efficiency, dict) else {},
        "manifest": manifest if isinstance(manifest, dict) else {},
        "review_lines": review_lines,
        "review_files": review_files,
        "is_test_project": is_test_project,
        "prd_quality_signals": collect_prd_quality_signals(project_dir),
        "diff_signals": [
            signal
            for signal in [
                diff_signal(project_dir / "02_prd.generated.md", project_dir / "02_prd.final.md"),
                diff_signal(project_dir / "03_user_stories.generated.md", project_dir / "03_user_stories.final.md"),
            ]
            if signal
        ],
    }


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    if not rows:
        return "_暂无_"
    header = "| " + " | ".join(headers) + " |"
    divider = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def truncate(value: str, limit: int = 120) -> str:
    text = " ".join(value.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def action_label(action: str) -> str:
    label = ACTION_LABELS.get(action, action)
    return f"{label} (`{action}`)"


def yes_no(value: bool) -> str:
    return "是" if value else "否"


def kind_label(kind: str) -> str:
    labels = {
        "markdown": "Markdown 文档",
        "json": "JSON 数据",
        "metadata": "生成元数据",
        "html": "HTML 文件",
        "visual": "视觉文件",
    }
    return labels.get(kind, kind)


def format_signal_labels(keys: list[str], labels: dict[str, str]) -> str:
    if not keys:
        return "_无_"
    return "、".join(f"`{labels.get(key, key)}`" for key in keys)


def build_closeout_report(context: dict[str, Any], records: list[FileRecord], generated_at: str) -> str:
    summary = summarize_records(records)
    brief = context["brief"]
    manifest = context["manifest"]
    harness = context["harness"]
    efficiency = context["efficiency"]

    run_status = manifest.get("status", "unknown") if isinstance(manifest, dict) else "unknown"
    harness_status = harness.get("status", "not_run") if isinstance(harness, dict) else "not_run"
    efficiency_status = efficiency.get("status", "not_run") if isinstance(efficiency, dict) else "not_run"
    required_outputs = manifest.get("required_outputs", []) if isinstance(manifest, dict) else []
    prd_signals = context.get("prd_quality_signals", {})
    generated_legacy = [
        key
        for key, found in prd_signals.get("generated_legacy_terms", {}).items()
        if found
    ]
    final_required = [
        key
        for key, found in prd_signals.get("final_required_terms", {}).items()
        if found
    ]

    action_rows = [[action_label(action), count] for action, count in summary["by_action"].items()]
    diff_rows = [
        [
            signal["generated_path"],
            signal["final_path"],
            signal["additions"],
            signal["deletions"],
        ]
        for signal in context["diff_signals"]
    ]

    return "\n".join(
        [
            f"# 项目收口报告 - {context['project_id']}",
            "",
            f"- 生成时间：`{generated_at}`",
            "- 模式：只生成报告，不执行清理",
            "- 破坏性动作：已禁用",
            "- 归档、删除、提交、PR、prompt、模板或框架变更都需要你审批。",
            "",
            "## 项目概况",
            f"- 标题：{context['title']}",
            f"- 需求类型：{brief.get('request_type', 'unknown')}",
            f"- 紧急度：{brief.get('urgency', 'unknown')}",
            f"- 业务目标：{brief.get('business_goal', 'unknown')}",
            f"- 收口解读：{'这是 PRD 生成链路测试项目，业务目标里可能混入测试目的。' if context.get('is_test_project') else '这是正常项目收口。'}",
            f"- 最近运行 ID：`{context['run_id'] or '无'}`",
            f"- Pipeline 状态：`{run_status}`",
            f"- Harness 状态：`{harness_status}`",
            f"- 效率检查状态：`{efficiency_status}`",
            f"- 用户故事数量：`{context['story_count']}`",
            "",
            "## 运行要求产物",
            ", ".join(f"`{item}`" for item in required_outputs) if required_outputs else "_没有找到运行 manifest 里的产物清单。_",
            "",
            "## 文件盘点摘要",
            f"- 扫描文件数：`{summary['file_count']}`",
            f"- 文件总大小：`{summary['total_bytes']}` bytes",
            "",
            markdown_table(["处理建议", "文件数"], action_rows),
            "",
            "## 人工修订信号",
            markdown_table(["生成稿", "最终稿", "新增行", "删除行"], diff_rows),
            "",
            "## 项目评审笔记",
            f"- 评审文件：{', '.join(f'`{item}`' for item in context.get('review_files', []))}"
            if context.get("review_files")
            else "_没有找到项目评审笔记。_",
            "\n".join(f"- {line}" for line in context["review_lines"]) if context["review_lines"] else "",
            "",
            "## PRD 质量信号",
            f"- 生成稿旧问题：{format_signal_labels(generated_legacy, LEGACY_SIGNAL_LABELS)}",
            f"- 最终稿已具备的关键结构：{format_signal_labels(final_required, FINAL_REQUIRED_LABELS)}",
            f"- 最终稿是否可作为结构黄金样例候选：`{yes_no(bool(prd_signals.get('final_is_prd_structure_golden_candidate')))}`",
            "",
            "## 收口审批清单",
            "- [ ] 确认项目可以进入收口。",
            "- [ ] 审核 final PRD、用户故事、风险检查、埋点计划里是否有可沉淀经验。",
            "- [ ] 决定哪些信号可以进入 GitHub 知识库或优化 backlog。",
            "- [ ] 确认原始输入如何归档、隐藏敏感信息或保留。",
            "- [ ] 审核 `cleanup-plan.md` 后再做任何归档或删除。",
            "- [ ] 对认可的架构反馈，后续再走受监督分支或 PR。",
            "",
            "## 需要人工审核的文件",
            markdown_table(
                ["路径", "处理建议", "原因"],
                [
                    [record.path, action_label(record.cleanup_action), truncate(record.rationale)]
                    for record in records
                    if not record.safe_to_delete_after_approval
                ],
            ),
            "",
        ]
    )


def build_architecture_feedback(context: dict[str, Any], records: list[FileRecord], generated_at: str) -> str:
    brief = context["brief"]
    harness = context["harness"]
    open_questions = brief.get("open_questions", []) if isinstance(brief, dict) else []
    prd_signals = context.get("prd_quality_signals", {})

    template_candidates: list[str] = []
    prompt_candidates: list[str] = []
    workflow_candidates: list[str] = []
    data_model_candidates: list[str] = []
    eval_candidates: list[str] = []
    adr_candidates: list[str] = []

    if len(open_questions) >= 8:
        template_candidates.append(
            "intake 和 PRD 模板需要持续把字段、权限、范围、指标、上线风险等未决问题压到显式评审区。"
        )
        prompt_candidates.append(
            "PRD 写作链路遇到大量开放问题时，应标记为上线准备风险，不能把不确定性写成确定结论。"
        )

    for line in context["review_lines"]:
        if any(token in line for token in ["权限", "permission", "越权"]):
            template_candidates.append("PRD 和用户故事模板需要加强权限边界、角色范围和越权风险描述。")
            eval_candidates.append("增加或保留权限边界回归样例，确保评审能发现权限描述不清的问题。")
        if any(token in line for token in ["审计", "audit", "日志"]):
            template_candidates.append("涉及敏感数据或关键操作时，审计日志和可追溯性应成为风险清单固定项。")
            eval_candidates.append("增加敏感操作回归样例，检查是否包含审计日志和追踪要求。")
        if "测试目的被混入产品问题" in line or "测试目的" in line:
            prompt_candidates.append(
                "需求解析器必须先区分“测试/文档目的”和“产品业务目标”，再进入 PRD 草稿。"
            )
            eval_candidates.append("保留测试目的误入产品问题的回归样例，防止测试说明再次被写成业务问题。")
        if "打车业务场景识别很弱" in line or "业务场景识别" in line:
            prompt_candidates.append(
                "rule mode 需要对常见 0-1 产品做领域化场景抽取，不能只输出泛化 fallback 场景。"
            )
        if "范围定义过泛" in line or "可视化图泛化严重" in line:
            template_candidates.append(
                "PRD 辅助图表必须使用项目自己的用户、范围、状态和页面模块，不能停留在通用占位。"
            )
        if "导出" in line or "Excel" in line or "异步导出" in line:
            prompt_candidates.append(
                "通用 fallback 内容不能把导出、Excel、异步导出等历史场景带入无关项目。"
            )
            eval_candidates.append("保留非导出类项目回归样例，检查是否出现导出领域污染。")
        if "AI 模型选型默认出现" in line or "AI 模型选型需要按项目" in line:
            eval_candidates.append("保留非 AI 项目回归样例，禁止默认生成 AI 模型选型。")
        if "原型章节仍是旧机制" in line or "页面说明和跳转关系" in line:
            eval_candidates.append("保留 PRD 原型图层回归样例，要求页面说明、页面跳转关系和原型图层齐全。")

    for signal in context["diff_signals"]:
        if signal["additions"] or signal["deletions"]:
            prompt_candidates.append(
                f"在把写作偏好提升为长期规则前，必须复查 `{signal['generated_path']}` 到 `{signal['final_path']}` 的人工修改。"
            )
            eval_candidates.append(
                f"经你批准并处理敏感信息后，可考虑把 `{signal['final_path']}` 作为黄金样例。"
            )

    generated_legacy = prd_signals.get("generated_legacy_terms", {})
    if generated_legacy.get("centralized_visual_layer"):
        eval_candidates.append("持续检查 PRD 不得重新引入集中式 `PRD 可视化层`。")
    if generated_legacy.get("old_prototype_wireframe"):
        eval_candidates.append("持续检查 PRD 不得使用旧的 `原型图 / 线框图` 默认章节。")
    if generated_legacy.get("ai_model_selection"):
        eval_candidates.append("持续检查非 AI 项目不得默认输出 AI 模型选型。")
    if prd_signals.get("final_is_prd_structure_golden_candidate"):
        template_candidates.append(
            "`02_prd.final.md` 是高价值 PRD 结构黄金样例候选，需经你批准并处理敏感信息后再沉淀。"
        )
        eval_candidates.append(
            "可用 taxi final PRD 的结构作为回归参考，覆盖图表分章节、页面说明、页面跳转、原型图层和非 AI 不输出模型选型。"
        )

    checks = harness.get("checks", []) if isinstance(harness, dict) else []
    for check in checks:
        if not isinstance(check, dict) or check.get("status") == "pass":
            continue
        details = check.get("details") or []
        workflow_candidates.append(
            f"Harness `{check.get('check', 'unknown')}` 报告 `{check.get('status')}`：{check.get('message', '')}"
        )
        for detail in details:
            if "steward" in str(detail).lower():
                adr_candidates.append("需要复核 steward 责任边界，并决定是否为 closeout 增加 steward 扩容 ADR。")

    if any(record.root == "memory_cache" for record in records):
        data_model_candidates.append(
            "项目收口需要明确项目偏好缓存处理结果：保留、隐藏敏感信息、归档、清除或拒绝沉淀。"
        )
    if any(record.cleanup_action == "retain_closeout_record" for record in records):
        data_model_candidates.append("closeout 记录默认不应进入清理预览。")
    data_model_candidates.append("closeout 状态应和生成产物分开保存，确保清理审批可审计。")
    workflow_candidates.append("closeout 应保持受监督流程：报告、沉淀、PR 草案、清理预览、明确审批。")
    adr_candidates.append("在启用清理执行能力前，应把经你批准的项目收口生命周期记录为架构决策。")

    def unique(items: list[str]) -> list[str]:
        seen = set()
        ordered = []
        for item in items:
            if item not in seen:
                ordered.append(item)
                seen.add(item)
        return ordered

    sections = [
        ("模板优化候选", unique(template_candidates)),
        ("Prompt / 生成链路优化候选", unique(prompt_candidates)),
        ("工作流优化候选", unique(workflow_candidates)),
        ("数据模型候选", unique(data_model_candidates)),
        ("回归测试候选", unique(eval_candidates)),
        ("架构决策候选", unique(adr_candidates)),
    ]

    lines = [
        f"# 架构反哺草案 - {context['project_id']}",
        "",
        f"- 生成时间：`{generated_at}`",
        "- 状态：待你审核的草案",
        "- 规则：项目证据不能直接修改稳定 prompt、模板、skill 或框架代码，必须先经你审核。",
        "",
        "## 证据来源",
        f"- 项目：`{context['project_id']}`",
        f"- 标题：{context['title']}",
        f"- 运行 ID：`{context['run_id'] or '无'}`",
        f"- 评审笔记条数：`{len(context['review_lines'])}`",
        f"- 评审文件：{', '.join(f'`{item}`' for item in context.get('review_files', [])) if context.get('review_files') else '`无`'}",
        f"- 人工修订对比：`{len(context['diff_signals'])}`",
        f"- 扫描文件数：`{len(records)}`",
        "",
    ]
    for title, items in sections:
        lines.extend([f"## {title}"])
        if items:
            lines.extend(f"- [ ] {item}" for item in items)
        else:
            lines.append("_暂无候选_")
        lines.append("")

    lines.extend(
        [
            "## 建议的 GitHub 沉淀路径",
            "- 只把你接受的条目转成 `docs/architecture-inbox/<project>-feedback.md`。",
            "- 只针对已审核知识创建分支和 PR。",
            "- 未经你明确批准，不把项目名称、客户细节、原始输入写进稳定文档。",
            "- 合并 prompt、模板或 workflow 变更前必须跑 regression 和 harness。",
            "",
            "## 需要你拍板",
            "- [ ] 接受部分条目进入 GitHub 知识文档。",
            "- [ ] 把部分条目转成后续 backlog。",
            "- [ ] 拒绝项目特定或置信度不足的条目。",
            "- [ ] 要求重新生成一版收口报告。",
            "",
        ]
    )
    return "\n".join(lines)


def build_cleanup_plan(context: dict[str, Any], records: list[FileRecord], generated_at: str, max_files: int) -> str:
    groups: dict[str, list[FileRecord]] = {}
    for record in records:
        groups.setdefault(record.cleanup_action, []).append(record)

    lines = [
        f"# 清理计划 - {context['project_id']}",
        "",
        f"- 生成时间：`{generated_at}`",
        "- 模式：只生成预览，不执行清理",
        "- 本次没有删除、移动、归档、覆盖、提交或推送任何文件。",
        "- 真正执行清理必须经过你明确批准，并且应该作为单独命令执行。",
        "- 保留规则：先归档，硬删除至少等归档后 30 天，并且仍需你二次确认精确清单。",
        "",
        "## 允许讨论清理的范围",
        f"- `projects/{context['project_id']}/`",
        f"- `memory-cache/projects/{context['project_id']}/`，仅在项目偏好缓存审核后处理",
        "",
        "## 受保护目录",
        *[f"- `{root}`" for root in PROTECTED_ROOTS],
        "",
        "## 文件处理分组",
    ]

    for action in sorted(groups):
        files = groups[action]
        lines.extend(
            [
                f"### {action_label(action)}",
                f"- 文件数：`{len(files)}`",
                markdown_table(
                    ["路径", "类型", "大小", "审批后是否可清理", "原因"],
                    [
                        [
                            record.path,
                            kind_label(record.kind),
                            record.bytes,
                            yes_no(record.safe_to_delete_after_approval),
                            truncate(record.rationale, 90),
                        ]
                        for record in files[:max_files]
                    ],
                ),
            ]
        )
        if len(files) > max_files:
            lines.append(f"_只展示前 {max_files} 个文件，完整清单见 `manifest.json`。_")
        lines.append("")

    lines.extend(
        [
            "## 清理前必须审批",
            "- [ ] 你确认项目已经可以收口。",
            "- [ ] 你已审核 `closeout-report.md`。",
            "- [ ] `architecture-feedback.md` 里的建议已被接受、拒绝或转成受监督 GitHub 变更。",
            "- [ ] 原始输入的归档 / 隐藏敏感信息 / 保留策略已确认。",
            "- [ ] 项目偏好缓存处理方式已确认。",
            "- [ ] 归档目标已确认。",
            "- [ ] 所有硬删除候选已经满足归档后 30 天。",
            "- [ ] 硬删除前已完成第二次精确清单审批。",
            "",
        ]
    )
    return "\n".join(lines)


def build_preference_memory_disposition(context: dict[str, Any], records: list[FileRecord], generated_at: str) -> str:
    memory_records = [record for record in records if record.root == "memory_cache"]
    lines = [
        f"# 项目偏好缓存处理 - {context['project_id']}",
        "",
        f"- 生成时间：`{generated_at}`",
        "- 状态：待你审核的草案",
        "- 规则：项目偏好缓存只能在本项目内使用，默认不能跨项目复用。",
        "- 长期记忆：禁用自动写入，必须等你明确批准某一条沉淀内容。",
        "",
        "## 当前缓存证据",
    ]
    if memory_records:
        lines.extend(f"- `{record.path}`" for record in memory_records)
        lines.extend(
            [
                "",
                "## 归档前必须对齐",
                "- [ ] 审核已批准的项目偏好。",
                "- [ ] 审核候选项目偏好。",
                "- [ ] 决定哪些只保留为项目档案证据。",
                "- [ ] 决定哪些在归档对齐后清除。",
                "- [ ] 决定是否有单条内容需要提议进入长期记忆。",
                "- [ ] 确认未经你批准不跨项目复用。",
                "",
                "## 默认建议",
                "- 偏好证据只保留在项目收口包里。",
                "- 归档对齐后清除 active cache 指针。",
                "- 不自动写入长期记忆。",
                "",
            ]
        )
    else:
        lines.append("_没有找到项目偏好缓存文件。_")
        lines.extend(
            [
                "",
                "## 归档前对齐",
                "- [x] 没有发现 active 项目偏好缓存。",
                "- [x] 本项目不需要清除 active cache 指针。",
                "- [ ] 如果后续发现散落的偏好笔记，必须经你审核后才能作为项目档案证据。",
                "",
                "## 默认建议",
                "- 本轮收口不需要处理项目偏好缓存。",
                "- 不自动写入长期记忆。",
                "",
            ]
        )
    return "\n".join(lines)


def build_manifest(project: str, generated_at: str, records: list[FileRecord]) -> dict[str, Any]:
    return {
        "schema_version": "closeout.v1",
        "project_id": project,
        "generated_at": generated_at,
        "mode": "dry_run_report_only",
        "destructive_actions_enabled": False,
        "approval_required": True,
        "archive_before_delete": True,
        "hard_delete_eligible_after_days": 30,
        "protected_roots": PROTECTED_ROOTS,
        "allowed_roots": [
            f"projects/{project}/",
            f"memory-cache/projects/{project}/",
        ],
        "summary": summarize_records(records),
        "files": [asdict(record) for record in records],
    }


def generate_closeout_package(base_dir: Path, project: str, run_id: str = "", output_dir: Path | None = None) -> dict[str, Path]:
    validate_project_id(project)
    base_dir = base_dir.resolve()
    project_dir = base_dir / "projects" / project
    if not project_dir.exists():
        raise SystemExit(f"Project not found: {project_dir}")

    generated_at = utc_now()
    records = iter_project_files(base_dir, project)
    context = collect_project_context(base_dir, project, run_id=run_id)
    closeout_dir = output_dir or project_dir / "closeout"

    outputs = {
        "manifest": closeout_dir / "manifest.json",
        "closeout_report": closeout_dir / "closeout-report.md",
        "architecture_feedback": closeout_dir / "architecture-feedback.md",
        "cleanup_plan": closeout_dir / "cleanup-plan.md",
        "preference_memory_disposition": closeout_dir / "preference-memory-disposition.md",
    }

    write_json(outputs["manifest"], build_manifest(project, generated_at, records))
    write_text(outputs["closeout_report"], build_closeout_report(context, records, generated_at))
    write_text(outputs["architecture_feedback"], build_architecture_feedback(context, records, generated_at))
    write_text(outputs["cleanup_plan"], build_cleanup_plan(context, records, generated_at, max_files=80))
    write_text(
        outputs["preference_memory_disposition"],
        build_preference_memory_disposition(context, records, generated_at),
    )
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate supervised project closeout reports without deleting files.")
    parser.add_argument("--base-dir", default=".", help="Repository root")
    parser.add_argument("--project", required=True, help="Single project directory name under projects/")
    parser.add_argument("--run-id", default="", help="Optional governance run id to summarize")
    parser.add_argument("--output-dir", default="", help="Optional output directory; defaults to projects/<project>/closeout")
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    outputs = generate_closeout_package(base_dir, args.project, run_id=args.run_id, output_dir=output_dir)
    print("项目收口预览包已生成：")
    for label, path in outputs.items():
        print(f"- {label}: {path}")


if __name__ == "__main__":
    main()
