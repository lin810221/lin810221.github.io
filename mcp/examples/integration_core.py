"""Original course domain layer. No network or model API calls.

The SQLite workflow is deliberately small: authorization, immutable previews,
separate reviewer identity, optimistic locking and receipts share one database.
"""
from __future__ import annotations

from contextlib import contextmanager, closing
from dataclasses import dataclass
from hashlib import sha256
from ipaddress import ip_address
from pathlib import Path
from typing import Callable
from urllib.parse import urlsplit
import json
import secrets
import sqlite3
import time


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str
    scopes: frozenset[str]
    issuer: str = "https://issuer.example.invalid"


ALICE = Principal("alpha", "alice", frozenset({"notes:read", "tickets:read", "tickets:write"}))
REVIEWER = Principal("alpha", "reviewer", frozenset({"tickets:review"}))
BOB = Principal("beta", "bob", ALICE.scopes)
NOTES = [
    {"id": "N1", "tenant": "alpha", "text": "MCP tools use validated input contracts."},
    {"id": "N2", "tenant": "alpha", "text": "Closing a ticket requires a reviewed preview."},
    {"id": "N3", "tenant": "beta", "text": "Private beta incident report."},
]


def require(principal: Principal, scope: str) -> None:
    if not principal.tenant or not principal.subject or scope not in principal.scopes:
        raise PermissionError("Missing identity or required scope")


def search_notes(principal: Principal, query: str, limit: int = 5) -> list[dict]:
    require(principal, "notes:read")
    if not isinstance(query, str) or not 1 <= len(query.strip()) <= 100:
        raise ValueError("Query must contain 1 to 100 characters")
    if type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError("Limit must be an integer from 1 to 10")
    return [{"id": n["id"], "text": n["text"]} for n in NOTES
            if n["tenant"] == principal.tenant and query.casefold() in n["text"].casefold()][:limit]


def cache_key(principal: Principal, revision: str, method: str, args: dict) -> str:
    # Token values never appear in keys; authorization and schema revisions do.
    envelope = [principal.issuer, principal.tenant, principal.subject,
                sorted(principal.scopes), revision, method, args]
    return sha256(json.dumps(envelope, sort_keys=True).encode()).hexdigest()


def endpoint_policy(url: str, allowed_hosts: set[str], resolved_ips: list[str]) -> str:
    parts = urlsplit(url)
    if (parts.scheme != "https" or parts.hostname not in allowed_hosts
            or parts.username or parts.password or parts.fragment or parts.port not in (None, 443)):
        raise ValueError("Endpoint must be an approved HTTPS origin")
    if not resolved_ips or any(not ip_address(value).is_global for value in resolved_ips):
        raise ValueError("Every resolved address must be public")
    # This validates a resolution snapshot; production must pin that resolution
    # at connect time and repeat checks for each redirect, or disable redirects.
    return url


def safe_file(root: Path, relative: str, max_bytes: int = 4096) -> str:
    root = root.resolve(strict=True)
    candidate = Path(relative)
    if candidate.is_absolute():
        raise PermissionError("A relative document path is required")
    target = (root / candidate).resolve(strict=True)
    if not target.is_relative_to(root) or target.suffix != ".txt":
        raise PermissionError("Only text documents inside the approved root")
    # A bounded read also enforces the size limit if a file grows after stat().
    with target.open("rb") as stream:
        data = stream.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("Document exceeds the byte limit")
    return data.decode("utf-8")


def audit_event(**fields) -> dict:
    allowed = {"request_id", "tenant", "subject", "tool", "status", "duration_ms", "error_code"}
    # Whitelist metadata; never include credentials, tool arguments or documents.
    return {key: value for key, value in fields.items() if key in allowed}


class WorkflowStore:
    def __init__(self, path: Path, clock: Callable[[], float] = time.time):
        self.path, self.clock = Path(path), clock
        with closing(self.connect()) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS tickets (
                  tenant TEXT NOT NULL, id TEXT NOT NULL, status TEXT NOT NULL,
                  version INTEGER NOT NULL, PRIMARY KEY(tenant,id));
                CREATE TABLE IF NOT EXISTS previews (
                  id TEXT PRIMARY KEY, issuer TEXT NOT NULL, tenant TEXT NOT NULL,
                  subject TEXT NOT NULL, ticket_id TEXT NOT NULL, version INTEGER NOT NULL,
                  payload TEXT NOT NULL, digest TEXT NOT NULL, state TEXT NOT NULL,
                  expires REAL NOT NULL, reviewer TEXT);
                CREATE TABLE IF NOT EXISTS receipts (
                  issuer TEXT NOT NULL, tenant TEXT NOT NULL, subject TEXT NOT NULL,
                  key TEXT NOT NULL, digest TEXT NOT NULL, result TEXT NOT NULL,
                  PRIMARY KEY(issuer,tenant,subject,key));
                CREATE TABLE IF NOT EXISTS audit (
                  id INTEGER PRIMARY KEY, event TEXT NOT NULL);
                INSERT OR IGNORE INTO tickets VALUES ('alpha','T1','open',1);
                INSERT OR IGNORE INTO tickets VALUES ('beta','T1','open',1);
            """)

    def connect(self):
        conn = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def transaction(self):
        with closing(self.connect()) as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                yield conn
                conn.commit()
            except BaseException:
                conn.rollback()
                raise

    def ticket(self, principal: Principal, ticket_id: str) -> dict:
        require(principal, "tickets:read")
        with closing(self.connect()) as conn:
            row = conn.execute("SELECT id,status,version FROM tickets WHERE tenant=? AND id=?",
                               (principal.tenant, ticket_id)).fetchone()
        if row is None:
            raise LookupError("Ticket not found")
        return dict(row)

    def preview(self, principal: Principal, ticket_id: str) -> dict:
        require(principal, "tickets:write")
        ticket = self.ticket(principal, ticket_id)
        if ticket["status"] != "open":
            raise ValueError("Ticket is not open")
        payload = json.dumps({"operation": "close_ticket", "ticket_id": ticket_id,
                              "from": "open", "to": "closed", "version": ticket["version"]}, sort_keys=True)
        preview_id, digest, expires = secrets.token_urlsafe(20), sha256(payload.encode()).hexdigest(), self.clock() + 300
        with self.transaction() as conn:
            conn.execute("INSERT INTO previews (id,issuer,tenant,subject,ticket_id,version,payload,digest,state,expires) VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (preview_id, principal.issuer, principal.tenant, principal.subject,
                          ticket_id, ticket["version"], payload, digest, "pending", expires))
        return {"preview_id": preview_id, "change": json.loads(payload), "digest": digest,
                "state": "pending", "expires_at": expires}

    def review(self, reviewer: Principal, preview_id: str, approve: bool) -> None:
        require(reviewer, "tickets:review")
        with self.transaction() as conn:
            row = conn.execute("SELECT * FROM previews WHERE id=?", (preview_id,)).fetchone()
            if row is None or (row["issuer"], row["tenant"]) != (reviewer.issuer, reviewer.tenant):
                raise PermissionError("Preview is unavailable to this reviewer")
            if row["subject"] == reviewer.subject:
                raise PermissionError("A second person must review this change")
            if row["state"] != "pending" or row["expires"] <= self.clock():
                raise ValueError("Preview is no longer pending")
            conn.execute("UPDATE previews SET state=?,reviewer=? WHERE id=?",
                         ("approved" if approve else "denied", reviewer.subject, preview_id))

    def commit(self, principal: Principal, preview_id: str, key: str, *, fail_before_receipt: bool = False) -> dict:
        require(principal, "tickets:write")
        if not isinstance(key, str) or not 1 <= len(key) <= 80:
            raise ValueError("Idempotency key must contain 1 to 80 characters")
        binding = (principal.issuer, principal.tenant, principal.subject, key)
        call_digest = sha256(preview_id.encode()).hexdigest()
        with self.transaction() as conn:
            receipt = conn.execute("SELECT * FROM receipts WHERE issuer=? AND tenant=? AND subject=? AND key=?", binding).fetchone()
            if receipt:
                if receipt["digest"] != call_digest:
                    raise ValueError("Idempotency key already binds a different preview")
                return json.loads(receipt["result"])
            row = conn.execute("SELECT * FROM previews WHERE id=?", (preview_id,)).fetchone()
            if row is None or (row["issuer"], row["tenant"], row["subject"]) != binding[:3]:
                raise PermissionError("Preview is unavailable to this caller")
            if row["state"] != "approved" or row["expires"] <= self.clock():
                raise PermissionError("Reviewed, unexpired approval is required")
            if sha256(row["payload"].encode()).hexdigest() != row["digest"]:
                raise ValueError("Preview payload changed")
            changed = conn.execute("UPDATE tickets SET status='closed',version=version+1 WHERE tenant=? AND id=? AND status='open' AND version=?",
                                   (principal.tenant, row["ticket_id"], row["version"])).rowcount
            if changed != 1:
                raise ValueError("Ticket changed after preview; create a new preview")
            if fail_before_receipt:
                raise RuntimeError("Injected crash before receipt")
            result = {"ticket_id": row["ticket_id"], "status": "closed", "version": row["version"] + 1}
            conn.execute("INSERT INTO receipts VALUES (?,?,?,?,?,?)", (*binding, call_digest, json.dumps(result)))
            conn.execute("UPDATE previews SET state='consumed' WHERE id=?", (preview_id,))
            event = audit_event(tenant=principal.tenant, subject=principal.subject, tool="close_ticket", status="committed")
            conn.execute("INSERT INTO audit(event) VALUES (?)", (json.dumps(event),))
            return result

    def audit(self) -> list[dict]:
        # Internal operator method. Not an MCP tool and not open to model input.
        with closing(self.connect()) as conn:
            return [json.loads(row[0]) for row in conn.execute("SELECT event FROM audit ORDER BY id")]
