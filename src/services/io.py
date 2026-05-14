"""I/O service for persisting processed trade datasets."""

import pandas as pd
from config import DATA_PROCESSED_DIR


def save_processed_dataset(
    df: pd.DataFrame, base_name: str, *, also_csv: bool = True
) -> None:
    """Save the processed DataFrame to Parquet, optionally also to CSV.

    Args:
        df (pd.DataFrame): Processed trade DataFrame to persist.
        base_name (str): Base filename without extension (e.g., 'trade_gtm_tha_2017_2025_processed').
            Output files will be saved under data/processed/.
        also_csv (bool): If True (default), also write a CSV next to the Parquet.
            Parquet is the canonical analytical artifact (compact and typed);
            the CSV is kept for human inspection (open in Excel / Sheets) and
            tooling that does not read Parquet. Set to False to skip when
            iterating to save serialization time.
    """
    parquet_path = DATA_PROCESSED_DIR / f"{base_name}.parquet"
    df.to_parquet(parquet_path, index=False, engine="pyarrow", compression="snappy")

    print(f"\t✅ Processed dataset saved in 'data/processed' as:")
    print(f"\n\t\tParquet file: {base_name}.parquet")

    if also_csv:
        csv_path = DATA_PROCESSED_DIR / f"{base_name}.csv"
        df.to_csv(csv_path, index=False)
        print(f"\t\tCSV file:     {base_name}.csv")
