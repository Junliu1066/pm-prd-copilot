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


def _run_value_gate_case(base_dir: Path, raw_text: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="pm-value-gate-regression-") as tmp:
        fixture_dir = Path(tmp)
        for name in ["pm-prd-copilot", "shared"]:
            _link_or_copy(base_dir / name, fixture_dir / name)
        project = "__regression_value_gate__"
        raw_input = fixture_dir / "projects" / project / "00_raw_input.md"
        raw_input.parent.mkdir(parents=True, exist_ok=True)
        raw_input.write_text(raw_text, encoding="utf-8")
        command = [
            sys.executable,
            str(fixture_dir / "pm-prd-copilot" / "scripts" / "generate_value_gate.py"),
            "--base-dir",
            str(fixture_dir),
            "--project",
            project,
            "--mode",
            "rule",
        ]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            raise AssertionError(f"Value gate generation failed: {result.stdout}\n{result.stderr}")
        return json.loads((raw_input.parent / "00_value_gate.json").read_text(encoding="utf-8"))


def validate_value_gate_rules(base_dir: Path) -> list[str]:
    cases = [
        (
            "vague",
            "# AI 平台\n\n我想做一个 AI 平台，帮助企业提升效率。",
            "E_RESEARCH_REQUIRED",
        ),
        (
            "strong",
            "\n".join(
                [
                    "# 企业经营报告自动化",
                    "- 目标用户：企业财务用户、经营负责人",
                    "- 价值对象：客户预算方、采购决策者、财务使用者、客户验收方",
                    "- 商业结果：增加合同收入和真实利润，提升复购，降低人工成本",
                    "- 付费/收益方式：客户预算确认，愿意付定金，进入采购流程",
                    "- 使用场景：客户每周生成经营报告并给管理层复盘",
                    "- 风险边界：权限、隐私、合规边界已确认，数据来自客户授权",
                    "- 获客路径：现有客户渠道、销售线索和转介绍",
                    "- 成本结构：获客成本、交付成本、维护成本、售后成本均需核算",
                    "- 客户访谈显示强烈需求，预算意向明确，试点意向明确",
                ]
            ),
            "A_ENTER_PRD",
        ),
        (
            "geo_paid_service",
            "\n".join(
                [
                    "# GEO AI 检索曝光平台",
                    "- 目标用户：企业品牌方、营销负责人、增长负责人、同行服务商",
                    "- 价值对象：企业预算方、服务商客户、品牌负责人、营销使用者",
                    "- 商业结果：提升 AI 检索曝光、品牌可见度、获客线索和内容转化",
                    "- 付费/收益方式：公司已完成 MVP 实验，同行已经为 GEO 服务买单",
                    "- 使用场景：监测 DeepSeek、豆包、Qwen、腾讯元宝等 AI 平台的品牌提及和竞品曝光",
                    "- 风险边界：不承诺排名、不承诺收益、不刷量、不绕过平台规则，不做虚假内容和黑灰产优化",
                    "- 获客路径：已有企业客户、SEO/内容营销客户、AI 转型需求公司和同行服务商",
                    "- 成本结构：多平台测试、提示词样本库、行业词库、内容分析、人工审核和持续监测成本",
                ]
            ),
            "A_ENTER_PRD",
        ),
        (
            "client_project",
            "\n".join(
                [
                    "# 客户定制报表项目",
                    "- 目标用户：单个客户的运营团队",
                    "- 价值对象：客户预算方、客户验收方、运营使用者",
                    "- 商业结果：项目收入和交付案例沉淀",
                    "- 付费/收益方式：客户已签合同并真实支付",
                    "- 使用场景：客户项目交付中的定制报表生成",
                    "- 风险边界：权限和隐私边界由客户确认",
                    "- 获客路径：现有客户项目渠道",
                    "- 成本结构：交付成本、维护成本、沟通成本较高",
                    "- 客户项目强定制，暂不具备标准化复用条件",
                ]
            ),
            "C_CLIENT_PROJECT_VALIDATION",
        ),
        (
            "low_cost_mvp",
            "\n".join(
                [
                    "# 线索跟进助手低成本 MVP",
                    "- 目标用户：小微销售团队、销售主管",
                    "- 价值对象：销售主管、销售使用者、业务负责人",
                    "- 商业结果：提升线索跟进效率和转化率",
                    "- 付费/收益方式：当前只有用户试点意向和愿意体验，没有预算确认",
                    "- 使用场景：销售每天处理新线索并记录跟进状态",
                    "- 风险边界：只处理企业内部线索，权限和隐私边界可控",
                    "- 获客路径：现有私域客户和销售社群",
                    "- 成本结构：先用表格和人工审核降低开发成本",
                    "- 核心场景明确，核心功能可低成本 MVP 试点",
                ]
            ),
            "B_LOW_COST_MVP",
        ),
        (
            "internal",
            "\n".join(
                [
                    "# 内部交付质检提效",
                    "- 目标用户：内部交付团队",
                    "- 价值对象：内部业务负责人、交付团队、验收负责人",
                    "- 商业结果：降低人工成本，提升交付效率，减少错误率",
                    "- 付费/收益方式：节省人工成本和返工成本",
                    "- 使用场景：交付前自动检查材料完整性",
                    "- 风险边界：只处理内部材料，权限和隐私边界可控",
                    "- 获客路径：内部流程推广，不涉及对外获客",
                    "- 成本结构：建设成本、维护成本和人工节省需要核算",
                ]
            ),
            "D_INTERNAL_EFFICIENCY",
        ),
        (
            "not_recommended",
            "\n".join(
                [
                    "# 重交付定制门户",
                    "- 目标用户：不明确的企业客户",
                    "- 价值对象：客户可能感兴趣，但没有明确付费者和决策者",
                    "- 商业结果：商业结果弱，利润不成立",
                    "- 付费/收益方式：没人付费，只有口头兴趣",
                    "- 使用场景：客户临时提出的低频场景",
                    "- 风险边界：需要大量权限和数据对接",
                    "- 获客路径：获客困难，没有稳定渠道",
                    "- 成本结构：交付过重，维护成本高，无法规模化",
                    "- 不建议继续投入",
                ]
            ),
            "F_NOT_RECOMMENDED",
        ),
        (
            "redline",
            "# 投资收益助手\n\n目标用户是散户。承诺收益，自动荐股，帮助用户稳赚。",
            "G_BLOCKED_BY_REDLINE",
        ),
    ]
    errors: list[str] = []
    for label, raw_text, expected in cases:
        try:
            gate = _run_value_gate_case(base_dir, raw_text)
        except AssertionError as error:
            errors.append(str(error))
            continue
        if gate.get("decision_gate") != expected:
            errors.append(f"Value gate case {label} expected {expected}, got {gate.get('decision_gate')}.")
        if expected != "A_ENTER_PRD" and gate.get("can_enter_full_prd") is not False:
            errors.append(f"Value gate case {label} must not allow full PRD.")
        if expected == "A_ENTER_PRD" and gate.get("can_enter_full_prd") is not True:
            errors.append("Strong value gate case must allow full PRD.")
        if not gate.get("prd_input_package"):
            errors.append(f"Value gate case {label} must include prd_input_package for downstream handoff.")
        if "missing_count" not in gate.get("input_completeness", {}):
            errors.append(f"Value gate case {label} must report input completeness.")
        if expected == "B_LOW_COST_MVP" and gate.get("downstream_input_package") != "mvp_input_package":
            errors.append("Low-cost MVP case must route to mvp_input_package.")
        if expected == "F_NOT_RECOMMENDED" and not gate.get("blocked_reasons"):
            errors.append("Not-recommended case must explain blocked reasons.")
    return errors


def validate_value_gate_prd_blocking(base_dir: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="pm-value-gate-pipeline-") as tmp:
        fixture_dir = Path(tmp)
        for name in ["pm-prd-copilot", "shared", "workflow", "registry"]:
            _link_or_copy(base_dir / name, fixture_dir / name)
        project = "__regression_value_gate_block__"
        project_dir = fixture_dir / "projects" / project
        project_dir.mkdir(parents=True)
        (project_dir / "00_raw_input.md").write_text(
            "# 模糊平台想法\n\n我想做一个平台，帮企业提升效率。\n",
            encoding="utf-8",
        )
        (project_dir / "project_state.json").write_text(
            json.dumps(
                {
                    "project_id": project,
                    "current_stage": "intake",
                    "completed_stages": [],
                    "approvals": [],
                    "assumption_overrides": {},
                    "pipeline_assumption_overrides": {
                        "target_user_priority": True,
                        "core_scenario": True,
                        "mvp_scope": True,
                        "prototype_preview": True,
                        "prd_structure": True,
                    },
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        blocked_command = [
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
            "--no-trace",
        ]
        blocked = subprocess.run(blocked_command, check=False, capture_output=True, text=True)
        if blocked.returncode == 0:
            return ["Value gate must block full PRD when decision_gate is not A_ENTER_PRD."]
        if "Value gate blocked full PRD" not in f"{blocked.stdout}\n{blocked.stderr}":
            return ["Value gate PRD block must explain that the value gate blocked full PRD."]

        fast_command = [
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
            "--run-id",
            "fast-draft-regression",
        ]
        fast = subprocess.run(fast_command, check=False, capture_output=True, text=True)
        if fast.returncode != 0:
            return [f"Fast draft must explicitly bypass value gate for draft PRD. Output: {fast.stdout}\n{fast.stderr}"]
        manifest = json.loads((project_dir / "runs" / "fast-draft-regression" / "manifest.json").read_text(encoding="utf-8"))
        if manifest.get("value_gate_bypassed") is not True:
            return ["Fast draft manifest must mark value_gate_bypassed=true."]
        if manifest.get("governance_mode") != "fast_draft":
            return ["Fast draft manifest must keep governance_mode=fast_draft."]
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
    golden_case_dir = base_dir / "pm-prd-copilot" / "evals" / "golden_cases" / "zero_to_one_service_prd"
    golden_input = golden_case_dir / "input.md"
    golden_prd = golden_case_dir / "expected_prd.md"
    golden_acceptance = golden_case_dir / "acceptance.md"

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

    missing_golden_files = [path for path in [golden_input, golden_prd, golden_acceptance] if not path.exists()]
    if missing_golden_files:
        errors.extend(f"Missing PRD structure golden case file: {path}" for path in missing_golden_files)
        return errors

    golden_text = _read_if_exists(golden_prd)
    golden_input_text = _read_if_exists(golden_input)
    for phrase in ["页面说明", "页面跳转关系", "原型图层"]:
        if phrase not in golden_text:
            errors.append(f"{golden_prd}: golden case must contain '{phrase}'.")
    for phrase in ["PRD 可视化层", "原型图 / 线框图"]:
        if phrase in golden_text:
            errors.append(f"{golden_prd}: golden case must not contain '{phrase}'.")
    if "AI 模型选型" in golden_text and not _looks_like_ai_prd(golden_input_text):
        errors.append(f"{golden_prd}: non-AI golden case must not force an AI model selection section.")
    for phrase in ["taxi-hailing-prd-test", "打车产品 PRD 测试输入", "/Users/"]:
        if phrase in golden_text:
            errors.append(f"{golden_prd}: deidentified golden case must not contain '{phrase}'.")
    if "当前边界：本阶段不输出 PNG，不输出 HTML" not in golden_text:
        errors.append(f"{golden_prd}: golden case must preserve the confirmed PNG/HTML boundary.")
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

    value_gate_schema_path = base_dir / "shared" / "schemas" / "value_gate.schema.json"
    value_gate_candidate_path = base_dir / "projects" / "demo-project" / "00_value_gate.json"
    if value_gate_schema_path.exists() and value_gate_candidate_path.exists():
        errors.extend(validate_json(value_gate_schema_path, value_gate_candidate_path))

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
    errors.extend(validate_value_gate_rules(base_dir))
    errors.extend(validate_value_gate_prd_blocking(base_dir))
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
