"""Project-wide path configuration and directory constants."""

from pathlib import Path

# Root directory — the folder containing pyproject.toml (one level above src/)
ROOT_DIR = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = ROOT_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

### Debug code
# print("'config.py' loaded")
