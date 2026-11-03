"""Show strict numeric validation; boolean true is not an integer limit."""
import anyio
from mcp import Client
from demo_server import build_server


async def main():
    async with Client(build_server()) as client:
        tool = next(t for t in (await client.list_tools()).tools if t.name == "search_notes")
        print(tool.input_schema)
        for limit in (2, 0, 11, "2", True):
            result = await client.call_tool("search_notes", {"query": "MCP", "limit": limit})
            print(repr(limit), "rejected" if result.is_error else "accepted")


if __name__ == "__main__":
    anyio.run(main)
