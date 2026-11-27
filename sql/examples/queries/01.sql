-- Grain: one returned row per paid order, in a deterministic order.
SELECT order_id, customer_id, amount_cents
FROM orders
WHERE status = 'paid'
ORDER BY created_at, order_id;
