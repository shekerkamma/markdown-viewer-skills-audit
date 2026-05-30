---
marp: true
theme: uncover
size: 16:9
paginate: true
footer: 'Agentic AI Use Cases Across Industries | Grounded by Domain Agents'
backgroundColor: '#0a0e1a'
color: '#e2e8f0'
style: |
  section {
    font-family: 'Segoe UI', system-ui, sans-serif;
  }
  h1 { color: #00d4aa; font-size: 2.2em; }
  h2 { color: #00d4aa; font-size: 1.6em; }
  h3 { color: #f59e0b; font-size: 1.2em; }
  strong { color: #00d4aa; }
  code { background: #1e293b; color: #7dd3fc; font-size: 0.75em; }
  pre { background: #1e293b; border-radius: 8px; padding: 16px; font-size: 0.65em; }
  table { font-size: 0.72em; }
  th { background: #00d4aa; color: #0a0e1a; }
  td { background: #111827; border-color: #1e293b; }
  blockquote { border-left: 4px solid #00d4aa; background: #111827; padding: 12px 20px; font-size: 0.85em; }
  .metric-row { display: flex; gap: 16px; margin-top: 20px; }
  .metric { background: #111827; border: 1px solid #1e293b; border-radius: 8px; padding: 16px 24px; text-align: center; flex: 1; }
  .metric .value { font-size: 1.8em; color: #00d4aa; font-weight: bold; }
  .metric .label { font-size: 0.7em; color: #94a3b8; margin-top: 4px; }
  .pill { display: inline-block; background: #00d4aa; color: #0a0e1a; padding: 4px 12px; border-radius: 12px; font-size: 0.7em; font-weight: bold; margin: 2px; }
  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .tech-badge { background: #1e293b; border: 1px solid #334155; padding: 4px 10px; border-radius: 6px; display: inline-block; font-size: 0.7em; margin: 2px; color: #7dd3fc; }
  .grounded { background: #111827; border: 1px solid #1e293b; border-left: 3px solid #f59e0b; border-radius: 6px; padding: 10px 16px; font-size: 0.72em; line-height: 1.5; margin-top: 8px; }
  .grounded .g-title { color: #f59e0b; font-weight: bold; font-size: 1.05em; margin-bottom: 6px; }
  .grounded .g-row { color: #cbd5e1; margin: 2px 0; }
  .grounded .g-label { color: #7dd3fc; font-weight: 600; }
  .grounded .g-val { color: #00d4aa; font-weight: 600; }
  .grounded .g-note { color: #94a3b8; font-style: italic; font-size: 0.9em; margin-top: 6px; }
  footer { font-size: 0.55em; color: #475569; }
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Agentic AI
# Use Cases Across Industries

**From Pilots to Production**

26 Real-World Deployments with Measurable Business Impact
Grounded by Domain Expert Agents with Real Code & Data

<span class="pill">Insurance</span> <span class="pill">Finance</span> <span class="pill">Supply Chain</span> <span class="pill">Manufacturing</span> <span class="pill">Healthcare</span> <span class="pill">Enterprise</span> <span class="pill">Automotive</span>

May 2026 | Domain-Agent Grounded Edition

---

# Workshop Agenda

| # | Section | Focus |
|---|---------|-------|
| 01 | AI Overview & Strategic Direction | Foundations, agent taxonomy, market positioning |
| 02 | Core Capabilities & AI Offerings | Solution portfolio, platform partnerships |
| 03 | **26 Use Cases Across 7 Industries** | Measurable business outcomes |
| 04 | Customer Pain Point Mapping | Enterprise challenges to agentic solutions |
| 05 | Success Stories & ROI Narratives | Production-validated case studies |
| 06 | Competitive Positioning | Differentiators, objection handling |
| 07 | Domain Agent Grounding | Real code, real data, real architectures |
| 08 | Implementation Roadmap | From pilot to production in 16 weeks |

> **Objective:** Improve sales readiness, strengthen positioning, enable proactive pipeline generation

---

# What Is Agentic AI?

<div class="columns">
<div>

### Traditional AI
Single prompt -> single response
- No memory between interactions
- Cannot use external tools or APIs
- Human must orchestrate each step
- Breaks on multi-step workflows

### Agentic AI
**Perceive -> Reason -> Plan -> Act -> Learn**
- Persistent memory across sessions
- Tool use: APIs, databases, enterprise systems
- Multi-agent orchestration and delegation
- Autonomous multi-step workflow execution

</div>
<div>

### From Our AI Agents Expert

<div class="grounded">
<div class="g-title">OpenHands Agent Architecture</div>
<div class="g-row"><span class="g-label">Pattern:</span> Stateless agent — all state lives in ConversationState</div>
<div class="g-row"><span class="g-label">Components:</span> LLM interface, Tool definitions, Context condenser, Agent context</div>
<div class="g-row"><span class="g-label">Step cycle:</span> Prepare messages from event history → condense context → LLM completion → dispatch actions</div>
<div class="g-note">Production architecture from OpenHands (~75K GitHub stars)</div>
</div>

</div>
</div>

---

# Agent Taxonomy -- 6 Types of Enterprise AI Agents

<div class="columns">
<div>

### Customer Agents
40-60% deflection rates. Wells Fargo, Allianz, Mercedes-Benz

### Employee Agents
2.5x capacity per employee. ServiceNow (90% IT), Cognizant (350K users)

### Code Agents
30-50% dev productivity gains. Wayfair (55% faster), Regnology

</div>
<div>

### Creative Agents
Campaigns: weeks to hours. Kraft Heinz (8wk -> 8hr)

### Data Agents
Digital twins, supply chain intelligence. BMW, Schroders

### Security Agents
Automated triage, anomaly detection. POLARIS, ServiceNow

</div>
</div>

> Source: Google Cloud -- 601 GenAI Agent Use Cases (Matt Renner, Brian Hall, 2024-2025)

---

# Core Capabilities & AI Offerings

<div class="columns">
<div>

### Solution Portfolio
- **Agentic Process Automation** -- 70-80% autonomous resolution
- **Intelligent Control Towers** -- real-time monitoring + RAG
- **Enterprise AI Agent Platforms** -- 350K+ user scale
- **AI-Powered Code Agents** -- 30-50% productivity gains
- **Clinical & Scientific AI** -- 211+ biomedical tools

### Key Differentiators

| Differentiator | Detail |
|---|---|
| Production-First | 80% use structured workflows |
| Governance-Native | Audit trails + token cost mgmt |
| Human-in-the-Loop | Confidence thresholds gate actions |
| Domain-Specific | Industry-tuned, not generic |

</div>
<div>

### Technology Partnerships

**Cloud & AI:** Google Vertex AI, AWS Bedrock, Azure OpenAI

**Orchestration:** LangChain/LangGraph, CrewAI, IBM watsonx

**Models:** Gemini, Claude, GPT-4o, Llama 3

**Enterprise:** ServiceNow, SAP, Salesforce, UiPath

### From Our AI Agents Expert

<div class="grounded">
<div class="g-title">Agent Framework Comparison</div>
<div class="g-row"><span class="g-label">LangChain</span> (~150K stars) — 700+ integrations, LangSmith observability</div>
<div class="g-row"><span class="g-label">CrewAI</span> (~44K stars) — Simple role/goal/backstory mental model</div>
<div class="g-row"><span class="g-label">OpenHands</span> (~75K stars) — Code sandbox, context condensation, MCP integration</div>
</div>

</div>
</div>

---

<!-- _class: lead -->

# 01 Insurance & Claims

Autonomous claims processing, underwriting, and fraud detection

**5 Agentic AI Use Cases**

---

# UC01 | Allianz Partners -- Autonomous Claims Execution

<div class="columns">
<div>

### Challenge
- 90M+ cases/year across health, auto, travel
- Single claim: 29 days to resolve
- Dozens of disconnected systems per lifecycle

### Agentic Solution
- Autonomous agents run full claims lifecycle
- Review, validate coverage, assess liability, settle
- Complex cases escalate; routine claims don't

### Agent Pipeline
`Intake -> Coverage -> Liability -> Settlement -> Comms`

</div>
<div>

### Results

| Metric | Impact |
|---|---|
| Claims handling | **29d -> 3.5d** |
| Settled in <12h | **70%** |
| Target annual profit | **EUR 300M** |
| Markets live | **10+** |

### Grounded: Healthcare IT Agent

<div class="grounded">
<div class="g-title">Insurance Verification via HL7v2</div>
<div class="g-row"><span class="g-label">Message type:</span> 270/271 — Eligibility request/response</div>
<div class="g-row"><span class="g-label">Avg latency:</span> <span class="g-val">2.3s</span> real-time verification</div>
<div class="g-row"><span class="g-label">Auto-verify rate:</span> <span class="g-val">94%</span> (remaining 6% require manual review)</div>
</div>

<span class="pill">Insurance</span> <span class="pill">Customer Agent</span> <span class="pill">Data Agent</span>

</div>
</div>

---

# UC02 | AIG -- Agentic Underwriting Ecosystem

<div class="columns">
<div>

### Challenge
- 370K+ excess & surplus submissions in 2025
- Sequential handoffs created bottlenecks
- No mechanism to predict conversion

### Agentic Solution
- 4 coordinated agent types in parallel
- Propensity scoring predicts conversion
- One underwriter now handles workload of five

### Pipeline
`Data Ingestion -> Risk Prioritization -> Decision Support -> Portfolio`

</div>
<div>

### Results

| Metric | Impact |
|---|---|
| Submissions processed | **370K+** |
| Faster underwriting | **2-5x** |
| Financial lines coverage | **100%** |
| Technology investment | **$1B** |

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">Fraud Detection Pipeline</div>
<div class="g-row"><span class="g-label">Throughput:</span> <span class="g-val">45,000 TPS</span></div>
<div class="g-row"><span class="g-label">Pipeline:</span> MSK/Kafka → Flink → SageMaker → DynamoDB</div>
<div class="g-row"><span class="g-label">P99 latency:</span> <span class="g-val">85ms</span></div>
<div class="g-row"><span class="g-label">Scoring:</span> Auto-block &gt;0.9 · Manual review 0.5–0.9 · Auto-approve &lt;0.5</div>
</div>

<span class="pill">Insurance</span> <span class="pill">Data Agent</span>

</div>
</div>

---

# UC03 | Clariva Group -- 5-Agent Claims Pipeline

<div class="columns">
<div>

### Challenge
- 14,000+ claims/month, all manually reviewed
- Claimants waiting days for first response

### 5-Agent Architecture
1. **Intake Agent** -- extract fields, validate policy, route
2. **Document Agent** -- analyze PDFs, photos, medical reports
3. **Fraud Agent** -- vector search against historical patterns
4. **Decision Agent** -- settle or escalate with brief
5. **Comms Agent** -- natural language customer interaction

</div>
<div>

### Results

| Metric | Impact |
|---|---|
| Claims resolved E2E | **73%** |
| Resolution time | **3.8d -> 4h** |
| To human adjusters | **27%** |
| Audit trail coverage | **100%** |

### Grounded: Healthcare IT Agent

<div class="grounded">
<div class="g-title">Hospital Workflow → Claims Severity Mapping</div>
<div class="g-row"><span class="g-label">Flow:</span> Arrival → Triage (ESI 1–5) → Registration → Insurance Verify → Admit (ADT^A01) → Orders → Results</div>
<div class="g-row"><span class="g-label">ESI 1:</span> Critical — immediate processing</div>
<div class="g-row"><span class="g-label">ESI 3:</span> Standard — within SLA</div>
<div class="g-row"><span class="g-label">ESI 5:</span> Low-touch — <span class="g-val">auto-process</span></div>
</div>

</div>
</div>

---

# UC04 | Autonomous Commercial Underwriting

<div class="columns">
<div>

### 6-Agent Pipeline + Guardian

| Agent | Role |
|---|---|
| Intake | Parse docs, extract data, validate |
| Enrichment | Company data, claims history, intel |
| Risk Assessment | Score risk, flag, route decision |
| Pricing | Calculate premium, apply rules |
| Wordings | Issue policy, generate docs |
| **Guardian** | Real-time monitoring, audit |

### Routing Logic
- **Autonomous (73%)** -- standard risks, no human touch
- **Assisted (19%)** -- minor concerns, UW review
- **Manual (8%)** -- complex risks, full human UW

</div>
<div>

### Results

| Metric | Impact |
|---|---|
| Quote turnaround | **48h -> 3.7min** |
| Submissions/day | **6x increase** |
| Decision agreement | **94.2%** |
| SME premium volume | **+47%** |

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Context Condensation Pattern</div>
<div class="g-row"><span class="g-label">Max events:</span> <span class="g-val">240</span> before condensation triggers</div>
<div class="g-row"><span class="g-label">Strategy:</span> Summarize old events → insert condensation summary → preserve first 2 events</div>
<div class="g-row"><span class="g-label">Skill precedence:</span> Project → User → Public (same pattern for claims history)</div>
<div class="g-note">Analogous to how claims agents manage growing case histories</div>
</div>

</div>
</div>

---

# UC05 | Vehicle Insurance AI Claims App

<div class="columns">
<div>

### 4 UiPath-Powered AI Agents
- **Claims Insights** -- auto-overview of history & risk
- **Fraud Investigator** -- pattern detection across data
- **Rules Agent** -- business logic, decision recommendation
- **Communication** -- policy-compliant email drafting

### Results

| Metric | Impact |
|---|---|
| ROI within 12 months | **245%** |
| Faster processing | **62%** |
| Annual cost savings | **$320K** |
| Processes automated | **72%** |

</div>
<div>

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">Streaming Architecture for Claims Telemetry</div>
<div class="g-row"><span class="g-label">Ingestion:</span> Kinesis — 8 shards, 8 MB/s write</div>
<div class="g-row"><span class="g-label">Processing:</span> Flink — 5-min tumbling windows</div>
<div class="g-row"><span class="g-label">Storage:</span> Redshift + S3 (Parquet) · <span class="g-val">sub-second queries</span></div>
<div class="g-row"><span class="g-label">Freshness SLA:</span> <span class="g-val">&lt; 5 minutes</span> end-to-end</div>
<div class="g-row" style="margin-top:6px"><span class="g-label">Monthly cost:</span> Redshift $2,345 · Kinesis $86 · Glue $198 · <span class="g-val">Total $4,050/mo</span> ($0.027/M records)</div>
</div>

<span class="pill">Insurance</span> <span class="pill">Employee Agent</span> <span class="pill">Data Agent</span>

</div>
</div>

---

<!-- _class: lead -->

# 02 Financial Services

Agentic banking, research, ERP automation, and business intelligence

**4 Agentic AI Use Cases**

---

# UC06 | Wells Fargo -- Agentic AI at Enterprise Scale

<div class="columns">
<div>

### Challenge
- Complex FX post-trade inquiries across systems
- Customer service limited to business hours
- Need real-time market insights during interactions

### Solution
- AI agents triage, answer, summarize FX inquiries
- Multimodal enterprise search across policies
- 24/7 hyper-personalized customer experiences

### Results

| Metric | Impact |
|---|---|
| Employees empowered | **30K+** |
| Customer service | **24/7** |
| Market insights | **Real-time** |
| Channels | **Multichannel** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Enterprise Customer Support — Production Maturity</div>
<div class="g-row"><span class="g-label">Status:</span> <span class="g-val">Production</span></div>
<div class="g-row"><span class="g-label">Live examples:</span> Klarna (2.3M conversations), Intercom Fin, Zendesk AI agents</div>
<div class="g-row"><span class="g-label">ROI:</span> <span class="g-val">67%</span> resolution without human</div>
<div class="g-row"><span class="g-label">Recommended stack:</span> LangChain — 700+ integrations, LangSmith observability ($39/seat/mo)</div>
</div>

**Platform:** Google Agentspace + NotebookLM

<span class="pill">Financial Services</span> <span class="pill">Customer Agent</span>

</div>
</div>

---

# UC07 | Schroders -- Multi-Agent Financial Research

<div class="columns">
<div>

### Challenge
- Equity research taking analysts days to complete
- Dependencies between deterministic + non-deterministic tasks

### Solution
- Parent-child graph structure with LangGraph
- Porter's 5 Forces Agent triggers children in parallel
- Complete company analysis in minutes, not days

### Results

| Metric | Impact |
|---|---|
| Company analysis | **Days -> Minutes** |
| Porter's analysis | **Fully automated** |
| Agent configs | **Versioned in Firestore** |
| Architecture | **Modular workflows** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Financial Research Agent Architecture</div>
<div class="g-row"><span class="g-label">Framework:</span> LangChain — Chain/Agent/Tool abstractions, LCEL</div>
<div class="g-row"><span class="g-label">Ecosystem:</span> 700+ integrations, LangSmith observability ($39/seat)</div>
<div class="g-row"><span class="g-label">Delegation:</span> Parent-child agent definitions — each agent carries name, tools, skills, and domain-specific system prompt</div>
<div class="g-note">Porter's 5 Forces agent triggers child analysts in parallel, same pattern as OpenHands subagent delegation</div>
</div>

**Stack:** Vertex AI + LangGraph + Firestore + AutoSxS

</div>
</div>

---

# UC08 | FinRobot -- Agentic ERP for Financial Workflows

<div class="columns">
<div>

### Challenge
- Wire transfers: SWIFT, AML/KYC compliance
- Traditional workflow engines are brittle
- End-to-end time measured in days

### Solution (GBPAs)
- Agents interpret intent, synthesize workflows in real time
- Chain-of-Actions (CoA) engine for dynamic execution
- 5W3H1R schema for structured process modeling

### Results

| Metric | Impact |
|---|---|
| Processing time | **-40%** |
| Error rate | **-94%** |
| Reimbursement time | **-82%** |
| Workflow synthesis | **Real-time** |

</div>
<div>

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">AWS Pricing for Financial Workloads (us-east-1)</div>
<div class="g-row"><span class="g-label">Kinesis:</span> $0.015/shard-hour · $0.014/1M payload units</div>
<div class="g-row"><span class="g-label">Redshift:</span> $1.086/hr/node (RA3) · $0.375/RPU-hour (Serverless)</div>
<div class="g-row"><span class="g-label">Glue ETL:</span> $0.44/DPU-hour</div>
<div class="g-row"><span class="g-label">MSK Kafka:</span> $0.0012/partition-hour (Serverless)</div>
<div class="g-row" style="margin-top:6px"><span class="g-label">Total platform:</span> <span class="g-val">~$4,050/mo</span> · $0.027 per million records</div>
</div>

</div>
</div>

---

# UC09 | OPLOG -- AI Agents for Business Intelligence

<div class="columns">
<div>

### 3 Independent AI Agents
- **Deal Analyzer** -- validates required HubSpot fields
- **Sales Coach** -- enforces data quality on stage changes
- **Lead Insight** -- scans 6 platforms per new lead

### Results

| Metric | Impact |
|---|---|
| Sales cycle | **-35%** |
| CRM data completeness | **91%** |
| Research time | **-98%** |
| Teams delivery success | **99.5%** |

</div>
<div>

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">CAC/LTV Channel Benchmarks</div>
<div class="g-row"><span class="g-label">Organic search:</span> CAC $28 · LTV $420 · Ratio <span class="g-val">15:1</span> → Scale</div>
<div class="g-row"><span class="g-label">Content marketing:</span> CAC $35 · LTV $380 · Ratio <span class="g-val">10.9:1</span> → Scale</div>
<div class="g-row"><span class="g-label">Paid search:</span> CAC $45 · LTV $180 · Ratio 4:1 → Optimize</div>
<div class="g-row"><span class="g-label">Social ads:</span> CAC $62 · LTV $95 · Ratio 1.5:1 → Cut 60%</div>
<div class="g-row"><span class="g-label">Display ads:</span> CAC $85 · LTV $120 · Ratio 1.4:1 → Pause</div>
<div class="g-note">Minimum viable ratio: 3:1 (below = unprofitable after overhead)</div>
</div>

**Stack:** Amazon Bedrock AgentCore + Claude Sonnet + HubSpot

</div>
</div>

---

<!-- _class: lead -->

# 03 Supply Chain & Logistics

Autonomous exception handling, email automation, and control towers

**4 Agentic AI Use Cases**

---

# UC10 | Singapore 3PL -- Autonomous Supply Chain Control Tower

<div class="columns">
<div>

### Challenge
- $2.8B annual freight, 42,000 active shipments
- Exception resolution: 4.7 hours per incident
- 45-person team handling exceptions manually
- 91.4% on-time delivery vs. >98% expected

### 3-Agent Pipeline
1. **Detection** -- correlate AIS vessel + carrier data
2. **Root Cause** -- RAG over 48,000 resolved exceptions
3. **Action Execution** -- auto-resolve when confidence >0.85

</div>
<div>

### Results

| Metric | Impact |
|---|---|
| Autonomous resolution | **73%** |
| Resolution time | **4.7h -> 22min** |
| Exception cost | **S$6.2M -> S$1.8M** |
| On-time delivery | **91.4% -> 99.2%** |

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">Control Tower Streaming + Data Quality</div>
<div class="g-row"><span class="g-label">Ingestion:</span> Kinesis — 8 shards, 8 MB/s write</div>
<div class="g-row"><span class="g-label">Processing:</span> Flink — windowed aggregation</div>
<div class="g-row"><span class="g-label">Freshness SLA:</span> <span class="g-val">&lt; 5 minutes</span> end-to-end</div>
<div class="g-row" style="margin-top:6px"><span class="g-label">Data quality:</span> Schema validation <span class="g-val">99.2%</span> · Completeness 99.7% · Accuracy 98.9% · Timeliness 96%</div>
</div>

</div>
</div>

---

# UC11 | C.H. Robinson -- Logistics Email Automation

<div class="columns">
<div>

### Challenge
- 15,000 shipping emails/day, inconsistent formatting
- Handwritten notes on PDFs, missing fields
- 4-hour queue wait, 7 min per email manually

### Solution
- LangGraph state management for LTL/FTL classification
- LangSmith traces for error quantification
- Meta-prompting optimizes user input formats

### Results

| Metric | Impact |
|---|---|
| Orders automated/day | **5,500** |
| Hours saved daily | **600** |
| Email queue time | **4h -> minutes** |
| Annual shipments | **37M** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">LangChain for Logistics Automation</div>
<div class="g-row"><span class="g-label">Architecture:</span> Chain/Agent/Tool abstractions with LCEL</div>
<div class="g-row"><span class="g-label">Strengths:</span> Largest ecosystem, 700+ integrations, LangSmith observability</div>
<div class="g-row"><span class="g-label">Trade-offs:</span> Abstraction overhead, breaking API changes in earlier versions</div>
<div class="g-row"><span class="g-label">Enterprise:</span> LangSmith at $39/seat/mo</div>
<div class="g-note">LangSmith traces stitch across the full order entry process for SME review</div>
</div>

**Stack:** LangChain + LangGraph + LangSmith

</div>
</div>

---

# UC12 | European 3PL -- Autonomous Logistics Support

<div class="columns">
<div>

### Challenge
- 1,200+ support tickets/day
- 60% escalation rate to specialists
- $3.2M annual support cost (50 FTEs)

### Composite AI Across 5 Systems
WMS + TMS + CRM + Accounting + Compliance

### 4-Phase Build
`Data Integration -> Predictive -> Agentic -> Rules`

</div>
<div>

### Results

| Metric | Impact |
|---|---|
| Autonomous resolution | **99.2%** |
| Resolution time | **2-4h -> 94 sec** |
| Annual cost savings | **$980K** |
| NPS improvement | **52 -> 78** |

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">Data Quality for Logistics Operations</div>
<div class="g-row"><span class="g-label">Monte Carlo:</span> Automated lineage + schema change alerts · MTTR <span class="g-val">23 min</span></div>
<div class="g-row"><span class="g-label">Integrations:</span> dbt, Airflow, Redshift, Snowflake, BigQuery</div>
<div class="g-row"><span class="g-label">Great Expectations:</span> Null rate 0.3% · Freshness 4 rules/week · Uniqueness <span class="g-val">99.99%</span></div>
</div>

</div>
</div>

---

# UC13 | UNACEM -- Industrial Logistics Agent

<div class="columns">
<div>

### Challenge
- Logistics bottleneck at cement plant gates
- 5 countries, 40+ subsidiaries
- Manual coordination across cement, aggregates, concrete

### Solution
- Logistics agent via **WhatsApp**
- IBM watsonx Orchestrate for multi-step work
- Same blueprint extends to IT, procurement, safety

### Results

| Metric | Impact |
|---|---|
| Driver wait time | **-40%** |
| Countries covered | **5** |
| Subsidiaries | **40+** |
| Next phase | **IT, procurement, safety** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Multi-Agent Delegation Pattern</div>
<div class="g-row"><span class="g-label">Agent definition:</span> Each agent carries name, description, model, tools, skills, and system prompt</div>
<div class="g-row"><span class="g-label">Tools:</span> Terminal, web search (extensible via MCP for WhatsApp)</div>
<div class="g-row"><span class="g-label">Skills:</span> BPMN, cloud, domain-specific capabilities</div>
<div class="g-row"><span class="g-label">Precedence:</span> Project → User → Public skill directories</div>
<div class="g-note">Same OpenHands AgentDefinition pattern powers UNACEM's logistics dispatcher</div>
</div>

**Platform:** IBM watsonx Orchestrate

</div>
</div>

---

<!-- _class: lead -->

# 04 Manufacturing

Root cause analysis, quality prediction, and digital twin agents

**3 Agentic AI Use Cases**

---

# UC14 | Apollo Tyres -- Manufacturing Reasoner

<div class="columns">
<div>

### Challenge
- RCA for curing press downtime: up to 7 hours
- 250+ automated presses across 3 plants
- 140+ SKUs, 3 curing mediums, 2 supplier types

### Solution
- Amazon Bedrock Agents with multi-agentic RAG
- Complex Transformation Engine + RCA Agent
- Natural language queries on streaming IoT data

### Results

| Metric | Impact |
|---|---|
| RCA effort reduction | **88%** |
| RCA time | **7h -> 10min** |
| Annual savings | **INR 15M** |
| Presses monitored | **250+** |

</div>
<div>

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">AWS Pricing for Manufacturing IoT Pipeline</div>
<div class="g-row"><span class="g-label">Kinesis:</span> $0.015/shard-hour · Extended retention $0.014/shard-hr (up to 365 days)</div>
<div class="g-row"><span class="g-label">Redshift:</span> $1.086/hr/node (RA3) · Spectrum $5.00/TB scanned</div>
<div class="g-row"><span class="g-label">Flink Managed:</span> $0.11/KPU-hour · Storage $0.10/GB/mo</div>
<div class="g-row"><span class="g-label">S3:</span> Standard $0.023/GB/mo · Glacier Instant $0.004/GB/mo</div>
</div>

**Stack:** Amazon Bedrock + IoT + Redshift

</div>
</div>

---

# UC15 | HCLTech Insight -- Quality AI Agent

<div class="columns">
<div>

### Challenge
- Defects across complex production lines
- Need real-time quality monitoring at scale
- Multiple data sources and manufacturing systems

### Solution
- Predict and eliminate different defect types
- Vertex AI + Google Cloud Cortex Framework
- Manufacturing Data Engine for unified data

### Results

| Metric | Impact |
|---|---|
| Defect prediction | **Real-time** |
| Defect coverage | **Multi-type** |
| Quality monitoring | **Automated** |
| Framework | **Cortex integration** |

</div>
<div>

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">Data Quality for Manufacturing Monitoring</div>
<div class="g-row"><span class="g-label">Schema validation:</span> <span class="g-val">99.2%</span> pass rate</div>
<div class="g-row"><span class="g-label">Null rate:</span> 0.3% across critical columns</div>
<div class="g-row"><span class="g-label">5 DQ dimensions:</span> Completeness 99.7% · Accuracy 98.9% · Consistency 99.4% · Timeliness 96% · Uniqueness 99.99%</div>
<div class="g-note">Same quality framework detects sensor anomalies = quality drift in production lines</div>
</div>

**Stack:** Vertex AI + Cortex Framework

</div>
</div>

---

# UC16 | BMW Group -- Digital Twin Supply Chain Agents

<div class="columns">
<div>

### Challenge
- Complex industrial planning and supply chains
- Physical asset scanning at scale
- Thousands of distribution simulations needed

### Solution
- AI agents create 3D digital twins from scans
- Autonomous distribution simulations
- Optimize supply chain based on results

### Results

| Metric | Impact |
|---|---|
| Simulations | **1000s autonomous** |
| Model generation | **3D digital twin** |
| Distribution | **Optimized** |
| Planning | **Real-time adjustments** |

</div>
<div>

### Grounded: Data Platform Agent

<div class="grounded">
<div class="g-title">Simulation Infrastructure Cost Benchmark</div>
<div class="g-row"><span class="g-label">Redshift RA3:</span> 3 nodes · $2,345/mo (58% of total)</div>
<div class="g-row"><span class="g-label">S3 Storage:</span> 12 TB · $276/mo</div>
<div class="g-row"><span class="g-label">MSK Kafka:</span> 3 brokers · $423/mo</div>
<div class="g-row"><span class="g-label">Total platform:</span> <span class="g-val">$4,050/mo</span> · $0.027 per million records</div>
<div class="g-note">Digital twin data pipeline follows same streaming pattern as analytics workloads</div>
</div>

**Stack:** Vertex AI + SORDI.ai + Monkeyway

</div>
</div>

---

<!-- _class: lead -->

# 05 Healthcare & Life Sciences

Clinical reasoning, precision therapeutics, and drug discovery automation

**3 Agentic AI Use Cases**

---

# UC17 | Autonomous Cognitive Concern Detection

<div class="columns">
<div>

### Challenge
- Early detection of cognitive impairment limited
- Expert-driven prompt refinement is costly
- Prevalence shift impacts generalizability

### 5-Agent Clinical System
- **Specialist Agent** -- 256 tokens, deterministic
- **Optimization Agents** -- 512 tokens each
- Iterative self-refinement: max 5 cycles
- Zero human input after deployment

### Results

| Metric | Impact |
|---|---|
| Validation F1 | **0.74** |
| Refinement F1 | **0.93** |
| Human input | **Zero** |
| False negatives | **44% clinically appropriate** |

</div>
<div>

### Grounded: Healthcare IT Agent

<div class="grounded">
<div class="g-title">HL7v2 → FHIR Clinical Data Mapping</div>
<div class="g-row"><span class="g-label">PID → Patient:</span> Patient.identifier (demographics)</div>
<div class="g-row"><span class="g-label">PV1 → Encounter:</span> Encounter.class (visit type)</div>
<div class="g-row"><span class="g-label">OBX → Observation:</span> Observation.value — cognitive screening scores</div>
<div class="g-row"><span class="g-label">DG1 → Condition:</span> Condition.code (ICD-10) — dementia diagnosis codes</div>
<div class="g-row"><span class="g-label">Throughput:</span> Mirth Connect <span class="g-val">10K+ msg/min</span> per channel — supports real-time clinical feeds</div>
</div>

**Model:** Llama 3.1 8B (5 specialized agents)

</div>
</div>

---

# UC18 | TXAGENT -- Precision Therapeutics Agent

<div class="columns">
<div>

### Challenge
- Clinicians must reason across drugs, genes, diseases
- Static knowledge bases become outdated
- Complex multi-step reasoning required

### TOOLUNIVERSE: 211 Biomedical Tools
- **TOOLRAG** -- adaptive tool retrieval model
- **TOOLGEN** -- multi-agent tool generator from API docs
- **TRACEGEN** -- reasoning trace generator
- Training: **85,340 multi-step samples**

### Results

| Metric | Impact |
|---|---|
| Biomedical tools | **211** |
| Reasoning | **Multi-step** |
| Knowledge | **Real-time retrieval** |
| Traceability | **Full evidence chain** |

</div>
<div>

### Grounded: Healthcare IT Agent

<div class="grounded">
<div class="g-title">Mirth Connect — Clinical Data Routing</div>
<div class="g-row"><span class="g-label">ORU^R01:</span> Lab results → routed to drug interaction check agent</div>
<div class="g-row"><span class="g-label">ORM^O01:</span> New orders → routed to contraindication agent</div>
<div class="g-row" style="margin-top:6px"><span class="g-label">Epic:</span> <span class="g-val">2.5M+</span> daily transactions</div>
<div class="g-row"><span class="g-label">FHIR endpoints:</span> <span class="g-val">2,800+</span></div>
<div class="g-row"><span class="g-label">Auto-verify rate:</span> <span class="g-val">94%</span></div>
<div class="g-note">Content-based router pattern maps directly to therapeutic reasoning agent dispatch</div>
</div>

</div>
</div>

---

# UC19 | Tippy -- Drug Discovery DMTA Automation

<div class="columns">
<div>

### 5+1 Agent Architecture

| Agent | DMTA Phase |
|---|---|
| Supervisor | Orchestrates all agents |
| Molecule | Design (computational chemistry) |
| Lab | Make/Test (HPLC, synthesis) |
| Analysis | Analyze (data processing, stats) |
| Report | Documentation & communication |
| **Safety Guardrail** | Oversight across all operations |

### Results

| Metric | Impact |
|---|---|
| Agents | **5 + Safety Guardrail** |
| Cycle coverage | **Full DMTA** |
| Production status | **First production-ready** |
| Integration | **LIMS + ELN + HPLC** |

</div>
<div>

### Grounded: Healthcare IT Agent

<div class="grounded">
<div class="g-title">Integration Metrics — HL7 Interop for LIMS/ELN</div>
<div class="g-row"><span class="g-label">Epic Systems:</span> <span class="g-val">38%</span> of US hospital beds · 2,800+ FHIR endpoints · 99.95% uptime</div>
<div class="g-row"><span class="g-label">Mirth Connect 4.6:</span> MLLP/HTTPS/SFTP · <span class="g-val">10K+ msg/min</span> · Docker or bare metal</div>
<div class="g-row"><span class="g-label">Parse error rate:</span> 0.3% · Insurance verify latency: 2.3s avg</div>
<div class="g-note">Same HL7 interoperability patterns apply to LIMS/ELN integration in drug discovery</div>
</div>

**Stack:** Artificial lab orchestration

</div>
</div>

---

<!-- _class: lead -->

# 06 Enterprise Operations

Workforce transformation, multi-agent platforms, and research intelligence

**3 Agentic AI Use Cases**

---

# UC20 | ServiceNow -- Workforce Transformation

<div class="columns">
<div>

### Challenge
- Finance queries: 4 days average resolution
- Workforce grew 14K -> 30K without ops growth
- Agent proliferation creating cost spirals

### Solution
- Redesigned processes around AI agents
- Agent Command Center for governance
- 85% of IT staff redeployed to higher value

### Results

| Metric | Impact |
|---|---|
| Finance resolution | **4d -> 8s** |
| IT tickets autonomous | **90%** |
| HR capacity | **2.5x per partner** |
| IT staff redeployed | **85%** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Enterprise Use Case Maturity</div>
<div class="g-row"><span class="g-label">Customer support:</span> <span class="g-val">Production</span> — 67% resolution without human</div>
<div class="g-row"><span class="g-label">Code review:</span> <span class="g-val">Production</span> — 4.2 hrs saved/dev/week</div>
<div class="g-row"><span class="g-label">Data analysis:</span> Pilot — 50–70% query time reduction</div>
<div class="g-row"><span class="g-label">Process automation:</span> Research → but ServiceNow proves production-scale</div>
<div class="g-note">ServiceNow revenue: $3.77B Q1 2026 (+22% YoY) — process automation has arrived</div>
</div>

</div>
</div>

---

# UC21 | Cognizant -- Multi-Agent Platform for 350K

<div class="columns">
<div>

### Challenge
- Employees toggling between multiple portals
- AI tools adopted in silos, increasing complexity

### Solution: OneCognizant (1C)
- Single AI-powered digital front door
- **Neuro-san** multi-agent accelerator
- Client Zero: proven internally first

### Results

| Metric | Impact |
|---|---|
| Users worldwide | **350K** |
| Enterprise apps unified | **100s** |
| Interface | **Single digital front door** |
| Validation | **Client Zero model** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Enterprise Multi-Agent Platforms</div>
<div class="g-row"><span class="g-label">AutoGen</span> (~45K stars) — Multi-agent conversation, group chat · Microsoft/Azure backing</div>
<div class="g-row"><span class="g-label">GitHub Copilot:</span> $39/user/mo · <span class="g-val">42% market share</span> · GPT-4o + fine-tunes</div>
<div class="g-note">350K users at Cognizant = enterprise-scale proof of multi-agent platforms</div>
</div>

</div>
</div>

---

# UC22 | Madrigal Pharma -- Multi-Agent Research Platform

<div class="columns">
<div>

### Challenge
- Disconnected data sources across pharma research
- Prototype-to-production gap measured in months

### Modular Skill Architecture
- Orchestrator loads the right skill per query
- Data normalized via consistent tool interface
- Production failures feed back as test cases

### Results

| Metric | Impact |
|---|---|
| Prototype to prod | **Weeks** |
| Architecture | **Modular skills** |
| Data sources | **Unified** |
| Scalability | **New skill = new use case** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Modular Skill Architecture (OpenHands Pattern)</div>
<div class="g-row"><span class="g-label">Skill precedence:</span> Project (.agents/skills) → User (~/.agents/skills) → Public</div>
<div class="g-row"><span class="g-label">Agent definition:</span> Name, description, model, tools, skills, system prompt</div>
<div class="g-row"><span class="g-label">Key insight:</span> New skill = new use case, no core changes needed</div>
<div class="g-note">Same modular pattern Madrigal uses — orchestrator loads the right skill per query</div>
</div>

**Stack:** LangChain DeepAgents + LangSmith Deploy

</div>
</div>

---

<!-- _class: lead -->

# 07 Automotive & Technology

In-vehicle agents, developer productivity, and code automation

**4 Agentic AI Use Cases**

---

# UC23-24 | Mercedes-Benz & Volkswagen -- Automotive AI

<div class="columns">
<div>

### Mercedes-Benz -- CLA Series
- Conversational search & navigation
- Google Cloud Automotive AI Agent
- Smart sales assistant for e-commerce
- AI call centers with personalized campaigns

### Volkswagen -- myVW Assistant
- Gemini multimodal: voice + camera
- Point camera at dashboard indicator lights
- Owner's manual as grounded knowledge base
- Vehicle-specific context awareness

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Automotive Customer Agents — Production Tier</div>
<div class="g-row"><span class="g-label">Maturity:</span> <span class="g-val">Production</span> — Mercedes & VW join Klarna (2.3M), Intercom Fin, Zendesk</div>
<div class="g-row"><span class="g-label">ROI benchmark:</span> <span class="g-val">67%</span> resolution without human</div>
<div class="g-row"><span class="g-label">Claude Agent SDK:</span> Native integration, simple API, strong reasoning · $15/$75 per 1M tokens</div>
</div>

**Both:** <span class="pill">Automotive</span> <span class="pill">Customer Agent</span>

</div>
</div>

---

# UC25 | Wayfair -- Code Agents for Developer Productivity

<div class="columns">
<div>

### Challenge
- Dev environment setup was time-consuming
- Unit testing quality varied across teams
- Product catalog enrichment was slow

### Solution
- Gemini Code Assist customized on private codebase
- Dual use: developer productivity + product ops

### Results

| Metric | Impact |
|---|---|
| Environment setup | **55% faster** |
| Code performance | **48% improvement** |
| Product attribute speed | **5x faster** |
| Dev satisfaction | **60% more satisfying** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Code Review Tool Comparison</div>
<div class="g-row"><span class="g-label">CodeRabbit:</span> $24/user/mo · <span class="g-val">#1 SWE-bench</span> · 43% more issues than Copilot · ~15% false positive</div>
<div class="g-row"><span class="g-label">GitHub Copilot:</span> $39/user/mo · <span class="g-val">42% market share</span> · Good style, weaker on architecture</div>
<div class="g-row"><span class="g-label">Sourcery:</span> $30/user/mo · Python-first</div>
<div class="g-row"><span class="g-label">Codacy:</span> $15/user/mo · Static analysis + coverage</div>
</div>

</div>
</div>

---

# UC26 | Regnology -- Ticket-to-Code AI Agent

<div class="columns">
<div>

### Challenge
- Bug tickets require manual analysis
- RegTech requires high accuracy + compliance
- Bottleneck at ticket triage and implementation

### Solution
- Gemini 1.5 Pro with long context
- Automatically converts tickets to code fixes
- Understands regulatory context

### Pipeline
`Ingest Ticket -> Analyze Codebase -> Generate Fix -> Human Review`

### Results

| Metric | Impact |
|---|---|
| Conversion | **Auto bug-to-code** |
| Model | **Gemini 1.5 Pro** |
| Process | **Streamlined** |
| Domain | **Compliance-aware** |

</div>
<div>

### Grounded: AI Agents Expert

<div class="grounded">
<div class="g-title">Code Agent Maturity — Production</div>
<div class="g-row"><span class="g-label">Production tools:</span> CodeRabbit, GitHub Copilot, Sourcery, Amazon CodeGuru</div>
<div class="g-row"><span class="g-label">ROI:</span> <span class="g-val">4.2 hrs saved/dev/week</span> (GitHub survey)</div>
<div class="g-row"><span class="g-label">OpenHands</span> (~75K stars) — CodeActAgent + Event Stream, code sandbox, browser automation, MCP integration</div>
<div class="g-note">Same CodeActAgent pattern powers Regnology's ticket-to-code pipeline</div>
</div>

</div>
</div>

---

# Customer Pain Point Mapping

| Pain Point | Agentic Solution | Key Metric | Use Cases |
|---|---|---|---|
| "We process thousands of documents manually" | Agentic Document Processing | 73% autonomous | UC01, UC03, UC04 |
| "Our support team can't scale" | Autonomous Customer Service | 99.2% resolution | UC12, UC20, UC06 |
| "Root cause analysis takes days" | Manufacturing Reasoner Agents | 88% effort reduction | UC14, UC15, UC16 |
| "Supply chain exceptions are killing us" | Autonomous Control Tower | 73% auto-resolved | UC10, UC11, UC12 |
| "Underwriting is too slow" | Autonomous Underwriting Pipeline | 48h -> 3.7min | UC02, UC04, UC05 |
| "Developers waste time on repetitive tasks" | Code & SDLC Agents | 55% faster setup | UC25, UC26 |
| "Clinical workflows don't scale" | Clinical Reasoning Agents | 211-tool reasoning | UC17, UC18, UC19 |
| "Can't get insights fast enough" | Multi-Agent Research & BI | 98% time reduction | UC07, UC09, UC22 |

---

# Success Stories & ROI Narratives

| Payback Period | Category | Proof Points |
|---|---|---|
| **3 Months** | Document-Intensive Back-Office | Allianz: 29d->3.5d, Clariva: 73% auto, AIG: 370K |
| **4-5 Months** | Software Development Lifecycle | Wayfair: 55% faster, Regnology: auto bug-to-code |
| **5-6 Months** | Customer Service Tier-1 | ServiceNow: 90% auto, European 3PL: 99.2% |
| **6 Months** | IT Operations & Monitoring | ServiceNow: 4d->8s, Apollo: 7h->10min |

### Market Headlines

| Metric | Value |
|---|---|
| Agentic AI market by 2030 | **$47.1B** (Gartner) |
| Enterprises in production | **60%** |
| Highest documented ROI | **245%** (vehicle claims) |
| Largest profit target | **EUR 300M** (Allianz Partners) |

---

# Competitive Positioning

<div class="columns">
<div>

### Why Agentic AI, Not Traditional
- RPA breaks on format changes; **agents reason**
- Chatbots wait for prompts; **agents act proactively**
- Rule engines need reprogramming; **agents adapt**
- Single-model AI gives one answer; **multi-agent pipelines verify**
- Traditional scales linearly; **agents decouple headcount**

### Common Objections

| Objection | Response |
|---|---|
| "AI will replace workforce" | ServiceNow redeployed 85% to higher value |
| "Not accurate enough" | 94.2% agreement with human underwriters |
| "Can't explain to regulators" | POLARIS: audit trails + policy guardrails |
| "Our data is too messy" | C.H. Robinson: 15K emails/day, handwritten PDFs |
| "ROI is uncertain" | 3-month payback, documented |

</div>
<div>

### Grounded: Production Insights

<div class="grounded">
<div class="g-title">Production Reality (arxiv 2512.04123)</div>
<div class="g-row"><span class="g-label">Structured workflows:</span> <span class="g-val">80%</span> — NOT fully autonomous</div>
<div class="g-row"><span class="g-label">Custom over frameworks:</span> <span class="g-val">85%</span> — for production stability</div>
<div class="g-row"><span class="g-label">Framework in pilot only:</span> 61% migrate away for production</div>
<div class="g-row" style="margin-top:6px"><span class="g-label">vs. RPA:</span> Agents reason; RPA scripts</div>
<div class="g-row"><span class="g-label">vs. Chatbots:</span> Agents act E2E; chat only answers</div>
<div class="g-row"><span class="g-label">vs. BPO:</span> $28/resolution vs $320</div>
</div>

</div>
</div>

---

# Domain Agent Grounding -- What Makes This Deck Different

<div class="columns">
<div>

### 3 Domain Expert Agents with Real Code

**Healthcare IT Expert**
- HL7v2 message types (ADT, ORM, ORU, DFT)
- FHIR R4 resource mapping (Python)
- Mirth Connect 4.6 content-based router (JS)
- Epic/Cerner market share, throughput data

**Data Platform Expert**
- AWS pricing dictionaries (current us-east-1)
- Streaming architecture patterns (Kafka/Flink)
- CAC/LTV marketing benchmarks
- Data quality framework (Great Expectations)

**AI Agents Expert**
- Framework comparison (LangChain, CrewAI, OpenHands)
- OpenHands class hierarchy (actual Python)
- Code review tool pricing & F1 scores
- Enterprise use case maturity levels

</div>
<div>

### Agent Architecture (OpenHands Format)

<div class="grounded">
<div class="g-title">3 Domain Agents in .agents/agents/</div>
<div class="g-row"><span class="g-label">healthcare-it-expert:</span> Tools: terminal, web_search · Skills: archimate, bpmn, uml</div>
<div class="g-row" style="padding-left:12px">Carries HL7v2 message types, FHIR R4 mapping, Mirth Connect router as context</div>
<div class="g-row"><span class="g-label">data-platform-expert:</span> Tools: terminal, web_search · Skills: data-analytics, cloud, vega</div>
<div class="g-row" style="padding-left:12px">Carries AWS pricing dicts, streaming patterns, CAC/LTV benchmarks as context</div>
<div class="g-row"><span class="g-label">ai-agents-expert:</span> Tools: terminal, web_search · Skills: mindmap, canvas, graphviz</div>
<div class="g-row" style="padding-left:12px">Carries framework comparison, OpenHands classes, code review tool data as context</div>
<div class="g-note">System prompt = markdown body with actual code — that's context engineering</div>
</div>

</div>
</div>

---

# Implementation Roadmap -- From Pilot to Production

<div class="columns">
<div>

### Phase 1: Discovery (Weeks 1-4)
- Identify high-volume, rule-governed processes
- Map workflows and decision points
- Define agent scope, guardrails, escalation triggers
- Establish success metrics and baselines

### Phase 2: Build (Weeks 5-12)
- Design multi-agent architecture
- Build tool integrations (ERP, CRM, TMS, WMS)
- Implement governance: audit trails, policy guardrails
- Deploy human-in-the-loop gates
- Shadow mode: run parallel with human workers

</div>
<div>

### Phase 3: Validate (Weeks 13-16)
- Compare agent vs. human decisions on live data
- Tune confidence thresholds (auto vs. escalated)
- Regulatory review of explainability
- Stress test with edge cases
- Train ops teams on agent monitoring

### Phase 4: Scale (Weeks 17+)
- Go live at 40% volume
- Expand to full volume over 4 weeks
- Deploy Agent Command Center for governance
- Extend to adjacent use cases
- Continuous improvement: failures -> training

</div>
</div>

---

<!-- _class: lead -->

# Key Takeaways

**26 Use Cases** | **8 Industries** | **$47.1B Market** | **3-6 mo Payback**

- Agentic AI is **production-ready**: 60% of enterprises have agents live
- **80% use structured workflows**, not fully autonomous planning
- **Multi-agent > single agent**: orchestrated specialists win
- **Governance is the differentiator**: audit trails, not just accuracy
- **Domain grounding is the edge**: real code, real data, real architectures

> This deck is grounded by 3 domain expert agents carrying actual code --
> not descriptions. That's the context engineering difference.
