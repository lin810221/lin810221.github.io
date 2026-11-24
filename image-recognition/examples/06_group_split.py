"""Offline executable teaching example; run from this directory."""
from vision_core import group_split,print_json

def main():
    records=[{'id':f'part-{g}-view-{v}','group':f'part-{g}'} for g in range(10) for v in range(3)]
    splits=group_split(records)
    groups={k:{r['group'] for r in rows} for k,rows in splits.items()}
    assert all(not groups[a]&groups[b] for a,b in [('train','valid'),('valid','test'),('train','test')])
    print_json({k:{'images':len(rows),'groups':sorted(groups[k])} for k,rows in splits.items()})

if __name__=='__main__': main()
