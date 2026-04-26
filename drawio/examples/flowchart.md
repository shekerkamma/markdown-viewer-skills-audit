# draw.io Example — Decision Flowchart

A minimal flowchart with start/end terminals, a process step, a decision diamond, and labeled edges. Demonstrates the basic vertex + edge pattern with no external stencils.

## Source XML (`flowchart.drawio`)

```xml
<mxfile host="app.diagrams.net">
  <diagram id="flow1" name="Login Flow">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="600" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="start" value="Start" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="360" y="40" width="120" height="40" as="geometry"/></mxCell>
        <mxCell id="login" value="Submit credentials" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1"><mxGeometry x="340" y="120" width="160" height="50" as="geometry"/></mxCell>
        <mxCell id="check" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="360" y="210" width="120" height="80" as="geometry"/></mxCell>
        <mxCell id="ok" value="Issue session token" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="540" y="225" width="180" height="50" as="geometry"/></mxCell>
        <mxCell id="fail" value="Increment fail counter" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1"><mxGeometry x="120" y="225" width="180" height="50" as="geometry"/></mxCell>
        <mxCell id="end" value="End" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="580" y="320" width="100" height="40" as="geometry"/></mxCell>
        <mxCell id="e1" style="endArrow=classic;html=1;" edge="1" parent="1" source="start" target="login"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" style="endArrow=classic;html=1;" edge="1" parent="1" source="login" target="check"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" value="yes" style="endArrow=classic;html=1;" edge="1" parent="1" source="check" target="ok"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" value="no" style="endArrow=classic;html=1;" edge="1" parent="1" source="check" target="fail"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e5" style="endArrow=classic;html=1;" edge="1" parent="1" source="ok" target="end"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e6" style="endArrow=classic;html=1;dashed=1;" edge="1" parent="1" source="fail" target="login"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Embedded in Markdown

Add the viewer script tag once at the top of the page (or in your site template):

```html
<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
```

Then drop the diagram in:

<div class="mxgraph" style="max-width:100%;border:1px solid #ddd;border-radius:4px;"
     data-mxgraph='{"highlight":"#0000ff","nav":true,"toolbar":"zoom layers lightbox","edit":"_blank","xml":"<mxfile host=\"app.diagrams.net\"><diagram id=\"flow1\" name=\"Login Flow\"><mxGraphModel dx=\"800\" dy=\"600\" grid=\"1\" gridSize=\"10\" guides=\"1\" tooltips=\"1\" connect=\"1\" arrows=\"1\" fold=\"1\" page=\"1\" pageScale=\"1\" pageWidth=\"850\" pageHeight=\"600\" math=\"0\" shadow=\"0\"><root><mxCell id=\"0\"/><mxCell id=\"1\" parent=\"0\"/><mxCell id=\"start\" value=\"Start\" style=\"ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;\" vertex=\"1\" parent=\"1\"><mxGeometry x=\"360\" y=\"40\" width=\"120\" height=\"40\" as=\"geometry\"/></mxCell><mxCell id=\"login\" value=\"Submit credentials\" style=\"rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;\" vertex=\"1\" parent=\"1\"><mxGeometry x=\"340\" y=\"120\" width=\"160\" height=\"50\" as=\"geometry\"/></mxCell><mxCell id=\"check\" value=\"Valid?\" style=\"rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;\" vertex=\"1\" parent=\"1\"><mxGeometry x=\"360\" y=\"210\" width=\"120\" height=\"80\" as=\"geometry\"/></mxCell><mxCell id=\"ok\" value=\"Issue session token\" style=\"rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;\" vertex=\"1\" parent=\"1\"><mxGeometry x=\"540\" y=\"225\" width=\"180\" height=\"50\" as=\"geometry\"/></mxCell><mxCell id=\"fail\" value=\"Increment fail counter\" style=\"rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;\" vertex=\"1\" parent=\"1\"><mxGeometry x=\"120\" y=\"225\" width=\"180\" height=\"50\" as=\"geometry\"/></mxCell><mxCell id=\"end\" value=\"End\" style=\"ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;\" vertex=\"1\" parent=\"1\"><mxGeometry x=\"580\" y=\"320\" width=\"100\" height=\"40\" as=\"geometry\"/></mxCell><mxCell id=\"e1\" style=\"endArrow=classic;html=1;\" edge=\"1\" parent=\"1\" source=\"start\" target=\"login\"><mxGeometry relative=\"1\" as=\"geometry\"/></mxCell><mxCell id=\"e2\" style=\"endArrow=classic;html=1;\" edge=\"1\" parent=\"1\" source=\"login\" target=\"check\"><mxGeometry relative=\"1\" as=\"geometry\"/></mxCell><mxCell id=\"e3\" value=\"yes\" style=\"endArrow=classic;html=1;\" edge=\"1\" parent=\"1\" source=\"check\" target=\"ok\"><mxGeometry relative=\"1\" as=\"geometry\"/></mxCell><mxCell id=\"e4\" value=\"no\" style=\"endArrow=classic;html=1;\" edge=\"1\" parent=\"1\" source=\"check\" target=\"fail\"><mxGeometry relative=\"1\" as=\"geometry\"/></mxCell><mxCell id=\"e5\" style=\"endArrow=classic;html=1;\" edge=\"1\" parent=\"1\" source=\"ok\" target=\"end\"><mxGeometry relative=\"1\" as=\"geometry\"/></mxCell><mxCell id=\"e6\" style=\"endArrow=classic;html=1;dashed=1;\" edge=\"1\" parent=\"1\" source=\"fail\" target=\"login\"><mxGeometry relative=\"1\" as=\"geometry\"/></mxCell></root></mxGraphModel></diagram></mxfile>"}'></div>

## Notes

- The `dashed=1` style on `e6` shows the retry path differently from forward flow.
- Click the diagram → lightbox modal opens. The "edit" button (toolbar) opens the XML in app.diagrams.net.
- Total source: 6 vertices, 6 edges. Anything bigger, build it visually first and export.
