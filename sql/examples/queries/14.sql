MERGE INTO orders AS target
USING (VALUES (102,4500),(105,1200)) AS source(order_id,new_cents)
ON target.order_id=source.order_id
WHEN MATCHED THEN UPDATE SET amount_cents=source.new_cents;
SELECT order_id,amount_cents FROM orders WHERE order_id IN (102,105) ORDER BY order_id;
