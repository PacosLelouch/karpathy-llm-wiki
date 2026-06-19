#!/usr/bin/env python3
"""Self-contained repository validation for the llm-wiki CodeBuddy skill.

Validates both the _shared/ source of truth and the generated platform packages.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Root-level required files
REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
]

# Root-level required directories
REQUIRED_ROOT_DIRS = [
    "_shared",
    "examples",
    "docs",
    "scripts",
    "assets",
]

# _shared/skills/llm-wiki/ required files
REQUIRED_SHARED_SKILL_FILES = [
    "SKILL.md",
    "README.md",
]

# _shared/skills/llm-wiki/references/ required files
REQUIRED_REFERENCES = [
    "initialize.md",
    "ingest.md",
    "query.md",
    "archive.md",
    "lint.md",
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
    "usage-guide.md",
    "bases-template.base",
    "knowledge-map-template.canvas",
]

# _shared/hooks/ required files
REQUIRED_HOOKS = [
    "llm-wiki-raw-guard.py",
    "llm-wiki-post-write-indexer.py",
]

# _shared/hooks/templates/ required files
REQUIRED_HOOK_TEMPLATES = [
    "codebuddy_utils.py",
    "codex_utils.py",
    "claude_utils.py",
]

# _shared/agents/ required files
REQUIRED_AGENTS_FILES = [
    "agents.yaml",
]

# examples/ required files
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

# docs/ required files
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

    # Root-level checks
    for rel in REQUIRED_ROOT_FILES:
        if not (root / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    for rel in REQUIRED_ROOT_DIRS:
        if not (root / rel).is_dir():
            errors.append(f"Missing required directory: {rel}")

    # _shared/skills/llm-wiki/ checks
    shared_skill_dir = root / "_shared" / "skills" / "llm-wiki"
    for rel in REQUIRED_SHARED_SKILL_FILES:
        if not (shared_skill_dir / rel).is_file():
            errors.append(f"Missing _shared skill file: _shared/skills/llm-wiki/{rel}")

    # _shared/skills/llm-wiki/references/ checks
    refs_dir = shared_skill_dir / "references"
    for rel in REQUIRED_REFERENCES:
        if not (refs_dir / rel).is_file():
            errors.append(f"Missing reference: _shared/skills/llm-wiki/references/{rel}")

    # _shared/hooks/ checks
    hooks_dir = root / "_shared" / "hooks"
    for rel in REQUIRED_HOOKS:
        if not (hooks_dir / rel).is_file():
            errors.append(f"Missing hook: _shared/hooks/{rel}")

    # _shared/hooks/templates/ checks
    hook_templates_dir = hooks_dir / "templates"
    for rel in REQUIRED_HOOK_TEMPLATES:
        if not (hook_templates_dir / rel).is_file():
            errors.append(f"Missing hook template: _shared/hooks/templates/{rel}")

    # _shared/agents/ checks
    agents_dir = root / "_shared" / "agents"
    for rel in REQUIRED_AGENTS_FILES:
        if not (agents_dir / rel).is_file():
            errors.append(f"Missing agents file: _shared/agents/{rel}")

    # _shared/agents/instructions/ checks
    agents_yaml_path = agents_dir / "agents.yaml"
    if agents_yaml_path.is_file():
        try:
            import yaml
            agents_meta = yaml.safe_load(agents_yaml_path.read_text(encoding="utf-8"))
            for agent_name in agents_meta.get("agents", {}):
                instruction_path = agents_dir / "instructions" / f"{agent_name}.md"
                if not instruction_path.is_file():
                    errors.append(f"Missing agent instruction: _shared/agents/instructions/{agent_name}.md")
        except Exception:
            warnings.append("Could not parse _shared/agents/agents.yaml; skipping agent instruction checks")

    # examples/ checks
    for rel in REQUIRED_EXAMPLES:
        if not (root / "examples" / rel).is_file():
            errors.append(f"Missing example: examples/{rel}")

    # docs/ checks
    for rel in REQUIRED_DOCS:
        if not (root / "docs" / rel).is_file():
            errors.append(f"Missing doc: docs/{rel}")

    # SKILL.md frontmatter validation
    skill_path = shared_skill_dir / "SKILL.md"
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

    # Canvas JSON validation
    canvas_path = refs_dir / "knowledge-map-template.canvas"
    if canvas_path.is_file():
        try:
            json.loads(read_text(canvas_path))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON Canvas file: _shared/skills/llm-wiki/references/knowledge-map-template.canvas ({exc})")

    # Schema template cross-references
    schema_path = refs_dir / "wiki-schema-template.md"
    if schema_path.is_file():
        schema = read_text(schema_path)
        for rel in REQUIRED_REFERENCES:
            if rel not in ("wiki-schema-template.md",) and rel not in schema:
                # Only warn for template files, not operation protocols
                if rel.endswith("-template.md") or rel in ("lint-checklist.md", "obsidian-style-guide.md", "usage-guide.md"):
                    warnings.append(f"references/wiki-schema-template.md does not mention {rel}")

    # Large file check
    for path in root.rglob("*"):
        # Skip generated platform directories
        if any(d in path.parts for d in ["CodeBuddy", "Codex", "ClaudeCode", "dist", ".git"]):
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
