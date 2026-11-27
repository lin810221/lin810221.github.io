SELECT 'orders' AS relation_name, COUNT(*) AS rows, COUNT(DISTINCT order_id) AS keys FROM orders
UNION ALL
SELECT 'items', COUNT(*), COUNT(DISTINCT order_id) FROM items;
