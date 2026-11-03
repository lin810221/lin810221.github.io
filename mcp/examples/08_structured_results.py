"""Read typed output only after checking the error flag."""
import anyio
from jsonschema import Draft202012Validator
from mcp import Client
from mcp.types import TextContent
from demo_server import build_server, SearchResult


async def main():
    async with Client(build_server()) as client:
        definition = next(t for t in (await client.list_tools()).tools if t.name == "search_notes")
        result = await client.call_tool("search_notes", {"query": "MCP"})
        if result.is_error:
            raise RuntimeError("Search failed")
        Draft202012Validator(definition.output_schema).validate(result.structured_content)
        parsed = SearchResult.model_validate(result.structured_content)
        print(parsed.total, parsed.matches)
        print([block.text for block in result.content if isinstance(block, TextContent)])


if __name__ == "__main__":
    anyio.run(main)
