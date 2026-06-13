# Data Dictionary

Source: **Bank Customer Churn ("Churn Modelling")** dataset — 10,000 retail-bank
customers across France, Spain and Germany, with a flag for whether each customer
left the bank. Widely circulated on Kaggle for churn analysis.

File used: `Churn_Modelling.csv` (10,000 rows, 14 columns, comma-separated).

## Identifiers (dropped from the analysis table)

| Column | Type | Description |
|---|---|---|
| `RowNumber` | int | Row index — no analytical value |
| `CustomerId` | int | Unique customer key — no analytical value |
| `Surname` | str | Customer surname — identifier, not used |

These are kept in the `raw_customers` audit table but removed from the cleaned
`customers` table.

## Customer attributes

| Column | Type | Description |
|---|---|---|
| `CreditScore` | int | Credit score (350–850 in this data) |
| `Geography` | cat | Country of residence: France / Spain / Germany |
| `Gender` | cat | Female / Male |
| `Age` | int | Customer age in years (18–92) |
| `Tenure` | int | Years as a customer (0–10) |
| `Balance` | float | Account balance; **0 for ~36% of customers** (see note) |
| `NumOfProducts` | int | Number of bank products held (1–4) |
| `HasCrCard` | int | Holds a credit card? (1 / 0) |
| `IsActiveMember` | int | Active member flag (1 / 0) |
| `EstimatedSalary` | float | Estimated annual salary |

## Target

| Column | Type | Description |
|---|---|---|
| `Exited` | int | **1 = customer churned (left the bank), 0 = retained** |

## Engineered fields (added in `src/prepare_data.py`)

| Field | Description |
|---|---|
| `churned` | `Exited` as an integer flag, so `AVG(churned)` is the churn rate |
| `age_band` | `<30`, `30-39`, `40-49`, `50-59`, `60+` |
| `balance_band` | `zero`, `under_100k`, `100k-150k`, `over_150k` |
| `zero_balance` | flag for `Balance = 0` |
| `tenure_band` | `0-2 (new)`, `3-7 (established)`, `8-10 (loyal)` |
| `products_group` | `1`, `2`, `3+` |
| `credit_band` | `poor`, `fair`, `good`, `very_good` |

## Notes & quality observations

- **No missing values and no duplicate customers** — the extract is clean; the
  work is in framing and engineering, not repair.
- **`Balance = 0` for ~36% of customers** is a real state (no funds parked at the
  bank), not missing data. It is kept and flagged; notably these customers churn
  *less*, not more.
- **`NumOfProducts` 3 and 4** are tiny cohorts (≈300 and ≈60 customers) that
  churn at 80–100%. Real signal, but report with the small sample size attached
  rather than as a headline rate.
- This is a snapshot, not a time series — there is no event date, so the analysis
  is cross-sectional (who has churned), not survival/time-to-churn.
