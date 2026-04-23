#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml


USER_AGENT = "PM-skill-ai-intel-bot/0.1"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch AI intel source pages")
    parser.add_argument("--base-dir", default=".")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    registry = yaml.safe_load((base_dir / "ai-intel" / "sources" / "registry.yaml").read_text(encoding="utf-8"))
    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_dir = base_dir / "ai-intel" / "raw" / run_date
    raw_dir.mkdir(parents=True, exist_ok=True)
    log_dir = base_dir / "ai-intel" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    session_log = []
    for source in registry["sources"]:
        source_dir = raw_dir / source["vendor"]
        source_dir.mkdir(parents=True, exist_ok=True)
        html_path = source_dir / f"{source['id']}.html"
        meta_path = source_dir / f"{source['id']}.json"
        event = {
            "source_id": source["id"],
            "vendor": source["vendor"],
            "url": source["url"],
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "stage": "fetch",
            "status": "ok",
            "likely_cause": "",
            "next_action": "",
        }
        try:
            response = requests.get(
                source["url"],
                headers={"User-Agent": USER_AGENT},
                timeout=30,
            )
            event["http_status"] = response.status_code
            response.raise_for_status()
            html_path.write_text(response.text, encoding="utf-8")
            event["bytes"] = len(response.text)
        except Exception as exc:  # noqa: BLE001
            event["status"] = "error"
            event["error_type"] = type(exc).__name__
            event["likely_cause"] = "network, rate limit, source-side block, or HTML access issue"
            event["next_action"] = "retry manually and inspect source availability"
            event["message"] = str(exc)
        finally:
            meta_path.write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            session_log.append(event)

    summary_path = log_dir / f"{run_date}.json"
    summary_path.write_text(json.dumps(session_log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
