#!/usr/bin/env python3
"""Validate the live paper-first Big Data Competition Skill (no third-party dependencies).

This intentionally does not validate the historical HSK mathmodel runtime. Its tests
and bootstrap apply to a different, superseded entrypoint in this repository.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("skills/big-data-competition-skill")
FRONT_VERSION = re.compile(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.M)
FRONT_NAME = re.compile(r"^name:\s*(\S+)\s*$", re.M)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REQUIRED_FIELDS = ("references", "playbooks", "competition", "templates")
SKILL_NAME = "big-data-competition-skill"


def frontmatter(source: str) -> str:
    if not source.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    sections = source.split("---\n", 2)
    if len(sections) != 3:
        raise ValueError("unterminated YAML frontmatter")
    return sections[1]


def version_from_skill(source: str) -> str:
    match = FRONT_VERSION.search(frontmatter(source))
    if not match:
        raise ValueError("missing semantic version in Skill frontmatter")
    return match.group(1)


def local_targets(markdown: str) -> list[str]:
    """Extract local Markdown links; do not include external or section anchors."""
    targets = []
    for match in LINK.finditer(markdown):
        target = match.group(1).strip().split("#", 1)[0].strip()
        if (not target or target.startswith(("http://", "https://", "mailto:", "data:", "//"))
                or target.startswith("<")):
            continue
        # Markdown supports an optional quoted title; the repository does not need
        # title-aware URL parsing for local paths with whitespace.
        targets.append(unquote(target))
    return targets


def check(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    def get(relative: Path | str) -> str:
        p = root / relative
        if not p.is_file():
            errors.append(f"missing active source: {relative}")
            return ""
        try:
            return p.read_text(encoding="utf-8-sig")
        except UnicodeError as exc:
            errors.append(f"not UTF-8: {relative}: {exc}")
            return ""

    top = get("SKILL.md")
    module = get(PACKAGE / "SKILL.md")
    if not top or not module:
        return errors
    try:
        primary = version_from_skill(top)
        packaged = version_from_skill(module)
        if primary != packaged:
            errors.append(f"root/module version mismatch: {primary} != {packaged}")
        for label, source in (("root", top), ("module", module)):
            if not re.search(r"(?m)^name:\s*big-data-competition-skill\s*$", frontmatter(source)):
                errors.append(f"{label} Skill name is not {SKILL_NAME}")
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    plugin_text = get(".codex-plugin/plugin.json")
    manifest_text = get(PACKAGE / "MANIFEST.json")
    try:
        plugin = json.loads(plugin_text)
        manifest = json.loads(manifest_text)
    except json.JSONDecodeError as exc:
        errors.append(f"invalid package JSON: {exc}")
        return errors
    for name, obj in (("plugin", plugin), ("manifest", manifest)):
        if obj.get("name") != SKILL_NAME:
            errors.append(f"{name} name mismatch")
        if obj.get("version") != primary:
            errors.append(f"{name} version mismatch with root Skill {primary}")
    if manifest.get("deliverable") != "paper-first":
        errors.append("manifest must be paper-first")
    if manifest.get("platform_submission_model") != "none":
        errors.append("Kaggle-style platform submission must not be the default")

    readme = get("README.md")
    changelog = get("CHANGELOG.md")
    module_readme = get(PACKAGE / "README.md")
    if f"v{primary}" not in readme:
        errors.append(f"README version marker must be v{primary}")
    if f"Current release: {primary}" not in changelog:
        errors.append(f"CHANGELOG current release must be {primary}")
    if f"v{primary}" not in module_readme:
        errors.append(f"module README must contain v{primary}")
    if not all(keyword in top for keyword in (
            "Competition Contract", "Baseline", "Leakage", "Evidence Map",
            "Paper Delivery", "论文")):
        errors.append("root Skill is missing mandatory paper-first evidence flow")

    expected_subdirs = {"references": "references", "playbooks": "playbooks",
                        "templates": "templates", "competition": "competition"}
    for key in REQUIRED_FIELDS:
        values = manifest.get(key)
        if not isinstance(values, list) or not values:
            errors.append(f"manifest {key} must be a nonempty list")
            continue
        if len(values) != len(set(values)):
            errors.append(f"manifest {key} contains duplicate entries")
        for name in values:
            if not isinstance(name, str) or "/" in name or not name.endswith(".md"):
                errors.append(f"invalid manifest {key} path: {name!r}")
            elif not (root / PACKAGE / expected_subdirs[key] / name).is_file():
                errors.append(f"manifest {key} path missing: {name}")
    optional_tools = manifest.get("optional_tools", [])
    if not isinstance(optional_tools, list):
        errors.append("manifest optional_tools must be a list")
    else:
        for rel in optional_tools:
            if not isinstance(rel, str) or ".." in Path(rel).parts:
                errors.append(f"invalid optional tool reference: {rel}")
            elif not (root / PACKAGE / rel).is_file():
                errors.append(f"missing optional tool: {rel}")

    docs = [root / "SKILL.md", root / "README.md", root / "REPOSITORY_INDEX.md",
            root / PACKAGE / "README.md", root / PACKAGE / "SKILL.md"]
    docs.extend(sorted((root / PACKAGE).rglob("*.md")))
    seen = set()
    for doc in docs:
        if doc in seen:
            continue
        seen.add(doc)
        if not doc.is_file():
            continue
        try:
            text = doc.read_text(encoding="utf-8-sig")
        except UnicodeError as exc:
            errors.append(f"invalid markdown encoding {doc}: {exc}")
            continue
        for target in local_targets(text):
            if any(x in target for x in ("\n", "\r")):
                errors.append(f"invalid markdown link in {doc.relative_to(root)}")
                continue
            # Markdown hyperlinks are relative to the hosting document.
            path = (doc.parent / target).resolve()
            try:
                path.relative_to(root.resolve())
            except ValueError:
                errors.append(f"link escapes repository: {doc.relative_to(root)} -> {target}")
                continue
            if not path.exists():
                errors.append(f"broken link: {doc.relative_to(root)} -> {target}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = check(args.root)
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    if errors:
        print(f"Big Data Skill validation failed: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    print("Big Data Skill validation passed: entrypoint, version, manifest, evidence flow, Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
