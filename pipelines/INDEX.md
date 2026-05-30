# Pipeline Test Index

End-to-end pipeline tests for all 15 project-level skills combined with global-level skills, organized by category.

## Categories

| # | Category | Project Skills | Global Skills | Pipelines | Steps | File |
|---|----------|---------------|---------------|-----------|-------|------|
| 1 | [Architecture](architecture/PIPELINE.md) | architecture, c4, drawio, repo-architecture, infocard, infographic, marp, slide-narrative, diagram-export | architecture-to-everything, architecture-presentation, workflow-visualizer, explainer-graphic, presentation-* suite | 4 | 21 | `architecture/PIPELINE.md` |
| 2 | [Cloud & Infrastructure](cloud-infrastructure/PIPELINE.md) | cloud, network, security, iot, diagram-export, architecture, infocard, marp | cso, canary, land-and-deploy, investigate | 5 | 31 | `cloud-infrastructure/PIPELINE.md` |
| 3 | [Business Process](business-process/PIPELINE.md) | archimate, bpmn, uml, infocard, infographic, marp, slide-narrative, diagram-export | office-hours, autoplan, plan-ceo-review, plan-eng-review, presales-deal-prep, contract-reviewer, 00-account-briefing | 5 | 28 | `business-process/PIPELINE.md` |
| 4 | [Data & Analytics](data-analytics/PIPELINE.md) | data-analytics, vega, infographic, infocard, architecture, marp, slide-narrative, diagram-export | ai-analyst, analytics-to-comms, health | 6 | 25 | `data-analytics/PIPELINE.md` |
| 5 | [Knowledge & Ideation](knowledge-ideation/PIPELINE.md) | mindmap, canvas, graphviz, infographic, infocard, vega, marp, slide-narrative | graphify, content-research, research-to-strategy, llm-council | 5 | 28 | `knowledge-ideation/PIPELINE.md` |

**Totals:** 25 pipelines, 133 test steps

## Cross-Category Skills

These skills appear in multiple category pipelines:

| Skill | Categories | Role |
|---|---|---|
| `infocard` | All 5 | Summary cards for components/metrics |
| `infographic` | All 5 | Visual overviews and comparisons |
| `marp` | All 5 | Final slide deck output |
| `slide-narrative` | All 5 | Story arc before deck building |
| `diagram-export` | Architecture, Cloud, Business | Rasterize diagrams for embedding |
| `architecture` | Architecture, Cloud, Data | HTML summary view |
| `vega` | Data, Knowledge | Statistical charts |

## How to Run

1. **Pick a category** that matches the system you're documenting
2. **Follow the pipeline steps in order** — each step builds on the prior one
3. **Grade each step** using the checkbox rubric
4. **Run adversarial tests** at the end to verify rule enforcement

## Pipeline Design Principles

- **Same system throughout** — each pipeline uses one consistent system (hospital, smart factory, e-commerce platform, etc.) across all steps
- **Zoom levels** — pipelines progress from high-level to detailed (enterprise landscape → process → software design)
- **Format cascade** — diagrams feed into cards, cards feed into decks, decks get exported
- **Global skills extend** — project skills produce artifacts, global skills orchestrate/review/deploy them
- **Adversarial at the end** — every category has 5-7 adversarial tests checking hard rules
