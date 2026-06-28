from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

from parser import parse_log
from resolver import resolve_known_issues
from analyzer import analyze_log_text
from stats import update_stats, get_stats
from history import save_diagnosis, get_history, get_diagnosis


app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
@app.post("/analyze-log")
async def analyze(file: UploadFile = File(...)):
    save_path = UPLOAD_DIR / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(save_path, "r", errors="ignore") as f:
        log_text = f.read()

    parsed = parse_log(log_text)
    known_issue = resolve_known_issues(parsed)

    if known_issue:
        diagnosis = known_issue
        ai_used = False
        ai_result = None
    else:
        diagnosis = analyze_log_text(log_text, parsed)
        ai_used = True
        ai_result = diagnosis

    result = {
        "filename": file.filename,
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

    update_stats(result)

    history_id = save_diagnosis(result)
    result["history_id"] = history_id

    return result


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
