"""Record PIT and search_after API shapes; this is not a server paging test."""
from engine_clients import RecordingNode,recording_client

if __name__ == "__main__":
    with recording_client() as client:
        pit = client.open_point_in_time(index="learningnote-catalog-v1",keep_alive="1m")["id"]
        try:
            client.search(pit={"id":pit,"keep_alive":"1m"},query={"term":{"tenant":"alpha"}},
                          sort=[{"point_id":"asc"}],size=2)
            # Synthetic cursor demonstrates serialization only. A live loop must
            # take it from the LAST HIT of the previous page and use fresh PIT IDs.
            client.search(pit={"id":pit,"keep_alive":"1m"},query={"term":{"tenant":"alpha"}},
                          sort=[{"point_id":"asc"}],search_after=[1002],size=2)
        finally: client.close_point_in_time(id=pit)
    print("OFFLINE operations",[(c["method"],c["target"]) for c in RecordingNode.calls])
