"""An explicit --url performs a real HTTP call; default uses in-process SDK."""
import argparse
import anyio
from mcp import Client
from demo_server import build_server


async def main(endpoint=None):
    async with Client(endpoint or build_server(), read_timeout_seconds=10) as client:
        result = await client.call_tool("search_notes", {"query": "resources"})
        print("transport", "HTTP" if endpoint else "in-process")
        print(client.protocol_version, result.structured_content, result.is_error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="Example: http://127.0.0.1:8765/mcp")
    anyio.run(main, parser.parse_args().url)
