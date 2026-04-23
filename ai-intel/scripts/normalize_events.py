#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup


def extract_excerpt(soup: BeautifulSoup) -> str:
    text = " ".join(soup.get_text(" ", strip=True).split())
    return text[:800]


def extract_headings(soup: BeautifulSoup) -> list[str]:
    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = " ".join(tag.get_text(" ", strip=True).split())
        if text and text not in headings:
            headings.append(text)
        if len(headings) >= 10:
            break
    return headings


def extract_dates(text: str) -> list[str]:
    patterns = [
        r"\b20\d{2}-\d{2}-\d{2}\b",
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, 20\d{2}\b",
    ]
    matches = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return matches[:5]


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize fetched source pages into event summaries")
    parser.add_argument("--base-dir", default=".")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_dir = base_dir / "ai-intel" / "raw" / run_date
    output_path = base_dir / "ai-intel" / "events" / f"{run_date}.json"
    events = []

    for html_path in sorted(raw_dir.rglob("*.html")):
        source_id = html_path.stem
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(text, "html.parser")
        excerpt = extract_excerpt(soup)
        headings = extract_headings(soup)
        events.append(
            {
                "source_id": source_id,
                "vendor": html_path.parent.name,
                "normalized_at": datetime.now(timezone.utc).isoformat(),
                "headline_candidates": headings,
                "date_candidates": extract_dates(excerpt),
                "excerpt": excerpt,
                "verification_required": True,
            }
        )

    output_path.write_text(json.dumps(events, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
