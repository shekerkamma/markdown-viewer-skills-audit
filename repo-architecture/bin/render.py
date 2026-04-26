#!/usr/bin/env python3
"""repo-architecture · Phase 3 — render layer-plan.yaml into a self-contained HTML diagram.

Usage: render.py <layer-plan.yaml> [--out <path.html>] [--prefix <css-prefix>]

Reads the chosen style from `architecture/styles/<style>.md` and the layout
hint from the plan, then emits HTML that follows the architecture skill's
visual contract. Drift-free by construction: when the architecture skill's
style files change, this renderer picks up the new CSS automatically — it
never duplicates style rules.

v1 supports the three-column layout only. Other layouts (single-stack,
pipeline, two-column-split) print a warning and fall back to three-column.

Hard deps: python3 stdlib + PyYAML.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

LAYER_ORDER = ["user", "application", "ai", "data", "infra", "external"]
LAYER_TITLES = {
    "user":        "User Layer",
    "application": "Application Layer",
    "ai":          "Intelligence Layer",
    "data":        "Data Layer",
    "infra":       "Infrastructure Layer",
    "external":    "External Services",
}
GRID_MAX = 6   # styles define grid-2..grid-6; clamp to that range
GRID_MIN = 2


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        print("error: PyYAML is required for render.py. `pip install pyyaml`.", file=sys.stderr)
        sys.exit(1)
    return yaml.safe_load(path.read_text())


def find_styles_dir(start: Path) -> Path:
    """Walk up from the plan path looking for `architecture/styles/`. This makes
    the script work whether run from inside the repo or via an absolute path."""
    here = start.resolve()
    for parent in [here, *here.parents]:
        candidate = parent / "architecture" / "styles"
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("could not locate architecture/styles/ from " + str(start))


def extract_style(style_md: str) -> tuple[str, str]:
    """Parse a style markdown file and return (outer_inline_style, scoped_css)."""
    m_outer = re.search(r'<div style="([^"]+)">', style_md)
    if not m_outer:
        raise ValueError("no outer <div style=\"...\"> found in style file")
    outer = m_outer.group(1)
    m_css = re.search(r'<style scoped>(.*?)</style>', style_md, re.DOTALL)
    if not m_css:
        raise ValueError("no <style scoped> block found in style file")
    return outer, m_css.group(1).strip()


def renamespace(css: str, prefix: str) -> str:
    """Replace .arch-* class names with .<prefix>-*."""
    return css.replace(".arch-", f".{prefix}-")


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_box(c: dict, prefix: str) -> str:
    classes = [f"{prefix}-box"]
    if c.get("highlight"):
        classes.append("highlight")
    if c.get("tech"):
        classes.append("tech")
    sub = f'<br><small>{esc(c.get("subtitle", ""))}</small>' if c.get("subtitle") else ""
    return f'<div class="{" ".join(classes)}">{esc(c["name"])}{sub}</div>'


def render_grid(components: list[dict], prefix: str) -> str:
    """Render components as one or more grids. Splits into chunks of 6 if needed."""
    if not components:
        return ""
    rows = []
    for i in range(0, len(components), GRID_MAX):
        chunk = components[i:i + GRID_MAX]
        n = max(GRID_MIN, len(chunk))
        boxes = "".join(render_box(c, prefix) for c in chunk)
        margin = ' style="margin-top: 8px;"' if i > 0 else ""
        rows.append(f'<div class="{prefix}-grid {prefix}-grid-{n}"{margin}>{boxes}</div>')
    return "".join(rows)


def render_layer(name: str, components: list[dict], prefix: str, custom_titles: dict) -> str:
    if not components:
        return ""
    title = custom_titles.get(name) or LAYER_TITLES.get(name, name.title())
    grids = render_grid(components, prefix)
    return (
        f'<div class="{prefix}-layer {name}">'
        f'<div class="{prefix}-layer-title">{esc(title)}</div>'
        f'{grids}'
        f'</div>'
    )


def render_sidebar(panels: list[dict], prefix: str, side: str) -> str:
    """Render one of the two sidebars. Empty panels list = empty sidebar div (still present
    in three-column layout to keep the grid consistent)."""
    if not panels:
        return f'<div class="{prefix}-sidebar"></div>'
    panel_html = []
    for p in panels:
        items = "".join(
            f'<div class="{prefix}-sidebar-item">{esc(item)}</div>'
            for item in p.get("items", [])
        )
        panel_html.append(
            f'<div class="{prefix}-sidebar-panel">'
            f'<div class="{prefix}-sidebar-title">{esc(p["title"])}</div>'
            f'{items}'
            f'</div>'
        )
    return f'<div class="{prefix}-sidebar">{"".join(panel_html)}</div>'


def render(plan: dict, styles_dir: Path, prefix: str) -> str:
    if "error" in plan:
        raise SystemExit(f"plan is a refusal, not a render input. reason: {plan.get('reason')}")

    style_name = plan.get("style", "ocean-teal")
    style_md = (styles_dir / f"{style_name}.md").read_text()
    outer_inline, scoped_css = extract_style(style_md)
    scoped_css = renamespace(scoped_css, prefix)

    layout = plan.get("layout", "three-column")
    if layout != "three-column":
        print(f"warning: layout '{layout}' not yet supported by render.py — falling back to three-column",
              file=sys.stderr)

    title = plan.get("title", "Architecture")
    subtitle = plan.get("subtitle", "")
    custom_titles = plan.get("layer_titles", {}) or {}

    layers_html = "".join(
        render_layer(name, plan.get("layers", {}).get(name, []) or [], prefix, custom_titles)
        for name in LAYER_ORDER
    )

    sidebars = plan.get("sidebars", {}) or {}
    left = render_sidebar(sidebars.get("left", []) or [], prefix, "left")
    right = render_sidebar(sidebars.get("right", []) or [], prefix, "right")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{esc(title)}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px 20px; margin: 0; background: #fafafa; }}
  .page-header {{ max-width: 1200px; margin: 0 auto 24px; }}
  .page-header h1 {{ margin: 0 0 6px; font-size: 24px; }}
  .page-header p {{ margin: 0 0 4px; }}
  .meta {{ max-width: 1200px; margin: 24px auto 0; font-size: 12px; color: #64748b; }}
  .{prefix}-title {{ text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 6px; }}
  .{prefix}-subtitle {{ text-align: center; font-size: 12px; margin-bottom: 14px; font-style: italic; opacity: 0.85; }}
</style>
</head>
<body>
<div class="page-header">
  <h1>{esc(title)}</h1>
  <p>{esc(subtitle)}</p>
  <p style="font-size: 12px; color: #64748b;">Generated by <code>repo-architecture/bin/render.py</code> · layout: three-column · style: {esc(style_name)}</p>
</div>
<div style="{outer_inline}; margin: 0 auto;">
<style scoped>{scoped_css}</style>
<div class="{prefix}-title">{esc(title)}</div>
<div class="{prefix}-subtitle">{esc(subtitle)}</div>
<div class="{prefix}-wrapper">
{left}
<div class="{prefix}-main">{layers_html}</div>
{right}
</div>
</div>
<div class="meta">Rendered from layer-plan.yaml — see repo-architecture/SKILL.md.</div>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("plan", help="path to layer-plan.yaml")
    ap.add_argument("--out", default="", help="output HTML path (default: <plan-stem>.html)")
    ap.add_argument("--prefix", default="ra", help="CSS class prefix to avoid collisions (default: ra)")
    ap.add_argument("--styles-dir", default="", help="override path to architecture/styles/")
    args = ap.parse_args()

    plan_path = Path(args.plan)
    plan = load_yaml(plan_path)
    if not isinstance(plan, dict):
        print("error: plan must be a YAML mapping", file=sys.stderr)
        return 1

    styles_dir = Path(args.styles_dir) if args.styles_dir else find_styles_dir(plan_path)
    out_path = Path(args.out) if args.out else plan_path.with_suffix(".html")

    try:
        html_out = render(plan, styles_dir, args.prefix)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    out_path.write_text(html_out)
    print(f"wrote {out_path}")
    print(f"  style:    {plan.get('style')}")
    print(f"  layout:   {plan.get('layout')}")
    print(f"  layers:   {sum(1 for k in LAYER_ORDER if plan.get('layers', {}).get(k))}")
    print(f"  prefix:   .{args.prefix}-*")
    return 0


if __name__ == "__main__":
    sys.exit(main())
