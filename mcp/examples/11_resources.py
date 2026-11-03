"""Concrete resources and templates are separate discovery lists."""
import anyio
from mcp import Client
from mcp.types import TextResourceContents
from demo_server import build_server


async def main():
    async with Client(build_server()) as client:
        print("concrete", (await client.list_resources()).resources)
        print("templates", (await client.list_resource_templates()).resource_templates)
        result = await client.read_resource("notes://guide/approval")
        for item in result.contents:
            if isinstance(item, TextResourceContents):
                print(item.text)


if __name__ == "__main__":
    anyio.run(main)
