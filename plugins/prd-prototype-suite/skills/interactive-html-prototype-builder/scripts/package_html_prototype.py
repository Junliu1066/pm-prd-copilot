#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile
from pathlib import Path


TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".md", ".txt", ".svg"}
ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"file://", re.IGNORECASE),
    re.compile(r"/Users/"),
    re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\\\/]"),
    re.compile(r"\\\\Users\\\\", re.IGNORECASE),
    re.compile(r"""(?:href|src)=["']/""", re.IGNORECASE),
]
EXTERNAL_ASSET_PATTERN = re.compile(r"""(?:href|src)=["']https?://""", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package a portable interactive HTML prototype."
    )
    parser.add_argument("prototype_dir", help="Directory containing index.html, styles.css, and app.js.")
    parser.add_argument("--entry", default="index.html", help="HTML entry file name.")
    parser.add_argument("--css", default="styles.css", help="CSS file name to inline.")
    parser.add_argument("--js", default="app.js", help="JS file name to inline.")
    parser.add_argument("--standalone", default="standalone.html", help="Generated standalone HTML file name.")
    parser.add_argument("--zip-name", default=None, help="Zip file name. Defaults to <prototype_dir>.zip.")
    parser.add_argument("--zip-out", default=None, help="Output directory for the zip. Defaults to prototype_dir parent.")
    parser.add_argument("--check-only", action="store_true", help="Only validate portability; do not write files.")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def required_files(prototype_dir: Path, names: list[str]) -> list[Path]:
    missing = [prototype_dir / name for name in names if not (prototype_dir / name).is_file()]
    if missing:
        joined = ", ".join(str(path) for path in missing)
        raise SystemExit(f"Missing required file(s): {joined}")
    return [prototype_dir / name for name in names]


def validate_portability(prototype_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for path in sorted(prototype_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(prototype_dir)
        text = read_text(path)
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: contains non-portable local/absolute path pattern: {pattern.pattern}")
        if EXTERNAL_ASSET_PATTERN.search(text):
            warnings.append(f"{rel}: references external http(s) asset; keep core prototype offline-capable.")
    return errors, warnings


def build_standalone(prototype_dir: Path, entry: str, css: str, js: str, standalone: str) -> Path:
    html_path, css_path, js_path = required_files(prototype_dir, [entry, css, js])
    html = read_text(html_path)
    css_text = read_text(css_path)
    js_text = read_text(js_path)

    link_pattern = re.compile(
        rf"\s*<link\s+rel=[\"']stylesheet[\"']\s+href=[\"']\.?/{re.escape(css)}[\"']\s*/?>",
        re.IGNORECASE,
    )
    script_pattern = re.compile(
        rf"\s*<script\s+src=[\"']\.?/{re.escape(js)}[\"']\s*></script>",
        re.IGNORECASE,
    )

    style_block = f"\n    <style>\n{css_text}\n    </style>"
    script_block = f"\n    <script>\n{js_text}\n    </script>"

    if link_pattern.search(html):
        html = link_pattern.sub(lambda _match: style_block, html, count=1)
    elif "</head>" in html:
        html = html.replace("</head>", f"{style_block}\n  </head>", 1)
    else:
        raise SystemExit("Could not find stylesheet link or </head> for standalone generation.")

    if script_pattern.search(html):
        html = script_pattern.sub(lambda _match: script_block, html, count=1)
    elif "</body>" in html:
        html = html.replace("</body>", f"{script_block}\n  </body>", 1)
    else:
        raise SystemExit("Could not find script tag or </body> for standalone generation.")

    output_path = prototype_dir / standalone
    output_path.write_text(html, encoding="utf-8")
    return output_path


def resolve_archive_path(prototype_dir: Path, zip_name: str | None, zip_out: str | None) -> Path:
    output_dir = Path(zip_out).expanduser().resolve() if zip_out else prototype_dir.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_name = zip_name or f"{prototype_dir.name}.zip"
    if not archive_name.endswith(".zip"):
        archive_name += ".zip"
    return output_dir / archive_name


def build_zip(prototype_dir: Path, zip_name: str | None, zip_out: str | None) -> Path:
    archive_path = resolve_archive_path(prototype_dir, zip_name, zip_out)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(prototype_dir.rglob("*")):
            if not path.is_file():
                continue
            arcname = Path(prototype_dir.name) / path.relative_to(prototype_dir)
            info = zipfile.ZipInfo.from_file(path, arcname.as_posix())
            if path.suffix == ".command":
                info.external_attr = 0o755 << 16
            with path.open("rb") as handle:
                archive.writestr(info, handle.read(), compress_type=zipfile.ZIP_DEFLATED)
    return archive_path


def update_manifest(prototype_dir: Path, standalone: str, archive_path: Path | None) -> None:
    manifest_path = prototype_dir / "prototype_manifest.json"
    if not manifest_path.is_file():
        return
    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError:
        return
    platform = manifest.setdefault("platform_compatibility", {})
    platform["single_file_entry"] = standalone
    if archive_path:
        platform["zip_package"] = Path(os.path.relpath(archive_path, prototype_dir)).as_posix()
    platform["handoff_rule"] = "Recommended handoff is the zip package; unzip it and open index.html. For one-file sharing use standalone.html."
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    prototype_dir = Path(args.prototype_dir).expanduser().resolve()
    if not prototype_dir.is_dir():
        raise SystemExit(f"Prototype directory does not exist: {prototype_dir}")

    required_files(prototype_dir, [args.entry, args.css, args.js])
    errors, warnings = validate_portability(prototype_dir)
    if errors:
        for issue in errors:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 2
    for issue in warnings:
        print(f"WARNING: {issue}", file=sys.stderr)

    archive_path = None
    standalone_path = None
    if not args.check_only:
        standalone_path = build_standalone(prototype_dir, args.entry, args.css, args.js, args.standalone)
        archive_path = resolve_archive_path(prototype_dir, args.zip_name, args.zip_out)
        update_manifest(prototype_dir, args.standalone, archive_path)
        archive_path = build_zip(prototype_dir, args.zip_name, args.zip_out)

    result = {
        "prototype_dir": str(prototype_dir),
        "standalone": str(standalone_path) if standalone_path else None,
        "zip": str(archive_path) if archive_path else None,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
