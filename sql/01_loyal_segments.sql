-- 01. Who are the most loyal customers? Segment by how often and how regularly they order.
-- Champions: 30+ orders and a median gap of 7 days or less (weekly habit).
-- Regulars: 15+ orders and median gap of 14 days or less. Everyone else: occasional.
WITH per_user AS (
    SELECT user_id,
           MAX(order_number)                                  AS orders,
           MEDIAN(days_since_prior_order)                     AS median_gap_days
    FROM orders GROUP BY user_id
)
SELECT
    CASE WHEN orders >= 30 AND median_gap_days <= 7  THEN 'Champions'
         WHEN orders >= 15 AND median_gap_days <= 14 THEN 'Regulars'
         ELSE 'Occasional' END                          AS segment,
    COUNT(*)                                            AS customers,
    ROUND(COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (), 3)    AS share_of_customers,
    SUM(orders)                                         AS orders,
    ROUND(SUM(orders) * 1.0 / SUM(SUM(orders)) OVER (), 3) AS share_of_orders,
    ROUND(MEDIAN(orders), 0)                            AS median_orders,
    ROUND(MEDIAN(median_gap_days), 1)                   AS median_gap_days
FROM per_user
GROUP BY 1
ORDER BY share_of_orders DESC;
