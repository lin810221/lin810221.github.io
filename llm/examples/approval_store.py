"""Atomic local approval and publication ledger. Does not deliver email or call external services."""
import hashlib
import json
import sqlite3
import uuid


class ApprovalStore:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("CREATE TABLE IF NOT EXISTS proposals (id TEXT PRIMARY KEY, owner TEXT, digest TEXT, body TEXT, status TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS publications (proposal_id TEXT PRIMARY KEY, body TEXT)")
        self.db.commit()

    def propose(self, owner: str, answer: str, sources: list[str]) -> dict:
        if not owner or not answer.strip() or not sources:
            raise ValueError("Proposal needs owner, answer and sources")
        body = json.dumps({"owner": owner, "answer": answer, "sources": sources}, ensure_ascii=False, sort_keys=True)
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
        proposal_id = uuid.uuid4().hex
        with self.db:
            self.db.execute("INSERT INTO proposals VALUES (?,?,?,?,?)", (proposal_id,owner,digest,body,"pending"))
        return self.get(owner, proposal_id)

    def get(self, owner: str, proposal_id: str) -> dict:
        row = self.db.execute("SELECT * FROM proposals WHERE id=? AND owner=?", (proposal_id,owner)).fetchone()
        if row is None:
            raise KeyError("Proposal not found for this owner")
        return {**dict(row), "body": json.loads(row["body"])}

    def resolve(self, owner: str, proposal_id: str, digest: str, approved: bool) -> dict:
        if type(approved) is not bool:
            raise ValueError("approved must be a boolean")
        target = "approved" if approved else "rejected"
        self.db.execute("BEGIN IMMEDIATE")
        try:
            proposal = self.get(owner, proposal_id)
            if proposal["digest"] != digest:
                raise ValueError("Approval does not match this content version")
            if proposal["status"] not in ("pending", target):
                raise ValueError("A completed decision cannot be reversed")
            if proposal["status"] == "pending":
                if approved:
                    self.db.execute("INSERT INTO publications VALUES (?,?)", (proposal_id,json.dumps(proposal["body"],ensure_ascii=False)))
                self.db.execute("UPDATE proposals SET status=? WHERE id=?", (target,proposal_id))
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        return self.get(owner, proposal_id)

    def publication_count(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM publications").fetchone()[0]

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
