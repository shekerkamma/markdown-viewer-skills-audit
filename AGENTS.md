# Markdown Viewer Skills Audit — Repo Context

This repository tests 22 diagram-rendering skills across 5 pipeline categories.
Each pipeline produces 8 HTML gallery pages grounded in real-world domain data.

## Architecture

```
.agents/
  skills/          # OpenHands-compatible SKILL.md files (22 skills)
  agents/          # Subagent definitions for pipeline orchestration
pipelines/
  business-process/    # ArchiMate, BPMN, EIP, UML, VSM, Infocard
  data-analytics/      # Vega, Cloud, Infographic, Infocard
  knowledge-ideation/  # Mindmap, Canvas, Graphviz
  cloud-infrastructure/# Cloud, Network, Security, IoT
  architecture/        # C4, Architecture, UML
```

## Content Engineering Principle

Diagrams are meaningless without grounded content. Every pipeline follows:
1. **Research** — gather real metrics, pricing, standards, benchmarks
2. **Structure** — organize into the skill's native format (PlantUML, Vega JSON, Canvas JSON, HTML)
3. **Render** — produce gallery HTML with consistent dark theme (`#0a0e1a`)

## Skill Format (AgentSkills Standard)

Each skill in `.agents/skills/<name>/SKILL.md` uses YAML frontmatter:
```yaml
---
name: <skill-name>
description: <one-line description>
metadata:
  author: <attribution>
---
```

Body contains syntax rules, stencil references, examples, and pitfalls.

## Agent Format (OpenHands-Compatible)

Each agent in `.agents/agents/<name>.md` uses YAML frontmatter:
```yaml
---
name: <agent-name>
description: <when to use this agent>
model: inherit
tools: [<tool-list>]
skills: [<skill-list>]
---
```

Body is the system prompt injected into the agent's context.
