"""I/O service for persisting processed trade datasets."""

import pandas as pd
from config import DATA_PROCESSED_DIR


def save_processed_dataset(df: pd.DataFrame, base_name: str) -> None:
    """Save the processed DataFrame to both Parquet and CSV formats.

    Args:
        df (pd.DataFrame): Processed trade DataFrame to persist.
        base_name (str): Base filename without extension (e.g., 'trade_gtm_tha_2017_2025_processed').
            Output files will be saved as <base_name>.parquet and <base_name>.csv under
            data/processed/.
    """
    parquet_path = DATA_PROCESSED_DIR / f"{base_name}.parquet"
    csv_path = DATA_PROCESSED_DIR / f"{base_name}.csv"

    df.to_parquet(parquet_path, index=False, engine="pyarrow", compression="snappy")
    df.to_csv(csv_path, index=False)
    print(f"\t✅ Processed dataset saved in 'data/processed' as:")
    print(f"\n\t\tParquet file: {base_name}.parquet")
    print(f"\t\tCSV file:     {base_name}.csv")


### Debug code
# print("'io.py' loaded")
