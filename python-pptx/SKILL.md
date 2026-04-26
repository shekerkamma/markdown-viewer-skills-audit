---
name: python-pptx
description: Generate PowerPoint decks programmatically from data using the python-pptx library. Best for templated decks — per-customer reports, weekly metrics, batched architecture summaries — where the deck structure is fixed but content varies per row.
metadata:
  author: shekerkamma — addition to markdown-viewer/skills
---

# python-pptx Slide Deck Generator

**Quick Start:** Install `python-pptx` → load a template `.pptx` → iterate over data → place text/images/shapes via the API → save. Outputs native, fully-editable PowerPoint files.

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation("template.pptx")
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Q2 Architecture Review"
slide.placeholders[1].text = "12 services · 3 incidents · 99.95% SLO"
prs.save("out.pptx")
```

## When to use this skill vs. [marp](../marp/SKILL.md)

| If you're… | Use |
|---|---|
| Authoring one deck by hand, want Markdown ergonomics | [marp](../marp/SKILL.md) |
| Generating one deck per row of a CSV / database query | **python-pptx** (this skill) |
| Building a PowerPoint *add-in* or modifying an existing deck | **python-pptx** |
| Combining diagrams from multiple skills into a presentation | [marp](../marp/SKILL.md) — easier composition |
| Need native PowerPoint shapes (charts, tables) the audience can edit | **python-pptx** |

**Rule of thumb:** if the input is *Markdown*, reach for Marp. If the input is *data*, reach for python-pptx.

## Critical Rules

### Rule 1: Always start from a template
Don't build slides from scratch — start from a `.pptx` template that has the slide masters, layouts, fonts, and brand colors already set up. python-pptx is for *populating* templates, not designing them.

```python
prs = Presentation("brand-template.pptx")    # good
prs = Presentation()                          # only for throwaway scripts
```

### Rule 2: Layouts are indexed but fragile
`prs.slide_layouts[0]` works but `[0]` could mean anything depending on the template. Look up by name:

```python
def layout(prs, name):
    for l in prs.slide_layouts:
        if l.name == name:
            return l
    raise KeyError(f"No layout named {name!r}; have {[l.name for l in prs.slide_layouts]}")

slide = prs.slides.add_slide(layout(prs, "Title and Content"))
```

### Rule 3: Placeholders > free shapes
Templates define placeholders (title, body, chart, image) with the right fonts/positions. Fill placeholders rather than adding new text boxes:

```python
slide.shapes.title.text = "..."           # title placeholder
slide.placeholders[1].text = "..."        # body placeholder by idx_id
# vs.
slide.shapes.add_textbox(...)              # last resort
```

### Rule 4: Units are Emu, but use helpers
PowerPoint uses English Metric Units (914,400 per inch). Always go through helpers:

```python
from pptx.util import Inches, Pt, Emu, Cm

left, top, width, height = Inches(1), Inches(2), Inches(8), Inches(4.5)
slide.shapes.add_picture("diagram.png", left, top, width, height)
```

### Rule 5: Image insertion via `add_picture`
```python
from pptx.util import Inches
pic = slide.shapes.add_picture("diagram.svg", Inches(1), Inches(1.5),
                                width=Inches(11), height=Inches(5))
```

**SVG is *not* natively supported.** Pre-render diagrams to PNG via the [diagram-export](../diagram-export/SKILL.md) skill — typically 1600px wide at 200 DPI for crisp 16:9 slides.

### Rule 6: Text styling is hierarchical
A `text_frame` contains `paragraphs`, which contain `runs`. Style at the run level for color/bold; at the paragraph level for alignment.

```python
tf = slide.placeholders[1].text_frame
tf.text = "First bullet"          # creates one paragraph

p2 = tf.add_paragraph()
p2.text = "Second bullet"
p2.level = 1                       # indent

run = p2.runs[0]
run.font.bold = True
run.font.size = Pt(18)
run.font.color.rgb = RGBColor(0x1d, 0x4e, 0xd8)
```

### Rule 7: Native charts > image charts
For data charts, use python-pptx's `add_chart` API rather than rendering with matplotlib and inserting as an image. Native charts let the audience edit the data inside PowerPoint.

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

data = CategoryChartData()
data.categories = ["Q1", "Q2", "Q3", "Q4"]
data.add_series("Revenue ($M)", (12.4, 14.1, 15.8, 19.2))
slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                        Inches(1), Inches(2), Inches(11), Inches(5), data)
```

### Rule 8: Speaker notes survive `.pptx`
```python
slide.notes_slide.notes_text_frame.text = "Walk through the trend, mention churn risk."
```

## Examples

| File | Demonstrates |
|---|---|
| [examples/quarterly-review.py](examples/quarterly-review.py) | Per-customer deck — title slide, KPI grid, embedded chart, architecture diagram from disk |

## Common patterns

### Find every placeholder index in a layout (for debugging templates)

```python
for layout in prs.slide_layouts:
    print(f"\n{layout.name}")
    for ph in layout.placeholders:
        print(f"  idx={ph.placeholder_format.idx} type={ph.placeholder_format.type} name={ph.name!r}")
```

### Replace every occurrence of a token in the template

```python
def replace_text(slide, mapping):
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                for token, value in mapping.items():
                    if token in run.text:
                        run.text = run.text.replace(token, value)

# Use {{tokens}} in your template, then:
replace_text(slide, {"{{customer_name}}": "Acme Corp", "{{quarter}}": "Q2 2026"})
```

This pattern lets non-engineers maintain the template (move boxes around, restyle) while the script just fills tokens — clean separation of design vs. content.

### One deck per row of input

```python
import csv
from pathlib import Path

with open("customers.csv") as f:
    for row in csv.DictReader(f):
        prs = Presentation("template.pptx")
        for slide in prs.slides:
            replace_text(slide, {
                "{{customer_name}}": row["name"],
                "{{mrr}}": f"${int(row['mrr']):,}",
                "{{health_score}}": row["health"],
            })
        Path("out").mkdir(exist_ok=True)
        prs.save(f"out/{row['name'].replace(' ', '-').lower()}.pptx")
```

## Best Practices

1. **Template ownership.** Designers own the `.pptx` template; engineers own the script. Don't mix.
2. **Token replacement over programmatic shape creation.** It's tempting to `add_textbox` everywhere — resist. Tokens in the template + `replace_text` keeps the template editable.
3. **One image, sized correctly.** A 4000×3000 PNG dropped into a 11×5-inch placeholder bloats the file. Pre-resize to ~1600px wide before insertion.
4. **Don't reinvent charts.** `XL_CHART_TYPE` covers 70+ chart kinds. Use them — your audience can edit the data, change the chart type, copy it into Excel.
5. **Render SVG diagrams to PNG first.** python-pptx ignores SVGs in `add_picture`. Use the [diagram-export](../diagram-export/SKILL.md) recipes.
6. **Validate with LibreOffice in CI.** `libreoffice --headless --convert-to pdf out.pptx` will fail loudly if you produced a malformed .pptx — better to catch this in CI than in front of an exec.
7. **Set fonts via the template, not the script.** If you're calling `run.font.name = "Arial"` in code, your template is wrong. Fix the template's slide masters.

## When *not* to use python-pptx

- One-off decks → use Marp or PowerPoint directly. python-pptx is overkill.
- Complex animations → not supported by python-pptx; build in PowerPoint.
- Editing decks containing complex SmartArt → python-pptx will round-trip but may lose fidelity. Test before committing.
