-- ---------------------------------------------------------------------------
-- 04 | Demographic drivers: age and gender
-- Churn is strongly non-linear in age -- it peaks in the 50-59 band rather than
-- rising monotonically -- and women churn more than men. GROUPING SETS returns
-- both cuts in one pass; `dimension` labels which cut each row belongs to.
-- ---------------------------------------------------------------------------
WITH segmented AS (
    SELECT
        CASE
            WHEN GROUPING(age_band) = 0 THEN 'age_band'
            WHEN GROUPING(Gender) = 0   THEN 'gender'
        END                                       AS dimension,
        COALESCE(age_band::VARCHAR, Gender)       AS segment,
        COUNT(*)                                  AS customers,
        SUM(churned)                              AS churned,
        ROUND(100.0 * AVG(churned), 1)            AS churn_rate_pct
    FROM customers
    GROUP BY GROUPING SETS ((age_band), (Gender))
)
SELECT *
FROM segmented
ORDER BY dimension, churn_rate_pct DESC;
