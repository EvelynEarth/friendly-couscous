#!/usr/bin/env python3
"""Generate deterministic indexes for the active, paper-first Big Data Skill only.

Historical HSK directories remain in the repository, but are not active entrypoints.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("skills/big-data-competition-skill")
SKILL_INDEX = Path("SKILL_FILE_INDEX.md")
TEMPLATE_INDEX = Path("TEMPLATE_INDEX.md")
MANIFEST = Path("MANIFEST.sha256")
LEGACY_SKILL_INDEX = Path("HSK_SKILL_FILE_INDEX_V622.md")
LEGACY_TEMPLATE_INDEX = Path("HSK_TEMPLATE_INDEX_V622.md")

ACTIVE_ROOT_FILES = {
    Path("SKILL.md"), Path("README.md"), Path("CHANGELOG.md"),
    Path("REPOSITORY_INDEX.md"), Path("AGENTS.md"),
    Path("SKILL_CHANGE_GOVERNANCE.md"), Path("THIRD_PARTY_NOTICES.md"),
    Path("PROJECT_INSTRUCTIONS.md"), Path("RUNTIME_ROUTER.md"),
    Path(".codex-plugin/plugin.json"), Path("agents/openai.yaml"),
    Path("scripts/generate_indexes.py"), Path("scripts/validate_bigdata_skill.py"),
    Path(".github/workflows/ci.yml"), Path(".github/workflows/refresh-generated.yml"),
}
GENERATED_FILES = {SKILL_INDEX, TEMPLATE_INDEX, MANIFEST}
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", ".mypy_cache"}


def current_skill_version(root: Path = ROOT) -> str:
    source = (root / "SKILL.md").read_text(encoding="utf-8-sig")
    parts = source.split("---\n", 2)
    if len(parts) != 3 or not source.startswith("---\n"):
        raise ValueError("root SKILL.md requires frontmatter")
    match = re.search(r"(?m)^version:\s*(\d+\.\d+\.\d+)\s*$", parts[1])
    if not match:
        raise ValueError("root SKILL.md frontmatter lacks a semantic version")
    return match.group(1)


def iter_files(root: Path = ROOT) -> list[Path]:
    included = GENERATED_FILES | ACTIVE_ROOT_FILES
    if (root / PACKAGE).is_dir():
        included = included | {
            p.relative_to(root) for p in (root / PACKAGE).rglob("*")
            if p.is_file() and not any(part in EXCLUDED_DIRS for part in p.parts)
        }
    if (root / "tests").is_dir():
        included = included | {
            p.relative_to(root) for p in (root / "tests").glob("test_bigdata_*.py")
            if p.is_file()
        }
    missing = [str(p) for p in ACTIVE_ROOT_FILES if not (root / p).is_file()]
    if missing:
        raise FileNotFoundError("active sources missing: " + ", ".join(sorted(missing)))
    return sorted(included, key=lambda p: p.as_posix())


def index_text(title: str, files: list[Path], version: str) -> str:
    header = (
        f"# {title}\n\n当前 Skill 版本：{version}\n\n"
        "本索引仅包含当前论文型大数据竞赛 Skill；历史 HSK 文件不属于活动入口。\n\n"
    )
    return header + "".join("- " + chr(96) + p.as_posix() + chr(96) + "\n" for p in files)


def compatibility_pointer(target: Path) -> str:
    return (
        "# Historical compatibility pointer\n\n"
        "当前大数据 Skill 请查看 " + chr(96) + str(target) + chr(96)
        + "。此文件不再提供 HSK 活动规则。\n"
    )


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def generated_payloads(root: Path = ROOT) -> dict[Path, str]:
    version = current_skill_version(root)
    files = iter_files(root)
    templates = [
        p for p in files
        if p.parts[:3] == ("skills", "big-data-competition-skill", "templates")
    ]
    generated = {
        SKILL_INDEX: index_text("Big Data Competition Skill Active Index", files, version),
        TEMPLATE_INDEX: index_text("Big Data Competition Skill Template Index", templates, version),
        LEGACY_SKILL_INDEX: compatibility_pointer(SKILL_INDEX),
        LEGACY_TEMPLATE_INDEX: compatibility_pointer(TEMPLATE_INDEX),
    }
    rows = []
    for rel in files:
        if rel == MANIFEST:
            continue
        source = (generated[rel].encode("utf-8") if rel in generated
                  else (root / rel).read_bytes())
        rows.append(f"{digest(source)}  {rel.as_posix()}")
    generated[MANIFEST] = "\n".join(rows) + "\n"
    return generated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    payloads = generated_payloads()
    if args.check:
        stale = [
            str(p) for p, value in payloads.items()
            if not (ROOT / p).is_file()
            or (ROOT / p).read_text(encoding="utf-8") != value
        ]
        if stale:
            print("stale Big Data Skill metadata:", ", ".join(stale))
            return 1
        print("active Big Data Skill indexes and manifest are current")
        return 0
    for path, value in payloads.items():
        (ROOT / path).write_text(value, encoding="utf-8", newline="\n")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
