SELECT customer_id, COUNT(*) AS paid_orders, SUM(amount_cents) AS paid_cents
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(amount_cents) >= 4000
ORDER BY customer_id;
