---
name: repo-architecture
description: Generate a layered HTML architecture diagram from a real GitHub repo URL. Walks the tree, classifies modules into semantic layers (user / application / ai / data / infra / external), picks an appropriate layout and style, and renders via the architecture skill. Pairs with codeflow for raw dependency graphs.
metadata:
  author: shekerkamma — addition to markdown-viewer/skills
  depends_on: architecture
---

# Repo → Architecture Diagram

**Quick Start:** `bin/run.sh <owner/repo> [--scope <subpath>]` walks the four-phase pipeline end-to-end. Deterministic phases (extract, validate, render) run automatically; LLM phases (summarize, classify) prompt you to paste model output. Output: one self-contained HTML file plus an optional codeflow embed for the raw import graph.

The `--scope` flag narrows extraction to a sub-tree (e.g. `--scope patterns/agents` on a broad repo). Use it when the full repo is too heterogeneous to classify into a single diagram — common for cookbooks, monorepos, and any repo where Phase 2 returns `error: refused`.

## What this skill produces

A publishable, layered architecture diagram derived from the actual code in a public GitHub repo — not a hand-drawn guess. Two views are produced:

1. **Logical view** (primary) — semantic layers using the [architecture](../architecture/SKILL.md) skill template. This is the diagram you put in slide decks, RFCs, and onboarding docs.
2. **Raw dependency view** (optional) — embedded [codeflow](https://github.com/braedonsaunders/codeflow) graph showing file-level imports. This is the diagram you use to find tight coupling, dead code, and circular deps.

Both share one HTML file with two tabs.

## When to use this skill vs. others

| If you need… | Use |
|---|---|
| File-level import graph, interactive | [codeflow](https://github.com/braedonsaunders/codeflow) directly |
| Hand-crafted layered diagram from a prompt | [architecture](../architecture/SKILL.md) |
| C4 levels (Context / Container / Component) | [c4](../c4/SKILL.md) |
| **Layered diagram derived from a real repo** | **repo-architecture** (this skill) |

Pick this skill when you want the architecture skill's polish but don't want to hand-author the layer assignments. The tradeoff: the LLM classifier will be wrong on edge cases — you must review `layer-plan.md` before render.

## Critical Rules

### Rule 1: Three phases, three artifacts
Always produce these intermediate files, in order, before render:

1. `structure.json` — what the repo contains (tree, manifests, entry points)
2. `layer-plan.md` — how each module maps to a semantic layer + chosen layout/style
3. `<repo-name>.html` — the rendered diagram

Never render directly from the URL. The intermediate files are the human override point — without them the skill is a black box.

### Rule 2: Tree-walk first, codeflow second
Codeflow is a browser app with no CLI. Do not depend on it for the logical view. Use `gh api` for tree extraction (Phase 1) and only embed codeflow as an iframe for the optional raw view (Phase 4). This keeps the skill runnable in headless environments.

### Rule 3: Classification must cite evidence
Every module assigned to a layer in `layer-plan.md` must include a one-line justification with a file path or manifest field. No "I think this is the data layer" — instead "data: `agent/tools/query_builder.py` builds OData queries; `mcp-server/src/odata-clients.ts` is the HTTP client."

### Rule 4: Reuse the architecture skill — do not reinvent
Phase 3 calls into [architecture/SKILL.md](../architecture/SKILL.md). All six rules from that skill apply to the rendered output (no `html` fences, no empty lines, semantic colors, etc.). This skill is a *front-end* for that skill, not a replacement.

### Rule 5: Public repos only by default
`gh api` works on private repos with auth, but the LLM classifier sees source code excerpts from the README and manifests. Default to public repos. For private repos, add an explicit `--allow-private` flag and warn the user that the classifier prompt will include private metadata.

## Workflow

### Phase 1 — Extract structure

Run [bin/extract.py](bin/extract.py):

```bash
bin/extract.py <owner/repo> [--scope <subpath>] [--out <dir>]
```

The script walks the top-level tree, drills into every top-level directory it finds (capped at 12, auto-derived — not a hard-coded list), pulls every recognised manifest that exists, and writes `structure.json` plus the raw `README.md` to `<out>/`. Missing manifests are skipped, not written as empty files. Hard deps: `python3` (stdlib only) and the `gh` CLI.

`structure.json` has these fields:

- `repo`, `scope` — passed-through identifiers
- `tree` — top-level entries as `[{type, path, name}, ...]`
- `subtrees` — list of `{dir, entries}` for each drilled directory
- `manifests` — map of filename → utf-8 content (only manifests that exist; never empty entries)
- `readme_summary` — initially `null`. Phase 1.5 fills it via [prompts/summarize-readme.md](prompts/summarize-readme.md), which produces a 200-word grounded summary of `README.md`.

The `--scope <subpath>` flag anchors all `gh api` calls at `repos/$REPO/contents/<subpath>` and is the recommended way to handle broad repos (cookbooks, monorepos) where Phase 2 would otherwise refuse.

### Phase 2 — Classify into layers

Feed `structure.json` to the LLM with the prompt at [prompts/classify-modules.md](prompts/classify-modules.md). Output schema:

```yaml
layout: three-column | pipeline | single-stack | two-column-split
style: steel-blue | indigo-deep | ocean-teal | neon-dark | frost-clean | ...
title: <repo title>
subtitle: <one-line description>
layers:
  user:
    - { name: "...", subtitle: "...", evidence: "<path or field>" }
  application:
    - { ... }
  ai: [...]
  data: [...]
  infra: [...]
  external: [...]
sidebars:
  left:  [{ title: "...", items: [...] }]
  right: [{ title: "...", items: [...] }]
```

**Validation rules** (block render if violated):
- Every component has a non-empty `evidence` field.
- At least 3 of the 6 standard layers are populated. Fewer means classification is too sparse — re-prompt or fall back to single-stack.
- Layout must match complexity: ≤ 5 components → single-stack; pipeline-shaped data flow → pipeline; cross-cutting concerns → three-column.

Run [bin/validate.py](bin/validate.py) to enforce the rules mechanically:

```bash
bin/validate.py out/<repo>/layer-plan.yaml
# exit 0 = VALID  ·  exit 1 = INVALID (errors printed)  ·  exit 2 = REFUSED (passthrough)
```

The validator accepts JSON or YAML (PyYAML required for YAML) and recognises the refusal schema (`error: refused` + `reason` + `recommendation`) — it relays the refusal to stdout and exits 2 so callers can branch.

### Phase 3 — Render

**First, check for a Phase 2 refusal.** If `layer-plan.yaml` is `error: refused`, do not render. Print the `reason` and `recommendation` fields to the user and stop. The expected next move is one of: re-run with `--scope <subpath>`, switch to the [architecture](../architecture/SKILL.md) skill from a prompt, or accept that this repo isn't a fit for a layered diagram. The validator handles this passthrough automatically (exit code 2).

Otherwise, run [bin/render.py](bin/render.py):

```bash
bin/render.py out/<repo>/layer-plan.yaml --out out/<repo>/diagram.html --prefix <css-prefix>
```

The renderer reads the chosen style from `architecture/styles/<style>.md` directly — it never duplicates the CSS rules in code. When the architecture skill's style files change, render.py picks up the new palettes automatically.

**v1 supports the three-column layout only.** Other layouts print a warning and fall back to three-column. Single-stack and pipeline support is an open follow-up.

The `--prefix` flag controls the CSS class namespace (default `ra`) so multiple diagrams can be embedded on the same page without collisions.

### Phase 4 — Optional codeflow embed

If the user passes `--with-dependency-graph`, append a second tab to the HTML with a codeflow iframe:

```html
<iframe src="https://codeflow-five.vercel.app/?repo=<encoded-url>" width="100%" height="800"></iframe>
```

Verify codeflow accepts a `?repo=` query param before relying on this — fall back to a "click here to load in codeflow" link if not.

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Classifier puts everything in `application` | README is sparse / no manifests | Pass `--include-source-samples` to feed top-N file headers into the prompt |
| Layout looks empty / one-sided | Repo has no infra or external deps in manifest | Acceptable — drop unused layers from the diagram, don't pad |
| Same module appears in two layers | Genuine cross-cutting concern | Move to a sidebar (left = ops, right = security/governance) instead of duplicating |
| Render fails Rule 2 from architecture skill (empty lines) | LLM injected blank lines in HTML | Run a post-pass that strips lines matching `^\s*$` inside the architecture HTML block |

## Examples

- [examples/sap-o2c-automation/](examples/sap-o2c-automation/) — full three-phase output for `github.com/shekerkamma/SAP-O2C-Automation`. The hand-rendered `architecture/demo-rendered/05-sap-o2c-automation.html` in this repo is the target output shape.

## Honest limitations

- **No code execution.** The classifier reads metadata, not behavior. A repo where every file is `utils.py` will get a useless diagram.
- **TypeScript/Python/Go bias.** The manifest list above covers maybe 80% of repos. Niche stacks (Elixir mix, Erlang rebar, Nim, Zig) need explicit handling.
- **Codeflow is a browser app.** The embed in Phase 4 requires the user to be online and CORS-allowed by codeflow-five.vercel.app. For air-gapped use, drop the embed and link to the locally-served clone instead.
- **Not a replacement for human review.** The skill produces a *first draft* you edit, not a finished diagram. Treat `layer-plan.md` as the review surface.
