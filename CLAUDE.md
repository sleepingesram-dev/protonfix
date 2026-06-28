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
# Backend tests / smoke checks
cd backend
python run_sample_tests.py
python test_parser.py

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
- `backend/fingerprints/known_issues.py` — `KNOWN_ISSUES`: pre-written solutions (currently sparse)
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

- **`.env` must not be committed** — `backend/.env` contains the OpenAI API key. Ensure it's in `.gitignore`.
- **CORS is open** — FastAPI uses `allow_origins=["*"]`; tighten this before any public deployment.
- **`KNOWN_ISSUES` is sparse** — only `VULKAN_DRIVER_MISSING` has a solution; most diagnoses go through the AI fallback or return raw fingerprint data.
- **Evidence field naming** — `evidence.py` has an `evidence_type` field but internal code sometimes expects `kind`; be consistent when modifying evidence handling.
- **Confidence type mismatch** — confidence is `int` internally but serialized as `str` in some frontend-facing paths; don't change one side without updating the other.
- **File upload collisions** — uploads are saved to `/uploads/<original_filename>`; same-named files overwrite silently.
