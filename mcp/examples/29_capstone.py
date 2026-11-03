"""End-to-end SDK workflow with a separately simulated human reviewer."""
from pathlib import Path
from tempfile import TemporaryDirectory
import anyio
from mcp import Client
from capstone_server import build_capstone
from integration_core import ALICE, REVIEWER, WorkflowStore


async def demonstrate(store):
    async with Client(build_capstone(store)) as client:
        names = {tool.name for tool in (await client.list_tools()).tools}
        assert "approve" not in names and "review" not in names
        proposal = await client.call_tool("preview_close_ticket", {"ticket_id": "T1"})
        if proposal.is_error:
            raise RuntimeError("The preview failed; no approval or commit is attempted")
        preview_id = proposal.structured_content["preview_id"]
        early = await client.call_tool("close_ticket", {"preview_id": preview_id, "idempotency_key": "demo-close"})
        assert early.is_error and store.ticket(ALICE, "T1")["status"] == "open"
        store.review(REVIEWER, preview_id, approve=True)  # Trusted operator test double.
        arguments = {"preview_id": preview_id, "idempotency_key": "demo-close"}
        done = await client.call_tool("close_ticket", arguments)
        again = await client.call_tool("close_ticket", arguments)
        assert not done.is_error and done.structured_content == again.structured_content
        return {"receipt": done.structured_content, "audit_count": len(store.audit())}


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        print(anyio.run(demonstrate, WorkflowStore(Path(folder) / "workorders.sqlite")))
