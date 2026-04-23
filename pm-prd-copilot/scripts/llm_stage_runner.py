#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from model_client import load_stage_model_config, make_model_client
from pipeline_common import validate_schema_object
from prompt_builders import sanitize_schema_for_llm


def run_stage_with_optional_llm(
    *,
    base_dir: Path,
    stage: str,
    mode: str,
    prompt_bundle: dict,
    validator_schema: dict | None,
    rule_fallback: Callable[[], object],
) -> tuple[object, dict]:
    if mode == "rule":
        return rule_fallback(), {
            "requested_mode": mode,
            "used_mode": "rule",
            "fallback_used": False,
            "stage": stage,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    config = load_stage_model_config(base_dir, stage, requested_mode=mode)
    try:
        artifact, llm_meta = make_model_client(config).generate_structured_json(
            stage=stage,
            schema_name=prompt_bundle["schema_name"],
            schema=sanitize_schema_for_llm(prompt_bundle["schema"]),
            system_prompt=prompt_bundle["system_prompt"],
            user_prompt=prompt_bundle["user_prompt"],
        )
        if validator_schema:
            errors = validate_schema_object(validator_schema, artifact)
            if errors:
                raise ValueError(f"Schema validation failed: {errors}")
        return artifact, {
            "requested_mode": mode,
            "used_mode": "llm",
            "fallback_used": False,
            **llm_meta,
        }
    except Exception as exc:  # noqa: BLE001
        if mode == "llm":
            raise
        return rule_fallback(), {
            "requested_mode": mode,
            "used_mode": "rule",
            "fallback_used": True,
            "fallback_reason": str(exc),
            "attempted_provider": config.provider,
            "attempted_model": config.model,
            "stage": stage,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
