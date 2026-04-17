#!/usr/bin/env python3
"""Validate every skills/*/SKILL.md frontmatter against Claude Code skill
authoring guidelines:

- name: lowercase-hyphen, ≤64 chars, must equal directory name
- description: ≤1024 chars, ≥1 char
- allowed-tools: optional, comma-separated string
- SKILL.md body: ≤500 lines (warn at 300)
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
NAME_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
LINE_HARD_LIMIT = 500
LINE_WARN_LIMIT = 300


def validate_skill(skill_md: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rel = skill_md.relative_to(ROOT)
    content = skill_md.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not m:
        errors.append(f"{rel}: missing frontmatter delimited by --- ... ---")
        return errors, warnings
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{rel}: invalid YAML — {e}")
        return errors, warnings

    name = fm.get("name")
    description = fm.get("description")
    allowed_tools = fm.get("allowed-tools")

    if not isinstance(name, str) or not NAME_RE.match(name):
        errors.append(
            f"{rel}: name must be lowercase-hyphen, ≤64 chars (got {name!r})"
        )
    elif name != skill_md.parent.name:
        errors.append(
            f"{rel}: frontmatter name {name!r} must equal directory "
            f"name {skill_md.parent.name!r}"
        )

    if not isinstance(description, str) or not description.strip():
        errors.append(f"{rel}: description is required and must be non-empty")
    elif len(description) > 1024:
        errors.append(
            f"{rel}: description {len(description)} chars exceeds 1024 limit"
        )

    if allowed_tools is not None and not isinstance(allowed_tools, str):
        errors.append(
            f"{rel}: allowed-tools must be a comma-separated string when present"
        )

    line_count = content.count("\n") + (0 if content.endswith("\n") else 1)
    if line_count > LINE_HARD_LIMIT:
        errors.append(
            f"{rel}: SKILL.md is {line_count} lines (>{LINE_HARD_LIMIT} hard limit). "
            "Move deep content to references/."
        )
    elif line_count > LINE_WARN_LIMIT:
        warnings.append(
            f"{rel}: SKILL.md is {line_count} lines (>{LINE_WARN_LIMIT} soft "
            "limit). Consider splitting into references/."
        )

    # Verify referenced files exist
    for ref in re.findall(r"references/[a-z0-9-]+\.md", content):
        if not (skill_md.parent / ref).exists():
            errors.append(f"{rel}: referenced file '{ref}' not found")

    return errors, warnings


def main() -> int:
    skills = sorted(ROOT.glob("skills/*/SKILL.md"))
    if not skills:
        print("No SKILL.md files found under skills/")
        return 1

    all_errors: list[str] = []
    all_warnings: list[str] = []
    for skill_md in skills:
        errors, warnings = validate_skill(skill_md)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    if all_warnings:
        print("Warnings:")
        for w in all_warnings:
            print(f"  - {w}")

    if all_errors:
        print("Skill validation FAILED:")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print(f"Skill validation OK ({len(skills)} skills checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
