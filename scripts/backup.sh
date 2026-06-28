#!/usr/bin/env bash
# backup.sh — snapshot the protonfix_data volume to a .tar.gz file.
#
# Usage: ./scripts/backup.sh [output-dir]
#   output-dir defaults to ./backups
#
# The stack can remain running during a backup.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

BACKUP_DIR="${1:-./backups}"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTFILE="$(realpath "$BACKUP_DIR")/protonfix_backup_${TIMESTAMP}.tar.gz"

echo "==> Backing up protonfix_data volume to $OUTFILE"

docker run --rm \
  -v protonfix_data:/data:ro \
  -v "$(realpath "$BACKUP_DIR"):/backup" \
  alpine tar czf "/backup/protonfix_backup_${TIMESTAMP}.tar.gz" /data

echo "==> Done: $OUTFILE"
echo "    $(du -h "$OUTFILE" | cut -f1) written."
