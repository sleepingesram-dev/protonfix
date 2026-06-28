import json
from pathlib import Path
from typing import Any


STATS_DIR = Path("stats")
STATS_FILE = STATS_DIR / "stats.json"


DEFAULT_STATS = {
    "total_logs": 0,
    "fingerprints": {},
    "games": {},
    "proton_versions": {},
    "gpus": {},
    "categories": {},
    "ai_used": 0,
    "known_issue_used": 0,
}


def ensure_stats_file() -> None:
    STATS_DIR.mkdir(exist_ok=True)

    if not STATS_FILE.exists():
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_STATS, f, indent=2)


def load_stats() -> dict[str, Any]:
    ensure_stats_file()

    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)
    except json.JSONDecodeError:
        stats = DEFAULT_STATS.copy()

    for key, value in DEFAULT_STATS.items():
        if key not in stats:
            stats[key] = value

    return stats


def save_stats(stats: dict[str, Any]) -> None:
    ensure_stats_file()

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def increment_counter(stats: dict[str, Any], section: str, key: str | None) -> None:
    if not key:
        return

    if section not in stats:
        stats[section] = {}

    stats[section][key] = stats[section].get(key, 0) + 1


def update_stats(result: dict[str, Any]) -> None:
    stats = load_stats()

    parsed = result.get("parsed", {})

    stats["total_logs"] = stats.get("total_logs", 0) + 1

    if result.get("ai_used"):
        stats["ai_used"] = stats.get("ai_used", 0) + 1

    if result.get("known_issue"):
        stats["known_issue_used"] = stats.get("known_issue_used", 0) + 1

    increment_counter(stats, "games", parsed.get("game"))
    increment_counter(stats, "proton_versions", parsed.get("proton_version"))

    for item in parsed.get("fingerprints", []):
        fingerprint = item.get("fingerprint")
        category = item.get("category")

        increment_counter(stats, "fingerprints", fingerprint)
        increment_counter(stats, "categories", category)

    save_stats(stats)


def get_stats() -> dict[str, Any]:
    return load_stats()
