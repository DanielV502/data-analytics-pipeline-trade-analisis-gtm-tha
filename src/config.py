"""Project-wide path configuration and shared business constants."""

from pathlib import Path

# Root directory — the folder containing pyproject.toml (one level above src/)
ROOT_DIR = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = ROOT_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

# HS product code lengths by granularity
HS_CODE_LENGTHS = {"HS2": 2, "HS6": 6}

# Allowed trade direction labels (validated against the data)
ALLOWED_TRADE_DIRECTIONS = frozenset({
    "GRULAC_to_APAC",
    "THA_to_GRULAC",
    "GTM_to_APAC",
    "GTM_to_WORLD",
})

# Required columns for the processed dataset
REQUIRED_COLUMNS = frozenset({
    "year",
    "productcode",
    "productdescription",
    "trade_value_usd",
    "trade_direction",
    "reportername",
    "partnername",
})

# Numeric columns coerced during dtype casting
NUMERIC_COLUMNS = (
    "tradevalue_in_1000_usd",
    "netweight_in_kgm",
    "quantity",
)

# World Bank region -> macro-region label
MACRO_REGION_MAP = {
    "East Asia & Pacific": "APAC",
    "South Asia": "APAC",
    "Latin America & Caribbean": "GRULAC",
    "Europe & Central Asia": "EMEA",
    "Middle East, North Africa, Afghanistan & Pakistan": "EMEA",
    "Sub-Saharan Africa": "EMEA",
    "North America": "NORTH_AMERICA",
}

# Output filename for the persisted processed dataset (no extension)
PROCESSED_DATASET_BASENAME = "trade_gtm_tha_2017_2025_processed"

### Debug code
# print("'config.py' loaded")
