"""A deterministic model double tests routing and budget, without API calls."""
import anyio
from mcp import Client
from demo_server import build_server


async def run_agent(proposals, max_calls=2):
    if max_calls < 1:
        raise ValueError("A positive call budget is required")
    outputs = []
    async with Client(build_server()) as client:
        allowed = {tool.name for tool in (await client.list_tools()).tools} & {"search_notes"}
        for proposal in proposals:
            if len(outputs) >= max_calls:
                raise RuntimeError("Tool call budget exhausted")
            if proposal["name"] not in allowed:
                raise PermissionError("Model proposed a tool outside the host allowlist")
            result = await client.call_tool(proposal["name"], proposal["arguments"])
            if result.is_error:
                raise ValueError("Tool failed; do not invent a successful result")
            outputs.append(result.structured_content)
    return outputs


if __name__ == "__main__":
    print(anyio.run(run_agent, [{"name": "search_notes", "arguments": {"query": "MCP"}}]))
