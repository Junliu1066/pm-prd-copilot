#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml


DISCLAIMER = "以下内容为自动抓取与摘要结果，请自行核验原始链接、发布日期、模型名、API 可用性与计费信息。"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a daily AI intel report")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--run-date", default="")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    run_date = args.run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    events_path = base_dir / "ai-intel" / "events" / f"{run_date}.json"
    registry = yaml.safe_load((base_dir / "ai-intel" / "sources" / "registry.yaml").read_text(encoding="utf-8"))
    source_map = {item["id"]: item for item in registry["sources"]}
    events = json.loads(events_path.read_text(encoding="utf-8")) if events_path.exists() else []

    lines = [
        f"# AI Daily Intel - {run_date}",
        "",
        DISCLAIMER,
        "",
        "## Today",
    ]

    if not events:
        lines.append("- No normalized events available.")
    for event in events:
        source = source_map.get(event["source_id"], {})
        headline = event.get("summary_title") or (event["headline_candidates"][0] if event["headline_candidates"] else event["source_id"])
        latest_items = event.get("latest_items") or []
        if latest_items and latest_items[0] not in headline:
            headline = f"{headline} - {latest_items[0]}"
        lines.extend(
            [
                f"- `{event['vendor']}` [{event.get('change_type', 'watchlist')}]: {headline}",
                f"  Source: {source.get('url', 'unknown')}",
                f"  Date hints: {', '.join(event['date_candidates']) if event['date_candidates'] else 'none detected'}",
                f"  Latest items: {', '.join(latest_items[:3]) if latest_items else 'none detected'}",
                "  Verification: required before architecture action.",
            ]
        )

    lines.extend(
        [
            "",
            "## Governance architecture signals",
            "- Classify each verified update as: no architecture action, watchlist only, proposal needed, or user approval needed before adoption.",
            "- Do not change workflow, registry, skills, model provider, external data source, retention, deletion, or publishing behavior from this report alone.",
            "",
            "## Decision reminders",
            "- Confirm whether the update is already generally available.",
            "- Confirm pricing, quotas, regional availability, and migration constraints.",
            "- Confirm whether the observed page change actually matters for your use case.",
            "",
        ]
    )

    output_path = base_dir / "ai-intel" / "daily" / f"{run_date}.md"
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
