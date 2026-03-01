"""Data loading module for raw trade CSV files."""

import pandas as pd
from glob import glob
from pathlib import Path
from config import DATA_RAW_DIR

### Debug code
# from config import ROOT_DIR
# print("CWD:", Path.cwd())
# print(
#     "DATA PATH EXISTS:",
#     DATA_RAW_DIR.resolve(),
#     "->",
#     DATA_RAW_DIR.exists(),
# )


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

        file_number = parts[0]
        hs_code = parts[9].split(".")[0].upper()
        trade_direction = "_".join(parts[5:8]).upper().replace("_TO_", "_to_")

        df = pd.read_csv(f, encoding="latin1", low_memory=False)

        df["file_number"] = file_number
        df["hs_code"] = hs_code
        df["trade_direction"] = trade_direction

        dfs.append(df)

    print(f"\n\t✅ Data Files list: {len(files_list)} | Files imported: {len(dfs)}\n")

    return pd.concat(dfs, ignore_index=True)


### Debug code
# print("'dataset.py' loaded")
