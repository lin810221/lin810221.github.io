"""Serialize bulk NDJSON and refresh=wait_for; no remote writes by default."""
import json
from dataclasses import asdict
from engine_clients import RecordingNode,recording_client
from search_core import RECIPE,fixture_vector,fixtures

if __name__ == "__main__":
    operations = []
    for doc in fixtures()[:2]:
        operations.extend([{"index":{"_index":"learningnote-catalog-v1","_id":str(doc.point_id)}},
            {**asdict(doc),"recipe":RECIPE,"embedding":fixture_vector(doc.title+" "+doc.body)}])
    with recording_client() as client: client.bulk(operations=operations,refresh="wait_for")
    call = RecordingNode.calls[-1]
    print("OFFLINE target",call["target"])
    print("NDJSON lines",len(call["body"].splitlines()))
    print("Live bulk delivery must inspect each item; HTTP 200 is insufficient.")
