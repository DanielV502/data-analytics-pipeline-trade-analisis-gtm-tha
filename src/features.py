"""Feature engineering and transformation functions for the trade pipeline.

Note:
    Transformation functions in this module mutate the input DataFrame in
    place and return it for chaining (the pipeline reassigns each result,
    so in-place mutation is intentional and avoids unnecessary copies).
    Callers that need to preserve the original should pass df.copy().
"""

# Step 1: Column normalization

import pandas as pd

from config import HS_CODE_LENGTHS, MACRO_REGION_MAP, NUMERIC_COLUMNS


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize DataFrame column names to snake_case and remove special characters.

    Args:
        df (pd.DataFrame): Input DataFrame with arbitrary column names.

    Returns:
        pd.DataFrame: The same DataFrame with lowercased, underscore-delimited
            column names free of non-alphanumeric characters (in-place).
    """
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
        pd.DataFrame: The same DataFrame with corrected dtypes and normalized
            product codes (in-place).
    """
    df["year"] = df["year"].astype(int)

    df["productcode"] = (
        df["productcode"].astype(str).str.removesuffix(".0").str.strip()
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
        ValueError: If 'tradevalue_in_1000_usd' is missing from the DataFrame
            or contains any NaN values.

    Returns:
        pd.DataFrame: The same DataFrame with an added 'trade_value_usd'
            column (float, in-place).
    """
    if "tradevalue_in_1000_usd" not in df.columns:
        raise ValueError(
            "Required column 'tradevalue_in_1000_usd' not found. "
            "Cannot compute trade_value_usd."
        )
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
        pd.DataFrame: The same DataFrame with an added 'partner_macro_region'
            category column (in-place). Unmapped regions are assigned 'OTHERS'.
    """
    df["partner_macro_region"] = (
        df["partner_region"].map(MACRO_REGION_MAP).fillna("OTHERS")
    )

    df["partner_macro_region"] = df["partner_macro_region"].astype("category")
    return df
