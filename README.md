# ProtonFix

Deterministic Linux gaming log analyzer for Proton, Steam, DXVK, VKD3D, and Vulkan issues.

Fingerprint-first: pattern matching runs against a hardcoded knowledge graph. OpenAI GPT-4.1-mini is called only when no fingerprint matches.

## Stack

- **Backend** — FastAPI (Python), SQLite, regex-based fingerprint engine
- **Frontend** — Next.js 15, TypeScript, Tailwind CSS

## Quick Start

```bash
# Backend
cd backend
cp .env.example .env          # add OPENAI_API_KEY
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

## Docker

```bash
cp backend/.env.example backend/.env   # add OPENAI_API_KEY
docker compose build
docker compose up -d
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for VPS deployment with HTTPS (Caddy).

## Diagnosis Pipeline

```
Upload Log → Parse → Extract Evidence → Generate Hypotheses
  → Rank Fingerprints → Build Dependency Chain → Resolve Known Issues
  → [fallback] OpenAI GPT-4.1-mini → Return Diagnosis + Store in SQLite
```

## Extending the Knowledge Graph

The knowledge base is hardcoded Python dicts in `backend/fingerprints/`. To add a new issue type:

1. Add a `FingerprintDefinition` following `fingerprints/models.py`
2. Add entries to `ERROR_PATTERNS` in `fingerprints/database.py`
3. Optionally add a solution to `KNOWN_ISSUES` in `fingerprints/known_issues.py`
4. Optionally wire causal relationships in `ROOT_CAUSE_GRAPH` in `fingerprints/dependencies.py`

## License

MIT
