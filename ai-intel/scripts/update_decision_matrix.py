#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


START = "<!-- LATEST_UPDATES_START -->"
END = "<!-- LATEST_UPDATES_END -->"


def replace_block(text: str, new_lines: list[str]) -> str:
    start = text.index(START) + len(START)
    end = text.index(END)
    replacement = "\n" + "\n".join(new_lines) + "\n"
    return text[:start] + replacement + text[end:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Update AI decision docs from daily events")
    parser.add_argument("--base-dir", default=".")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    events_path = base_dir / "ai-intel" / "events" / f"{run_date}.json"
    if not events_path.exists():
        raise SystemExit(f"Missing event file: {events_path}")
    events = json.loads(events_path.read_text(encoding="utf-8"))
    if not events:
        latest_lines = ["- No updates yet."]
    else:
        latest_lines = []
        for event in events[:5]:
            headline = event["headline_candidates"][0] if event["headline_candidates"] else event["source_id"]
            latest_lines.append(f"- {event['vendor']}: {headline} (verification required)")

    for relative_path in [
        "ai-intel/decisions/model-selection-matrix.md",
        "ai-intel/decisions/vendor-watchlist.md",
        "ai-intel/decisions/capability-map.md",
    ]:
        path = base_dir / relative_path
        content = path.read_text(encoding="utf-8")
        path.write_text(replace_block(content, latest_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
