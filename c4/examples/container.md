# C4 Example — Container Diagram

Zooms one level into the HR Onboarding Platform from [system-context.md](system-context.md). Shows the apps, services, and data stores that make up the system, with the technologies on every relationship.

## Source

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()
title Container Diagram — HR Onboarding Platform

Person(candidate, "Candidate")
Person(recruiter, "Recruiter")
Person(manager, "Hiring Manager")

System_Boundary(hr, "HR Onboarding Platform") {
  Container(web, "Candidate Portal", "Next.js / React", "Application + onboarding tasks UI")
  Container(admin, "Recruiter Console", "Next.js / React", "Reviews + advances candidates")
  Container(api, "API Gateway", "Kong + Go", "JWT auth, rate limiting, routing")
  Container(onboarding, "Onboarding Service", "Go", "Application & offer state machine")
  Container(workflow, "Workflow Engine", "Temporal", "Long-running orchestration of onboarding steps")
  Container(notify, "Notification Service", "Node.js", "Email + SMS dispatch")
  Container(screening, "Resume Screening", "Python / FastAPI", "ML resume scoring")
  ContainerDb(pg, "Operational DB", "PostgreSQL 15", "Candidates, offers, tasks")
  ContainerDb(redis, "Cache + Sessions", "Redis", "JWT sessions, rate-limit counters")
  ContainerQueue(kafka, "Event Bus", "Kafka", "Domain events: ApplicationSubmitted, OfferAccepted, …")
  Container(s3, "Document Store", "S3", "Resumes, signed contracts, ID docs")
}

System_Ext(docusign, "DocuSign")
System_Ext(checkr, "Checkr")
System_Ext(twilio, "Twilio / SendGrid")
System_Ext(workday, "Workday")

Rel(candidate, web, "Uses", "HTTPS")
Rel(recruiter, admin, "Uses", "HTTPS")
Rel(manager, admin, "Uses", "HTTPS")

Rel(web, api, "Submits applications, fetches tasks", "REST / JSON")
Rel(admin, api, "Reviews candidates, advances stages", "REST / JSON")

Rel(api, onboarding, "Forwards", "gRPC")
Rel(api, screening, "Scores resumes", "gRPC")
Rel(onboarding, pg, "Reads/writes", "JDBC")
Rel(onboarding, redis, "Locks + cache", "RESP")
Rel(onboarding, s3, "Stores docs", "S3 SDK")
Rel(onboarding, kafka, "Publishes events", "Kafka protocol")

Rel(workflow, kafka, "Consumes events", "Kafka protocol")
Rel(workflow, onboarding, "Drives state transitions", "gRPC")
Rel(workflow, notify, "Triggers notifications", "gRPC")
Rel(workflow, docusign, "Sends contracts", "REST + webhook")
Rel(workflow, checkr, "Runs background checks", "REST + webhook")
Rel(workflow, workday, "Provisions hire on Day 0", "REST")

Rel(notify, twilio, "Sends SMS + email", "REST")

@enduml
```

## What changes from Context to Container

The `hr_platform` system in [system-context.md](system-context.md) is now opened up as `System_Boundary(hr) { ... }` containing:

- **3 web frontends** (`web`, `admin`, plus the API surface)
- **5 services** (`api`, `onboarding`, `workflow`, `notify`, `screening`)
- **4 data stores** (`pg`, `redis`, `kafka`, `s3`) — using `ContainerDb` and `ContainerQueue` for visual distinction

External systems (`docusign`, `checkr`, etc.) carry over from Context unchanged. People (`candidate`, `recruiter`, `manager`) carry over but now connect to *specific containers*, not the whole system.

## Why every Rel has a tech label

Compare:

```plantuml
Rel(api, onboarding, "Forwards")
Rel(api, onboarding, "Forwards", "gRPC")
```

The second one tells an engineer *exactly* what to wire up. The first is a documentation smell. C4 Container diagrams without tech labels are decoration; with tech labels, they're integration specs.

## What's intentionally not here

- **No replicas / instance counts.** "3 pods of api" belongs on a Deployment diagram.
- **No internal modules.** "The Onboarding Service has a StateMachine, Validator, and Repository" belongs on a Component diagram.
- **No request/response sequences.** Belongs on a Dynamic diagram.
