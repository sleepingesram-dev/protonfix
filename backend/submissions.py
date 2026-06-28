import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from config import DATA_DIR

DB_FILE = DATA_DIR / "history.db"


def _conn():
    return sqlite3.connect(DB_FILE)


def _init():
    with _conn() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submitted_at TEXT NOT NULL,
                filename TEXT,
                note TEXT,
                ip_hash TEXT,
                log_text TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                diagnosis_json TEXT,
                redaction_json TEXT
            )
            """
        )
        # Migrate existing databases that predate the redaction column.
        try:
            c.execute("ALTER TABLE submissions ADD COLUMN redaction_json TEXT")
        except Exception:
            pass  # Column already exists


def save_submission(
    log_text: str,
    filename: str,
    note: str,
    ip: str,
    redaction: dict | None = None,
) -> int:
    _init()
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]
    with _conn() as c:
        cur = c.execute(
            """
            INSERT INTO submissions
                (submitted_at, filename, note, ip_hash, log_text, redaction_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                filename,
                note,
                ip_hash,
                log_text,
                json.dumps(redaction) if redaction else None,
            ),
        )
        return cur.lastrowid


def get_submissions(limit: int = 100) -> list[dict[str, Any]]:
    _init()
    with _conn() as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            """
            SELECT id, submitted_at, filename, note, ip_hash, status,
                   LENGTH(log_text) AS log_size
            FROM submissions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_submission(sub_id: int) -> dict[str, Any] | None:
    _init()
    with _conn() as c:
        c.row_factory = sqlite3.Row
        row = c.execute(
            "SELECT * FROM submissions WHERE id = ?", (sub_id,)
        ).fetchone()
        if not row:
            return None
        result = dict(row)
        diag_json = result.pop("diagnosis_json", None)
        if diag_json:
            result["diagnosis"] = json.loads(diag_json)
        redaction_json = result.pop("redaction_json", None)
        if redaction_json:
            result["redaction"] = json.loads(redaction_json)
        return result


def attach_diagnosis(sub_id: int, diagnosis: dict[str, Any]) -> None:
    _init()
    with _conn() as c:
        c.execute(
            "UPDATE submissions SET status = 'diagnosed', diagnosis_json = ? WHERE id = ?",
            (json.dumps(diagnosis), sub_id),
        )
