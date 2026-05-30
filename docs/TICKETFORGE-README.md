# TicketForge

**From ticket to PR. Automatically.**

TicketForge turns GitHub Issues into tested, reviewed pull requests using a multi-agent AI pipeline. Label a bug, get a PR.

```
Bug ticket lands → AI analyzes → Fix generated in sandbox → Code reviewed → PR created
```

## How it works

1. **Label an issue** — add your trigger label (e.g. `bug`) to any GitHub issue
2. **AI analyzes** — Content Researcher extracts the problem, affected files, and reproduction steps
3. **Code generated** — CodeAct Agent writes and tests a fix in an isolated Docker container (`--network=none`)
4. **Code reviewed** — Reviewer checks style, tests, regression risk, and security before approving
5. **PR created** — a clean PR appears on your repo with the fix, tests, and review summary

When confidence is low, TicketForge escalates to a human developer with analysis notes. It never force-merges. You always approve.

## Quick start

```bash
cp .env.example .env
# Add your GitHub OAuth, Anthropic API key, etc.

docker-compose up -d
open http://localhost:3000
```

Sign in with GitHub, connect a repository, and configure which issue labels trigger the pipeline.

## Architecture

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Pipeline agents | Python, Claude API | Analyze tickets, generate fixes, review code |
| Sandbox | Docker (--network=none) | Isolated code execution |
| Backend | FastAPI, SQLAlchemy, PostgreSQL | API, data, event stream |
| Task queue | ARQ, Redis | Async pipeline execution |
| Frontend | Next.js 14, TypeScript, Tailwind | Dashboard and settings |
| Auth | GitHub OAuth + JWT | Identity and repo access |
| Payments | Stripe | Subscription billing |

### Agent pipeline

```
Content Researcher (Sonnet) → CodeAct Agent (Opus) → Code Reviewer (Sonnet) → PR Creator
         ↓ escalate                ↓ escalate              ↓ reject
    Escalation Handler        Escalation Handler      Escalation Handler
```

Every agent logs actions, observations, and decisions to a PostgreSQL event stream. Full audit trail for every fix.

## Configuration

Set trigger labels per repository in the dashboard Settings page. Default: `bug`.

Configure review criteria per repo:

```json
{
  "review": {
    "require_tests": true,
    "security_check": true,
    "min_confidence": 0.6
  },
  "slack_webhook_url": "https://hooks.slack.com/services/..."
}
```

See [CONFIGURATION.md](docs/CONFIGURATION.md) for all environment variables and options.

## Plans

| Plan | Tickets/month | Features |
|------|--------------|----------|
| Free | 20 | Pipeline, dashboard, event log |
| Team | 500 | + Analytics, export, team management, priority queue |
| Enterprise | 10,000 | + Custom review criteria, SLA, dedicated support |

## Development

```bash
# Backend
cd backend && pip install -e ".[dev]"
ruff check .        # lint
mypy app/           # type check
pytest -q           # test
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install
npm run lint
npm run dev
```

## Docs

- [Deployment Guide](docs/DEPLOYMENT.md)
- [Configuration Reference](docs/CONFIGURATION.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Built with

- [Claude](https://anthropic.com) (Sonnet for analysis/review, Opus for code generation)
- [FastAPI](https://fastapi.tiangolo.com) + [SQLAlchemy](https://sqlalchemy.org) (async)
- [Next.js](https://nextjs.org) 14 App Router
- [Docker](https://docker.com) (sandboxed execution)
- [Stripe](https://stripe.com) (billing)

## License

MIT
