#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError:  # pragma: no cover - optional local dependency
    Draft202012Validator = None


def validate_json(schema_path: Path, candidate_path: Path) -> list[str]:
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    if Draft202012Validator is None:
        return []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(candidate), key=lambda err: list(err.path))
    return [f"{candidate_path}: {error.message}" for error in errors]


def validate_governed_pipeline_gate(base_dir: Path) -> list[str]:
    return _validate_pipeline_gate_blocks(base_dir, extra_args=["--governed"], label="Governed")


def validate_default_pipeline_gate(base_dir: Path) -> list[str]:
    return _validate_pipeline_gate_blocks(base_dir, extra_args=[], label="Default governed")


def _validate_pipeline_gate_blocks(base_dir: Path, *, extra_args: list[str], label: str) -> list[str]:
    command = [
        sys.executable,
        str(base_dir / "pm-prd-copilot" / "scripts" / "run_pipeline.py"),
        "--base-dir",
        str(base_dir),
        "--project",
        "__regression_missing_approvals__",
        "--stage",
        "prd",
        "--mode",
        "rule",
        "--no-trace",
    ] + extra_args
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    combined_output = f"{result.stdout}\n{result.stderr}"
    if result.returncode == 0:
        return [f"{label} pipeline did not block a PRD run with missing approvals."]
    if "missing approval, assumption override, or pipeline assumption override" not in combined_output:
        return [f"{label} pipeline failed without the expected missing-approval message."]
    return []


def _link_or_copy(src: Path, dst: Path) -> None:
    try:
        dst.symlink_to(src, target_is_directory=src.is_dir())
    except OSError:
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def validate_fast_draft_pipeline_path(base_dir: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="pm-pipeline-regression-") as tmp:
        fixture_dir = Path(tmp)
        for name in ["pm-prd-copilot", "shared", "workflow", "registry"]:
            _link_or_copy(base_dir / name, fixture_dir / name)
        project = "__regression_fast_draft__"
        raw_input = fixture_dir / "projects" / project / "00_raw_input.md"
        raw_input.parent.mkdir(parents=True, exist_ok=True)
        raw_input.write_text(
            "# 回归测试项目\n\n- 需要生成一个普通非 AI 功能的 PRD 草稿。\n- 当前没有任何审批或 assumption override。\n",
            encoding="utf-8",
        )
        command = [
            sys.executable,
            str(fixture_dir / "pm-prd-copilot" / "scripts" / "run_pipeline.py"),
            "--base-dir",
            str(fixture_dir),
            "--project",
            project,
            "--stage",
            "prd",
            "--mode",
            "rule",
            "--fast-draft",
            "--no-trace",
        ]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            combined_output = f"{result.stdout}\n{result.stderr}".strip()
            return [f"Fast draft pipeline should allow a draft run without approvals. Output: {combined_output}"]
        if not (fixture_dir / "projects" / project / "02_prd.generated.md").exists():
            return ["Fast draft pipeline completed without producing the expected PRD markdown."]
    return []


def validate_pipeline_manifest_stage_actions(base_dir: Path) -> list[str]:
    manifest_path = base_dir / "projects" / "demo-project" / "runs" / "pipeline-latest" / "manifest.json"
    if not manifest_path.exists():
        return []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("goal") != "production_pipeline":
        return []
    ordered_stages = manifest.get("ordered_stages", [])
    stage_actions = manifest.get("stage_actions", {})
    if not isinstance(ordered_stages, list) or not isinstance(stage_actions, dict):
        return [f"{manifest_path}: production pipeline manifest must declare ordered_stages and stage_actions."]
    missing = [stage for stage in ordered_stages if stage not in stage_actions]
    if missing:
        return [f"{manifest_path}: missing stage_actions for {', '.join(missing)}"]
    if manifest.get("governance_mode") != "governed":
        return [f"{manifest_path}: demo pipeline-latest must be governed, got {manifest.get('governance_mode')!r}."]
    if manifest.get("approval_gate_enforced") is not True:
        return [f"{manifest_path}: demo pipeline-latest must enforce approval gates."]
    return []


def validate_candidate_plugin_visibility(base_dir: Path) -> list[str]:
    errors: list[str] = []
    marketplace_path = base_dir / ".agents" / "plugins" / "marketplace.json"
    registry_path = base_dir / "registry" / "plugins.yaml"
    if not marketplace_path.exists():
        return [f"Missing marketplace file: {marketplace_path}"]
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    plugins = marketplace.get("plugins", [])
    if not plugins:
        return [f"{marketplace_path}: must list candidate plugins."]
    for item in plugins:
        name = item.get("name", "unknown")
        governance = item.get("governance", {})
        if governance.get("status") != "candidate":
            errors.append(f"{marketplace_path}: {name} must be marked candidate.")
        if governance.get("stable") is not False:
            errors.append(f"{marketplace_path}: {name} must not be marked stable.")
        if governance.get("requiresUserReviewBeforeStableUse") is not True:
            errors.append(f"{marketplace_path}: {name} must require user review before stable use.")
        if "candidate" not in str(governance.get("reviewLabel", "")):
            errors.append(f"{marketplace_path}: {name} must show a candidate review label.")
    registry_text = _read_if_exists(registry_path)
    if registry_text:
        if registry_text.count("marketplace_visibility: candidate_visible") < len(plugins):
            errors.append(f"{registry_path}: every marketplace-visible plugin must keep candidate visibility metadata.")
        if registry_text.count("stable_use_allowed: false") < len(plugins):
            errors.append(f"{registry_path}: every candidate plugin must declare stable_use_allowed: false.")
    return errors


def validate_b_package_packager(base_dir: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="pm-b-package-regression-") as tmp:
        tmp_path = Path(tmp)
        project_dir = tmp_path / "projects" / "sample"
        project_dir.mkdir(parents=True)
        (project_dir / "02_prd.final.md").write_text(
            "\n".join(
                [
                    "# Sample Operations Product",
                    "",
                    "The product helps operations users complete a reviewed workflow.",
                    "",
                    "## Page Notes",
                    "- Main workspace.",
                    "- Detail page.",
                    "- Review page.",
                    "",
                    "## Acceptance",
                    "- Main path works.",
                ]
            ),
            encoding="utf-8",
        )
        prototype_dir = project_dir / "prototype"
        prototype_dir.mkdir()
        (prototype_dir / "prototype_notes.txt").write_text("Approved prototype reference for external sharing.\n", encoding="utf-8")
        output = tmp_path / "B.zip"
        command = [
            sys.executable,
            str(base_dir / "pm-prd-copilot" / "scripts" / "package_b_delivery.py"),
            "--base-dir",
            str(base_dir),
            "--project-dir",
            str(project_dir),
            "--output",
            str(output),
        ]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            combined_output = f"{result.stdout}\n{result.stderr}".strip()
            return [f"B package packager failed on generic input. Output: {combined_output}"]
        if not output.exists():
            return ["B package packager did not create the expected zip."]
        with zipfile.ZipFile(output) as archive:
            names = set(archive.namelist())
        expected = {"README.md", "docs/A.md", "docs/B.md", "docs/C.md", "docs/D.md", "docs/E.md", "docs/F.md", "docs/H.md"}
        missing = sorted(expected - names)
        if missing:
            return [f"B package zip missing expected files: {', '.join(missing)}"]
        if "docs/G.md" in names:
            return ["B package for non-AI sample must not force an AI plan file."]
        if any(name.startswith("prototype/") for name in names):
            return ["B package must not include prototype files unless --include-prototype is explicit."]

        prototype_output = tmp_path / "B-with-prototype.zip"
        prototype_command = command[:-1] + [str(prototype_output), "--include-prototype"]
        prototype_result = subprocess.run(prototype_command, check=False, capture_output=True, text=True)
        if prototype_result.returncode != 0:
            combined_output = f"{prototype_result.stdout}\n{prototype_result.stderr}".strip()
            return [f"B package packager failed with explicit prototype include. Output: {combined_output}"]
        with zipfile.ZipFile(prototype_output) as archive:
            prototype_names = set(archive.namelist())
        if "prototype/prototype_notes.txt" not in prototype_names:
            return ["B package did not include approved prototype files when --include-prototype was explicit."]

        chinese_project = tmp_path / "projects" / "chinese-only"
        chinese_project.mkdir(parents=True)
        (chinese_project / "02_prd.final.md").write_text("# 中文项目\n\n这是中文需求，不能自动转成 B 包。\n", encoding="utf-8")
        chinese_output = tmp_path / "B-chinese.zip"
        chinese_command = [
            sys.executable,
            str(base_dir / "pm-prd-copilot" / "scripts" / "package_b_delivery.py"),
            "--base-dir",
            str(base_dir),
            "--project-dir",
            str(chinese_project),
            "--output",
            str(chinese_output),
        ]
        chinese_result = subprocess.run(chinese_command, check=False, capture_output=True, text=True)
        if chinese_result.returncode == 0:
            return ["B package packager must fail when no confirmed English source is available."]
        if "confirmed English source" not in f"{chinese_result.stdout}\n{chinese_result.stderr}":
            return ["B package packager failure must tell the user to provide a confirmed English source."]
    return []


def validate_preference_cache_policy(base_dir: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="pm-preference-cache-regression-") as tmp:
        tmp_path = Path(tmp)
        command = [
            sys.executable,
            str(base_dir / "pm-prd-copilot" / "scripts" / "manage_preference_cache.py"),
            "--base-dir",
            str(tmp_path),
            "--project",
            "sample",
            "--reason",
            "regression",
            "init",
        ]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            combined_output = f"{result.stdout}\n{result.stderr}".strip()
            return [f"Preference cache init failed. Output: {combined_output}"]
        current = json.loads((tmp_path / "memory-cache" / "projects" / "sample" / "current.json").read_text(encoding="utf-8"))
        policy = current.get("policy", {})
        required = {
            "scope": "project_only",
            "cross_project_reuse_allowed": False,
            "long_term_memory_requires_user_approval": True,
            "archive_alignment_required": True,
            "clear_after_project_archive_alignment": True,
            "store_in_project_closeout": True,
        }
        errors = [
            f"Preference cache policy.{key} must be {value!r}, got {policy.get(key)!r}"
            for key, value in required.items()
            if policy.get(key) != value
        ]
        active_path = tmp_path / str(current.get("active_cache_path"))
        manifest = json.loads((active_path / "manifest.json").read_text(encoding="utf-8"))
        isolation = manifest.get("isolation_policy", {})
        if isolation.get("do_not_read_other_project_caches") is not True:
            errors.append("Preference cache isolation must forbid reading other project caches.")
        if isolation.get("cross_project_reuse_allowed") is not False:
            errors.append("Preference cache isolation must disable cross-project reuse.")
        blocked_clear_command = [
            sys.executable,
            str(base_dir / "pm-prd-copilot" / "scripts" / "manage_preference_cache.py"),
            "--base-dir",
            str(tmp_path),
            "--project",
            "sample",
            "--reason",
            "regression",
            "clear",
        ]
        blocked_clear = subprocess.run(blocked_clear_command, check=False, capture_output=True, text=True)
        if blocked_clear.returncode == 0:
            errors.append("Preference cache clear must fail without explicit user approval.")
        if "--approved-by-user" not in f"{blocked_clear.stdout}\n{blocked_clear.stderr}":
            errors.append("Preference cache clear failure must mention --approved-by-user.")
        approved_archive_clear_command = [
            sys.executable,
            str(base_dir / "pm-prd-copilot" / "scripts" / "manage_preference_cache.py"),
            "--base-dir",
            str(tmp_path),
            "--project",
            "sample",
            "--reason",
            "regression-approved-archive-clear",
            "--approved-by-user",
            "archive-clear",
        ]
        approved_archive_clear = subprocess.run(
            approved_archive_clear_command,
            check=False,
            capture_output=True,
            text=True,
        )
        if approved_archive_clear.returncode != 0:
            errors.append(
                "Preference cache archive-clear with explicit approval must pass. "
                f"Output: {approved_archive_clear.stdout}\n{approved_archive_clear.stderr}"
            )
        cleared_current = json.loads(
            (tmp_path / "memory-cache" / "projects" / "sample" / "current.json").read_text(encoding="utf-8")
        )
        if cleared_current.get("status") != "cleared":
            errors.append("Preference cache approved archive-clear must mark current cache as cleared.")
        if cleared_current.get("user_approval_confirmed") is not True:
            errors.append("Preference cache approved archive-clear must record user_approval_confirmed=true.")
        return errors


def validate_internal_package_packager(base_dir: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="pm-internal-package-regression-") as tmp:
        tmp_path = Path(tmp)
        output = tmp_path / "internal.zip"
        command = [
            sys.executable,
            str(base_dir / "pm-prd-copilot" / "scripts" / "package_internal_delivery.py"),
            "--project-dir",
            str(base_dir / "projects" / "demo-project"),
            "--output",
            str(output),
        ]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            return [f"Internal package packager failed. Output: {result.stdout}\n{result.stderr}"]
        if not output.exists():
            return ["Internal package packager did not create output zip."]
        with zipfile.ZipFile(output) as archive:
            names = set(archive.namelist())
            manifest = json.loads(archive.read("MANIFEST.json").decode("utf-8"))
        required = {"README.md", "MANIFEST.json", "docs/02_prd.final.md"}
        missing = sorted(required - names)
        errors = [f"Internal package missing required file: {name}" for name in missing]
        forbidden_prefixes = ("runs/", "memory-cache/")
        forbidden = sorted(
            name for name in names if name.startswith(forbidden_prefixes) or name.endswith(".zip")
        )
        if forbidden:
            errors.append(f"Internal package must exclude run/cache/zip artifacts by default: {', '.join(forbidden)}")
        if manifest.get("package_type") != "trusted_internal":
            errors.append("Internal package manifest must declare package_type=trusted_internal.")
        if manifest.get("include_runs") is not False:
            errors.append("Internal package must exclude runs by default.")
        return errors


def _read_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _looks_like_ai_prd(text: str) -> bool:
    ai_terms = ("AI", "ai", "大模型", "模型路由", "智能体", "Agent", "RAG", "向量", "语义", "机器学习", "多模态")
    return any(term in text for term in ai_terms)


def validate_prd_structure_contract(base_dir: Path) -> list[str]:
    errors: list[str] = []
    demo_prd = base_dir / "projects" / "demo-project" / "02_prd.generated.md"
    taxi_prd = base_dir / "projects" / "taxi-hailing-prd-test" / "02_prd.final.md"

    if demo_prd.exists():
        text = _read_if_exists(demo_prd)
        raw_text = _read_if_exists(base_dir / "projects" / "demo-project" / "00_raw_input.md")
        forbidden = ["PRD 可视化层", "原型图 / 线框图"]
        for phrase in forbidden:
            if phrase in text:
                errors.append(f"{demo_prd}: must not contain centralized or default prototype section '{phrase}'.")
        for phrase in ["页面说明", "页面跳转关系", "原型图层"]:
            if phrase not in text:
                errors.append(f"{demo_prd}: must contain '{phrase}'.")
        if "AI 模型选型" in text and not _looks_like_ai_prd(raw_text):
            errors.append(f"{demo_prd}: non-AI PRD must not force an AI model selection section.")

    if not taxi_prd.exists():
        errors.append(f"Missing PRD golden sample: {taxi_prd}")
        return errors

    taxi_text = _read_if_exists(taxi_prd)
    for phrase in ["页面说明", "页面跳转关系", "原型图层"]:
        if phrase not in taxi_text:
            errors.append(f"{taxi_prd}: golden sample must contain '{phrase}'.")
    for phrase in ["PRD 可视化层", "原型图 / 线框图"]:
        if phrase in taxi_text:
            errors.append(f"{taxi_prd}: golden sample must not contain '{phrase}'.")
    if "当前边界：本阶段不输出 PNG，不输出 HTML" not in taxi_text:
        errors.append(f"{taxi_prd}: golden sample must preserve the confirmed PNG/HTML boundary.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Run lightweight regression checks")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    errors: list[str] = []

    schema_path = base_dir / "shared" / "schemas" / "requirement_brief.schema.json"
    candidate_path = base_dir / "projects" / "demo-project" / "01_requirement_brief.json"
    if schema_path.exists() and candidate_path.exists():
        errors.extend(validate_json(schema_path, candidate_path))

    prd_schema_path = base_dir / "shared" / "schemas" / "prd_document.schema.json"
    prd_candidate_path = base_dir / "projects" / "demo-project" / "02_prd.generated.json"
    if prd_schema_path.exists() and prd_candidate_path.exists():
        errors.extend(validate_json(prd_schema_path, prd_candidate_path))

    tracking_schema_path = base_dir / "shared" / "schemas" / "tracking_plan.schema.json"
    tracking_candidate_path = base_dir / "projects" / "demo-project" / "05_tracking_plan.generated.json"
    if tracking_schema_path.exists() and tracking_candidate_path.exists():
        errors.extend(validate_json(tracking_schema_path, tracking_candidate_path))
        tracking = json.loads(tracking_candidate_path.read_text(encoding="utf-8"))
        metric_names = {metric["name"] for metric in tracking.get("metrics", [])}
        for event in tracking.get("events", []):
            linked_metric = event.get("linked_metric")
            if linked_metric and linked_metric not in metric_names:
                errors.append(
                    f"{tracking_candidate_path}: linked_metric '{linked_metric}' is missing from metrics"
                )

    story_schema_path = base_dir / "shared" / "schemas" / "user_story.schema.json"
    stories_candidate_path = base_dir / "projects" / "demo-project" / "03_user_stories.generated.json"
    if story_schema_path.exists() and stories_candidate_path.exists():
        stories = json.loads(stories_candidate_path.read_text(encoding="utf-8"))
        if not isinstance(stories, list) or not stories:
            errors.append(f"{stories_candidate_path}: must contain a non-empty list")
        elif Draft202012Validator is not None:
            schema = json.loads(story_schema_path.read_text(encoding="utf-8"))
            validator = Draft202012Validator(schema)
            for story in stories:
                for error in validator.iter_errors(story):
                    errors.append(f"{stories_candidate_path}: {error.message}")

    stable_files = [
        base_dir / "pm-prd-copilot" / "SKILL.md",
        base_dir / "pm-prd-copilot" / "templates" / "prd_template_2026.md",
        base_dir / "pm-prd-copilot" / "memory" / "user_preferences.md",
        base_dir / "pm-prd-copilot" / "scripts" / "run_pipeline.py",
    ]
    for path in stable_files:
        if not path.exists():
            errors.append(f"Missing required file: {path}")

    errors.extend(validate_default_pipeline_gate(base_dir))
    errors.extend(validate_governed_pipeline_gate(base_dir))
    errors.extend(validate_fast_draft_pipeline_path(base_dir))
    errors.extend(validate_pipeline_manifest_stage_actions(base_dir))
    errors.extend(validate_candidate_plugin_visibility(base_dir))
    errors.extend(validate_b_package_packager(base_dir))
    errors.extend(validate_internal_package_packager(base_dir))
    errors.extend(validate_preference_cache_policy(base_dir))
    errors.extend(validate_prd_structure_contract(base_dir))

    if errors:
        print("Regression checks failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1 if args.strict else 0)

    print("Regression checks passed.")


if __name__ == "__main__":
    main()
