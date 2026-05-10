#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError:  # pragma: no cover - optional local dependency
    Draft202012Validator = None


FIELD_ALIASES = {
    "需求标题": "title",
    "提出人": "requester",
    "来源渠道": "channel",
    "业务线": "business_context",
    "希望上线时间": "desired_launch_date",
    "需求类型": "request_type_raw",
    "原始描述": "raw_description",
    "当前痛点": "pain_point",
    "影响角色": "target_users_raw",
    "影响规模 / 证据": "evidence_raw",
    "不做的后果": "consequence",
    "现有假设": "assumptions_raw",
    "依赖项": "dependencies_raw",
    "待确认问题": "open_questions_raw",
}

TARGET_USER_KEYWORDS = [
    "企业品牌方",
    "品牌方",
    "营销负责人",
    "内容负责人",
    "增长负责人",
    "SEO/GEO 服务商",
    "SEO 服务商",
    "GEO 服务商",
    "服务商",
    "企业客户",
    "老板",
    "决策者",
    "采购",
    "商家财务",
    "商家管理员",
    "管理员",
    "客服",
    "运营",
    "法务",
    "审核员",
    "用户",
    "财务",
]


def project_paths(base_dir: Path, project: str) -> dict[str, Path]:
    project_dir = base_dir / "projects" / project
    return {
        "project_dir": project_dir,
        "raw_input": project_dir / "00_raw_input.md",
        "value_gate_materials_json": project_dir / "00_value_gate_materials.json",
        "value_gate_json": project_dir / "00_value_gate.json",
        "value_gate_md": project_dir / "00_value_gate.md",
        "value_gate_prd_input_json": project_dir / "00_value_gate_prd_input.json",
        "value_gate_owner_decision_md": project_dir / "00_value_gate_owner_decision.md",
        "value_gate_owner_summary_md": project_dir / "00_value_gate_owner_summary.md",
        "value_gate_evidence_snapshot_json": project_dir / "00_value_gate_evidence_snapshot.json",
        "brief_json": project_dir / "01_requirement_brief.json",
        "brief_md": project_dir / "01_requirement_brief.md",
        "brief_meta": project_dir / "01_requirement_brief.meta.json",
        "prd_json": project_dir / "02_prd.generated.json",
        "prd_md": project_dir / "02_prd.generated.md",
        "prd_meta": project_dir / "02_prd.generated.meta.json",
        "prd_context_digest_json": project_dir / "analysis" / "prd_context_digest.json",
        "prd_final_md": project_dir / "02_prd.final.md",
        "stories_json": project_dir / "03_user_stories.generated.json",
        "stories_md": project_dir / "03_user_stories.generated.md",
        "stories_meta": project_dir / "03_user_stories.generated.meta.json",
        "stories_final_md": project_dir / "03_user_stories.final.md",
        "risk_json": project_dir / "04_risk_check.generated.json",
        "risk_md": project_dir / "04_risk_check.generated.md",
        "risk_meta": project_dir / "04_risk_check.generated.meta.json",
        "tracking_json": project_dir / "05_tracking_plan.generated.json",
        "tracking_md": project_dir / "05_tracking_plan.generated.md",
        "tracking_meta": project_dir / "05_tracking_plan.generated.meta.json",
        "review_merge_md": project_dir / "06_review_merge.md",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def default_value_gate_materials(project_id: str) -> dict:
    return {
        "project_id": project_id,
        "version": VALUE_GATE_VERSION,
        "materials": [
            {
                "material_id": f"mat-{index:03d}",
                "slot_key": slot_key,
                "material_type": "待填写",
                "title": slot["label"],
                "occurred_at": "待填写",
                "source_path_or_url": "待填写",
                "redaction_status": "redacted",
                "summary": "待填写",
                "proves": slot["supports"],
                "does_not_prove": slot["cannot_prove"],
                "review_status": "missing",
            }
            for index, (slot_key, slot) in enumerate(VALUE_GATE_MATERIAL_SLOTS.items(), 1)
        ],
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp_path, path)


def write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def validate_schema(schema_path: Path, payload: object) -> list[str]:
    if Draft202012Validator is None:
        return []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return validate_schema_object(schema, payload)


def validate_schema_object(schema: dict, payload: object) -> list[str]:
    if Draft202012Validator is None:
        return []
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
    return [error.message for error in errors]


def extract_template_fields(raw_text: str) -> dict[str, str]:
    results: dict[str, str] = {}
    for line in raw_text.splitlines():
        stripped = re.sub(r"^\s*[-*]\s*", "", line.strip())
        if "：" not in stripped and ":" not in stripped:
            continue
        key, value = re.split(r"[：:]", stripped, maxsplit=1)
        key = key.strip()
        value = value.strip()
        if key in FIELD_ALIASES and value:
            results[FIELD_ALIASES[key]] = value
    return results


def split_items(value: str) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[、,，;/；|]\s*", value)
    return unique_list(part.strip() for part in parts if part.strip())


def unique_list(items) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def has_specific_value(value) -> bool:
    if isinstance(value, list):
        return any(has_specific_value(item) for item in value)
    if value is None:
        return False
    text = str(value).strip()
    return bool(text and text not in VALUE_GATE_GENERIC_VALUES and "待验证" not in text)


def filter_core_users(users: list[str]) -> list[str]:
    filtered = [user for user in users if user not in VALUE_GATE_OPPONENT_ROLES and user not in {"用户", "法务"}]
    return unique_list(filtered or users)


def extract_bullets(raw_text: str) -> list[str]:
    bullets = []
    for line in raw_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            bullets.append(stripped[2:].strip())
    return unique_list(bullets)


def extract_title(raw_text: str, fields: dict[str, str], fallback: str) -> str:
    for line in raw_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fields.get("title") or fallback


def infer_request_type(raw_text: str, fields: dict[str, str]) -> str:
    text = f"{fields.get('request_type_raw', '')} {raw_text}".lower()
    if any(token in text for token in ["bug", "缺陷", "报错", "异常"]):
        return "bugfix"
    if any(token in text for token in ["合规", "法务", "审计", "监管"]):
        return "compliance"
    if any(token in text for token in ["重构", "技术债", "tech debt"]):
        return "tech_debt"
    if any(token in text for token in ["优化", "提升", "降低", "改进"]):
        return "optimization"
    if any(token in text for token in ["功能", "新增", "支持", "导出"]):
        return "new_feature"
    return "other"


def infer_target_users(raw_text: str, fields: dict[str, str]) -> list[str]:
    users = split_items(fields.get("target_users_raw", ""))
    if users:
        return users
    found = []
    for keyword in TARGET_USER_KEYWORDS:
        if keyword in raw_text:
            found.append(keyword)
    if len(found) > 1 and "用户" in found:
        found.remove("用户")
    if not found:
        found = ["业务方", "运营"]
    return unique_list(found)


def infer_urgency(raw_text: str) -> str:
    lowered = raw_text.lower()
    for level in ["p0", "p1", "p2", "p3"]:
        if level in lowered:
            return level
    if any(token in raw_text for token in ["紧急", "尽快", "投诉", "合规", "本周", "月底"]):
        return "p1"
    if any(token in raw_text for token in ["优化", "提升", "改进"]):
        return "p2"
    return "unknown"


def infer_problem_statement(title: str, fields: dict[str, str], bullets: list[str], users: list[str]) -> str:
    pain_point = fields.get("pain_point", "")
    consequence = fields.get("consequence", "")
    if pain_point:
        base = pain_point
    elif bullets:
        base = bullets[0]
    else:
        base = f"{'、'.join(users)}在相关场景下处理效率不足"
    if consequence:
        return f"{base}，导致{consequence}。"
    return f"{base}，需要通过“{title}”提升业务处理效率。"


def infer_business_goal(fields: dict[str, str], title: str) -> str:
    if fields.get("consequence"):
        return f"降低{fields['consequence']}"
    if "导出" in title:
        return "提升信息获取与对账效率，降低人工支持成本"
    if "权限" in title:
        return "降低合规与越权风险"
    return "提升关键流程效率并降低协作成本"


def infer_scenarios(raw_text: str, title: str) -> list[str]:
    scenarios = []
    if is_geo_context(raw_text):
        scenarios.extend(["AI 检索品牌曝光监测", "竞品曝光对比", "内容资产优化复测"])
    if "月底" in raw_text:
        scenarios.append("月底对账场景")
    if "客服" in raw_text:
        scenarios.append("客服协助查询场景")
    if "导出" in title:
        scenarios.append("后台批量导出场景")
    if not scenarios:
        scenarios.append("核心业务处理场景")
    return unique_list(scenarios)


def infer_evidence(fields: dict[str, str], bullets: list[str]) -> list[str]:
    evidence = split_items(fields.get("evidence_raw", ""))
    for bullet in bullets:
        if any(token in bullet for token in ["频繁", "经常", "投诉", "工单", "低", "慢", "追着"]):
            evidence.append(bullet)
    return unique_list(evidence)


def infer_assumptions(fields: dict[str, str], title: str, request_type: str) -> list[str]:
    assumptions = split_items(fields.get("assumptions_raw", ""))
    if assumptions:
        return assumptions
    if is_geo_context(title):
        assumptions.extend(
            [
                "AI 检索曝光可以通过问题样本、品牌提及、竞品提及和引用来源进行周期性监测",
                "客户愿意为可解释的诊断报告、优化建议和复测结果持续付费",
            ]
        )
        return unique_list(assumptions)
    if "导出" in title:
        assumptions.append("第一期以 CSV 导出即可覆盖主要使用场景")
    if request_type == "optimization":
        assumptions.append("优化现有流程比完全重做更快见效")
    if not assumptions:
        assumptions.append("第一期应先提供最小可上线闭环，再逐步扩展")
    return unique_list(assumptions)


def infer_dependencies(fields: dict[str, str], title: str) -> list[str]:
    dependencies = split_items(fields.get("dependencies_raw", ""))
    if "导出" in title:
        dependencies.extend(["权限系统", "数据查询接口", "日志或审计能力"])
    return unique_list(dependencies)


def infer_constraints(fields: dict[str, str], title: str) -> list[str]:
    constraints = []
    if fields.get("desired_launch_date"):
        constraints.append(f"目标上线时间：{fields['desired_launch_date']}")
    if "导出" in title:
        constraints.extend(["需要考虑大数据量性能", "需要明确敏感字段脱敏规则"])
    return unique_list(constraints)


def infer_open_questions(fields: dict[str, str], title: str) -> list[str]:
    questions = split_items(fields.get("open_questions_raw", ""))
    if questions:
        return questions
    if is_geo_context(title):
        questions.extend(
            [
                "首期覆盖哪些 AI 平台和行业？",
                "品牌曝光、推荐和引用质量的基线如何定义？",
                "客户买单的是 SaaS、诊断报告、持续监测还是服务交付？",
                "复测周期和效果归因口径如何定义？",
            ]
        )
    elif "导出" in title:
        questions.extend(
            [
                "导出字段范围是什么？",
                "哪些角色有权限导出？",
                "是否需要脱敏和审计日志？",
                "大数据量场景是否需要异步导出？",
            ]
        )
    elif "权限" in title:
        questions.extend(["权限粒度如何定义？", "是否需要操作审计？"])
    else:
        questions.extend(["本期最小上线闭环是什么？", "哪些依赖需要前置确认？"])
    return unique_list(questions)


def infer_scope(title: str, request_type: str) -> dict[str, list[str]]:
    if "导出" in title:
        return {
            "mvp": ["按日期范围导出", "角色权限控制", "导出行为审计"],
            "v1": ["支持常用筛选条件", "导出失败原因提示"],
            "later": ["自定义字段", "任务中心式异步导出", "移动端支持"],
        }
    if request_type == "bugfix":
        return {
            "mvp": ["修复核心问题场景", "补齐监控与告警"],
            "v1": ["补齐回归测试"],
            "later": ["相关流程体验优化"],
        }
    return {
        "mvp": ["先覆盖最高频主流程", "补齐最小可用校验与权限"],
        "v1": ["补齐次要场景"],
        "later": ["扩展低频增强能力"],
    }


VALUE_GATE_VERSION = "2.6.0"
VALUE_GATE_AGENT_NAME = "Product Value Gate Agent"
VALUE_GATE_ALLOW_PRD = "A_ENTER_PRD"
VALUE_GATE_DECISIONS = {
    "A_ENTER_PRD",
    "B_LOW_COST_MVP",
    "C_CLIENT_PROJECT_VALIDATION",
    "D_INTERNAL_EFFICIENCY",
    "E_RESEARCH_REQUIRED",
    "F_NOT_RECOMMENDED",
    "G_BLOCKED_BY_REDLINE",
}
VALUE_GATE_NEXT_MODULE = {
    "A_ENTER_PRD": "full_prd_generation",
    "B_LOW_COST_MVP": "low_cost_mvp_plan",
    "C_CLIENT_PROJECT_VALIDATION": "client_project_validation",
    "D_INTERNAL_EFFICIENCY": "internal_efficiency_plan",
    "E_RESEARCH_REQUIRED": "research_completion",
    "F_NOT_RECOMMENDED": "stop_with_reason",
    "G_BLOCKED_BY_REDLINE": "redline_block",
}
VALUE_GATE_ROUTE_PACKAGE = {
    "A_ENTER_PRD": "prd_input_package",
    "B_LOW_COST_MVP": "mvp_input_package",
    "C_CLIENT_PROJECT_VALIDATION": "client_project_input_package",
    "D_INTERNAL_EFFICIENCY": "internal_efficiency_input_package",
    "E_RESEARCH_REQUIRED": "research_input_package",
    "F_NOT_RECOMMENDED": "stop_reason_package",
    "G_BLOCKED_BY_REDLINE": "redline_block_package",
}
VALUE_GATE_EXECUTION_STATUS = {
    "B_LOW_COST_MVP": "routed_to_mvp",
    "C_CLIENT_PROJECT_VALIDATION": "routed_to_client_project",
    "D_INTERNAL_EFFICIENCY": "routed_to_internal_efficiency",
    "E_RESEARCH_REQUIRED": "routed_to_research",
    "F_NOT_RECOMMENDED": "stopped",
    "G_BLOCKED_BY_REDLINE": "blocked_by_redline",
}
VALUE_GATE_GENERIC_VALUES = {"", "待验证", "用户", "客户", "企业", "团队", "业务方", "运营", "相关用户"}
VALUE_GATE_OPPONENT_ROLES = {"法务", "合规", "预算负责人", "现有服务商", "平台规则"}
VALUE_GATE_HARD_GATE_LABELS = {
    "value_object": "价值对象",
    "business_result": "商业结果",
    "metrics": "衡量指标",
    "attribution": "价值归因",
    "evidence_level": "证据等级",
    "payment_evidence": "付费证据",
    "true_profit": "真实利润",
    "acquisition": "获客路径",
    "resource_fit": "资源匹配",
    "productization": "产品化价值",
    "redline": "红线风险",
}
VALUE_GATE_ALLOWED_PRD_TYPE = {
    "A_ENTER_PRD": "完整 PRD",
    "B_LOW_COST_MVP": "服务化 MVP PRD",
    "C_CLIENT_PROJECT_VALIDATION": "客户项目验证方案",
    "D_INTERNAL_EFFICIENCY": "内部提效方案",
    "E_RESEARCH_REQUIRED": "调研补全方案",
    "F_NOT_RECOMMENDED": "不允许生成 PRD",
    "G_BLOCKED_BY_REDLINE": "不允许生成 PRD",
}
VALUE_GATE_EVIDENCE_SUFFICIENCY_STATUSES = {
    "sufficient_for_full_prd",
    "sufficient_for_mvp",
    "sufficient_for_client_project",
    "sufficient_for_internal_efficiency",
    "research_required",
    "insufficient_stop",
    "blocked_by_redline",
}
VALUE_GATE_EVIDENCE_TYPE_MATRIX = {
    "商业价值证据": ["真实付款", "合同", "预算", "复购", "付费意向"],
    "需求证据": ["访谈", "试点", "使用数据", "留资", "预约", "明确场景"],
    "市场 / 对象证据": ["平台存在", "竞品存在", "行业趋势"],
    "经营证据": ["客单价", "获客成本", "交付工时", "复购周期", "维护成本"],
    "产品化证据": ["多个相似客户", "标准化流程", "边际成本下降", "可复用能力"],
    "红线证据": ["合规", "隐私", "行业规则", "平台规则"],
}
VALUE_GATE_MATERIAL_REVIEW_STATUSES = {
    "missing",
    "submitted_pending_review",
    "reviewed_accepted",
    "reviewed_rejected",
    "needs_more_context",
}
VALUE_GATE_MATERIAL_SLOTS = {
    "payment_proof": {
        "label": "付款 / 合同证据",
        "category": "商业价值证据",
        "supports": ["真实买单", "预算 / 采购流程", "S_claimed 复核"],
        "cannot_prove": ["复购", "ROI", "SaaS 产品化成立"],
    },
    "customer_record": {
        "label": "客户 / 行业记录",
        "category": "需求证据",
        "supports": ["目标客户清晰", "决策 / 付费对象清晰"],
        "cannot_prove": ["客户复购", "获客成本可控"],
    },
    "mvp_experiment_record": {
        "label": "MVP 实验记录",
        "category": "需求证据",
        "supports": ["服务闭环已试跑", "核心价值链路可复判"],
        "cannot_prove": ["真实利润", "规模化产品化"],
    },
    "delivery_acceptance_record": {
        "label": "交付 / 验收记录",
        "category": "经营证据",
        "supports": ["交付结果和验收状态", "返工 / 维护成本复判"],
        "cannot_prove": ["获客成本", "复购意愿"],
    },
    "repurchase_or_referral_record": {
        "label": "复购 / 续费 / 转介绍记录",
        "category": "产品化证据",
        "supports": ["持续价值", "LTV / 产品化升级候选"],
        "cannot_prove": ["首单获客成本", "交付边际成本下降"],
    },
    "price_or_quote_record": {
        "label": "报价 / 客单价证据",
        "category": "经营证据",
        "supports": ["收入输入", "最低利润条件"],
        "cannot_prove": ["成交真实", "交付成本可控"],
    },
    "delivery_time_record": {
        "label": "交付工时证据",
        "category": "经营证据",
        "supports": ["交付成本", "边际成本判断"],
        "cannot_prove": ["客户愿意付费", "获客可控"],
    },
    "acquisition_source_record": {
        "label": "获客来源证据",
        "category": "经营证据",
        "supports": ["冷启动来源", "CAC/LTV 复判输入"],
        "cannot_prove": ["服务价值成立", "复购成立"],
    },
}
VALUE_GATE_INPUT_CHECKS = {
    "target_user": "目标用户",
    "value_object": "价值对象",
    "business_result": "商业结果",
    "revenue_or_benefit": "付费 / 收益方式",
    "usage_scenario": "使用场景",
    "risk_boundary": "风险边界",
    "acquisition_path": "获客路径",
    "cost_structure": "成本结构",
}
VALUE_GATE_CONFLICT_ITEMS = [
    {
        "function": "完整 18 步价值判断链路",
        "classification": "direct_v0",
        "governance_check": "V0 只做轻量规则判断，复杂证据和财务深算留到 V1/V2。",
        "recommendation": "先纳入结构化输出和保守门禁，不扩大成重型自动化。",
    },
    {
        "function": "行业红线规则包",
        "classification": "v1_v2",
        "governance_check": "全量行业规则包会变成重能力和持续维护面。",
        "recommendation": "V0 只做红线关键词和人工确认提醒；V1 再沉淀行业规则包。",
    },
    {
        "function": "后续模块必须读取 decision_gate",
        "classification": "direct_v0",
        "governance_check": "符合治理架构，能防止 PRD 绕过前置价值判断。",
        "recommendation": "直接纳入 pipeline 和 PRD 二次门禁。",
    },
    {
        "function": "自动联网抓取证据",
        "classification": "needs_user_confirmation",
        "governance_check": "会引入网络证据、成本、事实核验和来源治理。",
        "recommendation": "V0 不做；后续如需要，单独走证据能力和来源审核。",
    },
    {
        "function": "新增专门 skill / harness",
        "classification": "needs_user_confirmation",
        "governance_check": "违反本轮最小新增原则；真实使用证明必要前不新增。",
        "recommendation": "V0 用 native script + existing pipeline contract 承接。",
    },
    {
        "function": "复盘闭环和长期规则反哺",
        "classification": "rewrite_before_include",
        "governance_check": "不能自动写长期记忆或 stable 规则。",
        "recommendation": "V0 只输出 closeout/复判候选，长期化必须用户批准。",
    },
]


def contains_any(text: str, terms: tuple[str, ...] | list[str]) -> bool:
    return any(term and term in text for term in terms)


def infer_mentions(raw_text: str, candidates: tuple[str, ...] | list[str], fallback: list[str] | None = None) -> list[str]:
    found = [candidate for candidate in candidates if candidate and candidate in raw_text]
    return unique_list(found or (fallback or []))


def is_geo_context(raw_text: str) -> bool:
    return contains_any(
        raw_text,
        (
            "GEO",
            "AI 检索",
            "AI搜索",
            "AI 搜索",
            "AI 问答",
            "DeepSeek",
            "豆包",
            "Qwen",
            "通义",
            "元宝",
            "品牌提及",
            "竞品曝光",
            "检索曝光",
        ),
    )


def contains_positive_any(text: str, terms: tuple[str, ...] | list[str]) -> bool:
    negation_markers = (
        "没有",
        "无",
        "未",
        "暂无",
        "不是",
        "不具备",
        "不能",
        "不会",
        "不做",
        "不涉及",
        "不承诺",
        "不保证",
        "不刷量",
        "不绕过",
        "不伪造",
        "不输出",
        "禁止",
        "避免",
        "尚无",
    )
    for term in terms:
        if not term:
            continue
        start = 0
        while True:
            index = text.find(term, start)
            if index < 0:
                break
            context = text[max(0, index - 10) : index + len(term)]
            if not any(marker in context for marker in negation_markers):
                return True
            start = index + len(term)
    return False


def detect_payment_evidence_level(raw_text: str) -> int:
    levels = [
        (5, ("真实支付", "已付款", "付款", "签合同", "合同", "已复购", "复购数据", "已续费", "续费数据", "项目收入")),
        (4, ("定金", "预付款", "预算确认", "确认预算", "已有预算", "有预算", "预算已批", "预算批准", "采购流程", "报价已接受", "买单", "已买单", "愿意买单")),
        (3, ("留资", "预约", "进群", "报名", "排队")),
        (2, ("试用", "试点", "愿意体验", "体验")),
        (1, ("感兴趣", "方向不错", "口头兴趣", "想了解")),
    ]
    for level, terms in levels:
        if contains_positive_any(raw_text, terms):
            return level
    return 0


def detect_evidence_level(raw_text: str, payment_level: int) -> str:
    if payment_level >= 5 or contains_any(raw_text, ("使用数据", "复购数据", "交付数据", "已上线数据")):
        return "S"
    if payment_level >= 4 or contains_any(raw_text, ("客户访谈", "强烈需求", "预算意向", "付费意向", "试点意向")):
        return "A"
    if contains_any(raw_text, ("竞品", "行业趋势", "相似产品", "市场需求", "市场报告")):
        return "B"
    if contains_any(raw_text, ("我觉得", "团队判断", "可能", "方向", "用户说")):
        return "C"
    return "D"


def detect_value_gate_completeness(raw_text: str, fields: dict[str, str]) -> dict:
    target_users = split_items(fields.get("target_users_raw", ""))
    checks = {
        "target_user": bool(target_users) or contains_any(raw_text, ("目标用户", "用户", "客户", "商家", "企业", "团队", "角色")),
        "value_object": contains_any(raw_text, ("谁付钱", "付费者", "决策者", "使用者", "受益", "验收", "客户", "内部团队")),
        "business_result": contains_any(raw_text, ("收入", "利润", "转化", "复购", "降本", "增效", "效率", "错误率", "交付周期", "风险降低")),
        "revenue_or_benefit": contains_any(raw_text, ("付费", "预算", "合同", "订阅", "会员", "佣金", "抽成", "降本", "节省", "成本")),
        "usage_scenario": bool(infer_scenarios(raw_text, fields.get("title", ""))) and contains_any(raw_text, ("场景", "流程", "使用", "交付", "运营", "客户", "用户")),
        "risk_boundary": contains_any(raw_text, ("风险", "合规", "隐私", "权限", "审核", "安全", "红线", "边界", "风控")),
        "acquisition_path": contains_any(raw_text, ("获客", "渠道", "线索", "转化", "销售", "推广", "投放", "冷启动", "私域")),
        "cost_structure": contains_any(raw_text, ("成本", "毛利", "利润", "交付成本", "维护成本", "人工成本", "售后", "获客成本")),
    }
    missing = [VALUE_GATE_INPUT_CHECKS[key] for key, present in checks.items() if not present]
    present = [VALUE_GATE_INPUT_CHECKS[key] for key, present in checks.items() if present]
    return {
        "checks": checks,
        "present_items": present,
        "missing_items": missing,
        "missing_count": len(missing),
        "is_complete_for_prd": len(missing) <= 1,
    }


def is_value_gate_non_fact(text: str) -> bool:
    stripped = text.strip(" -")
    return (
        stripped.startswith(("如果", "失败标准", "反证", "停止条件"))
        or "是否能" in stripped
        or "需要继续验证" in stripped
    )


def detect_red_line_risks(raw_text: str) -> list[str]:
    risks = []
    redline_terms = {
        "金融收益或投资建议风险": ("承诺收益", "稳赚", "保本", "荐股", "股票推荐", "投资建议", "高收益"),
        "医疗诊断风险": ("医疗诊断", "疾病诊断", "病情诊断", "诊断疾病", "治疗方案", "用药建议", "替代医生", "病情判断"),
        "法律责任风险": ("法律意见", "替代律师", "胜诉承诺", "规避法律"),
        "隐私与数据来源风险": ("未授权数据", "爬取个人信息", "身份证", "隐私数据", "敏感个人信息"),
        "支付资金安全风险": ("资金池", "代收代付", "支付清算", "资金托管"),
        "内容安全或平台规则风险": ("诱导", "违规内容", "绕过平台规则", "灰产", "违法"),
    }
    for title, terms in redline_terms.items():
        if contains_positive_any(raw_text, terms):
            risks.append(title)
    return unique_list(risks)


def build_industry_redline_rule_pack(raw_text: str, redlines: list[str]) -> dict:
    domains = []
    domain_terms = {
        "金融": ("金融", "投资", "荐股", "收益", "股票", "基金", "理财", "交易"),
        "医疗": ("医疗", "诊断", "治疗", "医生", "用药", "病情"),
        "法律": ("法律", "律师", "诉讼", "合同纠纷", "胜诉"),
        "教育": ("教育", "考试", "升学", "未成年人", "培训"),
        "数据隐私": ("隐私", "个人信息", "身份证", "手机号", "未授权数据", "用户数据"),
        "内容安全": ("内容安全", "诱导", "违法内容", "虚假内容", "黑灰产"),
        "支付资金": ("支付", "资金", "清算", "代收代付", "资金池"),
        "平台规则": ("平台规则", "刷量", "绕过平台", "排名", "推荐结果", "封禁"),
    }
    for domain, terms in domain_terms.items():
        if contains_positive_any(raw_text, terms) or any(domain in risk for risk in redlines):
            domains.append(domain)
    if is_geo_context(raw_text):
        domains.append("平台规则")
    if not domains:
        domains = ["通用平台与商业合规"]

    rule_map = {
        "金融": ["不得承诺收益", "不得违规荐股", "不得诱导高风险投资", "必须保留风险揭示和人工合规确认"],
        "医疗": ["不得替代医生诊断", "不得输出确定性治疗建议", "必须保留专业人工确认"],
        "法律": ["不得替代律师意见", "不得承诺法律结果", "必须明确责任边界"],
        "教育": ["不得承诺升学或考试结果", "涉及未成年人时必须加强合规和隐私边界"],
        "数据隐私": ["必须确认数据来源、授权、存储、使用和删除边界", "不得处理未授权敏感个人信息"],
        "内容安全": ["不得生成违法违规内容", "不得诱导误导用户", "必须保留内容审核边界"],
        "支付资金": ["必须明确资金安全、交易链路和责任边界", "不得形成未授权资金池或清算行为"],
        "平台规则": ["不得承诺 AI 推荐、排名或确定性曝光", "不得刷量、伪造内容、绕过平台规则或做黑灰产优化"],
        "通用平台与商业合规": ["不得把未验证收益写成确定承诺", "不得忽略隐私、品牌、平台和交付责任边界"],
    }
    triggered_rules = unique_list(rule for domain in domains for rule in rule_map.get(domain, []))
    unresolved = []
    if redlines:
        unresolved.extend(redlines)
    if "平台规则" in domains:
        unresolved.append("需确认各 AI 平台可接受的监测、内容优化和复测边界")
    if "数据隐私" in domains:
        unresolved.append("需确认客户数据、品牌材料和监测样本的授权边界")

    return {
        "status": "blocked" if redlines else ("needs_human_confirmation" if domains != ["通用平台与商业合规"] else "controlled_with_watch"),
        "triggered_domains": unique_list(domains),
        "triggered_rules": triggered_rules,
        "unresolved_questions": unique_list(unresolved),
        "full_prd_rule": "红线未解除或行业边界未确认前，不允许进入完整 PRD。",
        "allowed_when_uncertain": "可进入调研、风险复核、低成本 MVP 或服务化验证，但必须保留边界和人工确认。",
    }


def build_contextual_redline_filter(raw_text: str, redlines: list[str], industry_pack: dict) -> dict:
    """Keep redline checks focused on the actual business context."""
    if is_geo_context(raw_text):
        active_domains = ["平台规则", "数据隐私", "内容安全", "品牌风险"]
        conditional_domains = []
        if contains_positive_any(raw_text, ("法律", "法务", "律师")):
            conditional_domains.append("法律服务行业")
        if contains_positive_any(raw_text, ("教育", "培训", "未成年人")):
            conditional_domains.append("教育行业")
        if contains_positive_any(raw_text, ("医疗", "医美", "医生", "诊断")):
            conditional_domains.append("医疗 / 医美行业")
        if contains_positive_any(raw_text, ("财税", "金融", "理财", "投资")):
            conditional_domains.append("财税 / 金融相邻行业")
        excluded_domains = [
            "支付资金"
        ]
        active_rules = [
            "不得承诺 AI 推荐、排名或确定性曝光。",
            "不得刷量、伪造内容、虚假评价、虚假报道、伪造背书或黑帽 GEO。",
            "必须确认客户授权材料、监测样本、截图和看板数据的使用边界。",
            "必须避免误导性品牌承诺和平台规则违规。",
        ]
        return {
            "status": "contextual_review_required" if conditional_domains or redlines else "contextual_watch",
            "active_domains": active_domains,
            "conditional_domains": unique_list(conditional_domains),
            "excluded_domains": excluded_domains,
            "active_rules": active_rules,
            "why_filtered": "GEO 当前核心风险是平台规则、数据授权、内容安全和品牌承诺；医疗、法律、教育、金融等只在选定对应客户行业时进入专项红线复核。",
            "blocks_current_path": bool(redlines),
            "full_prd_condition": "完整 PRD 前必须确认首批行业边界和平台可接受操作范围。",
            "human_confirmation_required": bool(redlines or conditional_domains),
        }
    return {
        "status": industry_pack.get("status", "controlled_with_watch"),
        "active_domains": industry_pack.get("triggered_domains", []),
        "conditional_domains": [],
        "excluded_domains": [],
        "active_rules": industry_pack.get("triggered_rules", []),
        "why_filtered": "非 GEO 场景沿用行业红线规则包。",
        "blocks_current_path": bool(redlines),
        "full_prd_condition": industry_pack.get("full_prd_rule", "高风险未解除前不进入完整 PRD。"),
        "human_confirmation_required": industry_pack.get("status") in {"blocked", "needs_human_confirmation"},
    }


def detect_intent(raw_text: str, request_type: str) -> dict:
    if is_geo_context(raw_text) or contains_any(raw_text, ("SaaS", "订阅", "不同行业", "品牌方", "对外", "买单", "产品化平台")):
        primary = "对外商业产品 / B2B SaaS"
    elif contains_any(raw_text, ("客户项目", "客户需求", "定制", "交付", "预算", "合同")):
        primary = "客户项目需求"
    elif contains_any(raw_text, ("内部提效", "内部工具", "内部流程", "内部团队", "内部交付", "内部运营", "流程优化")):
        primary = "内部提效需求"
    elif contains_any(raw_text, ("帮我写 PRD", "生成 PRD", "PRD")):
        primary = "PRD 生成请求"
    elif request_type == "new_feature":
        primary = "功能需求"
    elif contains_any(raw_text, ("商业模式", "订阅", "会员", "抽成", "分润")):
        primary = "商业模式判断"
    elif contains_any(raw_text, ("想法", "机会", "方向", "产品")):
        primary = "新产品想法"
    else:
        primary = "模糊想法"
    secondary = []
    if contains_any(raw_text, ("产品化", "标准化", "复用")):
        secondary.append("项目转产品判断")
    if contains_any(raw_text, ("技术", "架构", "模型", "AI", "接口")):
        secondary.append("技术可行性判断")
    if contains_any(raw_text, ("订阅", "会员", "SaaS", "服务收入", "工具授权", "报告")):
        secondary.append("商业模式判断")
    return {
        "primary_intent": primary,
        "secondary_intents": secondary,
        "current_stage": "idea_intake",
    }


def infer_value_type(raw_text: str) -> list[str]:
    value_types = []
    if contains_any(raw_text, ("付费", "订阅", "会员", "抽成", "分润", "合同", "客户项目", "项目收入")):
        value_types.append("对外商业价值")
    if contains_any(raw_text, ("降本", "人工成本", "运营成本", "维护成本")):
        value_types.append("内部降本价值")
    if contains_any(raw_text, ("增效", "效率", "生产周期", "交付效率", "客户成功效率")):
        value_types.append("内部增效价值")
    if contains_any(raw_text, ("风险", "合规", "错误率", "流失率")):
        value_types.append("风险降低价值")
    if contains_any(raw_text, ("数据沉淀", "案例沉淀", "能力沉淀")):
        value_types.append("数据 / 能力沉淀价值")
    return value_types or ["价值类型待验证"]


def infer_value_type_detail(raw_text: str, value_types: list[str]) -> dict:
    if "对外商业价值" in value_types:
        primary = "对外商业价值"
    elif any("内部" in item for item in value_types):
        primary = "内部经营价值"
    elif "风险降低价值" in value_types:
        primary = "风险降低价值"
    else:
        primary = "价值类型待验证"

    secondary = [item for item in value_types if item != primary]
    if is_geo_context(raw_text):
        secondary = unique_list(
            secondary
            + [
                "服务收入价值",
                "项目收入价值",
                "产品化收入候选",
                "数据 / 能力沉淀价值",
            ]
        )
        reasoning = "GEO 当前首要验证对外服务收入和项目收入；内部 Agent / 工作台只作为交付降本工具，不能当作客户核心产品价值。"
        must_not_treat_as = [
            "不能把内部 Agent 降本工具当作客户核心产品价值。",
            "不能把一次服务买单直接写成完整 SaaS 产品化成立。",
            "不能把竞品存在直接写成本项目利润或 ROI 成立。",
        ]
    elif primary == "内部经营价值":
        reasoning = "当前主要判断内部降本、增效或控风险价值；除非出现外部付费者和商业场景，否则不能当作对外产品价值。"
        must_not_treat_as = ["不能把内部效率价值直接写成外部商业价值。"]
    else:
        reasoning = "当前价值类型需要后续证据继续确认。"
        must_not_treat_as = ["不能把待验证价值类型写成已确认价值。"]

    return {
        "primary_value_type": primary,
        "secondary_value_types": unique_list(secondary),
        "value_type_reasoning": reasoning,
        "must_not_treat_as": must_not_treat_as,
    }


def infer_business_result_definition(raw_text: str, value_types: list[str]) -> dict:
    if is_geo_context(raw_text):
        return {
            "primary_business_result": "服务收入 / 项目收入 / 复购或复测收入",
            "secondary_business_results": [
                "AI 提及率提升",
                "品牌推荐率提升",
                "竞品覆盖差距缩小",
                "引用来源质量改善",
                "后续优化项目转化",
                "月度代运营复购 / 续费",
            ],
            "result_metrics": [
                "免费检测提交数",
                "有效线索率",
                "加顾问率",
                "体检报告成交率",
                "后续优化项目转化率",
                "月度代运营复购 / 续费率",
                "单客户交付工时",
                "真实利润",
            ],
            "result_not_proven_yet": [
                "高 ROI 已成立",
                "完整 SaaS 收入成立",
                "规模化获客成立",
                "复购周期稳定",
                "边际交付成本已下降",
            ],
            "definition_rule": "商业结果必须能被收入、利润、复购、交付成本和可归因指标验证；不能只写曝光提升或市场机会。",
        }
    if "对外商业价值" in value_types:
        return {
            "primary_business_result": "外部收入 / 真实利润",
            "secondary_business_results": ["客户增长", "线索增长", "复购提升"],
            "result_metrics": ["收入", "真实利润", "获客成本", "复购率", "交付成本"],
            "result_not_proven_yet": ["高 ROI 已成立", "规模化产品化成立"],
            "definition_rule": "收入必须扣除获客、交付、维护、售后、合规和风险成本后再判断价值。",
        }
    if any("内部" in item for item in value_types):
        return {
            "primary_business_result": "内部降本 / 增效 / 降错",
            "secondary_business_results": ["交付周期缩短", "错误率下降", "运营成本降低"],
            "result_metrics": ["单次节省时间", "发生频率", "人工成本", "建设维护成本", "回本周期"],
            "result_not_proven_yet": ["外部商业价值成立", "对外产品化成立"],
            "definition_rule": "内部价值必须能量化节省时间、频率、人工成本、建设成本和回本周期。",
        }
    return {
        "primary_business_result": "待验证",
        "secondary_business_results": [],
        "result_metrics": ["待验证"],
        "result_not_proven_yet": ["价值明确"],
        "definition_rule": "商业结果不清时不能进入完整 PRD。",
    }


def infer_value_gate_facts(raw_text: str, fields: dict[str, str], bullets: list[str], title: str) -> list[str]:
    facts = [item for item in infer_evidence(fields, bullets) if not is_value_gate_non_fact(item)]
    fact_terms = (
        "已做 MVP",
        "做过 MVP",
        "完成 MVP",
        "MVP 实验",
        "MVP 试验",
        "已买单",
        "买单",
        "真实支付",
        "已付款",
        "签合同",
        "预算确认",
        "确认预算",
        "采购流程",
        "已上线",
        "使用数据",
        "复购数据",
        "试点数据",
        "交付数据",
    )
    for sentence in re.split(r"[。；;\n]", raw_text):
        stripped = sentence.strip(" -")
        if is_value_gate_non_fact(stripped):
            continue
        if stripped and contains_positive_any(stripped, fact_terms):
            facts.append(stripped)
    if not facts:
        facts.append(f"用户提出的原始主题为：{title}")
    return unique_list(facts)


def infer_value_object_detail(raw_text: str, target_users: list[str]) -> dict:
    core_users = filter_core_users(target_users)
    commercial_roles = infer_mentions(
        raw_text,
        (
            "企业预算方",
            "企业品牌方",
            "品牌方",
            "老板",
            "采购决策者",
            "营销负责人",
            "内容负责人",
            "增长负责人",
            "SEO/GEO 服务商",
            "SEO 服务商",
            "GEO 服务商",
            "同行服务商",
            "客户验收方",
            "业务负责人",
        ),
    )
    return {
        "core_user": core_users,
        "payer": infer_mentions(raw_text, ("企业预算方", "品牌方", "老板", "客户预算方", "同行服务商", "采购方"), ["待验证"]),
        "decision_maker": infer_mentions(raw_text, ("老板", "营销负责人", "增长负责人", "采购决策者", "品牌负责人", "业务负责人"), ["待验证"]),
        "user": core_users,
        "beneficiary": infer_mentions(raw_text, ("品牌方", "营销团队", "增长团队", "内容团队", "业务方", "客户"), core_users),
        "cost_bearer": infer_mentions(raw_text, ("企业预算方", "项目方", "内部团队", "客户", "服务商"), ["待验证"]),
        "acceptance_owner": infer_mentions(raw_text, ("品牌负责人", "客户验收方", "业务负责人", "营销负责人", "老板"), ["待验证"]),
        "renewal_influencer": infer_mentions(raw_text, ("使用者", "营销团队", "内容团队", "增长团队", "客户成功", "服务商"), ["待验证"]),
        "possible_opponents": infer_mentions(raw_text, ("法务", "内容团队", "预算负责人", "现有服务商", "合规", "平台规则"), ["待验证"]),
        "role_clarity": "明确" if len(commercial_roles) >= 3 or len(target_users) >= 3 else "待补充",
    }


def infer_measurability_judgment(raw_text: str) -> dict:
    if is_geo_context(raw_text):
        metrics = [
            "AI 提及率",
            "品牌推荐率",
            "竞品覆盖差距",
            "关键词回答覆盖率",
            "引用来源质量",
            "多模型一致性",
            "复测变化",
            "线索转化归因",
        ]
    else:
        metrics = ["收入", "真实利润", "获客成本", "交付成本", "效率提升", "错误率", "复购率"]
    quantified = contains_any(raw_text, ("%", "多少", "提升", "降低", "减少", "缩短", "转化", "收入", "利润", "成本", "次数", "周期"))
    return {
        "is_measurable": quantified or is_geo_context(raw_text),
        "metrics": unique_list(metrics),
        "missing_metrics": [] if quantified else ["基线值", "目标值", "验证周期", "归因口径"],
        "judgment": "具备可衡量方向，仍需补齐基线值和验证周期。" if quantified or is_geo_context(raw_text) else "目前只有价值描述，缺少可量化指标。",
    }


def infer_attribution_judgment(raw_text: str) -> dict:
    factors = []
    if is_geo_context(raw_text):
        factors.extend(["内容资产质量", "AI 平台回答机制", "外部可信引用", "品牌已有声量", "竞品内容布局"])
    if contains_any(raw_text, ("销售", "渠道", "投放", "转介绍")):
        factors.append("销售和渠道能力")
    return {
        "attribution_level": "medium" if factors else "unknown",
        "core_question": "商业结果是否主要由产品 / 服务直接带来，而不是由渠道、销售或外部平台变化带来。",
        "influencing_factors": unique_list(factors or ["待验证"]),
        "baseline_metrics": ["当前指标基线", "优化前样本", "转化前后对比"],
        "product_or_service_actions": ["交付动作", "内容优化动作", "复测动作"] if is_geo_context(raw_text) else ["产品使用动作", "交付动作"],
        "external_interference_factors": unique_list(factors or ["市场变化", "销售能力", "渠道变化"]),
        "attribution_risk": "中" if factors else "高",
        "review_materials": ["基线数据", "动作记录", "结果指标", "外部干扰记录"],
        "tracking_requirement": "需要记录产品动作、交付动作、结果指标和外部干扰因素。",
    }


def infer_value_quality_judgment(raw_text: str, decision: str) -> dict:
    is_project = contains_any(raw_text, ("定制", "客户项目", "项目交付", "单个客户"))
    is_service_heavy = contains_any(raw_text, ("人工", "服务", "报告", "审核", "交付", "专家"))
    is_standardizable = contains_any(raw_text, ("SaaS", "平台", "订阅", "词库", "模板", "监测", "标准化", "工具授权"))
    return {
        "continuity": "持续价值" if contains_any(raw_text, ("订阅", "复购", "续费", "持续监测", "周期性")) else "待验证",
        "gross_margin_risk": "中" if is_service_heavy else "待验证",
        "delivery_weight": "偏重交付" if is_service_heavy else "待验证",
        "standardization": "具备标准化线索" if is_standardizable else "待验证",
        "repurchase_potential": "具备复购 / 续费线索" if contains_any(raw_text, ("复购", "续费", "订阅", "持续监测")) else "待验证",
        "replicability": "项目价值优先，产品化需继续观察" if is_project and decision == "C_CLIENT_PROJECT_VALIDATION" else "可复制性待用多客户数据验证",
        "moat": "行业词库、提示词样本库、历史监测数据和优化案例可能形成壁垒" if is_geo_context(raw_text) else "待验证",
    }


def infer_true_profit_judgment(raw_text: str, payment_level: int) -> dict:
    cost_items = {
        "获客成本": contains_any(raw_text, ("获客成本", "销售", "渠道", "投放", "线索")),
        "交付成本": contains_any(raw_text, ("交付成本", "交付", "报告", "服务")),
        "人工成本": contains_any(raw_text, ("人工", "专家", "审核", "运营")),
        "维护成本": contains_any(raw_text, ("维护", "持续监测", "周期性", "复测")),
        "沟通成本": contains_any(raw_text, ("沟通", "客户成功", "服务商")),
        "售后成本": contains_any(raw_text, ("售后", "客户成功", "续费")),
        "合规成本": contains_any(raw_text, ("合规", "法务", "隐私", "平台规则")),
        "风险成本": contains_any(raw_text, ("风险", "波动", "不可控")),
    }
    covered = [key for key, present in cost_items.items() if present]
    return {
        "status": "初步成立，仍需核算" if payment_level >= 4 else "未验证",
        "revenue_signal": f"付费证据第 {payment_level} 层" if payment_level else "无明确付费证据",
        "price_assumption": "待确认客单价 / 报告价格 / 服务价格",
        "acquisition_cost_assumption": "待核算单个有效线索和成交客户获客成本",
        "delivery_hours_assumption": "待记录单客户交付工时",
        "human_review_cost_assumption": "待核算人工检测、复核和报告修订成本",
        "maintenance_after_sales_cost_assumption": "待核算看板维护、复测、客户成功和售后成本",
        "cost_items_checked": covered,
        "missing_cost_items": [key for key, present in cost_items.items() if not present],
        "minimum_profit_condition": "客单价必须覆盖获客、交付、人工复核、维护、售后、合规和风险成本，并保留可接受毛利。",
        "profit_risk": "服务交付和人工审核成本可能压缩毛利" if contains_any(raw_text, ("人工", "服务", "报告", "审核")) else "待验证",
        "next_calculation": "补齐客单价、获客成本、单客户交付工时、复购周期和维护成本。",
    }


def infer_resource_fit_judgment(raw_text: str) -> dict:
    advantages = infer_mentions(raw_text, ("已有企业客户", "现有客户", "SEO", "内容营销", "AI 转型", "同行服务商", "案例", "行业词库", "技术能力"))
    missing = []
    if not contains_any(raw_text, ("已有企业客户", "现有客户", "客户资源")):
        missing.append("客户资源")
    if not contains_any(raw_text, ("获客渠道", "SEO", "内容营销", "销售线索", "转介绍", "私域")):
        missing.append("获客渠道")
    if not contains_any(raw_text, ("行业词库", "行业认知", "SEO", "GEO")):
        missing.append("行业认知")
    if not contains_any(raw_text, ("技术能力", "AI", "模型", "平台", "脚本")):
        missing.append("技术能力")
    if not contains_any(raw_text, ("交付能力", "服务", "报告", "人工审核", "交付")):
        missing.append("交付能力")
    if not contains_any(raw_text, ("案例", "MVP", "已买单", "买单")):
        missing.append("案例背书")
    if not contains_any(raw_text, ("成本优势", "低成本", "脚本", "自动化")):
        missing.append("成本优势")
    if not contains_any(raw_text, ("合规", "法务", "平台规则", "不承诺", "不刷量")):
        missing.append("合规能力")
    if not contains_any(raw_text, ("团队资源", "团队", "人手", "交付团队", "研发资源", "运营资源")):
        missing.append("团队资源")
    return {
        "status": "有初步资源匹配" if advantages else "待验证",
        "available_assets": advantages or ["待验证"],
        "missing_assets": missing,
        "why_us": "已有客户 / SEO / 内容营销 / AI 转型资源可作为切入口。" if advantages else "需要说明为什么由我们来做，以及进入优势是什么。",
    }


def infer_acquisition_judgment(raw_text: str) -> dict:
    channels = infer_mentions(raw_text, ("现有客户", "企业客户", "SEO", "内容营销", "AI 转型", "同行服务商", "私域", "销售线索", "转介绍"))
    return {
        "first_users": channels or ["待验证"],
        "reach_method": "从已有客户、服务商和内容营销需求切入。" if channels else "待验证",
        "trust_basis": infer_mentions(raw_text, ("案例", "MVP", "买单", "服务商", "现有客户"), ["待验证"]),
        "cac_ltv_risk": "需要验证客单价能否覆盖获客、诊断、交付和持续监测成本。",
        "repeat_or_referral": "持续监测、复测和服务商工具授权可能带来复购。" if is_geo_context(raw_text) else "待验证",
    }


def build_value_quality_scorecard(value_quality: dict, project_to_product: dict) -> dict:
    dimensions = [
        ("continuity", "一次性 / 持续价值", value_quality.get("continuity"), "持续价值或周期性复购证据"),
        ("gross_margin", "高毛利 / 低毛利风险", value_quality.get("gross_margin_risk"), "扣除交付、人工、工具、维护后的毛利证据"),
        ("delivery_weight", "轻交付 / 重交付", value_quality.get("delivery_weight"), "单客户交付工时和返工记录"),
        ("standardization", "标准化 / 强定制", value_quality.get("standardization"), "标准化流程、配置边界和模板化交付"),
        ("repurchase", "可复购 / 一次性", value_quality.get("repurchase_potential"), "复购、续费、复测或转介绍记录"),
        ("replicability", "可复制 / 单客户", value_quality.get("replicability"), "第二个相似客户和多行业复用证据"),
        ("capability_asset", "能力沉淀", project_to_product.get("standardizable_parts"), "可沉淀的数据、流程、报告、词库或工具能力"),
        ("moat", "壁垒 / 易替代", value_quality.get("moat"), "数据积累、行业 know-how、交付质量或渠道优势"),
    ]
    rows = []
    blocking_items = []
    warning_items = []
    for key, label, value, required_evidence in dimensions:
        value_text = "、".join(value) if isinstance(value, list) else str(value or "待验证")
        if value_text in {"待验证", "[]"} or "待验证" in value_text:
            status = "Warning"
            warning_items.append(label)
        elif any(term in value_text for term in ("偏重", "风险", "暂不", "需继续观察", "不足")):
            status = "Warning"
            warning_items.append(label)
        else:
            status = "Pass"
        if key in {"gross_margin", "delivery_weight", "repurchase", "replicability"} and status != "Pass":
            blocking_items.append(label)
        rows.append(
            {
                "key": key,
                "label": label,
                "status": status,
                "current_judgment": value_text,
                "required_evidence": required_evidence,
                "decision_effect": "阻断完整 PRD / 产品化放大" if label in blocking_items else "允许继续验证，但不能当作产品化已成立",
            }
        )
    return {
        "overall_status": "needs_validation" if blocking_items else ("watch" if warning_items else "healthy"),
        "rows": rows,
        "blocking_items_for_full_prd": blocking_items,
        "warning_items": warning_items,
        "full_prd_rule": "价值质量关键项未被证据支持时，只能进入 MVP / 项目验证，不能直接进入完整 PRD 或产品化放大。",
    }


def build_resource_advantage_matrix(resource_fit: dict) -> dict:
    required_assets = [
        ("customer_resource", "客户资源"),
        ("acquisition_channel", "获客渠道"),
        ("industry_knowledge", "行业认知"),
        ("technical_capability", "技术能力"),
        ("delivery_capability", "交付能力"),
        ("case_proof", "案例背书"),
        ("cost_advantage", "成本优势"),
        ("compliance_capability", "合规能力"),
        ("team_resource", "团队资源"),
    ]
    available = set(resource_fit.get("available_assets", []))
    missing = set(resource_fit.get("missing_assets", []))
    claimed_advantages = [item for item in resource_fit.get("available_assets", []) if item and item != "待验证"]
    verified_advantages: list[str] = []
    unverified_advantages = list(claimed_advantages)
    rows = []
    for key, label in required_assets:
        if label in missing:
            status = "missing"
            evidence_status = "缺证据"
        elif available and "待验证" not in available:
            status = "candidate"
            evidence_status = "输入中有线索，需复核"
        else:
            status = "unknown"
            evidence_status = "待确认"
        rows.append(
            {
                "key": key,
                "label": label,
                "status": status,
                "evidence_status": evidence_status,
                "required_evidence": f"{label}对应的客户记录、案例、流程、能力或成本证明",
                "decision_effect": "missing 时不能声称我们有稳定进入优势",
            }
        )
    return {
        "overall_status": "needs_evidence" if any(row["status"] in {"missing", "unknown"} for row in rows) else "supported",
        "why_us": resource_fit.get("why_us", ""),
        "claimed_resource_advantages": claimed_advantages,
        "verified_resource_advantages": verified_advantages,
        "unverified_resource_advantages": unverified_advantages,
        "why_us_not_proven": unique_list(
            [
                "客户资源尚未形成可复核清单" if "客户资源" in missing else "",
                "获客成本和转化路径尚未被真实数据证明" if "获客渠道" in missing else "",
                "交付能力仍需用交付周期、工时、返工和验收记录证明" if "交付能力" in missing else "",
                "成本优势仍需用人工、工具、模型和维护成本证明" if "成本优势" in missing else "",
                "合规能力仍需平台规则、授权边界和风险话术证明" if "合规能力" in missing else "",
            ]
        ),
        "rows": rows,
        "missing_assets": resource_fit.get("missing_assets", []),
        "decision_rule": "市场有机会不等于我们能拿到价值；资源优势未被证据支持时，只能验证，不能放大投入。",
    }


def build_acquisition_decision_table(acquisition: dict, roi_input_table: dict) -> dict:
    roi_rows = {row.get("key"): row for row in roi_input_table.get("input_rows", [])}
    rows = [
        {
            "key": "first_users",
            "label": "第一批用户在哪里",
            "current_judgment": "、".join(acquisition.get("first_users", [])),
            "evidence_required": "首批客户名单、行业、来源或线索记录",
            "status": "missing" if acquisition.get("first_users") == ["待验证"] else "candidate",
        },
        {
            "key": "reach_method",
            "label": "如何触达",
            "current_judgment": acquisition.get("reach_method", "待验证"),
            "evidence_required": "渠道、转介绍、私域、内容、销售或服务商触达记录",
            "status": "missing" if acquisition.get("reach_method") == "待验证" else "candidate",
        },
        {
            "key": "trust_basis",
            "label": "为什么信任我们",
            "current_judgment": "、".join(acquisition.get("trust_basis", [])),
            "evidence_required": "案例、MVP 记录、成交记录、服务商背书或客户反馈",
            "status": "missing" if acquisition.get("trust_basis") == ["待验证"] else "candidate",
        },
        {
            "key": "cac",
            "label": "获客成本是否可控",
            "current_judgment": roi_rows.get("acquisition_cost", {}).get("current_value", "待确认"),
            "evidence_required": roi_rows.get("acquisition_cost", {}).get("evidence_required", "获客成本记录"),
            "status": roi_rows.get("acquisition_cost", {}).get("source_status", "missing"),
        },
        {
            "key": "repurchase_or_ltv",
            "label": "是否有复购 / LTV 信号",
            "current_judgment": acquisition.get("repeat_or_referral", "待验证"),
            "evidence_required": "复购、续费、复测、转介绍或代运营意向记录",
            "status": roi_rows.get("repurchase_signal", {}).get("source_status", "missing"),
        },
    ]
    blocking_items = [row["label"] for row in rows if row["status"] in {"missing", "unknown"}]
    return {
        "overall_status": "needs_validation" if blocking_items else "supported",
        "rows": rows,
        "blocking_items_for_full_prd": blocking_items,
        "cac_ltv_risk": acquisition.get("cac_ltv_risk", ""),
        "decision_rule": "获客路径、信任来源、CAC 和复购信号未被证据支持时，不允许进入完整 PRD 或规模化增长结论。",
    }


def infer_project_to_product_judgment(raw_text: str, decision: str) -> dict:
    return {
        "project_value": "成立" if contains_any(raw_text, ("客户项目", "买单", "合同", "项目收入", "真实支付")) else "待验证",
        "service_value": "成立" if contains_any(raw_text, ("服务", "报告", "人工", "交付", "优化建议")) else "待验证",
        "product_value": "具备候选" if decision == VALUE_GATE_ALLOW_PRD or contains_any(raw_text, ("SaaS", "平台", "订阅", "工具授权")) else "待验证",
        "standardizable_parts": infer_mentions(raw_text, ("监测", "诊断报告", "竞品对比", "行业词库", "提示词样本库", "内容分析", "复测"), ["核心价值闭环"]),
        "customized_parts": infer_mentions(raw_text, ("行业", "客户差异", "人工审核", "优化建议", "服务"), ["待验证"]),
        "productization_risk": "同行买单可能先证明服务价值，不必然证明 SaaS 产品化价值。" if is_geo_context(raw_text) else "待验证",
        "next_evidence": ["第二类客户买单", "标准化交付模板", "边际交付成本下降", "复购或续费信号"],
    }


def infer_low_cost_mvp_judgment(raw_text: str, target_users: list[str], scenarios: list[str]) -> dict:
    if is_geo_context(raw_text):
        core_features = ["品牌 / 产品输入", "关键词样本库", "多模型查询", "竞品曝光对比", "GEO 诊断报告", "优化建议", "复测记录"]
        data_loop = ["问题样本", "AI 回答", "品牌提及", "竞品提及", "引用来源", "优化动作", "复测结果"]
    else:
        core_features = ["核心用户", "核心场景", "核心任务", "核心功能", "核心交付", "核心反馈"]
        data_loop = ["输入", "处理", "输出", "反馈", "结果指标"]
    return {
        "core_user": target_users,
        "core_scenario": scenarios,
        "core_task": "验证核心价值闭环",
        "core_hypotheses": [
            "目标用户存在明确高频或高价值场景",
            "核心交付能让用户感知到结果",
            "用户愿意为结果付费、复购、节省成本或继续投入",
        ],
        "core_features": core_features,
        "core_delivery": "可被用户验收的最小结果物",
        "core_feedback": "用户是否认可结果、是否愿意继续付费或复购",
        "minimum_data_loop": data_loop,
        "validation_method_boundaries": {
            "research": "验证有没有需求，不等于 MVP。",
            "pre_sale": "验证有没有付费信号，不等于产品已经成立。",
            "prototype": "验证用户是否理解，不等于交付成立。",
            "pilot": "验证单次交付是否成立，不等于可规模化。",
            "low_cost_mvp": "保留核心功能和核心价值闭环，用最低成本验证价值是否成立。",
        },
        "can_replace_with_manual_or_tools": ["人工处理", "表格记录", "脚本", "第三方工具", "人工审核", "手动交付报告"],
        "not_mvp": ["完整后台", "复杂权限", "完整商业化系统", "非核心异常流程"],
    }


def infer_counter_evidence(raw_text: str) -> list[str]:
    items = [
        "如果用户只愿意试用但不愿意付费，商业价值不成立。",
        "如果获客成本高于客单价，利润价值不成立。",
        "如果交付严重依赖人工专家，产品化价值不足。",
        "如果节省的人力成本小于系统建设成本，内部价值不成立。",
    ]
    if is_geo_context(raw_text):
        items.extend(
            [
                "如果 AI 平台回答波动过大且无法归因，GEO 效果难以证明。",
                "如果客户只为一次性诊断报告付费，不愿持续订阅，SaaS 路径不成立。",
                "如果优化建议高度依赖人工专家，规模化毛利会受限。",
                "如果曝光提升无法带来线索、咨询或品牌指标变化，商业结果不成立。",
                "如果平台规则变化导致方法失效，需要降级为监测和合规内容优化服务。",
            ]
        )
    if contains_any(raw_text, ("定制", "客户项目", "项目交付")):
        items.append("如果客户只接受强定制，不接受标准化配置，产品化路径不成立。")
    return unique_list(items)


def build_review_loop(decision: str, blocked_reasons: list[str], counter_evidence: list[str]) -> dict:
    return {
        "current_status": "initial_judgment",
        "previous_decision_gate": "",
        "current_decision_gate": decision,
        "validation_round": 1,
        "last_updated_reason": blocked_reasons[0] if blocked_reasons else "价值门禁 V0.3 初判完成。",
        "next_review_trigger": "补齐证据、完成 MVP / 试点 / 客户项目验证后复判。",
        "success_criteria": ["真实买单或预算确认", "核心价值指标改善", "交付成本可控", "风险边界可控"],
        "failure_criteria": counter_evidence[:5],
        "next_review_materials": ["客户证据", "指标基线和结果", "成本核算", "交付复盘", "风险记录"],
    }


def detect_active_negative_value_signals(raw_text: str) -> list[str]:
    terms = ("没人付费", "获客困难", "交付过重", "利润不成立", "无法规模化", "不建议继续投入")
    conditional_markers = ("如果", "反证", "停止条件", "失败标准", "失败条件", "反向验证")
    signals = []
    for sentence in re.split(r"[。；;\n]", raw_text):
        stripped = sentence.strip(" -")
        if not stripped:
            continue
        if any(marker in stripped[:16] for marker in conditional_markers):
            continue
        if any(term in stripped for term in terms):
            signals.append(stripped)
    return unique_list(signals)


def choose_value_gate_decision(raw_text: str, completeness: dict, evidence_level: str, payment_level: int, redlines: list[str]) -> tuple[str, list[str], list[str]]:
    blocked_reasons: list[str] = []
    verify_next: list[str] = []
    active_negative_signals = detect_active_negative_value_signals(raw_text)
    if redlines:
        return "G_BLOCKED_BY_REDLINE", redlines, ["先确认红线是否可控；不可控时禁止推进。"]
    if completeness["missing_count"] >= 2:
        blocked_reasons.append("关键信息缺失 2 项以上，不能判断为价值明确。")
        verify_next.extend(completeness["missing_items"][:5])
        return "E_RESEARCH_REQUIRED", blocked_reasons, verify_next
    if active_negative_signals and payment_level < 4:
        return "F_NOT_RECOMMENDED", ["价值对象、利润、获客或交付条件不成立。"], ["如仍需推进，先补充反证材料。"]
    if contains_any(raw_text, ("客户项目", "定制", "项目交付", "单个客户")) and payment_level >= 4:
        return "C_CLIENT_PROJECT_VALIDATION", ["项目收入可能成立，但产品化复用条件仍需验证。"], ["沉淀第二个相似客户和可标准化范围。"]
    if is_geo_context(raw_text) and evidence_level in {"S", "A"} and payment_level >= 4:
        return (
            "B_LOW_COST_MVP",
            ["证据支持服务化 MVP / 客户项目验证，但不足以支持完整 SaaS PRD。"],
            ["补齐客单价、获客成本、交付工时、复购周期、多客户复用和产品化边际成本证据。"],
        )
    if evidence_level in {"S", "A"} and payment_level >= 4 and completeness["missing_count"] <= 1:
        return "A_ENTER_PRD", [], []
    if active_negative_signals:
        return "F_NOT_RECOMMENDED", ["价值对象、利润、获客或交付条件不成立。"], ["如仍需推进，先补充反证材料。"]
    if contains_any(raw_text, ("内部提效", "内部工具", "内部流程", "内部团队", "内部交付", "内部运营", "降本", "人工成本", "运营成本", "返工成本", "错误率", "交付效率")):
        return "D_INTERNAL_EFFICIENCY", ["内部经营价值可能成立，但不默认对外产品化。"], ["量化节省时间、频率、人工成本和建设维护成本。"]
    if (payment_level in {1, 2, 3} or evidence_level in {"B", "C"}) and contains_any(raw_text, ("核心场景", "核心功能", "MVP", "试点", "低成本")):
        return "B_LOW_COST_MVP", ["付费、获客、利润或复购证据不足，先验证核心价值闭环。"], ["明确 MVP 成功 / 失败标准。"]
    return "E_RESEARCH_REQUIRED", ["证据强度不足，仍需补齐用户、价值、获客或成本信息。"], ["补充客户访谈、付费意向、成本结构和风险边界。"]


def build_input_package_quality_gate(
    *,
    decision: str,
    completeness: dict,
    product_summary: dict,
    value_judgment: dict,
    value_object_detail: dict,
    measurability: dict,
    true_profit: dict,
    acquisition: dict,
    redlines: list[str],
    human_confirmation: dict,
) -> dict:
    checks = [
        ("product_positioning", "产品定位", product_summary.get("product_name")),
        ("target_users", "目标用户", value_object_detail.get("core_user") or value_object_detail.get("user")),
        ("payer", "付费者", value_object_detail.get("payer")),
        ("decision_maker", "决策者", value_object_detail.get("decision_maker")),
        ("business_result", "商业结果", value_judgment.get("business_result")),
        ("metrics", "衡量指标", measurability.get("metrics")),
        ("profit_condition", "真实利润条件", true_profit.get("minimum_profit_condition")),
        ("acquisition_path", "获客路径", acquisition.get("reach_method")),
    ]
    items = []
    missing_items = list(completeness.get("missing_items", []))
    over_generic_items = []
    for key, label, value in checks:
        if not has_specific_value(value):
            status = "missing" if not value else "over_generic"
            if status == "missing":
                missing_items.append(label)
            else:
                over_generic_items.append(label)
        else:
            status = "qualified"
        items.append({"key": key, "label": label, "status": status, "value": value})

    human_items = human_confirmation.get("confirmation_items", []) if human_confirmation.get("required") else []
    if human_items:
        items.append({"key": "human_confirmation", "label": "人工确认", "status": "needs_human_confirmation", "value": human_items})

    content_ready = decision == VALUE_GATE_ALLOW_PRD and not redlines and not missing_items and not over_generic_items
    if redlines:
        overall_status = "failed"
    elif human_items:
        overall_status = "needs_human_confirmation" if content_ready else "failed"
    elif content_ready:
        overall_status = "passed"
    else:
        overall_status = "failed"

    return {
        "overall_status": overall_status,
        "content_ready_for_prd": content_ready,
        "missing_items": unique_list(missing_items),
        "over_generic_items": unique_list(over_generic_items),
        "human_confirmation_items": unique_list(human_items),
        "quality_items": items,
    }


def build_execution_status(
    *,
    decision: str,
    blocked_reasons: list[str],
    redlines: list[str],
    quality_gate: dict,
    human_confirmation: dict,
) -> str:
    if redlines or decision == "G_BLOCKED_BY_REDLINE":
        return "blocked_by_redline"
    if decision != VALUE_GATE_ALLOW_PRD:
        return VALUE_GATE_EXECUTION_STATUS[decision]
    if blocked_reasons or not quality_gate.get("content_ready_for_prd"):
        return "blocked_by_missing_input"
    if human_confirmation.get("required") and not human_confirmation.get("confirmed"):
        return "pending_human_confirmation"
    return "ready_for_prd"


def build_validation_state(decision: str, execution_status: str, blocked_reasons: list[str], counter_evidence: list[str]) -> dict:
    status_by_decision = {
        "A_ENTER_PRD": "approved_for_prd" if execution_status == "ready_for_prd" else "initial_judgment",
        "B_LOW_COST_MVP": "mvp_testing",
        "C_CLIENT_PROJECT_VALIDATION": "client_project_testing",
        "D_INTERNAL_EFFICIENCY": "internal_validation",
        "E_RESEARCH_REQUIRED": "researching",
        "F_NOT_RECOMMENDED": "rejected",
        "G_BLOCKED_BY_REDLINE": "blocked",
    }
    trigger_by_decision = {
        "A_ENTER_PRD": "完成人工确认、补齐成本核算或完成首轮 PRD 修订后复判。",
        "B_LOW_COST_MVP": "完成低成本 MVP 核心价值闭环验证后复判。",
        "C_CLIENT_PROJECT_VALIDATION": "完成客户项目交付并沉淀共性需求后复判。",
        "D_INTERNAL_EFFICIENCY": "完成内部效率和成本节省验证后复判。",
        "E_RESEARCH_REQUIRED": "补齐目标用户、付费、成本、获客或风险材料后复判。",
        "F_NOT_RECOMMENDED": "出现新的强证据或关键反证被解决后复判。",
        "G_BLOCKED_BY_REDLINE": "红线风险被专业确认可控前不得复判为推进。",
    }
    return {
        "current_status": status_by_decision[decision],
        "previous_decision_gate": "",
        "current_decision_gate": decision,
        "execution_status": execution_status,
        "validation_round": 1,
        "last_updated_reason": blocked_reasons[0] if blocked_reasons else "价值门禁 V0.3 初判完成。",
        "next_review_trigger": trigger_by_decision[decision],
        "success_criteria": ["真实买单或预算确认", "核心价值指标改善", "交付成本可控", "风险边界可控"],
        "failure_criteria": counter_evidence[:5],
        "next_review_materials": ["客户证据", "指标基线和结果", "成本核算", "交付复盘", "风险记录"],
    }


def build_rejudgment_package(validation_state: dict, evidence_sufficiency_gate: dict, operating_model: dict, route_package_name: str) -> dict:
    records_by_route = {
        "mvp_input_package": [
            "免费检测提交数",
            "有效线索率",
            "加顾问率",
            "体检报告成交率",
            "报告交付周期",
            "单客户交付工时",
            "看板查看率",
            "复盘预约率",
            "后续优化 / 代运营意向",
            "客户对报告和看板的认可度",
        ],
        "client_project_input_package": [
            "客户付款 / 合同 / 预算记录",
            "交付范围",
            "验收记录",
            "交付工时",
            "返工轮次",
            "可复用需求",
            "不可复用定制项",
        ],
        "internal_efficiency_input_package": [
            "当前流程耗时",
            "使用频率",
            "人工成本",
            "错误率",
            "建设维护成本",
            "回本周期",
        ],
        "research_input_package": [
            "用户访谈记录",
            "付费测试结果",
            "竞品和价格证据",
            "成本结构",
            "风险边界确认",
        ],
    }
    required_records = records_by_route.get(route_package_name, [])
    return {
        "current_status": validation_state.get("current_status"),
        "current_decision_gate": validation_state.get("current_decision_gate"),
        "current_route_package": route_package_name,
        "next_review_trigger": validation_state.get("next_review_trigger"),
        "next_path_execution_record_required": bool(required_records),
        "required_validation_records": required_records,
        "rejudgment_trigger": validation_state.get("next_review_trigger"),
        "rejudgment_input_required": unique_list(required_records + list(evidence_sufficiency_gate.get("next_evidence_to_collect", []))[:5]),
        "minimum_materials_before_rejudgment": unique_list(
            list(validation_state.get("next_review_materials", []))
            + list(evidence_sufficiency_gate.get("next_evidence_to_collect", []))[:5]
        ),
        "success_criteria": validation_state.get("success_criteria", []),
        "failure_criteria": validation_state.get("failure_criteria", []),
        "upgrade_conditions": operating_model.get("upgrade_to_product_conditions", []),
        "stop_or_downgrade_conditions": operating_model.get("stop_or_downgrade_conditions", []),
        "rejudgment_rule": "B/C/D/E 路径不是终点，完成验证材料后必须回流产品价值门禁复判。",
    }


def build_lightweight_profit_model(true_profit: dict, operating_model: dict, payment_level: int) -> dict:
    profit_conditions = operating_model.get("minimum_profit_conditions", {})
    unknowns = unique_list(
        [
            "客单价" if profit_conditions.get("price_floor") == "待确认" else "",
            "获客成本" if profit_conditions.get("acquisition_cost") == "待确认" else "",
            "单客户交付工时" if profit_conditions.get("delivery_hours_per_customer") == "待确认" else "",
            "人工复核成本" if profit_conditions.get("human_review_cost") == "待确认" else "",
            "维护 / 售后成本" if profit_conditions.get("after_sales_maintenance") == "待确认" else "",
        ]
        + true_profit.get("missing_cost_items", [])
    )
    return {
        "model_type": "lightweight_profit_boundary",
        "formula": "真实利润 = 收入 - 获客成本 - 交付成本 - 人工成本 - 维护成本 - 沟通成本 - 售后成本 - 合规成本 - 风险成本",
        "payment_evidence_level": payment_level,
        "known_inputs": true_profit.get("cost_items_checked", []),
        "unknown_inputs": unknowns,
        "cycle_dimensions": ["首单利润", "单次利润", "月度利润", "客户生命周期利润", "复购利润", "维护期利润", "边际交付利润"],
        "minimum_profit_condition": true_profit.get("minimum_profit_condition") or profit_conditions.get("condition") or "待确认",
        "current_status": true_profit.get("status", "待验证"),
        "blocks_scaling_if_missing": ["客单价", "获客成本", "单客户交付工时", "复购周期"],
        "calculation_rule": "没有证据的数值只能标记为待确认，不能编造金额、工时或毛利。",
    }


def build_evidence_archive_policy(value_gate: dict) -> dict:
    return {
        "snapshot_file": "00_value_gate_evidence_snapshot.json",
        "snapshot_type": "metadata_excerpt_snapshot",
        "raw_html_saved": False,
        "what_is_saved": ["证据声明", "来源类型", "来源标题", "URL", "抓取日期", "HTTP 状态", "页面标题", "短摘录", "能证明什么", "不能证明什么"],
        "what_is_not_saved": ["完整网页 HTML", "登录态内容", "未授权数据", "个人敏感信息"],
        "retention_rule": "项目 closeout 前保留；归档时和用户对齐是否进入项目档案、删除候选或长期证据库。",
        "prd_usage_rule": "PRD 只能引用 safe_facts_for_prd；外部公开来源只能证明对象存在或趋势，不能直接证明商业价值成立。",
        "fetch_enabled": value_gate.get("evidence_fetcher", {}).get("enabled", False),
    }


def build_evidence_snapshot(value_gate: dict) -> dict:
    return {
        "project_id": value_gate.get("project_id"),
        "version": value_gate.get("version"),
        "captured_at": date.today().isoformat(),
        "evidence_archive_policy": value_gate.get("evidence_archive_policy", {}),
        "source_quality_gate": value_gate.get("source_quality_gate", {}),
        "evidence_research_agent": value_gate.get("evidence_research_agent", {}),
        "research_execution_queue": value_gate.get("research_execution_queue", {}),
        "material_intake_summary": value_gate.get("material_intake_summary", {}),
        "material_to_evidence_mapping": value_gate.get("material_to_evidence_mapping", []),
        "rejudgment_readiness_gate": value_gate.get("rejudgment_readiness_gate", {}),
        "external_research_results": value_gate.get("external_research_results", {}),
        "source_quality_scorecard": value_gate.get("source_quality_scorecard", {}),
        "competitor_pricing_evidence": value_gate.get("competitor_pricing_evidence", {}),
        "platform_rule_evidence": value_gate.get("platform_rule_evidence", {}),
        "verified_evidence_assessment": value_gate.get("verified_evidence_assessment", {}),
        "s_claimed_to_s_verified_gate": value_gate.get("s_claimed_to_s_verified_gate", {}),
        "real_profit_calculation": value_gate.get("real_profit_calculation", {}),
        "roi_scenario_analysis": value_gate.get("roi_scenario_analysis", {}),
        "investment_decision_gate": value_gate.get("investment_decision_gate", {}),
        "attachment_verification_plan": value_gate.get("attachment_verification_plan", {}),
        "rejudgment_execution_plan": value_gate.get("rejudgment_execution_plan", {}),
        "evidence_sufficiency_gate": value_gate.get("evidence_sufficiency_gate", {}),
        "verified_evidence_gate": value_gate.get("verified_evidence_gate", {}),
        "payment_evidence_verification": value_gate.get("payment_evidence_verification", {}),
        "evidence_verification_intake": value_gate.get("evidence_verification_intake", {}),
        "evidence_grade_gate": value_gate.get("evidence_grade_gate", {}),
        "competitor_benchmark_table": value_gate.get("competitor_benchmark_table", {}),
        "value_quality_scorecard": value_gate.get("value_quality_scorecard", {}),
        "resource_advantage_matrix": value_gate.get("resource_advantage_matrix", {}),
        "acquisition_decision_table": value_gate.get("acquisition_decision_table", {}),
        "value_realization_timeline": value_gate.get("value_realization_timeline", {}),
        "roi_input_table": value_gate.get("roi_input_table", {}),
        "roi_decision_model": value_gate.get("roi_decision_model", {}),
        "output_boundary_gate": value_gate.get("output_boundary_gate", {}),
        "contextual_redline_filter": value_gate.get("contextual_redline_filter", {}),
        "route_package_completeness_gate": value_gate.get("route_package_completeness_gate", {}),
        "evidence_decision_basis": value_gate.get("evidence_decision_basis", []),
        "safe_facts_for_prd": value_gate.get("safe_facts_for_prd", []),
        "blocked_claims": value_gate.get("blocked_claims", []),
    }


def build_source_quality_gate(
    *,
    evidence_basis: list[dict],
    competitor_table: dict,
    evidence_sufficiency_gate: dict,
    verified_gate: dict,
    payment_verification: dict,
    roi_input_table: dict,
) -> dict:
    counts = {
        "user_provided_fact": 0,
        "external_public_source": 0,
        "internal_project_evidence": 0,
        "inference": 0,
        "unsupported_claim": 0,
        "reachable_external": 0,
        "non_success_external": 0,
        "not_checked_external": 0,
        "competitor_rows": len(competitor_table.get("rows", [])),
    }
    rows = []
    for item in evidence_basis:
        source_type = item.get("source_type", "")
        if source_type in counts:
            counts[source_type] += 1
        if source_type == "external_public_source":
            fetch_status = item.get("fetch_status") or "not_checked"
            if fetch_status == "reachable":
                counts["reachable_external"] += 1
            elif fetch_status == "not_checked":
                counts["not_checked_external"] += 1
            else:
                counts["non_success_external"] += 1
        rows.append(
            {
                "claim": item.get("evidence") or item.get("claim") or "",
                "source_type": source_type,
                "source_title": item.get("source_title", ""),
                "source_url": item.get("source_url", ""),
                "fetch_status": item.get("fetch_status") or "not_applicable",
                "strength": item.get("strength", ""),
                "decision_use": item.get("prd_usage") or item.get("decision_impact") or "",
                "cannot_prove": item.get("does_not_prove") or item.get("note") or "",
            }
        )
    for item in competitor_table.get("rows", []):
        rows.append(
            {
                "claim": f"竞品参照：{item.get('name')}",
                "source_type": "competitor_public_source",
                "source_title": item.get("source_title", ""),
                "source_url": item.get("source_url", ""),
                "fetch_status": item.get("fetch_status") or "not_checked",
                "strength": "B：竞品形态证据",
                "decision_use": item.get("prd_usage", ""),
                "cannot_prove": item.get("what_it_does_not_prove", ""),
            }
        )
    blocking_gaps = unique_list(
        list(evidence_sufficiency_gate.get("missing_evidence_types", []))
        + list(verified_gate.get("full_prd_blocking_gap", []))
        + list(roi_input_table.get("missing_critical_inputs", []))
    )
    if payment_verification.get("verified_payment_layer", 0) < 5:
        blocking_gaps.append("付款 / 合同 / 复购材料尚未复核")
    warning_items = []
    if counts["not_checked_external"]:
        warning_items.append("部分外部公开来源尚未检查可达性。")
    if counts["non_success_external"]:
        warning_items.append("部分外部公开来源返回非成功状态，需要替换或人工复核。")
    if counts["external_public_source"] and not counts["user_provided_fact"]:
        warning_items.append("只有外部趋势 / 竞品证据，缺少自身业务证据。")
    overall_status = "usable_for_mvp_not_full_prd"
    if evidence_sufficiency_gate.get("overall_status") == "sufficient_for_full_prd" and not blocking_gaps:
        overall_status = "usable_for_full_prd"
    elif evidence_sufficiency_gate.get("overall_status") in {"research_required", "insufficient_stop"}:
        overall_status = "insufficient_for_route"
    elif evidence_sufficiency_gate.get("overall_status") == "blocked_by_redline":
        overall_status = "blocked_by_redline"
    return {
        "overall_status": overall_status,
        "source_counts": counts,
        "rows": rows,
        "blocking_gaps_for_full_prd": unique_list(blocking_gaps),
        "warning_items": unique_list(warning_items),
        "minimum_source_rule": "完整 PRD 至少需要自身业务证据、经营证据、产品化证据和红线证据同时达标；外部趋势和竞品只能作为机会参照。",
        "prd_usage_rule": "只有 safe_facts_for_prd 和已标注来源的事实可进入 PRD；claimed 用户事实必须标注为用户提供，不能伪装成独立验证。",
    }


def build_evidence_research_agent(
    *,
    evidence_sufficiency_gate: dict,
    source_quality_gate: dict,
    evidence_verification_intake: dict,
    route_package_name: str,
    competitor_table: dict,
) -> dict:
    missing = set(evidence_sufficiency_gate.get("missing_evidence_types", []))
    verification_labels = [item.get("label", "") for item in evidence_verification_intake.get("verification_slots", [])]
    track_defs = [
        (
            "customer_payment_verification",
            "确认真实付款、预算、合同或采购流程",
            ["付款 / 合同证据", "客户 / 行业记录"],
            ["付款截图", "合同 / 报价单", "客户脱敏记录", "预算或采购流程记录"],
            "决定 S_claimed 是否可升级为 S_verified，并决定是否允许完整 PRD。",
        ),
        (
            "roi_operating_inputs",
            "补齐真实利润和 ROI 的关键输入",
            ["报价 / 客单价证据", "交付工时证据", "获客来源证据"],
            ["首期价格", "获客成本", "单客户交付工时", "工具 / 模型成本", "维护和售后成本"],
            "决定是否只能服务化 MVP，还是可以讨论产品化放大。",
        ),
        (
            "competitor_productization",
            "继续跟踪国内外 GEO 竞品的产品形态、定价和交付边界",
            [row.get("name", "") for row in competitor_table.get("rows", [])[:6]],
            ["竞品定价页", "功能页", "案例页", "服务条款", "公开客户案例"],
            "只能证明市场和产品形态存在，不能单独证明本项目利润成立。",
        ),
        (
            "platform_rule_risk",
            "确认 DeepSeek、豆包、Qwen、元宝等平台对自动化采集、内容优化和排名承诺的边界",
            ["平台官方页面 / API 文档"],
            ["平台条款", "robots / API 限制", "数据授权", "内容安全规则"],
            "决定是否存在红线风险，以及 PRD 是否必须限制采集和承诺边界。",
        ),
        (
            "acquisition_channel_validation",
            "验证第一批客户从哪里来以及 CAC 是否可控",
            ["获客来源证据"],
            ["免费检测提交记录", "加顾问记录", "转介绍记录", "内容获客记录", "销售触达记录"],
            "决定获客路径是否足以支撑服务化 MVP 或后续产品化。",
        ),
        (
            "market_shift_monitoring",
            "补充 AI 搜索行为变化、品牌 AI 可见度需求和行业预算变化",
            ["Gartner / Bain / 公开行业资料"],
            ["行业报告", "平台公开数据", "品牌营销预算变化", "AI 搜索使用数据"],
            "只能证明机会窗口，不证明本项目必然盈利。",
        ),
    ]
    tracks = []
    for key, purpose, current_sources, required_source_types, decision_effect in track_defs:
        related_gap = []
        if key == "roi_operating_inputs" and {"经营证据", "真实利润", "获客路径"} & missing:
            related_gap = sorted({"经营证据", "真实利润", "获客路径"} & missing)
        elif key == "competitor_productization" and "产品化证据" in missing:
            related_gap = ["产品化证据"]
        elif key == "customer_payment_verification" and source_quality_gate.get("overall_status") != "usable_for_full_prd":
            related_gap = ["S_claimed 待复核"]
        elif key == "platform_rule_risk" and "红线证据" in missing:
            related_gap = ["红线证据"]
        tracks.append(
            {
                "key": key,
                "purpose": purpose,
                "current_sources": unique_list([item for item in current_sources if item]),
                "required_source_types": required_source_types,
                "related_current_gap": related_gap,
                "decision_effect": decision_effect,
                "next_action": "补齐可溯源材料后回流 value gate 复判。",
            }
        )
    return {
        "mode": "v2_research_plan",
        "current_route_package": route_package_name,
        "mission": "收集可溯源证据，判断当前项目是否值得投入、投入到什么范围，以及是否允许升级完整 PRD / SaaS。",
        "research_tracks": tracks,
        "verification_slots_reused": verification_labels,
        "does_not_do": [
            "不伪造数据",
            "不保存未授权 raw HTML",
            "不自动把用户声明升级为 verified evidence",
            "不自动生成完整 PRD",
            "不自动修改 stable 规则",
        ],
        "output_rule": "每条证据必须带来源、日期、可信度、能证明什么、不能证明什么；无来源内容只能进入假设或待验证。",
    }


def research_task_priority(track_key: str, related_gap: list[str], source_quality_status: str) -> str:
    if track_key in {"customer_payment_verification", "roi_operating_inputs"}:
        return "P0"
    if track_key in {"platform_rule_risk", "acquisition_channel_validation"}:
        return "P1"
    if related_gap:
        return "P1"
    if source_quality_status in {"insufficient_for_route", "blocked_by_redline"}:
        return "P1"
    return "P2"


def build_research_execution_queue(
    *,
    evidence_research_agent: dict,
    source_quality_gate: dict,
    attachment_verification_plan: dict,
    rejudgment_execution_plan: dict,
) -> dict:
    attachment_slots = {item.get("key"): item for item in attachment_verification_plan.get("slots", [])}
    task_to_slots = {
        "customer_payment_verification": ["payment_proof", "customer_record", "mvp_experiment_record"],
        "roi_operating_inputs": ["price_or_quote_record", "delivery_time_record", "acquisition_source_record"],
        "competitor_productization": [],
        "platform_rule_risk": [],
        "acquisition_channel_validation": ["acquisition_source_record"],
        "market_shift_monitoring": [],
    }
    tasks = []
    for index, track in enumerate(evidence_research_agent.get("research_tracks", []), 1):
        key = track.get("key", "")
        related_slots = [attachment_slots[slot_key] for slot_key in task_to_slots.get(key, []) if slot_key in attachment_slots]
        needs_private_material = bool(related_slots)
        priority = research_task_priority(
            key,
            track.get("related_current_gap", []),
            source_quality_gate.get("overall_status", ""),
        )
        tasks.append(
            {
                "task_id": f"research.{index:02d}.{key}",
                "track_key": key,
                "priority": priority,
                "objective": track.get("purpose", ""),
                "source_request": track.get("required_source_types", []),
                "related_attachment_slots": [slot.get("label", "") for slot in related_slots],
                "accepted_evidence": [
                    "公开网页 / 官方文档 / 公开报告，必须有 URL 和抓取日期",
                    "用户提供的付款、合同、客户、实验、交付、复购、报价、工时或获客材料，必须标注为 user_provided_fact 或 internal_project_evidence",
                    "推理判断必须绑定上游事实，不允许单独作为结论证据",
                ],
                "evidence_acceptance_criteria": [
                    "来源可追溯：必须有来源标题、来源类型、URL 或项目内材料路径、记录日期",
                    "证明边界清楚：必须写明能证明什么、不能证明什么",
                    "商业价值相关：必须能影响付款、ROI、获客、交付、复购、产品化或红线判断中的至少一项",
                    "未验证材料不得升级为 S_verified",
                ],
                "output_fields_required": [
                    "source_type",
                    "source_title",
                    "source_url_or_material_path",
                    "captured_at",
                    "proof_excerpt_or_material_summary",
                    "proves",
                    "does_not_prove",
                    "confidence",
                    "decision_effect",
                ],
                "decision_impact": track.get("decision_effect", ""),
                "done_definition": "至少补齐一条可追溯证据，或明确记录未找到可验证来源及其降级影响。",
                "fail_or_downgrade_rule": "找不到材料时不得编造；当前路径保持 MVP / 调研 / 客户项目验证，完整 PRD 和 SaaS 升级继续阻断。",
                "owner_material_required": needs_private_material,
                "writes_repo_files": False,
            }
        )
    p0_count = sum(1 for task in tasks if task.get("priority") == "P0")
    return {
        "mode": "v2_1_executable_research_queue",
        "queue_status": "ready_for_manual_or_agentic_research" if tasks else "empty",
        "current_route_package": evidence_research_agent.get("current_route_package", ""),
        "max_parallel_tasks": 3,
        "p0_task_count": p0_count,
        "tasks": tasks,
        "task_output_contract": {
            "required_fields": [
                "task_id",
                "source_type",
                "source_title",
                "source_url_or_material_path",
                "captured_at",
                "proof_excerpt_or_material_summary",
                "proves",
                "does_not_prove",
                "confidence",
                "decision_effect",
            ],
            "invalid_outputs": [
                "没有来源的市场规模数字",
                "无法追溯的客户付款说法",
                "把竞品存在当作本项目 ROI 成立",
                "把用户声明伪装成外部验证",
                "把未验证材料升级为 S_verified",
            ],
            "handoff_rule": "任务输出只能作为 value gate 复判输入，不得绕过门禁直接进入完整 PRD。",
        },
        "execution_boundary": [
            "不自动联网扩展到未批准的数据源",
            "不自动读取或上传私密附件",
            "不自动写长期记忆",
            "不自动生成完整 PRD",
            "不自动升级 stable 规则",
        ],
        "next_rejudgment_inputs": rejudgment_execution_plan.get("next_value_gate_inputs", []),
    }


def build_attachment_verification_plan(evidence_verification_intake: dict) -> dict:
    slots = []
    for item in evidence_verification_intake.get("verification_slots", []):
        slots.append(
            {
                "key": item.get("key", ""),
                "label": item.get("label", ""),
                "current_status": item.get("current_status", "missing"),
                "materials_to_request": item.get("accepted_materials", []),
                "manual_review_method": "由用户提供附件 / 截图 / 脱敏记录后人工核对真实性、时间、客户对象和可复用性。",
                "upgrade_effect": item.get("verification_effect", ""),
                "cannot_prove": item.get("cannot_prove", ""),
                "storage_rule": "项目 closeout 前作为项目证据候选保存；是否进入长期证据库或删除候选需用户批准。",
            }
        )
    return {
        "current_status": "waiting_for_user_materials" if slots else "not_required",
        "slots": slots,
        "s_verified_rule": evidence_verification_intake.get("upgrade_rule", ""),
        "no_auto_verification": True,
        "owner_action_required": "提供可脱敏材料，或确认本轮只按 claimed evidence 做服务化 MVP。",
    }


def build_rejudgment_execution_plan(
    *,
    route_package_name: str,
    route_package: dict,
    rejudgment_package: dict,
    operating_model: dict,
    evidence_sufficiency_gate: dict,
) -> dict:
    records = unique_list(
        list(route_package.get("execution_record_template", []))
        + list(rejudgment_package.get("required_validation_records", []))
        + list(evidence_sufficiency_gate.get("next_evidence_to_collect", []))[:6]
    )
    return {
        "current_route_package": route_package_name,
        "current_recommendation": operating_model.get("recommended_play", ""),
        "review_window": operating_model.get("validation_window", "待确认"),
        "records_to_collect": records,
        "owner_review_required": True,
        "upgrade_check": {
            "target": "是否允许从当前路径升级为完整 PRD / SaaS / 重研发。",
            "conditions": operating_model.get("upgrade_to_product_conditions", []),
        },
        "stop_or_downgrade_check": {
            "target": "是否停止产品化、降级为服务项目或继续调研。",
            "conditions": operating_model.get("stop_or_downgrade_conditions", []),
        },
        "next_value_gate_inputs": rejudgment_package.get("minimum_materials_before_rejudgment", []),
        "cadence": "服务化 MVP 完成 2-4 周验证或触发停止 / 升级条件时复判；不得自动升级。",
        "result_rule": "复判只更新 value gate 结论和候选路径；是否进入 stable、完整 PRD 或长期规则仍需用户批准。",
    }


def normalize_value_gate_materials(materials_payload: dict | None, project_id: str) -> dict:
    if not isinstance(materials_payload, dict) or not materials_payload:
        return default_value_gate_materials(project_id)
    normalized = {
        "project_id": materials_payload.get("project_id") or project_id,
        "version": materials_payload.get("version") or VALUE_GATE_VERSION,
        "materials": [],
    }
    for index, item in enumerate(materials_payload.get("materials", []), 1):
        if not isinstance(item, dict):
            continue
        slot_key = item.get("slot_key", "")
        slot = VALUE_GATE_MATERIAL_SLOTS.get(slot_key, {})
        review_status = item.get("review_status") or "submitted_pending_review"
        if review_status not in VALUE_GATE_MATERIAL_REVIEW_STATUSES:
            review_status = "needs_more_context"
        normalized["materials"].append(
            {
                "material_id": item.get("material_id") or f"mat-{index:03d}",
                "slot_key": slot_key,
                "material_type": item.get("material_type") or "unknown",
                "title": item.get("title") or slot.get("label", "未命名材料"),
                "occurred_at": item.get("occurred_at") or "待确认",
                "source_path_or_url": item.get("source_path_or_url") or "待确认",
                "redaction_status": item.get("redaction_status") or "redacted",
                "summary": item.get("summary") or "待确认",
                "proves": item.get("proves") or slot.get("supports", []),
                "does_not_prove": item.get("does_not_prove") or slot.get("cannot_prove", []),
                "review_status": review_status,
            }
        )
    known_slots = {item.get("slot_key") for item in normalized["materials"]}
    for slot_key, slot in VALUE_GATE_MATERIAL_SLOTS.items():
        if slot_key in known_slots:
            continue
        normalized["materials"].append(
            {
                "material_id": f"mat-{len(normalized['materials']) + 1:03d}",
                "slot_key": slot_key,
                "material_type": "待填写",
                "title": slot["label"],
                "occurred_at": "待填写",
                "source_path_or_url": "待填写",
                "redaction_status": "redacted",
                "summary": "待填写",
                "proves": slot["supports"],
                "does_not_prove": slot["cannot_prove"],
                "review_status": "missing",
            }
        )
    return normalized


def group_materials_by_slot(materials_payload: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {slot_key: [] for slot_key in VALUE_GATE_MATERIAL_SLOTS}
    for item in materials_payload.get("materials", []):
        grouped.setdefault(item.get("slot_key", ""), []).append(item)
    return grouped


def build_material_intake_summary(materials_payload: dict) -> dict:
    grouped = group_materials_by_slot(materials_payload)
    slot_rows = []
    totals = {status: 0 for status in sorted(VALUE_GATE_MATERIAL_REVIEW_STATUSES)}
    for slot_key, slot in VALUE_GATE_MATERIAL_SLOTS.items():
        materials = grouped.get(slot_key, [])
        statuses = [item.get("review_status", "missing") for item in materials]
        for status in statuses:
            totals[status] = totals.get(status, 0) + 1
        accepted = [item for item in materials if item.get("review_status") == "reviewed_accepted"]
        submitted = [item for item in materials if item.get("review_status") == "submitted_pending_review"]
        needs_context = [item for item in materials if item.get("review_status") == "needs_more_context"]
        if accepted:
            slot_status = "accepted"
        elif submitted:
            slot_status = "submitted_pending_review"
        elif needs_context:
            slot_status = "needs_more_context"
        else:
            slot_status = "missing"
        slot_rows.append(
            {
                "slot_key": slot_key,
                "label": slot["label"],
                "category": slot["category"],
                "slot_status": slot_status,
                "material_count": len([item for item in materials if item.get("review_status") != "missing"]),
                "accepted_count": len(accepted),
                "submitted_count": len(submitted),
                "decision_use": " / ".join(slot["supports"]),
                "cannot_prove": " / ".join(slot["cannot_prove"]),
            }
        )
    critical_slots = ["payment_proof", "customer_record", "mvp_experiment_record", "price_or_quote_record", "delivery_time_record", "acquisition_source_record"]
    missing_critical = [
        row["label"]
        for row in slot_rows
        if row["slot_key"] in critical_slots and row["slot_status"] == "missing"
    ]
    return {
        "status": "ready_for_review" if not missing_critical else "missing_critical_materials",
        "material_file_version": materials_payload.get("version", ""),
        "slot_rows": slot_rows,
        "status_counts": totals,
        "missing_critical_slots": missing_critical,
        "rule": "材料存在不等于验证通过；只有 reviewed_accepted 材料才能作为 verified evidence 候选。",
    }


def build_material_to_evidence_mapping(materials_payload: dict) -> list[dict]:
    rows = []
    for item in materials_payload.get("materials", []):
        slot_key = item.get("slot_key", "")
        slot = VALUE_GATE_MATERIAL_SLOTS.get(slot_key, {})
        status = item.get("review_status", "missing")
        usable_for_verified = status == "reviewed_accepted"
        rows.append(
            {
                "material_id": item.get("material_id", ""),
                "slot_key": slot_key,
                "slot_label": slot.get("label", ""),
                "material_type": item.get("material_type", ""),
                "title": item.get("title", ""),
                "occurred_at": item.get("occurred_at", ""),
                "source_path_or_url": item.get("source_path_or_url", ""),
                "review_status": status,
                "evidence_category": slot.get("category", ""),
                "proves": item.get("proves", []),
                "does_not_prove": item.get("does_not_prove", []),
                "usable_for_verified_evidence": usable_for_verified,
                "decision_effect": "可进入 verified evidence 候选" if usable_for_verified else "只能作为待复核材料或缺失项",
            }
        )
    return rows


def build_rejudgment_readiness_gate(material_summary: dict, material_mapping: list[dict]) -> dict:
    accepted_slots = {
        item.get("slot_key")
        for item in material_mapping
        if item.get("review_status") == "reviewed_accepted"
    }
    submitted_slots = {
        item.get("slot_key")
        for item in material_mapping
        if item.get("review_status") == "submitted_pending_review"
    }
    payment_ready = "payment_proof" in accepted_slots
    service_loop_ready = bool({"mvp_experiment_record", "delivery_acceptance_record"} & accepted_slots)
    roi_ready = {"price_or_quote_record", "delivery_time_record", "acquisition_source_record"}.issubset(accepted_slots)
    productization_ready = "repurchase_or_referral_record" in accepted_slots
    if payment_ready and service_loop_ready and roi_ready and productization_ready:
        status = "ready_for_productization_rejudgment"
    elif payment_ready and service_loop_ready and roi_ready:
        status = "ready_for_roi_rejudgment"
    elif payment_ready and service_loop_ready:
        status = "ready_for_service_mvp_rejudgment"
    elif submitted_slots:
        status = "submitted_pending_review"
    else:
        status = "not_ready_missing_materials"
    return {
        "status": status,
        "payment_ready": payment_ready,
        "service_loop_ready": service_loop_ready,
        "roi_ready": roi_ready,
        "productization_ready": productization_ready,
        "accepted_slots": sorted(accepted_slots),
        "submitted_slots": sorted(submitted_slots),
        "missing_critical_slots": material_summary.get("missing_critical_slots", []),
        "next_action": "先人工复核 submitted_pending_review 材料；缺失关键槽位时不得升级证据或 ROI 结论。",
    }


def build_verified_evidence_assessment(material_summary: dict, material_mapping: list[dict]) -> dict:
    accepted = [item for item in material_mapping if item.get("review_status") == "reviewed_accepted"]
    rejected = [item for item in material_mapping if item.get("review_status") == "reviewed_rejected"]
    pending = [item for item in material_mapping if item.get("review_status") == "submitted_pending_review"]
    accepted_slots = {item.get("slot_key") for item in accepted}
    evidence_rows = [
        {
            "slot_key": item.get("slot_key", ""),
            "slot_label": item.get("slot_label", ""),
            "material_id": item.get("material_id", ""),
            "review_status": item.get("review_status", ""),
            "verified_effect": item.get("decision_effect", ""),
            "cannot_prove": item.get("does_not_prove", []),
        }
        for item in material_mapping
        if item.get("review_status") != "missing"
    ]
    if {"payment_proof", "customer_record", "mvp_experiment_record"} <= accepted_slots or {
        "payment_proof",
        "customer_record",
        "delivery_acceptance_record",
    } <= accepted_slots:
        evidence_level = "S_verified"
    elif accepted_slots:
        evidence_level = "S_partial_verified"
    elif pending:
        evidence_level = "S_claimed"
    else:
        evidence_level = "S_claimed"
    return {
        "status": evidence_level,
        "accepted_material_count": len(accepted),
        "pending_material_count": len(pending),
        "rejected_material_count": len(rejected),
        "accepted_slots": sorted(accepted_slots),
        "evidence_rows": evidence_rows,
        "rule": "只有 reviewed_accepted 材料可以支撑 verified evidence；pending 材料不能进入完整 PRD 事实层。",
    }


def build_s_claimed_to_s_verified_gate(verified_assessment: dict, material_summary: dict, rejudgment_gate: dict) -> dict:
    status = verified_assessment.get("status", "S_claimed")
    if status == "S_verified":
        can_upgrade = True
        upgrade_blockers = []
    elif status == "S_partial_verified":
        can_upgrade = False
        upgrade_blockers = ["强证据链路部分成立，但缺少付款、客户、MVP/交付中的至少一个关键槽位。"]
    else:
        can_upgrade = False
        upgrade_blockers = material_summary.get("missing_critical_slots", []) or ["尚未提供可复核材料。"]
    return {
        "current_level": status,
        "can_upgrade_to_s_verified": can_upgrade,
        "upgrade_blockers": upgrade_blockers,
        "allowed_decision_use": "完整 PRD 候选" if can_upgrade and rejudgment_gate.get("roi_ready") else "服务化 MVP / 客户项目验证",
        "forbidden_use": [
            "未复核材料不得进入完整 PRD 事实层",
            "外部竞品不得升级自身商业价值证据",
            "只有截图但缺客户 / 时间 / 场景不得直接 S_verified",
        ],
    }


def build_external_research_results(evidence_basis: list[dict], competitor_table: dict, research_queue: dict) -> dict:
    rows = []
    for item in evidence_basis:
        if item.get("source_type") != "external_public_source":
            continue
        rows.append(
            {
                "source_title": item.get("source_title", ""),
                "url": item.get("source_url", ""),
                "captured_at": item.get("checked_at") or item.get("captured_at") or date.today().isoformat(),
                "excerpt": item.get("evidence_excerpt") or item.get("evidence", ""),
                "can_prove": item.get("proves", ""),
                "cannot_prove": item.get("does_not_prove", ""),
                "credibility": item.get("strength", ""),
                "decision_effect": item.get("decision_impact", ""),
                "fetch_status": item.get("fetch_status") or "not_checked",
            }
        )
    for item in competitor_table.get("rows", []):
        rows.append(
            {
                "source_title": item.get("source_title") or item.get("name", ""),
                "url": item.get("source_url", ""),
                "captured_at": item.get("checked_at") or date.today().isoformat(),
                "excerpt": item.get("focus", ""),
                "can_prove": item.get("what_it_proves", ""),
                "cannot_prove": item.get("what_it_does_not_prove", ""),
                "credibility": "competitor_public_reference",
                "decision_effect": "证明竞品形态、市场参照或价格锚点存在；不证明本项目利润、ROI、复购或获客成立。",
                "fetch_status": item.get("fetch_status") or "not_checked",
            }
        )
    return {
        "status": "available" if rows else "no_external_results",
        "generated_from_queue": research_queue.get("queue_status", ""),
        "row_count": len(rows),
        "rows": rows,
        "decision_rule": "外部证据只能证明市场、竞品、趋势、规则或对象存在；不能单独证明本项目利润、ROI、获客、复购或产品化成立。",
    }


def build_source_quality_scorecard(external_research_results: dict, source_quality_gate: dict) -> dict:
    rows = external_research_results.get("rows", [])
    reachable = [item for item in rows if item.get("fetch_status") == "reachable"]
    non_success = [item for item in rows if item.get("fetch_status") not in {"", "reachable", "not_checked"}]
    not_checked = [item for item in rows if item.get("fetch_status") in {"", "not_checked"}]
    if non_success:
        status = "has_source_risk"
    elif reachable or rows:
        status = "usable_for_market_context"
    else:
        status = "no_source_to_score"
    return {
        "overall_status": status,
        "source_quality_gate_status": source_quality_gate.get("overall_status", ""),
        "counts": {
            "total_external_rows": len(rows),
            "reachable": len(reachable),
            "non_success": len(non_success),
            "not_checked": len(not_checked),
        },
        "rows": [
            {
                "source_title": item.get("source_title", ""),
                "url": item.get("url", ""),
                "fetch_status": item.get("fetch_status", ""),
                "credibility": item.get("credibility", ""),
                "decision_use": item.get("decision_effect", ""),
            }
            for item in rows[:30]
        ],
        "decision_rule": "来源质量只决定外部证据能否作为市场上下文使用；不能把外部来源自动升级为自身商业验证。",
    }


def build_competitor_pricing_evidence(evidence_basis: list[dict], competitor_table: dict) -> dict:
    pricing_tokens = ("价格", "pricing", "Pricing", "月费", "套餐", "3,000", "25,000", "Goodie", "SEORCE")
    rows = []
    for item in evidence_basis:
        haystack = " ".join(str(item.get(key, "")) for key in ("evidence", "source_title", "evidence_excerpt"))
        if any(token in haystack for token in pricing_tokens):
            rows.append(
                {
                    "source_title": item.get("source_title", ""),
                    "url": item.get("source_url", ""),
                    "pricing_signal": item.get("evidence", ""),
                    "can_prove": item.get("proves", ""),
                    "cannot_prove": item.get("does_not_prove", ""),
                    "decision_effect": item.get("decision_impact", ""),
                }
            )
    for item in competitor_table.get("rows", []):
        haystack = " ".join(str(item.get(key, "")) for key in ("name", "source_title", "focus", "benchmark_signal"))
        if any(token in haystack for token in ("Goodie", "SEORCE", "pricing", "价格", "套餐")):
            rows.append(
                {
                    "source_title": item.get("source_title") or item.get("name", ""),
                    "url": item.get("source_url", ""),
                    "pricing_signal": item.get("benchmark_signal", ""),
                    "can_prove": item.get("what_it_proves", ""),
                    "cannot_prove": item.get("what_it_does_not_prove", ""),
                    "decision_effect": "可作为竞品价格和服务方式锚点；不能证明本项目 ROI。",
                }
            )
    return {
        "status": "available" if rows else "missing_pricing_evidence",
        "rows": rows,
        "decision_rule": "竞品价格只能作为定价参照和用户预算假设来源；本项目 ROI 必须用自身客单价、获客成本、交付工时、工具成本和复购材料计算。",
    }


def build_platform_rule_evidence(evidence_basis: list[dict], contextual_redline_filter: dict) -> dict:
    platform_tokens = ("DeepSeek", "豆包", "Qwen", "通义", "元宝", "平台规则", "AI 平台")
    rows = []
    for item in evidence_basis:
        haystack = " ".join(str(item.get(key, "")) for key in ("evidence", "source_title", "evidence_excerpt"))
        if any(token in haystack for token in platform_tokens):
            rows.append(
                {
                    "source_title": item.get("source_title", ""),
                    "url": item.get("source_url", ""),
                    "excerpt": item.get("evidence_excerpt") or item.get("evidence", ""),
                    "can_prove": item.get("proves", ""),
                    "cannot_prove": item.get("does_not_prove", ""),
                    "decision_effect": item.get("decision_impact", ""),
                }
            )
    return {
        "status": "needs_platform_boundary_review" if contextual_redline_filter.get("active_rules") else "no_platform_rule_detected",
        "rows": rows,
        "active_domains": contextual_redline_filter.get("active_domains", []),
        "active_rules": contextual_redline_filter.get("active_rules", []),
        "human_confirmation_required": contextual_redline_filter.get("human_confirmation_required", False),
        "decision_rule": "平台可达性和公开文档只能证明监测对象存在；GEO 操作方式、内容优化、截图/数据使用和客户授权边界仍需人工确认。",
    }


def material_value_for_slot(material_mapping: list[dict], slot_key: str) -> str:
    candidates = [
        item
        for item in material_mapping
        if item.get("slot_key") == slot_key and item.get("review_status") == "reviewed_accepted"
    ]
    if not candidates:
        return "待确认"
    parts = []
    for item in candidates:
        for key in ("title", "source_path_or_url"):
            value = str(item.get(key, "")).strip()
            if value and value not in {"待填写", "待确认"}:
                parts.append(value)
    return "；".join(unique_list(parts))[:120] if parts else "已复核材料存在，但需结构化录入具体数值"


def build_material_roi_values(material_mapping: list[dict]) -> dict:
    return {
        "price_floor": material_value_for_slot(material_mapping, "price_or_quote_record"),
        "acquisition_cost": material_value_for_slot(material_mapping, "acquisition_source_record"),
        "delivery_hours_per_customer": material_value_for_slot(material_mapping, "delivery_time_record"),
        "human_review_cost": "待确认",
        "tool_cost": "待确认",
        "maintenance_cost": material_value_for_slot(material_mapping, "delivery_acceptance_record"),
        "repurchase_signal": material_value_for_slot(material_mapping, "repurchase_or_referral_record"),
    }


def build_verified_evidence_gate(evidence_basis: list[dict], payment_level: int) -> dict:
    strong_tokens = ("MVP", "买单", "付款", "付费", "预算", "合同", "复购", "真实支付")
    claimed = [
        item
        for item in evidence_basis
        if item.get("source_type") == "user_provided_fact"
        and any(token in item.get("evidence", "") for token in strong_tokens)
    ]
    verified = [
        item
        for item in evidence_basis
        if item.get("source_type") == "internal_project_evidence"
        and any(token in item.get("evidence", "") for token in strong_tokens)
    ]
    status = "no_strong_evidence"
    if verified:
        status = "verified_strong_evidence_available"
    elif claimed:
        status = "claimed_strong_evidence_pending_verification"
    can_treat_as_s_level = bool(verified)
    verification_required = [
        "付款截图 / 收款记录 / 发票 / 合同",
        "客户名称或可脱敏客户记录",
        "MVP 实验记录、交付物或复测记录",
        "客户验收记录或明确预算记录",
        "复购、续费、复测或转介绍记录",
    ]
    full_prd_blocking_gap = []
    if claimed and not verified:
        full_prd_blocking_gap.append("强业务事实尚未附件 / 内部记录复核，不能当作 S 级已验证证据。")
    if payment_level >= 4 and not verified:
        full_prd_blocking_gap.append("付款 / 买单 / MVP 信号目前只能作为用户提供事实，不能直接证明完整 PRD 或 SaaS 产品化成立。")
    return {
        "status": status,
        "claimed_evidence_grade": "S_claimed" if payment_level >= 5 or claimed else "not_claimed",
        "verified_evidence_grade": "S_verified" if can_treat_as_s_level else "unverified",
        "can_treat_as_s_level": can_treat_as_s_level,
        "claimed_strong_evidence": [item.get("evidence", "") for item in claimed],
        "verified_strong_evidence": [item.get("evidence", "") for item in verified],
        "verification_required": verification_required,
        "full_prd_blocking_gap": full_prd_blocking_gap,
        "prd_fact_rule": "用户提供事实可以进入 PRD 事实层，但必须标注为用户提供；未经附件或内部记录复核，不得写成独立验证或 S 级已验证证据。",
    }


def build_payment_evidence_verification(payment_level: int, verified_gate: dict) -> dict:
    verified_level = 5 if verified_gate.get("can_treat_as_s_level") else 0
    usable_layer = verified_level if verified_level else (4 if payment_level >= 4 else payment_level)
    layers = [
        (1, "感兴趣", "只能证明方向可能有兴趣"),
        (2, "愿意试用", "只能证明愿意体验"),
        (3, "愿意留资 / 预约 / 进群", "只能证明轻量行动"),
        (4, "愿意付定金 / 预付款 / 进入采购流程", "强付费候选，需复核"),
        (5, "真实支付 / 签合同 / 复购", "强付费证据，必须有材料"),
    ]
    layer_rows = []
    for level, label, meaning in layers:
        if verified_level >= level:
            status = "verified"
        elif payment_level >= level:
            status = "claimed"
        else:
            status = "not_present"
        layer_rows.append(
            {
                "level": level,
                "label": label,
                "status": status,
                "meaning": meaning,
                "required_evidence": "客户记录、预算、定金、付款、合同或复购材料" if level >= 4 else "用户行为或意向记录",
            }
        )
    return {
        "claimed_payment_layer": payment_level,
        "verified_payment_layer": verified_level,
        "usable_payment_layer_for_decision": usable_layer,
        "usable_for_current_path": "服务化 MVP / 客户项目验证" if payment_level >= 4 and not verified_level else "按已验证层级判断",
        "cannot_support": [] if verified_level >= 5 else ["完整 SaaS PRD", "高 ROI 结论", "规模化产品化判断"],
        "layer_rows": layer_rows,
        "decision_rule": "用户声明的第 5 层付费信号未复核前，只能作为 claimed evidence；不得当作 S_verified 或完整 PRD 证据。",
    }


def build_evidence_verification_intake(verified_gate: dict) -> dict:
    slot_defs = [
        (
            "payment_proof",
            "付款 / 合同证据",
            ["付款截图", "收款记录", "发票", "合同", "定金记录", "采购流程记录"],
            "将用户声明的买单信号从 S_claimed 推进到 S_verified 候选。",
            "不能单独证明复购、获客成本、交付利润或 SaaS 产品化成立。",
            "完整 PRD / 产品化复判",
        ),
        (
            "customer_record",
            "客户 / 行业记录",
            ["客户名称", "脱敏客户记录", "行业类型", "联系人角色", "预算方 / 决策方说明"],
            "证明付费对象、决策者和第一批行业不是泛泛假设。",
            "不能单独证明客户会复购、转介绍或接受标准化产品。",
            "获客和目标客户边界",
        ),
        (
            "mvp_experiment_record",
            "MVP 实验记录",
            ["实验目标", "样本客户", "检测结果", "报告样例", "复测记录", "客户反馈"],
            "证明已有实验不是概念讨论，而是有可复判过程。",
            "不能单独证明真实利润、获客效率或多客户可复制。",
            "服务化 MVP / 价值兑现周期",
        ),
        (
            "delivery_acceptance_record",
            "交付 / 验收记录",
            ["交付周期", "交付工时", "人工复核轮次", "返工次数", "客户验收记录"],
            "证明交付成本和验收结果可被记录。",
            "不能单独证明长期复购或获客成本可控。",
            "真实利润和交付成本判断",
        ),
        (
            "repurchase_or_referral_record",
            "复购 / 续费 / 转介绍记录",
            ["复购记录", "续费意向", "复测意愿", "转介绍记录", "代运营意向"],
            "证明价值不是一次性项目，有持续收入或扩展机会。",
            "不能单独证明边际交付成本已经下降或 SaaS 产品化已成立。",
            "产品化升级和 ROI 复判",
        ),
        (
            "price_or_quote_record",
            "报价 / 客单价证据",
            ["报价单", "客户接受价格记录", "服务套餐价格", "议价记录", "最低可接受价格确认"],
            "证明服务价格区间和最低客单价不是主观假设。",
            "不能单独证明毛利成立，仍需交付、获客、工具和维护成本。",
            "ROI / 最小利润复判",
        ),
        (
            "delivery_time_record",
            "交付工时证据",
            ["报告制作工时", "数据采集工时", "人工复核工时", "返工工时", "客户解释 / 售后工时"],
            "证明单客户交付成本可被核算。",
            "不能单独证明客户愿意付费或复购。",
            "真实利润 / 是否可标准化",
        ),
        (
            "acquisition_source_record",
            "获客来源证据",
            ["线索来源", "转介绍记录", "内容获客记录", "销售触达记录", "免费检测提交记录", "加顾问记录"],
            "证明第一批客户从哪里来，以及 CAC/LTV 是否可以继续验证。",
            "不能单独证明服务价值成立，仍需成交和交付结果。",
            "获客路径 / CAC 复判",
        ),
    ]
    slots = []
    for key, label, accepted, effect, cannot_prove, required_for in slot_defs:
        slots.append(
            {
                "key": key,
                "label": label,
                "current_status": "missing",
                "accepted_materials": accepted,
                "verification_effect": effect,
                "cannot_prove": cannot_prove,
                "required_for": required_for,
            }
        )
    blocking_items = list(verified_gate.get("full_prd_blocking_gap", []))
    return {
        "status": "verification_required" if blocking_items else "verification_not_required",
        "purpose": "把用户声明、外部来源和项目材料分层复核，决定哪些证据能进入 PRD 事实层、哪些只能作为假设或待验证项。",
        "accepted_evidence_types": [
            "付款 / 合同",
            "客户记录",
            "MVP 实验记录",
            "交付验收",
            "复购 / 续费 / 转介绍",
            "报价 / 客单价",
            "交付工时",
            "获客来源",
        ],
        "verification_slots": slots,
        "current_blocking_items": blocking_items,
        "verification_table_status": "all_missing_until_user_materials_attached",
        "s_verified_upgrade_requirements": [
            "付款 / 合同证据至少补齐一项",
            "MVP 实验记录或交付验收记录至少补齐一项",
            "报价 / 客单价和交付工时必须能支持最小利润判断",
            "复购 / 复测 / 转介绍材料用于产品化升级，不用于首轮服务化 MVP 放行",
        ],
        "upgrade_rule": "只有付款 / 合同、MVP 实验、交付验收、报价、交付工时或复购等材料被项目内记录复核后，才允许从 S_claimed 升级为 S_verified；未补齐前只能支持服务化 MVP 或客户项目验证。",
        "prd_usage_rule": verified_gate.get("prd_fact_rule", ""),
        "next_action": "补齐付款、客户、MVP、交付、复购、报价、工时和获客来源材料后重新运行价值门禁；未补齐前只能支撑服务化 MVP 或客户项目验证。",
    }


def extract_roi_input_value(raw_text: str, labels: tuple[str, ...], fallback: str = "待确认") -> str:
    for label in labels:
        pattern = rf"{re.escape(label)}\s*(?:为|是|约|大概|大约|:|：)?\s*([^，。；;\n]+)"
        match = re.search(pattern, raw_text)
        if match:
            value = match.group(1).strip()
            if is_usable_roi_input_value(value):
                return value[:60]
    return fallback


def is_usable_roi_input_value(value: str) -> bool:
    cleaned = value.strip()
    if not cleaned:
        return False
    if cleaned.startswith(("未", "不", "待", "是否", "能否", "需要", "如果", "、", "-", "—", "：", ":")):
        return False
    if re.search(r"(是否|能否|不确定|待确认|需要确认|需要补|是否能)", cleaned):
        return False
    if re.search(r"([0-9０-９]|元|万元|美元|¥|￥|USD|人天|小时|工时|天|周|月|年|次|%|％)", cleaned):
        return True
    return bool(re.search(r"(已确认|已提供|有记录|有合同|已付款|已续费|已复购|已预约复测)", cleaned))


def build_roi_input_table(raw_text: str, operating_model: dict, true_profit: dict, material_roi_values: dict | None = None) -> dict:
    profit_conditions = operating_model.get("minimum_profit_conditions", {})
    material_roi_values = material_roi_values or {}
    def roi_value(key: str, fallback: str) -> str:
        material_value = material_roi_values.get(key, "待确认")
        if material_value and material_value != "待确认":
            return material_value
        return fallback
    input_defs = [
        {
            "key": "price_floor",
            "label": "首期服务价格 / 最低客单价",
            "current_value": roi_value("price_floor", profit_conditions.get("price_floor") if profit_conditions.get("price_floor") != "待确认" else extract_roi_input_value(raw_text, ("客单价", "服务价格", "首期价格", "报价"))),
            "evidence_required": "报价单、合同、付款记录或客户接受价格记录",
            "decision_rule": "低于获客、交付、工具、维护和风险成本总和时，不允许声称 ROI 成立。",
            "blocks_high_roi": True,
        },
        {
            "key": "acquisition_cost",
            "label": "单个有效客户获客成本",
            "current_value": roi_value("acquisition_cost", profit_conditions.get("acquisition_cost") if profit_conditions.get("acquisition_cost") != "待确认" else extract_roi_input_value(raw_text, ("获客成本", "CAC", "线索成本"))),
            "evidence_required": "渠道投放、转介绍、销售工时或线索转化记录",
            "decision_rule": "获客成本高于客单价或无法回收时，停止产品化或降级服务项目。",
            "blocks_high_roi": True,
        },
        {
            "key": "delivery_hours_per_customer",
            "label": "单客户交付工时",
            "current_value": roi_value("delivery_hours_per_customer", profit_conditions.get("delivery_hours_per_customer") if profit_conditions.get("delivery_hours_per_customer") != "待确认" else extract_roi_input_value(raw_text, ("交付工时", "交付时间", "服务工时"))),
            "evidence_required": "服务记录、报告制作记录、人工复核和返工记录",
            "decision_rule": "交付工时持续过高时，服务化可继续验证，但不能升级 SaaS 或重研发。",
            "blocks_high_roi": True,
        },
        {
            "key": "human_review_cost",
            "label": "人工复核成本",
            "current_value": roi_value("human_review_cost", profit_conditions.get("human_review_cost") if profit_conditions.get("human_review_cost") != "待确认" else extract_roi_input_value(raw_text, ("人工复核成本", "复核成本", "审核成本"))),
            "evidence_required": "审核轮次、审核人力、报告修改记录",
            "decision_rule": "人工复核不可控时，说明边际交付成本难以下降。",
            "blocks_high_roi": True,
        },
        {
            "key": "tool_cost",
            "label": "工具 / 模型 / 监测成本",
            "current_value": roi_value("tool_cost", extract_roi_input_value(raw_text, ("工具成本", "模型成本", "监测成本", "API 成本"))),
            "evidence_required": "API、工具订阅、监测工具、人工采样脚本成本记录",
            "decision_rule": "工具成本必须纳入真实利润，不得只看收入。",
            "blocks_high_roi": True,
        },
        {
            "key": "maintenance_cost",
            "label": "维护 / 售后成本",
            "current_value": roi_value("maintenance_cost", profit_conditions.get("after_sales_maintenance") if profit_conditions.get("after_sales_maintenance") != "待确认" else extract_roi_input_value(raw_text, ("维护成本", "售后成本", "复测成本"))),
            "evidence_required": "复测、客户答疑、报告解释、后续优化记录",
            "decision_rule": "维护成本不可控时，不允许把一次成交写成长期利润成立。",
            "blocks_high_roi": True,
        },
        {
            "key": "repurchase_signal",
            "label": "复购 / 续费 / 复测信号",
            "current_value": roi_value("repurchase_signal", extract_roi_input_value(raw_text, ("复购", "续费", "复测意愿", "代运营意向"))),
            "evidence_required": "复购记录、续费意向、复测预约、代运营合同或转介绍",
            "decision_rule": "没有复购或复测信号时，只能证明首单价值，不能证明 LTV 或产品化价值。",
            "blocks_high_roi": True,
        },
    ]
    rows = []
    missing_critical = []
    for item in input_defs:
        current_value = item["current_value"] or "待确认"
        source_status = "missing" if current_value == "待确认" else ("provided_in_reviewed_material" if material_roi_values.get(item["key"]) not in {"", None, "待确认"} else "provided_in_input")
        row = dict(item)
        row["current_value"] = current_value
        row["source_status"] = source_status
        rows.append(row)
        if item["blocks_high_roi"] and source_status == "missing":
            missing_critical.append(item["label"])
    status = "roi_inputs_complete" if not missing_critical else "missing_critical_roi_inputs"
    return {
        "status": status,
        "can_calculate_roi": not missing_critical,
        "can_claim_high_roi": False if missing_critical else None,
        "formula": "ROI = (收入 - 获客成本 - 交付成本 - 人工复核成本 - 工具成本 - 维护 / 售后成本 - 风险成本) / 总投入",
        "input_rows": rows,
        "missing_critical_inputs": missing_critical,
        "minimum_viable_roi_rule": "只有首期价格、获客成本、交付工时、工具成本、维护成本和复购 / 复测信号可被证据支持后，才允许讨论高 ROI 或产品化放大。",
        "decision_effect": "ROI 输入缺失时，价值门禁只能支持服务化 MVP 收集数据，不能支持完整 SaaS、重研发或高 ROI 结论。",
    }


def build_value_realization_timeline(raw_text: str, decision: str, operating_model: dict) -> dict:
    if is_geo_context(raw_text):
        milestones = [
            {
                "stage": "初筛检测",
                "expected_cycle": "1-3 天",
                "evidence_status": "待用首批客户记录确认",
                "required_material": "品牌 / 关键词 / 竞品在 DeepSeek、豆包、Qwen、元宝等平台的首轮检测记录。",
            },
            {
                "stage": "首单成交",
                "expected_cycle": operating_model.get("validation_window", "2-4 周"),
                "evidence_status": "待确认",
                "required_material": "真实付款、合同、预算或明确付费承诺记录。",
            },
            {
                "stage": "报告交付",
                "expected_cycle": "待确认",
                "evidence_status": "待确认",
                "required_material": "单客户报告交付周期、人工复核轮次和返工记录。",
            },
            {
                "stage": "复测验证",
                "expected_cycle": "2-4 周复测",
                "evidence_status": "待确认",
                "required_material": "AI 提及率、品牌推荐率、竞品覆盖差距、引用来源质量、多模型一致性复测变化。",
            },
            {
                "stage": "复购 / 续费",
                "expected_cycle": "4-8 周观察",
                "evidence_status": "待确认",
                "required_material": "复购、续费、代运营意向或转介绍记录。",
            },
            {
                "stage": "产品化复判",
                "expected_cycle": "完成 2-3 个相似客户后",
                "evidence_status": "未满足",
                "required_material": "相似客户、标准化流程、边际交付成本下降和可复用能力证据。",
            },
        ]
        unknowns = ["真实报告交付周期", "成交周期", "复购周期", "单客户交付工时", "复测归因周期"]
    else:
        milestones = [
            {
                "stage": "首轮验证",
                "expected_cycle": operating_model.get("validation_window", "待确认"),
                "evidence_status": "待确认",
                "required_material": "目标用户、核心任务、付费或效率证据。",
            },
            {
                "stage": "价值兑现",
                "expected_cycle": "待确认",
                "evidence_status": "待确认",
                "required_material": "可衡量结果、归因材料和成本记录。",
            },
            {
                "stage": "升级复判",
                "expected_cycle": "待确认",
                "evidence_status": "待确认",
                "required_material": "复购、复用、交付成本下降或内部效率稳定提升材料。",
            },
        ]
        unknowns = ["价值兑现周期", "交付周期", "复判周期"]
    return {
        "status": "timeline_unverified_blocks_scaling" if decision != VALUE_GATE_ALLOW_PRD else "timeline_needs_confirmation",
        "milestones": milestones,
        "unknowns": unique_list(unknowns + operating_model.get("unknowns_that_block_scaling", [])),
        "decision_effect": "价值兑现周期未被真实记录前，只能支撑验证路径，不能支撑完整 SaaS、重研发或规模化产品化判断。",
    }


def build_output_boundary_gate(decision: str, route_package_name: str) -> dict:
    return {
        "status": "within_boundary",
        "allowed_outputs": [
            "值不值得做的商业判断",
            "证据表和证据充分性结论",
            "经营边界和验证周期",
            "A/B/C/D/E/F/G 路径输入包",
            "给 PRD 模块的事实 / 假设 / 禁止声称边界",
            "单个想法的后续承接路径建议",
        ],
        "forbidden_outputs": [
            "完整 PRD 正文",
            "完整功能清单",
            "完整页面结构和交互流",
            "技术架构和开发排期",
            "自动化运营方案",
            "未经验证的 ROI 承诺",
            "跨项目优先级排序",
            "资源分配排名",
            "所有机会里的投资优先级判断",
        ],
        "does_not_rank_against_other_projects": True,
        "priority_boundary_rule": "前置模块只判断单个想法有没有价值、证据是否达标、应进入哪条验证路径；不判断它在所有机会中的优先级、资源排名或公司级投资顺序。",
        "detected_boundary_risks": [],
        "route_package": route_package_name,
        "current_decision_gate": decision,
        "rule": "价值门禁只决定是否值得做、走哪条验证路径、给下一模块哪些输入；不能替代 PRD、原型、开发文档、商业执行方案或跨项目优先级决策。",
    }


def is_geo_prd_input_package(prd_input_package: dict) -> bool:
    return is_geo_context(json.dumps(prd_input_package, ensure_ascii=False))


def build_geo_service_mvp_package(base_package: dict) -> dict:
    package = dict(base_package)
    package.update(
        {
            "path_goal": "用 2-4 周服务化 MVP 验证 GEO 商业闭环：免费检测获客、体检报告成交、复测证明价值、后续优化 / 代运营转化。",
            "free_diagnosis_entry": {
                "purpose": "用低门槛免费检测获取目标客户线索。",
                "required_inputs": ["品牌 / 产品名称", "官网或主要内容资产", "3-10 个核心业务词", "主要竞品", "联系人或顾问承接方式"],
                "output": "AI 检索曝光初筛结果和是否值得做完整体检报告的判断。",
                "records_required": ["免费检测提交数", "有效线索数", "加顾问数", "无效线索原因"],
            },
            "diagnosis_report": {
                "purpose": "把 GEO 价值转成客户能理解和愿意付费的服务结果。",
                "must_include": ["品牌 AI 提及率", "品牌推荐率", "竞品覆盖差距", "关键词回答覆盖率", "引用来源质量", "多模型一致性", "问题样本和复测建议"],
                "acceptance_signal": ["客户认可报告结论", "客户愿意付费进入优化 / 复测", "客户愿意提供更多词库或内容资产"],
            },
            "metric_dashboard": {
                "purpose": "用轻量表格 / 看板记录验证数据，不做完整 SaaS。",
                "minimum_metrics": [
                    "免费检测提交数",
                    "有效线索率",
                    "加顾问率",
                    "体检报告成交率",
                    "后续优化项目转化率",
                    "月度代运营复购 / 续费率",
                    "单客户交付工时",
                    "真实利润",
                ],
                "must_not_build_yet": ["完整多租户后台", "复杂权限系统", "自动化投放系统", "完整 SaaS 计费系统"],
            },
            "recheck_mechanism": {
                "purpose": "通过复测证明服务动作是否带来可解释变化。",
                "cadence": "首轮报告后 1-2 周复测一次，服务化 MVP 期至少保留前后对比。",
                "records_required": ["基线截图 / 表格", "优化动作记录", "复测结果", "变化解释", "外部干扰因素"],
            },
            "optimization_suggestions": {
                "purpose": "把诊断报告转成可销售的后续服务。",
                "examples": ["内容资产补齐", "FAQ / 问答页优化", "行业词库扩展", "品牌叙事统一", "引用来源优化", "竞品回答差距修复"],
                "boundary": "只能输出建议和可验证动作，不承诺 AI 平台排名或推荐结果。",
            },
            "service_conversion_path": [
                "免费检测提交",
                "有效线索筛选",
                "加顾问 / 沟通需求",
                "付费体检报告",
                "报告解释和优化建议",
                "复测",
                "后续优化项目 / 月度代运营",
            ],
            "execution_record_template": [
                "客户行业",
                "线索来源",
                "免费检测提交时间",
                "是否有效线索",
                "是否加顾问",
                "是否购买体检报告",
                "首期服务价格",
                "报告交付周期",
                "单客户交付工时",
                "是否复测",
                "是否转后续优化 / 代运营",
                "客户认可度",
            ],
            "success_criteria": [
                "免费检测提交数达到本轮验证目标",
                "有效线索率可被记录并解释",
                "加顾问率可被记录并解释",
                "体检报告成交率可被记录并解释",
                "复盘预约率可被记录并解释",
                "至少出现第二个付费信号或明确复测 / 续费 / 后续优化 / 代运营意向",
                "单客户交付工时进入可接受上限",
                "客户认可报告和复测结果",
            ],
            "failure_criteria": [
                "客户只愿免费检测但不愿付费体检报告",
                "报告结论不被客户认可",
                "单客户交付工时持续过高",
                "GEO 指标变化无法归因",
                "客户不愿复测 / 复购 / 续费 / 推荐",
                "获客成本高于客单价且无法回收",
            ],
            "minimum_data_loop": [
                "品牌 / 产品输入",
                "问题样本",
                "AI 回答",
                "品牌提及",
                "竞品提及",
                "引用来源",
                "诊断报告",
                "优化动作",
                "复测结果",
                "成交 / 复购记录",
            ],
        }
    )
    package["core_delivery"] = "免费检测结果 + 付费 GEO 体检报告 + 复测记录 + 后续优化建议，不是完整 SaaS。"
    package["core_feedback"] = "客户是否购买体检报告、认可报告、愿意复测、愿意进入后续优化 / 代运营。"
    return package


def build_route_input_packages(prd_input_package: dict, decision: str, blocked_reasons: list[str], verify_next: list[str], redlines: list[str]) -> dict:
    base_summary = prd_input_package.get("product_summary", {})
    low_cost = prd_input_package.get("low_cost_mvp_judgment", {})
    project_to_product = prd_input_package.get("project_to_product_judgment", {})
    evidence = prd_input_package.get("evidence_and_assumptions", {})
    mvp_package = {
        "product_summary": base_summary,
        "path_goal": "验证核心价值闭环是否成立，不等于完整产品化。",
        "core_user": low_cost.get("core_user", []),
        "core_scenario": low_cost.get("core_scenario", []),
        "core_task": low_cost.get("core_task"),
        "core_hypotheses": low_cost.get("core_hypotheses", []),
        "core_features": low_cost.get("core_features", []),
        "core_delivery": low_cost.get("core_delivery"),
        "core_feedback": low_cost.get("core_feedback"),
        "minimum_data_loop": low_cost.get("minimum_data_loop", []),
        "validation_method_boundaries": low_cost.get("validation_method_boundaries", {}),
        "manual_or_tool_replacement": low_cost.get("can_replace_with_manual_or_tools", []),
        "success_criteria": prd_input_package.get("mvp_boundary", {}).get("mvp_success_criteria", []),
        "failure_criteria": prd_input_package.get("mvp_boundary", {}).get("mvp_failure_criteria", []),
        "must_not_include": prd_input_package.get("mvp_boundary", {}).get("not_do_features", []),
    }
    if is_geo_prd_input_package(prd_input_package):
        mvp_package = build_geo_service_mvp_package(mvp_package)
    return {
        "mvp_input_package": mvp_package,
        "client_project_input_package": {
            "product_summary": base_summary,
            "path_goal": "验证项目价值和服务价值，沉淀共性需求，不直接包装成完整产品。",
            "project_value": project_to_product.get("project_value"),
            "service_value": project_to_product.get("service_value"),
            "standardizable_parts": project_to_product.get("standardizable_parts", []),
            "customized_parts": project_to_product.get("customized_parts", []),
            "next_evidence": project_to_product.get("next_evidence", []),
            "project_to_product_watchlist": ["第二个相似客户", "共性流程", "配置化边界", "边际交付成本", "复购或续费"],
            "delivery_scope": ["本客户明确需求", "服务交付过程", "可复用材料沉淀", "验收记录"],
            "acceptance_criteria": ["客户确认交付结果可用", "交付范围未无限扩张", "复盘出可标准化部分"],
            "reuse_observation_table": ["相似客户问题", "可复用流程", "不可复用定制", "边际成本变化", "产品化风险"],
            "customer_validation_metrics": ["付款或预算确认", "验收通过率", "交付工时", "返工轮次", "复购 / 续费意愿"],
            "project_closeout_required": True,
            "productization_rejudgment_materials": ["第二个相似客户", "可配置需求比例", "交付工时下降证据", "复购或转介绍材料"],
            "do_not_productize_until": ["至少出现第二个相似客户", "定制部分和标准部分可分离", "边际交付成本可被记录并下降"],
        },
        "internal_efficiency_input_package": {
            "product_summary": base_summary,
            "path_goal": "验证内部降本、增效、降错或风险降低，不默认对外产品化。",
            "efficiency_value": prd_input_package.get("value_judgment", {}).get("business_result"),
            "metrics": prd_input_package.get("measurability_judgment", {}).get("metrics", []),
            "cost_items": prd_input_package.get("true_profit_judgment", {}).get("cost_items_checked", []),
            "validation_materials": ["当前流程耗时", "使用频率", "人工成本", "错误率", "建设维护成本"],
            "must_quantify": ["节省谁的时间", "每次节省多久", "发生频率", "对应人工成本", "建设和维护成本", "回本周期"],
            "time_saved_per_run": "待确认",
            "frequency": "待确认",
            "labor_cost_baseline": "待确认",
            "build_maintenance_cost": "待确认",
            "payback_period": "待确认",
            "roi_inputs_required": ["单次节省时间", "使用频率", "人力成本", "建设成本", "维护成本", "错误率下降"],
            "efficiency_acceptance_criteria": ["节省时间可记录", "错误率或返工下降可记录", "建设维护成本低于节省价值"],
            "do_not_externalize_until": ["外部付费者明确", "外部场景和内部场景差异被验证", "权限和数据边界可控"],
        },
        "research_input_package": {
            "product_summary": base_summary,
            "path_goal": "补齐价值判断缺口，不进入 PRD 或 MVP 开发。",
            "missing_or_unclear_items": verify_next or evidence.get("must_validate_before_launch", []),
            "open_questions": prd_input_package.get("prd_generation_constraints", {}).get("open_questions", []),
            "recommended_research": ["用户访谈", "付费验证", "成本核算", "获客路径验证", "风险边界确认"],
            "research_outputs_required": ["事实 / 假设分离", "证据等级", "付费层级", "成本结构", "风险边界", "是否复判"],
            "interview_questions": [
                "谁是付费者、决策者、使用者和验收方？",
                "当前替代方案是什么，为什么不够好？",
                "愿意为什么结果付费，最低可接受价格区间是多少？",
                "什么结果出现后会复购、续费或推荐？",
            ],
            "minimum_sample_size": "至少 5 个目标用户 / 客户访谈，或 2 个明确付费 / 预算信号。",
            "payment_test_method": ["付费预售", "报价接受度测试", "试点转付费", "明确预算确认"],
            "competitor_research_tasks": ["竞品定价", "竞品交付方式", "竞品指标体系", "客户评价和痛点"],
            "risk_research_tasks": ["合规边界", "数据授权", "平台规则", "行业红线", "责任边界"],
            "exit_criteria": ["没有明确付费对象", "用户只愿免费试用", "成本结构无法覆盖", "风险边界不可控"],
            "rejudgment_required_materials": ["访谈记录", "付费证据", "成本估算", "竞品证据", "风险确认"],
        },
        "stop_reason_package": {
            "product_summary": base_summary,
            "path_goal": "停止正式 PRD 和开发投入，只允许低成本复判。",
            "blocked_reasons": blocked_reasons,
            "counter_evidence": prd_input_package.get("counter_evidence", []),
            "reopen_conditions": ["出现真实付费", "获客成本可控", "交付成本下降", "价值对象明确"],
        },
        "redline_block_package": {
            "product_summary": base_summary,
            "path_goal": "禁止推进，先完成专业风险确认。",
            "red_line_risks": redlines,
            "required_confirmation": ["专业合规确认", "风险边界重写", "禁止承诺和高风险动作清单"],
        },
    }


def evidence_entry(
    *,
    claim: str,
    source_type: str,
    source_title: str,
    source_url: str,
    confidence: str,
    prd_usage: str,
    note: str = "",
) -> dict:
    return {
        "claim": claim,
        "source_type": source_type,
        "source_title": source_title,
        "source_url": source_url,
        "captured_at": date.today().isoformat(),
        "confidence": confidence,
        "prd_usage": prd_usage,
        "note": note,
        "fetch_status": "not_checked" if source_type == "external_public_source" else "not_applicable",
        "checked_at": "",
        "http_status": None,
        "retrieved_title": "",
        "evidence_excerpt": "",
        "fetch_error": "",
    }


def strip_html_excerpt(html: str, limit: int = 260) -> str:
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
    if title and title not in text[: len(title) + 20]:
        text = f"{title}。{text}"
    return text[:limit]


def fetch_url_evidence(url: str, timeout: int = 6) -> dict:
    if not url.startswith(("http://", "https://")):
        return {
            "fetch_status": "not_applicable",
            "checked_at": "",
            "http_status": None,
            "retrieved_title": "",
            "evidence_excerpt": "",
            "fetch_error": "",
        }
    checked_at = date.today().isoformat()
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ProductValueGateEvidenceFetcher/0.8 (+https://openai.com)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", None) or response.getcode()
            content = response.read(24000)
            charset = response.headers.get_content_charset() or "utf-8"
            html = content.decode(charset, errors="replace")
            title_match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
            title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
            return {
                "fetch_status": "reachable" if 200 <= int(status) < 400 else "non_success_status",
                "checked_at": checked_at,
                "http_status": int(status),
                "retrieved_title": title[:160],
                "evidence_excerpt": strip_html_excerpt(html),
                "fetch_error": "",
            }
    except urllib.error.HTTPError as error:
        return {
            "fetch_status": "non_success_status",
            "checked_at": checked_at,
            "http_status": error.code,
            "retrieved_title": "",
            "evidence_excerpt": "",
            "fetch_error": str(error.reason),
        }
    except Exception as error:  # pragma: no cover - network-dependent
        curl_result = fetch_url_evidence_with_curl(url, timeout=timeout, checked_at=checked_at)
        if curl_result.get("fetch_status") != "unreachable":
            return curl_result
        return {
            "fetch_status": "unreachable",
            "checked_at": checked_at,
            "http_status": None,
            "retrieved_title": "",
            "evidence_excerpt": "",
            "fetch_error": error.__class__.__name__,
        }


def fetch_url_evidence_with_curl(url: str, *, timeout: int, checked_at: str) -> dict:
    try:
        result = subprocess.run(
            [
                "curl",
                "-L",
                "--max-time",
                str(timeout),
                "-A",
                "ProductValueGateEvidenceFetcher/0.8",
                "-sS",
                "-w",
                "\n__HTTP_STATUS__:%{http_code}",
                url,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception as error:  # pragma: no cover - local environment dependent
        return {
            "fetch_status": "unreachable",
            "checked_at": checked_at,
            "http_status": None,
            "retrieved_title": "",
            "evidence_excerpt": "",
            "fetch_error": error.__class__.__name__,
        }
    output = result.stdout or ""
    status_match = re.search(r"\n__HTTP_STATUS__:(\d{3})\s*$", output)
    status = int(status_match.group(1)) if status_match else None
    body = output[: status_match.start()] if status_match else output
    if result.returncode != 0 and not status:
        return {
            "fetch_status": "unreachable",
            "checked_at": checked_at,
            "http_status": None,
            "retrieved_title": "",
            "evidence_excerpt": "",
            "fetch_error": (result.stderr or f"curl_exit_{result.returncode}")[:120],
        }
    title_match = re.search(r"<title[^>]*>(.*?)</title>", body, flags=re.IGNORECASE | re.DOTALL)
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
    return {
        "fetch_status": "reachable" if status and 200 <= status < 400 else "non_success_status",
        "checked_at": checked_at,
        "http_status": status,
        "retrieved_title": title[:160],
        "evidence_excerpt": strip_html_excerpt(body),
        "fetch_error": "" if result.returncode == 0 else (result.stderr or f"curl_exit_{result.returncode}")[:120],
    }


def apply_external_evidence_fetch(ledger: list[dict], *, enabled: bool) -> list[dict]:
    if not enabled:
        return ledger
    updated = []
    for entry in ledger:
        copy = dict(entry)
        if copy.get("source_type") == "external_public_source":
            copy.update(fetch_url_evidence(copy.get("source_url", "")))
        updated.append(copy)
    return updated


def competitor_benchmark_row(
    *,
    name: str,
    market: str,
    source_title: str,
    source_url: str,
    focus: str,
    benchmark_signal: str,
    what_it_proves: str,
    what_it_does_not_prove: str,
    prd_usage: str,
    fetch_external: bool,
) -> dict:
    row = {
        "name": name,
        "market": market,
        "source_title": source_title,
        "source_url": source_url,
        "focus": focus,
        "benchmark_signal": benchmark_signal,
        "what_it_proves": what_it_proves,
        "what_it_does_not_prove": what_it_does_not_prove,
        "prd_usage": prd_usage,
        "fetch_status": "not_checked",
        "checked_at": "",
        "http_status": None,
        "retrieved_title": "",
        "evidence_excerpt": "",
        "fetch_error": "",
    }
    if fetch_external:
        row.update(fetch_url_evidence(source_url))
    return row


def build_competitor_benchmark_table(raw_text: str, *, fetch_external: bool = False) -> dict:
    if not is_geo_context(raw_text):
        return {
            "status": "not_applicable",
            "scope": "非 GEO 场景不生成 GEO 竞品标杆表。",
            "coverage": {"china_count": 0, "international_count": 0},
            "rows": [],
            "decision_rule": "竞品只能证明能力形态和市场参照存在，不能单独证明本项目商业价值、利润或 ROI 成立。",
            "prd_usage_rule": "PRD 可引用竞品作为市场和能力参照，但不得把竞品存在写成本项目必然成立。",
        }
    rows = [
        competitor_benchmark_row(
            name="KAWO GEO域见",
            market="中国",
            source_title="GEO域见 - KAWO",
            source_url="https://geo.kawo.com/zh/",
            focus="品牌 AI 可见度监测、叙事健康度、竞品对标、提示词挖掘和优化建议。",
            benchmark_signal="国内品牌监测 + 合规/技术准备 + 闭环优化。",
            what_it_proves="中国市场已有面向品牌的 GEO/AEO 监测和优化产品形态。",
            what_it_does_not_prove="不能证明本项目能获客、盈利或高 ROI。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="商脉通GEO",
            market="中国",
            source_title="商脉通GEO",
            source_url="https://www.smt.wang/",
            focus="面向中国企业的 AI 搜索优化，覆盖豆包、DeepSeek、Kimi 等平台的品牌曝光诊断和周期看板。",
            benchmark_signal="国内服务化 GEO 诊断 + 持续监测看板。",
            what_it_proves="国内已有围绕 DeepSeek、豆包等平台做 GEO 服务化交付的公开竞品。",
            what_it_does_not_prove="不能证明本项目的交付成本、复购和利润成立。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="GT-GEO",
            market="中国",
            source_title="广拓时代 GT-GEO",
            source_url="https://geo.cantotimes.com/",
            focus="覆盖 DeepSeek、豆包、文心一言、通义千问、Kimi、腾讯元宝的品牌监测、竞品分析和诊断报告。",
            benchmark_signal="国内多 AI 平台覆盖 + 竞品分析 + 诊断报告。",
            what_it_proves="国内竞品已把多平台监测、竞品分析和报告交付打包成 GEO 服务。",
            what_it_does_not_prove="不能证明本项目可直接做完整 SaaS。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="GEOBase",
            market="中国",
            source_title="GEOBase",
            source_url="https://geobase.org.cn/",
            focus="GEO 排名检测、GEO 指数查询、品牌可见度和引用/推荐路径分析。",
            benchmark_signal="免费/轻量工具入口 + 品牌可见度检测。",
            what_it_proves="国内存在低门槛检测工具，说明服务化 MVP 需要差异化深度和交付质量。",
            what_it_does_not_prove="不能证明低价工具模式适合本项目。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="711AI",
            market="中国",
            source_title="711AI-GEO优化监测平台",
            source_url="https://www.711.cn/",
            focus="AI 搜索查询、品牌检测、关键词热度趋势和行业 GEO 数据报告。",
            benchmark_signal="查询工具 + 行业数据报告。",
            what_it_proves="国内已有用行业报告和查询工具承接 GEO 需求的竞品形态。",
            what_it_does_not_prove="不能证明单客户服务利润或复购成立。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="Profound",
            market="海外",
            source_title="Profound",
            source_url="https://www.tryprofound.com/",
            focus="AI search visibility、answer engine 监测、引用和品牌表现分析。",
            benchmark_signal="海外企业级 AI 可见度平台参照。",
            what_it_proves="海外已有企业级 AI visibility/GEO 平台方向。",
            what_it_does_not_prove="不能证明中国市场客户愿意按海外价格付费。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="Peec AI",
            market="海外",
            source_title="Peec AI",
            source_url="https://peec.ai/",
            focus="AI search analytics、品牌可见度、情绪、位置、来源和竞品 benchmark。",
            benchmark_signal="可见度指标 + 竞品 benchmark + action 建议。",
            what_it_proves="海外产品已把品牌可见度、竞品、来源和行动建议做成平台能力。",
            what_it_does_not_prove="不能证明本项目已具备同等产品能力。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="Scrunch",
            market="海外",
            source_title="Scrunch",
            source_url="https://scrunch.com/faqs/",
            focus="AI search monitoring、AEO/GEO audit、optimization、agent traffic/referral tracking。",
            benchmark_signal="监测 + 审计 + 优化 + AI agent traffic/referral 数据。",
            what_it_proves="海外成熟竞品已把 prompt、presence、citation、referral traffic 组合成完整监测框架。",
            what_it_does_not_prove="不能证明本项目第一版需要完整复制这些能力。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="Otterly.AI",
            market="海外",
            source_title="Otterly AI",
            source_url="https://otterly.ai/",
            focus="ChatGPT、Google AI Overviews/AI Mode、Gemini、Perplexity、Copilot 的品牌覆盖和竞品 share of voice。",
            benchmark_signal="多平台品牌覆盖率 + 竞品 share of voice。",
            what_it_proves="海外存在偏轻量、面向 SEO/营销团队的 AI visibility tracker。",
            what_it_does_not_prove="不能证明服务化交付利润成立。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="Goodie",
            market="海外",
            source_title="Goodie",
            source_url="https://higoodie.com/pricing/",
            focus="品牌在 AI 搜索中的引用频率、排名位置、情绪和 share of voice。",
            benchmark_signal="GEO 指标产品化 + 定价参照。",
            what_it_proves="AI visibility 可被拆成可监测指标并作为 SaaS/服务销售。",
            what_it_does_not_prove="不能证明本项目高 ROI 已成立。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
        competitor_benchmark_row(
            name="Evertune",
            market="海外",
            source_title="Evertune",
            source_url="https://www.evertune.ai/",
            focus="AI brand monitoring、AI search optimization、品牌在 LLM 响应中的推荐和提及监测。",
            benchmark_signal="品牌监测 + AI search optimization。",
            what_it_proves="海外已有围绕 AI 品牌监测和优化的 SaaS 公司。",
            what_it_does_not_prove="不能证明国内 GEO 产品化速度或定价。",
            prd_usage="competitor_reference",
            fetch_external=fetch_external,
        ),
    ]
    china_count = sum(1 for row in rows if row["market"] == "中国")
    international_count = sum(1 for row in rows if row["market"] == "海外")
    return {
        "status": "available",
        "scope": "GEO / AI search visibility / AI brand monitoring 国内外竞品标杆。",
        "coverage": {"china_count": china_count, "international_count": international_count},
        "rows": rows,
        "decision_rule": "竞品只能证明赛道和能力形态存在，不能单独证明本项目商业价值、利润或 ROI 成立；是否值得做仍必须由付款、ROI、获客、交付、复购和资源优势证据决定。",
        "prd_usage_rule": "PRD 可引用竞品作为市场和能力参照，但不得把竞品存在写成本项目必然盈利、必然高 ROI 或完整 SaaS 已成立。",
    }


def build_evidence_ledger(project_id: str, raw_text: str, facts: list[str], *, fetch_external: bool = False) -> list[dict]:
    ledger: list[dict] = []
    local_source = f"projects/{project_id}/00_raw_input.md"
    if contains_any(raw_text, ("MVP 实验", "做过MVP", "做过 MVP", "MVP实验")):
        ledger.append(
            evidence_entry(
                claim="用户声明已经完成过 MVP 实验。",
                source_type="user_provided_fact",
                source_title="项目原始输入",
                source_url=local_source,
                confidence="high_user_claim",
                prd_usage="safe_fact_with_user_source",
                note="可作为业务方声明事实写入 PRD，但不得伪装为外部独立验证。",
            )
        )
    if contains_any(raw_text, ("同行已经为 GEO 服务买单", "同行已经买单", "真实支付", "签合同", "复购")):
        ledger.append(
            evidence_entry(
                claim="用户声明已有同行或客户为相关服务买单。",
                source_type="user_provided_fact",
                source_title="项目原始输入",
                source_url=local_source,
                confidence="high_user_claim",
                prd_usage="safe_fact_with_user_source",
                note="证明服务价值有强信号；不能直接证明完整 SaaS 产品化已经成立。",
            )
        )
    if is_geo_context(raw_text):
        ledger.extend(
            [
                evidence_entry(
                    claim="Gartner 预测到 2026 年传统搜索量将下降 25%，搜索营销会被 AI chatbots 和虚拟代理分流。",
                    source_type="external_public_source",
                    source_title="Gartner search volume forecast",
                    source_url="https://www.gartner.com/en/newsroom/press-releases/2024-02-19-gartner-predicts-search-engine-volume-will-drop-25-percent-by-2026-due-to-ai-chatbots-and-other-virtual-agents",
                    confidence="industry_research_source",
                    prd_usage="safe_fact_with_external_source",
                    note="证明搜索行为迁移趋势和营销渠道调整压力，不证明具体 GEO 项目一定有利润。",
                ),
                evidence_entry(
                    claim="Bain 引用 Sensor Tower 数据显示 2025 年上半年 ChatGPT prompt 量增长近 70%，购物相关 prompts 在占比和绝对量上明显增长。",
                    source_type="external_public_source",
                    source_title="Bain AI Search Research",
                    source_url="https://www.bain.com/insights/how-customers-are-using-ai-search/",
                    confidence="consulting_research_source",
                    prd_usage="safe_fact_with_external_source",
                    note="证明用户正在把 AI 用于搜索、购物和链接点击，不证明客户会为本 GEO 服务持续付费。",
                ),
                evidence_entry(
                    claim="公开 GEO agency pricing 资料显示，GEO 服务常见月费区间约为 3,000-25,000 美元。",
                    source_type="external_public_source",
                    source_title="RevvGrowth GEO pricing guide",
                    source_url="https://www.revvgrowth.com/geo/geo-agency-pricing",
                    confidence="market_pricing_reference",
                    prd_usage="assumption_or_inference_only",
                    note="只能作为海外服务价格锚点，不能直接证明国内客户可接受同等价格或 ROI。",
                ),
                evidence_entry(
                    claim="Goodie 将 AI search visibility 定义为品牌被 ChatGPT、Perplexity、Gemini 等 AI 搜索引用的频率，并跟踪引用频率、排名位置、情绪和 share of voice。",
                    source_type="external_public_source",
                    source_title="Goodie pricing and FAQ",
                    source_url="https://higoodie.com/pricing/",
                    confidence="competitor_product_source",
                    prd_usage="safe_fact_with_external_source",
                    note="证明竞品已经把 AI 可见度指标产品化，不证明本项目已有同等产品化能力。",
                ),
                evidence_entry(
                    claim="SEORCE 定义 prompt tracking 为监测 ChatGPT、Gemini、Perplexity、Google AI 中品牌或 URL 是否出现在回答里，并提供面向个人站点的低价 Lite 计划。",
                    source_type="external_public_source",
                    source_title="SEORCE pricing",
                    source_url="https://seorce.com/pricing",
                    confidence="competitor_product_source",
                    prd_usage="safe_fact_with_external_source",
                    note="证明 AI visibility 监测已有 SaaS 化和低价入口形态，不证明服务化交付利润更高。",
                ),
                evidence_entry(
                    claim="DeepSeek 有公开官方服务和 API 文档，是 GEO 监测可覆盖的 AI 平台之一。",
                    source_type="external_public_source",
                    source_title="DeepSeek API Docs",
                    source_url="https://api-docs.deepseek.com/api/deepseek-api/",
                    confidence="official_source",
                    prd_usage="safe_fact_with_external_source",
                    note="只证明平台和官方文档存在，不证明客户需求或商业价值成立。",
                ),
                evidence_entry(
                    claim="豆包有公开 AI 助手入口，是 GEO 监测可覆盖的 AI 平台之一。",
                    source_type="external_public_source",
                    source_title="豆包官网",
                    source_url="https://www.doubao.com/chat/",
                    confidence="official_source",
                    prd_usage="safe_fact_with_external_source",
                    note="只证明平台入口存在，不证明 GEO 服务商业化成立。",
                ),
                evidence_entry(
                    claim="Qwen 官方页面将 Qwen Studio 定位为面向用户的 AI assistant。",
                    source_type="external_public_source",
                    source_title="Qwen Chat",
                    source_url="https://qwen.ai/qwenchat",
                    confidence="official_source",
                    prd_usage="safe_fact_with_external_source",
                    note="只证明平台和产品定位存在，不证明 GEO 服务商业化成立。",
                ),
                evidence_entry(
                    claim="腾讯元宝官网将元宝描述为可问答和创作的智能助手。",
                    source_type="external_public_source",
                    source_title="腾讯元宝官网",
                    source_url="https://yuanbao.tencent.com/",
                    confidence="official_source",
                    prd_usage="safe_fact_with_external_source",
                    note="只证明平台和产品定位存在，不证明 GEO 服务商业化成立。",
                ),
            ]
        )
    for fact in facts:
        if not any(entry["claim"] == fact for entry in ledger) and contains_any(fact, ("可以先用", "证明", "初步信号")):
            ledger.append(
                evidence_entry(
                    claim=fact,
                    source_type="inference",
                    source_title="价值门禁规则推断",
                    source_url="",
                    confidence="derived",
                    prd_usage="assumption_or_inference_only",
                    note="只能作为推论，不能在 PRD 中写成已验证事实。",
                )
            )
    if not ledger:
        ledger.append(
            evidence_entry(
                claim="用户已提交原始想法或需求描述，但其中商业事实仍需继续验证。",
                source_type="user_provided_fact",
                source_title="项目原始输入",
                source_url=local_source,
                confidence="context_only",
                prd_usage="context_only_not_prd_fact",
                note="只能证明用户提出过该想法，不能证明商业价值、付费、利润或产品化成立。",
            )
        )
    return apply_external_evidence_fetch(ledger, enabled=fetch_external)


def safe_facts_from_ledger(ledger: list[dict]) -> list[str]:
    return [
        entry["claim"]
        for entry in ledger
        if entry.get("source_type") in {"user_provided_fact", "external_public_source", "internal_project_evidence"}
        and entry.get("prd_usage", "").startswith("safe_fact")
    ]


def evidence_strength_for_decision(entry: dict) -> str:
    source_type = entry.get("source_type")
    confidence = entry.get("confidence", "")
    if source_type == "user_provided_fact" and "high" in confidence:
        return "A：强业务事实（用户提供，仍需附件 / 记录复核）"
    if source_type == "internal_project_evidence":
        return "A：内部项目证据"
    if source_type == "external_public_source" and confidence == "official_source":
        return "C：外部官方事实"
    if source_type == "external_public_source" and confidence == "industry_research_source":
        return "B：行业趋势证据"
    if source_type == "external_public_source" and confidence == "consulting_research_source":
        return "B：用户行为趋势证据"
    if source_type == "external_public_source" and confidence == "market_pricing_reference":
        return "B：价格锚点证据"
    if source_type == "external_public_source" and confidence == "competitor_product_source":
        return "B：竞品产品化证据"
    if source_type == "inference":
        return "D：推理判断"
    if source_type == "unsupported_claim":
        return "D：无来源声明"
    return "C：上下文证据"


def evidence_proves_and_limits(entry: dict) -> tuple[str, str]:
    claim = entry.get("claim", "")
    note = entry.get("note", "")
    if "MVP" in claim:
        return (
            "证明不是纯想法，已经有初步实验或试跑基础。",
            "不能证明可规模化、可复购、真实利润成立或 SaaS 产品化成立。",
        )
    if "买单" in claim or "付费" in claim:
        return (
            "证明存在真实付费信号或预算意愿，商业价值不是零。",
            "不能证明客单价、复购、获客成本、交付工时、毛利或 SaaS 产品化已经成立。",
        )
    if any(platform in claim for platform in ("DeepSeek", "豆包", "Qwen", "腾讯元宝")):
        return (
            "证明 GEO 监测对象真实存在，PRD 可以把这些平台作为检测范围候选。",
            "不能证明客户一定愿意持续付费，也不能证明 GEO 服务商业化成立。",
        )
    if "Gartner" in claim:
        return (
            "证明传统搜索流量可能被 AI 助手分流，企业搜索营销预算存在被重新配置的外部压力。",
            "不能证明你的 GEO 服务一定能获客、成交、盈利或取得高 ROI。",
        )
    if "Bain" in claim:
        return (
            "证明用户正在把 AI 用于搜索、购物和链接点击，品牌需要关注 AI 搜索可见度。",
            "不能证明国内目标客户愿意持续付费，也不能证明单个 GEO 项目的投产比。",
        )
    if "月费区间" in claim or "3,000-25,000" in claim:
        return (
            "证明海外 GEO 服务存在公开价格锚点，可用于设计本项目价格验证区间。",
            "不能证明国内客户接受同等价格，也不能证明在本团队交付成本下 ROI 高。",
        )
    if "Goodie" in claim:
        return (
            "证明 AI search visibility 已被竞品拆成引用频率、排名位置、情绪、share of voice 等可产品化指标。",
            "不能证明本项目已具备同等产品能力，也不能证明客户会为本项目复购。",
        )
    if "SEORCE" in claim:
        return (
            "证明 AI tracking 已出现 SaaS 化低价入口，说明该方向有工具化竞争形态。",
            "不能证明服务化交付利润更高，也不能证明应立即重研发完整平台。",
        )
    if entry.get("source_type") == "external_public_source":
        return ("证明相关外部对象或公开资料存在。", note or "不能直接证明商业价值成立。")
    if entry.get("source_type") == "inference":
        return ("提供判断线索。", "只能作为推论，不能写成已验证事实。")
    return ("提供上下文事实。", note or "不能单独证明完整商业价值成立。")


def build_evidence_decision_basis(ledger: list[dict]) -> list[dict]:
    basis = []
    for entry in ledger:
        proves, does_not_prove = evidence_proves_and_limits(entry)
        if entry.get("source_type") == "unsupported_claim":
            decision_impact = "阻止进入事实层，只能进入假设或禁止声称。"
        elif "买单" in entry.get("claim", "") or "MVP" in entry.get("claim", ""):
            decision_impact = "支持“值得测试 / 服务化 MVP”，但不足以支持直接完整 SaaS。"
        elif any(token in entry.get("claim", "") for token in ("Gartner", "Bain", "月费区间", "Goodie", "SEORCE")):
            decision_impact = "支持“值得服务化 MVP 验证”，但 ROI 仍必须用价格、成本、复购和获客数据证明。"
        elif entry.get("source_type") == "external_public_source":
            decision_impact = "支持“场景对象真实存在”，不直接支持“商业价值已成立”。"
        elif entry.get("source_type") == "inference":
            decision_impact = "只支持待验证判断，不作为拍板事实。"
        else:
            decision_impact = "提供上下文支撑，需要结合其他证据判断。"
        basis.append(
            {
                "evidence": entry.get("claim", ""),
                "source_type": entry.get("source_type", ""),
                "source_title": entry.get("source_title", ""),
                "source_url": entry.get("source_url", ""),
                "captured_at": entry.get("captured_at", ""),
                "fetch_status": entry.get("fetch_status", ""),
                "checked_at": entry.get("checked_at", ""),
                "http_status": entry.get("http_status"),
                "retrieved_title": entry.get("retrieved_title", ""),
                "evidence_excerpt": entry.get("evidence_excerpt", ""),
                "strength": evidence_strength_for_decision(entry),
                "proves": proves,
                "does_not_prove": does_not_prove,
                "decision_impact": decision_impact,
            }
        )
    return basis


def build_evidence_to_verdict_reasoning(worth: dict, evidence_basis: list[dict]) -> dict:
    supports = [item["evidence"] for item in evidence_basis if "支持" in item.get("decision_impact", "")]
    limits = unique_list(item["does_not_prove"] for item in evidence_basis if item.get("does_not_prove"))
    return {
        "verdict": worth.get("verdict"),
        "plain_conclusion": worth.get("plain_conclusion"),
        "why_this_verdict_is_allowed": supports[:6] or [item["evidence"] for item in evidence_basis[:3]],
        "why_bigger_scope_is_not_allowed": unique_list(list(worth.get("critical_gaps", [])) + limits)[:8],
        "evidence_rule": "没有来源的数据不能进入结论；用户提供事实必须标注来源；外部公开事实可以证明趋势、价格锚点、竞品形态或监测对象存在，但不能单独证明本项目利润和高 ROI 已成立。",
    }


def allowed_prd_type_for_decision(decision: str) -> str:
    return VALUE_GATE_ALLOWED_PRD_TYPE.get(decision, "不允许生成 PRD")


def build_evidence_sufficiency_gate(
    *,
    raw_text: str,
    decision: str,
    evidence_level: str,
    payment_level: int,
    completeness: dict,
    redlines: list[str],
    scorecard: list[dict],
    evidence_basis: list[dict],
) -> dict:
    missing_evidence_types: list[str] = []
    if payment_level < 4:
        missing_evidence_types.append("商业价值证据")
    if evidence_level in {"C", "D"}:
        missing_evidence_types.append("需求证据")
    if completeness.get("missing_count", 0) >= 2:
        missing_evidence_types.extend(["需求证据", "经营证据"])
    if not contains_any(raw_text, ("客单价", "获客成本", "交付工时", "复购周期", "维护成本", "毛利", "利润")):
        missing_evidence_types.append("经营证据")
    if not contains_any(raw_text, ("多个相似客户", "第二个客户", "多客户", "标准化", "边际成本下降", "可复用", "复购", "续费")):
        missing_evidence_types.append("产品化证据")
    if redlines:
        missing_evidence_types.append("红线证据")
    missing_evidence_types = unique_list(missing_evidence_types)

    must_not_claim = [
        "不得把服务化 MVP 证据写成完整 SaaS 产品化已经成立。",
        "不得把用户提供的买单事实伪装成外部验证。",
        "不得把平台存在性证据写成客户愿意持续付费。",
        "不得把未验证价格、成本、复购、获客写成事实。",
    ]
    next_evidence = [
        "真实付款 / 合同 / 明确预算 / 复购记录",
        "客单价或价格区间",
        "获客成本和第一批客户来源",
        "单客户交付工时和人工复核成本",
        "复购周期、复测意愿或续费证据",
        "多客户相似需求和标准化交付证据",
        "合规、隐私、平台规则边界",
    ]

    if redlines or decision == "G_BLOCKED_BY_REDLINE":
        return {
            "overall_status": "blocked_by_redline",
            "supported_paths": ["风险复核"],
            "unsupported_paths": ["完整 PRD", "MVP", "客户项目验证", "开发排期"],
            "missing_evidence_types": unique_list(missing_evidence_types),
            "downgrade_reason": "存在红线风险，不能用商业价值证据覆盖合规、隐私、行业或平台规则风险。",
            "must_not_claim": must_not_claim + ["红线未解除前不得声称可以安全推进。"],
            "next_evidence_to_collect": ["红线风险专业确认", "合规边界", "责任边界", "数据和平台规则证明"],
        }
    if decision == "F_NOT_RECOMMENDED":
        return {
            "overall_status": "insufficient_stop",
            "supported_paths": ["停止", "低成本复判"],
            "unsupported_paths": ["完整 PRD", "MVP", "客户项目验证", "开发排期"],
            "missing_evidence_types": unique_list(missing_evidence_types),
            "downgrade_reason": "当前证据无法证明价值、利润、获客或交付条件成立。",
            "must_not_claim": must_not_claim + ["不得声称该方向已经值得投入产品开发。"],
            "next_evidence_to_collect": next_evidence[:5],
        }
    if decision == "E_RESEARCH_REQUIRED":
        return {
            "overall_status": "research_required",
            "supported_paths": ["调研补全"],
            "unsupported_paths": ["完整 PRD", "MVP 开发", "开发排期"],
            "missing_evidence_types": unique_list(missing_evidence_types or ["需求证据", "商业价值证据", "经营证据"]),
            "downgrade_reason": "关键信息或证据类型不足，只能证明方向可能存在，不能证明值得进入开发。",
            "must_not_claim": must_not_claim + ["不得把调研假设写成已验证事实。"],
            "next_evidence_to_collect": next_evidence,
        }
    if decision == "C_CLIENT_PROJECT_VALIDATION":
        return {
            "overall_status": "sufficient_for_client_project",
            "supported_paths": ["客户项目验证", "服务交付验证"],
            "unsupported_paths": ["完整 SaaS PRD", "规模化产品化判断"],
            "missing_evidence_types": unique_list(missing_evidence_types or ["产品化证据"]),
            "downgrade_reason": "付款或项目价值可以支持客户项目验证，但单客户强定制不能直接证明通用产品化。",
            "must_not_claim": must_not_claim + ["不得把单客户定制写成通用产品需求已经成立。"],
            "next_evidence_to_collect": ["第二个相似客户", "可标准化范围", "边际交付成本", "复用组件", "复购或续费"],
        }
    if decision == "D_INTERNAL_EFFICIENCY":
        return {
            "overall_status": "sufficient_for_internal_efficiency",
            "supported_paths": ["内部提效验证"],
            "unsupported_paths": ["对外商业 PRD", "完整 SaaS PRD"],
            "missing_evidence_types": unique_list(missing_evidence_types or ["外部商业价值证据"]),
            "downgrade_reason": "内部降本增效证据不能直接证明外部付费或产品化价值。",
            "must_not_claim": must_not_claim + ["不得把内部效率价值写成外部客户愿意买单。"],
            "next_evidence_to_collect": ["节省工时", "错误率下降", "建设维护成本", "内部推广阻力", "是否存在外部付费对象"],
        }
    if decision == "B_LOW_COST_MVP":
        if is_geo_context(raw_text):
            downgrade_reason = "已有 MVP 和买单信号支持服务化 MVP / 客户项目验证，但客单价、获客成本、交付工时、复购周期、多客户复用和 SaaS 产品化证据不足。"
            supported = ["服务化 MVP", "客户项目验证"]
            unsupported = ["完整 SaaS PRD", "重研发自动化平台", "规模化产品化判断"]
            missing = unique_list(["经营证据", "产品化证据"] + missing_evidence_types)
            next_items = [
                "真实付款 / 合同 / 明确预算附件或记录",
                "首期服务价格区间",
                "外部价格锚点与国内目标行业可接受价格对比",
                "单客户交付工时",
                "单客户 ROI 计算：收入 - 获客成本 - 交付成本 - 工具成本 - 维护成本",
                "复购 / 复测 / 续费意愿",
                "获客成本和第一批行业来源",
                "多客户相似需求",
                "GEO 指标复测变化和归因材料",
            ]
        else:
            downgrade_reason = "当前证据足够支持低成本 MVP 验证，但不足以支持完整 PRD 或重研发。"
            supported = ["低成本 MVP"]
            unsupported = ["完整 PRD", "重研发"]
            missing = missing_evidence_types or ["商业价值证据", "经营证据", "产品化证据"]
            next_items = next_evidence
        return {
            "overall_status": "sufficient_for_mvp",
            "supported_paths": supported,
            "unsupported_paths": unsupported,
            "missing_evidence_types": unique_list(missing),
            "downgrade_reason": downgrade_reason,
            "must_not_claim": must_not_claim,
            "next_evidence_to_collect": next_items,
        }

    blocking_scorecard = [item for item in scorecard if item.get("status") in {"Fail", "Blocked"}]
    if decision == VALUE_GATE_ALLOW_PRD and not blocking_scorecard:
        return {
            "overall_status": "sufficient_for_full_prd",
            "supported_paths": ["完整 PRD"],
            "unsupported_paths": ["无证据支持的规模化承诺", "绕过人工确认的开发排期"],
            "missing_evidence_types": unique_list(missing_evidence_types),
            "downgrade_reason": "",
            "must_not_claim": must_not_claim,
            "next_evidence_to_collect": unique_list(next_evidence),
        }
    return {
        "overall_status": "research_required",
        "supported_paths": ["调研补全"],
        "unsupported_paths": ["完整 PRD", "MVP 开发", "开发排期"],
        "missing_evidence_types": unique_list(missing_evidence_types or ["商业价值证据", "经营证据"]),
        "downgrade_reason": "证据门禁无法证明当前结论足够可靠，必须降级为调研补全。",
        "must_not_claim": must_not_claim,
        "next_evidence_to_collect": next_evidence,
    }


def build_evidence_grade_gate(
    *,
    decision: str,
    evidence_level: str,
    payment_level: int,
    evidence_basis: list[dict],
    sufficiency_gate: dict,
) -> dict:
    grade_counts = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0}
    for item in evidence_basis:
        strength = item.get("strength", "")
        if strength.startswith("A"):
            grade_counts["A"] += 1
        elif strength.startswith("B"):
            grade_counts["B"] += 1
        elif strength.startswith("C"):
            grade_counts["C"] += 1
        elif strength.startswith("D"):
            grade_counts["D"] += 1
    if payment_level >= 5:
        grade_counts["S"] += 1

    required_by_decision = {
        VALUE_GATE_ALLOW_PRD: "A 级以上证据，且真实利润、获客、风险和输入包完整度达标。",
        "B_LOW_COST_MVP": "B 级或 C+ 级证据即可，但必须有清晰核心假设和核心价值闭环。",
        "C_CLIENT_PROJECT_VALIDATION": "必须有明确客户、明确场景、明确付费或预算意向。",
        "D_INTERNAL_EFFICIENCY": "必须有明确内部流程、效率损耗、成本损耗或风险损耗。",
        "E_RESEARCH_REQUIRED": "C/D 级证据或关键价值信息缺失，只能调研补全。",
        "F_NOT_RECOMMENDED": "价值对象不成立、利润不真实、获客困难或交付过重时停止。",
        "G_BLOCKED_BY_REDLINE": "触发不可控红线时禁止推进。",
    }
    full_prd_gaps = list(sufficiency_gate.get("missing_evidence_types", []))
    if payment_level < 5:
        full_prd_gaps.append("S 级付款 / 合同 / 复购 / 使用数据证据")
    if grade_counts["B"] and not grade_counts["A"]:
        full_prd_gaps.append("外部趋势和竞品证据不能替代自身商业证据")
    if decision != VALUE_GATE_ALLOW_PRD:
        full_prd_gaps.append("当前 decision_gate 不是 A_ENTER_PRD")
    full_prd_gaps = unique_list(full_prd_gaps)

    if decision == VALUE_GATE_ALLOW_PRD and not full_prd_gaps:
        current_grade = evidence_level
        status = "passes_current_gate"
    elif decision in {"B_LOW_COST_MVP", "C_CLIENT_PROJECT_VALIDATION", "D_INTERNAL_EFFICIENCY"}:
        current_grade = "S/A + B" if grade_counts["S"] or grade_counts["A"] else evidence_level
        status = "passes_current_gate_but_not_full_prd"
    elif decision == "E_RESEARCH_REQUIRED":
        current_grade = "C/D"
        status = "research_required"
    elif decision == "F_NOT_RECOMMENDED":
        current_grade = evidence_level or "D"
        status = "insufficient_stop"
    else:
        current_grade = evidence_level or "D"
        status = "blocked_by_redline"

    return {
        "status": status,
        "current_grade": current_grade,
        "payment_evidence_level": payment_level,
        "grade_counts": grade_counts,
        "minimum_required_for_current_gate": required_by_decision.get(decision, "需要人工复核当前路径证据门槛。"),
        "meets_current_gate": status in {"passes_current_gate", "passes_current_gate_but_not_full_prd"},
        "full_prd_requirement": "A_ENTER_PRD 至少需要 A 级证据或 B 级证据 + 明确低风险 + 明确资源优势，同时真实利润、获客路径、红线和输入包完整度达标。",
        "full_prd_gap": full_prd_gaps,
        "upgrade_evidence_required": [
            "付款 / 合同 / 明确预算附件",
            "第二个相似客户或复购 / 复测证据",
            "客单价和获客成本",
            "单客户交付工时和工具成本",
            "可标准化交付流程和边际成本下降证据",
        ],
        "downgrade_rule": "如果证据只能证明趋势、竞品存在或用户兴趣，不能进入 A；只能进入 MVP、客户项目、内部提效或调研路径。",
    }


def build_roi_decision_model(
    *, true_profit: dict, operating_model: dict, evidence_sufficiency_gate: dict, evidence_grade_gate: dict, roi_input_table: dict
) -> dict:
    unknowns = unique_list(
        list(operating_model.get("unknowns_that_block_scaling", []))
        + list(true_profit.get("missing_cost_items", []))
        + list(evidence_sufficiency_gate.get("missing_evidence_types", []))
        + list(roi_input_table.get("missing_critical_inputs", []))
    )
    can_calculate = roi_input_table.get("can_calculate_roi") is True and not any(
        item in unknowns for item in ("客单价", "获客成本", "交付成本", "单客户交付工时")
    )
    scenarios = []
    for name, rule in [
        ("保守", "按最低可接受客单价、最高获客成本和最高交付工时计算。"),
        ("中性", "按目标客单价、可控获客成本和可复用交付流程计算。"),
        ("乐观", "按复购 / 转介绍成立、边际交付成本下降后计算。"),
    ]:
        scenarios.append(
            {
                "scenario": name,
                "calculation_rule": rule,
                "revenue": "待确认",
                "acquisition_cost": "待确认",
                "delivery_cost": "待确认",
                "tool_cost": "待确认",
                "maintenance_cost": "待确认",
                "estimated_profit": "不可计算，缺少真实数值",
                "roi_status": "not_proven",
                "required_evidence": ["客单价", "获客成本", "单客户交付工时", "工具成本", "维护 / 售后成本"],
            }
        )
    return {
        "status": "roi_not_proven" if not can_calculate else "roi_calculable",
        "can_claim_high_roi": False if not can_calculate else None,
        "formula": "ROI = (收入 - 获客成本 - 交付成本 - 人工成本 - 工具成本 - 维护 / 售后成本 - 风险成本) / 总投入",
        "roi_input_table_status": roi_input_table.get("status", ""),
        "scenario_table": scenarios,
        "minimum_data_needed": [
            "首期服务价格或报告价格",
            "单个有效线索获客成本",
            "单客户交付工时",
            "人工复核和报告修订成本",
            "工具 / 模型 / 看板成本",
            "复购、复测或代运营续费证据",
        ],
        "decision_effect": "当前不能声称高 ROI，只能用服务化 MVP 收集 ROI 所需数据。",
        "upgrade_condition": "三档 ROI 中至少中性场景可盈利，且复购或第二客户信号出现后，才允许讨论产品化放大。",
        "stop_condition": "保守和中性场景都无法覆盖获客、交付、工具和维护成本时，停止产品化或降级为服务项目。",
        "evidence_grade_dependency": evidence_grade_gate.get("status", ""),
    }


def build_real_profit_calculation(roi_input_table: dict, verified_assessment: dict) -> dict:
    missing = roi_input_table.get("missing_critical_inputs", [])
    can_calculate = roi_input_table.get("can_calculate_roi") is True and not missing
    known_inputs = [
        {
            "key": row.get("key", ""),
            "label": row.get("label", ""),
            "value": row.get("current_value", ""),
            "source_status": row.get("source_status", ""),
        }
        for row in roi_input_table.get("input_rows", [])
        if row.get("source_status") != "missing"
    ]
    return {
        "status": "calculable" if can_calculate else "missing_required_inputs",
        "can_calculate": can_calculate,
        "formula": "真实利润 = 客单价 - 获客成本 - 交付工时成本 - 人工复核成本 - 工具/模型成本 - 维护/售后成本 - 风险成本",
        "known_inputs": known_inputs,
        "missing_inputs": missing,
        "verified_evidence_level": verified_assessment.get("status", ""),
        "minimum_profit_condition": "至少基准场景为正毛利，且服务交付不依赖不可复制的专家工时。",
        "conclusion": "缺少关键 ROI 输入，不能证明高 ROI。" if not can_calculate else "具备计算条件，但是否正 ROI 仍需人工复核具体数值。",
    }


def build_roi_scenario_analysis(roi_input_table: dict, real_profit_calculation: dict) -> dict:
    can_calculate = real_profit_calculation.get("can_calculate") is True
    scenarios = []
    for scenario, assumption in [
        ("保守场景", "按最低客单价、最高获客成本、最高交付工时和最高维护成本估算。"),
        ("基准场景", "按当前最可能成交价格、可控获客成本和可复用交付流程估算。"),
        ("乐观场景", "按复购 / 转介绍出现、边际交付成本下降后估算。"),
    ]:
        scenarios.append(
            {
                "scenario": scenario,
                "assumption": assumption,
                "revenue": "待确认" if not can_calculate else "需代入已复核客单价",
                "total_cost": "待确认" if not can_calculate else "需代入已复核成本",
                "gross_profit": "待确认" if not can_calculate else "待人工计算",
                "roi_status": "not_calculable" if not can_calculate else "manual_review_required",
                "decision_effect": "不能支持高 ROI 或产品化升级" if not can_calculate else "可进入 ROI 人工复核",
            }
        )
    return {
        "status": "roi_unavailable_missing_inputs" if not can_calculate else "roi_manual_review_required",
        "scenarios": scenarios,
        "missing_inputs": real_profit_calculation.get("missing_inputs", []),
        "rule": "没有客单价、获客成本、交付工时、工具成本、维护成本和复购信号时，不允许声称 ROI 很高。",
    }


def build_investment_decision_gate(roi_scenario_analysis: dict, rejudgment_gate: dict, s_verified_gate: dict) -> dict:
    if s_verified_gate.get("current_level") != "S_verified":
        conclusion = "roi_unavailable_missing_inputs"
        reason = "强业务证据尚未从 S_claimed 升级到 S_verified。"
    elif roi_scenario_analysis.get("status") == "roi_unavailable_missing_inputs":
        conclusion = "roi_unavailable_missing_inputs"
        reason = "ROI 关键输入缺失。"
    elif rejudgment_gate.get("productization_ready"):
        conclusion = "roi_positive_productization_candidate"
        reason = "材料显示付款、服务闭环、ROI 输入和复购 / 转介绍均已满足产品化复判候选。"
    elif rejudgment_gate.get("roi_ready"):
        conclusion = "roi_positive_client_project"
        reason = "材料足以支持客户项目 / 服务化 MVP 的 ROI 复判，但产品化证据仍不足。"
    else:
        conclusion = "roi_possible_service_mvp"
        reason = "可继续服务化 MVP 收集 ROI 数据。"
    return {
        "conclusion": conclusion,
        "reason": reason,
        "allowed_next_path": "服务化 MVP / 客户项目验证" if conclusion != "roi_positive_productization_candidate" else "产品化候选复判",
        "blocked_paths": ["完整 SaaS PRD", "重研发自动化平台", "高 ROI 对外承诺"] if conclusion != "roi_positive_productization_candidate" else ["自动进入 stable / 自动开完整 SaaS"],
        "requires_owner_approval": True,
        "rule": "投资结论只作为 value gate 复判输入；升级完整 PRD、SaaS、stable 或重研发必须用户拍板。",
    }


def build_route_decision(
    *,
    decision: str,
    allowed_prd_type: str,
    execution_status: str,
    can_enter_full_prd: bool,
    path_recommendation: dict,
    business_worth_verdict: dict,
    evidence_sufficiency_gate: dict,
    material_intake_summary: dict,
    roi_scenario_analysis: dict,
    investment_decision_gate: dict,
    route_package_completeness_gate: dict,
) -> dict:
    route_package = VALUE_GATE_ROUTE_PACKAGE[decision]
    return {
        "canonical_decision": decision,
        "recommended_path": path_recommendation.get("recommended_path") or allowed_prd_type,
        "allowed_prd_type": allowed_prd_type,
        "can_enter_full_prd": can_enter_full_prd,
        "execution_status": execution_status,
        "downstream_input_package": route_package,
        "next_module": VALUE_GATE_NEXT_MODULE[decision],
        "business_worth": business_worth_verdict.get("verdict"),
        "evidence_sufficiency": evidence_sufficiency_gate.get("overall_status"),
        "material_status": material_intake_summary.get("status"),
        "roi_status": roi_scenario_analysis.get("status"),
        "route_package_status": route_package_completeness_gate.get("status"),
        "owner_decision_required": bool(investment_decision_gate.get("requires_owner_approval")),
        "allowed_paths": path_recommendation.get("allowed_paths", []),
        "deferred_paths": path_recommendation.get("deferred_paths", []),
        "blocked_paths": path_recommendation.get("blocked_paths", []),
        "rule": "下游模块以 route_decision 为唯一主路由结论；decision_gate、execution_status、allowed_prd_type 只作为兼容和审计字段。",
    }


def build_route_package_completeness_gate(route_package_name: str, route_package: dict) -> dict:
    required_by_route = {
        "mvp_input_package": [
            "core_user",
            "core_scenario",
            "core_task",
            "core_features",
            "core_delivery",
            "core_feedback",
            "minimum_data_loop",
            "success_criteria",
            "failure_criteria",
        ],
        "client_project_input_package": ["project_value", "service_value", "standardizable_parts", "customized_parts", "next_evidence"],
        "internal_efficiency_input_package": ["efficiency_value", "metrics", "validation_materials", "must_quantify"],
        "research_input_package": ["missing_or_unclear_items", "open_questions", "recommended_research", "research_outputs_required"],
        "stop_reason_package": ["blocked_reasons", "counter_evidence", "reopen_conditions"],
        "redline_block_package": ["red_line_risks", "required_confirmation"],
        "prd_input_package": ["product_summary", "value_judgment", "user_and_scenario", "business_model", "risk_and_constraints"],
    }
    required = required_by_route.get(route_package_name, [])
    missing = []
    over_generic = []
    specificity_checks = []
    for field in required:
        value = route_package.get(field)
        if value in (None, "", [], {}):
            missing.append(field)
        elif value == "待确认" or value == ["待验证"]:
            over_generic.append(field)
    if route_package_name == "mvp_input_package":
        required_terms = {
            "success_criteria": ["免费检测提交数", "有效线索率", "加顾问率", "体检报告成交率", "单客户交付工时", "复盘预约率", "后续优化", "代运营"],
            "failure_criteria": ["只愿免费", "报告", "交付工时", "无法归因", "复测", "复购"],
            "minimum_data_loop": ["品牌提及", "竞品提及", "引用来源", "诊断报告", "优化动作", "复测结果", "成交"],
        }
        for field, terms in required_terms.items():
            text = " ".join(str(item) for item in route_package.get(field, []))
            matched = [term for term in terms if term in text]
            missing_terms = [term for term in terms if term not in text]
            specificity_checks.append(
                {
                    "field": field,
                    "required_terms": terms,
                    "matched_terms": matched,
                    "missing_terms": missing_terms,
                    "status": "specific" if not missing_terms else "needs_specificity",
                }
            )
            if missing_terms and field not in over_generic:
                over_generic.append(field)
    status = "complete"
    if missing:
        status = "incomplete"
    elif over_generic:
        status = "needs_specificity"
    return {
        "route_package": route_package_name,
        "status": status,
        "required_fields": required,
        "missing_fields": missing,
        "over_generic_fields": over_generic,
        "specificity_checks": specificity_checks,
        "can_route_to_next_module": not missing,
        "fallback": "缺字段时退回前置模块补齐；字段过泛时允许进入验证路径，但不得进入完整 PRD。",
    }


def build_unsupported_claims(raw_text: str) -> list[str]:
    claims = [
        "完整 SaaS 产品化已经成立",
        "GEO 优化一定能提升 AI 推荐或排名",
        "AI 平台一定会稳定采纳优化内容",
        "同行买单可以直接证明规模化产品收入成立",
        "获客成本、交付工时、复购周期已经验证完成",
    ]
    if contains_any(raw_text, ("承诺", "保证", "稳赚", "排名第一")):
        claims.append("可以承诺确定性收益或确定性排名")
    return unique_list(claims)


def gate_item(key: str, status: str, reason: str, blocks_full_prd: bool, next_action: str) -> dict:
    return {
        "key": key,
        "label": VALUE_GATE_HARD_GATE_LABELS[key],
        "status": status,
        "reason": reason,
        "blocks_full_prd": blocks_full_prd,
        "next_action": next_action,
    }


def build_hard_gate_scorecard(
    *,
    raw_text: str,
    decision: str,
    evidence_level: str,
    payment_level: int,
    redlines: list[str],
    value_object_detail: dict,
    value_judgment: dict,
    measurability: dict,
    attribution: dict,
    true_profit: dict,
    acquisition: dict,
    resource_fit: dict,
    project_to_product: dict,
) -> list[dict]:
    scorecard = [
        gate_item(
            "value_object",
            "Pass" if has_specific_value(value_object_detail.get("payer")) and has_specific_value(value_object_detail.get("decision_maker")) else "Warning",
            "已识别付费者、决策者、使用者和潜在反对者。" if has_specific_value(value_object_detail.get("payer")) else "付费者或决策者仍不够明确。",
            False,
            "保持价值对象矩阵，PRD 不要混淆付费者、使用者和验收方。",
        ),
        gate_item(
            "business_result",
            "Pass" if has_specific_value(value_judgment.get("business_result")) else "Fail",
            f"商业结果为：{value_judgment.get('business_result') or '缺失'}。",
            not has_specific_value(value_judgment.get("business_result")),
            "把商业结果写成可验收指标，不写泛泛的“提升体验”。",
        ),
        gate_item(
            "metrics",
            "Pass" if has_specific_value(measurability.get("metrics")) else "Fail",
            "已给出可衡量指标。" if has_specific_value(measurability.get("metrics")) else "缺少可衡量指标。",
            not has_specific_value(measurability.get("metrics")),
            "补齐基线值、复测周期和指标口径。",
        ),
        gate_item(
            "attribution",
            "Warning" if attribution.get("attribution_risk") in {"中", "高"} else "Pass",
            f"归因风险：{attribution.get('attribution_risk') or '待验证'}。",
            False,
            "PRD 必须记录产品动作、服务动作、外部干扰和复测材料。",
        ),
        gate_item(
            "evidence_level",
            "Pass" if evidence_level in {"S", "A"} else ("Warning" if evidence_level in {"B", "C"} else "Fail"),
            f"证据等级为 {evidence_level}。",
            evidence_level == "D",
            "低于 A 级时，不得直接进入完整 PRD。",
        ),
        gate_item(
            "payment_evidence",
            "Pass" if payment_level >= 4 else ("Warning" if payment_level in {2, 3} else "Fail"),
            f"付费证据第 {payment_level} 层。",
            payment_level < 2,
            "确认真实付款、合同、预算或复购证据。",
        ),
        gate_item(
            "true_profit",
            "Warning" if contains_any(true_profit.get("next_calculation", ""), ("补齐", "核算")) else "Pass",
            true_profit.get("minimum_profit_condition") or "真实利润条件待验证。",
            False,
            "补齐客单价、获客成本、交付工时、人工复核和售后维护成本。",
        ),
        gate_item(
            "acquisition",
            "Warning" if "需要验证" in str(acquisition.get("cac_ltv_risk", "")) else ("Pass" if has_specific_value(acquisition.get("reach_method")) else "Fail"),
            acquisition.get("cac_ltv_risk") or acquisition.get("reach_method") or "获客路径待验证。",
            not has_specific_value(acquisition.get("reach_method")),
            "确认第一批用户、触达方式、信任来源和 CAC/LTV 风险。",
        ),
        gate_item(
            "resource_fit",
            "Warning" if resource_fit.get("missing_assets") else "Pass",
            f"可用资产：{'、'.join(resource_fit.get('available_assets', [])) or '待验证'}；缺失资产：{'、'.join(resource_fit.get('missing_assets', [])) or '无'}。",
            False,
            "把缺失资源转为 PRD 上线前拍板项。",
        ),
        gate_item(
            "productization",
            "Warning" if project_to_product.get("product_value") == "具备候选" or is_geo_context(raw_text) else ("Pass" if decision == VALUE_GATE_ALLOW_PRD else "Fail"),
            project_to_product.get("productization_risk") or "产品化价值待判断。",
            decision not in {VALUE_GATE_ALLOW_PRD, "C_CLIENT_PROJECT_VALIDATION"},
            "先区分项目价值、服务价值和完整 SaaS 产品化价值。",
        ),
        gate_item(
            "redline",
            "Blocked" if redlines else "Pass",
            "；".join(redlines) if redlines else "未识别到不可控红线，但仍需保留行业和平台规则边界。",
            bool(redlines),
            "红线不可控时禁止推进；可控时进入风险约束版路径。",
        ),
    ]
    if contains_any(raw_text, ("利润不成立", "获客成本长期高于客单价")) and payment_level < 4:
        for item in scorecard:
            if item["key"] == "true_profit":
                item.update(status="Fail", blocks_full_prd=True, reason="输入中存在利润不成立的当前负面信号。")
    return scorecard


def build_path_recommendation(raw_text: str, decision: str, redlines: list[str], scorecard: list[dict]) -> dict:
    if redlines or decision == "G_BLOCKED_BY_REDLINE":
        return {
            "recommended_path": "红线阻断",
            "allowed_paths": ["风险复核"],
            "deferred_paths": ["PRD", "MVP", "客户项目验证"],
            "blocked_paths": ["继续产品设计", "对外承诺", "开发排期"],
            "reason": "存在不可控红线或高风险声明，必须先完成专业确认。",
        }
    if is_geo_context(raw_text) and decision in {VALUE_GATE_ALLOW_PRD, "B_LOW_COST_MVP"}:
        return {
            "recommended_path": "服务化 MVP PRD",
            "allowed_paths": ["服务化 MVP", "客户项目验证", "PRD 小修订"],
            "deferred_paths": ["完整 SaaS PRD", "自动化平台建设"],
            "blocked_paths": ["承诺 AI 推荐结果", "黑灰产 GEO", "无验证直接重研发"],
            "reason": "已有 MVP 和买单信号，但真实利润、获客、交付成本和 SaaS 产品化仍需验证。",
        }
    by_decision = {
        "A_ENTER_PRD": ("完整 PRD", ["完整 PRD"], ["完整自动化平台建设"], ["绕过人工确认"]),
        "B_LOW_COST_MVP": ("低成本 MVP", ["低成本 MVP"], ["完整 PRD"], ["直接重研发"]),
        "C_CLIENT_PROJECT_VALIDATION": ("客户项目验证", ["客户项目验证"], ["完整产品化"], ["把单客户定制包装成通用产品"]),
        "D_INTERNAL_EFFICIENCY": ("内部提效方案", ["内部提效方案"], ["对外产品化"], ["未经验证对外销售"]),
        "E_RESEARCH_REQUIRED": ("调研补全", ["调研补全"], ["PRD", "MVP"], ["信息不足时直接开发"]),
        "F_NOT_RECOMMENDED": ("停止", ["复判"], ["PRD", "MVP"], ["继续投入开发"]),
    }
    recommended, allowed, deferred, blocked = by_decision.get(decision, by_decision["E_RESEARCH_REQUIRED"])
    return {
        "recommended_path": recommended,
        "allowed_paths": allowed,
        "deferred_paths": deferred,
        "blocked_paths": blocked,
        "reason": "根据当前门禁结论路由到对应验证路径。",
    }


def build_business_worth_verdict(raw_text: str, decision: str, path_recommendation: dict, scorecard: list[dict], safe_facts: list[str]) -> dict:
    fail_or_blocked = [item for item in scorecard if item.get("status") in {"Fail", "Blocked"}]
    warnings = [item for item in scorecard if item.get("status") == "Warning"]
    if decision == "G_BLOCKED_BY_REDLINE" or any(item.get("status") == "Blocked" for item in scorecard):
        return {
            "verdict": "blocked",
            "plain_conclusion": "不允许继续推进，必须先处理红线风险。",
            "worth_doing_scope": ["风险复核"],
            "not_worth_doing_scope": ["PRD", "MVP", "客户项目验证", "开发排期"],
            "confidence": "high",
            "evidence_basis": safe_facts,
            "critical_gaps": [item["reason"] for item in fail_or_blocked],
            "next_decision": "红线风险是否能被专业确认并降级为可控风险。",
        }
    if decision == "F_NOT_RECOMMENDED" or fail_or_blocked:
        return {
            "verdict": "not_worth_doing",
            "plain_conclusion": "当前不值得继续投入产品设计，除非关键反证被解决或出现新的强证据。",
            "worth_doing_scope": ["复判", "证据补充"],
            "not_worth_doing_scope": ["完整 PRD", "MVP", "开发排期"],
            "confidence": "medium_high",
            "evidence_basis": safe_facts,
            "critical_gaps": [item["reason"] for item in fail_or_blocked],
            "next_decision": "是否继续补证据，还是停止该方向。",
        }
    if decision == "E_RESEARCH_REQUIRED":
        return {
            "verdict": "worth_researching",
            "plain_conclusion": "方向可能有机会，但当前信息不足，只值得先做调研补全。",
            "worth_doing_scope": ["调研补全", "客户访谈", "付费验证"],
            "not_worth_doing_scope": ["完整 PRD", "MVP 开发", "开发排期"],
            "confidence": "medium",
            "evidence_basis": safe_facts,
            "critical_gaps": [item["reason"] for item in warnings] or ["关键价值信息仍需补齐。"],
            "next_decision": "是否先补齐目标用户、付费、成本、获客或风险材料。",
        }
    if is_geo_context(raw_text) and decision in {VALUE_GATE_ALLOW_PRD, "B_LOW_COST_MVP"}:
        return {
            "verdict": "worth_testing",
            "plain_conclusion": "值得继续做，但只值得先做服务化 MVP；不值得现在直接做完整 SaaS 或重研发自动化平台。",
            "worth_doing_scope": ["服务化 MVP PRD", "客户项目验证", "PRD 小修订"],
            "not_worth_doing_scope": ["完整 SaaS PRD", "自动化平台建设", "无验证重研发"],
            "confidence": "medium_high",
            "evidence_basis": safe_facts,
            "critical_gaps": ["真实利润未核算完成", "获客成本未验证", "交付工时未记录", "复购周期未确认", "完整 SaaS 产品化证据不足"],
            "next_decision": "是否按服务化 MVP 路径推进，而不是直接做完整 SaaS。",
        }
    by_decision = {
        "A_ENTER_PRD": (
            "worth_doing",
            "值得继续做，并可进入当前推荐的 PRD 路径。",
            path_recommendation.get("allowed_paths", []),
            path_recommendation.get("deferred_paths", []),
            "high",
            "是否按当前推荐 PRD 路径推进。",
        ),
        "B_LOW_COST_MVP": (
            "worth_testing",
            "值得测试，但不值得直接进入完整 PRD。",
            path_recommendation.get("allowed_paths", []),
            path_recommendation.get("deferred_paths", []),
            "medium",
            "是否先按低成本 MVP 验证核心价值闭环。",
        ),
        "C_CLIENT_PROJECT_VALIDATION": (
            "worth_testing",
            "项目价值可能成立，但产品化价值需要通过客户项目继续验证。",
            path_recommendation.get("allowed_paths", []),
            path_recommendation.get("deferred_paths", []),
            "medium_high",
            "是否先做客户项目验证，而不是直接产品化。",
        ),
        "D_INTERNAL_EFFICIENCY": (
            "worth_testing",
            "内部经营价值可能成立，适合先做内部提效验证。",
            path_recommendation.get("allowed_paths", []),
            path_recommendation.get("deferred_paths", []),
            "medium",
            "是否先验证内部效率和成本节省。",
        ),
    }
    verdict, conclusion, worth_scope, not_worth_scope, confidence, next_decision = by_decision.get(
        decision,
        ("worth_researching", "方向需要继续研究后再判断是否值得投入。", ["调研补全"], ["完整 PRD"], "medium", "是否继续调研补全。"),
    )
    return {
        "verdict": verdict,
        "plain_conclusion": conclusion,
        "worth_doing_scope": worth_scope,
        "not_worth_doing_scope": not_worth_scope,
        "confidence": confidence,
        "evidence_basis": safe_facts,
        "critical_gaps": [item["reason"] for item in warnings],
        "next_decision": next_decision,
    }


def build_operating_decision_model(raw_text: str, decision: str, path_recommendation: dict, worth: dict) -> dict:
    if decision == "G_BLOCKED_BY_REDLINE" or worth.get("verdict") == "blocked":
        return {
            "recommended_play": "红线复核，不进入经营推进。",
            "investment_ceiling": {
                "people_days": "待确认",
                "cash_cost": "待确认",
                "tool_cost": "待确认",
                "management_attention": "只保留风险复核精力",
                "principle": "红线未解除前不投入产品化、获客或开发资源。",
            },
            "validation_window": "待确认",
            "minimum_revenue_signal": ["不适用，先完成红线复核。"],
            "minimum_profit_conditions": {
                "price_floor": "不适用",
                "acquisition_cost": "不适用",
                "delivery_hours_per_customer": "不适用",
                "human_review_cost": "不适用",
                "after_sales_maintenance": "不适用",
                "condition": "红线未解除前不讨论利润模型。",
            },
            "delivery_cost_thresholds": {
                "max_delivery_hours_per_customer": "不适用",
                "max_manual_review_rounds": "不适用",
                "max_report_revision_rounds": "不适用",
                "warning": "红线风险比交付成本优先级更高。",
            },
            "acquisition_thresholds": {
                "first_customer_source": "不适用",
                "acceptable_cac": "不适用",
                "first_industries": "不适用",
                "warning": "不能在红线未解除时对外获客。",
            },
            "upgrade_to_product_conditions": ["红线风险被专业确认并降级为可控风险。"],
            "stop_or_downgrade_conditions": ["红线风险无法控制或需要承诺违法违规结果。"],
            "unknowns_that_block_scaling": ["合规边界", "责任边界", "平台或行业规则风险"],
        }
    if decision == "F_NOT_RECOMMENDED" or worth.get("verdict") == "not_worth_doing":
        return {
            "recommended_play": "停止投入或只保留复判。",
            "investment_ceiling": {
                "people_days": "待确认",
                "cash_cost": "待确认",
                "tool_cost": "待确认",
                "management_attention": "只允许低成本复判",
                "principle": "利润或价值不成立前，不进入 PRD、MVP 或研发。",
            },
            "validation_window": "待确认",
            "minimum_revenue_signal": ["出现新的明确付款、预算、复购或可规模交付证据。"],
            "minimum_profit_conditions": {
                "price_floor": "待确认",
                "acquisition_cost": "待确认",
                "delivery_hours_per_customer": "待确认",
                "human_review_cost": "待确认",
                "after_sales_maintenance": "待确认",
                "condition": "必须证明收入能覆盖获客、交付、维护、售后和风险成本。",
            },
            "delivery_cost_thresholds": {
                "max_delivery_hours_per_customer": "待确认",
                "max_manual_review_rounds": "待确认",
                "max_report_revision_rounds": "待确认",
                "warning": "交付过重时继续产品化会放大利润风险。",
            },
            "acquisition_thresholds": {
                "first_customer_source": "待确认",
                "acceptable_cac": "待确认",
                "first_industries": "待确认",
                "warning": "没有可控获客路径时不建议继续投入。",
            },
            "upgrade_to_product_conditions": ["负面反证被解决", "出现强付费证据", "交付成本下降到可控范围"],
            "stop_or_downgrade_conditions": ["继续无付款证据", "获客困难", "交付过重", "利润仍不成立"],
            "unknowns_that_block_scaling": ["付费证据", "获客成本", "交付成本", "复购意愿", "利润底线"],
        }
    if decision == "E_RESEARCH_REQUIRED" or worth.get("verdict") == "worth_researching":
        return {
            "recommended_play": "调研补全，不进入 PRD 投入。",
            "investment_ceiling": {
                "people_days": "待确认",
                "cash_cost": "待确认",
                "tool_cost": "待确认",
                "management_attention": "低，聚焦补齐关键事实",
                "principle": "只投入调研和访谈成本，不承诺研发或交付。",
            },
            "validation_window": "待确认",
            "minimum_revenue_signal": ["至少获得明确预算、真实付款、合同、复购意愿或强试点承诺之一。"],
            "minimum_profit_conditions": {
                "price_floor": "待确认",
                "acquisition_cost": "待确认",
                "delivery_hours_per_customer": "待确认",
                "human_review_cost": "待确认",
                "after_sales_maintenance": "待确认",
                "condition": "调研阶段只确认利润模型需要哪些数据，不假装利润已成立。",
            },
            "delivery_cost_thresholds": {
                "max_delivery_hours_per_customer": "待确认",
                "max_manual_review_rounds": "待确认",
                "max_report_revision_rounds": "待确认",
                "warning": "没有交付成本信息时不能进入产品化。",
            },
            "acquisition_thresholds": {
                "first_customer_source": "待确认",
                "acceptable_cac": "待确认",
                "first_industries": "待确认",
                "warning": "没有第一批客户来源时不能放大投入。",
            },
            "upgrade_to_product_conditions": ["目标用户、付费证据、成本结构、风险边界和获客路径补齐。"],
            "stop_or_downgrade_conditions": ["补证后仍没有付费者", "无法定义验收指标", "获客路径不存在"],
            "unknowns_that_block_scaling": ["目标用户", "付费证据", "成本结构", "获客路径", "风险边界"],
        }
    if is_geo_context(raw_text) and decision in {VALUE_GATE_ALLOW_PRD, "B_LOW_COST_MVP"}:
        return {
            "recommended_play": "2-4 周服务化 MVP，不做完整 SaaS。",
            "investment_ceiling": {
                "people_days": "待确认",
                "cash_cost": "待确认",
                "tool_cost": "待确认",
                "management_attention": "低到中，聚焦 2-4 周验证",
                "principle": "低成本验证，优先人工 + 半自动，不投入重研发。",
            },
            "validation_window": "2-4 周",
            "minimum_revenue_signal": [
                "真实付款 / 合同 / 明确预算",
                "至少拿到第二个付费信号或明确复购 / 复测意愿",
            ],
            "minimum_profit_conditions": {
                "price_floor": "待确认",
                "acquisition_cost": "待确认",
                "delivery_hours_per_customer": "待确认",
                "human_review_cost": "待确认",
                "after_sales_maintenance": "待确认",
                "condition": "客单价必须覆盖获客、交付、人工复核、维护、售后、合规和风险成本，并保留可接受毛利。",
            },
            "delivery_cost_thresholds": {
                "max_delivery_hours_per_customer": "待确认",
                "max_manual_review_rounds": "待确认",
                "max_report_revision_rounds": "待确认",
                "warning": "如果交付严重依赖人工专家，产品化价值不足。",
            },
            "acquisition_thresholds": {
                "first_customer_source": "待确认",
                "acceptable_cac": "待确认",
                "first_industries": "待确认",
                "warning": "如果获客成本高于客单价，利润价值不成立。",
            },
            "upgrade_to_product_conditions": [
                "连续出现相似客户需求",
                "单客户交付工时下降到可控范围",
                "客户愿意复测 / 续费 / 转介绍",
                "GEO 指标有可解释变化",
                "核心流程可标准化为工具或看板",
            ],
            "stop_or_downgrade_conditions": [
                "2-4 周内拿不到第二个付费信号",
                "客户只愿免费试用不愿付费",
                "获客成本高于客单价",
                "单客户交付工时持续过高",
                "GEO 效果无法归因",
                "客户不愿复测 / 续费 / 推荐",
            ],
            "unknowns_that_block_scaling": [
                "最低客单价",
                "获客成本",
                "单客户交付工时",
                "复购 / 复测意愿",
                "第一批行业边界",
                "平台规则风险",
            ],
        }
    if decision == "C_CLIENT_PROJECT_VALIDATION":
        recommended_play = "客户项目验证，不直接产品化研发。"
    elif decision == "D_INTERNAL_EFFICIENCY":
        recommended_play = "内部提效验证，不包装成对外产品。"
    elif decision == "B_LOW_COST_MVP":
        recommended_play = "低成本 MVP，先验证核心价值闭环。"
    else:
        recommended_play = f"{path_recommendation.get('recommended_path', '推荐路径')}。"
    return {
        "recommended_play": recommended_play,
        "investment_ceiling": {
            "people_days": "待确认",
            "cash_cost": "待确认",
            "tool_cost": "待确认",
            "management_attention": "待确认",
            "principle": "先用最小投入验证价值，不因方向成立就默认重研发。",
        },
        "validation_window": "待确认",
        "minimum_revenue_signal": ["待确认真实付款、明确预算、复购意愿或内部节省证明。"],
        "minimum_profit_conditions": {
            "price_floor": "待确认",
            "acquisition_cost": "待确认",
            "delivery_hours_per_customer": "待确认",
            "human_review_cost": "待确认",
            "after_sales_maintenance": "待确认",
            "condition": "收入或节省必须覆盖获客、交付、维护、售后和风险成本。",
        },
        "delivery_cost_thresholds": {
            "max_delivery_hours_per_customer": "待确认",
            "max_manual_review_rounds": "待确认",
            "max_report_revision_rounds": "待确认",
            "warning": "交付成本未确认时不得放大投入。",
        },
        "acquisition_thresholds": {
            "first_customer_source": "待确认",
            "acceptable_cac": "待确认",
            "first_industries": "待确认",
            "warning": "获客路径未确认时不得写成规模化增长。",
        },
        "upgrade_to_product_conditions": ["价值闭环成立", "交付成本可控", "复购或多客户需求出现", "风险边界可控"],
        "stop_or_downgrade_conditions": ["付费或节省证据不足", "交付成本不可控", "获客路径不成立", "风险边界不可控"],
        "unknowns_that_block_scaling": ["价格", "获客成本", "交付成本", "复购 / 留存", "规模化风险"],
    }


def build_decision_questions(raw_text: str, path_recommendation: dict) -> list[dict]:
    if is_geo_context(raw_text):
        questions = [
            (
                "是否确认本轮只做 2-4 周服务化 MVP？",
                "进入低成本验证，只做报告、复测、看板或半自动服务闭环。",
                "不进入 PRD，继续调研或等待更多证据。",
                "建议确认，先验证商业闭环，不直接重研发。",
            ),
            (
                "是否确认不投入完整 SaaS 研发？",
                "避免在真实利润、获客、交付工时未确认前扩大成本。",
                "如果现在投入完整 SaaS，研发和维护风险会明显升高。",
                "建议确认，完整 SaaS 等升级条件满足后再做。",
            ),
            (
                "是否确认最低客单价 / 价格区间？",
                "可以核算最低利润条件，判断是否值得继续交付。",
                "价格继续待确认，真实利润仍不能通过。",
                "建议先给出最低可接受价格区间。",
            ),
            (
                "是否确认单客户交付工时上限？",
                "可以判断服务化 MVP 是否有可接受毛利。",
                "无法判断交付是否过重，产品化仍需暂缓。",
                "建议设定单客户交付工时上限。",
            ),
            (
                "是否确认第一批行业和客户来源？",
                "PRD 可以聚焦行业词库、场景、指标和获客动作。",
                "范围会发散，获客和交付风险上升。",
                "建议先限定 1-2 个行业和明确客户来源。",
            ),
            (
                "是否确认达到什么结果才升级产品化？",
                "后续能根据复购、交付工时、指标变化和标准化程度决定是否升级。",
                "缺少升级标准时，容易把服务项目误放大成 SaaS。",
                "建议明确升级条件后再进入服务化 MVP PRD。",
            ),
            (
                "是否确认失败后停止或降级为服务项目？",
                "如果 2-4 周拿不到第二个付费信号、无法归因或交付过重，就停止产品化投入。",
                "没有止损条件会导致持续投入但无法判断价值。",
                "建议确认停止 / 降级条件。",
            ),
        ]
    else:
        questions = [
            (
                "是否接受当前推荐路径？",
                f"进入 {path_recommendation.get('recommended_path')}。",
                "保持当前模块阻断，继续补证据。",
                "建议按推荐路径推进，除非关键事实不成立。",
            )
        ]
    return [
        {
            "question": question,
            "option_a_result": option_a,
            "option_b_result": option_b,
            "recommendation": recommendation,
        }
        for question, option_a, option_b, recommendation in questions
    ]


def build_prd_agent_input_package(value_gate: dict) -> dict:
    route_name = value_gate.get("downstream_input_package")
    route_package = value_gate.get(route_name, {}) if route_name else {}
    worth = value_gate.get("business_worth_verdict", {})
    operating = value_gate.get("operating_decision_model", {})
    route_decision = value_gate.get("route_decision", {})
    material_summary = value_gate.get("material_intake_summary", {})
    source_quality = value_gate.get("source_quality_gate", {})
    evidence_sufficiency = value_gate.get("evidence_sufficiency_gate", {})
    roi_input_table = value_gate.get("roi_input_table", {})
    roi_decision_model = value_gate.get("roi_decision_model", {})
    investment_decision = value_gate.get("investment_decision_gate", {})

    material_rows = [
        {
            "key": item.get("key"),
            "label": item.get("label"),
            "status": item.get("slot_status"),
            "decision_use": item.get("decision_use"),
            "cannot_prove": item.get("cannot_prove"),
        }
        for item in material_summary.get("slot_rows", [])
    ]

    return {
        "project_id": value_gate.get("project_id"),
        "module": "value_gate_prd_input",
        "version": value_gate.get("version"),
        "contract": {
            "purpose": "给 PRD 模块的最小干净输入包；完整证据、竞品、ROI 明细只通过引用追溯。",
            "read_first": "route_decision",
            "must_not_use_as_full_evidence_report": True,
        },
        "route_decision": route_decision,
        "entry_permission": {
            "can_enter_full_prd": route_decision.get("can_enter_full_prd", value_gate.get("can_enter_full_prd")),
            "recommended_path": route_decision.get("recommended_path"),
            "allowed_paths": route_decision.get("allowed_paths", []),
            "deferred_paths": route_decision.get("deferred_paths", []),
            "blocked_paths": route_decision.get("blocked_paths", []),
            "decision_gate": route_decision.get("canonical_decision", value_gate.get("decision_gate")),
            "execution_status": route_decision.get("execution_status", value_gate.get("execution_status")),
            "allowed_prd_type": route_decision.get("allowed_prd_type", value_gate.get("allowed_prd_type")),
        },
        "business_worth_verdict": worth,
        "facts_allowed_for_prd": value_gate.get("safe_facts_for_prd", []),
        "assumptions_for_prd": value_gate.get("assumptions_for_prd", []),
        "claims_must_not_be_written": value_gate.get("blocked_claims", []),
        "unsupported_claims": value_gate.get("unsupported_claims", []),
        "prd_constraints": [
            "必须区分事实、假设、推论和待验证问题。",
            "不得把未溯源数据写成事实。",
            "不得把用户提供的买单信号夸大为完整 SaaS 产品化成立。",
            "不得承诺 AI 平台推荐、排名或确定性收益。",
        ],
        "required_sections": [
            "前置价值门禁结论",
            "真实利润与成本假设",
            "项目转产品判断",
            "反证与停止条件",
            "人工确认项",
        ],
        "business_limits": {
            "recommended_play": operating.get("recommended_play"),
            "investment_ceiling": operating.get("investment_ceiling", {}),
            "validation_window": operating.get("validation_window"),
            "minimum_revenue_signal": operating.get("minimum_revenue_signal", []),
            "minimum_profit_conditions": operating.get("minimum_profit_conditions", {}),
            "upgrade_conditions": operating.get("upgrade_to_product_conditions", []),
            "stop_conditions": operating.get("stop_or_downgrade_conditions", []),
            "financial_unknowns": operating.get("unknowns_that_block_scaling", []),
        },
        "current_route_package": {
            "name": route_name,
            "completeness_gate": value_gate.get("route_package_completeness_gate", {}),
            "package": route_package,
        },
        "evidence_summary": {
            "sufficiency": evidence_sufficiency,
            "source_quality_status": source_quality.get("overall_status"),
            "source_counts": source_quality.get("source_counts", {}),
            "material_status": material_summary.get("status"),
            "material_requirements": material_rows,
            "verified_evidence_status": value_gate.get("verified_evidence_assessment", {}).get("status"),
            "s_verified_gate": value_gate.get("s_claimed_to_s_verified_gate", {}),
        },
        "roi_summary": {
            "input_table_status": roi_input_table.get("status"),
            "missing_critical_inputs": roi_input_table.get("missing_critical_inputs", []),
            "can_calculate_roi": roi_input_table.get("can_calculate_roi"),
            "can_claim_high_roi": roi_input_table.get("can_claim_high_roi"),
            "roi_model_status": roi_decision_model.get("status"),
            "investment_conclusion": investment_decision.get("conclusion"),
            "investment_rule": investment_decision.get("rule"),
        },
        "human_confirmation_required": value_gate.get("human_confirmation", {}),
        "decision_dependent_inputs": {
            "if_accept_recommended_path": "PRD 只能围绕推荐形态展开，不得扩大到暂缓或阻断路径。",
            "if_reject_recommended_path": "保留证据并继续补充缺口，不生成正式 PRD。",
            "next_decision": worth.get("next_decision", ""),
        },
        "evidence_references": {
            "full_value_gate": "00_value_gate.json",
            "owner_decision_report": "00_value_gate_owner_decision.md",
            "owner_summary_report": "00_value_gate_owner_summary.md",
            "evidence_snapshot": "00_value_gate_evidence_snapshot.json",
        },
    }


def value_gate_owner_decision_markdown(value_gate: dict) -> str:
    path = value_gate.get("path_recommendation", {})
    route_decision = value_gate.get("route_decision", {})
    worth = value_gate.get("business_worth_verdict", {})
    evidence_basis = value_gate.get("evidence_decision_basis", [])
    evidence_reasoning = value_gate.get("evidence_to_verdict_reasoning", {})
    sufficiency = value_gate.get("evidence_sufficiency_gate", {})
    source_quality = value_gate.get("source_quality_gate", {})
    research_agent = value_gate.get("evidence_research_agent", {})
    research_queue = value_gate.get("research_execution_queue", {})
    material_summary = value_gate.get("material_intake_summary", {})
    material_mapping = value_gate.get("material_to_evidence_mapping", [])
    rejudgment_readiness = value_gate.get("rejudgment_readiness_gate", {})
    external_research = value_gate.get("external_research_results", {})
    source_quality_scorecard = value_gate.get("source_quality_scorecard", {})
    pricing_evidence = value_gate.get("competitor_pricing_evidence", {})
    platform_rules = value_gate.get("platform_rule_evidence", {})
    verified_assessment = value_gate.get("verified_evidence_assessment", {})
    s_verified_gate = value_gate.get("s_claimed_to_s_verified_gate", {})
    value_judgment = value_gate.get("prd_input_package", {}).get("value_judgment", {})
    evidence_grade_gate = value_gate.get("evidence_grade_gate", {})
    verified_gate = value_gate.get("verified_evidence_gate", {})
    payment_verification = value_gate.get("payment_evidence_verification", {})
    verification_intake = value_gate.get("evidence_verification_intake", {})
    attachment_plan = value_gate.get("attachment_verification_plan", {})
    competitor_table = value_gate.get("competitor_benchmark_table", {})
    redline_pack = value_gate.get("industry_redline_rule_pack", {})
    contextual_redline_filter = value_gate.get("contextual_redline_filter", {})
    profit_model = value_gate.get("lightweight_profit_model", {})
    roi_input_table = value_gate.get("roi_input_table", {})
    roi_model = value_gate.get("roi_decision_model", {})
    real_profit_calculation = value_gate.get("real_profit_calculation", {})
    roi_scenario_analysis = value_gate.get("roi_scenario_analysis", {})
    investment_decision = value_gate.get("investment_decision_gate", {})
    value_quality_scorecard = value_gate.get("value_quality_scorecard", {})
    resource_matrix = value_gate.get("resource_advantage_matrix", {})
    acquisition_table = value_gate.get("acquisition_decision_table", {})
    realization_timeline = value_gate.get("value_realization_timeline", {})
    output_boundary = value_gate.get("output_boundary_gate", {})
    route_gate = value_gate.get("route_package_completeness_gate", {})
    rejudgment_package = value_gate.get("rejudgment_package", {})
    rejudgment_execution = value_gate.get("rejudgment_execution_plan", {})
    archive_policy = value_gate.get("evidence_archive_policy", {})
    operating = value_gate.get("operating_decision_model", {})
    route_package = value_gate.get(value_gate.get("downstream_input_package"), {})
    investment = operating.get("investment_ceiling", {})
    profit_conditions = operating.get("minimum_profit_conditions", {})
    scorecard = value_gate.get("hard_gate_scorecard", [])
    questions = value_gate.get("decision_questions", [])
    blocked = [item for item in scorecard if item.get("status") in {"Fail", "Blocked"}]
    warnings = [item for item in scorecard if item.get("status") == "Warning"]

    def rows(items: list[dict]) -> list[str]:
        return [
            f"| {item.get('label')} | {item.get('status')} | {item.get('reason')} | {'是' if item.get('blocks_full_prd') else '否'} | {item.get('next_action')} |"
            for item in items
        ]

    def mermaid_label(value: object) -> str:
        return str(value or "待确认").replace('"', '\\"')

    def zh_status(value: object) -> str:
        mapping = {
            "A_ENTER_PRD": "A：允许完整 PRD",
            "B_LOW_COST_MVP": "B：服务化 MVP / 低成本 MVP",
            "C_CLIENT_PROJECT_VALIDATION": "C：客户项目验证",
            "D_INTERNAL_EFFICIENCY": "D：内部提效",
            "E_RESEARCH_REQUIRED": "E：需要补调研",
            "F_NOT_RECOMMENDED": "F：不建议推进",
            "G_BLOCKED_BY_REDLINE": "G：红线阻断",
            "worth_doing": "值得做",
            "worth_testing": "值得测试",
            "worth_researching": "值得先调研",
            "not_worth_doing": "暂不值得做",
            "blocked": "红线阻断",
            "sufficient_for_full_prd": "足够支持完整 PRD",
            "sufficient_for_mvp": "足够支持服务化 MVP",
            "sufficient_for_client_project": "足够支持客户项目验证",
            "research_required": "证据不足，需要补调研",
            "insufficient_stop": "证据不足，建议停止",
            "blocked_by_redline": "红线阻断",
            "missing_critical_materials": "关键材料缺失",
            "not_ready_missing_materials": "未达到复判条件",
            "S_claimed": "S_claimed（用户声明，待材料复核）",
            "S_partial_verified": "S_partial_verified（部分材料已复核）",
            "S_verified": "S_verified（已复核强证据）",
            "roi_unavailable_missing_inputs": "ROI 缺关键输入，暂不可计算",
            "roi_possible_service_mvp": "ROI 待复判，可先做服务化 MVP",
            "roi_positive_client_project": "ROI 支持客户项目",
            "roi_positive_productization_candidate": "ROI 支持产品化候选",
            "roi_negative_stop": "ROI 不成立，建议停止",
            "available": "可用",
            "has_source_risk": "有来源风险，需复核",
            "needs_platform_boundary_review": "需要平台边界复核",
            "usable_for_mvp_not_full_prd": "可用于 MVP 判断，不足以支持完整 PRD",
            "missing": "缺失",
            "submitted_pending_review": "已提交，待复核",
            "reviewed_accepted": "已复核通过",
            "reviewed_rejected": "已复核拒绝",
            "needs_more_context": "需要补充上下文",
        }
        text = str(value or "待确认")
        return mapping.get(text, text)

    def material_card_lines(item: dict, prefix: str | None = None, consequence: str | None = None) -> list[str]:
        title = item.get("label") or "未命名材料"
        heading = f"**{prefix}｜{title}**" if prefix else f"**{title}**"
        lines_out = [
            heading,
            f"- 当前状态：{zh_status(item.get('slot_status'))}",
            f"- 用来判断：{item.get('decision_use') or '待确认'}",
            f"- 不能证明：{item.get('cannot_prove') or '待确认'}",
        ]
        if consequence:
            lines_out.append(f"- 不提供的后果：{consequence}")
        lines_out.append("")
        return lines_out

    decision_gate = value_gate.get("decision_gate")
    allowed_prd_type = value_gate.get("allowed_prd_type")
    recommended_path = route_decision.get("recommended_path") or path.get("recommended_path") or allowed_prd_type
    unsupported_paths = sufficiency.get("unsupported_paths", [])
    missing_materials = material_summary.get("missing_critical_slots", [])
    material_status = material_summary.get("status")
    s_level = verified_assessment.get("status") or verified_gate.get("claimed_evidence_grade")
    roi_status = roi_scenario_analysis.get("status") or roi_model.get("status")
    investment_conclusion = investment_decision.get("conclusion") or "待确认"
    top_blockers = unique_list(
        list(missing_materials)
        + list(sufficiency.get("missing_evidence_types", []))
        + list(real_profit_calculation.get("missing_inputs", []))[:4]
        + list(investment_decision.get("blocked_paths", []))[:3]
    )[:10]
    material_priority_rows = []
    priority_labels = [
        "付款 / 合同证据",
        "客户 / 行业记录",
        "MVP 实验记录",
        "报价 / 客单价证据",
        "交付工时证据",
        "获客来源证据",
        "复购 / 续费 / 转介绍记录",
    ]
    for item in material_summary.get("slot_rows", []):
        if item.get("label") in priority_labels:
            material_priority_rows.append(item)

    lines = [
        f"# {value_gate.get('project_id')} - 商业拍板报告",
        "",
        "## 0. 先看这里：决策总览",
        f"- 结论：{worth.get('plain_conclusion')}",
        f"- 统一主路由：{recommended_path}",
        f"- 当前建议：{recommended_path}",
        f"- 当前门禁：{zh_status(decision_gate)} / {allowed_prd_type}",
        f"- 证据充分性：{zh_status(sufficiency.get('overall_status'))}",
        f"- 证据复核等级：{zh_status(s_level)}",
        f"- ROI 状态：{zh_status(roi_status)}",
        f"- 投资门禁：{zh_status(investment_conclusion)}",
        f"- 是否允许完整 PRD：{'是' if value_gate.get('can_enter_full_prd') else '否'}",
        f"- 你现在真正要决策：{worth.get('next_decision')}",
        "",
        "### 0.1 阅读顺序",
        "1. 先看 `0.2 决策路径图`，判断当前走哪条路。",
        "2. 再看 `0.4 你需要补的材料`，决定要不要给我补证据。",
        "3. 如果要深究，再看后面的证据表、竞品表、ROI 表。",
        "",
        "### 0.2 决策路径图",
        "```mermaid",
        "flowchart LR",
        f'    A["原始想法 / 项目输入"] --> B["值不值得做: {mermaid_label(zh_status(worth.get("verdict")))}"]',
        f'    B --> C["证据充分性: {mermaid_label(zh_status(sufficiency.get("overall_status")))}"]',
        f'    C --> D["推荐路径: {mermaid_label(recommended_path)}"]',
        f'    D --> E["材料复核: {mermaid_label(zh_status(material_status))}"]',
        f'    E --> F["ROI 复判: {mermaid_label(zh_status(roi_status))}"]',
        f'    F --> G["升级候选: {mermaid_label(zh_status(investment_conclusion))}"]',
        f'    C -. 暂缓 .-> H["暂缓路径: {mermaid_label(" / ".join(unsupported_paths[:2]) or "完整 PRD / 产品化")}"]',
        "```",
        "",
        "### 0.3 证据漏斗",
        "```mermaid",
        "flowchart TB",
        '    A["外部市场 / 竞品 / 平台证据"] --> B["能证明: 赛道、竞品、趋势、监测对象存在"]',
        '    A -.不能证明.-> C["不能证明: 本项目利润、ROI、复购、获客成立"]',
        '    D["用户声明: MVP / 买单"] --> E["当前等级: S_claimed"]',
        '    E --> F["材料复核"]',
        '    F -->|材料通过| G["S_verified 候选"]',
        '    F -->|材料缺失| H["完整 PRD / 高 ROI / SaaS 产品化继续阻断"]',
        "```",
        "",
        "### 0.4 你需要补的材料",
    ]
    if material_priority_rows:
        for index, item in enumerate(material_priority_rows, 1):
            priority = "P0" if index <= 4 else "P1"
            consequence = "不能升级 S_verified / ROI / 完整 PRD 候选" if priority == "P0" else "不能证明复购或产品化升级"
            lines.extend(material_card_lines(item, priority, consequence))
    else:
        lines.extend(
            [
                "**P0｜付款、客户、MVP、报价、工时、获客材料**",
                "- 当前状态：缺失",
                "- 用来判断：证据复核和 ROI 判断",
                "- 不能证明：完整 PRD、SaaS 产品化和高 ROI",
                "- 不提供的后果：只能停留在服务化 MVP / 调研",
                "",
            ]
        )
    lines.extend(
        [
            "",
            "### 0.5 当前阻断点",
        ]
    )
    if top_blockers:
        lines.extend(f"- {item}" for item in top_blockers)
    else:
        lines.append("- 当前没有识别到阻断点。")
    lines.extend(
        [
            "",
            "### 0.6 当前可以做 / 不能做",
            f"- 可以做：{', '.join(path.get('allowed_paths', [])) or recommended_path}",
            f"- 暂缓做：{', '.join(path.get('deferred_paths', [])) or '无'}",
            f"- 禁止做：{', '.join(path.get('blocked_paths', [])) or '无'}",
            "",
            "## 1. 值不值得做",
            f"- 结论：{worth.get('plain_conclusion')}",
            f"- 价值判定：{zh_status(worth.get('verdict'))}",
            f"- 置信度：{worth.get('confidence')}",
            f"- 下一步真正要决策：{worth.get('next_decision')}",
            "",
            "## 2. 证据决策表",
            "| 证据 | 来源 | 可达性 | 强度 | 能证明什么 | 不能证明什么 | 对结论的影响 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    if evidence_basis:
        for item in evidence_basis[:12]:
            source = item.get("source_title") or item.get("source_type") or "未标注"
            source_url = item.get("source_url")
            if source_url and str(source_url).startswith(("http://", "https://")):
                source = f"[{source}]({source_url})"
            elif source_url:
                source = f"{source} (`{source_url}`)"
            fetch_status = item.get("fetch_status") or "not_checked"
            if item.get("http_status"):
                fetch_status = f"{fetch_status}/{item.get('http_status')}"
            lines.append(
                f"| {item.get('evidence')} | {source} | {fetch_status} | {item.get('strength')} | {item.get('proves')} | {item.get('does_not_prove')} | {item.get('decision_impact')} |"
            )
    else:
        lines.append("| 无可用证据 | 未提供 | not_checked | D | 不能证明商业价值 | 不能进入结论 | 需要补证据 |")
    source_counts = source_quality.get("source_counts", {})
    lines.extend(
        [
            "",
            "### 2.1 证据来源质量门禁",
            f"- 总体状态：{zh_status(source_quality.get('overall_status'))}",
            f"- 用户提供事实：{source_counts.get('user_provided_fact', 0)} 条",
            f"- 外部公开来源：{source_counts.get('external_public_source', 0)} 条",
            f"- 可达外部来源：{source_counts.get('reachable_external', 0)} 条",
            f"- 非成功 / 不可达外部来源：{source_counts.get('non_success_external', 0)} 条",
            f"- 竞品参照：{source_counts.get('competitor_rows', 0)} 条",
            f"- 完整 PRD 阻断缺口：{', '.join(source_quality.get('blocking_gaps_for_full_prd', [])) or '无'}",
            f"- 使用规则：{source_quality.get('prd_usage_rule')}",
        ]
    )
    if source_quality.get("warning_items"):
        lines.append("- 来源质量提醒：")
        lines.extend(f"  - {item}" for item in source_quality.get("warning_items", []))
    lines.extend(
        [
            "",
            "### 2.2 Evidence Research Agent 下一步任务",
            f"- 模式：{research_agent.get('mode')}",
            f"- 任务：{research_agent.get('mission')}",
            f"- 当前路径：{research_agent.get('current_route_package')}",
            "",
            "| 研究轨道 | 目的 | 当前来源 | 还要补的来源 | 影响什么决策 |",
            "|---|---|---|---|---|",
        ]
    )
    for item in research_agent.get("research_tracks", []):
        lines.append(
            f"| {item.get('key')} | {item.get('purpose')} | {', '.join(item.get('current_sources', [])) or '无'} | {', '.join(item.get('required_source_types', [])) or '无'} | {item.get('decision_effect')} |"
        )
    lines.extend(
        [
            "",
            "### 2.3 研究任务执行队列",
            f"- 队列状态：{research_queue.get('queue_status')}",
            f"- 当前路径：{research_queue.get('current_route_package')}",
            f"- 最大并行任务数：{research_queue.get('max_parallel_tasks')}",
            f"- P0 任务数：{research_queue.get('p0_task_count')}",
            "",
            "| 任务 | 优先级 | 目标 | 需要来源 | 是否需要你提供材料 | 完成标准 | 失败 / 降级规则 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for item in research_queue.get("tasks", []):
        lines.append(
            f"| {item.get('task_id')} | {item.get('priority')} | {item.get('objective')} | {', '.join(item.get('source_request', [])) or '无'} | {'是' if item.get('owner_material_required') else '否'} | {item.get('done_definition')} | {item.get('fail_or_downgrade_rule')} |"
        )
    if research_queue.get("task_output_contract"):
        lines.extend(
            [
                f"- 输出字段要求：{', '.join(research_queue.get('task_output_contract', {}).get('required_fields', []))}",
                f"- 不能接受的输出：{', '.join(research_queue.get('task_output_contract', {}).get('invalid_outputs', []))}",
                f"- 交接规则：{research_queue.get('task_output_contract', {}).get('handoff_rule')}",
            ]
        )
    lines.extend(
        [
            "",
            "## 3. 材料接收与复判准备",
            "### 3.1 复判状态",
            f"- 材料状态：{zh_status(material_summary.get('status'))}",
            f"- 复判准备：{zh_status(rejudgment_readiness.get('status'))}",
            f"- 当前证据复核等级：{zh_status(verified_assessment.get('status'))}",
            f"- 是否允许升级 S_verified：{'是' if s_verified_gate.get('can_upgrade_to_s_verified') else '否'}",
            f"- 规则：{material_summary.get('rule')}",
            "",
            "### 3.2 材料槽位清单",
        ]
    )
    for item in material_summary.get("slot_rows", []):
        lines.extend(material_card_lines(item))
    if s_verified_gate.get("upgrade_blockers"):
        lines.extend(
            [
                "### 3.3 升级阻断",
                f"- {', '.join(s_verified_gate.get('upgrade_blockers', []))}",
            ]
        )
    lines.extend(
        [
            "",
            "## 4. 外部证据研究结果",
            f"- 外部证据状态：{zh_status(external_research.get('status'))}",
            f"- 外部证据数量：{external_research.get('row_count', 0)}",
            f"- 来源质量：{zh_status(source_quality_scorecard.get('overall_status'))}",
            f"- 竞品价格证据：{zh_status(pricing_evidence.get('status'))}",
            f"- 平台规则证据：{zh_status(platform_rules.get('status'))}",
            f"- 决策边界：{external_research.get('decision_rule')}",
            "",
            "| 来源 | 链接 | 能证明什么 | 不能证明什么 | 对决策的影响 |",
            "|---|---|---|---|---|",
        ]
    )
    for item in external_research.get("rows", [])[:12]:
        source = item.get("source_title", "")
        url = item.get("url", "")
        source_text = f"[{source}]({url})" if url else source
        lines.append(
            f"| {source_text} | {url or '无'} | {item.get('can_prove')} | {item.get('cannot_prove')} | {item.get('decision_effect')} |"
        )
    lines.extend(
        [
            "",
            "## 5. 国内外竞品标杆表",
            f"- 状态：{competitor_table.get('status')}",
            f"- 覆盖：中国 {competitor_table.get('coverage', {}).get('china_count', 0)} 个，海外 {competitor_table.get('coverage', {}).get('international_count', 0)} 个",
            f"- 决策规则：{competitor_table.get('decision_rule')}",
            "",
            "| 竞品 | 市场 | 链接 | 重点能力 | 标杆信号 | 能证明什么 | 不能证明什么 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for item in competitor_table.get("rows", []):
        source = item.get("source_title") or item.get("name")
        source_url = item.get("source_url")
        source_text = f"[{source}]({source_url})" if source_url else source
        lines.append(
            f"| {item.get('name')} | {item.get('market')} | {source_text} | {item.get('focus')} | {item.get('benchmark_signal')} | {item.get('what_it_proves')} | {item.get('what_it_does_not_prove')} |"
        )
    commercial_evidence = [
        item
        for item in evidence_basis
        if any(token in item.get("strength", "") for token in ("行业趋势", "用户行为", "价格锚点", "竞品产品化"))
    ]
    roi_unknowns = profit_model.get("unknown_inputs", []) or operating.get("unknowns_that_block_scaling", [])
    lines.extend(
        [
            "",
            "## 6. 外部商业证据与 ROI 证明状态",
            f"- 外部商业证据数量：{len(commercial_evidence)}",
            "- 已能证明：AI 搜索正在影响传统搜索 / 搜索营销；AI 搜索使用和购物相关使用在增长；海外 GEO 服务存在公开价格锚点；AI 可见度监测已有竞品指标和工具形态。",
            "- 还不能证明：本项目已经能稳定获客、持续成交、低成本交付、复购或取得高 ROI。",
            f"- ROI 仍缺证据：{', '.join(roi_unknowns) or '无'}",
            "- 允许的商业结论：值得服务化 MVP / 客户项目验证。",
            "- 不允许的商业结论：完整 SaaS 已成立、高 ROI 已证明、可以直接重研发自动化平台。",
            "",
            "### 6.1 价值类型与商业结果收敛",
            f"- 主价值类型：{value_judgment.get('primary_value_type')}",
            f"- 次级价值类型：{', '.join(value_judgment.get('secondary_value_types', [])) or '无'}",
            f"- 价值类型判断：{value_judgment.get('value_type_reasoning')}",
            f"- 主商业结果：{value_judgment.get('primary_business_result')}",
            f"- 次级商业结果：{', '.join(value_judgment.get('secondary_business_results', [])) or '无'}",
            f"- 结果指标：{', '.join(value_judgment.get('result_metrics', [])) or '无'}",
            f"- 当前不能证明：{', '.join(value_judgment.get('result_not_proven_yet', [])) or '无'}",
            f"- 禁止误写：{', '.join(value_judgment.get('must_not_treat_as', [])) or '无'}",
            "",
            "## 7. 证据等级门禁",
            f"- 当前证据等级：{evidence_grade_gate.get('current_grade')}",
            f"- 门禁状态：{evidence_grade_gate.get('status')}",
            f"- 当前路径最低要求：{evidence_grade_gate.get('minimum_required_for_current_gate')}",
            f"- 是否满足当前路径：{'是' if evidence_grade_gate.get('meets_current_gate') else '否'}",
            f"- 完整 PRD 缺口：{', '.join(evidence_grade_gate.get('full_prd_gap', [])) or '无'}",
            "- 升级需要补的证据：",
        ]
    )
    lines.extend(f"  - {item}" for item in evidence_grade_gate.get("upgrade_evidence_required", []))
    lines.extend(
        [
            "",
            "### 7.1 强证据复核门禁",
            f"- 状态：{verified_gate.get('status')}",
            f"- 声明证据等级：{verified_gate.get('claimed_evidence_grade')}",
            f"- 复核证据等级：{verified_gate.get('verified_evidence_grade')}",
            f"- 是否可当作 S 级已验证证据：{'是' if verified_gate.get('can_treat_as_s_level') else '否'}",
            f"- PRD 使用规则：{verified_gate.get('prd_fact_rule')}",
            "- 用户声明的强证据：",
        ]
    )
    lines.extend(f"  - {item}" for item in verified_gate.get("claimed_strong_evidence", []) or ["无"])
    lines.append("- 已复核的强证据：")
    lines.extend(f"  - {item}" for item in verified_gate.get("verified_strong_evidence", []) or ["无"])
    lines.append("- 复核需要补的材料：")
    lines.extend(f"  - {item}" for item in verified_gate.get("verification_required", []))
    if verified_gate.get("full_prd_blocking_gap"):
        lines.append("- 对完整 PRD 的阻断缺口：")
        lines.extend(f"  - {item}" for item in verified_gate.get("full_prd_blocking_gap", []))
    lines.extend(
        [
            "",
            "### 7.2 付费证据 claimed / verified 分离",
            f"- 声明付费层级：第 {payment_verification.get('claimed_payment_layer')} 层",
            f"- 已复核付费层级：第 {payment_verification.get('verified_payment_layer')} 层",
            f"- 当前可用于决策层级：第 {payment_verification.get('usable_payment_layer_for_decision')} 层",
            f"- 当前可支撑：{payment_verification.get('usable_for_current_path')}",
            f"- 不能支撑：{', '.join(payment_verification.get('cannot_support', [])) or '无'}",
            f"- 规则：{payment_verification.get('decision_rule')}",
            "",
            "| 层级 | 含义 | 状态 | 需要证据 |",
            "|---|---|---|---|",
        ]
    )
    for item in payment_verification.get("layer_rows", []):
        lines.append(
            f"| 第 {item.get('level')} 层 | {item.get('label')} | {item.get('status')} | {item.get('required_evidence')} |"
        )
    lines.extend(
        [
            "",
            "### 7.3 证据复核入口",
            f"- 状态：{verification_intake.get('status')}",
            f"- 目的：{verification_intake.get('purpose')}",
            f"- 升级规则：{verification_intake.get('upgrade_rule')}",
            f"- 下一步：{verification_intake.get('next_action')}",
            "",
            "| 复核槽位 | 当前状态 | 接受材料 | 能升级什么判断 | 不能证明什么 | 用于什么判断 |",
            "|---|---|---|---|---|---|",
        ]
    )
    for item in verification_intake.get("verification_slots", []):
        lines.append(
            f"| {item.get('label')} | {item.get('current_status')} | {', '.join(item.get('accepted_materials', []))} | {item.get('verification_effect')} | {item.get('cannot_prove')} | {item.get('required_for')} |"
        )
    lines.extend(
        [
            "",
            "### 7.4 附件验真计划",
            f"- 当前状态：{attachment_plan.get('current_status')}",
            f"- 是否禁止自动验真：{'是' if attachment_plan.get('no_auto_verification') else '否'}",
            f"- 你需要做什么：{attachment_plan.get('owner_action_required')}",
            f"- S_verified 规则：{attachment_plan.get('s_verified_rule')}",
            "",
            "| 验真槽位 | 当前状态 | 需要材料 | 验真方式 | 能升级什么 | 不能证明什么 |",
            "|---|---|---|---|---|---|",
        ]
    )
    for item in attachment_plan.get("slots", []):
        lines.append(
            f"| {item.get('label')} | {item.get('current_status')} | {', '.join(item.get('materials_to_request', []))} | {item.get('manual_review_method')} | {item.get('upgrade_effect')} | {item.get('cannot_prove')} |"
        )
    lines.extend(
        [
            "",
            "## 8. 证据到结论的推导",
            f"- 证据规则：{evidence_reasoning.get('evidence_rule')}",
            f"- 当前结论：{evidence_reasoning.get('plain_conclusion')}",
        ]
    )
    allowed_reasons = evidence_reasoning.get("why_this_verdict_is_allowed", [])
    if allowed_reasons:
        lines.append("- 为什么允许当前路径：")
        lines.extend(f"  - {item}" for item in allowed_reasons)
    bigger_limits = evidence_reasoning.get("why_bigger_scope_is_not_allowed", [])
    if bigger_limits:
        lines.append("- 为什么不能直接做大：")
        lines.extend(f"  - {item}" for item in bigger_limits)
    lines.extend(
        [
            "",
            "## 9. 证据充分性结论",
            f"- 充分性状态：{sufficiency.get('overall_status')}",
            f"- 当前支持路径：{', '.join(sufficiency.get('supported_paths', [])) or '无'}",
            f"- 当前不支持路径：{', '.join(sufficiency.get('unsupported_paths', [])) or '无'}",
            f"- 允许 PRD 类型：{value_gate.get('allowed_prd_type')}",
            f"- 降级原因：{sufficiency.get('downgrade_reason') or '无'}",
            f"- 缺失证据类型：{', '.join(sufficiency.get('missing_evidence_types', [])) or '无'}",
            "- 禁止声称：",
        ]
    )
    lines.extend(f"  - {item}" for item in sufficiency.get("must_not_claim", []))
    lines.append("- 下一步应收集证据：")
    lines.extend(f"  - {item}" for item in sufficiency.get("next_evidence_to_collect", []))
    lines.extend(
        [
            "",
            "### 9.1 价值兑现周期",
            f"- 状态：{realization_timeline.get('status')}",
            f"- 决策影响：{realization_timeline.get('decision_effect')}",
            f"- 未知项：{', '.join(realization_timeline.get('unknowns', [])) or '无'}",
            "",
            "| 阶段 | 预期周期 | 证据状态 | 需要材料 |",
            "|---|---|---|---|",
        ]
    )
    for item in realization_timeline.get("milestones", []):
        lines.append(
            f"| {item.get('stage')} | {item.get('expected_cycle')} | {item.get('evidence_status')} | {item.get('required_material')} |"
        )
    lines.extend(
        [
            "",
            "## 10. 行业红线规则包",
            f"- 状态：{redline_pack.get('status')}",
            f"- 触发领域：{', '.join(redline_pack.get('triggered_domains', [])) or '无'}",
            f"- 场景化状态：{contextual_redline_filter.get('status')}",
            f"- 当前真正活跃领域：{', '.join(contextual_redline_filter.get('active_domains', [])) or '无'}",
            f"- 条件触发领域：{', '.join(contextual_redline_filter.get('conditional_domains', [])) or '无'}",
            f"- 已排除领域：{', '.join(contextual_redline_filter.get('excluded_domains', [])) or '无'}",
            f"- 过滤原因：{contextual_redline_filter.get('why_filtered')}",
            f"- 完整 PRD 规则：{redline_pack.get('full_prd_rule')}",
            f"- 不确定时允许路径：{redline_pack.get('allowed_when_uncertain')}",
            "- 当前活跃规则：",
        ]
    )
    lines.extend(f"  - {item}" for item in contextual_redline_filter.get("active_rules", []) or redline_pack.get("triggered_rules", []))
    if redline_pack.get("unresolved_questions"):
        lines.append("- 未解决问题：")
        lines.extend(f"  - {item}" for item in redline_pack.get("unresolved_questions", []))
    lines.extend(
        [
            "",
            "## 11. 轻量真实利润模型",
            f"- 公式：{profit_model.get('formula')}",
            f"- 当前状态：{profit_model.get('current_status')}",
            f"- 已检查成本项：{', '.join(profit_model.get('known_inputs', [])) or '无'}",
            f"- 未知输入：{', '.join(profit_model.get('unknown_inputs', [])) or '无'}",
            f"- 最小利润条件：{profit_model.get('minimum_profit_condition')}",
            f"- 计算规则：{profit_model.get('calculation_rule')}",
            "",
            "## 12. ROI 决策模型",
            f"- ROI 输入表状态：{roi_input_table.get('status')}",
            f"- 是否可计算 ROI：{'是' if roi_input_table.get('can_calculate_roi') else '否'}",
            f"- 是否允许声称高 ROI：{'是' if roi_input_table.get('can_claim_high_roi') else '否'}",
            f"- 最低可行 ROI 规则：{roi_input_table.get('minimum_viable_roi_rule')}",
            f"- ROI 缺失关键输入：{', '.join(roi_input_table.get('missing_critical_inputs', [])) or '无'}",
            "",
            "| ROI 输入项 | 当前值 | 来源状态 | 需要证据 | 决策规则 |",
            "|---|---|---|---|---|",
        ]
    )
    for item in roi_input_table.get("input_rows", []):
        lines.append(
            f"| {item.get('label')} | {item.get('current_value')} | {item.get('source_status')} | {item.get('evidence_required')} | {item.get('decision_rule')} |"
        )
    lines.extend(
        [
            "",
            f"- 状态：{roi_model.get('status')}",
            f"- 是否允许声称高 ROI：{'是' if roi_model.get('can_claim_high_roi') else '否'}",
            f"- 公式：{roi_model.get('formula')}",
            f"- 决策影响：{roi_model.get('decision_effect')}",
            f"- 升级条件：{roi_model.get('upgrade_condition')}",
            f"- 停止条件：{roi_model.get('stop_condition')}",
            "",
            "| 场景 | 计算规则 | 收入 | 获客成本 | 交付成本 | 工具成本 | 维护成本 | 预估利润 | ROI 状态 |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in roi_model.get("scenario_table", []):
        lines.append(
            f"| {item.get('scenario')} | {item.get('calculation_rule')} | {item.get('revenue')} | {item.get('acquisition_cost')} | {item.get('delivery_cost')} | {item.get('tool_cost')} | {item.get('maintenance_cost')} | {item.get('estimated_profit')} | {item.get('roi_status')} |"
        )
    lines.extend(
        [
            "",
            "### 12.1 真实利润计算与投资门禁",
            f"- 真实利润计算状态：{real_profit_calculation.get('status')}",
            f"- 是否可计算：{'是' if real_profit_calculation.get('can_calculate') else '否'}",
            f"- 缺失输入：{', '.join(real_profit_calculation.get('missing_inputs', [])) or '无'}",
            f"- 计算结论：{real_profit_calculation.get('conclusion')}",
            f"- ROI 场景状态：{roi_scenario_analysis.get('status')}",
            f"- 投资门禁结论：{investment_decision.get('conclusion')}",
            f"- 投资门禁原因：{investment_decision.get('reason')}",
            f"- 允许下一步：{investment_decision.get('allowed_next_path')}",
            f"- 阻断路径：{', '.join(investment_decision.get('blocked_paths', [])) or '无'}",
            f"- 是否需要你拍板：{'是' if investment_decision.get('requires_owner_approval') else '否'}",
            "",
            "| 场景 | 假设 | 收入 | 总成本 | 毛利 | ROI 状态 | 决策影响 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for item in roi_scenario_analysis.get("scenarios", []):
        lines.append(
            f"| {item.get('scenario')} | {item.get('assumption')} | {item.get('revenue')} | {item.get('total_cost')} | {item.get('gross_profit')} | {item.get('roi_status')} | {item.get('decision_effect')} |"
        )
    lines.extend(
        [
            "",
            "## 13. 价值质量评分表",
            f"- 总体状态：{value_quality_scorecard.get('overall_status')}",
            f"- 阻断完整 PRD 的质量项：{', '.join(value_quality_scorecard.get('blocking_items_for_full_prd', [])) or '无'}",
            f"- 规则：{value_quality_scorecard.get('full_prd_rule')}",
            "",
            "| 质量项 | 状态 | 当前判断 | 需要证据 | 决策影响 |",
            "|---|---|---|---|---|",
        ]
    )
    for item in value_quality_scorecard.get("rows", []):
        lines.append(
            f"| {item.get('label')} | {item.get('status')} | {item.get('current_judgment')} | {item.get('required_evidence')} | {item.get('decision_effect')} |"
        )
    lines.extend(
        [
            "",
            "## 14. 资源优势矩阵",
            f"- 总体状态：{resource_matrix.get('overall_status')}",
            f"- 为什么是我们做：{resource_matrix.get('why_us')}",
            f"- 声明中的资源优势：{', '.join(resource_matrix.get('claimed_resource_advantages', [])) or '无'}",
            f"- 已复核资源优势：{', '.join(resource_matrix.get('verified_resource_advantages', [])) or '无'}",
            f"- 未复核资源优势：{', '.join(resource_matrix.get('unverified_resource_advantages', [])) or '无'}",
            f"- 为什么还不能证明是我们做：{', '.join(resource_matrix.get('why_us_not_proven', [])) or '无'}",
            f"- 缺失资源：{', '.join(resource_matrix.get('missing_assets', [])) or '无'}",
            f"- 规则：{resource_matrix.get('decision_rule')}",
            "",
            "| 资源项 | 状态 | 证据状态 | 需要证据 | 决策影响 |",
            "|---|---|---|---|---|",
        ]
    )
    for item in resource_matrix.get("rows", []):
        lines.append(
            f"| {item.get('label')} | {item.get('status')} | {item.get('evidence_status')} | {item.get('required_evidence')} | {item.get('decision_effect')} |"
        )
    lines.extend(
        [
            "",
            "## 15. 获客判断表",
            f"- 总体状态：{acquisition_table.get('overall_status')}",
            f"- 阻断完整 PRD 的获客项：{', '.join(acquisition_table.get('blocking_items_for_full_prd', [])) or '无'}",
            f"- CAC/LTV 风险：{acquisition_table.get('cac_ltv_risk')}",
            f"- 规则：{acquisition_table.get('decision_rule')}",
            "",
            "| 获客项 | 状态 | 当前判断 | 需要证据 |",
            "|---|---|---|---|",
        ]
    )
    for item in acquisition_table.get("rows", []):
        lines.append(
            f"| {item.get('label')} | {item.get('status')} | {item.get('current_judgment')} | {item.get('evidence_required')} |"
        )
    lines.extend(
        [
            "",
            "## 16. 经营决策面板",
        f"- 建议打法：{operating.get('recommended_play')}",
        f"- 投入上限：{investment.get('principle', '待确认')}",
        f"- 人天上限：{investment.get('people_days', '待确认')}",
        f"- 现金成本：{investment.get('cash_cost', '待确认')}",
        f"- 工具成本：{investment.get('tool_cost', '待确认')}",
        f"- 管理精力：{investment.get('management_attention', '待确认')}",
        f"- 验证周期：{operating.get('validation_window', '待确认')}",
        f"- 最小收入目标：{'; '.join(operating.get('minimum_revenue_signal', [])) or '待确认'}",
        f"- 最小利润条件：{profit_conditions.get('condition', '待确认')}",
        f"- 客单价：{profit_conditions.get('price_floor', '待确认')}",
        f"- 单客户交付工时：{profit_conditions.get('delivery_hours_per_customer', '待确认')}",
        f"- 升级条件：{'; '.join(operating.get('upgrade_to_product_conditions', [])) or '待确认'}",
        f"- 停止条件：{'; '.join(operating.get('stop_or_downgrade_conditions', [])) or '待确认'}",
        "",
            "## 17. 为什么值得做",
    ]
    )
    basis = worth.get("evidence_basis", [])
    if basis:
        lines.extend(f"- {item}" for item in basis[:8])
    else:
        lines.append("- 当前没有足够证据证明值得做。")
    lines.extend(
        [
            "",
            "## 18. 为什么不能直接做大",
        ]
    )
    gaps = worth.get("critical_gaps", [])
    if gaps:
        lines.extend(f"- {item}" for item in gaps)
    else:
        lines.append("- 当前没有识别到阻止放大的关键缺口。")
    lines.extend(
        [
            "",
            "## 19. 当前最值得做的形态",
            f"- 推荐路径：{path.get('recommended_path')}",
            f"- 值得投入范围：{', '.join(worth.get('worth_doing_scope', [])) or '无'}",
            f"- 推荐原因：{path.get('reason')}",
            "",
            "## 20. 承接输入包完整度",
            f"- 当前承接包：{route_gate.get('route_package')}",
            f"- 完整度状态：{route_gate.get('status')}",
            f"- 是否允许进入下一模块：{'是' if route_gate.get('can_route_to_next_module') else '否'}",
            f"- 缺失字段：{', '.join(route_gate.get('missing_fields', [])) or '无'}",
            f"- 过泛字段：{', '.join(route_gate.get('over_generic_fields', [])) or '无'}",
            f"- 回退规则：{route_gate.get('fallback')}",
            "",
            "### 20.1 服务化 MVP 执行承接包",
            f"- 目标：{route_package.get('path_goal', '无')}",
            f"- 核心交付：{route_package.get('core_delivery', '无')}",
            f"- 核心反馈：{route_package.get('core_feedback', '无')}",
            f"- 服务成交路径：{' → '.join(route_package.get('service_conversion_path', [])) or '无'}",
            f"- 成功标准：{', '.join(route_package.get('success_criteria', [])) or '无'}",
            f"- 失败标准：{', '.join(route_package.get('failure_criteria', [])) or '无'}",
            f"- 执行记录模板：{', '.join(route_package.get('execution_record_template', [])) or '无'}",
            f"- 免费检测入口：{route_package.get('free_diagnosis_entry', {}).get('purpose', '无')}",
            f"- 体检报告：{route_package.get('diagnosis_report', {}).get('purpose', '无')}",
            f"- 指标看板：{route_package.get('metric_dashboard', {}).get('purpose', '无')}",
            f"- 复测机制：{route_package.get('recheck_mechanism', {}).get('purpose', '无')}",
            "",
            "### 20.2 输出边界门禁",
            f"- 状态：{output_boundary.get('status')}",
            f"- 当前路径：{output_boundary.get('route_package')}",
            f"- 规则：{output_boundary.get('rule')}",
            f"- 优先级边界：{output_boundary.get('priority_boundary_rule')}",
            f"- 检测到的越界风险：{', '.join(output_boundary.get('detected_boundary_risks', [])) or '无'}",
            f"- 允许输出：{', '.join(output_boundary.get('allowed_outputs', [])) or '无'}",
            f"- 禁止输出：{', '.join(output_boundary.get('forbidden_outputs', [])) or '无'}",
            "",
            "## 21. 当前不值得做的范围",
            f"- 不值得投入范围：{', '.join(worth.get('not_worth_doing_scope', [])) or '无'}",
            f"- 暂缓路径：{', '.join(path.get('deferred_paths', [])) or '无'}",
            f"- 阻断路径：{', '.join(path.get('blocked_paths', [])) or '无'}",
            "",
            "## 22. 关键缺口",
        ]
    )
    if blocked:
        lines.extend(f"- 阻断：{item['label']} - {item['reason']}" for item in blocked)
    if warnings:
        lines.extend(f"- 待确认：{item['label']} - {item['next_action']}" for item in warnings)
    if not blocked and not warnings:
        lines.append("- 当前没有阻断项或重要待确认项。")
    lines.extend(
        [
            "",
            "## 23. 需要你拍板的问题",
        ]
    )
    if worth.get("verdict") in {"not_worth_doing", "blocked"}:
        lines.append("- 当前结论不支持进入 PRD 路径，暂不生成 PRD 拍板项。")
    else:
        for index, item in enumerate(questions, 1):
            lines.extend(
                [
                    f"### {index}. {item.get('question')}",
                    f"- 选 A 的结果：{item.get('option_a_result')}",
                    f"- 选 B 的结果：{item.get('option_b_result')}",
                    f"- 我的建议：{item.get('recommendation')}",
                ]
            )
    lines.extend(
        [
            "",
            "## 24. 不同选择的结果",
            f"- 接受推荐路径：进入 {path.get('recommended_path')}，先验证价值闭环，避免过早重研发。",
            f"- 坚持做大：需要先补齐 {', '.join(path.get('deferred_paths', [])) or '产品化证据'} 相关证据，否则风险偏高。",
            "- 暂缓推进：保留现有证据，继续补充客户、价格、交付和复购材料。",
            "",
            "## 25. 下一步动作",
            "- 先确认是否接受“值不值得做”的判断。",
            "- 如果接受，再确认经营边界：投入上限、验证周期、最低收入信号、升级条件和停止条件。",
            "- 让 PRD 模块只读取 `00_value_gate_prd_input.json`。",
            "- PRD 中必须保留事实 / 假设 / 禁止声称边界。",
            "- PRD 中必须保留经营边界章节，不得把待确认成本或价格写成事实。",
            "",
            "## 26. 停止 / 降级条件",
        ]
    )
    stop_items = operating.get("stop_or_downgrade_conditions", []) or value_gate.get("counter_evidence", [])[:8]
    lines.extend(f"- {item}" for item in stop_items)
    lines.extend(
        [
            "",
            "## 27. 复判与证据归档",
            f"- 复判触发：{rejudgment_package.get('next_review_trigger')}",
            f"- 是否要求下一路径执行记录：{'是' if rejudgment_package.get('next_path_execution_record_required') else '否'}",
            f"- 必须记录的验证数据：{', '.join(rejudgment_package.get('required_validation_records', [])) or '无'}",
            f"- 复判输入要求：{', '.join(rejudgment_package.get('rejudgment_input_required', [])) or '无'}",
            f"- 复判材料：{', '.join(rejudgment_package.get('minimum_materials_before_rejudgment', [])) or '无'}",
            f"- 证据快照文件：{archive_policy.get('snapshot_file')}",
            f"- 原始 HTML 是否保存：{archive_policy.get('raw_html_saved')}",
            f"- 归档规则：{archive_policy.get('retention_rule')}",
            "",
            "### 27.1 复判执行计划",
            f"- 当前路径包：{rejudgment_execution.get('current_route_package')}",
            f"- 当前建议：{rejudgment_execution.get('current_recommendation')}",
            f"- 复判周期：{rejudgment_execution.get('review_window')}",
            f"- 是否需要你复核：{'是' if rejudgment_execution.get('owner_review_required') else '否'}",
            f"- 记录要求：{', '.join(rejudgment_execution.get('records_to_collect', [])) or '无'}",
            f"- 升级检查：{'; '.join(rejudgment_execution.get('upgrade_check', {}).get('conditions', [])) or '无'}",
            f"- 停止 / 降级检查：{'; '.join(rejudgment_execution.get('stop_or_downgrade_check', {}).get('conditions', [])) or '无'}",
            f"- 规则：{rejudgment_execution.get('result_rule')}",
            "",
            "## 附录：核心硬门禁评分",
            "| 门禁项 | 状态 | 原因 | 是否阻断完整 PRD | 下一步 |",
            "|---|---|---|---|---|",
            *rows(scorecard),
        ]
    )
    return "\n".join(lines)


def value_gate_owner_summary_markdown(value_gate: dict) -> str:
    worth = value_gate.get("business_worth_verdict", {})
    path = value_gate.get("path_recommendation", {})
    route_decision = value_gate.get("route_decision", {})
    sufficiency = value_gate.get("evidence_sufficiency_gate", {})
    material_summary = value_gate.get("material_intake_summary", {})
    verified_assessment = value_gate.get("verified_evidence_assessment", {})
    roi_scenario = value_gate.get("roi_scenario_analysis", {})
    investment_decision = value_gate.get("investment_decision_gate", {})
    operating = value_gate.get("operating_decision_model", {})
    route_gate = value_gate.get("route_package_completeness_gate", {})
    route_package = value_gate.get(value_gate.get("downstream_input_package"), {})

    def zh_status(value: object) -> str:
        mapping = {
            "A_ENTER_PRD": "A：完整 PRD",
            "B_LOW_COST_MVP": "B：服务化 MVP",
            "C_CLIENT_PROJECT_VALIDATION": "C：客户项目验证",
            "D_INTERNAL_EFFICIENCY": "D：内部提效",
            "E_RESEARCH_REQUIRED": "E：补调研",
            "F_NOT_RECOMMENDED": "F：不建议推进",
            "G_BLOCKED_BY_REDLINE": "G：红线阻断",
            "worth_doing": "值得做",
            "worth_testing": "值得测试",
            "worth_researching": "值得先调研",
            "not_worth_doing": "暂不值得做",
            "sufficient_for_full_prd": "足够支持完整 PRD",
            "sufficient_for_mvp": "足够支持服务化 MVP",
            "S_claimed": "S_claimed（用户声明，待复核）",
            "S_verified": "S_verified（已复核）",
            "missing_critical_materials": "关键材料缺失",
            "roi_unavailable_missing_inputs": "ROI 缺关键输入",
            "not_ready_missing_materials": "未达到复判条件",
            "needs_specificity": "需要补具体业务指标",
            "missing": "缺失",
            "complete": "完整",
        }
        return mapping.get(str(value or ""), str(value or "待确认"))

    decision_gate = value_gate.get("decision_gate")
    recommended_path = route_decision.get("recommended_path") or path.get("recommended_path") or value_gate.get("allowed_prd_type") or "待确认"
    allowed_paths = route_decision.get("allowed_paths") or path.get("allowed_paths", [])
    deferred_paths = route_decision.get("deferred_paths") or path.get("deferred_paths", [])
    blocked_paths = route_decision.get("blocked_paths") or path.get("blocked_paths", [])
    material_rows = material_summary.get("slot_rows", [])
    priority_labels = [
        "付款 / 合同证据",
        "客户 / 行业记录",
        "MVP 实验记录",
        "报价 / 客单价证据",
        "交付工时证据",
        "获客来源证据",
        "复购 / 续费 / 转介绍记录",
    ]
    priority_materials = [item for item in material_rows if item.get("label") in priority_labels][:7]
    if not priority_materials:
        priority_materials = [
            {"label": "付款 / 合同证据", "slot_status": "missing", "decision_use": "复核真实买单"},
            {"label": "报价 / 客单价证据", "slot_status": "missing", "decision_use": "计算真实利润"},
            {"label": "交付工时证据", "slot_status": "missing", "decision_use": "判断交付成本"},
        ]

    operating_window = operating.get("validation_window") or "待确认"
    minimum_revenue = "; ".join(operating.get("minimum_revenue_signal", [])) or "待确认"
    stop_conditions = operating.get("stop_or_downgrade_conditions", [])[:5]
    upgrade_conditions = operating.get("upgrade_to_product_conditions", [])[:5]
    success_criteria = route_package.get("success_criteria", [])[:6]
    failure_criteria = route_package.get("failure_criteria", [])[:6]

    lines = [
        f"# {value_gate.get('project_id')} - 商业拍板简要版",
        "",
        "## 1. 一句话结论",
        worth.get("plain_conclusion") or "待确认",
        "",
        "## 2. 当前决策面板",
        "| 项目 | 结论 |",
        "|---|---|",
        f"| 值不值得做 | {zh_status(worth.get('verdict'))} |",
        f"| 统一主路由 | {recommended_path} |",
        f"| 推荐路径 | {recommended_path} |",
        f"| 当前门禁 | {zh_status(decision_gate)} |",
        f"| 证据充分性 | {zh_status(sufficiency.get('overall_status'))} |",
        f"| 证据复核等级 | {zh_status(verified_assessment.get('status'))} |",
        f"| ROI 状态 | {zh_status(roi_scenario.get('status'))} |",
        f"| 是否允许完整 PRD | {'是' if value_gate.get('can_enter_full_prd') else '否'} |",
        f"| 投资门禁 | {zh_status(investment_decision.get('conclusion'))} |",
        "",
        "## 3. 为什么是这个结论",
        "| 依据 | 当前判断 | 对决策的影响 |",
        "|---|---|---|",
        "| 真实买单 / MVP | 用户声明存在，但仍是 S_claimed | 支持服务化 MVP，不支持直接完整 SaaS |",
        "| 外部市场 / 竞品 | 已有公开来源和竞品参照 | 证明赛道存在，不证明本项目 ROI |",
        "| 经营输入 | 客单价、获客成本、交付工时缺失 | ROI 暂不可计算 |",
        "| 产品化证据 | 多客户、复购、边际成本下降未验证 | 完整 SaaS / 重研发暂缓 |",
        "",
        "## 4. 现在可以做 / 暂缓 / 禁止",
        "| 类型 | 内容 |",
        "|---|---|",
        f"| 可以做 | {', '.join(allowed_paths) or recommended_path} |",
        f"| 暂缓做 | {', '.join(deferred_paths) or '无'} |",
        f"| 禁止做 | {', '.join(blocked_paths) or '无'} |",
        "",
        "## 5. 最需要补的证据",
        "| 优先级 | 材料 | 当前状态 | 用来判断什么 |",
        "|---|---|---|---|",
    ]
    for index, item in enumerate(priority_materials, 1):
        priority = "P0" if index <= 4 else "P1"
        lines.append(
            f"| {priority} | {item.get('label')} | {zh_status(item.get('slot_status'))} | {item.get('decision_use') or '待确认'} |"
        )

    lines.extend(
        [
            "",
            "## 6. 本轮建议怎么做",
            "| 经营项 | 建议 |",
            "|---|---|",
            f"| 建议打法 | {operating.get('recommended_play') or recommended_path} |",
            f"| 验证周期 | {operating_window} |",
            f"| 最小收入信号 | {minimum_revenue} |",
            f"| 承接包状态 | {zh_status(route_gate.get('status'))} |",
            "",
            "## 7. 升级条件",
        ]
    )
    if upgrade_conditions:
        lines.extend(f"- {item}" for item in upgrade_conditions)
    else:
        lines.append("- 待确认。")
    lines.extend(["", "## 8. 停止 / 降级条件"])
    if stop_conditions:
        lines.extend(f"- {item}" for item in stop_conditions)
    else:
        lines.append("- 待确认。")
    lines.extend(["", "## 9. 服务化 MVP 验收重点"])
    if success_criteria:
        lines.extend(f"- 成功：{item}" for item in success_criteria)
    else:
        lines.append("- 成功标准待确认。")
    if failure_criteria:
        lines.extend(f"- 失败：{item}" for item in failure_criteria[:4])
    lines.extend(
        [
            "",
            "## 10. 详细依据在哪里看",
            "- 详细证据、竞品、ROI、材料复核和红线边界见 `00_value_gate_owner_decision.md`。",
            "- PRD 模块只读取 `00_value_gate_prd_input.json`，不能把未验证内容写成事实。",
        ]
    )
    return "\n".join(lines)


def _value_gate_field(raw_text: str, fields: dict[str, str], key: str, fallback: str) -> str:
    if fields.get(key):
        return fields[key]
    return fallback if fallback in raw_text else "待验证"


def build_value_gate(
    project_id: str,
    raw_text: str,
    seed: dict | None = None,
    materials_payload: dict | None = None,
    *,
    fetch_external_evidence: bool = False,
) -> dict:
    fields = extract_template_fields(raw_text)
    value_gate_materials = normalize_value_gate_materials(materials_payload, project_id)
    request_type = infer_request_type(raw_text, fields)
    title = extract_title(raw_text, fields, project_id)
    target_users = infer_target_users(raw_text, fields)
    scenarios = infer_scenarios(raw_text, title)
    completeness = detect_value_gate_completeness(raw_text, fields)
    payment_level = detect_payment_evidence_level(raw_text)
    evidence_level = detect_evidence_level(raw_text, payment_level)
    redlines = detect_red_line_risks(raw_text)
    industry_redline_rule_pack = build_industry_redline_rule_pack(raw_text, redlines)
    contextual_redline_filter = build_contextual_redline_filter(raw_text, redlines, industry_redline_rule_pack)
    decision, blocked_reasons, verify_next = choose_value_gate_decision(
        raw_text, completeness, evidence_level, payment_level, redlines
    )
    value_judgment_passed = decision in {"A_ENTER_PRD", "C_CLIENT_PROJECT_VALIDATION", "D_INTERNAL_EFFICIENCY"}
    value_types = infer_value_type(raw_text)
    value_type_detail = infer_value_type_detail(raw_text, value_types)
    business_result_definition = infer_business_result_definition(raw_text, value_types)
    intent = detect_intent(raw_text, request_type)
    bullets = extract_bullets(raw_text)
    facts = infer_value_gate_facts(raw_text, fields, bullets, title)
    evidence_ledger = build_evidence_ledger(project_id, raw_text, facts, fetch_external=fetch_external_evidence)
    safe_facts = safe_facts_from_ledger(evidence_ledger)
    assumptions = infer_assumptions(fields, title, request_type)
    unsupported_claims = build_unsupported_claims(raw_text)
    open_questions = infer_open_questions(fields, title)
    if decision != VALUE_GATE_ALLOW_PRD:
        open_questions = unique_list(open_questions + verify_next)
    human_required = (
        decision in {"A_ENTER_PRD", "C_CLIENT_PROJECT_VALIDATION", "G_BLOCKED_BY_REDLINE"}
        and (
            bool(redlines)
            or is_geo_context(raw_text)
            or contains_any(raw_text, ("价格策略", "对外销售", "正式立项", "客户承诺", "高风险", "金融", "医疗", "法律", "支付资金"))
        )
    )
    if decision == "B_LOW_COST_MVP" and (
        is_geo_context(raw_text)
        or contains_any(raw_text, ("价格", "客单价", "客户承诺", "对外销售", "正式立项", "预算", "合同", "买单", "付费"))
    ):
        human_required = True
    human_confirmation = {
        "required": human_required,
        "confirmation_items": unique_list(
            redlines
            + (
                [
                    "客户付款意向是否真实",
                    "是否允许进入当前推荐路径",
                    "价格 / 行业 / 客户承诺边界是否确认",
                    "是否确认不得直接升级为完整 PRD",
                ]
                if human_required
                else []
            )
        ),
        "confirmed": False,
        "confirmed_by": "",
        "confirmed_at": "",
    }
    value_object_detail = infer_value_object_detail(raw_text, target_users)
    measurability = infer_measurability_judgment(raw_text)
    attribution = infer_attribution_judgment(raw_text)
    value_quality = infer_value_quality_judgment(raw_text, decision)
    true_profit = infer_true_profit_judgment(raw_text, payment_level)
    resource_fit = infer_resource_fit_judgment(raw_text)
    acquisition = infer_acquisition_judgment(raw_text)
    project_to_product = infer_project_to_product_judgment(raw_text, decision)
    low_cost_mvp = infer_low_cost_mvp_judgment(raw_text, value_object_detail["core_user"], scenarios)
    counter_evidence = infer_counter_evidence(raw_text)
    product_summary = {
        "product_name": title,
        "one_sentence_positioning": f"围绕“{title}”验证是否具备可衡量、可归因、可兑现的价值。",
        "product_type": intent["primary_intent"],
        "target_stage": "value_gate",
        "business_context": fields.get("business_context") or "待验证",
    }
    value_judgment = {
        "value_type": value_types,
        "primary_value_type": value_type_detail["primary_value_type"],
        "secondary_value_types": value_type_detail["secondary_value_types"],
        "value_type_reasoning": value_type_detail["value_type_reasoning"],
        "must_not_treat_as": value_type_detail["must_not_treat_as"],
        "core_value": "待通过真实证据验证核心价值闭环" if decision != VALUE_GATE_ALLOW_PRD else "已有较强证据，可进入完整 PRD 候选。",
        "value_object": value_object_detail,
        "business_result": business_result_definition["primary_business_result"],
        "business_result_definition": business_result_definition,
        "primary_business_result": business_result_definition["primary_business_result"],
        "secondary_business_results": business_result_definition["secondary_business_results"],
        "result_metrics": business_result_definition["result_metrics"],
        "result_not_proven_yet": business_result_definition["result_not_proven_yet"],
        "measurable_metrics": measurability["metrics"] if decision != "G_BLOCKED_BY_REDLINE" else ["红线风险确认"],
        "value_realization_cycle": "待验证",
        "value_attribution": attribution["core_question"],
    }
    risk_level = "blocked" if redlines else ("controlled" if decision == VALUE_GATE_ALLOW_PRD else "unknown")
    prd_input_package = {
        "product_summary": product_summary,
        "value_judgment": value_judgment,
        "user_and_scenario": {
            "target_users": target_users,
            "user_segments": target_users,
            "core_scenarios": scenarios,
            "trigger_scenarios": scenarios,
            "high_frequency_scenarios": scenarios[:2],
            "decision_scenarios": ["付费 / 立项 / 验收场景"] if payment_level >= 4 else ["待验证"],
        },
        "problem_definition": {
            "core_problem": infer_problem_statement(title, fields, extract_bullets(raw_text), target_users),
            "current_alternative": "待验证",
            "pain_level": "待验证",
            "loss_if_unsolved": fields.get("consequence") or "待验证",
            "why_now": "待验证",
        },
        "business_model": {
            "revenue_model": "客户付费 / 项目收入" if payment_level >= 4 else "待验证",
            "pricing_assumption": "待验证",
            "payment_willingness": f"付费证据第 {payment_level} 层" if payment_level else "无明确付费证据",
            "payment_evidence_level": payment_level,
            "profit_logic": "收入需扣除获客、交付、维护、售后、合规和风险成本。",
            "payment_evidence_detail": {
                "level": payment_level,
                "interpretation": "强付费证据" if payment_level >= 4 else ("弱付费证据" if payment_level else "无明确付费证据"),
                "must_clarify": ["谁买单", "买的是软件 / 服务 / 报告 / 咨询", "是否可复购", "是否能证明产品化"],
            },
            "true_profit_judgment": true_profit,
        },
        "productization_judgment": {
            "is_productizable": decision == VALUE_GATE_ALLOW_PRD,
            "productization_type": "完整 PRD 候选" if decision == VALUE_GATE_ALLOW_PRD else "暂不进入完整产品化",
            "standardizable_parts": project_to_product["standardizable_parts"],
            "customized_parts": project_to_product["customized_parts"],
            "replicable_parts": ["多客户、复购和边际成本下降仍需验证"],
            "not_suitable_for_productization": ["信息不足或证据不足时不得默认产品化"] if decision != VALUE_GATE_ALLOW_PRD else [],
            "project_to_product_judgment": project_to_product,
        },
        "core_value_loop": {
            "core_user_action": "完成核心任务",
            "product_response": "交付可衡量结果",
            "value_delivery": value_judgment["business_result"],
            "feedback_data": "转化、收入、效率、成本、风险指标",
            "success_signal": "真实付费、效率提升或风险降低被验证",
        },
        "mvp_boundary": {
            "must_have_core_features": low_cost_mvp["core_features"],
            "can_use_manual_or_tool_replacement": low_cost_mvp["can_replace_with_manual_or_tools"],
            "deferred_features": ["完整后台", "复杂权限", "高级数据看板", "完整商业化系统"],
            "not_do_features": low_cost_mvp["not_mvp"],
            "mvp_success_criteria": ["核心价值闭环被验证", "至少获得明确付费或效率证据"],
            "mvp_failure_criteria": ["用户只愿试用但不愿付费", "获客成本高于客单价", "交付严重依赖人工专家"],
            "low_cost_mvp_judgment": low_cost_mvp,
        },
        "risk_and_constraints": {
            "red_line_risks": redlines,
            "controllable_risks": [] if redlines else ["证据不足", "成本结构未完全验证", "获客路径未完全验证"],
            "compliance_constraints": redlines,
            "privacy_constraints": ["涉及个人或敏感数据时必须确认授权、存储和使用边界"] if contains_any(raw_text, ("数据", "隐私", "个人")) else [],
            "technical_constraints": ["待后续方案阶段判断"],
            "resource_constraints": ["团队资源、交付能力、获客渠道需验证"],
        },
        "value_object_detail": value_object_detail,
        "measurability_judgment": measurability,
        "attribution_judgment": attribution,
        "value_quality_judgment": value_quality,
        "true_profit_judgment": true_profit,
        "resource_fit_judgment": resource_fit,
        "acquisition_judgment": acquisition,
        "project_to_product_judgment": project_to_product,
        "low_cost_mvp_judgment": low_cost_mvp,
        "counter_evidence": counter_evidence,
        "evidence_and_assumptions": {
            "known_facts": facts,
            "reasonable_assumptions": assumptions,
            "evidence_level": evidence_level,
            "evidence_sources": facts,
            "unverified_assumptions": unique_list(assumptions + ["真实利润、获客路径、价值归因仍需验证"]),
            "must_validate_before_launch": verify_next or ["真实利润", "获客路径", "价值归因"],
        },
        "prd_generation_constraints": {
            "prd_scope": "只允许 A_ENTER_PRD 且输入包完整时进入完整 PRD。",
            "must_include": ["事实 / 假设分离", "价值对象", "商业结果", "衡量指标", "风险约束", "MVP 边界"],
            "must_not_include": ["不得把未验证假设写成事实", "不得绕过 decision_gate", "不得自动写长期记忆"],
            "priority_focus": ["先验证价值，再做产品设计"],
            "open_questions": open_questions,
        },
    }
    quality_gate = build_input_package_quality_gate(
        decision=decision,
        completeness=completeness,
        product_summary=product_summary,
        value_judgment=value_judgment,
        value_object_detail=value_object_detail,
        measurability=measurability,
        true_profit=true_profit,
        acquisition=acquisition,
        redlines=redlines,
        human_confirmation=human_confirmation,
    )
    execution_status = build_execution_status(
        decision=decision,
        blocked_reasons=blocked_reasons,
        redlines=redlines,
        quality_gate=quality_gate,
        human_confirmation=human_confirmation,
    )
    can_enter = execution_status == "ready_for_prd"
    route_packages = build_route_input_packages(prd_input_package, decision, blocked_reasons, verify_next, redlines)
    validation_state = build_validation_state(decision, execution_status, blocked_reasons, counter_evidence)
    hard_gate_scorecard = build_hard_gate_scorecard(
        raw_text=raw_text,
        decision=decision,
        evidence_level=evidence_level,
        payment_level=payment_level,
        redlines=redlines,
        value_object_detail=value_object_detail,
        value_judgment=value_judgment,
        measurability=measurability,
        attribution=attribution,
        true_profit=true_profit,
        acquisition=acquisition,
        resource_fit=resource_fit,
        project_to_product=project_to_product,
    )
    path_recommendation = build_path_recommendation(raw_text, decision, redlines, hard_gate_scorecard)
    business_worth_verdict = build_business_worth_verdict(raw_text, decision, path_recommendation, hard_gate_scorecard, safe_facts)
    evidence_decision_basis = build_evidence_decision_basis(evidence_ledger)
    verified_evidence_gate = build_verified_evidence_gate(evidence_decision_basis, payment_level)
    payment_evidence_verification = build_payment_evidence_verification(payment_level, verified_evidence_gate)
    evidence_verification_intake = build_evidence_verification_intake(verified_evidence_gate)
    competitor_benchmark_table = build_competitor_benchmark_table(raw_text, fetch_external=fetch_external_evidence)
    evidence_to_verdict_reasoning = build_evidence_to_verdict_reasoning(business_worth_verdict, evidence_decision_basis)
    evidence_sufficiency_gate = build_evidence_sufficiency_gate(
        raw_text=raw_text,
        decision=decision,
        evidence_level=evidence_level,
        payment_level=payment_level,
        completeness=completeness,
        redlines=redlines,
        scorecard=hard_gate_scorecard,
        evidence_basis=evidence_decision_basis,
    )
    allowed_prd_type = allowed_prd_type_for_decision(decision)
    operating_decision_model = build_operating_decision_model(raw_text, decision, path_recommendation, business_worth_verdict)
    value_realization_timeline = build_value_realization_timeline(raw_text, decision, operating_decision_model)
    lightweight_profit_model = build_lightweight_profit_model(true_profit, operating_decision_model, payment_level)
    material_intake_summary = build_material_intake_summary(value_gate_materials)
    material_to_evidence_mapping = build_material_to_evidence_mapping(value_gate_materials)
    rejudgment_readiness_gate = build_rejudgment_readiness_gate(material_intake_summary, material_to_evidence_mapping)
    verified_evidence_assessment = build_verified_evidence_assessment(material_intake_summary, material_to_evidence_mapping)
    s_claimed_to_s_verified_gate = build_s_claimed_to_s_verified_gate(
        verified_evidence_assessment,
        material_intake_summary,
        rejudgment_readiness_gate,
    )
    material_roi_values = build_material_roi_values(material_to_evidence_mapping)
    roi_input_table = build_roi_input_table(raw_text, operating_decision_model, true_profit, material_roi_values)
    value_quality_scorecard = build_value_quality_scorecard(value_quality, project_to_product)
    resource_advantage_matrix = build_resource_advantage_matrix(resource_fit)
    acquisition_decision_table = build_acquisition_decision_table(acquisition, roi_input_table)
    evidence_grade_gate = build_evidence_grade_gate(
        decision=decision,
        evidence_level=evidence_level,
        payment_level=payment_level,
        evidence_basis=evidence_decision_basis,
        sufficiency_gate=evidence_sufficiency_gate,
    )
    roi_decision_model = build_roi_decision_model(
        true_profit=true_profit,
        operating_model=operating_decision_model,
        evidence_sufficiency_gate=evidence_sufficiency_gate,
        evidence_grade_gate=evidence_grade_gate,
        roi_input_table=roi_input_table,
    )
    route_package_completeness_gate = build_route_package_completeness_gate(
        VALUE_GATE_ROUTE_PACKAGE[decision],
        prd_input_package if VALUE_GATE_ROUTE_PACKAGE[decision] == "prd_input_package" else route_packages[VALUE_GATE_ROUTE_PACKAGE[decision]],
    )
    rejudgment_package = build_rejudgment_package(
        validation_state,
        evidence_sufficiency_gate,
        operating_decision_model,
        VALUE_GATE_ROUTE_PACKAGE[decision],
    )
    current_route_package_name = VALUE_GATE_ROUTE_PACKAGE[decision]
    current_route_package = (
        prd_input_package
        if current_route_package_name == "prd_input_package"
        else route_packages[current_route_package_name]
    )
    source_quality_gate = build_source_quality_gate(
        evidence_basis=evidence_decision_basis,
        competitor_table=competitor_benchmark_table,
        evidence_sufficiency_gate=evidence_sufficiency_gate,
        verified_gate=verified_evidence_gate,
        payment_verification=payment_evidence_verification,
        roi_input_table=roi_input_table,
    )
    evidence_research_agent = build_evidence_research_agent(
        evidence_sufficiency_gate=evidence_sufficiency_gate,
        source_quality_gate=source_quality_gate,
        evidence_verification_intake=evidence_verification_intake,
        route_package_name=current_route_package_name,
        competitor_table=competitor_benchmark_table,
    )
    attachment_verification_plan = build_attachment_verification_plan(evidence_verification_intake)
    rejudgment_execution_plan = build_rejudgment_execution_plan(
        route_package_name=current_route_package_name,
        route_package=current_route_package,
        rejudgment_package=rejudgment_package,
        operating_model=operating_decision_model,
        evidence_sufficiency_gate=evidence_sufficiency_gate,
    )
    research_execution_queue = build_research_execution_queue(
        evidence_research_agent=evidence_research_agent,
        source_quality_gate=source_quality_gate,
        attachment_verification_plan=attachment_verification_plan,
        rejudgment_execution_plan=rejudgment_execution_plan,
    )
    external_research_results = build_external_research_results(
        evidence_decision_basis,
        competitor_benchmark_table,
        research_execution_queue,
    )
    source_quality_scorecard = build_source_quality_scorecard(external_research_results, source_quality_gate)
    competitor_pricing_evidence = build_competitor_pricing_evidence(evidence_decision_basis, competitor_benchmark_table)
    platform_rule_evidence = build_platform_rule_evidence(evidence_decision_basis, contextual_redline_filter)
    real_profit_calculation = build_real_profit_calculation(roi_input_table, verified_evidence_assessment)
    roi_scenario_analysis = build_roi_scenario_analysis(roi_input_table, real_profit_calculation)
    investment_decision_gate = build_investment_decision_gate(
        roi_scenario_analysis,
        rejudgment_readiness_gate,
        s_claimed_to_s_verified_gate,
    )
    output_boundary_gate = build_output_boundary_gate(decision, VALUE_GATE_ROUTE_PACKAGE[decision])
    route_decision = build_route_decision(
        decision=decision,
        allowed_prd_type=allowed_prd_type,
        execution_status=execution_status,
        can_enter_full_prd=can_enter,
        path_recommendation=path_recommendation,
        business_worth_verdict=business_worth_verdict,
        evidence_sufficiency_gate=evidence_sufficiency_gate,
        material_intake_summary=material_intake_summary,
        roi_scenario_analysis=roi_scenario_analysis,
        investment_decision_gate=investment_decision_gate,
        route_package_completeness_gate=route_package_completeness_gate,
    )
    decision_questions = build_decision_questions(raw_text, path_recommendation)
    payload = {
        "project_id": project_id,
        "module": "product_value_gate",
        "version": VALUE_GATE_VERSION,
        "agent": {
            "name": VALUE_GATE_AGENT_NAME,
            "mode": "evidence_fetcher_rule_agent_v0",
            "responsibilities": ["evidence_collection", "commercial_judgment", "prd_input_sanitization", "owner_decision_report"],
            "does_not_do": ["generate_full_prd", "write_long_term_memory", "promote_candidate_to_stable", "create_skill_or_harness"],
        },
        "evidence_fetcher": {
            "enabled": fetch_external_evidence,
            "scope": "external_public_source_urls_only",
            "raw_snapshot_saved": False,
            "rule": "只校验公开来源可达性和摘录，不自动把外部信息提升为商业价值成立证据。",
        },
        "decision_gate": decision,
        "route_decision": route_decision,
        "allowed_prd_type": allowed_prd_type,
        "value_judgment_passed": value_judgment_passed,
        "execution_status": execution_status,
        "can_enter_full_prd": can_enter,
        "next_module": VALUE_GATE_NEXT_MODULE[decision],
        "evidence_level": evidence_level,
        "payment_evidence_level": payment_level,
        "risk_level": risk_level,
        "required_human_confirmation": human_required,
        "blocked_reasons": blocked_reasons,
        "must_verify_before_next_step": verify_next,
        "human_confirmation": human_confirmation,
        "intent_result": intent,
        "input_completeness": completeness,
        "input_package_quality_gate": quality_gate,
        "prd_input_package": prd_input_package,
        "mvp_input_package": route_packages["mvp_input_package"],
        "client_project_input_package": route_packages["client_project_input_package"],
        "internal_efficiency_input_package": route_packages["internal_efficiency_input_package"],
        "research_input_package": route_packages["research_input_package"],
        "stop_reason_package": route_packages["stop_reason_package"],
        "redline_block_package": route_packages["redline_block_package"],
        "downstream_input_package": VALUE_GATE_ROUTE_PACKAGE[decision],
        "evidence_ledger": evidence_ledger,
        "safe_facts_for_prd": safe_facts,
        "assumptions_for_prd": unique_list(assumptions + prd_input_package["evidence_and_assumptions"]["unverified_assumptions"]),
        "blocked_claims": unsupported_claims,
        "unsupported_claims": unsupported_claims,
        "hard_gate_scorecard": hard_gate_scorecard,
        "path_recommendation": path_recommendation,
        "business_worth_verdict": business_worth_verdict,
        "material_intake_summary": material_intake_summary,
        "material_to_evidence_mapping": material_to_evidence_mapping,
        "rejudgment_readiness_gate": rejudgment_readiness_gate,
        "external_research_results": external_research_results,
        "source_quality_scorecard": source_quality_scorecard,
        "competitor_pricing_evidence": competitor_pricing_evidence,
        "platform_rule_evidence": platform_rule_evidence,
        "verified_evidence_assessment": verified_evidence_assessment,
        "s_claimed_to_s_verified_gate": s_claimed_to_s_verified_gate,
        "real_profit_calculation": real_profit_calculation,
        "roi_scenario_analysis": roi_scenario_analysis,
        "investment_decision_gate": investment_decision_gate,
        "evidence_sufficiency_gate": evidence_sufficiency_gate,
        "source_quality_gate": source_quality_gate,
        "evidence_research_agent": evidence_research_agent,
        "research_execution_queue": research_execution_queue,
        "evidence_grade_gate": evidence_grade_gate,
        "verified_evidence_gate": verified_evidence_gate,
        "payment_evidence_verification": payment_evidence_verification,
        "evidence_verification_intake": evidence_verification_intake,
        "attachment_verification_plan": attachment_verification_plan,
        "competitor_benchmark_table": competitor_benchmark_table,
        "industry_redline_rule_pack": industry_redline_rule_pack,
        "contextual_redline_filter": contextual_redline_filter,
        "value_realization_timeline": value_realization_timeline,
        "value_quality_scorecard": value_quality_scorecard,
        "resource_advantage_matrix": resource_advantage_matrix,
        "acquisition_decision_table": acquisition_decision_table,
        "lightweight_profit_model": lightweight_profit_model,
        "roi_input_table": roi_input_table,
        "roi_decision_model": roi_decision_model,
        "output_boundary_gate": output_boundary_gate,
        "route_package_completeness_gate": route_package_completeness_gate,
        "rejudgment_package": rejudgment_package,
        "rejudgment_execution_plan": rejudgment_execution_plan,
        "evidence_decision_basis": evidence_decision_basis,
        "evidence_to_verdict_reasoning": evidence_to_verdict_reasoning,
        "operating_decision_model": operating_decision_model,
        "decision_questions": decision_questions,
        "known_facts": facts,
        "reasonable_assumptions": assumptions,
        "unverified_assumptions": prd_input_package["evidence_and_assumptions"]["unverified_assumptions"],
        "open_questions": open_questions,
        "red_line_risks": redlines,
        "counter_evidence": counter_evidence,
        "review_loop": build_review_loop(decision, blocked_reasons, counter_evidence),
        "validation_state": validation_state,
        "conflict_review": {
            "status": "no_blocking_conflict",
            "items": VALUE_GATE_CONFLICT_ITEMS,
        },
    }
    payload["evidence_archive_policy"] = build_evidence_archive_policy(payload)
    if seed:
        payload["previous_value_gate"] = {
            "decision_gate": seed.get("decision_gate", ""),
            "version": seed.get("version", ""),
        }
    return payload


def value_gate_allows_full_prd(value_gate: dict) -> bool:
    if not value_gate:
        return False
    if value_gate.get("decision_gate") != VALUE_GATE_ALLOW_PRD:
        return False
    if value_gate.get("value_judgment_passed") is not True:
        return False
    if value_gate.get("execution_status") != "ready_for_prd":
        return False
    if value_gate.get("can_enter_full_prd") is not True:
        return False
    if value_gate.get("allowed_prd_type") != "完整 PRD":
        return False
    sufficiency = value_gate.get("evidence_sufficiency_gate", {})
    if sufficiency.get("overall_status") != "sufficient_for_full_prd":
        return False
    evidence_grade_gate = value_gate.get("evidence_grade_gate", {})
    if evidence_grade_gate.get("status") != "passes_current_gate":
        return False
    roi_decision_model = value_gate.get("roi_decision_model", {})
    if roi_decision_model.get("status") == "roi_not_proven":
        return False
    route_gate = value_gate.get("route_package_completeness_gate", {})
    if route_gate and route_gate.get("can_route_to_next_module") is not True:
        return False
    if value_gate.get("blocked_reasons"):
        return False
    human_confirmation = value_gate.get("human_confirmation", {})
    if value_gate.get("required_human_confirmation") and not human_confirmation.get("confirmed"):
        return False
    package = value_gate.get("prd_input_package", {})
    if not isinstance(package, dict) or not package:
        return False
    quality_gate = value_gate.get("input_package_quality_gate", {})
    if quality_gate.get("content_ready_for_prd") is not True:
        return False
    completeness = value_gate.get("input_completeness", {})
    return completeness.get("is_complete_for_prd") is True


def value_gate_block_message(value_gate: dict, path: Path | None = None) -> str:
    if not value_gate:
        return "Missing product value gate. Run stage `value_gate` before full PRD generation."
    reasons = value_gate.get("blocked_reasons") or []
    reason_text = "；".join(str(item) for item in reasons) if reasons else "value gate did not allow full PRD."
    location = f" ({path})" if path else ""
    return (
        f"Value gate blocked full PRD{location}: decision_gate={value_gate.get('decision_gate')}, "
        f"execution_status={value_gate.get('execution_status')}, "
        f"can_enter_full_prd={value_gate.get('can_enter_full_prd')}. {reason_text}"
    )


def value_gate_to_brief_seed(value_gate: dict) -> dict:
    if not value_gate:
        return {}
    package = value_gate.get("prd_input_package", {})
    product_summary = package.get("product_summary", {})
    user_scenario = package.get("user_and_scenario", {})
    problem = package.get("problem_definition", {})
    value = package.get("value_judgment", {})
    evidence = package.get("evidence_and_assumptions", {})
    scope = package.get("mvp_boundary", {})
    return {
        "title": product_summary.get("product_name"),
        "business_context": product_summary.get("business_context"),
        "problem_statement": problem.get("core_problem"),
        "target_users": user_scenario.get("target_users"),
        "scenarios": user_scenario.get("core_scenarios"),
        "business_goal": value.get("business_result"),
        "evidence": evidence.get("evidence_sources"),
        "facts": evidence.get("known_facts"),
        "assumptions": evidence.get("reasonable_assumptions"),
        "open_questions": package.get("prd_generation_constraints", {}).get("open_questions"),
        "suggested_scope": {
            "mvp": scope.get("must_have_core_features", []),
            "v1": scope.get("can_use_manual_or_tool_replacement", []),
            "later": scope.get("deferred_features", []),
        },
    }


def value_gate_markdown(value_gate: dict) -> str:
    package = value_gate.get("prd_input_package", {})
    product_summary = package.get("product_summary", {})
    value_judgment = package.get("value_judgment", {})
    completeness = value_gate.get("input_completeness", {})
    business_model = package.get("business_model", {})
    value_object_detail = package.get("value_object_detail", {})
    measurability = package.get("measurability_judgment", {})
    attribution = package.get("attribution_judgment", {})
    value_quality = package.get("value_quality_judgment", {})
    true_profit = package.get("true_profit_judgment", {})
    resource_fit = package.get("resource_fit_judgment", {})
    acquisition = package.get("acquisition_judgment", {})
    project_to_product = package.get("project_to_product_judgment", {})
    low_cost_mvp = package.get("low_cost_mvp_judgment", {})
    review_loop = value_gate.get("review_loop", {})
    quality_gate = value_gate.get("input_package_quality_gate", {})
    validation_state = value_gate.get("validation_state", {})
    sufficiency = value_gate.get("evidence_sufficiency_gate", {})
    verified_gate = value_gate.get("verified_evidence_gate", {})
    payment_verification = value_gate.get("payment_evidence_verification", {})
    verification_intake = value_gate.get("evidence_verification_intake", {})
    competitor_table = value_gate.get("competitor_benchmark_table", {})
    redline_pack = value_gate.get("industry_redline_rule_pack", {})
    profit_model = value_gate.get("lightweight_profit_model", {})
    roi_input_table = value_gate.get("roi_input_table", {})
    value_quality_scorecard = value_gate.get("value_quality_scorecard", {})
    resource_matrix = value_gate.get("resource_advantage_matrix", {})
    acquisition_table = value_gate.get("acquisition_decision_table", {})
    archive_policy = value_gate.get("evidence_archive_policy", {})
    realization_timeline = value_gate.get("value_realization_timeline", {})
    output_boundary = value_gate.get("output_boundary_gate", {})
    rejudgment_package = value_gate.get("rejudgment_package", {})

    def list_text(items) -> str:
        if isinstance(items, list):
            return "、".join(str(item) for item in items) if items else "无"
        return str(items) if items else "待验证"

    lines = [
        f"# {product_summary.get('product_name') or value_gate.get('project_id')} - 产品价值门禁",
        "",
        "## 1. 门禁结论",
        f"- version：{value_gate.get('version')}",
        f"- decision_gate：{value_gate.get('decision_gate')}",
        f"- value_judgment_passed：{value_gate.get('value_judgment_passed')}",
        f"- execution_status：{value_gate.get('execution_status')}",
        f"- can_enter_full_prd：{value_gate.get('can_enter_full_prd')}",
        f"- allowed_prd_type：{value_gate.get('allowed_prd_type')}",
        f"- evidence_sufficiency：{sufficiency.get('overall_status')}",
        f"- verified_evidence：{verified_gate.get('status')}",
        f"- evidence_verification_intake：{verification_intake.get('status')}",
        f"- roi_input_table：{roi_input_table.get('status')}",
        f"- value_realization_timeline：{realization_timeline.get('status')}",
        f"- output_boundary：{output_boundary.get('status')}",
        f"- redline_pack_status：{redline_pack.get('status')}",
        f"- evidence_snapshot：{archive_policy.get('snapshot_file')}",
        f"- next_module：{value_gate.get('next_module')}",
        f"- evidence_level：{value_gate.get('evidence_level')}",
        f"- payment_evidence_level：{value_gate.get('payment_evidence_level')}",
        f"- payment_claimed_layer：{payment_verification.get('claimed_payment_layer')}",
        f"- payment_verified_layer：{payment_verification.get('verified_payment_layer')}",
        f"- risk_level：{value_gate.get('risk_level')}",
        f"- required_human_confirmation：{value_gate.get('required_human_confirmation')}",
        f"- downstream_input_package：{value_gate.get('downstream_input_package')}",
        "",
        "## 2. 为什么是这个结论",
    ]
    if value_gate.get("blocked_reasons"):
        lines.extend(f"- {item}" for item in value_gate.get("blocked_reasons", []))
    else:
        lines.append("- 当前证据和输入完整度满足价值判断最低门槛。")
    if value_gate.get("execution_status") == "pending_human_confirmation":
        lines.append("- 价值判断已通过，但人工确认未完成，正式 PRD 仍被硬门禁阻断。")
    elif value_gate.get("execution_status") == "ready_for_prd":
        lines.append("- 价值判断、输入包质量、风险和人工确认均已满足，可以进入正式 PRD。")
    elif value_gate.get("can_enter_full_prd") is not True:
        lines.append("- 当前不能进入正式 PRD，应按 execution_status 路由到对应验证路径。")
    if sufficiency.get("downgrade_reason"):
        lines.append(f"- 证据充分性降级原因：{sufficiency.get('downgrade_reason')}")
    if sufficiency.get("unsupported_paths"):
        lines.append(f"- 当前证据不支持：{'、'.join(sufficiency.get('unsupported_paths', []))}")
    lines.extend(["", "## 3. 意图与价值判断"])
    intent = value_gate.get("intent_result", {})
    lines.extend(
        [
            f"- 主意图：{intent.get('primary_intent')}",
            f"- 次级意图：{list_text(intent.get('secondary_intents', []))}",
            f"- 价值类型：{list_text(value_judgment.get('value_type', []))}",
            f"- 主价值类型：{value_judgment.get('primary_value_type')}",
            f"- 次级价值类型：{list_text(value_judgment.get('secondary_value_types', []))}",
            f"- 价值类型判断：{value_judgment.get('value_type_reasoning')}",
            f"- 商业结果：{value_judgment.get('business_result')}",
            f"- 次级商业结果：{list_text(value_judgment.get('secondary_business_results', []))}",
            f"- 当前不能证明：{list_text(value_judgment.get('result_not_proven_yet', []))}",
            f"- 核心价值：{value_judgment.get('core_value')}",
            f"- 价值归因：{attribution.get('core_question')}",
            f"- 归因影响因素：{list_text(attribution.get('influencing_factors', []))}",
        ]
    )
    lines.extend(["", "## 4. 输入完整度"])
    lines.append(f"- 已覆盖：{'、'.join(completeness.get('present_items', [])) or '无'}")
    lines.append(f"- 缺失：{'、'.join(completeness.get('missing_items', [])) or '无'}")
    lines.append(f"- 输入包质量：{quality_gate.get('overall_status')}")
    lines.append(f"- 内容是否已达 PRD 输入标准：{quality_gate.get('content_ready_for_prd')}")
    if quality_gate.get("missing_items"):
        lines.append(f"- 质量缺失项：{list_text(quality_gate.get('missing_items', []))}")
    if quality_gate.get("over_generic_items"):
        lines.append(f"- 过泛项：{list_text(quality_gate.get('over_generic_items', []))}")
    if quality_gate.get("human_confirmation_items"):
        lines.append(f"- 需人工确认项：{list_text(quality_gate.get('human_confirmation_items', []))}")
    lines.extend(["", "## 5. 证据与假设"])
    lines.append("### 5.1 已知事实 / 证据")
    lines.extend(f"- {item}" for item in value_gate.get("known_facts", []))
    lines.append("")
    lines.append("### 5.1.1 国内外竞品标杆")
    lines.append(f"- 状态：{competitor_table.get('status')}")
    lines.append(f"- 决策规则：{competitor_table.get('decision_rule')}")
    lines.append("| 竞品 | 市场 | 链接 | 重点能力 | 标杆信号 |")
    lines.append("|---|---|---|---|---|")
    for item in competitor_table.get("rows", []):
        source_url = item.get("source_url")
        source = f"[{item.get('source_title') or item.get('name')}]({source_url})" if source_url else item.get("name")
        lines.append(
            f"| {item.get('name')} | {item.get('market')} | {source} | {item.get('focus')} | {item.get('benchmark_signal')} |"
        )
    lines.append("")
    lines.append("### 5.2 合理假设")
    lines.extend(f"- {item}" for item in value_gate.get("reasonable_assumptions", []))
    lines.append("")
    lines.append("### 5.3 未验证假设")
    lines.extend(f"- {item}" for item in value_gate.get("unverified_assumptions", []))
    lines.append("")
    lines.append("### 5.4 开放问题")
    lines.extend(f"- {item}" for item in value_gate.get("open_questions", []))
    lines.extend(["", "## 6. 价值对象"])
    lines.extend(
        [
            f"- 核心用户：{list_text(value_object_detail.get('core_user'))}",
            f"- 付费者：{list_text(value_object_detail.get('payer'))}",
            f"- 决策者：{list_text(value_object_detail.get('decision_maker'))}",
            f"- 使用者：{list_text(value_object_detail.get('user'))}",
            f"- 受益者：{list_text(value_object_detail.get('beneficiary'))}",
            f"- 成本承担者：{list_text(value_object_detail.get('cost_bearer'))}",
            f"- 验收方：{list_text(value_object_detail.get('acceptance_owner'))}",
            f"- 复购影响者：{list_text(value_object_detail.get('renewal_influencer'))}",
            f"- 潜在反对者：{list_text(value_object_detail.get('possible_opponents'))}",
        ]
    )
    lines.extend(["", "## 7. 商业结果与衡量指标"])
    lines.extend(
        [
            f"- 是否可衡量：{measurability.get('is_measurable')}",
            f"- 应衡量指标：{list_text(measurability.get('metrics', []))}",
            f"- 缺失指标：{list_text(measurability.get('missing_metrics', []))}",
            f"- 判断：{measurability.get('judgment')}",
            f"- 基线指标：{list_text(attribution.get('baseline_metrics', []))}",
            f"- 产品 / 服务动作：{list_text(attribution.get('product_or_service_actions', []))}",
            f"- 外部干扰因素：{list_text(attribution.get('external_interference_factors', []))}",
            f"- 归因风险：{attribution.get('attribution_risk')}",
        ]
    )
    lines.extend(["", "## 8. 真实利润与成本"])
    lines.extend(
        [
            f"- 收益模式：{business_model.get('revenue_model')}",
            f"- 付费证据：{business_model.get('payment_willingness')}",
            f"- 利润状态：{true_profit.get('status')}",
            f"- 客单价假设：{true_profit.get('price_assumption')}",
            f"- 获客成本假设：{true_profit.get('acquisition_cost_assumption')}",
            f"- 交付工时假设：{true_profit.get('delivery_hours_assumption')}",
            f"- 人工复核成本假设：{true_profit.get('human_review_cost_assumption')}",
            f"- 维护 / 售后成本假设：{true_profit.get('maintenance_after_sales_cost_assumption')}",
            f"- 已识别成本：{list_text(true_profit.get('cost_items_checked', []))}",
            f"- 缺失成本：{list_text(true_profit.get('missing_cost_items', []))}",
            f"- 最小利润成立条件：{true_profit.get('minimum_profit_condition')}",
            f"- 利润风险：{true_profit.get('profit_risk')}",
            f"- 下一步核算：{true_profit.get('next_calculation')}",
            f"- 轻量利润模型：{profit_model.get('formula')}",
            f"- 利润未知输入：{list_text(profit_model.get('unknown_inputs', []))}",
        ]
    )
    lines.extend(["", "## 9. 获客与资源匹配"])
    lines.extend(
        [
            f"- 资源匹配：{resource_fit.get('status')}",
            f"- 可用资产：{list_text(resource_fit.get('available_assets', []))}",
            f"- 缺失资产：{list_text(resource_fit.get('missing_assets', []))}",
            f"- 第一批用户：{list_text(acquisition.get('first_users', []))}",
            f"- 触达方式：{acquisition.get('reach_method')}",
            f"- 信任基础：{list_text(acquisition.get('trust_basis', []))}",
            f"- CAC/LTV 风险：{acquisition.get('cac_ltv_risk')}",
        ]
    )
    lines.extend(
        [
            "",
            "### 9.1 价值质量评分表",
            f"- 总体状态：{value_quality_scorecard.get('overall_status')}",
            f"- 阻断完整 PRD 的质量项：{list_text(value_quality_scorecard.get('blocking_items_for_full_prd', []))}",
            "| 质量项 | 状态 | 当前判断 | 需要证据 |",
            "|---|---|---|---|",
        ]
    )
    for item in value_quality_scorecard.get("rows", []):
        lines.append(
            f"| {item.get('label')} | {item.get('status')} | {item.get('current_judgment')} | {item.get('required_evidence')} |"
        )
    lines.extend(
        [
            "",
            "### 9.2 资源优势矩阵",
            f"- 总体状态：{resource_matrix.get('overall_status')}",
            f"- 缺失资源：{list_text(resource_matrix.get('missing_assets', []))}",
            f"- 声明中的资源优势：{list_text(resource_matrix.get('claimed_resource_advantages', []))}",
            f"- 已复核资源优势：{list_text(resource_matrix.get('verified_resource_advantages', []))}",
            f"- 未复核资源优势：{list_text(resource_matrix.get('unverified_resource_advantages', []))}",
            f"- 还不能证明是我们做的原因：{list_text(resource_matrix.get('why_us_not_proven', []))}",
            "| 资源项 | 状态 | 证据状态 | 需要证据 |",
            "|---|---|---|---|",
        ]
    )
    for item in resource_matrix.get("rows", []):
        lines.append(
            f"| {item.get('label')} | {item.get('status')} | {item.get('evidence_status')} | {item.get('required_evidence')} |"
        )
    lines.extend(
        [
            "",
            "### 9.3 获客判断表",
            f"- 总体状态：{acquisition_table.get('overall_status')}",
            f"- 阻断完整 PRD 的获客项：{list_text(acquisition_table.get('blocking_items_for_full_prd', []))}",
            "| 获客项 | 状态 | 当前判断 | 需要证据 |",
            "|---|---|---|---|",
        ]
    )
    for item in acquisition_table.get("rows", []):
        lines.append(
            f"| {item.get('label')} | {item.get('status')} | {item.get('current_judgment')} | {item.get('evidence_required')} |"
        )
    lines.extend(["", "## 10. 项目转产品判断"])
    lines.extend(
        [
            f"- 项目价值：{project_to_product.get('project_value')}",
            f"- 服务价值：{project_to_product.get('service_value')}",
            f"- 产品价值：{project_to_product.get('product_value')}",
            f"- 可标准化部分：{list_text(project_to_product.get('standardizable_parts', []))}",
            f"- 需定制部分：{list_text(project_to_product.get('customized_parts', []))}",
            f"- 产品化风险：{project_to_product.get('productization_risk')}",
        ]
    )
    lines.extend(["", "## 11. MVP / PRD 输入建议"])
    lines.extend(
        [
            f"- 核心用户：{list_text(low_cost_mvp.get('core_user', []))}",
            f"- 核心场景：{list_text(low_cost_mvp.get('core_scenario', []))}",
            f"- 核心功能：{list_text(low_cost_mvp.get('core_features', []))}",
            f"- 核心交付：{low_cost_mvp.get('core_delivery')}",
            f"- 最小数据闭环：{list_text(low_cost_mvp.get('minimum_data_loop', []))}",
            f"- 可人工 / 工具替代：{list_text(low_cost_mvp.get('can_replace_with_manual_or_tools', []))}",
        ]
    )
    lines.extend(["", "## 12. 风险与红线"])
    lines.append(f"- 红线规则包状态：{redline_pack.get('status')}")
    lines.append(f"- 触发领域：{list_text(redline_pack.get('triggered_domains', []))}")
    if redline_pack.get("triggered_rules"):
        lines.append("### 12.1 触发规则")
        lines.extend(f"- {item}" for item in redline_pack.get("triggered_rules", []))
    if redline_pack.get("unresolved_questions"):
        lines.append("### 12.2 未解决问题")
        lines.extend(f"- {item}" for item in redline_pack.get("unresolved_questions", []))
    if value_gate.get("red_line_risks"):
        lines.extend(f"- {item}" for item in value_gate.get("red_line_risks", []))
    else:
        lines.append("- 当前版本未识别到明确不可控红线；后续仍需人工确认具体行业边界。")
    lines.extend(["", "## 13. 反证与停止条件"])
    lines.extend(f"- {item}" for item in value_gate.get("counter_evidence", []))
    lines.extend(["", "## 14. 复判计划"])
    lines.extend(
        [
            f"- 当前状态：{validation_state.get('current_status') or review_loop.get('current_status')}",
            f"- 当前轮次：{validation_state.get('validation_round') or review_loop.get('validation_round')}",
            f"- 下次复判触发：{validation_state.get('next_review_trigger') or review_loop.get('next_review_trigger')}",
            f"- 是否要求下一路径执行记录：{'是' if rejudgment_package.get('next_path_execution_record_required') else '否'}",
            f"- 必须记录的验证数据：{list_text(rejudgment_package.get('required_validation_records', []))}",
            f"- 复判输入要求：{list_text(rejudgment_package.get('rejudgment_input_required', []))}",
            f"- 复判材料：{list_text(validation_state.get('next_review_materials') or review_loop.get('next_review_materials', []))}",
        ]
    )
    lines.append("### 14.1 成功标准")
    lines.extend(f"- {item}" for item in (validation_state.get("success_criteria") or review_loop.get("success_criteria", [])))
    lines.append("### 14.2 失败标准")
    lines.extend(f"- {item}" for item in (validation_state.get("failure_criteria") or review_loop.get("failure_criteria", [])))
    lines.extend(["", "## 15. 后续输入包"])
    lines.append(f"- 当前应进入：{value_gate.get('downstream_input_package')}")
    constraints = package.get("prd_generation_constraints", {})
    lines.append(f"- PRD 约束：{constraints.get('prd_scope')}")
    lines.append(f"- 执行状态：{value_gate.get('execution_status')}")
    lines.extend(["", "## 16. txt 功能 vs 治理架构对照"])
    lines.extend(
        f"- {item['function']}：{item['classification']}。{item['governance_check']} 建议：{item['recommendation']}"
        for item in value_gate.get("conflict_review", {}).get("items", [])
    )
    return "\n".join(lines)


def classify_open_question_priority(question: str) -> str:
    p0_terms = [
        "目标用户",
        "用户",
        "MVP",
        "范围",
        "商业模式",
        "收费",
        "权限",
        "合规",
        "数据源",
        "授权",
        "AI",
        "模型",
        "上线",
        "平台",
        "端",
        "主路径",
    ]
    p1_terms = ["字段", "文案", "提醒", "导出", "筛选", "排序", "看板", "埋点"]
    if any(term in question for term in p0_terms):
        return "P0"
    if any(term in question for term in p1_terms):
        return "P1"
    return "P2"


def mermaid_label(value: object, fallback: str = "待补充") -> str:
    text = str(value or fallback).strip() or fallback
    return text.replace('"', "'").replace("\n", " ")[:48]


def limited_items(items: list[str] | None, fallback: list[str], limit: int = 5) -> list[str]:
    cleaned = [str(item).strip() for item in (items or []) if str(item).strip()]
    return (cleaned or fallback)[:limit]


def mermaid_block(lines: list[str]) -> str:
    return "```mermaid\n" + "\n".join(lines) + "\n```"


def infer_page_modules(title: str) -> list[str]:
    if "导出" in title:
        return ["导出入口 / 流水列表", "导出任务详情", "字段与权限配置", "导出记录 / 审计日志"]
    if "审核" in title or "审批" in title:
        return ["审核工作台", "待处理详情", "规则配置", "审核日志"]
    if "搜索" in title or "查询" in title:
        return ["搜索入口", "结果列表", "详情页", "筛选与历史记录"]
    return ["主工作台 / 列表", "核心详情 / 状态", "操作表单 / 任务发起", "管理审核 / 日志"]


AI_TRIGGER_TERMS = (
    "大模型",
    "模型路由",
    "模型选型",
    "智能体",
    "向量",
    "语义",
    "智能",
    "多模态",
    "机器学习",
)
AI_TRIGGER_PATTERNS = (
    r"\bAI\b",
    r"\bLLM\b",
    r"\bAgent\b",
    r"\bRAG\b",
)
AI_NEGATION_PATTERNS = (
    r"非\s*AI",
    r"不涉及\s*AI",
    r"不需要\s*AI",
    r"non[-\s]?AI",
)


def brief_involves_ai(brief: dict, sections: dict | None = None) -> bool:
    values: list[str] = []
    for key in ("title", "business_context", "problem_statement", "business_goal"):
        values.append(str(brief.get(key) or ""))
    for key in ("facts", "assumptions", "constraints", "dependencies", "open_questions", "scenarios"):
        values.extend(str(item) for item in brief.get(key, []) or [])
    if sections:
        for key in ("summary", "background", "problem", "solution"):
            values.append(str(sections.get(key) or ""))
        for key in ("requirements", "risks", "dependencies"):
            values.extend(str(item) for item in sections.get(key, []) or [])
    text = "\n".join(values)
    strong_match = any(term in text for term in AI_TRIGGER_TERMS)
    word_match = any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in AI_TRIGGER_PATTERNS)
    negated = any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in AI_NEGATION_PATTERNS)
    return strong_match or (word_match and not negated)


def build_page_specs(brief: dict, sections: dict) -> list[str]:
    title = brief.get("title") or "产品"
    primary_user = (sections.get("target_users") or brief.get("target_users") or ["目标用户"])[0]
    modules = infer_page_modules(title)
    specs = [
        f"全局工作台：首页承接{primary_user}的主入口，展示搜索/筛选、待处理状态、快捷动作、异常提示和最近记录。",
    ]
    specs.extend(
        f"{module}：说明页面目标、入口来源、核心信息区、主要动作、退出路径、空状态、无权限状态和异常反馈。"
        for module in modules
    )
    specs.append("管理与审计页：面向管理员/审核角色，覆盖配置、审批、日志追踪、撤回或回滚入口。")
    return specs


def build_page_flow(brief: dict, sections: dict) -> list[str]:
    title = brief.get("title") or "产品"
    modules = infer_page_modules(title)
    main_module = modules[0] if modules else "主页面"
    return [
        f"主路径：首页/工作台 -> {main_module} -> 详情/表单 -> 提交或确认 -> 成功状态 -> 返回列表或进入下一任务。",
        "管理路径：管理入口 -> 配置/审核列表 -> 详情处理 -> 通过/拒绝/退回 -> 审计日志留痕。",
        "异常路径：入口无权限、参数错误、空结果、系统失败时，页面必须给出原因、下一步动作和可追踪状态。",
        "反馈路径：用户完成主流程后进入通知/反馈入口，系统沉淀问题、指标和后续优化线索。",
    ]


def build_prototype_layer(brief: dict, sections: dict) -> list[str]:
    title = brief.get("title") or "产品"
    modules = infer_page_modules(title)
    items = [
        "当前边界：PRD 阶段必须给出页面级低保真原型图或页面原型说明；本阶段不输出 PNG，不输出 HTML，不输出高保真 UI，除非用户确认进入原型/UI 阶段。",
        f"全局布局：{title}默认由主入口、核心任务区、状态反馈区、异常提示区和管理/审核入口组成，必须和页面说明、页面跳转关系保持一致。",
    ]
    items.extend(
        f"页面级低保真原型 - {module}：标明入口来源、核心信息区、主要动作、成功/失败状态、权限提示、异常反馈和返回路径。"
        for module in modules
    )
    items.append("交付衔接：原型图层只作为 UI 设计和 Codex 开发文档的产品参考；PNG、HTML、完整原型和视觉设计在用户确认方向后单独进入后续阶段。")
    return items


def build_prd_visual_sections(brief: dict, sections: dict) -> dict[str, str]:
    title = mermaid_label(brief.get("title") or sections.get("summary"), "产品")
    users = limited_items(sections.get("target_users"), ["目标用户"], 5)
    scenarios = limited_items(sections.get("scenarios"), ["核心场景"], 5)
    mvp = limited_items(sections.get("scope_in"), ["最高频主流程", "最小权限与校验", "基础验收闭环"], 5)
    out_scope = limited_items(sections.get("scope_out"), ["低频增强能力"], 4)
    v1 = limited_items(brief.get("suggested_scope", {}).get("v1"), ["次要场景", "体验增强", "运营配置"], 4)
    later = limited_items(brief.get("suggested_scope", {}).get("later"), ["长期扩展能力"], 4)
    risks = limited_items(sections.get("risks"), ["关键依赖未确认", "权限或合规边界待确认"], 5)
    metrics = limited_items(sections.get("metrics"), ["主流程使用量", "任务成功率", "人工支持工单量"], 4)

    overview = [
        "flowchart TB",
        f'  P["{title}"]',
        '  P --> U["目标用户"]',
        '  P --> S["核心场景"]',
        '  P --> M["MVP 范围"]',
        '  P --> R["风险边界"]',
        '  P --> K["成功指标"]',
    ]
    overview.extend(f'  U --> U{index}["{mermaid_label(item)}"]' for index, item in enumerate(users, start=1))
    overview.extend(f'  S --> S{index}["{mermaid_label(item)}"]' for index, item in enumerate(scenarios, start=1))
    overview.extend(f'  M --> M{index}["{mermaid_label(item)}"]' for index, item in enumerate(mvp, start=1))
    overview.extend(f'  R --> R{index}["{mermaid_label(item)}"]' for index, item in enumerate(risks, start=1))
    overview.extend(f'  K --> K{index}["{mermaid_label(item)}"]' for index, item in enumerate(metrics, start=1))

    primary_user = mermaid_label(users[0] if users else "用户")
    primary_scope = mermaid_label(mvp[0] if mvp else "核心任务")
    swimlane = [
        "flowchart LR",
        '  subgraph L1["用户"]',
        f'    U0["{primary_user}"]',
        '    U1["进入入口"]',
        '    U2["发起核心任务"]',
        '    U3["查看结果 / 反馈"]',
        "  end",
        '  subgraph L2["前台产品"]',
        '    P0["展示入口与筛选"]',
        '    P1["展示详情与状态"]',
        '    P2["展示成功 / 失败反馈"]',
        "  end",
        '  subgraph L3["系统"]',
        '    S0["权限 / 参数校验"]',
        f'    S1["处理：{primary_scope}"]',
        '    S2["记录日志 / 状态"]',
        "  end",
        '  subgraph L4["运营 / 管理"]',
        '    A0["处理异常"]',
        '    A1["复盘指标与反馈"]',
        "  end",
        "  U0 --> U1 --> P0",
        "  U2 --> P1 --> S0 --> S1 --> S2 --> P2 --> U3",
        "  S0 -->|失败| A0 --> P2",
        "  U3 --> A1",
    ]

    page_modules = infer_page_modules(title)
    page_ia = [
        "flowchart TB",
        f'  Home["{title} 首页 / 工作台"]',
        '  Home --> Search["搜索 / 筛选"]',
        '  Home --> Notice["通知 / 反馈"]',
        '  Home --> Admin["管理 / 审核"]',
    ]
    page_ia.extend(f'  Home --> Page{index}["{mermaid_label(item)}"]' for index, item in enumerate(page_modules, start=1))
    for index, item in enumerate(page_modules, start=1):
        page_ia.append(f'  Page{index} --> Detail{index}["状态 / 详情"]')
        page_ia.append(f'  Detail{index} --> Action{index}["主要操作 / 异常反馈"]')
    page_ia.extend(
        [
            '  Admin --> Admin1["权限 / 配置"]',
            '  Admin --> Admin2["日志 / 审计"]',
            "  Notice --> Home",
        ]
    )

    scope_map = [
        "flowchart LR",
        f'  Scope["{title} 范围"]',
        '  Scope --> MVP["MVP 必须做"]',
        '  Scope --> V1["V1 可做"]',
        '  Scope --> Later["Later 暂缓"]',
        '  Scope --> Out["明确不做"]',
    ]
    scope_map.extend(f'  MVP --> MVP{index}["{mermaid_label(item)}"]' for index, item in enumerate(mvp, start=1))
    scope_map.extend(f'  V1 --> V1_{index}["{mermaid_label(item)}"]' for index, item in enumerate(v1, start=1))
    scope_map.extend(f'  Later --> L{index}["{mermaid_label(item)}"]' for index, item in enumerate(later, start=1))
    scope_map.extend(f'  Out --> O{index}["{mermaid_label(item)}"]' for index, item in enumerate(out_scope, start=1))

    risk_loop = [
        "flowchart TD",
        '  R0["风险来源"]',
    ]
    risk_loop.extend(f'  R0 --> R{index}["{mermaid_label(item)}"]' for index, item in enumerate(risks, start=1))
    risk_loop.extend(f"  R{index} --> I" for index, _ in enumerate(risks, start=1))
    risk_loop.extend(
        [
            '  I["风险识别"]',
            '  I --> C1["规则 / 权限检查"]',
            '  I --> C2["数据 / 口径检查"]',
            '  I --> C3["用户反馈"]',
            '  C1 --> D{"风险等级"}',
            '  C2 --> D',
            '  C3 --> D',
            '  D -->|高| B["阻断 / 待确认"]',
            '  D -->|中| Q["降级 / 提示"]',
            '  D -->|低| W["记录后展示"]',
            '  B --> H["人工处理"]',
            '  Q --> H',
            '  H --> L["日志留痕"]',
            '  W --> L',
            '  L --> F["复盘规则与产品方案"]',
            '  F --> C1',
        ]
    )

    return {
        "product_overview_map": mermaid_block(overview),
        "core_business_swimlane": mermaid_block(swimlane),
        "page_information_architecture": mermaid_block(page_ia),
        "mvp_scope_map": mermaid_block(scope_map),
        "risk_control_loop": mermaid_block(risk_loop),
    }


def merge_value(seed_value, inferred_value):
    if isinstance(seed_value, list):
        return seed_value or inferred_value
    return seed_value if seed_value not in (None, "", {}) else inferred_value


def build_requirement_brief(project_id: str, raw_text: str, seed: dict | None = None) -> dict:
    seed = seed or {}
    fields = extract_template_fields(raw_text)
    bullets = extract_bullets(raw_text)
    title = extract_title(raw_text, fields, project_id)
    target_users = infer_target_users(raw_text, fields)
    request_type = infer_request_type(raw_text, fields)

    brief = {
        "project_id": project_id,
        "title": title,
        "request_type": request_type,
        "requester": fields.get("requester", ""),
        "channel": fields.get("channel", ""),
        "business_context": fields.get("business_context", ""),
        "problem_statement": infer_problem_statement(title, fields, bullets, target_users),
        "target_users": target_users,
        "scenarios": infer_scenarios(raw_text, title),
        "business_goal": infer_business_goal(fields, title),
        "urgency": infer_urgency(raw_text),
        "desired_launch_date": fields.get("desired_launch_date") or None,
        "evidence": infer_evidence(fields, bullets),
        "facts": bullets or [f"当前需求主题为：{title}"],
        "assumptions": infer_assumptions(fields, title, request_type),
        "constraints": infer_constraints(fields, title),
        "dependencies": infer_dependencies(fields, title),
        "open_questions": infer_open_questions(fields, title),
        "suggested_scope": infer_scope(title, request_type),
    }

    for key, value in list(brief.items()):
        if key in seed:
            brief[key] = merge_value(seed.get(key), value)
    return brief


def requirement_brief_markdown(brief: dict) -> str:
    sections = [
        f"# {brief['title']} - Requirement Brief",
        "",
        "## 基本信息",
        f"- Project ID：{brief['project_id']}",
        f"- 类型：{brief['request_type']}",
        f"- 紧急度：{brief['urgency']}",
        f"- 目标上线时间：{brief.get('desired_launch_date') or '待定'}",
        "",
        "## 问题定义",
        f"- 问题陈述：{brief['problem_statement']}",
        f"- 目标用户：{'、'.join(brief['target_users'])}",
        f"- 业务目标：{brief['business_goal']}",
        "",
        "## 场景",
    ]
    sections.extend(f"- {item}" for item in brief.get("scenarios", []))
    sections.extend(["", "## Facts"])
    sections.extend(f"- {item}" for item in brief.get("facts", []))
    sections.extend(["", "## Assumptions"])
    sections.extend(f"- {item}" for item in brief.get("assumptions", []))
    sections.extend(["", "## Open Questions"])
    sections.extend(f"- {item}" for item in brief.get("open_questions", []))
    sections.extend(["", "## 待确认问题分级", "### P0：不确认会影响 PRD 方向"])
    p0_questions = [item for item in brief.get("open_questions", []) if classify_open_question_priority(item) == "P0"]
    p1_questions = [item for item in brief.get("open_questions", []) if classify_open_question_priority(item) == "P1"]
    p2_questions = [item for item in brief.get("open_questions", []) if classify_open_question_priority(item) == "P2"]
    sections.extend(f"- {item}" for item in (p0_questions or ["暂无明确 P0，但仍需确认 MVP 主路径和目标用户。"]))
    sections.extend(["", "### P1：可先假设，PRD 评审时调整"])
    sections.extend(f"- {item}" for item in (p1_questions or ["暂无明确 P1。"]))
    sections.extend(["", "### P2：细节问题，不阻塞初稿"])
    sections.extend(f"- {item}" for item in (p2_questions or ["暂无明确 P2。"]))
    sections.extend(["", "## 建议范围", "### MVP"])
    sections.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("mvp", []))
    sections.extend(["", "### V1"])
    sections.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("v1", []))
    sections.extend(["", "### Later"])
    sections.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("later", []))
    return "\n".join(sections)


def brief_to_prd(brief: dict) -> dict:
    scope = brief.get("suggested_scope", {})
    requirements = scope.get("mvp", []) + scope.get("v1", [])
    risks = []
    if any("权限" in question for question in brief.get("open_questions", [])):
        risks.append("权限边界未确认，可能导致越权访问风险")
    if any("脱敏" in question for question in brief.get("open_questions", [])):
        risks.append("敏感字段脱敏规则未明确，存在合规风险")
    if any("异步" in question for question in brief.get("open_questions", [])):
        risks.append("大数据量导出性能未验证，可能导致超时")
    if not risks:
        risks.append("关键依赖未完全确认，需在评审前锁定")

    metrics = [
        f"{brief['title']}主流程使用量",
        f"{brief['title']}成功率",
        "相关人工支持工单量",
    ]

    sections = {
        "summary": f"围绕“{brief['title']}”构建最小可上线闭环，优先解决{brief['problem_statement']}",
        "background": brief.get("business_context") or "需求来自一线反馈，需要先解决高频主场景问题。",
        "problem": brief["problem_statement"],
        "goals": [brief["business_goal"], "让目标用户更快完成关键任务"],
        "non_goals": scope.get("later", []) or ["本期不处理低频增强能力"],
        "target_users": brief["target_users"],
        "scenarios": brief.get("scenarios", []),
        "scope_in": scope.get("mvp", []),
        "scope_out": scope.get("later", []),
        "solution": "基于现有后台流程补齐核心入口、权限控制、审计和数据反馈，先上线最小闭环，再视使用情况扩展。",
        "functional_flowcharts": [
            "产品总流程：用户进入 -> 核心入口 -> 主流程任务 -> 成功/失败反馈 -> 留存或复用。",
            "核心业务流程：触发条件 -> 用户动作 -> 系统校验 -> 系统处理 -> 成功状态或异常处理。",
            "异常/审核流程：异常触发 -> 权限/数据/合规检查 -> 阻断或进入审核 -> 记录日志 -> 用户可见反馈。",
        ],
        "page_specs": [],
        "page_flow": [],
        "prototype_layer": [],
        "requirements": requirements,
        "metrics": metrics,
        "risks": risks,
        "dependencies": brief.get("dependencies", []),
        "launch_plan": "建议先灰度给内部或小范围用户，监控成功率、时延和投诉情况，异常时支持快速回退。",
    }
    sections["page_specs"] = build_page_specs(brief, sections)
    sections["page_flow"] = build_page_flow(brief, sections)
    sections["prototype_layer"] = build_prototype_layer(brief, sections)
    if brief_involves_ai(brief, sections):
        sections["ai_model_selection"] = [
            "涉及 AI 能力时，PRD 必须拆分 AI 任务类型、输入输出、模型路由、fallback、评测标准、成本/延迟权衡和合规约束。",
            "低风险高频任务优先使用快速低成本模型；复杂推理、长上下文或多模态任务使用高能力模型；高风险内容必须叠加规则、模型复核和人工审核。",
            "模型能力上线前必须定义离线评测集、线上监控指标、人工复核阈值和回滚策略。",
        ]
    sections.update(build_prd_visual_sections(brief, sections))

    return {
        "project_id": brief["project_id"],
        "title": brief["title"],
        "status": "draft",
        "version": "v0.1",
        "sections": sections,
        "open_questions": brief.get("open_questions", []),
        "change_log": ["v0.1 初始自动生成草稿"],
    }


def prd_markdown(prd: dict, brief: dict) -> str:
    s = prd["sections"]
    title = prd["title"]
    target_users = s["target_users"]
    user_goals = [
        f"{user}可以更快完成“{title}”相关任务，减少人工协作与等待成本。"
        for user in target_users[: min(3, len(target_users))]
    ] or [f"目标用户可以自助完成“{title}”相关关键任务。"]
    detail_rows = s["requirements"] or ["待补充详细需求"]
    acceptance_focus = unique_list(
        [f"系统支持：{item}" for item in s["requirements"][:4]]
        + [f"风险兜底：{item}" for item in s["risks"][:2]]
    )
    edge_cases = unique_list(
        brief.get("constraints", [])[:2]
        + prd["open_questions"][:4]
        + ["空结果返回需明确提示且不误导用户", "权限不足时必须阻断并记录审计日志"]
    )
    compatibility = unique_list(
        [
            "需覆盖主流桌面浏览器与常见商家办公环境",
            "导出文件需验证 Excel 打开兼容性与编码格式",
            "若支持异步导出，任务状态刷新在弱网下仍需可用",
        ]
    )
    non_functional = unique_list(
        [
            "服务端必须执行强权限校验，不依赖前端隐藏入口",
            "导出链路需具备基础监控、告警与失败原因归因能力",
            "大数据量场景需控制超时、排队与资源隔离风险",
        ]
        + (["敏感字段需按已确认规则脱敏，并保留审计记录"] if any("脱敏" in item for item in prd["open_questions"] + s["risks"]) else [])
    )
    checklist = unique_list(
        [
            "字段清单、字段口径与权限矩阵已评审确认",
            "核心主流程、无权限、空结果、超量四类场景已验收",
            "埋点、日志、监控与告警已联调通过",
            "灰度范围、回滚开关与对外口径已准备完成",
        ]
    )
    change_log = prd.get("change_log", ["v0.1 初始自动生成草稿"])
    lines = [
        f"# {prd['title']}",
        "",
        f"- 文档状态：{prd['status']}",
        f"- 文档版本：{prd.get('version', 'v0.1')}",
        "",
        "## 1. 摘要",
        s["summary"],
        "",
        "### 1.1 产品总览思维导图",
        s.get("product_overview_map", "待补充"),
        "",
        "## 2. 背景与问题定义",
        f"- 背景：{s['background']}",
        f"- 问题：{s['problem']}",
        "",
        "## 3. 为什么现在做",
        f"- 业务目标：{brief['business_goal']}",
        f"- 紧急度：{brief['urgency']}",
    ]
    lines.extend(["", "## 4. 目标用户 / 角色 / JTBD"])
    lines.extend(f"- {item}" for item in s["target_users"])
    lines.extend(["", "## 5. 使用场景"])
    lines.extend(f"- {item}" for item in s["scenarios"])
    lines.extend(["", "## 6. 范围定义", "### 6.1 In Scope（本期包含）"])
    lines.extend(f"- {item}" for item in s["scope_in"])
    lines.extend(["", "### 6.2 Out of Scope（本期不包含）"])
    lines.extend(f"- {item}" for item in s["scope_out"])
    lines.extend(["", "### 6.3 分阶段规划", "#### MVP"])
    lines.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("mvp", []))
    lines.extend(["", "#### V1"])
    lines.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("v1", []))
    lines.extend(["", "#### Later"])
    lines.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("later", []))
    lines.extend(["", "### 6.4 MVP 范围地图", s.get("mvp_scope_map", "待补充")])
    lines.extend(["", "## 7. 方案概述", "### 7.1 方案摘要", s["solution"]])
    lines.extend(["", "### 7.2 核心业务泳道图", s.get("core_business_swimlane", "待补充")])
    lines.extend(["", "### 7.3 功能流程图"])
    lines.extend(f"- {item}" for item in s.get("functional_flowcharts", []))
    lines.extend(["", "### 7.4 页面信息架构图", s.get("page_information_architecture", "待补充")])
    lines.extend(["", "### 7.5 页面说明"])
    lines.extend(f"- {item}" for item in s.get("page_specs", []))
    lines.extend(["", "### 7.6 页面跳转关系"])
    lines.extend(f"- {item}" for item in s.get("page_flow", []))
    lines.extend(["", "### 7.7 原型图层"])
    lines.extend(f"- {item}" for item in s.get("prototype_layer", []))
    if s.get("ai_model_selection"):
        lines.extend(["", "### 7.8 AI 模型选型"])
        lines.extend(f"- {item}" for item in s.get("ai_model_selection", []))
    lines.extend(["", "## 8. 详细需求（按模块写）"])
    lines.extend(f"- {item}" for item in s["requirements"])
    lines.extend(["", "## 9. 需求明细表", "| ID | 需求 | 优先级 | 备注 |", "| --- | --- | --- | --- |"])
    lines.extend(
        f"| REQ-{index:03d} | {item} | {brief['urgency']} | 首版纳入 |"
        for index, item in enumerate(detail_rows, start=1)
    )
    lines.extend(["", "## 10. 用户故事与验收标准", "### 10.1 核心验收关注点"])
    lines.extend(f"- {item}" for item in acceptance_focus)
    lines.extend(["", "### 10.2 Definition of Done"])
    lines.extend(f"- {item}" for item in checklist)
    lines.extend(["", "## 11. 异常、边界与兼容性", "### 11.1 异常与边界"])
    lines.extend(f"- {item}" for item in edge_cases)
    lines.extend(["", "### 11.2 兼容性"])
    lines.extend(f"- {item}" for item in compatibility)
    lines.extend(["", "## 12. 非功能要求"])
    lines.extend(f"- {item}" for item in non_functional)
    lines.extend(["", "## 13. 埋点与数据方案"])
    lines.extend(f"- {item}" for item in s["metrics"])
    lines.extend(["", "## 14. 成功指标"])
    lines.extend(f"- {item}" for item in s["metrics"])
    lines.extend(["", "## 15. 目标 / 非目标", "### 15.1 业务目标"])
    lines.extend(f"- {item}" for item in s["goals"])
    lines.extend(["", "### 15.2 用户目标"])
    lines.extend(f"- {item}" for item in user_goals)
    lines.extend(["", "### 15.3 非目标（本期明确不做）"])
    lines.extend(f"- {item}" for item in s["non_goals"])
    lines.extend(["", "## 16. 依赖、风险与开放问题", "### 16.1 外部依赖"])
    lines.extend(f"- {item}" for item in s["dependencies"])
    lines.extend(["", "### 16.2 风险清单"])
    lines.extend(f"- {item}" for item in s["risks"])
    lines.extend(["", "### 16.3 风险控制闭环图", s.get("risk_control_loop", "待补充")])
    lines.extend(["", "### 16.4 开放问题"])
    lines.extend(f"- {item}" for item in prd["open_questions"])
    lines.extend(["", "## 17. 上线与灰度方案", s["launch_plan"]])
    lines.extend(["", "## 18. 验收 Checklist"])
    lines.extend(f"- {item}" for item in checklist)
    lines.extend(["", "## 19. 版本记录"])
    lines.extend(f"- {item}" for item in change_log)
    lines.extend(["", "## 20. 附录 / 链接资料", "### Facts"])
    lines.extend(f"- {item}" for item in brief.get("facts", []))
    lines.extend(["", "### Assumptions"])
    lines.extend(f"- {item}" for item in brief.get("assumptions", []))
    return "\n".join(lines)


def build_prd_context_digest(prd: dict, brief: dict) -> dict:
    sections = prd.get("sections", {}) if isinstance(prd, dict) else {}
    suggested_scope = brief.get("suggested_scope", {}) if isinstance(brief, dict) else {}
    open_questions = unique_list(list(prd.get("open_questions", [])) + list(brief.get("open_questions", [])))[:8]
    constraints = unique_list(
        list(brief.get("constraints", []))
        + list(sections.get("non_goals", []))
        + list(sections.get("dependencies", []))
    )[:10]
    risk_seeds = unique_list(
        list(sections.get("risks", []))
        + list(open_questions)
        + list(brief.get("assumptions", []))
    )[:10]
    acceptance_focus = unique_list(
        [f"系统支持：{item}" for item in sections.get("requirements", [])[:6]]
        + [f"风险兜底：{item}" for item in sections.get("risks", [])[:3]]
    )[:10]
    key_flows = unique_list(
        [sections.get("solution", "")]
        + list(sections.get("functional_flowcharts", []))
        + list(sections.get("page_flow", []))
    )[:8]
    return {
        "project_id": prd.get("project_id") or brief.get("project_id"),
        "title": prd.get("title") or brief.get("title"),
        "generated_from": ["source_brief", "prd_document"],
        "target_users": list(sections.get("target_users", []))[:8],
        "core_scenarios": list(sections.get("scenarios", []))[:8],
        "mvp_scope": {
            "scope_in": list(sections.get("scope_in", []))[:8],
            "scope_out": list(sections.get("scope_out", []))[:8],
            "suggested_mvp": list(suggested_scope.get("mvp", []))[:8],
        },
        "key_flows": key_flows,
        "constraints": constraints,
        "risk_seeds": risk_seeds,
        "acceptance_focus": acceptance_focus,
        "metric_seeds": list(sections.get("metrics", []))[:8],
        "dependencies": list(sections.get("dependencies", []))[:8],
        "open_questions": open_questions,
    }


def prd_to_user_stories(prd: dict, brief: dict) -> list[dict]:
    stories = []
    title = prd["title"]
    target_users = prd["sections"]["target_users"]
    primary_user = target_users[0] if target_users else "业务用户"
    stories.append(
        {
            "id": "STORY-001",
            "persona": primary_user,
            "need": f"完成“{title}”的核心操作",
            "benefit": "更快完成主流程任务",
            "story_statement": f"作为{primary_user}，我希望能完成“{title}”的核心操作，以便更快完成业务目标。",
            "acceptance_criteria": [
                "用户可以在主流程入口完成核心操作",
                "系统对关键字段和必填项进行校验",
                "成功结果可被用户确认并用于后续业务处理",
            ],
            "priority": brief["urgency"] if brief["urgency"] in {"p0", "p1", "p2", "p3"} else "p1",
            "dependencies": brief.get("dependencies", []),
            "edge_cases": brief.get("open_questions", [])[:2],
        }
    )

    if any(user in {"客服", "运营", "财务", "商家财务"} for user in target_users[1:] + target_users[:1]):
        stories.append(
            {
                "id": "STORY-002",
                "persona": target_users[1] if len(target_users) > 1 else "客服",
                "need": "快速查看结果并响应异常",
                "benefit": "减少人工沟通和重复处理",
                "story_statement": f"作为{target_users[1] if len(target_users) > 1 else '客服'}，我希望能快速定位处理结果和异常原因，以便减少人工支持成本。",
                "acceptance_criteria": [
                    "系统展示关键状态或结果信息",
                    "异常时有明确原因或下一步提示",
                    "必要时支持追踪操作记录",
                ],
                "priority": "p1",
                "dependencies": brief.get("dependencies", []),
                "edge_cases": brief.get("open_questions", [])[2:4],
            }
        )

    if any("权限" in question for question in brief.get("open_questions", [])):
        stories.append(
            {
                "id": "STORY-003",
                "persona": "管理员",
                "need": "控制功能访问权限",
                "benefit": "降低越权和合规风险",
                "story_statement": "作为管理员，我希望能按角色控制功能访问权限，以便降低越权风险。",
                "acceptance_criteria": [
                    "无权限用户不可见或不可执行对应操作",
                    "权限校验失败时返回明确提示",
                    "关键操作写入审计日志",
                ],
                "priority": "p1",
                "dependencies": ["权限系统", "审计日志能力"],
                "edge_cases": ["角色切换后的权限是否实时生效", "批量操作是否需要单独审计"],
            }
        )

    return stories


def user_stories_markdown(stories: list[dict], brief: dict) -> str:
    lines = [f"# {brief['title']} - User Stories", "", "## 用户故事与验收标准"]
    for story in stories:
        lines.append(f"- {story['story_statement']}")
        lines.extend(f"  - 验收标准：{criterion}" for criterion in story["acceptance_criteria"])
        if story.get("edge_cases"):
            lines.extend(f"  - 边界条件：{edge}" for edge in story["edge_cases"])
        lines.append("")
    lines.append("## Open Questions")
    lines.extend(f"- {item}" for item in brief.get("open_questions", []))
    return "\n".join(lines)


def normalize_user_stories(stories: list[dict]) -> list[dict]:
    deprioritized_personas = ("产品经理", "销售")
    deduped: list[dict] = []
    seen_personas: set[str] = set()

    for story in stories:
        persona = (story.get("persona") or "").strip()
        if not persona or persona in seen_personas:
            continue
        seen_personas.add(persona)
        deduped.append(story)

    preferred = [story for story in deduped if not any(token in story.get("persona", "") for token in deprioritized_personas)]
    fallback = [story for story in deduped if story not in preferred]
    selected = preferred + fallback
    normalized: list[dict] = []
    for index, story in enumerate(selected[:5], start=1):
        item = dict(story)
        item["id"] = f"STORY-{index:03d}"
        normalized.append(item)
    return normalized


def build_risk_report(prd: dict, brief: dict) -> dict:
    risks = [
        {
            "category": "permissions",
            "priority": "high",
            "title": "权限边界未锁定",
            "detail": "若角色与入口控制不清晰，可能出现越权访问或错误暴露。",
            "mitigation": "在开发前锁定角色矩阵，并在验收中覆盖无权限路径。",
        },
        {
            "category": "data",
            "priority": "high",
            "title": "敏感信息暴露风险",
            "detail": "若字段脱敏和导出规则不明确，可能触发合规问题。",
            "mitigation": "确认脱敏字段清单，并将审计日志纳入上线要求。",
        },
        {
            "category": "performance",
            "priority": "medium",
            "title": "高负载或大数据量超时",
            "detail": "高峰期或大数据量操作可能导致接口超时和失败率上升。",
            "mitigation": "预估数据量阈值，必要时改为异步任务并增加失败重试。",
        },
        {
            "category": "launch",
            "priority": "medium",
            "title": "上线后反馈闭环不足",
            "detail": "若缺少埋点和灰度计划，问题难以及时发现和回滚。",
            "mitigation": "首批灰度上线，监控成功率、耗时和客服反馈。",
        },
    ]
    return {
        "project_id": brief["project_id"],
        "title": brief["title"],
        "facts": brief.get("facts", []),
        "assumptions": brief.get("assumptions", []),
        "open_questions": brief.get("open_questions", []),
        "risks": risks,
        "recommendations": [
            "评审前明确角色权限矩阵",
            "补齐脱敏、审计、灰度和回滚要求",
            "将关键失败场景纳入测试与监控",
        ],
    }


def risk_report_markdown(report: dict) -> str:
    lines = [f"# {report['title']} - Risk Check", "", "## 风险清单"]
    for item in report["risks"]:
        lines.extend(
            [
                f"- [{item['priority']}] {item['title']}",
                f"  - 类别：{item['category']}",
                f"  - 风险说明：{item['detail']}",
                f"  - 建议动作：{item['mitigation']}",
                "",
            ]
        )
    lines.append("## Open Questions")
    lines.extend(f"- {item}" for item in report["open_questions"])
    lines.extend(["", "## Recommendations"])
    lines.extend(f"- {item}" for item in report["recommendations"])
    return "\n".join(lines)


def build_tracking_plan(prd: dict, brief: dict) -> dict:
    title = brief["title"]
    if "导出" in title:
        events = [
            {
                "name": "export_click",
                "trigger": "用户点击导出入口",
                "properties": ["role", "module", "date_range"],
                "linked_metric": "export_usage",
                "owner": "产品/数据",
                "qa_method": "前端事件校验 + 日志抽样核对",
            },
            {
                "name": "export_submit",
                "trigger": "用户提交导出请求",
                "properties": ["role", "row_estimate", "filters"],
                "linked_metric": "export_usage",
                "owner": "产品/数据",
                "qa_method": "请求链路日志比对",
            },
            {
                "name": "export_success",
                "trigger": "导出任务成功完成",
                "properties": ["duration_ms", "row_count", "file_size"],
                "linked_metric": "export_success_rate",
                "owner": "产品/数据",
                "qa_method": "服务端日志与埋点对账",
            },
            {
                "name": "export_failure",
                "trigger": "导出任务失败",
                "properties": ["error_code", "duration_ms", "role"],
                "linked_metric": "export_failure_rate",
                "owner": "产品/数据",
                "qa_method": "错误码分布核对",
            },
        ]
        metrics = [
            {
                "name": "export_usage",
                "metric_type": "input",
                "definition": "导出请求次数",
                "formula": "count(export_submit)",
                "baseline": None,
                "target": None,
                "window": "daily",
            },
            {
                "name": "export_success_rate",
                "metric_type": "input",
                "definition": "导出成功次数 / 导出请求次数",
                "formula": "count(export_success) / count(export_submit)",
                "baseline": None,
                "target": ">= 95%",
                "window": "daily",
            },
            {
                "name": "manual_support_tickets",
                "metric_type": "guardrail",
                "definition": "相关人工支持工单量",
                "formula": "count(tickets tagged export)",
                "baseline": None,
                "target": "不高于当前水平",
                "window": "weekly",
            },
            {
                "name": "export_failure_rate",
                "metric_type": "guardrail",
                "definition": "导出失败次数 / 导出请求次数",
                "formula": "count(export_failure) / count(export_submit)",
                "baseline": None,
                "target": "<= 5%",
                "window": "daily",
            },
        ]
    else:
        events = [
            {
                "name": "feature_entry_click",
                "trigger": "用户进入功能主入口",
                "properties": ["role", "module"],
                "linked_metric": "feature_usage",
                "owner": "产品/数据",
                "qa_method": "前端埋点校验",
            },
            {
                "name": "feature_success",
                "trigger": "主流程成功完成",
                "properties": ["duration_ms", "role"],
                "linked_metric": "feature_success_rate",
                "owner": "产品/数据",
                "qa_method": "服务端日志核对",
            },
        ]
        metrics = [
            {
                "name": "feature_usage",
                "metric_type": "input",
                "definition": "主流程使用次数",
                "formula": "count(feature_entry_click)",
                "baseline": None,
                "target": None,
                "window": "daily",
            },
            {
                "name": "feature_success_rate",
                "metric_type": "input",
                "definition": "主流程成功完成率",
                "formula": "count(feature_success) / count(feature_entry_click)",
                "baseline": None,
                "target": ">= 90%",
                "window": "daily",
            },
        ]
    return {
        "project_id": brief["project_id"],
        "metrics": metrics,
        "events": events,
    }


def tracking_plan_markdown(plan: dict, brief: dict) -> str:
    lines = [
        f"# {brief['title']} - Tracking Plan",
        "",
        "请自行核验事件命名、属性定义、采集位置和统计口径后再用于正式开发。",
        "",
        "## Metrics",
    ]
    for metric in plan["metrics"]:
        lines.extend(
            [
                f"- {metric['name']} ({metric['metric_type']})",
                f"  - 定义：{metric['definition']}",
                f"  - 公式：{metric.get('formula', '待补充')}",
                f"  - 观察窗口：{metric.get('window', '待定')}",
            ]
        )
    lines.extend(["", "## Events"])
    for event in plan["events"]:
        lines.extend(
            [
                f"- {event['name']}",
                f"  - 触发时机：{event['trigger']}",
                f"  - 属性：{'、'.join(event['properties'])}",
                f"  - 关联指标：{event.get('linked_metric', '待补充')}",
                f"  - QA：{event.get('qa_method', '待补充')}",
            ]
        )
    lines.extend(["", "## Open Questions"])
    lines.extend(f"- {item}" for item in brief.get("open_questions", []))
    return "\n".join(lines)
