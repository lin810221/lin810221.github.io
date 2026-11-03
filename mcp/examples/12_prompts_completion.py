"""Render a prompt and complete a user-entered argument; no generation call."""
import anyio
from mcp import Client
from mcp.types import Completion, PromptReference
from demo_server import build_server


async def main():
    server = build_server()

    @server.completion()
    async def complete(ref, argument, context):
        return Completion(values=[topic for topic in ("mcp", "approval") if topic.startswith(argument.value)])

    async with Client(server) as client:
        result = await client.complete(PromptReference(type="ref/prompt", name="explain"),
                                       {"name": "topic", "value": "ap"})
        print(result.completion.values)
        prompt = await client.get_prompt("explain", {"topic": "approval"})
        print(prompt.messages[0].content)


if __name__ == "__main__":
    anyio.run(main)
