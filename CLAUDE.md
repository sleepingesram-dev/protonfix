# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ProtonFix is a deterministic Linux gaming diagnosis engine. It analyzes Proton, Wine, DXVK, VKD3D, and GPU driver logs to identify gaming failures. The philosophy is **deterministic pattern matching first, OpenAI GPT-4.1-mini fallback only when fingerprints don't match**.

## Dev Startup

Two separate terminals are required:

```bash
# Terminal 1 — backend
cd backend
uvicorn main:app --reload

# Terminal 2 — frontend
cd frontend
npm run dev
```

Frontend connects to `http://127.0.0.1:8000` (set in `frontend/.env.local`).

## Key Commands

```bash
# Backend test suite
cd backend
python -m pytest tests/

# Backend smoke checks
python run_sample_tests.py
python test_parser.py
python corpus/harness.py

# Frontend lint
cd frontend
npm run lint

# Frontend build
cd frontend
npm run build
```

## Architecture: Diagnosis Pipeline

```
Upload Log → Parse → Extract Evidence → Generate Hypotheses
  → Rank Fingerprints → Build Dependency Chain → Resolve Known Issues
  → [fallback] OpenAI GPT-4.1-mini → Return Diagnosis + Store in SQLite
```

- `backend/parser.py` — extracts versions, errors from raw log text
- `backend/evidence.py` — `Evidence` dataclass with `EvidenceKind` and `EvidenceSeverity`
- `backend/fingerprints/database.py` — `ERROR_PATTERNS`: raw log pattern → fingerprint mapping
- `backend/fingerprints/known_issues.py` — `KNOWN_ISSUES`: pre-written solutions for ~40 fingerprints
- `backend/fingerprints/dependencies.py` — `ROOT_CAUSE_GRAPH`: causal parent→child relationships
- `backend/fingerprints/ranking.py` — hypothesis scoring via `ROOT_CAUSE_PRIORITY` weights (0–100)
- `backend/analyzer.py` — OpenAI fallback; only invoked when pattern matching yields nothing
- `backend/history.py` — SQLite storage (`history.db`, table: `diagnoses`)

## Knowledge Graph

The knowledge base is **hardcoded Python dicts**, not a database. To add new issue types:
1. Add a `FingerprintDefinition` (`fingerprints/models.py` pattern)
2. Add entries to `ERROR_PATTERNS` in `fingerprints/database.py`
3. Optionally add a solution to `KNOWN_ISSUES` in `fingerprints/known_issues.py`
4. Optionally wire causal relationships in `ROOT_CAUSE_GRAPH` (`fingerprints/dependencies.py`)

## Gotchas

- **`.env` must not be committed** — `backend/.env` contains the OpenAI API key. It's covered by `.gitignore`.
- **CORS** — defaults to `*` for local dev; set `PROTONFIX_ALLOWED_ORIGINS` (comma-separated) for any public deployment. The prod compose overlay sets it from `DOMAIN`.
- **Admin auth** — `/admin` endpoints are open unless `PROTONFIX_ADMIN_TOKEN` is set; then they require an `X-Admin-Token` header (the admin UI prompts for it).
- **AI fallback is optional** — without `OPENAI_API_KEY` the app still runs; unmatched logs get a low-confidence "AI unavailable" diagnosis from `analyzer.py`.
- **Two confidence representations** — fingerprint confidence is an `int` 0–100; diagnosis-level confidence is a `"low" | "medium" | "high"` label. Don't mix them up when serializing.
- **Runtime data lives under `PROTONFIX_DATA_DIR`** — `history.db`, `uploads/`, and `stats/` are runtime artifacts and gitignored; never commit them.
