"""Replay a receipt; prove that the ticket version changes only once."""
from pathlib import Path
from tempfile import TemporaryDirectory
from integration_core import ALICE, REVIEWER, WorkflowStore


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        store = WorkflowStore(Path(folder) / "workorders.sqlite")
        preview = store.preview(ALICE, "T1")
        store.review(REVIEWER, preview["preview_id"], approve=True)
        first = store.commit(ALICE, preview["preview_id"], "stable-operation-key")
        replay = store.commit(ALICE, preview["preview_id"], "stable-operation-key")
        assert first == replay and store.ticket(ALICE, "T1")["version"] == 2
        assert len(store.audit()) == 1
        print("one effect, one receipt, one committed audit event")
