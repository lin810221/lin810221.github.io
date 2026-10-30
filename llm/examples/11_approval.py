"""Simulated approval inside a temporary local SQLite ledger, with no outbound action."""
from pathlib import Path
from tempfile import TemporaryDirectory
from approval_store import ApprovalStore

if __name__ == "__main__":
    with TemporaryDirectory() as folder, ApprovalStore(Path(folder) / "approval.sqlite") as store:
        proposal = store.propose("student", "Agent 透過工具工作。[D1]", ["D1"])
        print("模擬待審：", proposal["status"], proposal["digest"])
        store.resolve("student", proposal["id"], proposal["digest"], approved=True)
        store.resolve("student", proposal["id"], proposal["digest"], approved=True)
        print("相同核准重送兩次，僅一份本機發布紀錄：", store.publication_count())
