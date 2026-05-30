#!/bin/bash
set -euo pipefail

# TicketForge production deployment script
# Usage: ./scripts/deploy.sh [host]

HOST="${1:-ticketforge.example.com}"
REMOTE_DIR="/opt/ticketforge"

echo "Deploying TicketForge to ${HOST}..."

# Build images locally
echo "Building Docker images..."
docker-compose -f docker-compose.prod.yml build

# Push images to registry (or use SSH + build on remote)
echo "Syncing files to ${HOST}..."
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' \
  . "${HOST}:${REMOTE_DIR}/"

echo "Restarting services on ${HOST}..."
ssh "${HOST}" "cd ${REMOTE_DIR} && docker-compose -f docker-compose.prod.yml pull && docker-compose -f docker-compose.prod.yml up -d"

echo "Building sandbox image on remote..."
ssh "${HOST}" "cd ${REMOTE_DIR} && docker build -t ticketforge-sandbox -f sandbox/Dockerfile.sandbox sandbox/"

echo "Deployment complete. Health check:"
curl -s "https://${HOST}/api/health" || echo "Health check pending — services may still be starting."
