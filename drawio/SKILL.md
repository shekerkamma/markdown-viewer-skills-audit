---
name: drawio
description: Embed editable draw.io / diagrams.net diagrams inline in Markdown using the official viewer.js library. Best for network topologies, AWS/Azure/GCP architectures, BPMN, and any diagram that benefits from draw.io's 5,000+ shape library.
metadata:
  author: shekerkamma — addition to markdown-viewer/skills
---

# draw.io Diagram Generator

**Quick Start:** Author the diagram as mxGraph XML → wrap in `<div class="mxgraph" data-mxgraph='{"xml":"…"}'>` → include the viewer script tag once per page → diagrams auto-render in any browser.

## When to use this skill vs. others

| If you need… | Use |
|---|---|
| Static layered architecture with semantic colors | [architecture](../architecture/SKILL.md) |
| Quick flowchart / sequence / ER inside GitHub Markdown | [mermaid](../mermaid/SKILL.md) |
| Software architecture with industry-standard notation | [c4](../c4/SKILL.md) |
| Rich shape libraries (Cisco, AWS, Azure, BPMN, mockups), interactive viewing, "open-in-editor" round-trip | **drawio** (this skill) |

draw.io's strength is the shape catalog and the round-trip: anyone who clicks the diagram in the lightbox can copy the XML straight into [app.diagrams.net](https://app.diagrams.net) and edit it.

## Critical Rules

### Rule 1: One viewer script per page
Include this **once** per HTML page or rendered Markdown document — not per diagram:

```html
<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
```

For offline/air-gapped use, self-host `viewer-static.min.js` (~400 KB).

### Rule 2: Diagram = single `<div>` with JSON config
Every diagram is one `<div class="mxgraph">` with the XML packed into a `data-mxgraph` JSON attribute. **Do not** wrap the div in a code fence.

```html
<div class="mxgraph" style="max-width:100%;border:1px solid #ccc;"
     data-mxgraph='{"highlight":"#0000ff","nav":true,"toolbar":"zoom layers","edit":"_blank","xml":"<mxfile>…</mxfile>"}'></div>
```

### Rule 3: Escape the XML for JSON
The `xml` value is a JSON string, so `"` becomes `\"`, newlines become `\n`. The simplest workflow: keep the XML in a `.drawio` file during authoring, then minify + JSON-escape when embedding. See [examples/](examples/) for the pattern.

### Rule 4: mxGraph XML skeleton
Every diagram has the same outer shell. You only edit the `<root>` contents.

```xml
<mxfile host="app.diagrams.net">
  <diagram id="d1" name="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- your shapes & edges here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Rule 5: Cells are vertices or edges
- **Vertex** (shape): `<mxCell id="v1" value="Web Server" style="…" vertex="1" parent="1"><mxGeometry x="40" y="40" width="120" height="60" as="geometry"/></mxCell>`
- **Edge** (connector): `<mxCell id="e1" style="endArrow=classic;" edge="1" parent="1" source="v1" target="v2"><mxGeometry relative="1" as="geometry"/></mxCell>`

`parent="1"` puts the cell on the default page layer. `id` values must be unique within the diagram.

### Rule 6: Style strings drive appearance
Style is a semicolon-separated list of `key=value` pairs. The most useful ones:

| Key | Example | Effect |
|---|---|---|
| `shape` | `shape=cylinder3` | Built-in shape (database, cloud, actor, etc.) |
| `fillColor` | `fillColor=#dae8fc` | Background |
| `strokeColor` | `strokeColor=#6c8ebf` | Border |
| `rounded` | `rounded=1` | Rounded rectangle |
| `dashed` | `dashed=1` | Dashed border / line |
| `endArrow` | `endArrow=classic` | Arrowhead on edges |
| `mxgraph.aws4.ec2` | `shape=mxgraph.aws4.ec2` | Reference an AWS4 stencil |

Open [app.diagrams.net](https://app.diagrams.net), draw a shape you want, right-click → *Edit Style* — that gives you the exact style string to copy.

### Rule 7: Use shape libraries instead of redrawing
draw.io ships with these libraries — call them by their `mxgraph.<lib>.<shape>` style names rather than building rectangles by hand:

| Library | Style prefix | Coverage |
|---|---|---|
| AWS 4 | `mxgraph.aws4.*` | ~1,000 AWS service icons |
| Azure | `mxgraph.azure.*` | All Azure services |
| GCP | `mxgraph.gcp.*` | GCP service icons |
| Cisco | `mxgraph.cisco.*` | Routers, switches, firewalls |
| BPMN | `shape=mxgraph.bpmn.*` | BPMN 2.0 elements |
| Mockup | `shape=mxgraph.mockup.*` | Wireframe components |

## Viewer config options

Common `data-mxgraph` keys:

| Key | Default | Effect |
|---|---|---|
| `xml` | required | The mxfile XML |
| `nav` | `false` | Show page navigation if multi-page |
| `toolbar` | `null` | Space-separated: `pages zoom layers lightbox edit` |
| `lightbox` | `true` | Click-to-zoom modal |
| `edit` | `null` | URL to open editor; `_blank` = `app.diagrams.net` |
| `highlight` | `#0000ff` | Selection highlight color |
| `resize` | `true` | Auto-fit to container |

## Examples

| File | Diagram type | Demonstrates |
|---|---|---|
| [examples/flowchart.md](examples/flowchart.md) | Decision flowchart | Plain shapes, edges, labels — start here |
| [examples/aws-architecture.md](examples/aws-architecture.md) | AWS three-tier web app | `mxgraph.aws4.*` stencil library |
| [examples/network-topology.md](examples/network-topology.md) | DMZ + internal network | Cisco stencils, grouped containers |

## Best Practices

1. **Author in the editor, embed the export.** Build the diagram visually at app.diagrams.net, then *Extras → Edit Diagram* to copy the XML. Hand-writing mxGraph XML for anything beyond 10 cells is unproductive.
2. **Keep `.drawio` source alongside `.md`.** The XML embedded in HTML is hard to diff. Commit the original `.drawio` next to the Markdown.
3. **Don't escape twice.** When pasting XML into `data-mxgraph='{"xml":"…"}'`, escape `"` → `\"` *once*. Double-escaping silently breaks rendering.
4. **One viewer script per page.** Multiple `<script>` tags work but waste bandwidth.
5. **For air-gapped environments**, self-host viewer-static.min.js and add `<base>` or vendor it. Don't rely on the CDN for production docs.
6. **For static export** (PDF, PNG, slides): use the [drawio-desktop](https://github.com/jgraph/drawio-desktop) CLI — `drawio --export --format svg input.drawio` — and embed the SVG directly. The viewer script is only needed for interactive viewing.
