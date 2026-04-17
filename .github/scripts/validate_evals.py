#!/usr/bin/env python3
"""Validate skills/*/evals/*.json files."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def validate_evals_json(path: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"{rel}: invalid JSON — {e}"]

    if not isinstance(data, dict):
        return [f"{rel}: must be an object with 'skill_name' and 'evals'"]
    if "skill_name" not in data or "evals" not in data:
        errors.append(f"{rel}: missing 'skill_name' or 'evals' field")
        return errors

    expected_name = path.parent.parent.name
    if data["skill_name"] != expected_name:
        errors.append(
            f"{rel}: skill_name {data['skill_name']!r} must equal "
            f"directory name {expected_name!r}"
        )

    for i, ev in enumerate(data.get("evals", [])):
        prefix = f"{rel}: evals[{i}]"
        if not isinstance(ev, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        for required in ("id", "prompt"):
            if required not in ev:
                errors.append(f"{prefix}: missing '{required}'")
    return errors


def validate_trigger_eval(path: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"{rel}: invalid JSON — {e}"]

    if not isinstance(data, list) or not data:
        return [f"{rel}: must be a non-empty array of trigger eval items"]

    for i, item in enumerate(data):
        prefix = f"{rel}: [{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        if "query" not in item or not isinstance(item["query"], str) or not item["query"].strip():
            errors.append(f"{prefix}: 'query' must be a non-empty string")
        if "should_trigger" not in item or not isinstance(item["should_trigger"], bool):
            errors.append(f"{prefix}: 'should_trigger' must be a boolean")
    return errors


def main() -> int:
    errors: list[str] = []
    eval_count = 0

    for path in sorted(ROOT.glob("skills/*/evals/evals.json")):
        errors.extend(validate_evals_json(path))
        eval_count += 1

    for path in sorted(ROOT.glob("skills/*/evals/trigger-eval.json")):
        errors.extend(validate_trigger_eval(path))
        eval_count += 1

    if errors:
        print("Eval validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"Eval validation OK ({eval_count} files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
