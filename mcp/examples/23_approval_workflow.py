"""Model tools cannot mark a preview approved; a trusted reviewer does that."""
from pathlib import Path
from tempfile import TemporaryDirectory
from integration_core import ALICE, REVIEWER, WorkflowStore


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        store = WorkflowStore(Path(folder) / "workorders.sqlite")
        preview = store.preview(ALICE, "T1")
        try:
            store.commit(ALICE, preview["preview_id"], "close-1")
        except PermissionError:
            print("pending preview cannot execute")
        # This method belongs to a trusted operator UI, not the MCP tool registry.
        store.review(REVIEWER, preview["preview_id"], approve=True)
        print(store.commit(ALICE, preview["preview_id"], "close-1"))
