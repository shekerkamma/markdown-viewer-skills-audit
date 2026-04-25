# Audit — markdown-viewer/skills

This is a fork of [markdown-viewer/skills](https://github.com/markdown-viewer/skills) at commit `c9c64d1` (2026-04-23). Full upstream commit history is preserved.

## What this fork changes vs upstream

| Change | Why |
|---|---|
| Added `LICENSE` (GPL-3.0) | Upstream README claims GPL-3.0 but ships no `LICENSE` file. Without a `LICENSE`, the GPL grant is not legally operative. |
| Added this `AUDIT.md` | Honest record of what you're inheriting if you consume these skills. |
| Rewrote `metadata.author` in all 15 `SKILL.md` files | Upstream embedded promotional copy ("powered by Markdown Viewer — the best...") into the field every agent loads on skill invocation. Replaced with plain attribution: `xicilion (upstream markdown-viewer/skills); audited fork by shekerkamma`. |

Everything else — skill content, examples, stencils, layouts, styles — is byte-identical to upstream.

## Per-skill audit

Grades weigh: portability (works without the `docu.md` viewer?), file-count vs README-claim consistency, token cost, and disclosure.

| Skill | SKILL.md | Files | Depends on | Grade | Notes |
|---|---:|---:|---|:---:|---|
| [vega](vega/SKILL.md) | 2.2 KB / 328w | 2 | Vega-Lite / Vega (open) | A | Most portable. |
| [graphviz](graphviz/SKILL.md) | 2.3 KB / 357w | 2 | Graphviz DOT (open) | A | Portable — **missing from upstream README**. Orphan skill. |
| [cloud](cloud/SKILL.md) | 4.2 KB / 535w | 9 | PlantUML AWS/Azure/GCP stdlib | A | Official stdlib, portable. |
| [mindmap](mindmap/SKILL.md) | 6.2 KB / 1025w | 8 | PlantUML `@startmindmap` | A- | Clean progressive disclosure. |
| [uml](uml/SKILL.md) | 4.7 KB / 583w | 77 | PlantUML + mxgraph preprocessor | A- | Biggest library. 61 stencil files are **catalogs** (`aws4.md` lists 1,034 shapes), not preprocessor code. `mxgraph.*` fails on stock PlantUML. |
| [canvas](canvas/SKILL.md) | 2.6 KB / 412w | 2 | JSON Canvas (open, niche) | B+ | Small, tidy. |
| [bpmn](bpmn/SKILL.md) | 7.3 KB / 891w | 9 | PlantUML BPMN / EIP stdlib | B+ | Stdlib-based, mostly portable. |
| [archimate](archimate/SKILL.md) | 7.7 KB / 912w | 9 | PlantUML archimate stdlib | B+ | TOGAF coverage. |
| [network](network/SKILL.md) | 4.4 KB / 580w | 10 | PlantUML + mxgraph Cisco/Citrix | B- | mxgraph lock-in. |
| [security](security/SKILL.md) | 5.7 KB / 713w | 9 | PlantUML + mxgraph | B- | mxgraph lock-in. |
| [data-analytics](data-analytics/SKILL.md) | 5.3 KB / 677w | 9 | PlantUML + stencils | B | Moderate stencil dependency. |
| [iot](iot/SKILL.md) | 5.3 KB / 649w | 9 | PlantUML + stencils | B | Moderate stencil dependency. |
| [architecture](architecture/SKILL.md) | 13 KB / 1589w | 26 | Bespoke HTML/CSS, rendered only by `docu.md` | B | Counts match README (13 × 12 = 156). Viewer-locked. |
| [infographic](infographic/SKILL.md) | 10.5 KB / 1135w | 4 | `docu.md` ` ```infographic` fence, space-separated key-value | C+ | Proprietary format; viewer-locked. |
| [infocard](infocard/SKILL.md) | 23 KB / 2954w | 66 | Bespoke HTML/CSS | C | Count mismatch: README says 13 × 14 = 182 combos, disk has **36 × 29 = 1,044**. ~4k tokens loaded per invocation. Viewer-locked. |

## Repo-level findings

| Check | Result |
|---|---|
| Broken relative links across all 15 `SKILL.md` | **0 / 181** links — all resolve |
| Total markdown files | 252 (100%, no code) |
| Upstream `LICENSE` file | **Missing** (fixed in this fork) |
| `npx skills add markdown-viewer/skills` install CLI | **Not in this repo** — no `package.json`, no `bin/`, no install script |
| Upstream README install path `skills/<skill-name>` | **Wrong** — skill dirs are at repo root |
| Skill count | README says 14, repo has **15** (`graphviz` undocumented) |
| Promotional `metadata.author` on every skill | **15 / 15** (stripped in this fork) |
| CI / tests / eval harness | None |
| Upstream contributors | 1 (`xicilion`, 18 commits) for 2,127 ★ |

## Renderer lock-in summary

- **Portable (open tools, any renderer):** vega, graphviz, canvas, mindmap, cloud, bpmn, archimate, uml (without mxgraph stencils)
- **Requires `docu.md`'s PlantUML fork for mxgraph stencils:** uml (with stencils), network, security, iot, data-analytics
- **Requires `docu.md` viewer to render at all:** architecture, infocard, infographic

## License note

Upstream's README claims GPL-3.0. This fork redistributes under the same license and adds the missing `LICENSE` file. Per GPL-3.0 §5, modifications from upstream are documented in the git history and this file.
