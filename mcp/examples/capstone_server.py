"""A local fictional work-order server. Review is outside the model's tools."""
from typing import Callable
from pydantic import BaseModel, Field
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from integration_core import ALICE, Principal, WorkflowStore, search_notes


class CloseReceipt(BaseModel):
    ticket_id: str
    status: str
    version: int


class TicketView(BaseModel):
    id: str
    status: str
    version: int


class PreviewResult(BaseModel):
    preview_id: str
    change: dict[str, object]
    digest: str
    state: str
    expires_at: float


class NotesResult(BaseModel):
    matches: list[dict[str, str]]
    total: int


def build_capstone(store: WorkflowStore, principal_provider: Callable[[], Principal] = lambda: ALICE,
                   *, auth=None, token_verifier=None) -> MCPServer:
    """Default identity is an explicit offline fixture, for in-process/stdio use.

    An authenticated HTTP app must inject a provider backed by a verified token.
    Neither tenant nor approval state can be supplied as model arguments.
    """
    server = MCPServer("ReviewedWorkOrders", version="1.0.0", auth=auth, token_verifier=token_verifier)

    def domain(operation):
        try:
            return operation()
        except (PermissionError, LookupError, ValueError) as error:
            # In a real service use a public error catalog, never raw exceptions.
            raise ToolError(str(error)) from error

    @server.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False))
    async def find_notes(query: str, limit: int = Field(default=5, ge=1, le=10, strict=True)) -> NotesResult:
        """Search only the authenticated caller's fictional notes."""
        matches = domain(lambda: search_notes(principal_provider(), query, limit))
        return NotesResult(matches=matches, total=len(matches))

    @server.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False))
    async def get_ticket(ticket_id: str) -> TicketView:
        """Read a ticket belonging to the authenticated caller's tenant."""
        return TicketView(**domain(lambda: store.ticket(principal_provider(), ticket_id)))

    @server.tool(annotations=ToolAnnotations(read_only_hint=False, destructive_hint=False, open_world_hint=False))
    async def preview_close_ticket(ticket_id: str) -> PreviewResult:
        """Create a pending immutable preview; this does not close the ticket."""
        return PreviewResult(**domain(lambda: store.preview(principal_provider(), ticket_id)))

    @server.tool(annotations=ToolAnnotations(read_only_hint=False, destructive_hint=True,
                                           idempotent_hint=True, open_world_hint=False))
    async def close_ticket(preview_id: str, idempotency_key: str) -> CloseReceipt:
        """Execute an unexpired preview reviewed by a separate trusted operator; replay a key safely."""
        data = domain(lambda: store.commit(principal_provider(), preview_id, idempotency_key))
        return CloseReceipt(**data)

    @server.resource("notes://guide/{topic}")
    async def guide(topic: str) -> str:
        """Read a bounded tenant-scoped guide from the same authorization path."""
        matches = domain(lambda: search_notes(principal_provider(), topic, 3))
        return "\n".join(row["text"] for row in matches) or "No matching notes."

    return server
