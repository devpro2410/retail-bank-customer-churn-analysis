"""Export Tableau-ready extracts to tableau/extracts/.

Two kinds of extracts are produced:
  customers_enriched.csv - the full cleaned row-level table, for free-form
                           exploration and the dashboard's detail views
  agg_*.csv              - small pre-aggregated cuts that back the headline
                           dashboard tiles (fast to load on Tableau Public)

Run:  python src/export_tableau.py      (after src/prepare_data.py)
"""

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "churn.duckdb"
OUT_DIR = ROOT / "tableau" / "extracts"

AGGREGATES = {
    "agg_geography": """
        SELECT Geography AS geography,
               COUNT(*) AS customers,
               SUM(churned) AS churned,
               ROUND(100.0 * AVG(churned), 2) AS churn_rate_pct
        FROM customers GROUP BY Geography ORDER BY churn_rate_pct DESC
    """,
    "agg_products_activity": """
        SELECT products_group AS products,
               CASE WHEN IsActiveMember = 1 THEN 'active' ELSE 'inactive' END AS membership,
               COUNT(*) AS customers,
               SUM(churned) AS churned,
               ROUND(100.0 * AVG(churned), 2) AS churn_rate_pct
        FROM customers GROUP BY products_group, IsActiveMember
        ORDER BY products, membership
    """,
    "agg_age_band": """
        SELECT age_band::VARCHAR AS age_band,
               COUNT(*) AS customers,
               SUM(churned) AS churned,
               ROUND(100.0 * AVG(churned), 2) AS churn_rate_pct
        FROM customers GROUP BY age_band ORDER BY age_band
    """,
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH), read_only=True)

    row_level = OUT_DIR / "customers_enriched.csv"
    con.execute(f"COPY customers TO '{row_level}' (HEADER, DELIMITER ',')")
    print(f"Wrote {row_level.relative_to(ROOT)}")

    for name, query in AGGREGATES.items():
        out = OUT_DIR / f"{name}.csv"
        con.execute(query).df().to_csv(out, index=False)
        print(f"Wrote {out.relative_to(ROOT)}")

    con.close()


if __name__ == "__main__":
    main()
