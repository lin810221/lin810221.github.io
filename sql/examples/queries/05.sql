SELECT order_id, CASE WHEN amount_cents >= 4000 THEN 'large' ELSE 'small' END AS band
FROM orders
WHERE status = 'paid' AND amount_cents BETWEEN 1000 AND 5000
ORDER BY order_id;
