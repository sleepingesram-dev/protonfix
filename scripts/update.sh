#!/usr/bin/env bash
# update.sh — pull latest code and restart the stack.
#
# On a VPS with docker-compose.prod.yml active via .env:
#   COMPOSE_FILE=docker-compose.yml:docker-compose.prod.yml
# plain `docker compose` commands below automatically pick up both files.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "==> git pull"
git pull

echo "==> docker compose build"
docker compose build

echo "==> docker compose up -d"
docker compose up -d

echo ""
docker compose ps
