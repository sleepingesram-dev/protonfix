import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from config import DATA_DIR

DB_FILE = DATA_DIR / "history.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_history_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnoses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                filename TEXT,
                game TEXT,
                appid TEXT,
                proton_version TEXT,
                primary_fingerprint TEXT,
                confidence INTEGER,
                severity TEXT,
                summary TEXT,
                probable_cause TEXT,
                full_result_json TEXT NOT NULL
            )
            """
        )


def save_diagnosis(result: dict[str, Any]) -> int:
    init_history_db()

    parsed = result.get("parsed", {})
    primary = parsed.get("primary_fingerprint") or {}

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO diagnoses (
                created_at,
                filename,
                game,
                appid,
                proton_version,
                primary_fingerprint,
                confidence,
                severity,
                summary,
                probable_cause,
                full_result_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                result.get("filename"),
                parsed.get("game"),
                parsed.get("appid"),
                parsed.get("proton_version"),
                primary.get("fingerprint"),
                primary.get("confidence"),
                result.get("severity"),
                result.get("summary"),
                result.get("probable_cause"),
                json.dumps(result),
            ),
        )

        return cursor.lastrowid


def get_history(limit: int = 50) -> list[dict[str, Any]]:
    init_history_db()

    with get_connection() as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT
                id,
                created_at,
                filename,
                game,
                appid,
                proton_version,
                primary_fingerprint,
                confidence,
                severity,
                summary,
                probable_cause
            FROM diagnoses
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]


def get_diagnosis(diagnosis_id: int) -> dict[str, Any] | None:
    init_history_db()

    with get_connection() as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            """
            SELECT full_result_json
            FROM diagnoses
            WHERE id = ?
            """,
            (diagnosis_id,),
        ).fetchone()

        if not row:
            return None

        return json.loads(row["full_result_json"])
