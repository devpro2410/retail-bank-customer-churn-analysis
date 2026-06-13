# Tableau Dashboard — Customer Churn & Retention Priorities

The dashboard is built on the extracts in `tableau/extracts/`
(regenerate them with `python src/export_tableau.py`).

**Data source:** connect `customers_enriched.csv` as the primary source. The
small `agg_*.csv` files are optional pre-aggregated alternatives if Tableau
Public feels slow on the row-level file.

## Calculated fields

| Field | Formula |
|---|---|
| `Churn Rate` | `SUM([Churned]) / COUNT([Churned])` (format: percentage, 1 dp) |
| `Portfolio Churn` | `{ FIXED : SUM([Churned]) } / { FIXED : COUNT([Churned]) }` — the true 20.4% baseline for reference lines (a plain "Average" line would wrongly average the segment rates) |
| `Risk Cohort` | `IF [Geography] = "Germany" AND [IsActiveMember] = 0 THEN "Germany / inactive" ELSE "Other" END` |

## Worksheets

1. **KPI tiles** — total customers, churned customers, `Churn Rate`,
   % active. One sheet per tile, text mark only. (Optional — these numbers also
   appear in the charts, so skip if you prefer a cleaner layout.)
2. **Churn by geography** — `Geography` on columns, `Churn Rate` on rows, bars;
   add a `Portfolio Churn` reference line so Germany visibly clears the baseline.
   Colour Germany red, the rest grey.
3. **Product × activity (heat or bars)** — `products` on columns, `membership`
   on colour, `Churn Rate` on rows. Shows the two-product sweet spot and the
   inactive penalty in one view.
4. **Age band** — `age_band` on columns (sorted `<30 → 60+`), `Churn Rate` on
   rows, bars; reference line at `Portfolio Churn`. The 50–59 peak is the story.
5. **Demographic risk** — `Geography` on columns, `Gender` on colour,
   `Churn Rate` on rows — surfaces German women as the highest-risk group.

## Dashboard layout

- Size: 1366 × 768 (fixed, so it renders identically when published).
- Title strip on top; 2×2 grid of the four charts below.
- Global filter: `age_band` (or `Geography`) applied to **All Using This Data
  Source** so one control re-slices everything.
- Add a one-line takeaway under each chart title (small grey text) — e.g.
  *"Germany churns at 2× the other markets."*

## Publish

`File → Save to Tableau Public As…`, then paste the public link and a screenshot
(`tableau/dashboard.png`) into the main README's Dashboard section.
