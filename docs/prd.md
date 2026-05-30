# PRD — TicketForge

## 1. Overview

### Product Summary

**TicketForge** — Turns GitHub Issues into tested, reviewed pull requests using a multi-agent AI pipeline.

TicketForge is an autonomous code pipeline that monitors GitHub Issues for bug tickets, analyzes them with a content-researcher agent, generates candidate fixes in Docker sandboxes using a CodeActAgent, validates fixes through a code-review-specialist agent, and creates pull requests via the GitHub CLI. The entire pipeline runs without developer intervention, producing PRs that developers review and merge like any human-written code.

### Objective

This PRD covers the MVP as defined in the product vision: a complete ticket-to-PR pipeline for single-service bug fixes, with a web dashboard for monitoring. The MVP is buildable in 6–8 weeks and targets 3 pilot teams processing 50+ tickets/month.

### Market Differentiation

The technical implementation must deliver three things to achieve differentiation: (1) **full pipeline execution** — from webhook receipt to PR creation without human intervention, (2) **sandboxed code generation** — Docker containers that isolate agent execution from production systems, and (3) **transparent audit trails** — an event stream that logs every agent action so developers can trace any PR back to its decision chain. These are the capabilities that GitHub Copilot (code completion only) and CodeRabbit (review only) do not provide.

### Magic Moment

A developer opens GitHub notifications and finds a PR already created for a bug ticket. The PR has a clean diff, updated tests, and a review summary. They review it in 5 minutes and merge. The technical implementation must ensure: webhook-to-PR latency under 30 minutes, fix accuracy above 70% for single-service bugs, and review notes that are specific enough to give the developer confidence without reading every changed line.

### Success Criteria

- Pipeline processes a bug ticket from webhook receipt to PR creation in < 30 minutes
- Fix acceptance rate ≥ 70% (PRs merged without significant modification)
- Escalation rate between 25–45% (conservative quality gates)
- Regression rate < 2% for merged agent PRs
- Dashboard loads in < 2 seconds with real-time pipeline status
- All P0 features functional with test coverage ≥ 80%
- Docker sandbox spin-up time < 60 seconds

---

## 2. Technical Architecture

### Architecture Overview

```mermaid
graph TB
    subgraph "GitHub"
        GI[GitHub Issues] -->|webhook| WH[Webhook Listener]
        PR_OUT[Pull Requests] 
    end

    subgraph "TicketForge Backend (FastAPI)"
        WH --> Q[Task Queue]
        Q --> CR[Content Researcher Agent]
        CR --> CA[CodeActAgent]
        CA --> RV[Code Review Specialist]
        RV -->|approved| PRC[PR Creator]
        RV -->|rejected/low-confidence| ESC[Escalation Handler]
        PRC --> PR_OUT
        ESC -->|comment| GI
        
        ES[Event Stream Logger] 
        CR -.->|log| ES
        CA -.->|log| ES
        RV -.->|log| ES
    end

    subgraph "Infrastructure"
        DB[(PostgreSQL)]
        DK[Docker Sandbox]
        CL[Claude API]
    end

    CA -->|execute in| DK
    CR -->|analyze via| CL
    CA -->|generate via| CL
    RV -->|review via| CL
    ES -->|persist| DB

    subgraph "Dashboard (Next.js)"
        DASH[Web Dashboard]
        DASH -->|read| DB
    end
```

### Chosen Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | Next.js | Dashboard for monitoring pipeline status, viewing metrics, and managing configuration. SSR for fast initial load, React ecosystem for interactive dashboards. |
| Backend | Python (FastAPI) | Agent pipeline is Python-native — Claude API SDK, Docker SDK, and GitHub CLI integration all run in Python. FastAPI provides async HTTP endpoints for webhook ingestion and dashboard API. |
| Database | PostgreSQL | Stores ticket analysis, agent event logs, fix quality metrics, and team config. Handles relational data (tickets → fixes → reviews → PRs) and JSONB for flexible event storage. |
| Auth | GitHub OAuth | Users authenticate with GitHub accounts, which also grants pipeline access to repositories. GitHub is both identity provider and integration target. |
| Payments | Stripe | Industry standard for SaaS subscriptions. Handles team billing, usage-based pricing, and self-serve plan management. |

### Stack Integration Guide

**Setup order:**

1. **PostgreSQL** — Set up database first (local Docker for dev, managed for prod). Create the schema.
2. **FastAPI backend** — Initialize the Python project with FastAPI, connect to PostgreSQL via SQLAlchemy + asyncpg.
3. **GitHub OAuth** — Register a GitHub OAuth App, configure callback URL, store client ID/secret.
4. **Claude API** — Obtain API key from Anthropic Console, set rate limits.
5. **Docker SDK** — Install Docker Engine, configure the Python Docker SDK for sandbox management.
6. **Next.js dashboard** — Initialize frontend project, configure API proxy to FastAPI backend.
7. **Stripe** — Create products/prices in Stripe Dashboard, configure webhook endpoint.

**Integration patterns:**

- FastAPI serves both the webhook endpoint (`/api/webhooks/github`) and the dashboard API (`/api/v1/*`).
- Next.js frontend calls the FastAPI API via `NEXT_PUBLIC_API_URL` environment variable.
- GitHub OAuth flow: Next.js redirects to GitHub → GitHub redirects to FastAPI callback → FastAPI creates session → redirects to dashboard.
- Docker containers are ephemeral — created per fix attempt, destroyed after PR creation or failure.
- Claude API calls use the `anthropic` Python SDK with `ANTHROPIC_API_KEY`.

**Required environment variables:**

```
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/ticketforge

# GitHub OAuth
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
GITHUB_WEBHOOK_SECRET=xxx

# Claude API
ANTHROPIC_API_KEY=xxx

# Stripe
STRIPE_SECRET_KEY=xxx
STRIPE_WEBHOOK_SECRET=xxx
STRIPE_PRICE_ID_TEAM=xxx

# App
APP_URL=http://localhost:3000
API_URL=http://localhost:8000
JWT_SECRET=xxx
```

**Common gotchas:**

- GitHub webhook payloads can be large — set FastAPI's `max_request_size` accordingly.
- Docker SDK needs the Docker socket mounted or TCP access — configure `DOCKER_HOST` for remote Docker.
- Claude API has rate limits per organization — implement retry with exponential backoff using `tenacity`.
- PostgreSQL JSONB columns need GIN indexes for query performance on event logs.

### Repository Structure

```
ticketforge/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # Environment config (pydantic-settings)
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── ticket.py
│   │   │   ├── pipeline_run.py
│   │   │   ├── event.py
│   │   │   └── user.py
│   │   ├── api/
│   │   │   ├── webhooks.py          # GitHub webhook handler
│   │   │   ├── auth.py              # GitHub OAuth endpoints
│   │   │   ├── dashboard.py         # Dashboard API endpoints
│   │   │   └── stripe_webhooks.py   # Stripe webhook handler
│   │   ├── agents/
│   │   │   ├── base.py              # Base agent class (event stream logging)
│   │   │   ├── content_researcher.py # Ticket analysis agent
│   │   │   ├── code_act_agent.py    # Code generation agent (Docker sandbox)
│   │   │   └── code_reviewer.py     # Code review agent
│   │   ├── services/
│   │   │   ├── github_service.py    # GitHub API / gh CLI wrapper
│   │   │   ├── docker_service.py    # Docker container management
│   │   │   ├── claude_service.py    # Claude API client
│   │   │   └── event_logger.py      # Event stream persistence
│   │   └── tasks/
│   │       └── pipeline.py          # Pipeline orchestration (Celery/ARQ)
│   ├── alembic/                     # Database migrations
│   │   └── versions/
│   ├── tests/
│   │   ├── test_agents/
│   │   ├── test_api/
│   │   └── test_services/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── app/                     # Next.js App Router pages
│   │   │   ├── page.tsx             # Landing / login
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx         # Main dashboard
│   │   │   │   ├── tickets/
│   │   │   │   │   └── page.tsx     # Ticket list & status
│   │   │   │   ├── analytics/
│   │   │   │   │   └── page.tsx     # Quality metrics
│   │   │   │   └── settings/
│   │   │   │       └── page.tsx     # Repo config, labels, API keys
│   │   │   └── auth/
│   │   │       └── callback/
│   │   │           └── page.tsx     # GitHub OAuth callback
│   │   ├── components/
│   │   │   ├── ui/                  # Design system primitives
│   │   │   └── features/            # Feature-specific components
│   │   └── lib/
│   │       ├── api.ts               # API client
│   │       └── auth.ts              # Auth utilities
│   ├── public/
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── package.json
├── sandbox/
│   ├── Dockerfile.sandbox           # Base image for code execution
│   └── entrypoint.sh               # Sandbox initialization script
├── docker-compose.yml               # Local dev environment
├── .env.example
└── README.md
```

### Infrastructure & Deployment

**Backend:** Deploy FastAPI to a single VPS (DigitalOcean Droplet, $24/mo for 4GB RAM) or Railway ($5 base + usage). Docker Engine runs on the same machine for sandbox containers during pilot phase. Use Gunicorn with Uvicorn workers for production.

**Frontend:** Deploy Next.js to Vercel (free tier for hobby, $20/mo for Pro). Configure `NEXT_PUBLIC_API_URL` to point at the backend.

**Database:** Use managed PostgreSQL — Neon (free tier, generous for pilot) or Supabase Postgres ($25/mo). Alternatively, run PostgreSQL in Docker on the backend VPS.

**Task Queue:** Use ARQ (async Redis queue) for pipeline orchestration. Redis runs in Docker on the backend VPS or use Upstash Redis (free tier).

**CI/CD:** GitHub Actions for both backend (pytest, ruff lint) and frontend (TypeScript check, ESLint). Auto-deploy on merge to main.

**Monitoring:** Sentry for error tracking (free tier), basic health check endpoint at `/api/health`.

### Security Considerations

- **Webhook verification:** Validate GitHub webhook signatures using `GITHUB_WEBHOOK_SECRET` and HMAC-SHA256. Reject unverified payloads.
- **OAuth flow:** Use PKCE for GitHub OAuth. Store access tokens encrypted in PostgreSQL. Tokens scoped to `repo` and `read:user`.
- **Sandbox isolation:** Docker containers run with `--network=none` (no network access during code execution), `--memory=2g` (memory limit), `--cpus=1` (CPU limit), and `--read-only` root filesystem (writable `/tmp` only). Containers are destroyed after each run.
- **API authentication:** Dashboard API endpoints require JWT tokens issued after GitHub OAuth. Tokens expire after 24 hours with refresh via GitHub access token.
- **Secrets management:** All secrets via environment variables, never committed. `.env` in `.gitignore`.
- **Input validation:** Pydantic models validate all API inputs. SQLAlchemy parameterized queries prevent SQL injection.
- **Rate limiting:** Apply rate limits on webhook endpoint (100 req/min) and API endpoints (60 req/min per user) using `slowapi`.

### Cost Estimate

Monthly costs for pilot phase (< 5 teams, < 200 tickets/month):

| Service | Tier | Monthly Cost |
|---------|------|-------------|
| VPS (backend + Docker) | DigitalOcean 4GB Droplet | $24 |
| PostgreSQL | Neon free tier | $0 |
| Redis | Upstash free tier | $0 |
| Next.js hosting | Vercel free tier | $0 |
| Claude API | ~500 fix attempts × ~10K tokens avg | ~$75–150 |
| GitHub | Free (public repos) or Team ($4/user) | $0–16 |
| Stripe | 2.9% + $0.30 per transaction | ~$5 |
| Sentry | Free tier | $0 |
| **Total** | | **~$104–195/mo** |

Free tier limits to monitor: Neon (0.5GB storage, 3GB transfer), Upstash (10K commands/day), Vercel (100GB bandwidth).

---

## 3. Data Model

### Entity Definitions

```sql
-- Users (authenticated via GitHub OAuth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    github_id BIGINT UNIQUE NOT NULL,
    github_login VARCHAR(255) NOT NULL,
    github_access_token TEXT NOT NULL,          -- Encrypted
    email VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Teams (billing unit)
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_id UUID NOT NULL REFERENCES users(id),
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    plan VARCHAR(50) NOT NULL DEFAULT 'free',   -- 'free', 'team', 'enterprise'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Team memberships
CREATE TABLE team_members (
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member', -- 'owner', 'admin', 'member'
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (team_id, user_id)
);

-- Connected repositories
CREATE TABLE repositories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    github_repo_id BIGINT NOT NULL,
    full_name VARCHAR(255) NOT NULL,            -- e.g. "org/repo"
    webhook_id BIGINT,                          -- GitHub webhook ID
    trigger_labels JSONB DEFAULT '["bug"]',     -- Issue labels that trigger pipeline
    is_active BOOLEAN DEFAULT TRUE,
    config JSONB DEFAULT '{}',                  -- Per-repo agent config overrides
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(team_id, github_repo_id)
);

-- Tickets (GitHub Issues processed by the pipeline)
CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    github_issue_number INTEGER NOT NULL,
    github_issue_url TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    labels JSONB DEFAULT '[]',
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    -- Status: 'pending' | 'analyzing' | 'generating' | 'reviewing' | 'pr_created' | 'escalated' | 'failed'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(repository_id, github_issue_number)
);

-- Pipeline runs (one per ticket processing attempt)
CREATE TABLE pipeline_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'running',
    -- Status: 'running' | 'completed' | 'failed' | 'escalated'
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    -- Agent outputs
    analysis JSONB,                             -- Content researcher output
    fix_diff TEXT,                               -- Generated code diff
    review_result JSONB,                        -- Code review assessment
    -- PR info (if created)
    pr_number INTEGER,
    pr_url TEXT,
    pr_status VARCHAR(50),                      -- 'open' | 'merged' | 'closed'
    -- Escalation info (if escalated)
    escalation_reason TEXT,
    escalation_notes TEXT,
    -- Metrics
    tokens_used INTEGER DEFAULT 0,
    container_id VARCHAR(255),
    error_message TEXT
);

-- Event log (audit trail for every agent action)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pipeline_run_id UUID NOT NULL REFERENCES pipeline_runs(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,           -- 'content_researcher' | 'code_act_agent' | 'code_reviewer'
    event_type VARCHAR(100) NOT NULL,           -- 'action' | 'observation' | 'decision' | 'error'
    payload JSONB NOT NULL,                     -- Event-specific data
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
```

### Relationships

- **User → Team:** Many-to-many via `team_members`. A user can belong to multiple teams. Cascade: removing a user removes their team memberships.
- **Team → Repository:** One-to-many. A team connects multiple repos. Cascade: deleting a team disconnects all repos.
- **Repository → Ticket:** One-to-many. Each ticket belongs to one repo. Cascade: removing a repo removes its tickets.
- **Ticket → Pipeline Run:** One-to-many. A ticket can have multiple pipeline run attempts (retries). Cascade: removing a ticket removes its runs.
- **Pipeline Run → Event:** One-to-many. Each run has many events. Cascade: removing a run removes its events.

### Indexes

```sql
-- Fast lookup by GitHub ID (login flow)
CREATE INDEX idx_users_github_id ON users(github_id);

-- List repos for a team
CREATE INDEX idx_repositories_team_id ON repositories(team_id);

-- List tickets for a repo, ordered by recency
CREATE INDEX idx_tickets_repository_id ON tickets(repository_id, created_at DESC);

-- List tickets by status (dashboard filtering)
CREATE INDEX idx_tickets_status ON tickets(status);

-- List pipeline runs for a ticket
CREATE INDEX idx_pipeline_runs_ticket_id ON pipeline_runs(ticket_id);

-- Query events for a pipeline run, ordered chronologically
CREATE INDEX idx_events_pipeline_run_id ON events(pipeline_run_id, timestamp);

-- Query events by agent (debugging, analytics)
CREATE INDEX idx_events_agent_name ON events(agent_name);

-- GIN index on event payload for JSONB queries
CREATE INDEX idx_events_payload ON events USING GIN(payload);
```

---

## 4. API Specification

### API Design Philosophy

RESTful JSON API served by FastAPI. Authentication via JWT tokens obtained through GitHub OAuth. Standard error format:

```json
{
  "error": "error_code",
  "message": "Human-readable description",
  "details": {}
}
```

Pagination uses cursor-based pagination with `cursor` and `limit` query parameters (default limit: 50, max: 100).

### Endpoints

#### Auth

```
GET /api/auth/github
  → Redirects to GitHub OAuth authorization URL
  Response 302: Redirect to https://github.com/login/oauth/authorize

GET /api/auth/github/callback?code=xxx
  → Exchanges code for access token, creates/updates user, returns JWT
  Response 200: { token: string, user: { id, github_login, avatar_url } }
  Response 400: { error: "invalid_code" }

POST /api/auth/refresh
  Auth: Required
  → Refreshes JWT using stored GitHub access token
  Response 200: { token: string }
  Response 401: { error: "token_expired" }
```

#### Teams

```
GET /api/v1/teams
  Auth: Required
  → List teams the authenticated user belongs to
  Response 200: { teams: [{ id, name, plan, role, member_count }] }

POST /api/v1/teams
  Auth: Required
  Body: { name: string }
  Response 201: { id, name, plan: "free", owner_id }

GET /api/v1/teams/:team_id
  Auth: Required (team member)
  Response 200: { id, name, plan, owner, members: [...], repositories: [...] }
```

#### Repositories

```
GET /api/v1/teams/:team_id/repos
  Auth: Required (team member)
  Response 200: { repositories: [{ id, full_name, is_active, trigger_labels }] }

POST /api/v1/teams/:team_id/repos
  Auth: Required (team admin)
  Body: { github_repo_full_name: string, trigger_labels?: string[] }
  → Registers webhook on the GitHub repo, stores repo config
  Response 201: { id, full_name, webhook_id, trigger_labels }
  Response 400: { error: "webhook_registration_failed", message: "..." }

PATCH /api/v1/teams/:team_id/repos/:repo_id
  Auth: Required (team admin)
  Body: { trigger_labels?: string[], is_active?: boolean, config?: object }
  Response 200: { id, full_name, trigger_labels, is_active, config }

DELETE /api/v1/teams/:team_id/repos/:repo_id
  Auth: Required (team admin)
  → Removes webhook from GitHub, deletes repo record
  Response 204: No content
```

#### Tickets & Pipeline

```
GET /api/v1/teams/:team_id/tickets
  Auth: Required (team member)
  Query: status?, repo_id?, cursor?, limit?
  Response 200: { tickets: [{ id, repo_full_name, issue_number, title, status, created_at, latest_run }], next_cursor }

GET /api/v1/teams/:team_id/tickets/:ticket_id
  Auth: Required (team member)
  Response 200: { ticket: { ...full ticket data }, pipeline_runs: [{ id, status, started_at, duration, pr_url, escalation_reason }] }

GET /api/v1/teams/:team_id/tickets/:ticket_id/runs/:run_id/events
  Auth: Required (team member)
  Query: cursor?, limit?
  Response 200: { events: [{ id, agent_name, event_type, payload, timestamp }], next_cursor }

POST /api/v1/teams/:team_id/tickets/:ticket_id/retry
  Auth: Required (team admin)
  → Creates a new pipeline run for the ticket
  Response 201: { pipeline_run_id, status: "running" }
```

#### Analytics

```
GET /api/v1/teams/:team_id/analytics
  Auth: Required (team member)
  Query: period? (7d|30d|90d)
  Response 200: {
    tickets_processed: number,
    prs_created: number,
    prs_merged: number,
    escalations: number,
    acceptance_rate: number,          # percentage
    avg_fix_time_seconds: number,
    tokens_used: number,
    estimated_hours_saved: number
  }
```

#### Webhooks (GitHub → TicketForge)

```
POST /api/webhooks/github
  Headers: X-Hub-Signature-256, X-GitHub-Event
  Body: GitHub webhook payload
  → Validates signature, filters by event type (issues.opened, issues.labeled),
    checks label match, creates ticket and enqueues pipeline run
  Response 200: { received: true }
  Response 401: { error: "invalid_signature" }
```

#### Webhooks (Stripe → TicketForge)

```
POST /api/webhooks/stripe
  Headers: Stripe-Signature
  Body: Stripe event payload
  → Handles: checkout.session.completed, customer.subscription.updated,
    customer.subscription.deleted
  Response 200: { received: true }
```

---

## 5. User Stories

### Epic: Ticket Processing Pipeline

**US-001: Automatic bug ticket intake**
As Alex (Tech Lead), I want TicketForge to automatically pick up new bug issues from my repo so that routine bugs enter the pipeline without manual assignment.

Acceptance Criteria:
- [ ] Given a new issue is created with the `bug` label, when the webhook fires, then a ticket record is created and a pipeline run is enqueued within 5 seconds.
- [ ] Given a new issue is created without a configured trigger label, when the webhook fires, then the issue is ignored and no ticket is created.
- [ ] Edge case: duplicate webhook delivery → idempotent handling, no duplicate tickets.

**US-002: Automated ticket analysis**
As Alex, I want the system to analyze the bug ticket and extract structured information so that subsequent agents have clean input to work with.

Acceptance Criteria:
- [ ] Given a ticket enters the pipeline, when the content-researcher agent runs, then it produces a structured analysis with: problem statement, affected files (if mentioned), reproduction steps, and severity estimate.
- [ ] Given a ticket with minimal information (just a title, no body), when analysis runs, then the agent flags it as low-confidence and escalates.
- [ ] Edge case: issue body contains images/screenshots → agent notes them but doesn't analyze image content in MVP.

**US-003: Sandboxed code fix generation**
As Alex, I want the system to generate a fix in an isolated environment so that no production systems are affected and the fix can be validated against the test suite.

Acceptance Criteria:
- [ ] Given a valid ticket analysis, when the CodeActAgent runs, then a Docker container is created with the repo cloned, the fix is generated, and existing tests are executed.
- [ ] Given the fix causes test failures, when the agent detects failures, then it iterates up to 3 times to fix test failures before escalating.
- [ ] Given the container exceeds 5-minute timeout, when the timeout fires, then the container is destroyed and the ticket is escalated.
- [ ] Edge case: repo requires specific language runtime versions → base sandbox image includes Python 3.11+, Node 20+, and common build tools.

**US-004: Automated code review**
As Alex, I want generated fixes to be reviewed before a PR is created so that I can trust the quality of agent-generated code.

Acceptance Criteria:
- [ ] Given a fix is generated, when the code-review-specialist runs, then it checks: code style consistency, test coverage (new tests exist for the fix), regression risk, and security patterns.
- [ ] Given the review identifies critical issues, when the review concludes, then the fix is rejected and the ticket is escalated with review notes.
- [ ] Given the review passes, when the review concludes, then the pipeline proceeds to PR creation.

**US-005: PR creation with context**
As Alex, I want the PR to contain a clear description linking to the original issue so that I can review it efficiently.

Acceptance Criteria:
- [ ] Given a fix passes review, when the PR is created, then it includes: the fix diff, any test changes, a description with "Fixes #[issue_number]", and the review summary.
- [ ] Given the PR is created, when I view it on GitHub, then it looks like any well-written human PR with a clear title and body.

**US-006: Escalation with analysis**
As Alex, I want failed pipeline runs to leave useful notes on the issue so that the developer who picks it up starts with context.

Acceptance Criteria:
- [ ] Given any agent fails or reports low confidence, when escalation occurs, then a comment is posted on the GitHub Issue with: which agent failed, why, and any partial analysis or findings.
- [ ] Given an escalation, when I view the issue, then the comment is clearly labeled as from TicketForge and includes structured analysis notes.

### Epic: Dashboard & Monitoring

**US-007: Pipeline status dashboard**
As Jordan (Engineering Manager), I want to see the current status of all ticket processing so that I know what's being handled automatically vs. what needs human attention.

Acceptance Criteria:
- [ ] Given I open the dashboard, when the page loads, then I see: tickets in progress, PRs created today, escalations, and a recent activity feed.
- [ ] Given a pipeline run completes, when I'm viewing the dashboard, then the status updates within 10 seconds.

**US-008: Quality analytics**
As Jordan, I want to see fix quality metrics over time so that I can justify continued investment and expansion.

Acceptance Criteria:
- [ ] Given I navigate to analytics, when the page loads, then I see: acceptance rate, MTTR, escalation rate, estimated hours saved, and token usage.
- [ ] Given I select a time period (7d/30d/90d), when I change the filter, then all metrics update to reflect the selected period.

### Epic: Repository Configuration

**US-009: Connect a GitHub repository**
As Alex, I want to connect my team's repos to TicketForge so that bug tickets are automatically processed.

Acceptance Criteria:
- [ ] Given I'm authenticated, when I add a repo, then a webhook is registered on the GitHub repo and the repo appears in my dashboard.
- [ ] Given I configure trigger labels, when an issue with a matching label is created, then the pipeline starts.
- [ ] Edge case: webhook registration fails (insufficient permissions) → clear error message with required permissions listed.

**US-010: GitHub OAuth login**
As Alex, I want to log in with my GitHub account so that TicketForge can access my repositories.

Acceptance Criteria:
- [ ] Given I click "Sign in with GitHub", when the OAuth flow completes, then I'm authenticated and redirected to the dashboard.
- [ ] Given my GitHub token expires, when I make an API call, then the token is refreshed automatically.

---

## 6. Functional Requirements

### Pipeline Core

**FR-001: GitHub Webhook Receiver**
Priority: P0
Description: HTTP endpoint that receives GitHub webhook events, validates the HMAC-SHA256 signature, filters for `issues.opened` and `issues.labeled` events, matches against configured trigger labels, and creates a ticket + pipeline run record.
Acceptance Criteria:
- Validates webhook signature using `GITHUB_WEBHOOK_SECRET`
- Handles `issues.opened` and `issues.labeled` event types
- Ignores events that don't match configured trigger labels
- Idempotent — duplicate deliveries don't create duplicate tickets
- Responds within 5 seconds (enqueues async processing)
Related Stories: US-001

**FR-002: Content Researcher Agent**
Priority: P0
Description: Analyzes a GitHub Issue body using Claude API to extract structured information: problem statement, affected files, reproduction steps, severity estimate, and confidence score. Uses Claude Sonnet for cost efficiency.
Acceptance Criteria:
- Outputs structured JSON with all required fields
- Confidence score between 0.0 and 1.0
- Tickets with confidence < 0.4 are escalated immediately
- Handles issues with minimal content (title only) gracefully
- Logs all actions to event stream
Related Stories: US-002

**FR-003: CodeActAgent Sandbox**
Priority: P0
Description: Manages Docker containers for code generation. For each fix attempt: creates a container from the base sandbox image, clones the target repo, runs the Claude-powered code generation loop (read files → generate fix → run tests → iterate), and extracts the final diff.
Acceptance Criteria:
- Container runs with `--network=none`, `--memory=2g`, `--cpus=1`
- Container timeout: 5 minutes (configurable)
- Up to 3 iteration cycles (generate → test → fix failures)
- Extracts clean `git diff` as the fix output
- Destroys container on completion or timeout
- Logs all actions to event stream
Related Stories: US-003

**FR-004: Code Review Specialist Agent**
Priority: P0
Description: Reviews the generated diff using Claude API. Checks: code style consistency with the existing codebase, test coverage (new tests added), regression risk assessment, security pattern check (no hardcoded secrets, no SQL injection, no XSS). Outputs approve/reject/escalate recommendation.
Acceptance Criteria:
- Reviews diff against at least 4 quality dimensions (style, tests, regression, security)
- Outputs structured review with per-dimension assessment
- Rejects fixes with critical security issues
- Escalates fixes with medium confidence (score 0.4–0.6)
- Approves fixes with high confidence (score > 0.6) and no critical issues
- Logs all actions to event stream
Related Stories: US-004

**FR-005: PR Creator**
Priority: P0
Description: Creates a GitHub Pull Request using `gh pr create` via the authenticated user's GitHub token. PR includes: fix branch, commit with descriptive message, PR body with issue link ("Fixes #N"), review summary, and TicketForge attribution.
Acceptance Criteria:
- Creates a branch named `ticketforge/fix-{issue_number}`
- Commit message follows conventional commit format
- PR body includes: fix summary, files changed, test changes, review assessment, and "Fixes #{issue_number}"
- PR is assigned to the repository's configured reviewers (if any)
Related Stories: US-005

**FR-006: Escalation Handler**
Priority: P0
Description: When any agent fails or reports low confidence, posts a structured comment on the GitHub Issue with: which step failed, why, and any partial analysis. Updates the ticket status to `escalated`.
Acceptance Criteria:
- Comment is clearly labeled as from TicketForge
- Includes the failing agent name and specific reason
- Includes any partial analysis that was completed before failure
- Comment is formatted in readable markdown
Related Stories: US-006

**FR-007: Event Stream Logger**
Priority: P0
Description: Persists every agent action, observation, and decision to the `events` table in PostgreSQL. Each event includes: pipeline run ID, agent name, event type, payload (JSONB), and timestamp.
Acceptance Criteria:
- All agent actions are logged before execution (intent) and after (result)
- Events are queryable by pipeline run, agent, and time range
- JSONB payload supports arbitrary event-specific data
- Write performance: < 10ms per event
Related Stories: US-001 through US-006

### Dashboard

**FR-008: Pipeline Status View**
Priority: P0
Description: Web dashboard page showing: active pipeline runs, recent completed runs, tickets by status, and a real-time activity feed.
Acceptance Criteria:
- Shows counts by status: pending, analyzing, generating, reviewing, pr_created, escalated, failed
- Activity feed shows last 50 events with timestamps
- Refreshes automatically every 10 seconds (polling) or via SSE
Related Stories: US-007

**FR-009: Analytics View**
Priority: P1
Description: Dashboard page showing quality metrics: acceptance rate, MTTR, escalation rate, hours saved, token usage. Filterable by time period (7d/30d/90d).
Acceptance Criteria:
- Calculates all metrics from pipeline run data
- Period filter updates all metrics
- Hours saved = (accepted PRs × average manual fix time) where average manual fix time defaults to 2 hours
Related Stories: US-008

### Auth & Configuration

**FR-010: GitHub OAuth Flow**
Priority: P0
Description: Full GitHub OAuth 2.0 flow with PKCE. Creates user record on first login, issues JWT for API authentication.
Acceptance Criteria:
- Redirects to GitHub authorization URL with `repo` and `read:user` scopes
- Exchanges code for access token
- Creates or updates user record
- Issues JWT with 24-hour expiry
- Stores GitHub access token encrypted in database
Related Stories: US-010

**FR-011: Repository Connection**
Priority: P0
Description: Allows users to connect a GitHub repository by registering a webhook. Configurable trigger labels.
Acceptance Criteria:
- Lists user's accessible repos from GitHub API
- Registers a webhook on the selected repo
- Stores trigger labels (default: `["bug"]`)
- Validates that the user has admin access to the repo
Related Stories: US-009

**FR-012: Stripe Subscription Management**
Priority: P1
Description: Handles team billing via Stripe. Free tier: 10 tickets/month. Team tier: unlimited tickets.
Acceptance Criteria:
- Creates Stripe checkout session for plan upgrade
- Handles `checkout.session.completed` webhook to activate plan
- Handles `customer.subscription.deleted` to downgrade to free
- Enforces ticket limit on free tier (rejects pipeline runs over limit)
Related Stories: N/A

---

## 7. Non-Functional Requirements

### Performance

- Webhook response time: < 5 seconds (async processing enqueued)
- Pipeline completion time: < 30 minutes for single-service bugs
- Docker container spin-up: < 60 seconds (pre-pulled base image)
- Dashboard page load: < 2 seconds (LCP)
- API response time: < 200ms (p95) for read endpoints
- Event stream write latency: < 10ms per event

### Security

- GitHub webhook signature validation (HMAC-SHA256) on every request
- Docker sandbox: `--network=none`, `--memory=2g`, `--cpus=1`, `--read-only` root filesystem
- All secrets via environment variables, never in code
- GitHub access tokens encrypted at rest (AES-256)
- JWT tokens expire after 24 hours
- Rate limiting: 100 req/min on webhook endpoint, 60 req/min per user on API
- OWASP Top 10 addressed: input validation (Pydantic), parameterized queries (SQLAlchemy), CSRF protection, XSS prevention (React default escaping)

### Accessibility

- Dashboard meets WCAG 2.1 AA
- All interactive elements keyboard navigable
- Color contrast ratio ≥ 4.5:1
- Screen reader compatible (semantic HTML, ARIA labels)

### Scalability

- MVP supports 5 teams, 200 tickets/month on a single VPS
- Database can handle 100K events without degradation (GIN indexes on JSONB)
- Pipeline runs can be parallelized up to `max_concurrent_containers` (default: 3)

### Reliability

- 99.5% uptime target for webhook endpoint (GitHub retries on failure)
- Graceful degradation: if Claude API is down, tickets queue for later processing
- Pipeline runs have automatic retry on transient failures (network, Docker errors)
- Health check endpoint at `/api/health` for monitoring

---

## 8. UI/UX Requirements

**Design system defined in [`docs/design.md`](design.md).** All visual implementation must reference the token spec in that file. Key decisions:

- **Dark mode primary.** Surface hierarchy: `surface` (#0F1117) → `surface-raised` (#161B22) → `surface-overlay` (#1C2128). No shadows — depth via border and contrast only.
- **Typography:** Inter for UI, JetBrains Mono for all agent output and code references. Body text at 0.875rem (14px).
- **Interactive color:** Primary blue (#2F81F7) is reserved exclusively for clickable/interactive elements. One primary button per view maximum.
- **Status badges:** Fully rounded pills with semantic color pairings — green (success/merged), red (error/failed), amber (warning/review-needed), blue (info/in-progress).
- **Component height:** Buttons and inputs are 36px tall. Cards use 16px internal padding with 8px border-radius.
- **Event stream:** Monospace typography, no rounding, stacked as a continuous log — the signature transparency component.

### Screen: Login

Route: `/`
Purpose: Authenticate with GitHub to access the dashboard.
Layout: Centered card on a minimal background. GitHub logo + "Sign in with GitHub" button.

States:
- **Default:** Sign-in button visible.
- **Loading:** Button shows spinner after click while OAuth redirect processes.
- **Error:** Error banner if OAuth callback fails (e.g., "GitHub authorization failed. Please try again.").

Key Interactions:
- Click "Sign in with GitHub" → redirect to GitHub OAuth → callback → redirect to `/dashboard`.

### Screen: Dashboard (Main)

Route: `/dashboard`
Purpose: Overview of pipeline status and recent activity.
Layout: Top nav (team selector, user avatar, settings link). Main content: status summary cards (top), activity feed (center), quick actions (right sidebar).

States:
- **Empty:** "No repositories connected yet. Connect your first repo to get started." with a CTA button.
- **Loading:** Skeleton cards for status summary, skeleton list for activity feed.
- **Populated:** Status cards showing ticket counts by status. Activity feed showing recent pipeline events with timestamps. Quick action: "Connect Repository" button.
- **Error:** Error banner if API call fails, with retry button.

Key Interactions:
- Click a status card → navigates to tickets list filtered by that status.
- Click an activity feed item → navigates to the ticket detail view.
- Click "Connect Repository" → opens repo connection flow.

### Screen: Tickets List

Route: `/dashboard/tickets`
Purpose: Browse and filter all processed tickets.
Layout: Filter bar (status dropdown, repo dropdown, date range). Table view with columns: Issue #, Title, Repo, Status, Time, PR link.

States:
- **Empty:** "No tickets processed yet. Bug issues with your configured labels will appear here automatically."
- **Loading:** Skeleton table rows.
- **Populated:** Sortable, filterable table with pagination.
- **Error:** Error banner with retry.

Key Interactions:
- Click a ticket row → navigates to ticket detail with pipeline run history and event log.
- Click PR link → opens GitHub PR in new tab.
- Filter by status/repo → table updates.

### Screen: Ticket Detail

Route: `/dashboard/tickets/:id`
Purpose: View full pipeline run history and event stream for a ticket.
Layout: Header with issue title + link to GitHub. Tabs: "Pipeline Runs" (list of attempts), "Event Log" (chronological agent actions).

States:
- **Running:** Live event log with updates. Status badge shows "In Progress" with elapsed time.
- **Completed:** Full event log with final status (PR created or escalated). Link to PR if created.
- **Failed/Escalated:** Event log showing where failure occurred. Escalation reason highlighted. "Retry" button.

Key Interactions:
- Click "Retry" → creates a new pipeline run for this ticket.
- Click an event → expands to show full payload (collapsible JSON viewer).
- Click "View PR" → opens GitHub PR in new tab.

### Screen: Analytics

Route: `/dashboard/analytics`
Purpose: View quality metrics and time savings.
Layout: Period selector (7d/30d/90d) at top. Metric cards (acceptance rate, MTTR, escalation rate, hours saved). Charts: tickets over time (bar), acceptance rate trend (line).

States:
- **Empty:** "Not enough data yet. Metrics will appear after processing 10+ tickets."
- **Loading:** Skeleton cards and chart placeholders.
- **Populated:** Metric cards with current values and trend indicators (↑/↓). Charts with data.

Key Interactions:
- Change period selector → all metrics and charts update.
- Hover on chart data points → tooltip with exact values.

### Screen: Settings

Route: `/dashboard/settings`
Purpose: Manage connected repos, trigger labels, and team settings.
Layout: Tabs: "Repositories", "Team", "Billing".

States:
- **Repositories tab:** List of connected repos with toggle (active/inactive), label editor, and delete button. "Add Repository" button.
- **Team tab:** Team name, member list with roles, invite link.
- **Billing tab:** Current plan, usage (tickets this month / limit), upgrade button (Stripe checkout).

Key Interactions:
- Toggle repo active/inactive → PATCH API call, immediate visual update.
- Edit trigger labels → inline editor with save button.
- Click "Add Repository" → dropdown of accessible GitHub repos → select → webhook registration.
- Click "Upgrade" → Stripe Checkout redirect.

---

## 9. Auth Implementation

### Auth Flow

1. User clicks "Sign in with GitHub" on the login page.
2. Frontend redirects to `GET /api/auth/github`.
3. Backend redirects to GitHub OAuth authorization URL with scopes: `repo`, `read:user`.
4. User authorizes on GitHub.
5. GitHub redirects to `GET /api/auth/github/callback?code=xxx`.
6. Backend exchanges `code` for GitHub access token via `POST https://github.com/login/oauth/access_token`.
7. Backend fetches user info via `GET https://api.github.com/user`.
8. Backend creates or updates user record in PostgreSQL.
9. Backend issues JWT (signed with `JWT_SECRET`, 24-hour expiry) containing: `user_id`, `github_login`, `exp`.
10. Backend redirects to `{APP_URL}/dashboard?token=xxx`.
11. Frontend stores JWT in `httpOnly` cookie (set by backend) or `localStorage`.

### Provider Configuration

Register a GitHub OAuth App at `https://github.com/settings/developers`:
- Application name: "TicketForge"
- Homepage URL: `{APP_URL}`
- Authorization callback URL: `{API_URL}/api/auth/github/callback`

Store `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in environment variables.

### Protected Routes

All `/api/v1/*` endpoints require a valid JWT in the `Authorization: Bearer <token>` header. Implement a FastAPI dependency:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    payload = verify_jwt(credentials.credentials)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")
    user = await get_user_by_id(payload["user_id"])
    if not user:
        raise HTTPException(401, "User not found")
    return user
```

Frontend Next.js middleware checks for the JWT cookie and redirects unauthenticated users to `/`.

### User Session Management

- JWT tokens expire after 24 hours.
- On API 401 response, frontend redirects to login page.
- GitHub access tokens are stored encrypted in PostgreSQL and used for GitHub API calls on behalf of the user.
- Token refresh: `POST /api/auth/refresh` verifies the stored GitHub token is still valid and issues a new JWT.

### Role-Based Access

- **Owner:** Full access. Can delete team, manage billing, add/remove members.
- **Admin:** Can add/remove repos, configure trigger labels, retry pipeline runs.
- **Member:** Read-only access to dashboard, tickets, and analytics.

Implemented via the `team_members.role` field, checked in FastAPI dependencies per endpoint.

---

## 10. Payment Integration

### Payment Flow

1. User clicks "Upgrade to Team" on the billing settings page.
2. Frontend calls `POST /api/v1/teams/:team_id/billing/checkout`.
3. Backend creates a Stripe Checkout Session with the team's plan price.
4. Frontend redirects to Stripe Checkout.
5. User completes payment on Stripe.
6. Stripe sends `checkout.session.completed` webhook to `POST /api/webhooks/stripe`.
7. Backend updates team plan to "team" and stores `stripe_subscription_id`.
8. User is redirected back to settings page showing the active plan.

### Provider Setup

1. Create a Stripe account at `https://dashboard.stripe.com`.
2. Create a Product: "TicketForge Team" with a recurring price (e.g., $49/team/month).
3. Store the `STRIPE_PRICE_ID_TEAM` in environment variables.
4. Configure the webhook endpoint at `{API_URL}/api/webhooks/stripe` for events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`.
5. Store `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` in environment variables.

### Pricing Model Implementation

| Plan | Price | Ticket Limit | Features |
|------|-------|-------------|----------|
| Free | $0 | 10 tickets/month | Pipeline processing, basic dashboard |
| Team | $49/team/month | Unlimited | Analytics, priority queue, team management |

Ticket limit enforcement: before enqueuing a pipeline run, check `COUNT(tickets WHERE team_id = X AND created_at > start_of_month) < limit`.

### Webhook Handling

```python
@app.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        team_id = session["metadata"]["team_id"]
        await update_team_plan(team_id, "team", session["subscription"])
    
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        team = await get_team_by_subscription(subscription["id"])
        await update_team_plan(team.id, "free", None)
    
    return {"received": True}
```

### Subscription Management

- Billing portal: redirect users to Stripe Customer Portal for self-serve plan changes, cancellation, and invoice history via `stripe.billing_portal.Session.create()`.
- Grace period: on subscription deletion, team retains "team" access for remaining billing period.
- Downgrade: when reverting to free, pipeline runs in progress complete, but new runs are subject to the 10 ticket/month limit.

---

## 11. Edge Cases & Error Handling

### Feature: Webhook Processing

| Scenario | Expected Behavior | Priority |
|----------|-------------------|----------|
| Invalid webhook signature | Return 401, log attempt, don't create ticket | P0 |
| Duplicate webhook delivery | Idempotent — check `(repo_id, issue_number)` unique constraint, skip if exists | P0 |
| Issue lacks trigger label | Ignore silently, return 200 | P0 |
| GitHub API rate limit during webhook processing | Queue for retry with exponential backoff (1m, 5m, 15m) | P1 |
| Webhook endpoint is down | GitHub retries (up to 3 times). Pipeline processes when back up | P1 |

### Feature: Pipeline Execution

| Scenario | Expected Behavior | Priority |
|----------|-------------------|----------|
| Docker daemon unavailable | Log error, set ticket to "failed", alert via Sentry | P0 |
| Container timeout (> 5 min) | Destroy container, escalate with "timeout" reason and partial analysis | P0 |
| Claude API rate limit | Retry with exponential backoff (30s, 60s, 120s). After 3 retries, escalate | P0 |
| Claude API down entirely | Queue ticket for later processing, set status to "pending" | P1 |
| Repo clone fails (private repo, permissions) | Escalate with "repo access failed" message, suggest checking OAuth token scope | P0 |
| Repo is very large (> 5GB) | Use shallow clone (`--depth 1`), limit to relevant directories based on analysis | P1 |
| Test suite fails with pre-existing failures | Agent compares test results before and after fix — only new failures count | P1 |
| Generated fix is empty diff | Escalate with "no changes generated" and analysis of what was attempted | P0 |

### Feature: PR Creation

| Scenario | Expected Behavior | Priority |
|----------|-------------------|----------|
| Branch name conflict | Append timestamp to branch name: `ticketforge/fix-{issue}-{ts}` | P1 |
| User lacks push access | Escalate with "push permission denied" message | P0 |
| PR creation fails (API error) | Retry once. If fails again, save the diff locally and escalate with the diff attached | P0 |
| Target branch has been updated since clone | Rebase attempt. If conflicts, escalate with "merge conflicts detected" | P1 |

### Feature: Dashboard

| Scenario | Expected Behavior | Priority |
|----------|-------------------|----------|
| API returns 500 | Show error banner: "Failed to load data. Retrying..." with auto-retry after 5s | P1 |
| WebSocket/SSE disconnects | Fallback to polling every 10 seconds | P1 |
| User's JWT expires during session | Redirect to login page with "Session expired" message | P0 |
| No data for analytics period | Show "Not enough data" message instead of empty charts | P1 |

### Feature: Auth

| Scenario | Expected Behavior | Priority |
|----------|-------------------|----------|
| GitHub OAuth callback with invalid code | Show error page: "Authorization failed. Please try again." | P0 |
| GitHub access token revoked | On next API call using token, detect 401 from GitHub, invalidate session, redirect to login | P0 |
| User removed from GitHub org | Continue processing tickets for repos they still have access to. Fail gracefully for removed repos. | P1 |

---

## 12. Dependencies & Integrations

### Core Dependencies (Python Backend)

```
fastapi
uvicorn[standard]
gunicorn
sqlalchemy[asyncio]
asyncpg
alembic
anthropic                    # Claude API SDK
docker                       # Docker SDK for Python
pydantic
pydantic-settings
python-jose[cryptography]    # JWT handling
httpx                        # Async HTTP client (GitHub API)
stripe
celery or arq                # Task queue (pick one)
redis                        # Queue backend
tenacity                     # Retry logic
slowapi                      # Rate limiting
sentry-sdk[fastapi]
cryptography                 # Token encryption
```

### Core Dependencies (Next.js Frontend)

```json
{
  "next": "latest",
  "react": "latest",
  "react-dom": "latest",
  "tailwindcss": "latest",
  "@tailwindcss/postcss": "latest",
  "recharts": "latest",
  "date-fns": "latest",
  "lucide-react": "latest"
}
```

### Development Dependencies

```json
{
  "typescript": "latest",
  "eslint": "latest",
  "@types/react": "latest",
  "@types/node": "latest"
}
```

Python dev dependencies:
```
pytest
pytest-asyncio
httpx                        # For TestClient
ruff                         # Linting + formatting
mypy
```

### Third-Party Services

| Service | Purpose | Pricing | API Key Required | Rate Limits |
|---------|---------|---------|-----------------|-------------|
| GitHub API | Webhooks, PR creation, repo access | Free (5000 req/hr with auth) | OAuth token | 5000 req/hr |
| Claude API (Anthropic) | Ticket analysis, code generation, code review | $3/$15 per 1M tokens (Sonnet), $15/$75 (Opus) | API key | Org-level limits |
| Docker Engine | Sandbox container management | Free (self-hosted) | N/A | Local resource limits |
| Stripe | Payment processing | 2.9% + $0.30 per transaction | Secret key | 100 req/s |
| Sentry | Error tracking | Free tier (5K events/mo) | DSN | N/A |

---

## 13. Out of Scope

| Feature | Why Excluded | Revisit When |
|---------|-------------|-------------|
| Multi-repo / multi-service fixes | Requires cross-repo context, significantly increases complexity | After single-repo accuracy > 80%, ~3 months |
| Custom model fine-tuning | Needs data collection infrastructure and training pipeline | After processing 1,000+ tickets, ~6 months |
| Auto-merge capability | Requires demonstrated accuracy > 95% to maintain trust | After 6 months of quality data |
| IDE integration | Core value is CI/CD-level automation, not IDE productivity | Based on user feedback |
| Non-GitHub platforms (GitLab, Bitbucket) | GitHub has largest market share and best CLI tooling | After 20 paying teams |
| Custom agent definitions | AgentDefinition schema exists architecturally but ships with fixed configs | After validating default pipeline |
| Mobile app | Dashboard is web-only in MVP | Based on demand |
| Real-time collaboration (multiple users viewing same ticket) | Adds WebSocket complexity without core value | Post-MVP if requested |

---

## 14. Open Questions

**Q1: Task queue — Celery vs ARQ?**
Options: Celery (mature, battle-tested, synchronous API) vs ARQ (async-native, lighter weight, Python-only).
Tradeoffs: Celery has broader ecosystem but heavier footprint. ARQ is async-native (matches FastAPI) but less proven at scale.
Recommended default: **ARQ** — lighter, async-native, sufficient for MVP scale. Migrate to Celery if scaling requires it.

**Q2: Claude model selection per agent?**
Options: Use Sonnet for all agents (cheaper) vs Opus for code generation only (higher quality fixes).
Tradeoffs: Opus costs 5x more but produces higher quality code. Sonnet is sufficient for ticket analysis and review.
Recommended default: **Sonnet for content-researcher and code-review-specialist, Opus for CodeActAgent.** Monitor fix quality and adjust.

**Q3: Sandbox base image — generic or per-language?**
Options: Single base image with Python/Node/common tools vs separate images per language.
Tradeoffs: Single image is simpler but larger. Per-language images are smaller but require build pipeline.
Recommended default: **Single base image** for MVP. Include Python 3.11+, Node 20+, Go 1.22+, and common build tools. Optimize later.

**Q4: Event stream delivery to dashboard — polling vs SSE vs WebSocket?**
Options: Polling (simplest), SSE (server-push, one-way), WebSocket (bidirectional).
Tradeoffs: Polling adds latency (10s). SSE is simpler than WebSocket and sufficient for one-way updates. WebSocket is overkill for read-only updates.
Recommended default: **SSE** for real-time event feed, with polling fallback for browsers that don't support SSE.

**Q5: How to handle monorepos with multiple services?**
Options: Treat each service directory as a separate "repo" context vs attempt to understand the full monorepo.
Tradeoffs: Isolating to a service directory limits fix scope but improves accuracy. Full monorepo context risks exceeding context windows.
Recommended default: **Defer to out-of-scope.** MVP handles single-service repos. Monorepo support requires path-based routing logic.
