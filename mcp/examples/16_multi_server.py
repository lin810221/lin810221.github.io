"""A host owns the namespace-to-client mapping, not the model."""
from contextlib import AsyncExitStack
import anyio
from mcp import Client
from demo_server import build_server


async def main():
    async with AsyncExitStack() as stack:
        clients = {name: await stack.enter_async_context(Client(build_server())) for name in ("notes", "support")}
        routes = {}
        for name, client in clients.items():
            for tool in (await client.list_tools()).tools:
                routes[f"{name}__{tool.name}"] = (client, tool.name)
        client, original = routes["notes__search_notes"]
        result = await client.call_tool(original, {"query": "MCP"})
        print(sorted(routes), result.structured_content)


if __name__ == "__main__":
    anyio.run(main)
