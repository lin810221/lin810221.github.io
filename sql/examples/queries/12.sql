SELECT order_id,customer_id,amount_cents,
 LAG(amount_cents) OVER (PARTITION BY customer_id ORDER BY created_at,order_id) AS previous_cents,
 SUM(amount_cents) OVER (PARTITION BY customer_id ORDER BY created_at,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS customer_cents
FROM orders ORDER BY customer_id,created_at,order_id;
