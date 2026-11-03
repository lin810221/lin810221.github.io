"""Inspect a modern envelope. This is a message example, not a raw MCP client."""
import json


def request(request_id=1):
    return {"jsonrpc": "2.0", "id": request_id, "method": "tools/list", "params": {
        "_meta": {"io.modelcontextprotocol/protocolVersion": "2026-07-28",
                  "io.modelcontextprotocol/clientCapabilities": {},
                  "io.modelcontextprotocol/clientInfo": {"name": "course", "version": "1.0"}}}}


def match_response(sent, received):
    if received.get("jsonrpc") != "2.0" or received.get("id") != sent["id"]:
        raise ValueError("Response correlation failed")
    if ("result" in received) == ("error" in received):
        raise ValueError("Exactly one of result or error is required")
    return received


if __name__ == "__main__":
    sent = request()
    reply = {"jsonrpc": "2.0", "id": 1, "result": {"resultType": "complete", "tools": []}}
    print(json.dumps({"request": sent, "response": match_response(sent, reply)}, indent=2))
