"""A not-found domain error returns is_error, not a successful empty object."""
import anyio
from mcp import Client
from mcp.types import TextContent
from demo_server import build_server


async def main():
    async with Client(build_server()) as client:
        for ticket_id in ("T1", "does-not-exist"):
            result = await client.call_tool("lookup_ticket", {"ticket_id": ticket_id})
            print(ticket_id, "is_error", result.is_error)
            print([part.text for part in result.content if isinstance(part, TextContent)])
        # Unknown high-level tools also yield an error result in this SDK.
        result = await client.call_tool("unknown_tool", {})
        assert result.is_error


if __name__ == "__main__":
    anyio.run(main)
