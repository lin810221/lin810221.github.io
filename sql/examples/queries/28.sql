WITH by_item AS (SELECT order_id,SUM(quantity*unit_cents) AS item_cents FROM items GROUP BY order_id)
SELECT o.order_id,o.amount_cents,i.item_cents,o.amount_cents-i.item_cents AS difference
FROM orders o JOIN by_item i ON o.order_id=i.order_id
WHERE o.amount_cents<>i.item_cents;
