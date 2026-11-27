-- The first page ends at (2026-11-02 09:00Z, 102); ties still advance safely.
SELECT order_id,created_at FROM orders
WHERE (created_at,order_id) > (TIMESTAMPTZ '2026-11-02 09:00:00+00',102)
ORDER BY created_at,order_id LIMIT 2;
