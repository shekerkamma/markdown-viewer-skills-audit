#!/usr/bin/env python3
"""repo-architecture · Phase 2.5 — validate a layer-plan before render.

Usage: validate.py <layer-plan.yaml-or-json>
Exit codes: 0 valid, 1 invalid (errors printed), 2 refusal (relayed verbatim).

Enforces the validation rules from SKILL.md Phase 2:
- Every component has a non-empty `evidence` field.
- At least 3 of the 6 standard layers are populated.
- Layout matches the standard set.
- Style matches the standard set.

Stdlib only. Accepts either YAML (if PyYAML is importable) or JSON. If you
hand-author layer-plan.md with a fenced YAML block, extract just the YAML
into layer-plan.yaml first, or convert to JSON.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

VALID_LAYERS = {"user", "application", "ai", "data", "infra", "external"}
VALID_LAYOUTS = {
    "single-stack", "two-column-split", "three-column",
    "pipeline", "hub-spoke", "dashboard", "banner-center",
}
VALID_STYLES = {
    "steel-blue", "indigo-deep", "ocean-teal", "neon-dark", "frost-clean",
    "slate-dark", "sage-forest", "rose-bloom", "ember-warm", "dusk-glow",
    "pastel-mix", "stark-block",
}


def load(path: Path) -> dict:
    text = path.read_text()
    # Try JSON first.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Then YAML, if available.
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        print("error: PyYAML not installed and file isn't JSON. "
              "Either `pip install pyyaml` or convert layer-plan to JSON.", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <layer-plan.yaml-or-json>", file=sys.stderr)
        return 1

    plan = load(Path(sys.argv[1]))
    if not isinstance(plan, dict):
        print("error: top-level must be a mapping", file=sys.stderr)
        return 1

    # Refusal passthrough.
    if "error" in plan and plan["error"] == "refused":
        print("REFUSED")
        print(f"reason:         {plan.get('reason', '<missing>').strip()}")
        print(f"recommendation: {plan.get('recommendation', '<missing>').strip()}")
        return 2

    errors: list[str] = []

    for field in ("title", "subtitle", "layout", "style", "layers"):
        if field not in plan:
            errors.append(f"missing required field: {field}")

    layout = plan.get("layout")
    if layout and layout not in VALID_LAYOUTS:
        errors.append(f"invalid layout '{layout}'. one of: {sorted(VALID_LAYOUTS)}")

    style = plan.get("style")
    if style and style not in VALID_STYLES:
        errors.append(f"invalid style '{style}'. one of: {sorted(VALID_STYLES)}")

    layers = plan.get("layers", {})
    if not isinstance(layers, dict):
        errors.append("layers must be a mapping")
        layers = {}

    populated = [k for k, v in layers.items() if v]
    for layer_name in layers:
        if layer_name not in VALID_LAYERS:
            errors.append(f"unknown layer '{layer_name}'. one of: {sorted(VALID_LAYERS)}")

    if len(populated) < 3:
        errors.append(
            f"only {len(populated)} layer(s) populated; minimum is 3. "
            f"either re-prompt the classifier or fall back to single-stack with a prompt."
        )

    # Component-level evidence check.
    for layer_name, components in layers.items():
        if not isinstance(components, list):
            errors.append(f"layer '{layer_name}' must be a list, got {type(components).__name__}")
            continue
        for i, c in enumerate(components):
            if not isinstance(c, dict):
                errors.append(f"layer '{layer_name}'[{i}]: must be a mapping")
                continue
            if not c.get("name"):
                errors.append(f"layer '{layer_name}'[{i}]: missing name")
            if not c.get("evidence", "").strip():
                errors.append(
                    f"layer '{layer_name}'[{i}] '{c.get('name', '?')}': "
                    f"missing evidence (required by Rule 3)"
                )

    if errors:
        print("INVALID")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("VALID")
    print(f"  title:    {plan['title']}")
    print(f"  layout:   {plan['layout']}")
    print(f"  style:    {plan['style']}")
    print(f"  layers:   {', '.join(populated)} ({len(populated)} populated)")
    print(f"  components: {sum(len(layers[l]) for l in populated)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
