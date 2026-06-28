import os
from pathlib import Path

# All persistent data (SQLite DB, uploads, stats) lives under DATA_DIR.
# Default is "." so local dev works without any env var.
# In Docker, set PROTONFIX_DATA_DIR=/data and mount that as a named volume.
DATA_DIR = Path(os.getenv("PROTONFIX_DATA_DIR", "."))
DATA_DIR.mkdir(parents=True, exist_ok=True)
