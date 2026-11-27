SELECT c.region,COUNT(*) AS paid_orders,SUM(o.amount_cents) AS paid_cents
FROM orders o JOIN customers c ON c.customer_id=o.customer_id
WHERE o.status='paid' GROUP BY c.region ORDER BY c.region;
