---
name: diagram-export
description: Reference cookbook of CLI commands to convert each diagram skill in this repo (Mermaid, PlantUML, Graphviz, draw.io, Vega) into slide-ready PNG/SVG. Pairs with marp and python-pptx — pre-render diagrams before embedding so decks are reproducible without internet.
metadata:
  author: shekerkamma — addition to markdown-viewer/skills
---

# Diagram Export Cookbook

**Quick Start:** Pick the diagram type → run the corresponding CLI → embed the resulting SVG/PNG in your slide deck or doc. Every command below is one-liner copyable.

## Why pre-render

Authoring tools (Marp, GitHub) render Mermaid/PlantUML on the fly via JavaScript or a server. That's fine for *viewing* but breaks for:

- **Slide decks.** PowerPoint doesn't run JavaScript — diagrams must be raster/vector before insertion.
- **Reproducible builds.** A `.pptx` regenerated next year should look identical. Pre-rendered SVG = git-trackable, internet-free.
- **High-DPI output.** Inline rendering targets screen DPI (~96). Slides need 200+ for projector clarity.
- **Air-gapped environments.** No CDN access for Mermaid's runtime, no PlantUML server.

## Universal targets

| Output | Use for | Notes |
|---|---|---|
| **SVG** | Any vector pipeline (Marp, browsers, Inkscape, Illustrator) | First choice. Crisp at any zoom. python-pptx does **not** accept SVG — convert to PNG first. |
| **PNG @ 1600px / 200 DPI** | python-pptx, PowerPoint, Word, Confluence, Slack | Wide enough for full-bleed 16:9 slides. |
| **PDF** | Print, archival, vector embed in LaTeX | Most CLIs can produce it directly. |

The recipes below default to SVG; PNG / PDF flags are noted alongside.

## Recipes by diagram source

### [mermaid](../mermaid/SKILL.md) — `.mmd` or fenced ` ```mermaid `

```bash
# Install once
npm i -g @mermaid-js/mermaid-cli

# SVG (preferred)
mmdc -i diagram.mmd -o diagram.svg

# PNG @ 1600px wide
mmdc -i diagram.mmd -o diagram.png -w 1600

# Dark theme + transparent background
mmdc -i diagram.mmd -o diagram.png -t dark -b transparent -w 1600

# Custom config (font, theme variables)
mmdc -i diagram.mmd -o diagram.svg -c mermaid.config.json
```

**Extracting from Markdown:** if your Mermaid source is inside a `.md` file, use `mmdc -i README.md -o out` — it auto-extracts every fenced block to `out-1.svg`, `out-2.svg`, etc.

### [c4](../c4/SKILL.md), [uml](../uml/SKILL.md), [bpmn](../bpmn/SKILL.md), [archimate](../archimate/SKILL.md), [cloud](../cloud/SKILL.md), [data-analytics](../data-analytics/SKILL.md), [iot](../iot/SKILL.md), [network](../network/SKILL.md), [security](../security/SKILL.md), [mindmap](../mindmap/SKILL.md) — PlantUML

```bash
# Install once  (Java + Graphviz are required)
brew install plantuml      # mac
sudo apt install plantuml  # debian/ubuntu — or download plantuml.jar

# SVG
plantuml -tsvg diagram.puml

# PNG @ 200 DPI
plantuml -tpng -dpi 200 diagram.puml

# PDF (vector)
plantuml -tpdf diagram.puml

# Render every .puml in a directory
plantuml -tsvg -o ./out 'src/**/*.puml'
```

**For mxgraph stencils** ([network](../network/SKILL.md), [security](../security/SKILL.md), [iot](../iot/SKILL.md), [data-analytics](../data-analytics/SKILL.md)): the upstream PlantUML jar does **not** include them. Use `docu.md`'s PlantUML fork or a stock setup will fail. Plain stdlib diagrams (cloud, bpmn, archimate, c4) work with any PlantUML.

### [graphviz](../graphviz/SKILL.md) — DOT

```bash
brew install graphviz       # mac
sudo apt install graphviz   # debian/ubuntu

dot -Tsvg graph.dot -o graph.svg
dot -Tpng -Gdpi=200 graph.dot -o graph.png
dot -Tpdf graph.dot -o graph.pdf

# Different layout engines
neato -Tsvg undirected.dot -o out.svg   # spring-model
twopi -Tsvg radial.dot -o out.svg        # radial tree
circo -Tsvg circular.dot -o out.svg      # circular
```

### [drawio](../drawio/SKILL.md) — `.drawio` XML

```bash
# Install desktop app once  (CLI is shipped inside)
brew install --cask drawio   # mac
# Linux: download .deb / .AppImage from https://github.com/jgraph/drawio-desktop/releases

# SVG
drawio --export --format svg --output diagram.svg diagram.drawio

# PNG with transparent background
drawio --export --format png --transparent --scale 2 --output diagram.png diagram.drawio

# All pages of a multi-page .drawio
drawio --export --format svg --crop --output diagram.svg diagram.drawio

# Headless (CI / Linux server) — needs xvfb
xvfb-run drawio --no-sandbox --export --format svg -o out.svg in.drawio
```

### [vega](../vega/SKILL.md) — Vega / Vega-Lite JSON

```bash
npm i -g vega-cli vega-lite

# Vega-Lite spec to SVG
vl2svg chart.vl.json chart.svg

# Vega-Lite to PNG @ 2x density
vl2png chart.vl.json chart.png -s 2

# Lower-level Vega spec (not Lite)
vg2svg chart.vg.json chart.svg
```

### [canvas](../canvas/SKILL.md) — JSON Canvas

JSON Canvas has no official renderer-to-image yet. Workaround: open in [Obsidian Canvas](https://obsidian.md) (free), use *File → Export → PDF*, then `pdftocairo -svg out.pdf out.svg` for vector or screenshot the canvas pane.

### [architecture](../architecture/SKILL.md), [infocard](../infocard/SKILL.md), [infographic](../infographic/SKILL.md) — HTML

These skills emit raw HTML. For slide embedding, render each one to PNG via headless Chrome:

```bash
# Wrap the HTML snippet in a minimal page (see demo-rendered/ for examples).
# Then headless-screenshot it:

google-chrome --headless --disable-gpu --no-sandbox \
  --window-size=1200,800 \
  --screenshot=architecture.png \
  file:///abs/path/to/diagram.html

# Or use Puppeteer for control over wait conditions and full-page captures:
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1240, height: 900, deviceScaleFactor: 2 });
  await page.goto('file:///abs/path/to/diagram.html', { waitUntil: 'networkidle0' });
  await page.screenshot({ path: 'architecture.png', fullPage: true });
  await browser.close();
})();
"
```

## Batch render every diagram in a repo

A common pattern when generating decks in CI:

```bash
#!/usr/bin/env bash
# render-all.sh — re-render every diagram source into ./diagrams/
set -euo pipefail
mkdir -p diagrams

# Mermaid: every .mmd file
find src -name '*.mmd' | while read f; do
  out="diagrams/$(basename "$f" .mmd).svg"
  mmdc -i "$f" -o "$out"
done

# PlantUML: every .puml file
plantuml -tsvg -o "$(pwd)/diagrams" 'src/**/*.puml'

# DOT: every .dot file
find src -name '*.dot' | while read f; do
  out="diagrams/$(basename "$f" .dot).svg"
  dot -Tsvg "$f" -o "$out"
done

# draw.io: every .drawio file
find src -name '*.drawio' | while read f; do
  out="diagrams/$(basename "$f" .drawio).svg"
  drawio --export --format svg --output "$out" "$f"
done

echo "Rendered $(ls diagrams | wc -l) diagrams to ./diagrams/"
```

Pair with [marp](../marp/SKILL.md) or [python-pptx](../python-pptx/SKILL.md): rendered SVGs in `./diagrams/` can be referenced from the deck source as `![](diagrams/foo.svg)`.

## Sizing reference for 16:9 slides

| Slide content | Pixel width @ 200 DPI | Inches |
|---|---|---|
| Full-bleed background | 2560 | 12.8 (1920px @ 150 DPI also fine) |
| Center diagram with margins | 1920 | 9.6 |
| Half-slide diagram | 1280 | 6.4 |
| Inline / quadrant | 800 | 4.0 |

For SVG, dimensions are infinite — these still matter for the *aspect ratio* you author at, since misaligned aspect ratios crop awkwardly.

## Best Practices

1. **Commit the rendered output.** Don't render diagrams in CI from scratch every time — commit `*.svg` alongside `*.mmd` so a new contributor can preview without installing the toolchain.
2. **Pin the renderer version.** `mmdc 11.x` and `mmdc 10.x` produce visibly different layouts. Pin in CI: `npm i -g @mermaid-js/mermaid-cli@11.4.0`.
3. **SVG first, PNG only when needed.** PowerPoint accepts both, but SVG stays sharp on any projector. PNG only for python-pptx (which can't read SVG) or when the SVG has fonts that won't be available.
4. **Embed fonts in the SVG.** PlantUML's `-tsvg` references system fonts — viewing on a machine without those fonts substitutes ugly defaults. Convert to PNG (which rasterizes the text) or convert SVG to outlines with `inkscape --export-text-to-path`.
5. **One diagram per file.** Don't put three Mermaid blocks in one Markdown file expecting `mmdc` to give you three named files — the auto-generated names are positional and brittle. Split into `flow-1.mmd`, `flow-2.mmd`.
6. **For air-gapped builds**, vendor the renderers: a Docker image with `plantuml.jar`, `mmdc`, `graphviz`, `drawio-headless` baked in. Build artifacts are then bit-reproducible.
