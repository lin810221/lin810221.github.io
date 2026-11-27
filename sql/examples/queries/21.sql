WITH raw(id,amount) AS (VALUES ('001','12.50'),('002','oops'),('003',NULL)),
staging AS (SELECT id,amount,TRY_CAST(amount AS DECIMAL(12,2)) AS parsed FROM raw)
SELECT id,amount,parsed,
 CASE WHEN amount IS NULL THEN 'missing' WHEN parsed IS NULL THEN 'invalid' ELSE 'valid' END AS result
FROM staging ORDER BY id;
