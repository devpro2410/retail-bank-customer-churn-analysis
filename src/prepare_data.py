"""Clean the raw customer extract and build the DuckDB analytical database.

Pipeline:
    data/raw/Churn_Modelling.csv
        -> cleaning + feature engineering (pandas)
        -> data/churn.duckdb
               raw_customers : untouched raw load (audit trail)
               customers     : cleaned, enriched analysis table

Run:  python src/prepare_data.py
"""

from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "Churn_Modelling.csv"
DB_PATH = ROOT / "data" / "churn.duckdb"

# Pure identifiers: kept in the audit table, dropped from the analysis table.
ID_COLUMNS = ["RowNumber", "CustomerId", "Surname"]

AGE_BINS = [0, 30, 40, 50, 60, 200]
AGE_LABELS = ["<30", "30-39", "40-49", "50-59", "60+"]

CREDIT_BINS = [0, 580, 670, 740, 1000]
CREDIT_LABELS = ["poor", "fair", "good", "very_good"]


def balance_band(balance: float) -> str:
    if balance == 0:
        return "zero"
    if balance < 100_000:
        return "under_100k"
    if balance < 150_000:
        return "100k-150k"
    return "over_150k"


def tenure_band(years: int) -> str:
    if years <= 2:
        return "0-2 (new)"
    if years <= 7:
        return "3-7 (established)"
    return "8-10 (loyal)"


def products_group(n: int) -> str:
    return "3+" if n >= 3 else str(n)


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.drop(columns=ID_COLUMNS).copy()

    # Binary target so AVG(churned) == churn rate.
    df["churned"] = df["Exited"].astype("int8")

    df["age_band"] = pd.cut(df["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=False)
    df["credit_band"] = pd.cut(
        df["CreditScore"], bins=CREDIT_BINS, labels=CREDIT_LABELS, right=False
    )
    df["balance_band"] = df["Balance"].map(balance_band)
    df["zero_balance"] = (df["Balance"] == 0).astype("int8")
    df["tenure_band"] = df["Tenure"].map(tenure_band)
    df["products_group"] = df["NumOfProducts"].map(products_group)

    return df


def main() -> None:
    raw = pd.read_csv(RAW_CSV)
    print(f"Loaded {len(raw):,} rows x {raw.shape[1]} columns from {RAW_CSV.name}")
    print(f"Duplicate customers: {raw['CustomerId'].duplicated().sum()} | "
          f"missing values: {int(raw.isna().sum().sum())}")

    customers = clean(raw)

    con = duckdb.connect(str(DB_PATH))
    con.register("raw_df", raw)
    con.register("customers_df", customers)
    con.execute("CREATE OR REPLACE TABLE raw_customers AS SELECT * FROM raw_df")
    con.execute("CREATE OR REPLACE TABLE customers AS SELECT * FROM customers_df")

    n, rate = con.execute(
        "SELECT COUNT(*), ROUND(100.0 * AVG(churned), 1) FROM customers"
    ).fetchone()
    print(f"Built {DB_PATH.name}: customers table = {n:,} rows, "
          f"overall churn = {rate}%")
    con.close()


if __name__ == "__main__":
    main()
