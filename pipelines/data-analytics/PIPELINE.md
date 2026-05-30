# Data & Analytics Category — Pipeline Tests

End-to-end pipeline combining **project-level** visualization skills (`data-analytics`, `vega`) with **global-level** analytics and communication skills (`ai-analyst`, `analytics-to-comms`, `health`) for data pipeline documentation, metric visualization, and stakeholder reporting.

## Skills in this pipeline

### Project-level (installed in `.agents/skills/`)
| Skill | Role | Output | Notation |
|---|---|---|---|
| `data-analytics` | Data pipeline architecture diagrams (ETL, streaming, warehouse, lake) | PlantUML (` ```plantuml `) | `mxgraph.aws4.*` — analytics stencils (`glue`, `kinesis`, `redshift`, `athena`, `quicksight`, `s3`, `lake_formation`) |
| `vega` | Statistical charts and data visualization | Vega-Lite JSON (` ```vega-lite `) or Vega JSON (` ```vega `) | Declarative: mark type + encoding + data type. Vega for radar/wordcloud/force-directed |
| `infographic` | Visual overviews / dashboards | Templated HTML | Space-separated key-value syntax |
| `infocard` | Metric cards and summaries | Embedded HTML | Direct HTML |
| `architecture` | Layered HTML summary view | Embedded HTML | Direct HTML |
| `marp` / `slide-narrative` | Presentation layer | Markdown slides / prose | Marp frontmatter |
| `diagram-export` | Rasterize diagrams | Image files | CLI commands |

### Global-level (in `~/.claude/skills/`)
| Skill | Role | Output |
|---|---|---|
| `ai-analyst` | Business question → validated findings + charts | Analysis report + Marp deck |
| `analytics-to-comms` | Orchestrator: analytics → infographic → slides → Slack/Notion | Multi-format package |
| `health` | Code quality dashboard (type, lint, test, dead code) | Composite 0-10 score + trends |

### How They Connect

```
data-analytics ──→ vega ──→ infographic ──→ infocard
(pipeline arch)   (charts)   (visual)       (metric cards)
      │              │           │               │
      └──────┬───────┘           └───────┬───────┘
             │                           │
             ▼                           ▼
       diagram-export              marp / slide-narrative
             │                           │
             └───────────┬───────────────┘
                         ▼
                  analytics-to-comms (global)
                         │
                         ▼
                   ai-analyst (global)
                         │
                         ▼
                    health (global)
```

---

## Pipeline 1: Data Platform Architecture + Metrics Dashboard

**Goal:** Document a complete data platform — pipeline architecture diagram, metric charts for pipeline health, and an executive dashboard.

**System under test:** E-commerce analytics platform ingesting clickstream, order, and inventory data.

### Step 1 — Data pipeline architecture
**Skill:** `data-analytics`

> Use the data-analytics skill to draw the data platform for an e-commerce analytics system. Left-to-right flow:
>
> **Sources zone:** Aurora (orders DB), DynamoDB (user sessions), Kinesis Data Streams (clickstream), S3 (product catalog CSVs)
>
> **Ingestion zone:** Glue Crawlers discover schemas, Kinesis Data Firehose buffers clickstream, DynamoDB Streams capture CDC events
>
> **Processing zone:** Glue ETL jobs transform and join data, EMR (Spark) runs daily aggregation jobs, Lambda handles real-time enrichment
>
> **Storage zone:** S3 Data Lake (raw + curated tiers managed by Lake Formation), Redshift (star-schema warehouse)
>
> **Serving zone:** Athena for ad-hoc SQL on the lake, Redshift for BI queries, ElastiCache (Redis) for pre-computed dashboard metrics
>
> **Visualization zone:** QuickSight dashboards, custom React app via Athena API
>
> Show batch flows (`-->`) for nightly ETL and streaming flows (`..>`) for real-time clickstream.

**Grade:**
- [ ] `@startuml` / `@enduml`, `left to right direction`
- [ ] ` ```plantuml ` fence
- [ ] `mxgraph.aws4.*` stencils: `aurora`, `dynamodb`, `kinesis_data_streams`, `s3`, `glue`, `glue_crawlers`, `kinesis_data_firehose`, `dynamodb_stream`, `emr`, `lambda_function`, `lake_formation`, `redshift`, `athena`, `elasticache_for_redis`, `quicksight`
- [ ] Six `rectangle` zones matching the pipeline stages
- [ ] Batch `-->` and streaming `..>` visually distinguished
- [ ] Labels on connections: `"nightly ETL"`, `"real-time CDC"`, `"clickstream"`, `"ad-hoc SQL"`
- [ ] No manual `fillColor`/`strokeColor`

### Step 2 — Pipeline health metrics (Vega-Lite)
**Skill:** `vega`

> Create four Vega-Lite charts for the data platform dashboard:
>
> **2a. Throughput line chart:** Daily records processed over 30 days. Two series: "Batch ETL" (avg 12M/day) and "Streaming" (avg 45M/day). X: date (temporal), Y: records (quantitative), color: pipeline type (nominal).
>
> **2b. Latency heatmap:** Hours (0-23) on X axis, days of week on Y axis, color intensity = p99 query latency in ms. Show that weekday business hours (9-17) are hotspots.
>
> **2c. Cost breakdown stacked bar:** Monthly cost for last 6 months. Stacks: Redshift, Glue, Kinesis, S3, EMR. Show that Redshift dominates cost.
>
> **2d. Data freshness gauge:** Grouped bar comparing target freshness vs. actual freshness for each data domain: Orders (target: 1h, actual: 45min), Clickstream (target: 5min, actual: 3min), Inventory (target: 24h, actual: 22h), Product Catalog (target: 24h, actual: 26h — OVER target, highlight in red).

**Grade:**
- [ ] All four charts valid JSON with `$schema`
- [ ] ` ```vega-lite ` fence for each
- [ ] **2a:** `"mark": "line"`, `"encoding"` with temporal x, quantitative y, nominal color. Two series in data.
- [ ] **2b:** `"mark": "rect"`, x = hour (ordinal), y = day (ordinal), color = latency (quantitative). Scale shows hotspot pattern.
- [ ] **2c:** `"mark": "bar"`, stacked via `"stack": true` on y encoding, color = service (nominal), x = month (ordinal)
- [ ] **2d:** `"mark": "bar"`, grouped (not stacked), with conditional color for over-target values
- [ ] Field names case-sensitive and matching data array
- [ ] Data types: `quantitative`/`nominal`/`ordinal`/`temporal` (NOT `numeric`/`string`/`date`)

### Step 3 — Executive dashboard infographic
**Skill:** `infographic`

> Create a dashboard infographic showing the platform's key metrics:
>
> - Total records processed: 1.7B/month
> - Pipeline uptime: 99.94%
> - Average query latency: 340ms (p50), 1.2s (p99)
> - Monthly cost: $47K (down 12% after Redshift RA3 migration)
> - Data freshness SLA compliance: 96% (orders/clickstream on target, inventory slightly over)
> - Active dashboards: 42 (accessed by 180 users)
>
> Use the `stats-dashboard` or `metrics` template.

**Grade:**
- [ ] Space-separated key-value syntax (NOT YAML colons)
- [ ] `desc` not `description`
- [ ] 2-space indentation
- [ ] All 6 metrics included with correct values
- [ ] Trend annotations (down 12%, on target/over)

### Step 4 — Metric cards
**Skill:** `infocard`

> Create three metric cards:
> 1. **Pipeline Health** — uptime 99.94%, last incident 18 days ago, MTTR 23 min
> 2. **Cost Efficiency** — $47K/month, $0.027 per million records, 12% reduction MoM
> 3. **Data Quality** — 99.2% schema validation pass rate, 0.3% null rate, 4 DQ rules triggered this week
>
> Use `metric-board` layout. Business tone.

**Grade:**
- [ ] 3 cards with metrics prominently displayed
- [ ] Direct HTML, no code fence
- [ ] Business tone (not tech-blueprint)
- [ ] Trend indicators included

### Step 5 — Presentation
**Skills:** `slide-narrative` → `marp`

> 1. Outline a 10-minute quarterly data platform review for the VP of Engineering. Goal: approve $15K/month budget increase for Redshift RA3 upgrade (pays for itself in 3 months via cost savings). Audience: technical leadership.
> 2. Build the Marp deck embedding the pipeline architecture diagram and key Vega charts.

**Grade:**
- [ ] Narrative builds to the $15K ask with ROI argument
- [ ] Pipeline architecture diagram referenced
- [ ] Vega charts embedded or described for inclusion
- [ ] Marp deck with speaker notes and valid frontmatter

---

## Pipeline 2: Real-Time Streaming Architecture + Monitoring

**Goal:** Document a real-time streaming pipeline with live monitoring dashboards.

### Step 1 — Streaming architecture
**Skill:** `data-analytics`

> Draw a real-time streaming architecture for fraud detection in a payment platform:
>
> - Sources: Payment Gateway (transaction events), User Service (login events), Device Fingerprint service
> - Ingestion: MSK (Kafka) with 3 topics: transactions, logins, device-signals
> - Processing: Kinesis Data Analytics (Flink) for real-time pattern matching, Lambda for enrichment (lookup user history from DynamoDB)
> - Storage: DynamoDB (fraud decisions, TTL 90 days), S3 (raw events for audit), OpenSearch (searchable fraud log)
> - Alerting: SNS → PagerDuty for high-confidence fraud, SQS → manual review queue for medium-confidence
>
> Show all connections as streaming (`..>`) since everything is real-time.

**Grade:**
- [ ] All connections `..>` (dashed — streaming)
- [ ] `mxgraph.aws4.msk` for Kafka, `mxgraph.aws4.kinesis_data_analytics` for Flink
- [ ] Two output paths: auto-block (high confidence) and manual review (medium confidence)
- [ ] Audit trail to S3 shown as a side branch

### Step 2 — Monitoring charts
**Skill:** `vega`

> Create three monitoring charts:
>
> **2a. Transaction volume area chart:** 24 hours of transaction volume (1-minute granularity). Two overlaid areas: "Normal" baseline band and "Actual" volume. Highlight any 1-minute window where actual > 2x baseline.
>
> **2b. Fraud rate scatter plot:** Each point = 1 hour. X = transaction count (quantitative), Y = fraud rate % (quantitative), color = risk tier (nominal: low/medium/high), size = dollar amount flagged (quantitative). Tooltip on hover showing the hour and values.
>
> **2c. Dual-axis line chart:** Processing latency (left Y, ms) and throughput (right Y, transactions/sec) over 24 hours. Must use `resolve: {scale: {y: "independent"}}` for dual axis.

**Grade:**
- [ ] **2a:** `"mark": "area"`, two layers (baseline + actual), conditional highlight for anomaly windows
- [ ] **2b:** `"mark": "point"`, four encodings: x (quantitative), y (quantitative), color (nominal), size (quantitative), tooltip configured
- [ ] **2c:** Layer with two marks, `"resolve": {"scale": {"y": "independent"}}` for dual axis
- [ ] All valid JSON with `$schema`, ` ```vega-lite ` fence

### Step 3 — CDC pipeline architecture
**Skill:** `data-analytics`

> Draw a CDC (Change Data Capture) pipeline that keeps the fraud detection system's lookup tables fresh:
>
> - Source: Aurora (user profiles, merchant profiles) with DynamoDB Streams
> - CDC: DynamoDB Streams → Lambda (transform) → DynamoDB (denormalized lookup table)
> - Also: Aurora → Glue CDC job (daily) → S3 (historical snapshots) → Athena (for investigation queries)
>
> Show two paths: real-time CDC (`..>`) and batch snapshot (`-->`).

**Grade:**
- [ ] Two distinct paths visually separated
- [ ] `mxgraph.aws4.dynamodb_stream` for CDC source
- [ ] Real-time `..>` and batch `-->` distinguished
- [ ] Lookup table shown feeding back into the fraud detection pipeline from Step 1

---

## Pipeline 3: Analytics Question → Communication

**Goal:** Use `ai-analyst` to answer a business question, then pipe through visualization and communication skills.

### Step 1 — Business question
**Skill:** `ai-analyst` (global)

> Analyze: "Which marketing channel has the highest customer acquisition cost (CAC), and is it justified by lifetime value (LTV)?"
>
> Data: Channels are Paid Search ($45 CAC, $180 LTV), Social Ads ($62 CAC, $95 LTV), Organic ($12 CAC, $210 LTV), Email ($8 CAC, $160 LTV), Affiliate ($38 CAC, $140 LTV).

**Grade:**
- [ ] Question framed with hypothesis
- [ ] Data validated (CAC/LTV ratios calculated)
- [ ] Finding: Social Ads has worst LTV/CAC ratio (1.53x — below 3x threshold)
- [ ] Recommendation with confidence level

### Step 2 — Visualize findings
**Skill:** `vega`

> Based on the ai-analyst findings, create:
>
> **2a. Grouped bar chart:** Channel (x, nominal) with two bars per channel: CAC and LTV (quantitative). Color distinguishes CAC vs LTV.
>
> **2b. Scatter plot:** X = CAC (quantitative), Y = LTV (quantitative), each point = channel (labeled). Add a diagonal reference line showing 3:1 LTV/CAC threshold. Points below the line are underperforming.
>
> **2c. Horizontal bar chart:** LTV/CAC ratio per channel, sorted descending. Conditional color: green if ratio > 3, yellow if 2-3, red if < 2.

**Grade:**
- [ ] **2a:** Grouped (not stacked) bars, both metrics visible per channel
- [ ] **2b:** Reference line at 3:1 ratio via a `"layer"` with `"mark": "rule"` or a calculated line
- [ ] **2c:** Sorted by ratio descending, conditional color encoding
- [ ] Data matches the ai-analyst findings exactly

### Step 3 — Pipeline architecture for the analytics
**Skill:** `data-analytics`

> Draw the data pipeline that feeds the CAC/LTV analysis:
>
> - Sources: Google Ads API, Facebook Ads API, Stripe (payments), Mixpanel (events)
> - Ingestion: Lambda functions pulling from each API → S3 raw zone
> - Processing: Glue ETL → join ad spend with revenue attribution → S3 curated zone
> - Warehouse: Redshift (marketing_analytics schema)
> - BI: QuickSight dashboard + Athena for ad-hoc

**Grade:**
- [ ] Four source systems shown with appropriate stencils
- [ ] S3 raw → Glue → S3 curated → Redshift pipeline
- [ ] Connection labels describe the data (`"ad spend"`, `"revenue events"`, `"attribution join"`)

### Step 4 — Infographic summary
**Skill:** `infographic`

> Create an infographic comparing all 5 marketing channels. Use the `comparison` or `ranking` template. Show: channel name, CAC, LTV, LTV/CAC ratio, verdict (scale/maintain/cut).

**Grade:**
- [ ] Space-separated key-value syntax
- [ ] All 5 channels with correct metrics
- [ ] Verdict clearly stated per channel

### Step 5 — Full communication package
**Skill:** `analytics-to-comms` (global)

> Package the analysis into a stakeholder communication:
> 1. Run the analysis (already done in Step 1)
> 2. Create an explainer graphic for the CMO
> 3. Build a 5-slide Marp deck: Finding, Channel Comparison, Recommendation, Budget Reallocation Proposal, Next Steps
> 4. Draft a Slack post for #marketing-analytics summarizing the key finding

**Grade:**
- [ ] Infographic/explainer produced (not just text)
- [ ] Marp deck with 5 slides, valid frontmatter, speaker notes
- [ ] Slack post concise (3-5 sentences), links to full analysis
- [ ] All outputs reference the same data consistently

---

## Pipeline 4: Code Health Dashboard

**Goal:** Use `health` to assess a project, then visualize the results with `vega` and `data-analytics`.

### Step 1 — Run health check
**Skill:** `health` (global)

> Run `/health` on the current project. Show the composite score and category breakdown.

**Grade:**
- [ ] Health stack detected (what tools are available)
- [ ] Categories scored: type (25%), lint (20%), test (30%), dead code (15%), shell (10%)
- [ ] Composite 0-10 score calculated
- [ ] Ranked recommendations for improvement

### Step 2 — Visualize health trends
**Skill:** `vega`

> Create a multi-series line chart showing health score trends over 8 weeks (simulate data). Five lines: Type Safety, Linting, Test Coverage, Dead Code, Shell Quality. X: week (ordinal), Y: score 0-10 (quantitative), color: category (nominal). Add a horizontal rule at score 7 (team target).

**Grade:**
- [ ] `"mark": "line"`, 5 series distinguished by color
- [ ] Horizontal rule via layer with `"mark": "rule"` at y=7
- [ ] Valid temporal or ordinal x encoding
- [ ] Target line labeled

### Step 3 — Health architecture diagram
**Skill:** `data-analytics`

> Draw the data pipeline for the health metrics system:
> - Sources: GitHub Actions (CI runs), tsc/biome/bun output (piped to S3)
> - Processing: Lambda parses tool output → DynamoDB (score history)
> - Visualization: QuickSight health dashboard

**Grade:**
- [ ] Simple 3-zone pipeline (source → process → visualize)
- [ ] Appropriate stencils for CI/CD context

---

## Pipeline 5: Vega Deep-Dive — Chart Type Coverage

**Goal:** Test every major chart type Vega/Vega-Lite supports.

### Step 1 — Basic marks
**Skill:** `vega`

> Create one chart of each basic mark type using sample data:
> 1. **Bar chart:** Top 5 programming languages by GitHub stars
> 2. **Line chart:** Monthly website traffic over 12 months
> 3. **Point (scatter):** Height vs. weight for 20 people, colored by gender
> 4. **Area chart:** Cumulative revenue over 4 quarters
> 5. **Arc (pie/donut):** Budget allocation across 5 departments

**Grade:**
- [ ] Each chart uses the correct mark: `bar`, `line`, `point`, `area`, `arc`
- [ ] All include `$schema`
- [ ] Field names match data exactly (case-sensitive)
- [ ] Data types correct: `quantitative`/`nominal`/`ordinal`/`temporal`

### Step 2 — Advanced charts (Vega)
**Skill:** `vega`

> Create charts that require full Vega (not Vega-Lite):
> 1. **Radar chart:** Compare 5 product features across 3 competitors (performance, usability, price, support, ecosystem)
> 2. **Word cloud:** Top 30 keywords from customer feedback, sized by frequency

**Grade:**
- [ ] ` ```vega ` fence (not ` ```vega-lite `)
- [ ] `$schema` points to Vega (not Vega-Lite)
- [ ] **Radar:** Polar coordinates, multiple overlaid paths
- [ ] **Word cloud:** Word placement algorithm, size encoding by frequency

### Step 3 — Interactive features
**Skill:** `vega`

> Create a Vega-Lite chart with interactive selection:
> - Scatter plot of 50 products: X = price, Y = rating, color = category
> - Add interval selection: user can brush-select a region to highlight points
> - Add a linked bar chart below showing category counts of the selected points

**Grade:**
- [ ] `"params"` with `"select": "interval"` for brush selection
- [ ] `"condition"` on color encoding for selection feedback
- [ ] `"vconcat"` linking scatter to bar chart
- [ ] Valid interactive spec

---

## Pipeline 6: Adversarial & Edge Cases

### 6a — Vega: invalid data types
> Create a Vega-Lite bar chart with `"type": "numeric"` for the Y axis.

**Expected:** Correction — `numeric` is not a valid type. Must be `quantitative`. Should fix to the correct type.

### 6b — Vega: trailing comma
> Create a chart with this spec:
> ```json
> {"mark": "bar", "encoding": {"x": {"field": "a",}}}
> ```

**Expected:** Correction — trailing comma is invalid JSON. Should produce valid JSON.

### 6c — data-analytics: use ` ```text ` fence
> Use the data-analytics skill to draw a pipeline. Output it in a ` ```text ` block.

**Expected:** Refusal — skill requires ` ```plantuml ` fence, never ` ```text `.

### 6d — Vega: wrong chart type
> Create a Vega-Lite radar chart.

**Expected:** Correction — Vega-Lite doesn't support radar. Should suggest full Vega with ` ```vega ` fence, or offer a grouped bar as an alternative.

### 6e — data-analytics: 30 services in one diagram
> Draw a data pipeline with all 30 AWS analytics services in one diagram.

**Expected:** Pushback — 30 services in one diagram is unreadable. Should suggest decomposing into sub-diagrams (ingestion, processing, storage, serving) or using the `architecture` skill for a summary view.

### 6f — Infographic: YAML syntax
> Create an infographic:
> ```
> title: My Dashboard
> items:
>   - name: Revenue
>     description: $1.2M this quarter
> ```

**Expected:** Correction — infographic uses space-separated syntax, not YAML. Should show correct format: `title My Dashboard`, `desc $1.2M this quarter`.

---

## Grading Summary

| Pipeline | Steps | What it proves |
|---|---|---|
| **1: Platform Architecture + Dashboard** | 5 | `data-analytics` pipeline → `vega` charts → `infographic` → `infocard` → presentation |
| **2: Real-Time Streaming** | 3 | Streaming-specific architecture; monitoring charts; CDC pattern |
| **3: Analytics → Communication** | 5 | `ai-analyst` → `vega` → `data-analytics` → `infographic` → `analytics-to-comms` full chain |
| **4: Code Health** | 3 | `health` → `vega` trends → `data-analytics` pipeline for metrics system |
| **5: Vega Deep-Dive** | 3 | Every chart type: basic marks, Vega-only (radar, wordcloud), interactive selection |
| **6: Adversarial** | 6 | JSON validity, data types, fence types, chart type limits, diagram scale |

### Pass criteria
- **data-analytics passes** when: valid PlantUML, correct `mxgraph.aws4.*` stencils, pipeline stages grouped in zones, batch vs. streaming visually distinct.
- **vega passes** when: valid JSON, `$schema` present, correct data types (`quantitative`/`nominal`/`ordinal`/`temporal`), field names case-match data, correct mark type for the visualization goal.
- **Cross-skill consistency** when: metrics in Vega charts match values in infographic and infocard; pipeline architecture matches the data flow described in the analysis.
- **Adversarial tests pass** when invalid syntax is corrected and wrong chart/fence types are caught.
