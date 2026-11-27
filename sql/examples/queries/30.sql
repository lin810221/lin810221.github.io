WITH history(id,start_at,end_at) AS (
 VALUES (1,DATE '2026-01-01',DATE '2026-11-03'),(1,DATE '2026-11-02',NULL)
), checked AS (
 SELECT *,LAG(end_at) OVER (PARTITION BY id ORDER BY start_at) AS previous_end FROM history
)
SELECT id,start_at FROM checked WHERE previous_end>start_at;
