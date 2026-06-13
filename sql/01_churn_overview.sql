-- ---------------------------------------------------------------------------
-- 01 | Portfolio overview KPIs
-- How large is the customer base, and what does churn look like overall?
-- ---------------------------------------------------------------------------
SELECT
    COUNT(*)                                          AS total_customers,
    SUM(churned)                                      AS churned_customers,
    ROUND(100.0 * AVG(churned), 1)                    AS churn_rate_pct,
    ROUND(AVG(Age), 1)                                AS avg_age,
    ROUND(AVG(Balance), 0)                            AS avg_balance,
    ROUND(100.0 * AVG(IsActiveMember), 1)             AS pct_active,
    ROUND(100.0 * AVG(CASE WHEN Geography = 'Germany' THEN 1 ELSE 0 END), 1)
                                                      AS pct_german
FROM customers;
