"""Data loading module for raw trade CSV files."""

import pandas as pd
from glob import glob
from pathlib import Path
from config import DATA_RAW_DIR


def load_all_trade_data() -> pd.DataFrame:
    """Load and concatenate all raw trade CSV files from the data/raw/ directory.

    Parses the file naming convention to extract the HS code granularity and trade
    direction for each file, then tags each row accordingly before concatenation.

    File naming convention (underscore-delimited):
        <seq>_<date>_<...>_<direction_parts>_<...>_<hs_code>.csv

    Returns:
        pd.DataFrame: Concatenated dataframe with added columns:
            - 'file_number' (str): Sequential file identifier from the filename.
            - 'hs_code' (str): HS code granularity, e.g., 'HS2' or 'HS6'.
            - 'trade_direction' (str): Direction label, e.g., 'GRULAC_to_APAC'.
    """
    files_list = sorted(glob(str(DATA_RAW_DIR / "*.csv")))
    dfs = []

    for f in files_list:
        fname = Path(f).name
        parts = fname.split("_")

        if len(parts) < 10:
            raise ValueError(
                f"Unexpected filename format (expected >=10 underscore-separated "
                f"segments, got {len(parts)}): {fname!r}"
            )

        file_number = parts[0]
        src_region = parts[5].upper()
        dst_region = parts[7].upper()
        trade_direction = f"{src_region}_to_{dst_region}"
        hs_code = parts[9].split(".")[0].upper()

        df = pd.read_csv(f, encoding="latin1", low_memory=False)

        df["file_number"] = file_number
        df["hs_code"] = hs_code
        df["trade_direction"] = trade_direction

        dfs.append(df)

    print(f"\n\t✅ Data Files list: {len(files_list)} | Files imported: {len(dfs)}\n")

    return pd.concat(dfs, ignore_index=True)
