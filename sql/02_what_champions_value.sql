-- 02. What do Champions value? Their most reordered departments vs everyone else's,
-- to decide what a surprise should be (a premium version of what they already love).
WITH per_user AS (
    SELECT user_id, MAX(order_number) AS orders, MEDIAN(days_since_prior_order) AS gap
    FROM orders GROUP BY user_id
),
champs AS (SELECT user_id FROM per_user WHERE orders >= 30 AND gap <= 7),
items AS (
    SELECT o.user_id, d.department, op.reordered,
           CASE WHEN c.user_id IS NOT NULL THEN 'Champions' ELSE 'Others' END AS grp
    FROM order_items op
    JOIN orders o USING (order_id)
    JOIN products p USING (product_id)
    JOIN departments d USING (department_id)
    LEFT JOIN champs c ON c.user_id = o.user_id
)
SELECT department,
       ROUND(AVG(reordered) FILTER (WHERE grp = 'Champions'), 3)                       AS champions_reorder_rate,
       ROUND(COUNT(*) FILTER (WHERE grp = 'Champions') * 1.0
             / SUM(COUNT(*) FILTER (WHERE grp = 'Champions')) OVER (), 3)              AS champions_share_of_items,
       ROUND(COUNT(*) FILTER (WHERE grp = 'Others') * 1.0
             / SUM(COUNT(*) FILTER (WHERE grp = 'Others')) OVER (), 3)                 AS others_share_of_items
FROM items
GROUP BY department
ORDER BY champions_share_of_items DESC
LIMIT 10;
