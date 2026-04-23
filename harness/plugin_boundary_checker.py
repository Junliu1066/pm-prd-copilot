#!/usr/bin/env python3
from __future__ import annotations

from os.path import isabs
from pathlib import Path

from common import CheckResult, VALID_STATUSES, load_yaml, read_json, result_from_issues


TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}


def _is_relative_plugin_path(value: str) -> bool:
    return value.startswith("./") and not isabs(value)


def _scan_for_forbidden_references(plugin_dir: Path, forbidden: list[str]) -> list[str]:
    issues: list[str] = []
    for file_path in plugin_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix not in TEXT_SUFFIXES:
            continue
        text = file_path.read_text(encoding="utf-8")
        for pattern in forbidden:
            if pattern in text:
                rel_path = file_path.relative_to(plugin_dir)
                issues.append(f"{rel_path} references forbidden host path pattern: {pattern}")
    return issues


def check_plugin_boundaries(base_dir: Path) -> CheckResult:
    issues: list[str] = []
    plugins_path = base_dir / "registry" / "plugins.yaml"
    if not plugins_path.exists():
        return result_from_issues("plugin_boundary", ["Missing registry/plugins.yaml"])

    plugins = load_yaml(plugins_path).get("plugins", {})
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    if not plugins:
        return result_from_issues("plugin_boundary", ["No plugins registered."])

    for plugin_id, plugin in plugins.items():
        status = plugin.get("status")
        if status not in VALID_STATUSES:
            issues.append(f"Plugin {plugin_id} has invalid status: {status}")

        plugin_path = str(plugin.get("path", ""))
        if not plugin_path:
            issues.append(f"Plugin {plugin_id} is missing path.")
            continue
        if isabs(plugin_path):
            issues.append(f"Plugin {plugin_id} path must be relative: {plugin_path}")
            continue

        plugin_dir = base_dir / plugin_path
        manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
        if not manifest_path.exists():
            issues.append(f"Plugin {plugin_id} is missing manifest: {manifest_path}")
            continue

        manifest = read_json(manifest_path)
        if manifest.get("name") != plugin_id:
            issues.append(f"Plugin {plugin_id} manifest name mismatch: {manifest.get('name')}")

        skills_path = manifest.get("skills")
        if skills_path:
            if not _is_relative_plugin_path(str(skills_path)):
                issues.append(f"Plugin {plugin_id} skills path must be plugin-relative: {skills_path}")
            elif not (plugin_dir / str(skills_path).removeprefix("./")).exists():
                issues.append(f"Plugin {plugin_id} skills path does not exist: {skills_path}")

        owned_skills = set(plugin.get("owns_skills", []))
        for skill_id in owned_skills:
            skill = skills.get(skill_id)
            if not skill:
                issues.append(f"Plugin {plugin_id} owns unregistered skill: {skill_id}")
                continue
            if skill.get("plugin") != plugin_id:
                issues.append(f"Skill {skill_id} does not declare plugin owner {plugin_id}")
            expected_path = f"{plugin_path}/skills/{skill_id}"
            skill_path = str(skill.get("path", ""))
            if skill_path != expected_path:
                issues.append(f"Skill {skill_id} path must stay inside plugin: {expected_path}")
            if not (base_dir / skill_path / "SKILL.md").exists():
                issues.append(f"Skill {skill_id} is missing plugin SKILL.md: {skill_path}")

        for skill_id, skill in skills.items():
            if skill.get("plugin") == plugin_id and skill_id not in owned_skills:
                issues.append(f"Skill {skill_id} declares plugin {plugin_id} but plugin does not own it.")

        issues.extend(_scan_for_forbidden_references(plugin_dir, plugin.get("forbidden_path_references", [])))

    return result_from_issues("plugin_boundary", issues)
