# Domain Agent Prompt Library

Quick-reference prompts for the 3 domain expert agents. Each prompt is ready to use — copy, paste, get grounded answers.

**How to use:** Prefix any prompt with:
```
Read ~/.agents/agents/{agent-name}.md as your domain context.
```

---

## Healthcare IT Expert

### HL7v2 Messaging

```
"List all 9 HL7v2 message types you know with their triggers and 
production use cases. Include which ones drive billing vs clinical flow."
```

```
"A 400-bed hospital is sending us ADT messages. How many should we 
expect per day? What's the parse error rate and how do we handle 
malformed segments?"
```

```
"Walk me through what happens when a patient is admitted: which HL7v2 
messages fire in sequence from arrival to discharge?"
```

```
"What's the difference between ADT^A01 (admit), ADT^A03 (discharge), 
and ADT^A08 (update)? When does each trigger downstream actions?"
```

### FHIR R4 Mapping

```
"Map all 7 HL7v2 segments to their FHIR R4 resources. Include the 
specific field-level mappings (e.g., PID-3 → Patient.identifier)."
```

```
"We need to transform OBX segments into FHIR Observations for a 
cognitive screening system. What fields map where, and what's the 
Mirth Connect throughput for real-time feeds?"
```

```
"Design a Mirth Connect channel that routes HL7v2 messages by type: 
ADT to one channel, orders to another, results to a third. Include 
the content-based router pattern."
```

### Epic & Cerner

```
"Compare Epic vs Cerner/Oracle Health: market share, FHIR endpoints, 
daily transaction volume, and uptime SLA. Which is better for a 
large health system integration?"
```

```
"A client is migrating from Cerner to Epic. What do we need to know 
about the integration differences? Include the $16B VA contract context."
```

```
"What are Epic's real production numbers? FHIR endpoints, daily 
transactions, and uptime SLA."
```

### Insurance & Eligibility

```
"How does real-time insurance eligibility verification work via 270/271 
messages? What's the latency and auto-verify rate?"
```

```
"A claims processing system needs to verify insurance before admission. 
Walk through the 270/271 flow with real latency numbers and the 
6% manual review fallback."
```

### Hospital Workflow

```
"Describe the full patient intake workflow from arrival to results. 
Include ESI triage levels with percentage distributions."
```

```
"Map ESI severity levels to automated processing tiers for a claims 
system. Which levels can be auto-processed vs need human review?"
```

```
"We're building an AI triage agent. What are the 5 ESI levels, their 
time targets, and volume distributions in a typical ED?"
```

---

## Data Platform Expert

### AWS Pricing

```
"Price out a streaming analytics platform on AWS: Kinesis, Redshift, 
Glue, MSK, Flink, and S3. Give per-unit costs in us-east-1."
```

```
"Compare Kinesis Data Streams vs MSK Kafka Serverless for a high-TPS 
workload. Include per-shard vs per-partition pricing."
```

```
"What does Redshift cost? Compare ra3.xlplus, ra3.4xlarge, serverless, 
and Spectrum. When should we use each?"
```

```
"A client wants to store 12TB of data with tiered access. Compare S3 
Standard vs Glacier Instant Retrieval pricing."
```

```
"Price out a Glue ETL pipeline: 450 DPU-hours/month of ETL, plus 
catalog and crawler costs. What's the total?"
```

### Fraud Detection Pipeline

```
"Design a real-time fraud detection pipeline handling 45K TPS. 
Include the full architecture, P99 latency target, and scoring 
thresholds for auto-block vs manual review vs auto-approve."
```

```
"What sensitivity and false positive rates should we target for 
fraud detection? Include the threshold breakdowns by percentage 
of transactions."
```

```
"A fintech client asks: 'What's the detection latency for card fraud?' 
Give the real P99 number and explain the MSK → Flink → SageMaker → 
DynamoDB pipeline."
```

### Real-Time Analytics

```
"Design a real-time analytics pipeline with <5 minute freshness SLA. 
Include ingestion, processing, storage, and serving layers with 
specific AWS services."
```

```
"How do we get sub-second query performance on streaming data? 
Walk through the Kinesis → Flink → Redshift Streaming Ingestion 
→ Metabase/Looker pattern."
```

### Platform Cost Benchmarks

```
"Break down the monthly cost for a production data platform: 
Redshift, Kinesis, Glue, S3, MSK, Flink, and supporting services. 
What percentage does each consume?"
```

```
"A client asks: 'What does it cost per million records to run a 
production data platform on AWS?' Give the specific number and 
the full cost stack behind it."
```

```
"We need to justify a $4K/month data platform budget. Break down 
exactly what we get: nodes, shards, brokers, storage, and 
processing capacity."
```

### CAC/LTV Marketing Benchmarks

```
"Rank all 8 marketing channels by CAC/LTV ratio. Which should we 
scale, optimize, cut, or pause? Include specific dollar amounts."
```

```
"Our social ads CAC is $62 with LTV of $95. Is that sustainable? 
Compare against all channels and recommend a reallocation strategy."
```

```
"What's the minimum viable CAC/LTV ratio for profitability? 
Which channels fall below it and what's the recommended action?"
```

```
"A CMO asks: 'Where should I put my next marketing dollar?' 
Rank channels by ROI with specific CAC, LTV, and ratio data."
```

### Data Quality

```
"What data quality metrics should we track in production? 
Include schema validation rates, null rates, freshness checks, 
and all 5 DQ dimensions with target percentages."
```

```
"Compare Great Expectations vs Monte Carlo for data observability. 
Include specific metrics each tracks and MTTR for incident response."
```

```
"Our pipeline has a 0.3% null rate across critical columns. 
Is that acceptable? What are the industry benchmarks for each 
DQ dimension?"
```

---

## AI Agents Expert

### Framework Comparison

```
"Compare all 5 agent frameworks: LangChain, CrewAI, AutoGen, 
Claude Agent SDK, and OpenHands. Include GitHub stars, architecture, 
strengths, weaknesses, and enterprise pricing for each."
```

```
"A client is choosing between LangChain and CrewAI for a multi-agent 
system. What are the trade-offs? When would you recommend each?"
```

```
"Compare AutoGen vs OpenHands for a code automation use case. 
Include architecture differences, ecosystem maturity, and deployment 
requirements."
```

```
"What's the enterprise cost of each agent framework? Compare 
LangSmith, CrewAI Enterprise, Azure AI, and Anthropic API pricing."
```

```
"Which framework has the largest ecosystem? Rank by GitHub stars, 
number of integrations, and community maturity."
```

### OpenHands Architecture

```
"Explain the OpenHands Agent class architecture: what components 
does an agent have, how does the step() cycle work, and where 
does state live?"
```

```
"How does OpenHands context condensation work? What happens when 
events exceed max_size=240? How many events are preserved?"
```

```
"Explain the OpenHands skill loading precedence. How do project-level 
skills override user-level and public skills?"
```

```
"What is the AgentDefinition schema? List all fields including 
name, model, tools, skills, system_prompt, and MCP servers."
```

```
"How does OpenHands handle conversation state? Explain EventLog 
persistence, activated knowledge skills, and execution status."
```

### Code Review Tools

```
"Compare CodeRabbit, GitHub Copilot, Sourcery, and Codacy. Include 
pricing, accuracy benchmarks (SWE-bench), market share, and 
false positive rates."
```

```
"A CTO asks: 'Is CodeRabbit worth it over GitHub Copilot?' 
Make the case with specific data: price difference, issues caught, 
SWE-bench ranking, and integration coverage."
```

```
"Which code review tool has the best accuracy? Compare F1 scores, 
false positive rates, and the 43% issue-detection gap between 
CodeRabbit and Copilot."
```

```
"Our team does Python. Which code review tool is best? Compare 
Sourcery's Python-first approach against CodeRabbit and Copilot."
```

```
"What's the total cost of code review tooling for a 50-person 
engineering team? Compare all 4 tools at scale."
```

### Enterprise Use Case Maturity

```
"Which enterprise AI use cases are production-ready vs still in 
pilot? List maturity levels with specific company examples and 
ROI data for each."
```

```
"A client says 'AI agents aren't ready for production.' Counter 
with specific production deployments: Klarna's 2.3M conversations, 
GitHub's 4.2 hrs/dev/week savings, and resolution rates."
```

```
"What's the ROI for customer support AI agents? Include Klarna's 
67% resolution rate and other production benchmarks."
```

```
"Where is process automation on the maturity curve? Is it still 
research-stage or has it moved to production?"
```

---

## Cross-Domain Prompts (Chain 2+ Agents)

### Healthcare + Data Platform

```
Read ~/.agents/agents/healthcare-it-expert.md AND 
~/.agents/agents/data-platform-expert.md as your domain context.

"Design a real-time clinical data pipeline: HL7v2 messages from 
Epic → AWS streaming platform → analytics dashboard. Include 
message types, FHIR mapping, AWS services, cost breakdown, 
and data quality framework."
```

```
Read both healthcare-it-expert.md and data-platform-expert.md.

"A hospital processes 2000 ADT messages/day. Architect the AWS 
infrastructure needed: ingestion, processing, storage, and serving. 
What will it cost monthly?"
```

### Healthcare + AI Agents

```
Read both healthcare-it-expert.md and ai-agents-expert.md.

"Design a multi-agent system for hospital insurance verification. 
Which agent framework fits best for real-time 270/271 processing? 
Include throughput requirements and framework comparison."
```

```
Read both healthcare-it-expert.md and ai-agents-expert.md.

"Build a clinical coding agent that maps HL7v2 OBX observations 
to FHIR resources. Which OpenHands architecture pattern fits? 
Include the Agent class design and Mirth Connect integration."
```

### Data Platform + AI Agents

```
Read both data-platform-expert.md and ai-agents-expert.md.

"A client wants AI-powered fraud detection. Design the end-to-end 
system: streaming pipeline (with AWS pricing), ML scoring agent 
(with framework choice), and monitoring. Total monthly cost?"
```

```
Read both data-platform-expert.md and ai-agents-expert.md.

"Compare the cost of building a data analytics agent with each 
framework. Factor in AWS infrastructure costs plus framework 
licensing. Which combination gives best ROI?"
```

### All Three Agents

```
Read all three agent definitions in ~/.agents/agents/.

"A healthcare client wants an agentic AI platform for claims 
processing. Design the full stack: HL7v2 ingestion, AWS streaming 
pipeline, multi-agent processing, and governance layer. Include 
message types, FHIR mapping, AWS costs, framework choice, and 
data quality metrics."
```

```
Read all three agent definitions in ~/.agents/agents/.

"Prepare a competitive analysis slide: why should a hospital choose 
our agentic AI platform over traditional RPA? Ground the argument 
with clinical data standards, infrastructure costs, framework 
maturity levels, and production ROI benchmarks."
```

```
Read all three agent definitions in ~/.agents/agents/.

"A CIO asks for a 90-day pilot plan. Which use case do we start 
with, what infrastructure do we need, which agent framework, and 
what's the expected ROI? Use real data from all three domains."
```

---

## Prompt Engineering Tips

| Tip | Example |
|-----|---------|
| **Be specific about output format** | "Give me a table comparing..." |
| **Ask for numbers** | "Include specific pricing, metrics, and percentages" |
| **Constrain to agent context** | "Using ONLY the data in your agent definition..." |
| **Request trade-offs** | "What are the strengths AND weaknesses?" |
| **Chain for depth** | Read 2+ agent files for cross-domain answers |
| **Set length** | "Answer in 3-4 lines" or "Create a one-page summary" |
| **Specify audience** | "Explain for a CTO" vs "Explain for an engineer" |
