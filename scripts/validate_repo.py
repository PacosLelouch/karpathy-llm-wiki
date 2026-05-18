#!/usr/bin/env python3
"""Self-contained repository validation for the llm-wiki CodeBuddy skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    ".gitignore",
    ".editorconfig",
    ".gitattributes",
]

REQUIRED_DIRS = [
    "references",
    "examples",
    "docs",
    "scripts",
    "assets",
]


REQUIRED_REFERENCES = [
    "wiki-schema-template.md",
    "raw-template.md",
    "source-template.md",
    "entity-template.md",
    "concept-template.md",
    "analysis-template.md",
    "archive-template.md",
    "index-template.md",
    "log-template.md",
    "lint-checklist.md",
    "obsidian-style-guide.md",
    "codebuddy-usage-guide.md",
    "bases-template.base",
    "knowledge-map-template.canvas",
]

REQUIRED_EXAMPLES = [
    "README.md",
    "raw-source-example.md",
    "source-page-example.md",
    "concept-page-example.md",
    "entity-page-example.md",
    "analysis-page-example.md",
    "archive-page-example.md",
    "index-example.md",
    "log-example.md",
]

REQUIRED_DOCS = [
    "repository-guide.md",
    "release-checklist.md",
    "skill-design.md",
    "usage-recipes.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            value = match.group(2).strip().strip('"').strip("'")
            data[match.group(1)] = value
    return data


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            errors.append(f"Missing required directory: {rel}")

    for rel in REQUIRED_REFERENCES:
        if not (root / "references" / rel).is_file():
            errors.append(f"Missing reference: references/{rel}")

    for rel in REQUIRED_EXAMPLES:
        if not (root / "examples" / rel).is_file():
            errors.append(f"Missing example: examples/{rel}")

    for rel in REQUIRED_DOCS:
        if not (root / "docs" / rel).is_file():
            errors.append(f"Missing doc: docs/{rel}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = read_text(skill_path)
        meta = parse_frontmatter(skill_text)
        if meta.get("name") != "llm-wiki":
            errors.append("SKILL.md frontmatter name must be 'llm-wiki'")
        description = meta.get("description", "")
        if not description:
            errors.append("SKILL.md frontmatter description is required")
        elif "This skill should be used" not in description:
            warnings.append("SKILL.md description should use third-person trigger wording")
        if len(skill_text) > 20_000:
            warnings.append("SKILL.md is getting long; move details into references/")

    canvas_path = root / "references" / "knowledge-map-template.canvas"
    if canvas_path.is_file():
        try:
            json.loads(read_text(canvas_path))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON Canvas file: references/knowledge-map-template.canvas ({exc})")

    schema_path = root / "references" / "wiki-schema-template.md"
    if schema_path.is_file():
        schema = read_text(schema_path)
        for rel in REQUIRED_REFERENCES:
            if rel != "wiki-schema-template.md" and rel not in schema:
                warnings.append(f"references/wiki-schema-template.md does not mention {rel}")

    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.stat().st_size > 1_000_000:
            warnings.append(f"Large file over 1 MB: {path.relative_to(root).as_posix()}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the llm-wiki skill repository")
    parser.add_argument("root", nargs="?", default=".", help="Path to the skill repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors, warnings = validate(root)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"\nValidation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"Validation passed: 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
