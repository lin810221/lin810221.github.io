"""Inspect x-mcp-header metadata. Headers are not authenticated identity."""
from typing import Annotated
import anyio
from pydantic import WithJsonSchema
from mcp import Client
from mcp.server import MCPServer


async def main():
    server = MCPServer("HeaderExample")

    @server.tool()
    def region_notice(region: Annotated[str, WithJsonSchema({"type": "string", "x-mcp-header": "Region"})]) -> str:
        """Select a display region, never grant a tenant permission."""
        return f"Display region: {region}"

    async with Client(server) as client:
        definition = (await client.list_tools()).tools[0]
        print(definition.input_schema)
    print("This example validates registration; HTTP header forwarding is a separate integration test.")


if __name__ == "__main__":
    anyio.run(main)
