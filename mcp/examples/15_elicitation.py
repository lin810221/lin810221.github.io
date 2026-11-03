"""Exercise MCP 2026 MRTR via Resolve and a scripted user callback."""
from typing import Annotated
import anyio
from pydantic import BaseModel
from mcp import Client
from mcp.server import MCPServer
from mcp.server.mcpserver import Elicit, Resolve
from mcp.types import ElicitResult


class Language(BaseModel):
    language: str


def ask_language() -> Elicit[Language]:
    return Elicit("Which language should the explanation use?", Language)


def build_server():
    server = MCPServer("UserInput")

    @server.tool()
    async def prepare(topic: str, preference: Annotated[Language, Resolve(ask_language)]) -> str:
        """Prepare an explanation label using user-supplied preferences."""
        return f"{topic}: {preference.language}"

    return server


async def main():
    async def scripted_user(context, params):
        # A test double for the host UI; not a permission or payment approval.
        return ElicitResult(action="accept", content={"language": "zh-TW"})

    async with Client(build_server(), elicitation_callback=scripted_user) as client:
        schema = (await client.list_tools()).tools[0].input_schema
        assert "preference" not in schema.get("properties", {})
        result = await client.call_tool("prepare", {"topic": "MCP"})
        assert not result.is_error
        print(result.content)


if __name__ == "__main__":
    anyio.run(main)
