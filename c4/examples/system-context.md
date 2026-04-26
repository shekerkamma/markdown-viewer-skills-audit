# C4 Example — System Context Diagram

The "zoom-out" view: who uses our system and what does it talk to. Audience: anyone — execs, sales, new engineers, support. This is usually the first diagram you draw.

## Source

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

LAYOUT_WITH_LEGEND()
title System Context — HR Onboarding Platform

Person(candidate, "Candidate", "External applicant going through hire process")
Person(recruiter, "Recruiter", "Reviews and advances candidates")
Person(manager, "Hiring Manager", "Approves offers")
Person_Ext(it_admin, "IT Admin", "Provisions accounts in downstream systems")

Enterprise_Boundary(acme, "Acme Corp") {
  System(hr_platform, "HR Onboarding Platform", "Tracks applications, offers, e-signatures, onboarding tasks")
  System(workday, "Workday", "System of record for employees, payroll, benefits")
}

System_Ext(docusign, "DocuSign", "Electronic signature service")
System_Ext(checkr, "Checkr", "Background check provider")
System_Ext(twilio, "Twilio / SendGrid", "SMS + email delivery")
System_Ext(linkedin, "LinkedIn Recruiter", "Sourcing platform")

Rel(candidate, hr_platform, "Submits application, signs offer, completes onboarding tasks", "HTTPS")
Rel(recruiter, hr_platform, "Reviews + advances candidates", "HTTPS")
Rel(manager, hr_platform, "Approves offers", "HTTPS")
Rel(linkedin, hr_platform, "Sends candidate profiles", "Webhook")

Rel(hr_platform, docusign, "Sends offer letters", "REST + webhook")
Rel(hr_platform, checkr, "Runs background checks", "REST + webhook")
Rel(hr_platform, twilio, "Sends notifications", "REST")
Rel(hr_platform, workday, "Provisions hire on Day 0", "REST")
Rel(workday, it_admin, "Triggers AD/Okta provisioning", "Email")

@enduml
```

## Rendering hint

If your viewer supports PlantUML inline, the block above renders directly. Otherwise, encode it for the public PlantUML server:

```
https://www.plantuml.com/plantuml/svg/<encoded-source>
```

Or generate locally:

```bash
plantuml -tsvg system-context.puml
```

## What's intentionally not on this diagram

- No databases. No ECS / Kubernetes / VPC.
- No internal services (auth, notification, workflow). Those are *inside* `hr_platform`.
- No DevOps tooling.

If a reviewer asks "where's Postgres?" — that's the signal you owe them a Container diagram. Don't pollute Context.

## What's intentionally there

- **`Person_Ext(it_admin)`** — the IT admin doesn't use the HR Platform directly, but they're a downstream actor in the workflow. Marking them external prevents a future "we forgot to design the IT handoff" surprise.
- **`Enterprise_Boundary(acme)`** — explicitly groups "things we own" vs. SaaS. Helps with vendor / build-vs-buy conversations.
- **Technology labels on every `Rel`** — "Webhook", "REST + webhook", "Email". Even at Context level, these inform integration risk.
