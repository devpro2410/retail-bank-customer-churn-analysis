-- ---------------------------------------------------------------------------
-- 03 | Product holdings and engagement
-- Two of the strongest, most actionable levers: how many products a customer
-- holds, and whether they are an active member. The 3+ product cohort is tiny
-- but churns almost completely -- flagged here with its customer count so the
-- rate is never read without the sample size.
-- ---------------------------------------------------------------------------
SELECT
    products_group                            AS products,
    CASE WHEN IsActiveMember = 1 THEN 'active' ELSE 'inactive' END AS membership,
    COUNT(*)                                  AS customers,
    SUM(churned)                              AS churned,
    ROUND(100.0 * AVG(churned), 1)            AS churn_rate_pct
FROM customers
GROUP BY products_group, IsActiveMember
ORDER BY products_group, membership;
