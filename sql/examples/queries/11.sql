SELECT order_id,created_at,
 SUM(amount_cents) OVER (ORDER BY created_at,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rows_total,
 SUM(amount_cents) OVER (ORDER BY created_at RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS range_total,
 ROW_NUMBER() OVER (ORDER BY created_at,order_id) AS stable_rank
FROM orders ORDER BY created_at,order_id;
