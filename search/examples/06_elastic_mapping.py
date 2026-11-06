"""Exercise the real Elasticsearch client serializer with a recording node."""
import json
from engine_clients import RecordingNode,elastic_mapping,recording_client

if __name__ == "__main__":
    with recording_client() as client:
        client.indices.create(index="learningnote-catalog-v1",mappings=elastic_mapping())
    call = RecordingNode.calls[-1]
    print("OFFLINE request:",call["method"],call["target"])
    print(json.loads(call["body"]))
    print("No Elasticsearch server was started or validated by this example.")
