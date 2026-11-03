"""Offline payload/config construction only; provider APIs are not executed."""
from pathlib import Path
import json
import sys


def configurations():
    endpoint = "https://mcp.example.invalid/mcp"  # Replace with your reviewed endpoint.
    return {
        "openai_responses": {"model": "SET_SUPPORTED_OPENAI_MODEL", "input": "Search the MCP course notes.",
            "tools": [{"type": "mcp", "server_label": "course_notes", "server_url": endpoint,
                       "allowed_tools": ["search_notes"], "require_approval": "always"}]},
        "claude_messages": {"beta_header": "mcp-client-2026-09-15", "body": {
            "model": "SET_SUPPORTED_CLAUDE_MODEL", "max_tokens": 512,
            "messages": [{"role": "user", "content": "Search the MCP course notes."}],
            "mcp_servers": [{"type": "url", "name": "course_notes", "url": endpoint}],
            "tools": [{"type": "mcp_toolset", "mcp_server_name": "course_notes",
                       "default_config": {"enabled": False}, "configs": {"search_notes": {"enabled": True}}}]}},
        "gemini_cli": {"mcpServers": {"course_notes": {"command": sys.executable,
            "args": [str(Path(__file__).with_name("01_first_server.py").resolve()), "--serve"],
            "trust": False, "includeTools": ["search_notes"]}}},
    }


if __name__ == "__main__":
    print(json.dumps(configurations(), indent=2))
