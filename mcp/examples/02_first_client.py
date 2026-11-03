"""Discover tools, read a resource and render a prompt without an LLM."""
import anyio
from mcp import Client
from demo_server import build_server


async def main():
    async with Client(build_server()) as client:
        print("protocol", client.protocol_version)
        for tool in (await client.list_tools()).tools:
            print(tool.name, tool.input_schema)
        resource = await client.read_resource("notes://guide/mcp")
        print(resource.contents[0].text)
        prompt = await client.get_prompt("explain", {"topic": "MCP"})
        print(prompt.messages[0].content)


if __name__ == "__main__":
    anyio.run(main)
