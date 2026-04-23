#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - optional local dependency
    requests = None

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional local dependency
    yaml = None


@dataclass
class StageModelConfig:
    provider: str
    model: str
    base_url: str
    endpoint: str
    timeout_seconds: int
    max_retries: int
    reasoning_effort: str | None
    max_output_tokens: int | None
    temperature: float | None
    mode: str
    api_key_env: str


class ModelInvocationError(RuntimeError):
    pass


def load_stage_model_config(base_dir: Path, stage: str, requested_mode: str | None = None) -> StageModelConfig:
    config_path = base_dir / "pm-prd-copilot" / "config" / "model_config.yaml"
    if yaml is None:
        raw = {}
    else:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    defaults = raw.get("defaults", {})
    stage_overrides = raw.get("stages", {}).get(stage, {})
    merged = {**defaults, **stage_overrides}

    return StageModelConfig(
        provider=os.environ.get("PM_COPILOT_PROVIDER") or merged.get("provider", "openai"),
        model=os.environ.get("OPENAI_MODEL") or merged.get("model", "gpt-5-mini"),
        base_url=(os.environ.get("OPENAI_BASE_URL") or merged.get("base_url", "https://api.openai.com/v1")).rstrip("/"),
        endpoint=merged.get("endpoint", "responses"),
        timeout_seconds=int(os.environ.get("PM_COPILOT_TIMEOUT_SECONDS") or merged.get("timeout_seconds", 60)),
        max_retries=int(os.environ.get("PM_COPILOT_MAX_RETRIES") or merged.get("max_retries", 1)),
        reasoning_effort=os.environ.get("PM_COPILOT_REASONING_EFFORT") or merged.get("reasoning_effort"),
        max_output_tokens=merged.get("max_output_tokens"),
        temperature=merged.get("temperature"),
        mode=requested_mode or os.environ.get("PM_COPILOT_MODEL_MODE") or merged.get("mode", "auto"),
        api_key_env=merged.get("api_key_env", "OPENAI_API_KEY"),
    )


def parse_response_output(response_json: dict) -> str:
    output_text = response_json.get("output_text")
    if output_text:
        return output_text
    for item in response_json.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                return content["text"]
    raise ModelInvocationError("Model response did not contain output_text content.")


def parse_sse_response_output(response_text: str) -> tuple[str, dict]:
    output_text = ""
    delta_buffer: list[str] = []
    response_meta: dict = {}
    for raw_line in response_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("data: "):
            continue
        try:
            event = json.loads(line[6:])
        except json.JSONDecodeError:
            continue
        event_type = event.get("type")
        if event_type == "response.output_text.delta":
            delta = event.get("delta")
            if isinstance(delta, str):
                delta_buffer.append(delta)
        if event_type == "response.output_text.done":
            output_text = event.get("text", output_text)
        elif event_type == "response.completed":
            response_meta = event.get("response", {})
    if not output_text and delta_buffer:
        output_text = "".join(delta_buffer)
    if not output_text:
        raise ModelInvocationError("SSE response did not contain response.output_text.done text.")
    return output_text, response_meta


class OpenAIResponsesClient:
    def __init__(self, config: StageModelConfig):
        self.config = config
        if requests is None:
            raise ModelInvocationError("Missing dependency: requests")
        api_key = os.environ.get(config.api_key_env)
        if not api_key:
            raise ModelInvocationError(f"Missing API key in env: {config.api_key_env}")
        self.api_key = api_key

    def generate_structured_json(
        self,
        *,
        stage: str,
        schema_name: str,
        schema: dict,
        system_prompt: str,
        user_prompt: str,
    ) -> tuple[object, dict]:
        url = f"{self.config.base_url}/{self.config.endpoint}"
        payload = {
            "model": self.config.model,
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": system_prompt}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": user_prompt}],
                },
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                }
            },
        }
        if self.config.reasoning_effort:
            payload["reasoning"] = {"effort": self.config.reasoning_effort}
        if self.config.max_output_tokens:
            payload["max_output_tokens"] = self.config.max_output_tokens
        if self.config.temperature is not None:
            payload["temperature"] = self.config.temperature

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=self.config.timeout_seconds)
                if response.status_code >= 400:
                    detail = response.text.strip()
                    raise ModelInvocationError(f"HTTP {response.status_code}: {detail}")

                response_text = response.content.decode("utf-8", errors="replace")
                response_json = None
                response_meta = {}
                try:
                    response_json = response.json()
                except json.JSONDecodeError:
                    response_json = None

                if response_json is not None:
                    parsed = json.loads(parse_response_output(response_json))
                    response_meta = response_json
                else:
                    output_text, response_meta = parse_sse_response_output(response_text)
                    parsed = json.loads(output_text)
                meta = {
                    "provider": self.config.provider,
                    "model": response_meta.get("model", self.config.model),
                    "status": response_meta.get("status"),
                    "response_id": response_meta.get("id"),
                    "usage": response_meta.get("usage", {}),
                    "attempt": attempt + 1,
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "stage": stage,
                }
                return parsed, meta
            except (requests.RequestException, json.JSONDecodeError, ModelInvocationError) as exc:
                last_error = exc
        raise ModelInvocationError(str(last_error)) from last_error


def make_model_client(config: StageModelConfig) -> OpenAIResponsesClient:
    if config.provider != "openai":
        raise ModelInvocationError(f"Unsupported provider: {config.provider}")
    return OpenAIResponsesClient(config)
