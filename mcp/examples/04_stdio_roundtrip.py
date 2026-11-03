"""Launch the pinned Python interpreter, not a shell command string."""
from pathlib import Path
import sys
import anyio
from mcp import Client, StdioServerParameters


async def main():
    folder = Path(__file__).resolve().parent
    params = StdioServerParameters(command=sys.executable,
        args=[str(folder / "01_first_server.py"), "--serve"], cwd=str(folder),
        env={"PYTHONUTF8": "1"})
    async with Client(params, read_timeout_seconds=10) as client:
        result = await client.call_tool("search_notes", {"query": "MCP"})
        assert not result.is_error
        print("stdio", client.protocol_version, result.structured_content)


if __name__ == "__main__":
    anyio.run(main)
