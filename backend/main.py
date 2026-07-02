import os
import secrets
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from config import DATA_DIR
from parser import parse_log
from synthesizer import synthesize_diagnosis
from analyzer import analyze_log_text
from stats import update_stats, get_stats
from history import save_diagnosis, get_history, get_diagnosis
from submissions import save_submission, get_submissions, get_submission, attach_diagnosis
from redactor import redact

APP_VERSION = "0.8.0"
MAX_LOG_BYTES = 10 * 1024 * 1024  # 10 MB

app = FastAPI(title="ProtonFix", version=APP_VERSION)

UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Comma-separated list of allowed origins, e.g.
#   PROTONFIX_ALLOWED_ORIGINS=https://protonfix.example.com
# Defaults to "*" for local development. Credentials are only enabled for an
# explicit origin list — the CORS spec forbids wildcard + credentials.
_origins = [
    origin.strip()
    for origin in os.getenv("PROTONFIX_ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials="*" not in _origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional shared secret protecting the /admin endpoints. If unset, admin
# routes stay open (local development). Set it for any public deployment.
ADMIN_TOKEN = os.getenv("PROTONFIX_ADMIN_TOKEN", "")


def _require_admin(request: Request) -> None:
    if ADMIN_TOKEN and not secrets.compare_digest(
        request.headers.get("X-Admin-Token", ""), ADMIN_TOKEN
    ):
        raise HTTPException(status_code=401, detail="Invalid or missing admin token")


async def _read_upload(file: UploadFile) -> bytes:
    """Read upload in chunks, enforcing the 10 MB cap."""
    chunks, total = [], 0
    while True:
        chunk = await file.read(65_536)
        if not chunk:
            break
        total += len(chunk)
        if total > MAX_LOG_BYTES:
            raise HTTPException(status_code=413, detail="Log file exceeds 10 MB limit.")
        chunks.append(chunk)
    return b"".join(chunks)


def _safe_filename(raw: str) -> str:
    """Strip directory traversal components from an uploaded filename."""
    return Path(raw).name or "upload.log"


def _diagnose(log_text: str, parsed: dict, filename: str) -> dict:
    """Run deterministic synthesis, falling back to AI, and return a full result dict."""
    synth = synthesize_diagnosis(parsed)
    if synth:
        diagnosis = synth
        known_issue = synth if synth.get("used_known_issue") else None
        ai_used = False
        ai_result = None
    else:
        diagnosis = analyze_log_text(log_text, parsed)
        known_issue = None
        ai_used = True
        ai_result = diagnosis

    return {
        "version": APP_VERSION,
        "filename": filename,
        "characters": len(log_text),
        "summary": diagnosis.get("summary", ""),
        "probable_cause": diagnosis.get("probable_cause", ""),
        "confidence": diagnosis.get("confidence", "low"),
        "severity": diagnosis.get("severity", "low"),
        "used_known_issue": diagnosis.get("used_known_issue", False),
        "known_issue_id": diagnosis.get("known_issue_id"),
        "detected_errors": diagnosis.get("detected_errors", []),
        "fix_steps": diagnosis.get("fix_steps", []),
        "recommended_commands": diagnosis.get("recommended_commands", []),
        "extra_info_needed": diagnosis.get("extra_info_needed", []),
        "warnings": diagnosis.get("warnings", []),
        "parsed": parsed,
        "dependency_chain": parsed.get("dependency_chain", []),
        "known_issue": known_issue,
        "ai_used": ai_used,
        "ai_result": ai_result,
    }


@app.get("/health")
async def health():
    return {"status": "ok", "version": APP_VERSION}


@app.post("/analyze")
@app.post("/analyze-log")
async def analyze(file: UploadFile = File(...)):
    raw = await _read_upload(file)
    if not raw.strip():
        raise HTTPException(status_code=400, detail="Uploaded log file is empty.")
    filename = _safe_filename(file.filename or "upload.log")

    # Prefix with timestamp + random suffix so same-named uploads never collide.
    stored_name = f"{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}_{filename}"
    (UPLOAD_DIR / stored_name).write_bytes(raw)

    log_text = raw.decode("utf-8", errors="ignore")
    parsed = parse_log(log_text)
    result = _diagnose(log_text, parsed, filename)

    update_stats(result)
    result["history_id"] = save_diagnosis(result)
    return result


@app.post("/submit")
async def submit_log(
    request: Request,
    file: UploadFile = File(...),
    note: str = Form(""),
):
    raw = await _read_upload(file)
    if not raw.strip():
        raise HTTPException(status_code=400, detail="Uploaded log file is empty.")
    filename = _safe_filename(file.filename or "upload.log")
    log_text = raw.decode("utf-8", errors="ignore")

    redaction = redact(log_text)

    ip = request.client.host if request.client else "unknown"
    # The UI caps notes at 500 chars; enforce the same limit server-side.
    sub_id = save_submission(
        redaction.text, filename, note.strip()[:500], ip, redaction.report()
    )
    return {
        "submitted": True,
        "submission_id": sub_id,
        "redaction": redaction.report(),
    }


@app.get("/stats")
async def stats():
    return get_stats()


@app.get("/history")
async def history():
    return get_history()


@app.get("/history/{diagnosis_id}")
async def history_item(diagnosis_id: int):
    result = get_diagnosis(diagnosis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return result


@app.get("/admin/submissions")
async def admin_submissions(request: Request):
    _require_admin(request)
    return get_submissions()


@app.get("/admin/submissions/{sub_id}")
async def admin_submission(sub_id: int, request: Request):
    _require_admin(request)
    result = get_submission(sub_id)
    if not result:
        raise HTTPException(status_code=404, detail="Submission not found")
    return result


@app.post("/admin/submissions/{sub_id}/diagnose")
async def admin_diagnose(sub_id: int, request: Request):
    _require_admin(request)
    sub = get_submission(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    log_text = sub["log_text"]
    parsed = parse_log(log_text)
    result = _diagnose(log_text, parsed, sub.get("filename") or "submitted.log")
    attach_diagnosis(sub_id, result)
    return result
