-- ---------------------------------------------------------------------------
-- 02 | Churn by geography (and gender within geography)
-- Where is attrition concentrated? Germany is the standout cohort; splitting by
-- gender shows the risk is compounded, not uniform, within each country.
-- ---------------------------------------------------------------------------
SELECT
    Geography                                 AS geography,
    Gender                                    AS gender,
    COUNT(*)                                  AS customers,
    SUM(churned)                              AS churned,
    ROUND(100.0 * AVG(churned), 1)            AS churn_rate_pct,
    ROUND(AVG(Balance), 0)                    AS avg_balance
FROM customers
GROUP BY GROUPING SETS ((Geography), (Geography, Gender))
ORDER BY geography, gender NULLS FIRST;
