"""Invoke an idempotent DataHarbor DAG manually; use an external scheduler to automate it."""
from pathlib import Path
import argparse,json
from orchestrator import run_dag
from pipeline import process_batch,read_current
from run_lab import load_batch

def workflow(workspace):
    graph={'load_first':[],'apply_changes':['load_first'],'verify_snapshot':['apply_changes']}
    tasks={'load_first':lambda:process_batch(workspace,load_batch(1)),
           'apply_changes':lambda:process_batch(workspace,load_batch(2)),
           'verify_snapshot':lambda:read_current(workspace)}
    return run_dag(graph,tasks)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workspace',required=True,type=Path);args=parser.parse_args()
    print(json.dumps(workflow(args.workspace),ensure_ascii=False,indent=2))
