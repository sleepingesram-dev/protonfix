#!/usr/bin/env bash
# restore.sh — restore the protonfix_data volume from a backup archive.
#
# Usage: ./scripts/restore.sh <backup-file.tar.gz>
#
# IMPORTANT: stop the stack before restoring.
#   docker compose down
#   ./scripts/restore.sh backups/protonfix_backup_YYYYMMDD_HHMMSS.tar.gz
#   docker compose up -d

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

BACKUP_FILE="${1:?Usage: $0 <backup-file.tar.gz>}"

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "Error: file not found: $BACKUP_FILE"
  exit 1
fi

BACKUP_FILE="$(realpath "$BACKUP_FILE")"

echo "Restore source : $BACKUP_FILE"
echo "Restore target : protonfix_data Docker volume"
echo ""
echo "WARNING: all existing data in the volume will be overwritten."
echo "         Run 'docker compose down' first if the stack is running."
echo ""
printf "Type 'yes' to continue: "
read -r CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
  echo "Aborted."
  exit 0
fi

echo ""
echo "==> Restoring..."

docker run --rm \
  -v protonfix_data:/data \
  -v "$BACKUP_FILE:/backup.tar.gz:ro" \
  alpine sh -c "
    rm -rf /data/*
    tar xzf /backup.tar.gz --strip-components=1 -C /data
  "

echo "==> Restore complete."
echo "    Run: docker compose up -d"
