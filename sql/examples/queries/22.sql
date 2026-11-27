WITH source(id,seq,value) AS (VALUES (1,10,'old'),(1,11,'new'),(2,9,'other')),
ranked AS (SELECT *,ROW_NUMBER() OVER (PARTITION BY id ORDER BY seq DESC) AS winner FROM source)
SELECT id,seq,value FROM ranked WHERE winner=1 ORDER BY id;
