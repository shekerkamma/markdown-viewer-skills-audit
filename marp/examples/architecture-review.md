---
marp: true
theme: default
paginate: true
size: 16:9
header: 'Architecture Review · 2026 Q2'
footer: 'Acme · Confidential'
style: |
  section.lead h1 { font-size: 2.4em; }
  section.lead h2 { font-weight: 400; color: #64748b; }
  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
  .pill { display: inline-block; padding: 2px 10px; border-radius: 999px; background: #dbeafe; color: #1e40af; font-size: 0.7em; }
---

<!-- _class: lead -->
<!-- _backgroundColor: #0f172a -->
<!-- _color: white -->

# HR Onboarding Platform
## Architecture Review — Q2 2026

Sheker · April 2026

---

# Agenda

1. **Context** — who uses the system, what it talks to
2. **Containers** — services, data stores, technology choices
3. **One critical sequence** — onboarding workflow end-to-end
4. **Open questions** — the two decisions we need this meeting to resolve

<!--
Speaker note: 25 min total. 5 / 10 / 5 / 5. Hold questions to the end of each section.
-->

---

# Context <span class="pill">Level 1</span>

```mermaid
C4Context
  Person(candidate, "Candidate")
  Person(recruiter, "Recruiter")
  Person(manager, "Hiring Manager")
  System(hr, "HR Onboarding Platform", "Tracks applications, offers, e-signatures")
  System_Ext(workday, "Workday", "Employee SOR")
  System_Ext(docusign, "DocuSign")
  System_Ext(checkr, "Checkr", "Background checks")
  Rel(candidate, hr, "Applies, signs offer")
  Rel(recruiter, hr, "Reviews + advances")
  Rel(manager, hr, "Approves offers")
  Rel(hr, workday, "Provisions hire")
  Rel(hr, docusign, "Sends contracts")
  Rel(hr, checkr, "Runs checks")
```

---

# Containers <span class="pill">Level 2</span>

<div class="columns">
<div>

```mermaid
flowchart TB
  web[Candidate Portal<br/>Next.js]
  admin[Recruiter Console<br/>Next.js]
  api[API Gateway<br/>Kong + Go]
  onboard[Onboarding Svc<br/>Go]
  workflow[Workflow Engine<br/>Temporal]
  notify[Notification Svc<br/>Node]
  pg[(Postgres)]
  redis[(Redis)]
  kafka((Kafka))
  s3[(S3)]
  web --> api
  admin --> api
  api --> onboard
  onboard --> pg
  onboard --> redis
  onboard --> s3
  onboard --> kafka
  kafka -.-> workflow
  workflow --> onboard
  workflow --> notify
```

</div>
<div>

**Stack choices**

- **Go** for state-machine services — operational simplicity
- **Temporal** for long-running workflows — durability over hand-rolled retries
- **Kafka** as the inter-service bus — replay capability for audit
- **Postgres** as system of record — Temporal's history is *not* a SOR

**Out of scope today:** mobile clients, ML resume screening (separate review)

</div>
</div>

---

# Sequence: Application → Offer

```mermaid
sequenceDiagram
  autonumber
  Candidate->>API: POST /applications
  API->>Onboarding: createApplication
  Onboarding->>Postgres: INSERT
  Onboarding->>Kafka: ApplicationSubmitted
  Kafka-->>Workflow: consume
  Workflow->>Checkr: run check (async)
  Checkr-->>Workflow: webhook clear/flag
  alt clear
    Workflow->>Onboarding: advanceTo("offer")
    Workflow->>Notify: send offer email
  else flagged
    Workflow->>Notify: notify recruiter for review
  end
```

<!--
The async fan-out is the architecturally interesting bit. Walk through
why we put Workflow on the consume side rather than calling Checkr from
Onboarding directly: durability, retry semantics, separation of state.
-->

---

# Open Questions

<div class="columns">
<div>

## 1. State of record

**Should the onboarding state machine live in Temporal or Postgres?**

- Today: Postgres is canonical, Temporal mirrors
- Pro mirror: clear ownership, audit clarity
- Con: dual writes, drift risk
- **Ask:** keep dual or move to Temporal-as-SOR?

</div>
<div>

## 2. Checkr feature flag

**Wrap Checkr behind a per-tenant flag?**

- Today: every tenant gets background checks
- Some enterprises want their own provider (HireRight)
- **Ask:** invest in the abstraction now or wait for the second tenant?

</div>
</div>

---

<!-- _class: lead -->
<!-- _backgroundColor: #f1f5f9 -->

# Decisions needed today

1. **State of record** — keep dual, or move to Temporal?
2. **Checkr flag** — abstract now, or wait?

Thank you.
