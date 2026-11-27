WITH item_totals AS (
  SELECT order_id, SUM(quantity * unit_cents) AS gross_cents FROM items GROUP BY order_id
), refund_totals AS (
  SELECT order_id, SUM(amount_cents) AS refund_cents FROM refunds GROUP BY order_id
)
SELECT o.order_id, i.gross_cents, COALESCE(r.refund_cents,0) AS refund_cents,
       i.gross_cents - COALESCE(r.refund_cents,0) AS net_cents
FROM orders o JOIN item_totals i ON i.order_id=o.order_id
LEFT JOIN refund_totals r ON r.order_id=o.order_id
WHERE o.status='paid' ORDER BY o.order_id;
