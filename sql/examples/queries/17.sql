EXPLAIN ANALYZE SELECT customer_id,SUM(amount_cents)
FROM orders WHERE status='paid' GROUP BY customer_id;
