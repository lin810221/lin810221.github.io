WITH RECURSIVE tree(id,parent_id,name,depth) AS (
  SELECT id,parent_id,name,0 FROM staff WHERE parent_id IS NULL
  UNION ALL
  SELECT s.id,s.parent_id,s.name,t.depth+1
  FROM staff s JOIN tree t ON s.parent_id=t.id WHERE t.depth<10
)
SELECT id,name,depth FROM tree ORDER BY depth,id;
