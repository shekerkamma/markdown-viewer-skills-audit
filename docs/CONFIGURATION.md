# TicketForge Configuration Reference

## Environment Variables

All configuration is via environment variables. Copy `.env.example` to `.env` and fill in values.

### Required

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (`postgresql+asyncpg://...`) |
| `GITHUB_CLIENT_ID` | GitHub OAuth app client ID |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret |
| `GITHUB_WEBHOOK_SECRET` | Shared secret for webhook signature verification |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude |
| `JWT_SECRET` | Secret key for JWT token signing (use a strong random value) |
| `ENCRYPTION_KEY` | Fernet-compatible key for encrypting GitHub tokens at rest |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_URL` | `http://localhost:3000` | Frontend URL (used for CORS and Stripe redirects) |
| `API_URL` | `http://localhost:8000` | Backend URL (used for webhook registration) |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection for ARQ task queue |
| `JWT_EXPIRY_HOURS` | `24` | JWT token lifetime in hours |
| `STRIPE_SECRET_KEY` | _(empty)_ | Stripe secret key for billing |
| `STRIPE_WEBHOOK_SECRET` | _(empty)_ | Stripe webhook signing secret |
| `STRIPE_PRICE_ID_TEAM` | _(empty)_ | Stripe Price ID for the Team plan |
| `SENTRY_DSN` | _(empty)_ | Sentry DSN for backend error tracking |
| `NEXT_PUBLIC_SENTRY_DSN` | _(empty)_ | Sentry DSN for frontend error tracking |

## Repository Configuration

Each connected repository has a JSONB `config` field. Set via the API (`PATCH /api/v1/teams/:id/repos/:repo_id`):

```json
{
  "review": {
    "require_tests": true,
    "security_check": true,
    "style_check": true,
    "min_confidence": 0.6
  },
  "slack_webhook_url": "https://hooks.slack.com/services/..."
}
```

### Review Config

| Key | Default | Description |
|-----|---------|-------------|
| `require_tests` | `true` | Require test coverage in generated fixes |
| `security_check` | `true` | Reject fixes with security score < 0.3 |
| `style_check` | `true` | Include style dimension in review |
| `min_confidence` | `0.6` | Minimum confidence threshold for auto-approve |

### Slack Notifications

Set `slack_webhook_url` in repo config to receive Slack messages when tickets are escalated.

## Plan Limits

| Plan | Monthly Tickets |
|------|----------------|
| Free | 20 |
| Team | 500 |
| Enterprise | 10,000 |

## Trigger Labels

Configure which GitHub issue labels trigger the pipeline. Default: `["bug"]`. Set per-repository in the dashboard Settings page.
