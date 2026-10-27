-- 03. Build the pilot cohort: Champions, each with a personal "hero product" (the item they
-- reorder most), randomly split into test (gets the gesture) and control (doesn't).
-- hash() gives a stable, reproducible 50/50 split.
WITH per_user AS (
    SELECT user_id, MAX(order_number) AS orders, MEDIAN(days_since_prior_order) AS gap
    FROM orders GROUP BY user_id
),
champs AS (SELECT user_id, orders FROM per_user WHERE orders >= 30 AND gap <= 7),
fav AS (
    SELECT o.user_id, p.product_name, COUNT(*) AS times,
           ROW_NUMBER() OVER (PARTITION BY o.user_id ORDER BY COUNT(*) DESC, p.product_name) AS rk
    FROM order_items op JOIN orders o USING (order_id) JOIN products p USING (product_id)
    WHERE o.user_id IN (SELECT user_id FROM champs)
    GROUP BY o.user_id, p.product_name
)
SELECT c.user_id, c.orders, f.product_name AS hero_product, f.times AS hero_times_bought,
       CASE WHEN hash(c.user_id) % 2 = 0 THEN 'test' ELSE 'control' END AS arm
FROM champs c JOIN fav f ON f.user_id = c.user_id AND f.rk = 1
ORDER BY c.user_id;
