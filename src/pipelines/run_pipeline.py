"""Pipeline entry point: load, transform, validate, and persist trade data."""

try:
    from IPython.display import display
except ImportError:
    display = print

from dataset import load_all_trade_data
from features import (
    normalize_columns,
    cast_dtypes,
    add_trade_value_usd,
    add_partner_macro_region,
)
from validation import (
    validate_schema,
    validate_dtypes,
    validate_values,
    validate_business_rules,
)
from services.io import save_processed_dataset


def run():
    """Execute the full trade data pipeline: load → transform → validate → persist.

    Returns:
        pd.DataFrame: Fully processed trade DataFrame.
    """
    df = load_all_trade_data()
    # Transformations
    df = normalize_columns(df)
    df = cast_dtypes(df)
    df = add_trade_value_usd(df)
    df = add_partner_macro_region(df)

    # Validations
    validate_schema(df)
    validate_dtypes(df)
    validate_values(df)
    validate_business_rules(df)

    # Persistence
    save_processed_dataset(df, "trade_gtm_tha_2017_2025_processed")

    return df


if __name__ == "__main__":
    df = run()
    print(f"\n\t✅ Dataset shape: Rows = {df.shape[0]}, Columns = {df.shape[1]}\n")
    display(df.head())
    print("\n\t✅ Pipeline executed successfully\n")
