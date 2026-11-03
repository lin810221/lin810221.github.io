"""Default: in-process demo. --serve explicitly starts a stdio MCP server."""
import argparse
import anyio
from mcp import Client
from demo_server import build_server

server = build_server()


async def main():
    async with Client(server) as client:
        result = await client.call_tool("search_notes", {"query": "MCP", "limit": 2})
        print(client.protocol_version, result.structured_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true")
    args = parser.parse_args()
    if args.serve:
        server.run(transport="stdio")  # Never print application logs to stdout here.
    else:
        anyio.run(main)
