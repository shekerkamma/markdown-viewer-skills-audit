#!/bin/bash
set -e

if [ -n "$REPO_URL" ]; then
    echo "Cloning $REPO_URL (branch: ${BRANCH:-main})..."
    git clone --depth 1 --branch "${BRANCH:-main}" "$REPO_URL" /workspace/repo 2>/dev/null || \
    git clone --depth 1 "$REPO_URL" /workspace/repo
    cd /workspace/repo
    echo "Repository cloned successfully."
fi

exec "$@"
