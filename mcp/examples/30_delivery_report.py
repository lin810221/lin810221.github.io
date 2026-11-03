"""Generate a real acceptance report in a caller-selected or temporary folder."""
from contextlib import closing
from importlib import import_module
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse
import json
import anyio
from integration_core import ALICE, BOB, REVIEWER, WorkflowStore, search_notes


async def deliver(destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    store = WorkflowStore(destination / "workorders.sqlite")
    # An existing closed T1 is not reset: use a fresh destination for each run.
    demonstration = await import_module("29_capstone").demonstrate(store)
    report = {"sdk": version("mcp"), "transport": "in-process", "provider_api_calls": 0,
              "cross_tenant_notes": search_notes(ALICE, "Private beta"),
              "beta_ticket": store.ticket(BOB, "T1"), **demonstration}
    (destination / "acceptance.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    assert report["cross_tenant_notes"] == [] and report["beta_ticket"]["status"] == "open"
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output:
        print(anyio.run(deliver, args.output))
    else:
        with TemporaryDirectory() as folder:
            print(anyio.run(deliver, Path(folder)))
