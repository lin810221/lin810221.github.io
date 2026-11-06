"""Default is offline; --live performs a read-only query on your own index."""
import argparse
import os
from elasticsearch import Elasticsearch
from engine_clients import RecordingNode,elastic_query,recording_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live",action="store_true")
    args = parser.parse_args()
    if args.live:
        endpoint = os.environ.get("SEARCH_ES_URL","http://127.0.0.1:9200")
        options = {"api_key":os.environ["SEARCH_ES_API_KEY"]} if os.environ.get("SEARCH_ES_API_KEY") else {}
        if os.environ.get("SEARCH_ES_CA"): options["ca_certs"] = os.environ["SEARCH_ES_CA"]
        with Elasticsearch(endpoint,request_timeout=5,**options) as client:
            response = client.search(index=os.environ.get("SEARCH_ES_INDEX","learningnote-catalog-v1"),body=elastic_query("alpha","usb hub"))
            print(response["hits"])
    else:
        with recording_client() as client: client.search(index="learningnote-catalog-v1",body=elastic_query("alpha","usb hub"))
        print("OFFLINE serialized request",RecordingNode.calls[-1]["body"].decode())
