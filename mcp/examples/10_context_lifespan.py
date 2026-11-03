"""Verify that app resources open once and close on context exit."""
from contextlib import asynccontextmanager
from dataclasses import dataclass
import anyio
from mcp import Client
from mcp.server import MCPServer
from mcp.server.mcpserver import Context


@dataclass
class AppState:
    connected: bool = False


async def main():
    state = AppState()

    @asynccontextmanager
    async def lifespan(server):
        state.connected = True
        try:
            yield state
        finally:
            state.connected = False

    server = MCPServer("Lifecycle", lifespan=lifespan)

    @server.tool()
    async def connection_status(ctx: Context[AppState]) -> dict:
        """Inspect the shared fake connection."""
        return {"connected": ctx.request_context.lifespan_context.connected}

    async with Client(server) as client:
        print((await client.call_tool("connection_status", {})).structured_content)
    assert not state.connected
    print("connection closed")


if __name__ == "__main__":
    anyio.run(main)
