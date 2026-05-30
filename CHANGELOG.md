# Changelog

All notable changes to TicketForge are documented here.

## [0.1.0] - 2026-05-30

### Added

**Pipeline Core**
- Content Researcher agent — analyzes GitHub Issues, extracts problem statement, affected files, reproduction steps, severity
- CodeAct Agent — generates fixes in Docker sandboxes with iterative test-fix loops (up to 3 iterations)
- Code Reviewer agent — 4-dimension review (style, tests, regression, security) with configurable criteria per repo
- PR Creator agent — creates branches, pushes fixes, opens PRs with structured descriptions
- Escalation Handler — posts analysis notes on GitHub Issues when pipeline confidence is low, with optional Slack notifications
- Full event stream logging — every agent action, observation, and decision stored in PostgreSQL JSONB

**Dashboard**
- Real-time pipeline status with auto-refresh
- Ticket list with status filtering and cursor-based pagination
- Ticket detail view with pipeline run selector and expandable event log
- Analytics page with 8 metric cards, pipeline outcome bars, and efficiency summary
- Period selector (7d / 30d / 90d) and CSV/JSON export
- Settings page with repository management and billing section
- Landing page with hero, features, how-it-works, and GitHub OAuth CTA

**Infrastructure**
- GitHub webhook handler with HMAC-SHA256 signature verification
- GitHub OAuth authentication with JWT tokens (24h expiry)
- ARQ task queue for async pipeline execution
- Docker sandbox service with --network=none, 2GB memory, 1 CPU limits
- Rate limiting via slowapi (60/min user, 100/min webhooks)
- Global error handlers with consistent {error, message, details} format
- AES-256 encryption for GitHub access tokens at rest
- Sentry integration (backend + frontend)

**Billing**
- Stripe checkout session creation and subscription lifecycle webhooks
- Plan-based ticket limits (free: 20/mo, team: 500/mo, enterprise: 10K/mo)
- Usage tracking with monthly reset
- Billing settings UI with usage meter and upgrade flow

**Quality & Operations**
- Configurable review criteria per repository (min_confidence, require_tests, security_check)
- PR quality tracking — webhook handler for pull_request.closed events (merged/rejected)
- Ticket priority queue based on issue labels (critical > high > medium > low)
- Pipeline resilience — pre-existing test baseline, clone failure handling, API downtime retry
- Cost tracking service with per-run cost estimation and ROI calculation
- Team member management (invite, remove, change role)

**DevOps**
- CI/CD workflows for backend (ruff + mypy + pytest) and frontend (eslint + tsc + build)
- Production docker-compose with Gunicorn, ARQ worker, and Caddy SSL
- Deploy script for VPS deployment
- Locust load test scenarios
- Input validation with Pydantic across all API endpoints
- Accessibility improvements (ARIA labels, semantic nav, keyboard support)
- SEO meta tags (OG, Twitter cards)
