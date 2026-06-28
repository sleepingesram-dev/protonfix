# Deployment

ProtonFix runs as two containers: a FastAPI backend and a Next.js frontend.

## Requirements

- Docker 24+
- Docker Compose v2+

## Quick Start (local)

### 1. Create the backend env file

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and set `OPENAI_API_KEY`. The deterministic fingerprint
engine works without it; the key is only used when no fingerprint matches
the uploaded log and the AI fallback is triggered.

### 2. Build and start

```bash
docker compose build
docker compose up -d
```

### 3. Open in browser

| Service  | URL                           |
|----------|-------------------------------|
| Frontend | http://localhost:3000         |
| Backend  | http://localhost:8000         |
| API docs | http://localhost:8000/docs    |
| Health   | http://localhost:8000/health  |

The frontend waits for the backend health check to pass before starting.

---

## Data Persistence

All persistent data is stored in the `protonfix_data` Docker named volume,
mounted at `/data` inside the backend container:

| Path in container   | Contents                    |
|---------------------|-----------------------------|
| `/data/history.db`  | SQLite diagnosis history    |
| `/data/uploads/`    | Uploaded log files          |
| `/data/stats/`      | Usage statistics JSON       |

---

## Common Commands

```bash
# View live logs
docker compose logs -f

# Restart a single service
docker compose restart backend

# Stop without losing data
docker compose down

# Stop and delete the data volume (irreversible)
docker compose down -v
```

---

## Notes

- **CORS**: The backend allows all origins (`allow_origins=["*"]`). Restrict
  this in `backend/main.py` before exposing the service to the internet.
- **Admin**: `/admin` has no authentication. Do not expose it publicly.
- **File uploads**: Limited to 10 MB per log. Stored under `/data/uploads/`.

---

## VPS Deployment (HTTPS via Caddy)

Caddy is included as a service in `docker-compose.prod.yml`. It terminates TLS
and reverse-proxies to the frontend and backend. Certificates are obtained from
Let's Encrypt automatically — no manual cert setup needed.

### Architecture

```
Internet → Caddy (:80/:443)
               ├── protonfix.example.com       → frontend:3000
               └── api.protonfix.example.com   → backend:8000
```

`NEXT_PUBLIC_API_URL` is baked into the frontend bundle at build time as
`https://api.DOMAIN`, so the browser calls the backend via the public subdomain.

---

### 1. DNS

Create two A records pointing to your VPS IP:

| Record                        | Type | Value      |
|-------------------------------|------|------------|
| `protonfix.example.com`       | A    | `<VPS IP>` |
| `api.protonfix.example.com`   | A    | `<VPS IP>` |

DNS must resolve before Caddy can complete the ACME challenge.

---

### 2. Firewall

Open only these ports on the VPS:

| Port | Protocol | Purpose                  |
|------|----------|--------------------------|
| 22   | TCP      | SSH                      |
| 80   | TCP      | HTTP (ACME + redirect)   |
| 443  | TCP      | HTTPS                    |
| 443  | UDP      | HTTP/3 (optional)        |

Block 3000 and 8000 from the public internet — Caddy proxies them internally.

```bash
# ufw example
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 443/udp
ufw deny 3000
ufw deny 8000
ufw enable
```

---

### 3. Server setup

```bash
git clone <repo-url> protonfix-ai
cd protonfix-ai

# Backend secrets
cp backend/.env.example backend/.env
# Edit backend/.env and set OPENAI_API_KEY

# Root .env — sets DOMAIN and activates the prod overlay
cp .env.example .env
# Edit .env: set DOMAIN=protonfix.example.com
```

---

### 4. Build and start

Because `.env` sets `COMPOSE_FILE=docker-compose.yml:docker-compose.prod.yml`,
plain `docker compose` commands automatically merge both files:

```bash
docker compose build
docker compose up -d
```

The frontend is rebuilt with `NEXT_PUBLIC_API_URL=https://api.DOMAIN` baked in.

---

### 5. Verify

```bash
# All containers running
docker compose ps

# HTTPS health check
curl https://api.protonfix.example.com/health
# → {"status":"ok","version":"..."}

# Caddy logs (cert issuance, proxy errors)
docker compose logs -f caddy
```

---

## Backup and Restore

### Backup

```bash
./scripts/backup.sh
# or specify a custom output directory:
./scripts/backup.sh /mnt/backups
```

Archives are written to `./backups/protonfix_backup_YYYYMMDD_HHMMSS.tar.gz`.
The stack can remain running during a backup.

### Restore

```bash
docker compose down
./scripts/restore.sh backups/protonfix_backup_YYYYMMDD_HHMMSS.tar.gz
docker compose up -d
```

The script prompts for confirmation before overwriting.

### Automate with cron

```bash
# Daily backup at 03:00
0 3 * * * /path/to/protonfix-ai/scripts/backup.sh /mnt/backups >> /var/log/protonfix-backup.log 2>&1
```

---

## Updating

```bash
./scripts/update.sh
```

Runs `git pull`, `docker compose build`, and `docker compose up -d` from the
project root. If `COMPOSE_FILE` is set in `.env`, the prod overlay is included
automatically and the frontend is rebuilt with the correct `NEXT_PUBLIC_API_URL`.

Data in the named volume is preserved across rebuilds.
