#!/usr/bin/env python3
"""repo-architecture · Phase 1 — extract structure from a public GitHub repo.

Usage: extract.py <owner/repo> [--scope <subpath>] [--out <dir>]
Produces: <out>/structure.json + <out>/<manifest> files (raw, for Phase 1.5).

Closes spec gaps #4 (hard-coded directory list) and #5 (empty manifest files):
- Directories to drill are auto-derived from the actual top-level tree, capped at 12.
- Manifests that don't exist in the repo are skipped, not written as empty files.

Hard deps: python3 (stdlib only) + gh CLI. No pip installs required.
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path

MANIFESTS = [
    "README.md", "package.json", "pyproject.toml", "Cargo.toml",
    "go.mod", "requirements.txt", "composer.json", "mix.exs", "Gemfile",
]
DRILL_CAP = 12


def gh_api(path: str) -> tuple[int, str]:
    """Call `gh api <path>`. Returns (rc, stdout). Stderr is dropped."""
    p = subprocess.run(
        ["gh", "api", path],
        capture_output=True, text=True,
    )
    return p.returncode, p.stdout


def fetch_tree(anchor: str) -> list[dict] | None:
    rc, out = gh_api(anchor)
    if rc != 0:
        return None
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, list):
        return None
    return [{"type": e["type"], "path": e["path"], "name": e["name"]} for e in data]


def fetch_manifest(anchor: str, filename: str, dest: Path) -> str | None:
    """Fetch a single manifest. Returns its decoded content or None if missing/empty."""
    rc, out = gh_api(f"{anchor}/{filename}")
    if rc != 0:
        return None
    try:
        meta = json.loads(out)
    except json.JSONDecodeError:
        return None
    content_b64 = meta.get("content")
    if not content_b64:
        return None
    try:
        content = base64.b64decode(content_b64).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None
    if not content.strip():
        return None
    dest.write_text(content)
    return content


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("repo", help="owner/name (e.g. shekerkamma/SAP-O2C-Automation)")
    ap.add_argument("--scope", default="", help="restrict to a sub-tree path")
    ap.add_argument("--out", default="", help="output dir (default: out/<repo>)")
    args = ap.parse_args()

    out = Path(args.out or f"out/{args.repo.replace('/', '-')}")
    out.mkdir(parents=True, exist_ok=True)

    anchor = f"repos/{args.repo}/contents"
    if args.scope:
        anchor = f"{anchor}/{args.scope.strip('/')}"

    # 1.a — top-level tree.
    tree = fetch_tree(anchor)
    if tree is None:
        print(f"error: could not fetch {anchor}. Is the repo public and gh authed?", file=sys.stderr)
        return 1

    # 1.b — drill every dir, capped, auto-derived from the actual tree.
    # Skip hidden dirs (.github, .devcontainer, .husky, .codesandbox …) — they're
    # tooling metadata, not architecture. They burn drill slots without producing
    # classifiable content.
    all_dirs = [e["name"] for e in tree if e["type"] == "dir"]
    dirs = [d for d in all_dirs if not d.startswith(".")][:DRILL_CAP]
    skipped = [d for d in all_dirs if d.startswith(".")]
    print(f"drilling: {', '.join(dirs) if dirs else '<none>'}", file=sys.stderr)
    if skipped:
        print(f"skipped:  {', '.join(skipped)} (hidden dirs)", file=sys.stderr)
    subtrees: list[dict] = []
    for d in dirs:
        sub = fetch_tree(f"{anchor}/{d}")
        if sub:
            subtrees.append({"dir": d, "entries": sub})

    # 1.c — manifests. Skip missing/empty ones rather than creating empty files.
    manifests: dict[str, str] = {}
    for f in MANIFESTS:
        content = fetch_manifest(anchor, f, out / f)
        if content is not None:
            manifests[f] = content

    # 1.d — assemble structure.json.
    structure = {
        "repo": args.repo,
        "scope": args.scope or None,
        "tree": tree,
        "subtrees": subtrees,
        "manifests": manifests,
        "readme_summary": None,
    }
    (out / "structure.json").write_text(json.dumps(structure, indent=2))

    print(f"wrote {out}/structure.json")
    print(f"manifests: {', '.join(manifests.keys()) or '<none>'}")
    print(f"subtrees:  {len(subtrees)}")
    print()
    print(f"next: feed {out}/structure.json + the README into prompts/summarize-readme.md,")
    print(f"      then prompts/classify-modules.md, to produce {out}/layer-plan.yaml.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
