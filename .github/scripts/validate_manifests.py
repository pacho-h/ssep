#!/usr/bin/env python3
"""Validate .claude-plugin/plugin.json and .claude-plugin/marketplace.json
against minimal schemas matching Claude Code expectations."""
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]

PLUGIN_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "version"],
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-z][a-z0-9-]{0,63}$"},
        "description": {"type": "string", "minLength": 1, "maxLength": 1024},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+(-[\w.]+)?$"},
        "author": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "url": {"type": "string"},
            },
        },
        "license": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "homepage": {"type": "string"},
        "repository": {"type": "string"},
    },
}

MARKETPLACE_SCHEMA = {
    "type": "object",
    "required": ["name", "plugins"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "owner": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string"},
                "url": {"type": "string"},
                "email": {"type": "string"},
            },
        },
        "metadata": {"type": "object"},
        "plugins": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["name", "source"],
                "properties": {
                    "name": {"type": "string", "pattern": r"^[a-z][a-z0-9-]{0,63}$"},
                    "source": {},
                    "description": {"type": "string"},
                    "version": {"type": "string"},
                    "category": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "strict": {"type": "boolean"},
                },
            },
        },
    },
}


def validate(path: Path, schema: dict) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"{path.relative_to(ROOT)}: invalid JSON — {e}"]
    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors(data):
        loc = "/".join(str(p) for p in err.absolute_path)
        errors.append(f"{path.relative_to(ROOT)}: {loc or '<root>'}: {err.message}")
    return errors


def main() -> int:
    errors: list[str] = []
    plugin = ROOT / ".claude-plugin/plugin.json"
    market = ROOT / ".claude-plugin/marketplace.json"

    if not plugin.exists():
        errors.append(".claude-plugin/plugin.json: missing")
    else:
        errors.extend(validate(plugin, PLUGIN_SCHEMA))

    if not market.exists():
        errors.append(".claude-plugin/marketplace.json: missing")
    else:
        errors.extend(validate(market, MARKETPLACE_SCHEMA))

    if errors:
        print("Manifest validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Manifest validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
