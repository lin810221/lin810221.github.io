WITH versions(customer_id,region,valid_from,valid_to) AS (
 VALUES (1,'north',DATE '2026-01-01',DATE '2026-11-02'),
        (1,'south',DATE '2026-11-02',NULL)
)
SELECT o.order_id,v.region
FROM orders o JOIN versions v ON o.customer_id=v.customer_id
 AND CAST(o.created_at AS DATE)>=v.valid_from
 AND (v.valid_to IS NULL OR CAST(o.created_at AS DATE)<v.valid_to)
ORDER BY o.order_id;
