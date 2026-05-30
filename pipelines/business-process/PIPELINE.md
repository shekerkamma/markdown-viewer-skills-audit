# Business Process & Enterprise Category — Pipeline Tests

End-to-end pipeline combining **project-level** modeling skills (`archimate`, `bpmn`, `uml`) with **global-level** business planning and review skills (`office-hours`, `autoplan`, `plan-ceo-review`, `plan-eng-review`, `presales-deal-prep`, `contract-reviewer`, `00-account-briefing`) for enterprise architecture documentation, process design, and business planning workflows.

## Skills in this pipeline

### Project-level (installed in `.agents/skills/`)
| Skill | Role | Output | Notation |
|---|---|---|---|
| `archimate` | Enterprise architecture (Business/Application/Technology layers, TOGAF viewpoints) | PlantUML with ArchiMate stdlib | `!include <archimate/Archimate>`, `Business_*`, `Application_*`, `Technology_*`, `Motivation_*`, `Strategy_*`, `Implementation_*` |
| `bpmn` | Business process flows, approval chains, integration patterns | PlantUML with mxgraph stencils | `mxgraph.bpmn.*` (events, gateways, tasks), `mxgraph.eip.*` (EIP), `mxgraph.lean_mapping.*` (VSM) |
| `uml` | Software modeling (class, sequence, activity, state, component, deployment) | PlantUML | Standard PlantUML keywords + optional `mxgraph.*` stencils |
| `infocard` | Component/service summary cards | Embedded HTML | Direct HTML |
| `infographic` | Visual process overviews | Templated HTML | Space-separated key-value syntax |
| `marp` / `slide-narrative` | Presentation layer | Markdown slides / prose | Marp frontmatter |
| `diagram-export` | Rasterize to PNG/SVG/PDF | Image files | CLI commands |

### Global-level (in `~/.claude/skills/`)
| Skill | Role | Output |
|---|---|---|
| `office-hours` | Problem framing (YC-style forcing questions) | Design doc |
| `plan-ceo-review` | CEO/founder plan review (premise challenge, 10-star product, dual voices) | Review report with consensus table |
| `plan-eng-review` | Eng manager plan review (architecture, test coverage, performance) | Review report with test plan artifact |
| `autoplan` | Orchestrator: chains CEO → design → eng → DX reviews with auto-decisions | Fully reviewed plan with decision audit trail |
| `00-account-briefing` | Pre-meeting enterprise account briefing | Markdown briefing |
| `presales-deal-prep` | End-to-end presales: research → strategy → contract → meeting prep | Multi-file package |
| `contract-reviewer` | Contract risk analysis (red flags, yellow flags, negotiation scripts) | Markdown report |

### How They Connect

```
                     MODELING (what the system IS)
                     ┌────────────────────────────┐
                     │  archimate (enterprise EA)  │
                     │       ↓ zooms into          │
                     │  bpmn (process workflows)   │
                     │       ↓ zooms into          │
                     │  uml (software design)      │
                     └──────────┬─────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ↓                       ↓                       ↓
  infocard/infographic    diagram-export         slide-narrative
  (summary visuals)       (PNG/SVG for docs)     → marp (deck)

                    PLANNING (what to BUILD)
                    ┌──────────────────────────────┐
                    │  office-hours (problem frame) │
                    │       ↓                       │
                    │  plan-ceo-review (scope)      │
                    │       ↓                       │
                    │  plan-eng-review (execution)  │
                    │       ↓                       │
                    │  autoplan (orchestrate all)   │
                    └──────────┬───────────────────┘
                               │
                    BUSINESS (who to SELL to)
                    ┌──────────────────────────────┐
                    │  00-account-briefing          │
                    │       ↓                       │
                    │  presales-deal-prep           │
                    │       ↓                       │
                    │  contract-reviewer            │
                    └──────────────────────────────┘
```

---

## Pipeline 1: Enterprise Architecture — Top-Down Modeling

**Goal:** Model a single enterprise system at three zoom levels — ArchiMate (enterprise landscape), BPMN (process detail), UML (software design) — then package for stakeholder delivery.

**System under test:** Hospital Patient Intake — from the business process of a patient arriving, through the application services that support intake, down to the software components.

### Step 1 — Enterprise landscape (ArchiMate)
**Skill:** `archimate`

> Use the archimate skill to draw an enterprise landscape for a hospital patient intake system. Three layers:
>
> **Business layer:**
> - Actors: Patient, Receptionist, Triage Nurse, Attending Physician
> - Processes: Patient Registration, Insurance Verification, Triage Assessment, Bed Assignment
> - Services: Intake Service, Scheduling Service, Billing Service
>
> **Application layer:**
> - Components: EHR System, Insurance Gateway, Bed Management App, Patient Portal
> - Services: Patient Record API, Insurance Check API, Scheduling API
> - Data Objects: Patient Record, Insurance Claim, Appointment
>
> **Technology layer:**
> - Nodes: App Server Cluster, Database Server
> - System Software: PostgreSQL, Redis, Nginx
> - Communication Network: Hospital LAN, HL7 FHIR Interface
>
> Show relationships: Patient triggers Registration, Registration realizes Intake Service, EHR System serves Intake Service, App Server runs EHR System.

**Grade:**
- [ ] `@startuml` / `@enduml` present
- [ ] `!include <archimate/Archimate>` included
- [ ] ` ```plantuml ` fence (not ` ```text `)
- [ ] Three `rectangle` groups: Business, Application, Technology
- [ ] Correct macros: `Business_Actor`, `Business_Process`, `Application_Component`, `Technology_Node`, etc.
- [ ] Correct relationship macros: `Rel_Triggering`, `Rel_Realization`, `Rel_Serving`, `Rel_Assignment`
- [ ] Cross-layer relationships connect Business → Application → Technology
- [ ] No raw `-->` arrows — uses `Rel_*` macros throughout

### Step 2 — Motivation & strategy overlay (ArchiMate)
**Skill:** `archimate`

> Add a motivation layer to the hospital intake model:
> - Stakeholders: Hospital Board, CIO, Chief Medical Officer, Patients
> - Drivers: Reduce wait times (current avg 45 min), Regulatory compliance (HIPAA), Cost reduction
> - Goals: Average intake < 15 min, 100% insurance pre-verification, Zero paper forms
> - Requirements: Real-time bed availability, HL7 FHIR integration, Mobile check-in
> - Constraints: Budget $500K, 6-month timeline, Must integrate with legacy Cerner EHR
>
> Connect: Board influences Goals, Goals realize Requirements, Requirements constrain Application Components from Step 1.

**Grade:**
- [ ] `Motivation_Stakeholder`, `Motivation_Driver`, `Motivation_Goal`, `Motivation_Requirement`, `Motivation_Constraint` macros used
- [ ] `Rel_Influence` from stakeholders to drivers/goals
- [ ] `Rel_Realization` from goals to requirements
- [ ] Cross-layer: requirements connect to application components from Step 1
- [ ] Separate `rectangle "Motivation"` layer group

### Step 3 — Process detail (BPMN)
**Skill:** `bpmn`

> Use the bpmn skill to draw the detailed Patient Registration process from the ArchiMate model. Show:
>
> **Pool: "Patient Intake"**
> - Start event (patient arrives)
> - User task: Receptionist collects demographics
> - Service task: System checks for existing record (EHR lookup)
> - Exclusive gateway: Existing patient?
>   - Yes → Service task: Pull existing record
>   - No → User task: Create new record
> - Parallel gateway (split): simultaneously run:
>   - Service task: Insurance verification (calls Insurance Gateway)
>   - User task: Triage nurse assessment
> - Parallel gateway (join): both complete
> - Exclusive gateway: Insurance verified?
>   - Yes → Service task: Assign bed (Bed Management)
>   - No → User task: Manual insurance follow-up → loop back to verification
> - End event: Patient assigned to bed
>
> **Pool: "Insurance Provider"** (separate pool, message flows)
> - Receives verification request (message catching event)
> - Sends verification response (message end event)

**Grade:**
- [ ] `@startuml` / `@enduml`, `left to right direction`
- [ ] ` ```plantuml ` fence
- [ ] `mxgraph.bpmn.event.start`, `mxgraph.bpmn.event.end` for events
- [ ] `mxgraph.bpmn.gateway2.exclusive` for XOR decisions
- [ ] `mxgraph.bpmn.gateway2.parallel` for AND split/join
- [ ] Two pools: `rectangle "Patient Intake"` and `rectangle "Insurance Provider"`
- [ ] Sequence flows `-->` within pools, message flows `..>` across pools
- [ ] Gateway branches labeled (`"Yes"`, `"No"`)
- [ ] Loop-back from manual follow-up to verification shown

### Step 4 — Integration patterns (BPMN/EIP)
**Skill:** `bpmn`

> Use the bpmn skill with EIP stencils to draw the message integration architecture between the hospital systems. Show:
>
> - EHR System publishes patient events to a Message Channel
> - Content-Based Router routes by event type: registration → Insurance Gateway, triage → Bed Management, discharge → Billing
> - Insurance Gateway uses a Message Translator (HL7 FHIR → payer-specific format)
> - Dead Letter Channel catches failed messages
> - Wire Tap copies all messages to an Audit Log
> - Competing Consumers on the Bed Management queue (2 instances for load)

**Grade:**
- [ ] `mxgraph.eip.*` stencils: `messageChannel`, `content_based_router`, `message_translator`, `deadLetterChannel`, `wire_tap`, `competing_consumers`
- [ ] Correct EIP patterns (not just labeled boxes)
- [ ] Dead Letter Channel shown as a separate path from the router
- [ ] Wire Tap taps the main channel (not a branch from the router)
- [ ] Competing Consumers shown as parallel consumers on one channel

### Step 5 — Software design (UML)
**Skill:** `uml`

> Use the uml skill to produce three diagrams for the EHR System component:
>
> **5a. Class diagram:**
> - `Patient` (id, name, dob, insuranceId, medicalRecordNumber)
> - `InsurancePolicy` (policyId, provider, planType, copay, status)
> - `IntakeRecord` (recordId, patientId, triageLevel, chiefComplaint, vitalSigns, arrivalTime)
> - `BedAssignment` (assignmentId, bedId, patientId, department, assignedAt, releasedAt)
> - Relationships: Patient 1--* IntakeRecord, Patient 1--1 InsurancePolicy, IntakeRecord 1--0..1 BedAssignment
>
> **5b. Sequence diagram:**
> - Actors: Receptionist, EHR System, Insurance Gateway, Bed Manager
> - Flow: Receptionist → EHR: createIntake() → EHR → Insurance Gateway: verifyInsurance(policyId) → response → EHR → Bed Manager: requestBed(department, acuity) → response → EHR → Receptionist: intakeComplete(bedNumber)
>
> **5c. State machine diagram:**
> - States for IntakeRecord: Created → Demographics Collected → Insurance Verified (or Insurance Pending) → Triaged → Bed Assigned → Completed
> - Transitions with guard conditions (e.g., [insuranceValid] / [insuranceInvalid])

**Grade:**
- [ ] Three separate `@startuml`/`@enduml` blocks
- [ ] **Class:** `class Patient { }` with attributes, correct cardinality notation (`"1" -- "*"`)
- [ ] **Sequence:** `participant` declarations, `->` for sync calls, `-->` for responses, correct message signatures
- [ ] **State machine:** `[*] -->` for initial state, `state` declarations, guard conditions in brackets
- [ ] All three diagrams model the same system consistently (same class names, same methods, same states)

### Step 6 — Component summary cards
**Skill:** `infocard`

> Create info cards for the four main application components from the ArchiMate model:
> 1. **EHR System** — core patient record management, integrates with 3 external systems, handles 500 intakes/day
> 2. **Insurance Gateway** — real-time verification, supports 12 payer formats, avg response 2.3s, HL7 FHIR translation
> 3. **Bed Management App** — real-time bed availability across 8 departments, 400 beds, 94% occupancy rate
> 4. **Patient Portal** — mobile check-in, pre-registration, wait time display, satisfaction score 4.2/5
>
> Use `metric-board` layout with a business tone.

**Grade:**
- [ ] 4 cards with metrics from the prompt (not hallucinated numbers)
- [ ] Direct HTML, no code fence
- [ ] Business tone auto-sensed (not tech-blueprint for this audience)
- [ ] Metrics prominently displayed (500 intakes/day, 2.3s response, 94% occupancy, 4.2/5 score)

### Step 7 — Presentation
**Skills:** `slide-narrative` → `marp`

> 1. Use slide-narrative to outline a 20-minute architecture review for the hospital CIO. Goal: approve the $500K modernization budget. Audience: CIO + IT leadership (technical but time-constrained). Use all three model levels (ArchiMate landscape, BPMN process, UML design) as visual evidence.
>
> 2. Use marp to build the deck from that narrative. 12-15 slides.

**Grade:**
- [ ] Narrative arc culminates in the $500K ask
- [ ] Three zoom levels referenced: enterprise landscape → process flow → software design
- [ ] Marp deck with speaker notes, valid frontmatter
- [ ] Architecture diagrams referenced by name (not generic "see diagram")
- [ ] Motivation layer (goals, constraints) used to frame the business case

---

## Pipeline 2: Process Redesign — Current State vs. Future State

**Goal:** Model a broken process, identify waste, redesign it, and present the before/after.

**System under test:** Employee onboarding at a 500-person company — currently takes 3 weeks, goal is 3 days.

### Step 1 — Current state value stream (BPMN/Lean)
**Skill:** `bpmn`

> Use the bpmn skill with lean mapping stencils to draw the current-state value stream map for employee onboarding:
>
> - Outside Source: HR (supplier) → Outside Source: New Hire (customer)
> - Process steps: Offer Letter Sent → Background Check (5 days wait) → IT Equipment Order (3 days) → Account Provisioning (2 days, manual) → Orientation Scheduling (1 day) → First Day Orientation → Buddy Assignment (often forgotten) → 30-Day Check-in
> - Inventory buffers: 15 pending background checks, 8 equipment orders in queue
> - Kaizen bursts on: manual account provisioning, equipment ordering (no automation)
> - Timeline at bottom showing lead time vs. processing time per step

**Grade:**
- [ ] `mxgraph.lean_mapping.*` stencils: `outside_sources`, `manufacturing_process`, `inventory_box`, `kaizen_lightening_burst`, `timeline2`
- [ ] Wait times annotated between process steps
- [ ] Inventory buffers shown at bottleneck points
- [ ] Kaizen bursts mark improvement opportunities
- [ ] Timeline shows total lead time (21 days) vs. actual processing time (~4 days)

### Step 2 — Current state BPMN process
**Skill:** `bpmn`

> Draw the detailed BPMN for the current onboarding process. Show three pools:
>
> **Pool: HR** — Start → Create employee record → Send offer letter → Wait for background check (timer event, 5 days) → Schedule orientation
>
> **Pool: IT** — Receive account request (message) → Manual provisioning (user task, 2 days) → Order equipment (manual task, 3 days) → Ship equipment → Configure laptop
>
> **Pool: Manager** — Receive new hire notification (message) → Assign buddy (often delayed — timer boundary event, escalates after 3 days) → Plan first-week tasks
>
> Message flows between pools. Show error boundary event on background check (check fails → terminate process).

**Grade:**
- [ ] Three pools with internal sequence flows
- [ ] `mxgraph.bpmn.event.timerCatching` for wait states
- [ ] `mxgraph.bpmn.event.errorBound` on background check
- [ ] `mxgraph.bpmn.user_task` for manual steps, `mxgraph.bpmn.service_task` for automated
- [ ] Message flows `..>` between pools
- [ ] Timer boundary event on buddy assignment with escalation path

### Step 3 — Future state BPMN process
**Skill:** `bpmn`

> Draw the redesigned BPMN for automated onboarding (target: 3 days). Changes:
>
> **Pool: HR** — Start → Service task: Auto-create employee record (from signed offer) → Service task: Trigger background check API → Parallel gateway: simultaneously start IT provisioning + orientation scheduling + manager notification
>
> **Pool: IT (automated)** — Service task: Auto-provision accounts (SCIM/SSO) → Service task: Auto-order equipment (asset management API) → Service task: Auto-configure laptop (MDM)
>
> **Pool: Manager** — Receive notification → Business rule task: Auto-assign buddy (by team, seniority) → Service task: Generate first-week calendar from template
>
> All manual tasks replaced with service tasks. No timer waits. Background check runs in parallel (no blocking).

**Grade:**
- [ ] `mxgraph.bpmn.service_task` replaces `mxgraph.bpmn.user_task` and `mxgraph.bpmn.manual_task`
- [ ] Parallel gateway enables concurrent execution
- [ ] No timer intermediate events (no waiting steps)
- [ ] `mxgraph.bpmn.business_rule_task` for buddy assignment logic
- [ ] Visually simpler than Step 2 (fewer steps, no escalation paths)
- [ ] Total process time annotated (~3 days vs. 21 days)

### Step 4 — Software design for the automation
**Skill:** `uml`

> Draw a component diagram for the onboarding automation platform:
>
> - Components: Onboarding Orchestrator, HR System Adapter, Background Check API Client, SCIM Provisioner, Asset Management Client, MDM Configurator, Notification Service, Calendar Service
> - Interfaces: IOnboardingWorkflow (exposed by Orchestrator), IHREvents (consumed from HR System), IBackgroundCheck (external), ISCIMProvider (external SSO), IAssetOrder (external)
> - Dependencies: Orchestrator uses all other components; HR System Adapter provides IHREvents; SCIM Provisioner requires ISCIMProvider
>
> Also draw an activity diagram (with swimlanes) showing the automated onboarding flow across HR, IT, and Manager lanes.

**Grade:**
- [ ] **Component diagram:** `component` declarations, `interface` or `()` notation, correct `-->` dependencies
- [ ] **Swimlane activity:** `|HR|`, `|IT|`, `|Manager|` lane syntax, `:action;` notation, `fork`/`join` for parallel
- [ ] Both diagrams consistent (same component names, same flow)

### Step 5 — Before/after infographic
**Skill:** `infographic`

> Create a comparison infographic showing the onboarding transformation:
>
> **Before:** 21 days, 6 manual steps, 3 handoffs, 15-item backlog, 62% satisfaction score
> **After:** 3 days, 1 manual step (buddy intro), 0 handoffs, 0 backlog, target 95% satisfaction
>
> Use the `comparison` template.

**Grade:**
- [ ] `infographic comparison` template
- [ ] Space-separated key-value syntax (NOT YAML colons)
- [ ] Exactly 2 items (Before, After) with children metrics
- [ ] `desc` not `description`
- [ ] Numbers match the prompt

### Step 6 — Plan review pipeline
**Skills:** `office-hours` → `plan-ceo-review` → `plan-eng-review` (or `autoplan`)

> 1. Use office-hours to frame the problem: "Employee onboarding takes 3 weeks. New hires report feeling lost. IT is overwhelmed with manual provisioning. We want to automate."
>
> 2. Use plan-ceo-review on the resulting design doc. Challenge: is automation the right answer, or is the real problem poor process design regardless of tooling?
>
> 3. Use plan-eng-review on the technical plan. Focus on: integration complexity (5 external APIs), failure modes (what if background check API is down?), test strategy.

**Grade:**
- [ ] **office-hours:** 6 forcing questions answered, design doc produced
- [ ] **plan-ceo-review:** Premise challenged (automation vs. process redesign), 10-star product articulated, dual voices consensus
- [ ] **plan-eng-review:** Architecture diagram (ASCII), test plan artifact, failure modes enumerated, complexity assessed
- [ ] Plans reference the BPMN/UML diagrams from earlier steps

---

## Pipeline 3: Enterprise Sales — Account Briefing to Contract

**Goal:** Use the business modeling skills to support a presales engagement — from account research through architecture presentation to contract review.

**Scenario:** Selling the hospital onboarding platform (from Pipeline 2) to a large hospital network.

### Step 1 — Account briefing
**Skill:** `00-account-briefing` (global)

> Generate a pre-meeting briefing for "Memorial Health Network" — a 12-hospital system. Meeting topic: IT modernization, specifically patient intake and employee onboarding automation. Research their current tech stack, recent news, key IT leadership.

**Grade:**
- [ ] One-page briefing with account context
- [ ] Key personnel identified (CIO, VP Engineering, etc.)
- [ ] Recent news/initiatives referenced
- [ ] Meeting-relevant context highlighted

### Step 2 — Enterprise architecture for the prospect
**Skill:** `archimate`

> Draw an ArchiMate diagram showing how our onboarding platform fits into Memorial Health Network's enterprise landscape:
>
> **Their existing systems (Application layer):**
> - Cerner EHR, Workday HR, ServiceNow IT, Active Directory
>
> **Our platform (Application layer, highlighted):**
> - Onboarding Orchestrator, SCIM Provisioner, Asset Manager
>
> **Integration layer:**
> - HL7 FHIR Interface (to Cerner), SCIM (to Active Directory), REST API (to Workday), ServiceNow API (to ServiceNow)
>
> **Business layer:**
> - Services: Patient Intake, Employee Onboarding, IT Provisioning
>
> Show serving relationships from our platform to their business services, and realization relationships from integration interfaces to the connections.

**Grade:**
- [ ] Clear visual distinction between "their systems" and "our platform" (grouping or annotation)
- [ ] Integration interfaces explicitly modeled as `Application_Interface`
- [ ] `Rel_Serving` from our components to their business services
- [ ] `Rel_Realization` from interfaces to integration connections
- [ ] Enterprise-grade diagram (not a simple flowchart)

### Step 3 — Presales deal prep
**Skill:** `presales-deal-prep` (global)

> Run the full presales pipeline for Memorial Health Network. We're selling our healthcare IT modernization platform. Focus on patient intake automation and employee onboarding. Budget range: $500K-$2M. Timeline: 6-month pilot on 2 hospitals, then rollout.

**Grade:**
- [ ] Account briefing stage completed (research)
- [ ] AI strategy brief generated (how AI/automation fits their landscape)
- [ ] Conversation prep with likely objections and responses
- [ ] Cheat sheet produced for the meeting

### Step 4 — Contract review
**Skill:** `contract-reviewer` (global)

> Review this MSA (Master Service Agreement) from Memorial Health Network. Key areas to flag:
> - IP ownership clauses (who owns customizations?)
> - Data handling (we'll process PHI — HIPAA BAA required)
> - SLA penalties (they want 99.99% uptime with $10K/hour penalty)
> - Termination clauses (they want 30-day termination for convenience)
> - Liability cap (they propose uncapped for data breaches)

**Grade:**
- [ ] Red flags identified (uncapped liability, aggressive SLA penalties)
- [ ] Yellow flags identified (30-day termination, IP ambiguity)
- [ ] Missing items flagged (HIPAA BAA not mentioned)
- [ ] Negotiation scripts provided for each flag
- [ ] Plain-English "Short Version" summary
- [ ] Bottom line recommendation (sign / negotiate / walk away)

### Step 5 — Architecture presentation for the prospect
**Skills:** `slide-narrative` → `marp`

> Build a 15-minute pitch deck for Memorial Health Network's CIO. Use:
> - The ArchiMate integration diagram from Step 2 (shows platform fit)
> - The BPMN before/after from Pipeline 2 (shows process improvement)
> - The comparison infographic from Pipeline 2 (shows ROI numbers)
>
> Goal: get approval for a 2-hospital pilot ($500K).

**Grade:**
- [ ] Narrative references the specific prospect (Memorial Health Network, not generic)
- [ ] ArchiMate diagram shows integration with their Cerner/Workday/ServiceNow stack
- [ ] Before/after BPMN shows the transformation story
- [ ] ROI numbers from the infographic anchor the $500K ask
- [ ] Marp deck with speaker notes referencing the contract review findings (potential objections)

---

## Pipeline 4: Migration Planning with ArchiMate Implementation Layer

**Goal:** Use ArchiMate's Strategy and Implementation layers to plan and track a system migration.

### Step 1 — Current-state plateau
**Skill:** `archimate`

> Draw an ArchiMate implementation planning diagram for migrating the hospital from Cerner EHR to Epic EHR:
>
> **Plateau: "Current State (Q1 2026)"**
> - Cerner EHR (Application Component)
> - Manual intake process (Business Process)
> - On-premise database server (Technology Node)
>
> **Plateau: "Transition (Q2-Q3 2026)"**
> - Cerner EHR + Epic EHR running in parallel
> - Hybrid intake process (some patients on each system)
> - Data migration pipeline (Technology Process)
>
> **Plateau: "Target State (Q4 2026)"**
> - Epic EHR only
> - Automated intake process
> - Cloud database (AWS RDS)
>
> **Gaps:** Data migration risk, Staff retraining, Dual-system operational cost
>
> Connect with `Implementation_WorkPackage` for each migration task and `Implementation_Gap` between plateaus.

**Grade:**
- [ ] `Implementation_Plateau` for each state (Current, Transition, Target)
- [ ] `Implementation_Gap` between plateaus
- [ ] `Implementation_WorkPackage` for migration tasks
- [ ] `Implementation_Deliverable` for key outputs (migrated data, trained staff)
- [ ] Chronological left-to-right flow
- [ ] Gaps clearly annotated with risk descriptions

### Step 2 — Strategy capability map
**Skill:** `archimate`

> Draw a strategy layer showing the capabilities needed for the migration:
>
> - Capabilities: Data Migration, System Integration, Staff Training, Process Redesign, Vendor Management
> - Resources: DBA team (3), Integration engineers (2), Training budget ($150K), Epic implementation partner
> - Value Streams: Patient care continuity, Operational efficiency, Regulatory compliance
> - Courses of Action: Phased migration (chosen) vs. Big-bang cutover (rejected)

**Grade:**
- [ ] `Strategy_Capability`, `Strategy_Resource`, `Strategy_ValueStream`, `Strategy_CourseOfAction` macros
- [ ] `Rel_Realization` from capabilities to value streams
- [ ] `Rel_Assignment` from resources to capabilities
- [ ] Rejected alternative (big-bang) still shown but annotated as rejected

### Step 3 — Migration process detail
**Skill:** `bpmn`

> Draw a BPMN process for the data migration workflow:
>
> - Start: Migration window opens (timer start event, Saturday 2 AM)
> - Service task: Extract patient records from Cerner (batch)
> - Service task: Transform records (Cerner format → Epic FHIR)
> - Exclusive gateway: Validation passed?
>   - Yes → Service task: Load into Epic
>   - No → Service task: Log to error queue → Manual task: Fix data quality issues → loop back to transform
> - Parallel tasks after load: Verify record counts, Run reconciliation report, Notify stakeholders
> - End event: Migration batch complete
>
> Add error boundary event on the extract task (Cerner connection failure → retry 3x → escalate to on-call DBA).

**Grade:**
- [ ] `mxgraph.bpmn.event.timerStart` for the migration window
- [ ] `mxgraph.bpmn.service_task` for automated steps
- [ ] Error handling with `mxgraph.bpmn.event.errorBound`
- [ ] Loop-back for data quality fixes
- [ ] Parallel gateway for post-load verification tasks

### Step 4 — Technical design
**Skill:** `uml`

> Draw a deployment diagram for the migration infrastructure:
>
> - Node "On-Premise DC": Cerner DB Server (artifact: patient_records.db), Migration ETL Server (artifact: etl-pipeline.jar)
> - Node "AWS": Epic RDS Instance (artifact: epic_fhir.db), Lambda (artifact: transform-function), S3 (artifact: migration-staging)
> - Communication paths: On-Premise DC ←→ AWS via VPN (labeled "IPsec, 1 Gbps")
> - ETL Server deploys to Lambda via CI/CD pipeline

**Grade:**
- [ ] `node` declarations for On-Premise DC and AWS
- [ ] `artifact` declarations for deployable units
- [ ] `database` for database servers
- [ ] Communication path labeled with protocol and bandwidth
- [ ] Deployment relationships shown

---

## Pipeline 5: Adversarial & Edge Cases

### 5a — ArchiMate: mixed layer elements
> Use the archimate skill but put Business_Actor inside the Technology layer rectangle and Technology_Node inside the Business layer.

**Expected:** Pushback — ArchiMate elements belong in their named layers. Cross-layer placement violates the metamodel. The skill should suggest using cross-layer relationships (`Rel_Serving`, `Rel_Realization`) instead of misplacing elements.

### 5b — BPMN: merge sequence and message flows
> Use the bpmn skill. Draw a process where sequence flows (`-->`) go between two different pools.

**Expected:** Correction — BPMN rules: sequence flows are within a pool, message flows (`..>`) are between pools. Should fix the arrow types.

### 5c — UML: wrong diagram type for the task
> Use the uml skill. Draw a class diagram showing the runtime interaction between a user clicking "Submit" and the server processing the request.

**Expected:** Pushback — runtime interactions are sequence diagrams, not class diagrams. Class diagrams show static structure. Should suggest a sequence diagram instead.

### 5d — ArchiMate: using raw arrows instead of Rel_ macros
> Use the archimate skill. Connect elements with `-->` instead of `Rel_Serving(a, b, "label")`.

**Expected:** Correction — ArchiMate stdlib requires `Rel_*` macros for semantically correct relationships. Raw arrows lose the ArchiMate relationship types. Should convert to proper macros.

### 5e — BPMN: 50-step linear process
> Use the bpmn skill. Draw an onboarding process with 50 sequential steps, no gateways, no parallel paths.

**Expected:** Pushback — 50 linear steps indicate the process should be decomposed into sub-processes. BPMN best practice is to use collapsed sub-processes for groups of related steps. Should suggest decomposition.

### 5f — EIP: wrong stencil family
> Use the bpmn skill with `mxgraph.aws4.sqs` for the message queue instead of `mxgraph.eip.messageChannel`.

**Expected:** Correction — EIP integration patterns should use `mxgraph.eip.*` stencils for pattern correctness. AWS stencils are for cloud architecture diagrams. Should use the right family for the diagram type.

---

## Grading Summary

| Pipeline | Steps | What it proves |
|---|---|---|
| **1: Top-Down Modeling** | 7 | ArchiMate → BPMN → UML zoom levels compose; same system at three abstraction layers |
| **2: Process Redesign** | 6 | Before/after process modeling; lean VSM + BPMN + UML + plan reviews chain end-to-end |
| **3: Enterprise Sales** | 5 | Modeling skills support business workflows; archimate → presales → contract review |
| **4: Migration Planning** | 4 | ArchiMate implementation/strategy layers for roadmap planning; BPMN + UML for execution detail |
| **5: Adversarial** | 6 | Metamodel rules enforced; wrong layer placement, wrong flow types, wrong stencil families caught |

### Pass criteria
- **ArchiMate passes** when: correct `!include`, layer-appropriate macros (`Business_*` in Business, `Application_*` in Application, etc.), `Rel_*` macros for relationships (not raw arrows), elements grouped in correct layer rectangles.
- **BPMN passes** when: sequence flows within pools, message flows between pools, correct event/gateway types, pools/lanes properly structured.
- **UML passes** when: right diagram type for the question, consistent naming across diagrams, standard PlantUML syntax.
- **Cross-skill consistency** when: the same entity (e.g., "EHR System") has the same name and role across ArchiMate, BPMN, and UML diagrams.
- **Global skills pass** when: they reference and build on the modeling outputs (not generic advice disconnected from the diagrams).
- **Adversarial tests pass** when the skill corrects or refuses. They **fail** when the skill silently produces invalid models.
