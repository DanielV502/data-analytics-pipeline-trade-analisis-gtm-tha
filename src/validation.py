"""Schema, type, value, and business rule validation for the trade pipeline.

Convention:
    - validate_schema, validate_dtypes, validate_values raise on failure
      (fatal: missing columns, wrong dtypes, negative trade values, etc.).
    - validate_business_rules emits warnings only (advisory: HS code length,
      unexpected trade direction labels). Pipeline continues regardless.
"""

import pandas as pd
import warnings

from config import ALLOWED_TRADE_DIRECTIONS, HS_CODE_LENGTHS, REQUIRED_COLUMNS


def validate_schema(df: pd.DataFrame) -> None:
    """Validate that all required columns are present in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Raises:
        ValueError: If any required column is missing.
    """
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


# Step 2: Type validation


def validate_dtypes(df: pd.DataFrame) -> None:
    """Validate that key columns have the expected data types.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Raises:
        TypeError: If 'year' is not integer or 'trade_value_usd' is not numeric.
    """
    if not pd.api.types.is_integer_dtype(df["year"]):
        raise TypeError("Column 'year' must be integer")

    if not pd.api.types.is_numeric_dtype(df["trade_value_usd"]):
        raise TypeError("Column 'trade_value_usd' must be numeric")


# Step 3: Value validation


def validate_values(df: pd.DataFrame) -> None:
    """Validate that trade values and product codes contain no invalid entries.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Raises:
        ValueError: If negative trade values or missing product codes are detected.
    """
    if (df["trade_value_usd"] < 0).any():
        raise ValueError("Negative trade values detected")

    if df["productcode"].isna().any():
        raise ValueError("Missing product codes detected")


# Step 4: Business rules (WITS / HS)


def validate_business_rules(df: pd.DataFrame) -> None:
    """Validate business rules without stopping the pipeline.

    Emits warnings if unexpected values are detected, allowing the pipeline to
    continue while surfacing data quality issues for review.

    Args:
        df (pd.DataFrame): DataFrame to validate.
    """

    # Step 4a: Validate HS product code length (HS2 = 2 digits, HS6 = 6 digits)
    lengths = df["productcode"].str.len()
    invalid_hs = ~lengths.isin(HS_CODE_LENGTHS.values())

    if invalid_hs.any():
        warnings.warn(
            f"{invalid_hs.sum()} rows contain non-standard HS2 or HS6 product codes and were retained for transparency.",
            UserWarning,
        )

    # Step 4b: Validate trade direction values
    invalid_directions = set(df["trade_direction"].unique()) - ALLOWED_TRADE_DIRECTIONS

    if invalid_directions:
        warnings.warn(
            f"Unexpected trade_direction values detected: {invalid_directions}",
            UserWarning,
        )
