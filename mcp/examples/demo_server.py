"""Small, deterministic MCP 2.3.0 server shared by transport examples."""
from typing import Annotated
from pydantic import BaseModel, Field
from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from mcp.server.mcpserver.exceptions import ToolError


class SearchResult(BaseModel):
    matches: list[str]
    total: int


def build_server() -> MCPServer:
    server = MCPServer("CourseNotes", version="1.0.0", instructions="Search notes before answering project questions.")

    @server.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False))
    def search_notes(query: Annotated[str, Field(min_length=1, max_length=100)],
                     limit: Annotated[int, Field(strict=True, ge=1, le=10)] = 5) -> SearchResult:
        """Search the fictional course notes. No external services or mutations."""
        notes = ["MCP tools have typed input schemas.", "MCP resources provide context.", "Reviewed previews protect writes."]
        hits = [text for text in notes if query.casefold() in text.casefold()]
        return SearchResult(matches=hits[:limit], total=len(hits))

    @server.tool()
    def lookup_ticket(ticket_id: str) -> dict:
        """Read the one fictional ticket T1; missing tickets are tool failures."""
        if ticket_id != "T1":
            raise ToolError("Ticket not found; check the ticket identifier")
        return {"ticket_id": ticket_id, "status": "open"}

    @server.resource("notes://guide/{topic}")
    def guide(topic: str) -> str:
        """Read an allowlisted course guide."""
        content = {"mcp": "MCP connects hosts to tools and resources.", "approval": "Review immutable previews before executing writes."}
        if topic not in content:
            raise ValueError("Unknown topic")
        return content[topic]

    @server.prompt()
    def explain(topic: str) -> str:
        """Prepare a teaching prompt; rendering does not execute the model."""
        return f"Explain {topic} using the course guide and distinguish evidence from inference."

    return server
