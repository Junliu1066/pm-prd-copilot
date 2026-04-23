#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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
        "brief_json": project_dir / "01_requirement_brief.json",
        "brief_md": project_dir / "01_requirement_brief.md",
        "brief_meta": project_dir / "01_requirement_brief.meta.json",
        "prd_json": project_dir / "02_prd.generated.json",
        "prd_md": project_dir / "02_prd.generated.md",
        "prd_meta": project_dir / "02_prd.generated.meta.json",
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


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    if "导出" in title:
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
        "requirements": requirements,
        "metrics": metrics,
        "risks": risks,
        "dependencies": brief.get("dependencies", []),
        "launch_plan": "建议先灰度给内部或小范围用户，监控成功率、时延和投诉情况，异常时支持快速回退。",
    }

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
        "## 1. 一句话摘要",
        s["summary"],
        "",
        "## 2. 背景与问题定义",
        f"- 背景：{s['background']}",
        f"- 问题：{s['problem']}",
        "",
        "## 3. 为什么现在做",
        f"- 业务目标：{brief['business_goal']}",
        f"- 紧急度：{brief['urgency']}",
        "",
        "## 4. 目标 / 非目标",
        "### 4.1 业务目标",
    ]
    lines.extend(f"- {item}" for item in s["goals"])
    lines.extend(["", "### 4.2 用户目标"])
    lines.extend(f"- {item}" for item in user_goals)
    lines.extend(["", "### 4.3 非目标（本期明确不做）"])
    lines.extend(f"- {item}" for item in s["non_goals"])
    lines.extend(["", "## 5. 成功指标"])
    lines.extend(f"- {item}" for item in s["metrics"])
    lines.extend(["", "## 6. 目标用户 / 角色 / JTBD"])
    lines.extend(f"- {item}" for item in s["target_users"])
    lines.extend(["", "## 7. 使用场景"])
    lines.extend(f"- {item}" for item in s["scenarios"])
    lines.extend(["", "## 8. 范围定义", "### 8.1 In Scope（本期包含）"])
    lines.extend(f"- {item}" for item in s["scope_in"])
    lines.extend(["", "### 8.2 Out of Scope（本期不包含）"])
    lines.extend(f"- {item}" for item in s["scope_out"])
    lines.extend(["", "### 8.3 分阶段规划", "#### MVP"])
    lines.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("mvp", []))
    lines.extend(["", "#### V1"])
    lines.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("v1", []))
    lines.extend(["", "#### Later"])
    lines.extend(f"- {item}" for item in brief.get("suggested_scope", {}).get("later", []))
    lines.extend(["", "## 9. 方案概述", s["solution"], "", "## 10. 详细需求（按模块写）"])
    lines.extend(f"- {item}" for item in s["requirements"])
    lines.extend(["", "## 11. 需求明细表", "| ID | 需求 | 优先级 | 备注 |", "| --- | --- | --- | --- |"])
    lines.extend(
        f"| REQ-{index:03d} | {item} | {brief['urgency']} | 首版纳入 |"
        for index, item in enumerate(detail_rows, start=1)
    )
    lines.extend(["", "## 12. 用户故事与验收标准", "### 12.1 核心验收关注点"])
    lines.extend(f"- {item}" for item in acceptance_focus)
    lines.extend(["", "### 12.2 Definition of Done"])
    lines.extend(f"- {item}" for item in checklist)
    lines.extend(["", "## 13. 异常、边界与兼容性", "### 13.1 异常与边界"])
    lines.extend(f"- {item}" for item in edge_cases)
    lines.extend(["", "### 13.2 兼容性"])
    lines.extend(f"- {item}" for item in compatibility)
    lines.extend(["", "## 14. 非功能要求"])
    lines.extend(f"- {item}" for item in non_functional)
    lines.extend(["", "## 15. 埋点与数据方案"])
    lines.extend(f"- {item}" for item in s["metrics"])
    lines.extend(["", "## 16. 依赖、风险与开放问题", "### 16.1 外部依赖"])
    lines.extend(f"- {item}" for item in s["dependencies"])
    lines.extend(["", "### 16.2 风险清单"])
    lines.extend(f"- {item}" for item in s["risks"])
    lines.extend(["", "### 16.3 开放问题"])
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
