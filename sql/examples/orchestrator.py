"""A manual, single-process DAG runner; not a scheduling service."""
import time
from contracts import topological_sort,retry_delays

class TransientError(RuntimeError):pass

class TaskFailed(RuntimeError):
    def __init__(self,task,events):
        super().__init__('Task failed: '+task);self.task=task;self.events=events

def run_dag(dependencies,tasks,max_attempts=3,sleeper=time.sleep):
    order=topological_sort(dependencies)
    if set(tasks)!=set(dependencies):raise ValueError('Every task needs exactly one callable')
    delays=retry_delays(max_attempts);events=[];results={}
    for name in order:
        for attempt in range(1,max_attempts+1):
            try:
                results[name]=tasks[name]();events.append({'task':name,'attempt':attempt,'status':'success'});break
            except Exception as exc:
                events.append({'task':name,'attempt':attempt,'status':'failed','error_type':type(exc).__name__})
                if not isinstance(exc,TransientError) or attempt==max_attempts:raise TaskFailed(name,events) from exc
                sleeper(delays[attempt-1])
    return {'order':order,'results':results,'events':events}
