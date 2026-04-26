---
name: c4
description: Generate C4 model diagrams (System Context, Container, Component, Dynamic, Deployment) using PlantUML's C4-PlantUML stdlib. Industry-standard notation for software architecture, suitable for architecture review docs, RFCs, and exec presentations.
metadata:
  author: shekerkamma — addition to markdown-viewer/skills
---

# C4 Model Diagram Generator

**Quick Start:** Open a `@startuml` block → `!include` the appropriate C4 stdlib URL → declare `Person`, `System`, `Container`, `Component` → connect with `Rel(...)` → close with `@enduml`.

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
Person(user, "User")
System(app, "My Application", "Does the thing")
Rel(user, app, "Uses")
@enduml
```

## What is C4?

The C4 model is a hierarchy of four diagram types for describing software architecture, popularized by Simon Brown:

| Level | Diagram | Audience | Question it answers |
|---|---|---|---|
| 1 | **System Context** | Everyone | Who uses our system, and what does it talk to? |
| 2 | **Container** | Engineers + technical stakeholders | What apps / services / data stores make up the system? |
| 3 | **Component** | Engineers | What's inside a single container? |
| 4 | **Code** (UML class) | Engineers | What's inside a single component? *(rarely drawn — let your IDE do it)* |

Plus three supplementary diagrams: **Dynamic** (collaboration over time), **Deployment** (runtime infrastructure), and **System Landscape** (multiple systems in an enterprise).

## When to use this skill vs. others

| If you need… | Use |
|---|---|
| C4 inside GitHub Markdown, no toolchain | [mermaid](../mermaid/SKILL.md) `C4Context` block |
| Polished C4 with icons, gradients, layout control | **c4** (this skill) |
| TOGAF / ArchiMate enterprise modeling | [archimate](../archimate/SKILL.md) |
| Visual layered HTML architecture | [architecture](../architecture/SKILL.md) |

This skill produces higher-fidelity C4 than Mermaid's beta `C4Context` syntax. The tradeoff: it requires a PlantUML server (online or self-hosted) to render. Pick this for architecture review documents and exec slides; pick Mermaid for PRs and READMEs.

## Critical Rules

### Rule 1: Use the right include for the level
Each C4 level has its own stdlib include. They are cumulative — `C4_Container.puml` includes `C4_Context.puml`, and so on.

```plantuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Deployment.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Dynamic.puml
```

For air-gapped environments, mirror the repo and replace the URL with a local path. PlantUML caches `!include` content, so the first render is slow and subsequent ones are instant.

### Rule 2: One diagram = one C4 level
Don't mix levels. A Context diagram shows external actors and one big "your system" box — it does **not** show internal services. If you find yourself wanting to draw containers inside a system on a Context diagram, you need a separate Container diagram.

### Rule 3: Element vocabulary by level

| Level | Available elements |
|---|---|
| Context | `Person`, `Person_Ext`, `System`, `System_Ext`, `Enterprise_Boundary` |
| Container | + `Container`, `ContainerDb`, `ContainerQueue`, `Container_Boundary`, `System_Boundary` |
| Component | + `Component`, `ComponentDb`, `ComponentQueue`, `Component_Boundary` |
| Deployment | + `Deployment_Node`, `Node` |

`_Ext` variants render in gray to mark out-of-scope third parties.

### Rule 4: Relationship syntax with technology label

```plantuml
Rel(api, db, "Reads/writes", "JDBC")
Rel_R(api, db, "...", "...")    // force right
Rel_D(api, db, "...", "...")    // force down
Rel_L / Rel_U                    // left, up
BiRel(a, b, "talks to", "gRPC") // bidirectional
```

The fourth argument is the technology — render as italic gray. **Always include it** for Container and Component diagrams; it's what makes C4 useful for engineers.

### Rule 5: Use boundaries for organization
```plantuml
Enterprise_Boundary(b1, "Acme Corp") {
  System(internal, "Internal System")
}
System_Boundary(b2, "Order Domain") {
  Container(orderApi, "Order API", "Go", "Handles orders")
  ContainerDb(orderDb, "Order DB", "Postgres", "Order state")
}
```

Boundaries make Context diagrams readable when there are many external systems and Container diagrams readable when one system spans multiple bounded contexts.

### Rule 6: Layout hints over manual positioning
PlantUML auto-lays-out. Nudge it with directional `Rel_R / Rel_D / Rel_L / Rel_U` and `Lay_R(a, b)` / `Lay_D(a, b)` rather than fighting the engine. The `together { ... }` block forces grouping.

### Rule 7: Add `LAYOUT_WITH_LEGEND()` once per diagram
Renders the standard C4 legend (Person / System / External / Relationship). Without it, a stakeholder seeing a C4 diagram for the first time has to guess the notation.

## Examples

| File | Level | Demonstrates |
|---|---|---|
| [examples/system-context.md](examples/system-context.md) | Context | Persons, internal vs external systems, enterprise boundary |
| [examples/container.md](examples/container.md) | Container | Containers + databases, technology labels, system boundary |

## Rendering

PlantUML diagrams need a renderer. Options:

| Option | How |
|---|---|
| Online PlantUML server | Embed `https://www.plantuml.com/plantuml/svg/<encoded>` — works in any Markdown viewer |
| `docu.md` (markdown-viewer) | Renders inline via embedded PlantUML — see other skills in this repo |
| Local CLI | `plantuml -tsvg diagram.puml` (requires Java + Graphviz) |
| VS Code extension | "PlantUML" by jebbs |
| Static export for slides | `plantuml -tpng -dpi 200 diagram.puml` for high-DPI PNGs |

## Best Practices

1. **Start at Context, only zoom in when asked.** A Context diagram answers 80% of "what is this thing?" questions. Don't draw Containers/Components until someone needs them.
2. **One diagram per audience.** Exec deck → Context. Architecture review → Container. New-engineer onboarding → Container, then Component for the service they'll work on.
3. **Always label relationships with verbs.** "Reads/writes", "Publishes events to", "Authenticates against". `Rel(a, b, "")` is a code smell.
4. **Always include the technology** on Container/Component relationships. "REST/HTTPS", "gRPC", "Kafka", "JDBC". It's what separates C4 from boxes-and-lines.
5. **Use `_Ext` for SaaS/third-party.** Stripe, Auth0, Datadog — all `System_Ext`. Visual signal that you don't own them.
6. **Don't draw networking infrastructure** on Container diagrams. Load balancers, NAT gateways, VPCs belong on Deployment diagrams. Container diagrams show *logical* architecture.
7. **Pair with [archimate](../archimate/SKILL.md)** when the audience is enterprise architects. C4 is engineering-flavored; ArchiMate is enterprise-flavored.
