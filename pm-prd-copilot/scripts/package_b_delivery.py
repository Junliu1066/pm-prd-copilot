#!/usr/bin/env python3
"""Build a generic letter-coded B execution package and scan protected terms."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt", ".html", ".css", ".js", ".json", ".yaml", ".yml"}
SOURCE_CANDIDATES = [
    "02_prd.final.md",
    "02_prd.generated.md",
    "01_requirement_brief.md",
    "00_raw_input.md",
]
AI_TERMS = (
    "artificial intelligence",
    "model routing",
    "embedding",
    "vector",
    "semantic",
    "prediction",
    "recommendation",
)
AI_WORD_PATTERNS = (
    r"\bAI\b",
    r"\bLLM\b",
    r"\bRAG\b",
    r"\bagent\b",
)


def contains_cjk(text: str) -> bool:
    return any(
        "\u3400" <= ch <= "\u4dbf"
        or "\u4e00" <= ch <= "\u9fff"
        or "\uf900" <= ch <= "\ufaff"
        for ch in text
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_blocked_terms(path: Path) -> list[str]:
    terms: list[str] = []
    in_terms = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "blocked_terms:":
            in_terms = True
            continue
        if in_terms and line.endswith(":") and not line.startswith("-"):
            break
        if in_terms and line.startswith("-"):
            terms.append(line[1:].strip().strip('"').strip("'"))
    return [term for term in terms if term]


def has_blocked_term(text: str, terms: list[str]) -> bool:
    return any(term and term in text for term in terms)


def is_safe_share_text(text: str, terms: list[str]) -> bool:
    return bool(text.strip()) and not contains_cjk(text) and not has_blocked_term(text, terms)


def assert_english_only(root: Path) -> None:
    offenders: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if contains_cjk(text):
            offenders.append(str(path.relative_to(root)))
    if offenders:
        joined = ", ".join(offenders)
        raise SystemExit(f"B package must be English-only. CJK text found in: {joined}")


def resolve_source_file(project_dir: Path, source_file: str) -> Path | None:
    if not source_file:
        return None
    path = Path(source_file)
    return path if path.is_absolute() else project_dir / path


def safe_source_text(project_dir: Path, terms: list[str], source_file: str = "") -> str:
    chunks: list[str] = []
    candidates = [resolve_source_file(project_dir, source_file)] if source_file else [project_dir / name for name in SOURCE_CANDIDATES]
    for candidate in candidates:
        if candidate is None:
            continue
        text = read_text(candidate)
        if is_safe_share_text(text, terms):
            chunks.append(text[:12000])
    return "\n\n".join(chunks)


def project_involves_ai(project_dir: Path, source_file: str = "") -> bool:
    snippets: list[str] = []
    candidates = [resolve_source_file(project_dir, source_file)] if source_file else [project_dir / name for name in SOURCE_CANDIDATES]
    for candidate in candidates:
        if candidate is not None:
            snippets.append(read_text(candidate)[:20000])
    text = "\n".join(snippets)
    lowered = text.lower()
    if any(term.lower() in lowered for term in AI_TERMS):
        return True
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in AI_WORD_PATTERNS)


def extract_title(project_dir: Path, terms: list[str], source_file: str = "") -> str:
    candidates = [resolve_source_file(project_dir, source_file)] if source_file else [project_dir / name for name in SOURCE_CANDIDATES]
    for candidate in candidates:
        if candidate is None:
            continue
        text = read_text(candidate)
        if not is_safe_share_text(text, terms):
            continue
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                if title and not contains_cjk(title) and not has_blocked_term(title, terms):
                    return title[:80]
    metadata = project_dir / "01_requirement_brief.json"
    if metadata.exists():
        try:
            title = str(json.loads(metadata.read_text(encoding="utf-8")).get("title") or "")
        except json.JSONDecodeError:
            title = ""
        if title and not contains_cjk(title) and not has_blocked_term(title, terms):
            return title[:80]
    return "Product Delivery"


def first_safe_lines(source_text: str, *, limit: int = 5) -> list[str]:
    lines: list[str] = []
    for raw_line in source_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("|") or line.startswith("```"):
            continue
        line = re.sub(r"^[-*]\s*", "", line)
        if 20 <= len(line) <= 180:
            lines.append(line.rstrip(".") + ".")
        if len(lines) >= limit:
            break
    return lines


def bullet_lines(items: list[str], fallback: list[str]) -> list[str]:
    values = items or fallback
    return [f"- {item}" for item in values]


def build_docs(project_dir: Path, terms: list[str], source_file: str = "") -> dict[str, str]:
    title = extract_title(project_dir, terms, source_file)
    source_text = safe_source_text(project_dir, terms, source_file)
    if not source_text.strip():
        raise SystemExit(
            "B package requires a confirmed English source file. "
            "Provide --source-file with an English B-package source, or add an English PRD/brief candidate before packaging."
        )
    source_lines = first_safe_lines(source_text)
    include_ai = project_involves_ai(project_dir, source_file)

    docs: dict[str, str] = {
        "A.md": "\n".join(
            [
                "# A",
                "",
                "## Product Requirements",
                "",
                f"Project: {title}.",
                "",
                "## Product Summary",
                *bullet_lines(
                    source_lines[:3],
                    [
                        "The product should solve a confirmed user workflow with a small first release.",
                        "The first release should keep scope clear, testable, and ready for acceptance.",
                    ],
                ),
                "",
                "## Required Product Inputs",
                "- Product goal and target users.",
                "- Scope and out-of-scope list.",
                "- User flow and key page notes.",
                "- Page navigation relationships.",
                "- Page-level prototype notes.",
                "- Acceptance criteria and known risks.",
            ]
        ),
        "B.md": "\n".join(
            [
                "# B",
                "",
                "## Delivery Plan",
                "",
                "## Use Boundary",
                "This document describes build scope, technical approach, staged delivery, quality requirements, and acceptance standards.",
                "",
                "## Development Flow",
                "```mermaid",
                "flowchart TD",
                '  A["Requirements and design inputs"] --> B["Task breakdown"]',
                '  B --> C["Key question confirmation"]',
                '  C --> D{"Blocking issue?"}',
                '  D -->|Yes| E["Return for confirmation"]',
                '  D -->|No| F["Readiness check"]',
                '  F --> G["Build"]',
                '  G --> H["Testing"]',
                '  H --> I["Safety and quality review"]',
                '  I --> J["Acceptance"]',
                "```",
                "",
                "## Rules",
                "- Do not add features outside approved requirements.",
                "- Confirm before changing data sources, model providers, database schema, or release behavior.",
                "- If checks cannot run, state the reason and provide a substitute check.",
            ]
        ),
        "C.md": "\n".join(
            [
                "# C",
                "",
                "## Release Plan",
                "",
                "### Stage 1",
                "- Complete the minimum usable path.",
                "- Deliver the core pages, data path, and acceptance checks.",
                "",
                "### Stage 2",
                "- Improve quality, retention, and operational visibility.",
                "",
                "### Stage 3",
                "- Improve permissions, scale, monitoring, and support workflows.",
                "",
                "### Final Stage",
                "- Stabilize release, review usage, and decide the next scope.",
            ]
        ),
        "D.md": "\n".join(
            [
                "# D",
                "",
                "## Tracking And Acceptance",
                "",
                "## Metrics",
                "- Core path usage.",
                "- Core path success rate.",
                "- Time to complete key task.",
                "- Support issue count.",
                "- Quality check pass rate.",
                "",
                "## Acceptance Requirements",
                "- Main path can be completed by an allowed user.",
                "- Empty, error, permission, and retry states are handled.",
                "- Key data includes source, status, and update time when applicable.",
                "- Risk-sensitive output is blocked or sent to review.",
            ]
        ),
        "E.md": "\n".join(
            [
                "# E",
                "",
                "## Functional Flow",
                "",
                "```mermaid",
                "flowchart TD",
                '  A["User enters workspace"] --> B["Open main task"]',
                '  B --> C["View required information"]',
                '  C --> D["Take primary action"]',
                '  D --> E{"Success?"}',
                '  E -->|Yes| F["Show result and next step"]',
                '  E -->|No| G["Show reason and recovery action"]',
                '  F --> H["Record status"]',
                '  G --> H',
                "```",
            ]
        ),
        "F.md": "\n".join(
            [
                "# F",
                "",
                "## Page And Prototype Notes",
                "",
                "## Required Page Notes",
                "- Entry page or main workspace.",
                "- Core list or main task page.",
                "- Detail or status page.",
                "- Management, review, or log page when required.",
                "",
                "## Page-Level Prototype Notes",
                "- Each page must state entry source, main content area, primary action, result state, permission state, and return path.",
                "- This file is a product reference for build and design work. It is not a high-fidelity UI design.",
            ]
        ),
        "H.md": "\n".join(
            [
                "# H",
                "",
                "## Open Questions",
                "",
                "## Blocking",
                "- Confirm final first-release scope.",
                "- Confirm required roles and permission boundaries.",
                "- Confirm data source authorization and update cadence.",
                "",
                "## Non-Blocking",
                "- Confirm future enhancements after the first release.",
                "- Confirm report or export formats if needed.",
            ]
        ),
    }

    if include_ai:
        docs["G.md"] = "\n".join(
            [
                "# G",
                "",
                "## AI Plan",
                "",
                "## Routing Criteria",
                "- Use a fast low-cost model for extraction, tagging, and simple classification.",
                "- Use a stronger model for complex reasoning, long context, or high-risk summaries.",
                "- Add fallback behavior for timeout, low confidence, missing source, or unsafe output.",
                "- Define offline evaluation, online monitoring, review threshold, and rollback plan before release.",
                "",
                "## Output Requirements",
                "- Separate facts, inferences, risks, unknowns, source references, and confidence.",
                "- Risk-sensitive output must include review status and user-facing limitations.",
            ]
        )
    return docs


def build_readme(docs: dict[str, str], include_prototype_dir: bool) -> str:
    index = [
        "# B Package",
        "",
        "This package contains product requirements, delivery plan, flow, page notes, quality checks, acceptance requirements, and open questions.",
        "",
        "## File Index",
    ]
    names = {
        "A.md": "Product requirements.",
        "B.md": "Delivery plan.",
        "C.md": "Release plan.",
        "D.md": "Tracking and acceptance.",
        "E.md": "Functional flow.",
        "F.md": "Page and prototype notes.",
        "G.md": "AI plan.",
        "H.md": "Open questions.",
    }
    for name in sorted(docs):
        index.append(f"- `docs/{name}`: {names[name]}")
    if include_prototype_dir:
        index.append("- `prototype/`: approved prototype files.")
    index.extend(
        [
            "",
            "## Delivery Requirements",
            "- Do not add features outside approved product requirements.",
            "- Each stage must state deliverables, delivered effects, and acceptance standards.",
            "- Confirm before changing data sources, model providers, database structure, or release behavior.",
            "- If tests or checks are not completed, state the reason and provide a substitute check.",
        ]
    )
    return "\n".join(index)


def copy_safe_prototype(project_dir: Path, package_root: Path, terms: list[str]) -> bool:
    source = project_dir / "prototype"
    if not source.exists() or not source.is_dir():
        return False
    copied_any = False
    target = package_root / "prototype"
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(source)
        if rel.parts and any(part.startswith(".") for part in rel.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if not is_safe_share_text(text, terms):
                continue
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        copied_any = True
    return copied_any


def write_package(project_dir: Path, package_root: Path, terms: list[str], *, source_file: str = "", include_prototype: bool = False) -> None:
    docs = build_docs(project_dir, terms, source_file)
    include_prototype_dir = copy_safe_prototype(project_dir, package_root, terms) if include_prototype else False
    write_text(package_root / "README.md", build_readme(docs, include_prototype_dir))
    for name, content in docs.items():
        write_text(package_root / "docs" / name, content)
    assert_english_only(package_root)


def zip_dir(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(src.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(src))


def run_redaction_check(base_dir: Path, package_root: Path) -> None:
    checker = base_dir / "harness" / "external_redaction_checker.py"
    terms = base_dir / "pm-prd-copilot" / "rules" / "redaction_terms.yaml"
    result = subprocess.run(
        [sys.executable, str(checker), str(package_root), "--terms", str(terms)],
        cwd=base_dir,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
        raise SystemExit(output or "B package protected-term scan failed.")
    print(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a generic B execution package.")
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--source-file", default="", help="Optional confirmed English B-package source file. Relative paths are resolved from project-dir.")
    parser.add_argument("--include-prototype", action="store_true", help="Explicitly include approved prototype files after manual share review.")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    project_dir = Path(args.project_dir).resolve()
    output = Path(args.output).resolve()
    if not project_dir.exists():
        raise SystemExit(f"Project directory not found: {project_dir}")

    terms = load_blocked_terms(base_dir / "pm-prd-copilot" / "rules" / "redaction_terms.yaml")
    with tempfile.TemporaryDirectory(prefix="b-package-") as tmp:
        package_root = Path(tmp) / "B"
        package_root.mkdir(parents=True, exist_ok=True)
        write_package(project_dir, package_root, terms, source_file=args.source_file, include_prototype=args.include_prototype)
        run_redaction_check(base_dir, package_root)
        zip_dir(package_root, output)
    print(f"Built B package: {output}")


if __name__ == "__main__":
    main()
