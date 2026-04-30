#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup


NAVIGATION_HEADINGS = {
    "solutions",
    "partners",
    "learn",
    "company",
    "help and security",
    "terms and policies",
    "products",
    "models",
    "resources",
    "claude platform",
    "news",
    "overview",
    "notifications",
}


def compact_text(text: str) -> str:
    return " ".join(text.split())


def short_text(text: str, limit: int = 180) -> str:
    text = compact_text(text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "..."


def clean_title(title: str) -> str:
    title = compact_text(title)
    for separator in [" | ", " \\ ", " - "]:
        if separator in title:
            return title.split(separator, 1)[0].strip()
    return title


def extract_excerpt(soup: BeautifulSoup) -> str:
    text = compact_text(soup.get_text(" ", strip=True))
    return text[:800]


def is_date_heading(text: str) -> bool:
    return bool(
        re.fullmatch(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, 20\d{2}", text, flags=re.IGNORECASE)
        or re.fullmatch(r"20\d{2}-\d{2}-\d{2}", text)
    )


def extract_headings(soup: BeautifulSoup) -> list[str]:
    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = compact_text(tag.get_text(" ", strip=True))
        if not text:
            continue
        if text.lower() in NAVIGATION_HEADINGS and not is_date_heading(text):
            continue
        if text not in headings:
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
    unique = []
    for match in matches:
        if match not in unique:
            unique.append(match)
    return unique[:5]


def extract_date_section_items(soup: BeautifulSoup) -> list[str]:
    items = []
    for heading in soup.find_all(["h2", "h3"]):
        heading_text = compact_text(heading.get_text(" ", strip=True))
        if not is_date_heading(heading_text):
            continue
        for sibling in heading.find_next_siblings():
            if sibling.name in {"h2", "h3"}:
                break
            if sibling.name not in {"p", "ul", "ol"}:
                continue
            section_items = sibling.find_all("li", recursive=False) if sibling.name in {"ul", "ol"} else [sibling]
            for item in section_items:
                text = short_text(item.get_text(" ", strip=True))
                if text and text not in items:
                    items.append(text)
                if len(items) >= 5:
                    return items
    return items


def infer_change_type(source_id: str) -> str:
    if "deprecation" in source_id:
        return "deprecation_watch"
    if "release" in source_id or "changelog" in source_id:
        return "release_notes"
    if "news" in source_id:
        return "newsroom_watch"
    return "watchlist"


def select_latest_items(document_title: str, headings: list[str]) -> list[str]:
    items = []
    for heading in headings:
        if heading == document_title or is_date_heading(heading):
            continue
        items.append(heading)
        if len(items) >= 5:
            break
    return items


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize fetched source pages into event summaries")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--run-date", default="")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    run_date = args.run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_dir = base_dir / "ai-intel" / "raw" / run_date
    output_path = base_dir / "ai-intel" / "events" / f"{run_date}.json"
    events = []

    for html_path in sorted(raw_dir.rglob("*.html")):
        source_id = html_path.stem
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(text, "html.parser")
        excerpt = extract_excerpt(soup)
        headings = extract_headings(soup)
        document_title = clean_title(soup.title.get_text(" ", strip=True)) if soup.title else source_id
        if document_title and document_title not in headings:
            headings.insert(0, document_title)
        date_candidates = extract_dates(" ".join(headings) + " " + soup.get_text(" ", strip=True))
        latest_items = select_latest_items(document_title, headings)
        if not latest_items:
            latest_items = extract_date_section_items(soup)
        events.append(
            {
                "source_id": source_id,
                "vendor": html_path.parent.name,
                "normalized_at": datetime.now(timezone.utc).isoformat(),
                "summary_title": document_title,
                "change_type": infer_change_type(source_id),
                "headline_candidates": headings,
                "latest_items": latest_items,
                "date_candidates": date_candidates,
                "excerpt": excerpt,
                "quality_notes": [
                    "auto_extracted_from_html",
                    "human_verification_required_before_architecture_action",
                ],
                "verification_required": True,
            }
        )

    output_path.write_text(json.dumps(events, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
