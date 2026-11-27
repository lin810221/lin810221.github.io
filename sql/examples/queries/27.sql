WITH raw(id,amount) AS (VALUES (1,10),(1,10),(2,NULL)),
counts AS (SELECT COUNT(*) AS total,COUNT(amount) AS present,COUNT(DISTINCT id) AS unique_keys FROM raw)
SELECT total,present,unique_keys,present*1.0/NULLIF(total,0) AS completeness FROM counts;
