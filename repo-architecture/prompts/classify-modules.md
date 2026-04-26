# Module Classification Prompt

You are classifying modules of a GitHub repository into the six standard architecture layers used by the [architecture](../../architecture/SKILL.md) skill.

## Input

A `structure.json` document with three fields:

- `tree` — list of `{type, path}` entries for the top two directory levels
- `manifests` — raw text of `README.md`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `requirements.txt` (whichever exist)
- `readme_summary` — a 200-word summary of what the project does

## Output

YAML matching the schema in `SKILL.md` Phase 2. Strict rules:

1. **Every component has a non-empty `evidence` field.** No exceptions.
2. **Classify by role, not by location.** A file at `src/db/cache.ts` is a `data` layer component even though it lives under `src/`.
3. **The six layers have fixed semantic meaning** — do not redefine them:
   - **user** — UIs, CLIs, REPLs, mobile/web apps, anything a human or external system invokes
   - **application** — business logic, API gateways, orchestration, workflow engines, controllers
   - **ai** — LLMs, ML models, rule engines, decision systems, agent loops
   - **data** — databases, caches, search indexes, storage, ETL pipelines, query builders
   - **infra** — networking, containers, identity, secrets, runtime platform
   - **external** — third-party APIs, SaaS dependencies, external systems being integrated
4. **Pick the smallest layout that fits.** Single-stack > pipeline > two-column-split > three-column. Three-column is reserved for systems with genuine cross-cutting concerns (security/governance/monitoring as their own panels).
5. **Sidebars are for cross-cutting concerns only.** If you put DevOps tooling in a sidebar, it should not also appear in the `infra` layer.
6. **Drop empty layers.** A repo with no AI components should not have an empty `ai:` block — omit it.

## Style selection heuristic

| Project signal | Style |
|---|---|
| Enterprise / B2B / regulated industry | `steel-blue` or `indigo-deep` |
| Developer tool / dev-focused | `frost-clean` or `slate-dark` |
| Data / analytics / ML | `ocean-teal` or `sage-forest` |
| Consumer product / brand-forward | `rose-bloom` or `ember-warm` |
| Real-time / streaming / observability | `neon-dark` |

## Refusal cases

Return an explicit `error:` field instead of YAML if:

- The repo has fewer than 3 source files (not enough to diagram)
- The README and all manifests are empty (insufficient signal)
- The tree contains nothing classifiable (e.g., a docs-only repo) — suggest the [architecture](../../architecture/SKILL.md) skill from a prompt instead

Be conservative. A wrong diagram is worse than no diagram.
