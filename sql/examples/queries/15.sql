-- Repeated customer attributes live in a dimension instead of each order line.
SELECT o.order_id,c.region,o.amount_cents
FROM orders o JOIN customers c ON o.customer_id=c.customer_id
WHERE o.status='paid' ORDER BY o.order_id;
