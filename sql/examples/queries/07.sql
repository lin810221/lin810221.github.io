SELECT c.customer_id, COUNT(o.order_id) AS paid_orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id AND o.status = 'paid'
GROUP BY c.customer_id
ORDER BY c.customer_id;
