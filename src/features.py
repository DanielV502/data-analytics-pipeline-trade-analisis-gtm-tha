"""Feature engineering and transformation functions for the trade pipeline."""

# Step 1: Column normalization

import pandas as pd

from config import HS_CODE_LENGTHS, MACRO_REGION_MAP, NUMERIC_COLUMNS


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize DataFrame column names to snake_case and remove special characters.

    Args:
        df (pd.DataFrame): Input DataFrame with arbitrary column names.

    Returns:
        pd.DataFrame: Copy of the DataFrame with lowercased, underscore-delimited
            column names free of non-alphanumeric characters.
    """
    df = df.copy()

    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w_]", "", regex=True)
    )

    return df


# Step 2: Data type conversion


def cast_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Cast DataFrame columns to their expected types and normalize HS product codes.

    Converts year to int, strips trailing '.0' from product codes, casts hs_code and
    trade_direction to category dtype, zero-pads product codes to their standard lengths
    (2 digits for HS2, 6 digits for HS6), and coerces numeric trade/weight/quantity columns.

    Args:
        df (pd.DataFrame): Input DataFrame after column normalization.

    Returns:
        pd.DataFrame: Copy with corrected dtypes and normalized product codes.
    """
    df = df.copy()

    df["year"] = df["year"].astype(int)

    df["productcode"] = (
        df["productcode"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    )

    df["hs_code"] = df["hs_code"].astype("category")

    df["trade_direction"] = df["trade_direction"].astype("category")

    # Normalize HS codes to standard lengths
    for hs_label, length in HS_CODE_LENGTHS.items():
        mask = df["hs_code"] == hs_label
        df.loc[mask, "productcode"] = df.loc[mask, "productcode"].str.zfill(length)

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# Step 3: Core trade value metric (actual USD)


def add_trade_value_usd(df: pd.DataFrame) -> pd.DataFrame:
    """Derive the 'trade_value_usd' column by converting thousands-USD values to full USD.

    Args:
        df (pd.DataFrame): DataFrame containing a 'tradevalue_in_1000_usd' column with no NaNs.

    Raises:
        ValueError: If 'tradevalue_in_1000_usd' contains any NaN values.

    Returns:
        pd.DataFrame: Copy with an added 'trade_value_usd' column (float).
    """
    df = df.copy()
    if df["tradevalue_in_1000_usd"].isna().any():
        raise ValueError(
            "tradevalue_in_1000_usd contains NaN values. "
            "Cannot compute trade_value_usd reliably."
        )

    df["trade_value_usd"] = df["tradevalue_in_1000_usd"] * 1000
    return df


def add_partner_macro_region(df: pd.DataFrame) -> pd.DataFrame:
    """Map the partner's World Bank region to a macro-region label (APAC, GRULAC, EMEA, etc.).

    Args:
        df (pd.DataFrame): DataFrame containing a 'partner_region' column with World Bank
            region strings.

    Returns:
        pd.DataFrame: Copy with an added 'partner_macro_region' category column.
            Unmapped regions are assigned 'OTHERS'.
    """
    df = df.copy()

    df["partner_macro_region"] = (
        df["partner_region"].map(MACRO_REGION_MAP).fillna("OTHERS")
    )

    df["partner_macro_region"] = df["partner_macro_region"].astype("category")
    return df


### Debug code
# print("'features.py' loaded")
