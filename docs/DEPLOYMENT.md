# TicketForge Deployment Guide

## Production Architecture

- **Backend**: FastAPI + Gunicorn/Uvicorn, PostgreSQL, Redis
- **Frontend**: Next.js deployed to Vercel (or self-hosted)
- **Sandbox**: Docker daemon on the same VPS as the backend

## VPS Deployment

### Prerequisites

- Ubuntu 22.04+ VPS with Docker installed
- Domain name with DNS pointing to VPS
- PostgreSQL 16 (managed or self-hosted)
- Redis 7

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ticketforge.git
   cd ticketforge
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Build and run**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Set up SSL** (Caddy handles automatic HTTPS)
   ```
   # Caddyfile
   ticketforge.example.com {
       reverse_proxy localhost:8000
   }
   ```

5. **Build the sandbox image**
   ```bash
   docker build -t ticketforge-sandbox -f sandbox/Dockerfile.sandbox sandbox/
   ```

## Vercel Frontend Deployment

1. Connect the `frontend/` directory to Vercel
2. Set environment variables:
   - `NEXT_PUBLIC_API_URL` = `https://api.ticketforge.example.com`
   - `NEXT_PUBLIC_SENTRY_DSN` = your Sentry DSN
3. Deploy

## GitHub OAuth App

Create a GitHub OAuth app:
- Homepage URL: `https://ticketforge.example.com`
- Callback URL: `https://api.ticketforge.example.com/api/auth/github/callback`

## Stripe Setup

1. Create a product and price in Stripe Dashboard
2. Set `STRIPE_PRICE_ID_TEAM` to the price ID
3. Configure webhook endpoint: `https://api.ticketforge.example.com/api/webhooks/stripe`
4. Events to listen for: `checkout.session.completed`, `customer.subscription.deleted`

## Monitoring

- **Sentry**: Backend and frontend error tracking
- **Health check**: `GET /api/health` returns `{"status": "ok"}`
