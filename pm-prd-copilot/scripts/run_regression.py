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
                    "- 反证：如果客户只愿意免费试用但不愿意为报告付费，则商业价值不成立",
                    "- 停止条件：如果获客成本长期高于客单价，利润不成立",
                ]
            ),
            "B_LOW_COST_MVP",
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
        if expected == "A_ENTER_PRD" and label != "geo_paid_service" and gate.get("can_enter_full_prd") is not True:
            errors.append("Strong value gate case must allow full PRD.")
        if expected == "A_ENTER_PRD" and gate.get("value_judgment_passed") is not True:
            errors.append(f"Value gate case {label} must mark value_judgment_passed=true.")
        if not gate.get("execution_status"):
            errors.append(f"Value gate case {label} must include execution_status.")
        if not gate.get("input_package_quality_gate"):
            errors.append(f"Value gate case {label} must include input_package_quality_gate.")
        if not gate.get("prd_input_package"):
            errors.append(f"Value gate case {label} must include prd_input_package for downstream handoff.")
        if not gate.get("agent") or gate.get("agent", {}).get("name") != "Product Value Gate Agent":
            errors.append(f"Value gate case {label} must identify the product value gate agent.")
        if not gate.get("evidence_fetcher"):
            errors.append(f"Value gate case {label} must include evidence fetcher configuration.")
        if not gate.get("evidence_ledger"):
            errors.append(f"Value gate case {label} must include an evidence ledger.")
        if "safe_facts_for_prd" not in gate or "assumptions_for_prd" not in gate:
            errors.append(f"Value gate case {label} must split PRD-safe facts from assumptions.")
        if not gate.get("blocked_claims"):
            errors.append(f"Value gate case {label} must include blocked claims.")
        if not gate.get("hard_gate_scorecard"):
            errors.append(f"Value gate case {label} must include hard gate scorecard.")
        if not gate.get("path_recommendation"):
            errors.append(f"Value gate case {label} must include path recommendation.")
        if not gate.get("business_worth_verdict"):
            errors.append(f"Value gate case {label} must include business worth verdict.")
        if not gate.get("evidence_sufficiency_gate"):
            errors.append(f"Value gate case {label} must include evidence sufficiency gate.")
        if not gate.get("evidence_grade_gate"):
            errors.append(f"Value gate case {label} must include evidence grade gate.")
        if not gate.get("verified_evidence_gate"):
            errors.append(f"Value gate case {label} must include verified evidence gate.")
        if not gate.get("payment_evidence_verification"):
            errors.append(f"Value gate case {label} must include payment evidence verification.")
        if not gate.get("evidence_verification_intake"):
            errors.append(f"Value gate case {label} must include evidence verification intake.")
        if not gate.get("competitor_benchmark_table"):
            errors.append(f"Value gate case {label} must include competitor benchmark table.")
        if not gate.get("allowed_prd_type"):
            errors.append(f"Value gate case {label} must include allowed PRD type.")
        if not gate.get("industry_redline_rule_pack"):
            errors.append(f"Value gate case {label} must include industry redline rule pack.")
        if not gate.get("contextual_redline_filter"):
            errors.append(f"Value gate case {label} must include contextual redline filter.")
        if not gate.get("value_realization_timeline"):
            errors.append(f"Value gate case {label} must include value realization timeline.")
        if not gate.get("value_quality_scorecard"):
            errors.append(f"Value gate case {label} must include value quality scorecard.")
        if not gate.get("resource_advantage_matrix"):
            errors.append(f"Value gate case {label} must include resource advantage matrix.")
        if not gate.get("acquisition_decision_table"):
            errors.append(f"Value gate case {label} must include acquisition decision table.")
        if not gate.get("lightweight_profit_model"):
            errors.append(f"Value gate case {label} must include lightweight profit model.")
        if not gate.get("roi_input_table"):
            errors.append(f"Value gate case {label} must include ROI input table.")
        if not gate.get("roi_decision_model"):
            errors.append(f"Value gate case {label} must include ROI decision model.")
        if not gate.get("output_boundary_gate"):
            errors.append(f"Value gate case {label} must include output boundary gate.")
        if not gate.get("route_package_completeness_gate"):
            errors.append(f"Value gate case {label} must include route package completeness gate.")
        if not gate.get("rejudgment_package"):
            errors.append(f"Value gate case {label} must include rejudgment package.")
        if not gate.get("evidence_archive_policy"):
            errors.append(f"Value gate case {label} must include evidence archive policy.")
        if not gate.get("evidence_decision_basis"):
            errors.append(f"Value gate case {label} must include evidence decision basis.")
        if not gate.get("evidence_to_verdict_reasoning"):
            errors.append(f"Value gate case {label} must include evidence-to-verdict reasoning.")
        if not gate.get("operating_decision_model"):
            errors.append(f"Value gate case {label} must include operating decision model.")
        if not gate.get("decision_questions"):
            errors.append(f"Value gate case {label} must include decision questions.")
        if "missing_count" not in gate.get("input_completeness", {}):
            errors.append(f"Value gate case {label} must report input completeness.")
        if expected == "B_LOW_COST_MVP" and gate.get("downstream_input_package") != "mvp_input_package":
            errors.append("Low-cost MVP case must route to mvp_input_package.")
        route_package_name = gate.get("downstream_input_package")
        if route_package_name and not gate.get(route_package_name):
            errors.append(f"Value gate case {label} must include concrete route package: {route_package_name}.")
        if expected == "F_NOT_RECOMMENDED" and not gate.get("blocked_reasons"):
            errors.append("Not-recommended case must explain blocked reasons.")
        package = gate.get("prd_input_package", {})
        required_v03_sections = [
            "value_object_detail",
            "measurability_judgment",
            "attribution_judgment",
            "value_quality_judgment",
            "true_profit_judgment",
            "resource_fit_judgment",
            "acquisition_judgment",
            "project_to_product_judgment",
            "low_cost_mvp_judgment",
            "counter_evidence",
        ]
        for section in required_v03_sections:
            if not package.get(section):
                errors.append(f"Value gate case {label} must include V0.3 section: {section}.")
        if not gate.get("known_facts"):
            errors.append(f"Value gate case {label} must separate known facts from assumptions.")
        if label == "geo_paid_service":
            value_judgment = package.get("value_judgment", {})
            metrics = package.get("measurability_judgment", {}).get("metrics", [])
            primary_intent = gate.get("intent_result", {}).get("primary_intent", "")
            value_object = package.get("value_object_detail", {})
            path = gate.get("path_recommendation", {})
            route_decision = gate.get("route_decision", {})
            worth = gate.get("business_worth_verdict", {})
            operating = gate.get("operating_decision_model", {})
            profit_conditions = operating.get("minimum_profit_conditions", {})
            delivery_thresholds = operating.get("delivery_cost_thresholds", {})
            sufficiency = gate.get("evidence_sufficiency_gate", {})
            redline_pack = gate.get("industry_redline_rule_pack", {})
            contextual_redline = gate.get("contextual_redline_filter", {})
            profit_model = gate.get("lightweight_profit_model", {})
            evidence_grade_gate = gate.get("evidence_grade_gate", {})
            verified_gate = gate.get("verified_evidence_gate", {})
            payment_verification = gate.get("payment_evidence_verification", {})
            verification_intake = gate.get("evidence_verification_intake", {})
            competitor_table = gate.get("competitor_benchmark_table", {})
            roi_model = gate.get("roi_decision_model", {})
            roi_input_table = gate.get("roi_input_table", {})
            value_quality_scorecard = gate.get("value_quality_scorecard", {})
            resource_matrix = gate.get("resource_advantage_matrix", {})
            acquisition_table = gate.get("acquisition_decision_table", {})
            realization_timeline = gate.get("value_realization_timeline", {})
            output_boundary = gate.get("output_boundary_gate", {})
            route_gate = gate.get("route_package_completeness_gate", {})
            rejudgment = gate.get("rejudgment_package", {})
            source_quality = gate.get("source_quality_gate", {})
            research_agent = gate.get("evidence_research_agent", {})
            research_queue = gate.get("research_execution_queue", {})
            material_summary = gate.get("material_intake_summary", {})
            material_mapping = gate.get("material_to_evidence_mapping", [])
            rejudgment_readiness = gate.get("rejudgment_readiness_gate", {})
            external_research = gate.get("external_research_results", {})
            source_quality_scorecard = gate.get("source_quality_scorecard", {})
            pricing_evidence = gate.get("competitor_pricing_evidence", {})
            platform_rules = gate.get("platform_rule_evidence", {})
            verified_assessment = gate.get("verified_evidence_assessment", {})
            s_verified_gate = gate.get("s_claimed_to_s_verified_gate", {})
            real_profit = gate.get("real_profit_calculation", {})
            roi_scenario = gate.get("roi_scenario_analysis", {})
            investment_gate = gate.get("investment_decision_gate", {})
            attachment_plan = gate.get("attachment_verification_plan", {})
            rejudgment_execution = gate.get("rejudgment_execution_plan", {})
            client_package = gate.get("client_project_input_package", {})
            internal_package = gate.get("internal_efficiency_input_package", {})
            research_package = gate.get("research_input_package", {})
            evidence_basis = gate.get("evidence_decision_basis", [])
            evidence_reasoning = gate.get("evidence_to_verdict_reasoning", {})
            source_types = {entry.get("source_type") for entry in gate.get("evidence_ledger", [])}
            if "AI 提及率" not in metrics or "多模型一致性" not in metrics:
                errors.append("GEO paid service case must include GEO-specific metrics.")
            if value_judgment.get("primary_value_type") != "对外商业价值":
                errors.append("GEO paid service must keep external commercial value as the primary value type.")
            if any("内部" in item for item in [value_judgment.get("primary_value_type", "")]):
                errors.append("GEO paid service must not treat internal efficiency as the primary value type.")
            if "服务收入" not in value_judgment.get("primary_business_result", ""):
                errors.append("GEO paid service must define service/project revenue as the primary business result.")
            if not value_judgment.get("result_not_proven_yet"):
                errors.append("GEO paid service must list commercial results that are not proven yet.")
            if "对外商业产品" not in primary_intent:
                errors.append("GEO paid service case must be classified as an external commercial product.")
            if path.get("recommended_path") != "服务化 MVP PRD":
                errors.append("GEO paid service case must recommend service MVP PRD before full SaaS PRD.")
            if route_decision.get("recommended_path") != path.get("recommended_path"):
                errors.append("GEO paid service route_decision must be the canonical route summary.")
            if route_decision.get("canonical_decision") != gate.get("decision_gate"):
                errors.append("GEO paid service route_decision must mirror decision_gate for compatibility.")
            if route_decision.get("downstream_input_package") != "mvp_input_package":
                errors.append("GEO paid service route_decision must point to the MVP package.")
            if route_decision.get("rule", "").find("唯一主路由结论") == -1:
                errors.append("GEO paid service route_decision must define itself as the single routing source.")
            if "完整 SaaS PRD" not in path.get("deferred_paths", []):
                errors.append("GEO paid service case must defer full SaaS PRD.")
            if worth.get("verdict") != "worth_testing":
                errors.append("GEO paid service case must be worth testing rather than direct full SaaS.")
            if "服务化 MVP" not in worth.get("plain_conclusion", ""):
                errors.append("GEO paid service worth verdict must say service MVP is the current worthy scope.")
            if "完整 SaaS PRD" not in worth.get("not_worth_doing_scope", []):
                errors.append("GEO paid service worth verdict must mark full SaaS PRD as not worth doing now.")
            if not {"user_provided_fact", "external_public_source"}.issubset(source_types):
                errors.append("GEO paid service case must include user-provided and external public source evidence.")
            if not any("Gartner" in item.get("evidence", "") for item in evidence_basis):
                errors.append("GEO paid service case must include external AI search market-shift evidence.")
            if not any("月费区间" in item.get("evidence", "") for item in evidence_basis):
                errors.append("GEO paid service case must include external GEO pricing anchor evidence.")
            if not any(
                "Goodie" in item.get("evidence", "") or "SEORCE" in item.get("evidence", "")
                for item in evidence_basis
            ):
                errors.append("GEO paid service case must include competitor productization evidence.")
            if not any("不能证明" in item.get("does_not_prove", "") for item in evidence_basis):
                errors.append("GEO paid service evidence basis must state what each evidence item cannot prove.")
            if not all("fetch_status" in item for item in evidence_basis):
                errors.append("GEO paid service evidence basis must include fetch status for traceability.")
            if not evidence_reasoning.get("why_this_verdict_is_allowed"):
                errors.append("GEO paid service must explain how evidence supports the verdict.")
            if not evidence_reasoning.get("why_bigger_scope_is_not_allowed"):
                errors.append("GEO paid service must explain why bigger scope is not allowed.")
            if not gate.get("safe_facts_for_prd"):
                errors.append("GEO paid service case must expose source-backed PRD facts.")
            if "完整 SaaS 产品化已经成立" not in gate.get("blocked_claims", []):
                errors.append("GEO paid service case must block unsupported SaaS productization claims.")
            if "平台规则" not in redline_pack.get("triggered_domains", []):
                errors.append("GEO paid service must include platform-rule redline review.")
            if not profit_model.get("unknown_inputs"):
                errors.append("GEO paid service must expose profit model unknown inputs.")
            if rejudgment.get("current_route_package") != "mvp_input_package":
                errors.append("GEO paid service rejudgment package must point to MVP route package.")
            if gate.get("execution_status") != "routed_to_mvp":
                errors.append("GEO paid service case must route to MVP instead of full PRD execution.")
            if gate.get("can_enter_full_prd") is not False:
                errors.append("GEO paid service case must not set can_enter_full_prd=true before human confirmation.")
            if gate.get("allowed_prd_type") != "服务化 MVP PRD":
                errors.append("GEO paid service case must only allow service MVP PRD.")
            if sufficiency.get("overall_status") != "sufficient_for_mvp":
                errors.append("GEO paid service evidence sufficiency must be sufficient_for_mvp.")
            if "服务化 MVP" not in sufficiency.get("supported_paths", []):
                errors.append("GEO paid service evidence sufficiency must support service MVP.")
            if "完整 SaaS PRD" not in sufficiency.get("unsupported_paths", []):
                errors.append("GEO paid service evidence sufficiency must reject full SaaS PRD.")
            if "经营证据" not in sufficiency.get("missing_evidence_types", []) or "产品化证据" not in sufficiency.get("missing_evidence_types", []):
                errors.append("GEO paid service evidence sufficiency must identify operating and productization evidence gaps.")
            if source_quality.get("overall_status") != "usable_for_mvp_not_full_prd":
                errors.append("GEO paid service source quality gate must allow MVP but block full PRD.")
            if not source_quality.get("rows") or not source_quality.get("blocking_gaps_for_full_prd"):
                errors.append("GEO paid service source quality gate must list source rows and full PRD gaps.")
            source_counts = source_quality.get("source_counts", {})
            if source_counts.get("external_public_source", 0) < 5 or source_counts.get("competitor_rows", 0) < 8:
                errors.append("GEO paid service source quality gate must count external and competitor sources.")
            if research_agent.get("mode") != "v2_research_plan":
                errors.append("GEO paid service must include V2 evidence research agent plan.")
            research_track_keys = {item.get("key") for item in research_agent.get("research_tracks", [])}
            required_tracks = {
                "customer_payment_verification",
                "roi_operating_inputs",
                "competitor_productization",
                "platform_rule_risk",
                "acquisition_channel_validation",
                "market_shift_monitoring",
            }
            if not required_tracks.issubset(research_track_keys):
                errors.append("GEO paid service evidence research agent must cover payment, ROI, competitor, platform, acquisition, and market tracks.")
            if research_queue.get("mode") != "v2_1_executable_research_queue":
                errors.append("GEO paid service must include V2.1 executable research queue.")
            if research_queue.get("current_route_package") != "mvp_input_package":
                errors.append("GEO paid service research queue must stay on MVP route.")
            if research_queue.get("p0_task_count", 0) < 2:
                errors.append("GEO paid service research queue must mark payment and ROI tasks as P0.")
            queue_task_keys = {item.get("track_key") for item in research_queue.get("tasks", [])}
            if not required_tracks.issubset(queue_task_keys):
                errors.append("GEO paid service research queue must convert every research track into a task.")
            if not all(item.get("done_definition") and item.get("fail_or_downgrade_rule") for item in research_queue.get("tasks", [])):
                errors.append("GEO paid service research tasks must include done and downgrade rules.")
            if not all(item.get("writes_repo_files") is False for item in research_queue.get("tasks", [])):
                errors.append("GEO paid service research tasks must not write repo files by default.")
            if not any(item.get("owner_material_required") for item in research_queue.get("tasks", [])):
                errors.append("GEO paid service research queue must identify tasks that need owner materials.")
            output_contract = research_queue.get("task_output_contract", {})
            if "source_url_or_material_path" not in output_contract.get("required_fields", []):
                errors.append("GEO paid service research task output contract must require source URL or material path.")
            if "把用户声明伪装成外部验证" not in output_contract.get("invalid_outputs", []):
                errors.append("GEO paid service research output contract must reject fake external verification.")
            if material_summary.get("status") != "missing_critical_materials":
                errors.append("GEO paid service must keep material intake incomplete when no reviewed materials are attached.")
            if len(material_mapping) < 8:
                errors.append("GEO paid service material mapping must cover all required material slots.")
            if rejudgment_readiness.get("status") != "not_ready_missing_materials":
                errors.append("GEO paid service rejudgment readiness must block evidence upgrade without materials.")
            if verified_assessment.get("status") != "S_claimed":
                errors.append("GEO paid service must stay S_claimed before reviewed materials exist.")
            if s_verified_gate.get("can_upgrade_to_s_verified") is not False:
                errors.append("GEO paid service must not upgrade S_claimed to S_verified without reviewed materials.")
            if external_research.get("status") != "available" or external_research.get("row_count", 0) < 10:
                errors.append("GEO paid service external research results must include source-backed market and competitor rows.")
            if source_quality_scorecard.get("overall_status") not in {"usable_for_market_context", "has_source_risk"}:
                errors.append("GEO paid service source quality scorecard must classify external source usability.")
            if pricing_evidence.get("status") != "available":
                errors.append("GEO paid service must expose competitor pricing evidence.")
            if platform_rules.get("status") != "needs_platform_boundary_review":
                errors.append("GEO paid service must expose platform rule evidence and boundary review.")
            if real_profit.get("can_calculate") is not False:
                errors.append("GEO paid service real profit calculation must be blocked without ROI inputs.")
            if roi_scenario.get("status") != "roi_unavailable_missing_inputs":
                errors.append("GEO paid service ROI scenario analysis must stay unavailable without ROI inputs.")
            if investment_gate.get("conclusion") != "roi_unavailable_missing_inputs":
                errors.append("GEO paid service investment gate must block ROI conclusion without materials.")
            if investment_gate.get("requires_owner_approval") is not True:
                errors.append("GEO paid service investment gate must require owner approval.")
            if evidence_grade_gate.get("status") != "passes_current_gate_but_not_full_prd":
                errors.append("GEO paid service evidence grade gate must pass current MVP path but reject full PRD.")
            if "当前 decision_gate 不是 A_ENTER_PRD" not in evidence_grade_gate.get("full_prd_gap", []):
                errors.append("GEO paid service evidence grade gate must explain full PRD gap.")
            if verified_gate.get("status") != "claimed_strong_evidence_pending_verification":
                errors.append("GEO paid service must mark user-provided strong evidence as pending verification.")
            if verified_gate.get("can_treat_as_s_level") is not False:
                errors.append("GEO paid service must not treat unverified user claims as S-level verified evidence.")
            if not verified_gate.get("verification_required"):
                errors.append("GEO paid service verified evidence gate must list verification materials.")
            if payment_verification.get("claimed_payment_layer") != gate.get("payment_evidence_level"):
                errors.append("GEO paid service payment verification must preserve detected claimed payment layer.")
            if payment_verification.get("verified_payment_layer") != 0:
                errors.append("GEO paid service payment verification must keep verified layer at 0 before materials are checked.")
            if "完整 SaaS PRD" not in payment_verification.get("cannot_support", []):
                errors.append("GEO paid service unverified payment evidence must not support full SaaS PRD.")
            if verification_intake.get("status") != "verification_required":
                errors.append("GEO paid service evidence verification intake must require verification.")
            if not verification_intake.get("verification_slots") or len(verification_intake.get("verification_slots", [])) < 5:
                errors.append("GEO paid service evidence verification intake must include core verification slots.")
            verification_slot_keys = {item.get("key") for item in verification_intake.get("verification_slots", [])}
            required_verification_slots = {
                "payment_proof",
                "customer_record",
                "mvp_experiment_record",
                "delivery_acceptance_record",
                "repurchase_or_referral_record",
                "price_or_quote_record",
                "delivery_time_record",
                "acquisition_source_record",
            }
            if not required_verification_slots.issubset(verification_slot_keys):
                errors.append("GEO paid service evidence verification intake must include payment, customer, MVP, delivery, repurchase, price, time, and acquisition slots.")
            if not all(item.get("cannot_prove") for item in verification_intake.get("verification_slots", [])):
                errors.append("GEO paid service verification slots must state what each material cannot prove.")
            if "报价 / 客单价" not in verification_intake.get("accepted_evidence_types", []) or "交付工时" not in verification_intake.get("accepted_evidence_types", []):
                errors.append("GEO paid service evidence verification intake must accept quote/price and delivery-time evidence.")
            if attachment_plan.get("current_status") != "waiting_for_user_materials":
                errors.append("GEO paid service attachment verification plan must wait for user materials.")
            if attachment_plan.get("no_auto_verification") is not True:
                errors.append("GEO paid service attachment verification must not be automatic.")
            attachment_keys = {item.get("key") for item in attachment_plan.get("slots", [])}
            if not required_verification_slots.issubset(attachment_keys):
                errors.append("GEO paid service attachment verification plan must mirror evidence verification slots.")
            if competitor_table.get("status") != "available":
                errors.append("GEO paid service competitor benchmark table must be available.")
            competitor_rows = competitor_table.get("rows", [])
            markets = {row.get("market") for row in competitor_rows}
            if not {"中国", "海外"}.issubset(markets):
                errors.append("GEO paid service competitor benchmark table must include China and international competitors.")
            if len(competitor_rows) < 8:
                errors.append("GEO paid service competitor benchmark table must include enough market references.")
            if not all(row.get("source_url", "").startswith("http") for row in competitor_rows):
                errors.append("GEO paid service competitor benchmark rows must include source links.")
            if not any(row.get("name") == "KAWO GEO域见" for row in competitor_rows):
                errors.append("GEO paid service competitor benchmark must include a strong China reference.")
            if not any(row.get("name") == "Peec AI" for row in competitor_rows):
                errors.append("GEO paid service competitor benchmark must include a strong international reference.")
            if "不能单独证明" not in competitor_table.get("decision_rule", ""):
                errors.append("GEO paid service competitor benchmark must keep evidence boundaries clear.")
            if roi_model.get("status") != "roi_not_proven" or roi_model.get("can_claim_high_roi") is not False:
                errors.append("GEO paid service ROI model must not claim high ROI before cost data.")
            if roi_input_table.get("status") != "missing_critical_roi_inputs":
                errors.append("GEO paid service ROI input table must mark critical ROI inputs as missing.")
            if roi_input_table.get("can_claim_high_roi") is not False:
                errors.append("GEO paid service ROI input table must not allow high ROI claims.")
            if not roi_input_table.get("input_rows") or len(roi_input_table.get("input_rows", [])) < 6:
                errors.append("GEO paid service ROI input table must include concrete ROI input rows.")
            if "首期服务价格 / 最低客单价" not in roi_input_table.get("missing_critical_inputs", []):
                errors.append("GEO paid service ROI input table must require price evidence.")
            if roi_model.get("roi_input_table_status") != roi_input_table.get("status"):
                errors.append("GEO paid service ROI model must reference ROI input table status.")
            if not roi_model.get("scenario_table") or len(roi_model.get("scenario_table", [])) < 3:
                errors.append("GEO paid service ROI model must include conservative/base/optimistic scenarios.")
            if value_quality_scorecard.get("overall_status") != "needs_validation":
                errors.append("GEO paid service value quality scorecard must require validation before full PRD.")
            if not value_quality_scorecard.get("blocking_items_for_full_prd"):
                errors.append("GEO paid service value quality scorecard must expose full PRD blockers.")
            if resource_matrix.get("overall_status") != "needs_evidence":
                errors.append("GEO paid service resource advantage matrix must require evidence.")
            if not resource_matrix.get("rows") or len(resource_matrix.get("rows", [])) < 8:
                errors.append("GEO paid service resource advantage matrix must cover core resource dimensions.")
            if not resource_matrix.get("claimed_resource_advantages"):
                errors.append("GEO paid service must separate claimed resource advantages.")
            if resource_matrix.get("verified_resource_advantages"):
                errors.append("GEO paid service must not mark resource advantages as verified without records.")
            if not resource_matrix.get("why_us_not_proven"):
                errors.append("GEO paid service must explain why resource advantage is not proven yet.")
            if acquisition_table.get("overall_status") != "needs_validation":
                errors.append("GEO paid service acquisition table must require validation.")
            if "获客成本是否可控" not in acquisition_table.get("blocking_items_for_full_prd", []):
                errors.append("GEO paid service acquisition table must block full PRD without CAC evidence.")
            if "平台规则" not in contextual_redline.get("active_domains", []):
                errors.append("GEO paid service contextual redline filter must keep platform rules active.")
            if "支付资金" not in contextual_redline.get("excluded_domains", []):
                errors.append("GEO paid service contextual redline filter must exclude irrelevant payment-fund checks.")
            if route_gate.get("route_package") != "mvp_input_package" or route_gate.get("can_route_to_next_module") is not True:
                errors.append("GEO paid service route package completeness gate must allow MVP handoff.")
            if route_gate.get("status") != "complete":
                errors.append("GEO paid service route package completeness gate must be complete after V1.5 specificity hardening.")
            mvp_package = gate.get("mvp_input_package", {})
            for key in ["free_diagnosis_entry", "diagnosis_report", "metric_dashboard", "recheck_mechanism", "optimization_suggestions", "service_conversion_path", "execution_record_template"]:
                if not mvp_package.get(key):
                    errors.append(f"GEO paid service MVP package must include {key}.")
            mvp_success_text = " ".join(mvp_package.get("success_criteria", []))
            for term in ["免费检测提交数", "有效线索率", "加顾问率", "体检报告成交率", "单客户交付工时", "复盘预约率", "后续优化", "代运营"]:
                if term not in mvp_success_text:
                    errors.append(f"GEO paid service MVP success criteria must include {term}.")
            mvp_failure_text = " ".join(mvp_package.get("failure_criteria", []))
            for term in ["只愿免费", "报告", "交付工时", "无法归因", "复测", "复购"]:
                if term not in mvp_failure_text:
                    errors.append(f"GEO paid service MVP failure criteria must include {term}.")
            mvp_loop_text = " ".join(mvp_package.get("minimum_data_loop", []))
            for term in ["品牌提及", "竞品提及", "引用来源", "诊断报告", "优化动作", "复测结果", "成交"]:
                if term not in mvp_loop_text:
                    errors.append(f"GEO paid service MVP data loop must include {term}.")
            if realization_timeline.get("status") != "timeline_unverified_blocks_scaling":
                errors.append("GEO paid service value realization timeline must block scaling until timeline is verified.")
            if not any(item.get("stage") == "产品化复判" for item in realization_timeline.get("milestones", [])):
                errors.append("GEO paid service value realization timeline must include productization rejudgment.")
            if output_boundary.get("status") != "within_boundary":
                errors.append("GEO paid service output boundary gate must stay within value-gate scope.")
            if "完整 PRD 正文" not in output_boundary.get("forbidden_outputs", []):
                errors.append("GEO paid service output boundary gate must forbid full PRD generation.")
            if output_boundary.get("does_not_rank_against_other_projects") is not True:
                errors.append("Value gate must explicitly avoid cross-project priority ranking.")
            if "优先级" not in output_boundary.get("priority_boundary_rule", ""):
                errors.append("Value gate priority boundary must be explicit.")
            if not client_package.get("acceptance_criteria") or not client_package.get("reuse_observation_table"):
                errors.append("Client project route package must include acceptance criteria and reuse observation table.")
            if not internal_package.get("roi_inputs_required") or not internal_package.get("payback_period"):
                errors.append("Internal efficiency route package must include ROI inputs and payback period.")
            if not research_package.get("interview_questions") or not research_package.get("payment_test_method"):
                errors.append("Research route package must include interview questions and payment test method.")
            if "2-4 周" not in operating.get("validation_window", ""):
                errors.append("GEO paid service operating model must recommend a 2-4 week validation window.")
            if "完整 SaaS PRD" not in worth.get("not_worth_doing_scope", []):
                errors.append("GEO paid service operating model must keep full SaaS outside current worthy scope.")
            if profit_conditions.get("price_floor") != "待确认":
                errors.append("GEO paid service must not invent price floor evidence.")
            if delivery_thresholds.get("max_delivery_hours_per_customer") != "待确认":
                errors.append("GEO paid service must not invent delivery hour thresholds.")
            if not operating.get("upgrade_to_product_conditions"):
                errors.append("GEO paid service must include upgrade-to-product conditions.")
            if not operating.get("stop_or_downgrade_conditions"):
                errors.append("GEO paid service must include stop or downgrade conditions.")
            if rejudgment.get("next_path_execution_record_required") is not True:
                errors.append("GEO paid service must require execution records before rejudgment.")
            if "体检报告成交率" not in rejudgment.get("required_validation_records", []):
                errors.append("GEO paid service MVP route must require concrete conversion records.")
            if not rejudgment.get("rejudgment_input_required"):
                errors.append("GEO paid service must list rejudgment input requirements.")
            if rejudgment_execution.get("current_route_package") != "mvp_input_package":
                errors.append("GEO paid service rejudgment execution plan must target MVP route.")
            if rejudgment_execution.get("owner_review_required") is not True:
                errors.append("GEO paid service rejudgment execution must require owner review.")
            if "体检报告成交率" not in rejudgment_execution.get("records_to_collect", []):
                errors.append("GEO paid service rejudgment execution must collect concrete MVP conversion records.")
            if not rejudgment_execution.get("upgrade_check", {}).get("conditions") or not rejudgment_execution.get("stop_or_downgrade_check", {}).get("conditions"):
                errors.append("GEO paid service rejudgment execution must include upgrade and stop conditions.")
            if "法务" in value_object.get("core_user", []):
                errors.append("GEO paid service core_user must not include legal/compliance reviewer roles.")
            if not set(value_object.get("possible_opponents", [])) & {"法务", "合规", "平台规则"}:
                errors.append("GEO paid service must classify legal/compliance as possible opponents or reviewers.")
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
