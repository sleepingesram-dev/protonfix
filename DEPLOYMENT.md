# Deployment

ProtonFix AI runs as two containers: a FastAPI backend and a Next.js frontend.

## Requirements

- Docker 24+
- Docker Compose v2+

## Quick Start

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

## Changing the Backend URL

`NEXT_PUBLIC_API_URL` is baked into the frontend bundle at build time.
If your backend is behind a domain or non-default port, rebuild the frontend:

```bash
docker compose build \
  --build-arg NEXT_PUBLIC_API_URL=https://api.your-domain.com \
  frontend
```

---

## Data Persistence

All persistent data is stored in the `protonfix_data` Docker named volume,
mounted at `/data` inside the backend container:

| Path in container   | Contents                    |
|---------------------|-----------------------------|
| `/data/history.db`  | SQLite diagnosis history    |
| `/data/uploads/`    | Uploaded log files          |
| `/data/stats/`      | Usage statistics JSON       |

### Backup

```bash
docker run --rm \
  -v protonfix_data:/data \
  -v "$(pwd):/backup" \
  alpine tar czf /backup/protonfix-backup.tar.gz /data
```

### Restore

```bash
docker run --rm \
  -v protonfix_data:/data \
  -v "$(pwd):/backup" \
  alpine tar xzf /backup/protonfix-backup.tar.gz -C /
```

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

# Rebuild after code changes
docker compose build
docker compose up -d
```

---

## Updating

```bash
docker compose build
docker compose up -d
```

Data in the named volume is preserved across rebuilds.

---

## Notes

- **CORS**: The backend allows all origins (`allow_origins=["*"]`). Restrict
  this in `backend/main.py` before exposing the service to the internet.
- **Admin**: `/admin` has no authentication. Do not expose it publicly.
- **File uploads**: Limited to 10 MB per log. Stored under `/data/uploads/`.
