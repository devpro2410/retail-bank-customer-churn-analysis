-- ---------------------------------------------------------------------------
-- 05 | Balance and tenure
-- Two relationships that run against the naive intuition: customers with a zero
-- balance churn LESS than funded ones (many are German customers who hold large
-- balances and leave), and tenure barely moves churn -- loyalty in years is not
-- protective here. Balance band is the primary cut; tenure band is included to
-- show how flat it is.
-- ---------------------------------------------------------------------------
SELECT
    balance_band                              AS balance_band,
    COUNT(*)                                  AS customers,
    SUM(churned)                              AS churned,
    ROUND(100.0 * AVG(churned), 1)            AS churn_rate_pct,
    ROUND(AVG(Tenure), 1)                     AS avg_tenure
FROM customers
GROUP BY balance_band
ORDER BY
    CASE balance_band
        WHEN 'zero' THEN 0
        WHEN 'under_100k' THEN 1
        WHEN '100k-150k' THEN 2
        ELSE 3
    END;
