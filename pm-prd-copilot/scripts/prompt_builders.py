#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

from pipeline_common import read_text


def _read_reference(base_dir: Path, relative_path: str) -> str:
    return read_text(base_dir / relative_path)


def _memory_block(base_dir: Path) -> str:
    return "\n\n".join(
        [
            "# Approved user preferences",
            _read_reference(base_dir, "pm-prd-copilot/memory/user_preferences.md"),
            "# Approved domain glossary",
            _read_reference(base_dir, "pm-prd-copilot/memory/domain_glossary.md"),
            "# Approved recurring fix patterns",
            _read_reference(base_dir, "pm-prd-copilot/memory/recurring_fix_patterns.md"),
        ]
    )


def _style_block(base_dir: Path) -> str:
    return _read_reference(base_dir, "pm-prd-copilot/references/output_style_guide.md")


def _drop_schema_keywords(schema: object) -> object:
    if isinstance(schema, dict):
        cleaned = {}
        for key, value in schema.items():
            if key == "$schema":
                continue
            if key == "type" and isinstance(value, list):
                non_null = [item for item in value if item != "null"]
                if len(non_null) == 1:
                    cleaned[key] = non_null[0]
                    continue
            cleaned[key] = _drop_schema_keywords(value)
        return cleaned
    if isinstance(schema, list):
        return [_drop_schema_keywords(item) for item in schema]
    return schema


def _force_all_properties_required(schema: object) -> object:
    if isinstance(schema, dict):
        updated = {key: _force_all_properties_required(value) for key, value in schema.items()}
        properties = updated.get("properties")
        if isinstance(properties, dict):
            updated["required"] = list(properties.keys())
        return updated
    if isinstance(schema, list):
        return [_force_all_properties_required(item) for item in schema]
    return schema


def build_brief_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "project_id",
            "title",
            "request_type",
            "problem_statement",
            "target_users",
            "business_goal",
            "urgency",
            "facts",
            "assumptions",
            "open_questions",
        ],
        "properties": {
            "project_id": {"type": "string"},
            "title": {"type": "string"},
            "request_type": {
                "type": "string",
                "enum": ["new_feature", "optimization", "bugfix", "compliance", "tech_debt", "other"],
            },
            "requester": {"type": "string"},
            "channel": {"type": "string"},
            "business_context": {"type": "string"},
            "problem_statement": {"type": "string"},
            "target_users": {"type": "array", "items": {"type": "string"}},
            "scenarios": {"type": "array", "items": {"type": "string"}},
            "business_goal": {"type": "string"},
            "urgency": {"type": "string", "enum": ["p0", "p1", "p2", "p3", "unknown"]},
            "desired_launch_date": {"type": "string"},
            "evidence": {"type": "array", "items": {"type": "string"}},
            "facts": {"type": "array", "items": {"type": "string"}},
            "assumptions": {"type": "array", "items": {"type": "string"}},
            "constraints": {"type": "array", "items": {"type": "string"}},
            "dependencies": {"type": "array", "items": {"type": "string"}},
            "open_questions": {"type": "array", "items": {"type": "string"}},
            "suggested_scope": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "mvp": {"type": "array", "items": {"type": "string"}},
                    "v1": {"type": "array", "items": {"type": "string"}},
                    "later": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    }


def build_prd_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["project_id", "title", "status", "sections", "open_questions"],
        "properties": {
            "project_id": {"type": "string"},
            "title": {"type": "string"},
            "status": {"type": "string", "enum": ["draft", "review", "aligned", "frozen", "released", "archived"]},
            "version": {"type": "string"},
            "sections": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "summary",
                    "background",
                    "problem",
                    "goals",
                    "non_goals",
                    "target_users",
                    "scenarios",
                    "scope_in",
                    "scope_out",
                    "solution",
                    "product_overview_map",
                    "core_business_swimlane",
                    "page_information_architecture",
                    "mvp_scope_map",
                    "risk_control_loop",
                    "functional_flowcharts",
                    "page_specs",
                    "page_flow",
                    "requirements",
                    "metrics",
                    "risks",
                    "dependencies",
                    "launch_plan",
                ],
                "properties": {
                    "summary": {"type": "string"},
                    "background": {"type": "string"},
                    "problem": {"type": "string"},
                    "goals": {"type": "array", "items": {"type": "string"}},
                    "non_goals": {"type": "array", "items": {"type": "string"}},
                    "target_users": {"type": "array", "items": {"type": "string"}},
                    "scenarios": {"type": "array", "items": {"type": "string"}},
                    "scope_in": {"type": "array", "items": {"type": "string"}},
                    "scope_out": {"type": "array", "items": {"type": "string"}},
                    "solution": {"type": "string"},
                    "product_overview_map": {"type": "string"},
                    "core_business_swimlane": {"type": "string"},
                    "page_information_architecture": {"type": "string"},
                    "mvp_scope_map": {"type": "string"},
                    "risk_control_loop": {"type": "string"},
                    "functional_flowcharts": {"type": "array", "items": {"type": "string"}},
                    "page_specs": {"type": "array", "items": {"type": "string"}},
                    "page_flow": {"type": "array", "items": {"type": "string"}},
                    "ai_model_selection": {"type": "array", "items": {"type": "string"}},
                    "requirements": {"type": "array", "items": {"type": "string"}},
                    "metrics": {"type": "array", "items": {"type": "string"}},
                    "risks": {"type": "array", "items": {"type": "string"}},
                    "dependencies": {"type": "array", "items": {"type": "string"}},
                    "launch_plan": {"type": "string"},
                },
            },
            "open_questions": {"type": "array", "items": {"type": "string"}},
        },
    }


def build_user_stories_schema() -> dict:
    return {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["id", "persona", "need", "benefit", "acceptance_criteria"],
            "properties": {
                "id": {"type": "string"},
                "persona": {"type": "string"},
                "need": {"type": "string"},
                "benefit": {"type": "string"},
                "story_statement": {"type": "string"},
                "acceptance_criteria": {"type": "array", "items": {"type": "string"}},
                "priority": {"type": "string", "enum": ["p0", "p1", "p2", "p3"]},
                "dependencies": {"type": "array", "items": {"type": "string"}},
                "edge_cases": {"type": "array", "items": {"type": "string"}},
            },
        },
    }


def build_user_stories_response_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["stories"],
        "properties": {
            "stories": build_user_stories_schema(),
        },
    }


def build_risk_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["project_id", "title", "facts", "assumptions", "open_questions", "risks", "recommendations"],
        "properties": {
            "project_id": {"type": "string"},
            "title": {"type": "string"},
            "facts": {"type": "array", "items": {"type": "string"}},
            "assumptions": {"type": "array", "items": {"type": "string"}},
            "open_questions": {"type": "array", "items": {"type": "string"}},
            "risks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["category", "priority", "title", "detail", "mitigation"],
                    "properties": {
                        "category": {"type": "string"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                        "title": {"type": "string"},
                        "detail": {"type": "string"},
                        "mitigation": {"type": "string"},
                    },
                },
            },
            "recommendations": {"type": "array", "items": {"type": "string"}},
        },
    }


def build_tracking_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["project_id", "metrics", "events"],
        "properties": {
            "project_id": {"type": "string"},
            "metrics": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["name", "metric_type", "definition"],
                    "properties": {
                        "name": {"type": "string"},
                        "metric_type": {"type": "string", "enum": ["north_star", "input", "guardrail"]},
                        "definition": {"type": "string"},
                        "formula": {"type": "string"},
                        "baseline": {"type": "string"},
                        "target": {"type": "string"},
                        "window": {"type": "string"},
                    },
                },
            },
            "events": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["name", "trigger", "event_properties"],
                    "properties": {
                        "name": {"type": "string"},
                        "trigger": {"type": "string"},
                        "event_properties": {"type": "array", "items": {"type": "string"}},
                        "linked_metric": {"type": "string"},
                        "owner": {"type": "string"},
                        "qa_method": {"type": "string"},
                    },
                },
            },
        },
    }


def build_stage_prompt_bundle(base_dir: Path, stage: str, *, project: str, raw_text: str = "", brief: dict | None = None, prd: dict | None = None) -> dict:
    memory = _memory_block(base_dir)
    style = _style_block(base_dir)
    if stage == "brief":
        return {
            "schema_name": "requirement_brief",
            "schema": build_brief_schema(),
            "system_prompt": (
                "You are the PM requirement-intake normalizer. "
                "Produce a structured Chinese JSON artifact that strictly matches the schema. "
                "Separate facts, assumptions, and open questions. "
                "Do not invent certainty where the input is incomplete."
            ),
            "user_prompt": "\n\n".join(
                [
                    f"Project: {project}",
                    "# Raw requirement input",
                    raw_text,
                    "",
                    style,
                    "",
                    memory,
                ]
            ),
        }
    if stage == "prd":
        template = _read_reference(base_dir, "pm-prd-copilot/templates/prd_template_2026.md")
        return {
            "schema_name": "prd_document",
            "schema": build_prd_schema(),
            "system_prompt": (
                "You are the PM PRD drafter. "
                "Write a reviewable PRD artifact in Chinese as structured JSON that strictly matches the schema. "
                "Use the requirement brief and template structure. "
                "The PRD must place visual diagrams in their corresponding chapters instead of collecting them in one visual layer. "
                "Include product_overview_map, core_business_swimlane, page_information_architecture, mvp_scope_map, and risk_control_loop. "
                "Use Mermaid where possible for these diagrams. "
                "The PRD body must include functional_flowcharts, page_specs, and page_flow. "
                "Only fill ai_model_selection when the project actually includes AI capability; otherwise leave it empty and do not create an AI model section in the PRD body. "
                "If key P0 questions are unresolved, keep assumptions explicit instead of presenting them as confirmed. "
                "Keep the content practical, specific, and suitable for engineering review."
            ),
            "user_prompt": "\n\n".join(
                [
                    "# Requirement brief JSON",
                    json.dumps(brief, ensure_ascii=False, indent=2),
                    "",
                    "# PRD template",
                    template,
                    "",
                    style,
                    "",
                    memory,
                ]
            ),
        }
    if stage == "stories":
        return {
            "schema_name": "user_stories",
            "schema": build_user_stories_response_schema(),
            "system_prompt": (
                "You are the PM user-story generator. "
                "Generate user stories in Chinese that strictly match the schema. "
                "Acceptance criteria must be testable. "
                "Use clear personas, user value, dependencies, and edge cases. "
                "Return 3 to 5 stories maximum. "
                "Prioritize direct product users and at most one governance or ops role. "
                "Do not create PM or sales personas unless they directly operate the workflow."
            ),
            "user_prompt": "\n\n".join(
                [
                    "# Requirement brief JSON",
                    json.dumps(brief, ensure_ascii=False, indent=2),
                    "",
                    "# PRD JSON",
                    json.dumps(prd, ensure_ascii=False, indent=2),
                    "",
                    style,
                    "",
                    memory,
                ]
            ),
        }
    if stage == "risk":
        return {
            "schema_name": "risk_report",
            "schema": build_risk_schema(),
            "system_prompt": (
                "You are the PM edge-case and risk checker. "
                "Generate a structured Chinese risk report that strictly matches the schema. "
                "Focus on permissions, data, performance, rollout, and operational risks. "
                "Keep recommendations specific and actionable."
            ),
            "user_prompt": "\n\n".join(
                [
                    "# Requirement brief JSON",
                    json.dumps(brief, ensure_ascii=False, indent=2),
                    "",
                    "# PRD JSON",
                    json.dumps(prd, ensure_ascii=False, indent=2),
                    "",
                    style,
                    "",
                    memory,
                ]
            ),
        }
    if stage == "tracking":
        return {
            "schema_name": "tracking_plan",
            "schema": build_tracking_schema(),
            "system_prompt": (
                "You are the PM tracking-plan designer. "
                "Generate a structured Chinese tracking plan that strictly matches the schema. "
                "Include metrics, event triggers, properties, and QA methods. "
                "Prefer practical names and definitions that engineering and data teams can implement."
            ),
            "user_prompt": "\n\n".join(
                [
                    "# Requirement brief JSON",
                    json.dumps(brief, ensure_ascii=False, indent=2),
                    "",
                    "# PRD JSON",
                    json.dumps(prd, ensure_ascii=False, indent=2),
                    "",
                    style,
                    "",
                    memory,
                ]
            ),
        }
    raise ValueError(f"Unsupported stage: {stage}")


def sanitize_schema_for_llm(schema: dict) -> dict:
    cleaned = copy.deepcopy(_drop_schema_keywords(schema))
    return _force_all_properties_required(cleaned)
