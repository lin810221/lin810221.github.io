"""Deliver real local source/index artifacts and verify restore into a NEW index."""
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse
import json
import apsw
from catalog_project import ALPHA,BETA,CatalogSearch,build_demo
from qdrant_store import VectorStore,rebuild_from_source
from source_store import SourceStore

def deliver(destination):
    destination = Path(destination)
    destination.mkdir(parents=True,exist_ok=False)
    source,vectors = build_demo(destination/"source.sqlite",destination/"vectors")
    try:
        before = CatalogSearch(source,vectors,ALPHA).search("usb hub",3)
        beta = CatalogSearch(source,vectors,BETA).search("usb hub",3)
        source.backup(destination/"source-backup.sqlite")
        expected = [hit["point_id"] for hit in before["hits"]]
    finally:
        vectors.close(); source.close()
    with SourceStore(destination/"source-backup.sqlite") as restored, VectorStore(destination/"restored-vectors") as rebuilt:
        rebuilt_points = rebuild_from_source(restored,rebuilt)
        after = CatalogSearch(restored,rebuilt,ALPHA).search("usb hub",3)
        assert [hit["point_id"] for hit in after["hits"]] == expected
    report = {"sqlite":apsw.sqlitelibversion(),"apsw":apsw.apswversion(),
              "qdrant_client":version("qdrant-client"),"faiss_cpu":version("faiss-cpu"),
              "mode":"real SQLite FTS5 and Qdrant Local; no external service",
              "alpha_ids":expected,"beta_ids":[hit["point_id"] for hit in beta["hits"]],
              "rebuilt_points":rebuilt_points,"restore_matches":True,"model_api_calls":0}
    (destination/"acceptance.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    if args.output: print(deliver(args.output))
    else:
        with TemporaryDirectory() as folder: print(deliver(Path(folder)/"run"))
