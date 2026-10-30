"""Normalize a small set of recorded event-shaped fixtures, not a full SSE client."""


def normalize_event(provider: str, event: dict) -> dict | None:
    if provider == "openai":
        if event.get("type") == "response.output_text.delta":
            return {"kind": "text", "text": event["delta"]}
        if event.get("type") in ("response.completed", "response.incomplete", "response.failed"):
            return {"kind": "end", "status": event["type"].split(".")[-1]}
    elif provider == "gemini":
        if event.get("event_type") == "step.delta" and event.get("delta", {}).get("type") == "text":
            return {"kind": "text", "text": event["delta"]["text"]}
        if event.get("event_type") in ("interaction.completed", "interaction.failed"):
            return {"kind": "end", "status": event["event_type"].split(".")[-1]}
    elif provider == "claude":
        if event.get("type") == "content_block_delta" and event.get("delta", {}).get("type") == "text_delta":
            return {"kind": "text", "text": event["delta"]["text"]}
        if event.get("type") == "message_stop":
            return {"kind": "end", "status": "stopped"}  # Inspect message_delta.stop_reason separately.
    else:
        raise ValueError("Unknown provider")
    return None


if __name__ == "__main__":
    fixtures = [
        ("openai", {"type": "response.output_text.delta", "delta": "你好"}),
        ("gemini", {"event_type": "step.delta", "delta": {"type": "text", "text": "你好"}}),
        ("claude", {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "你好"}}),
    ]
    for provider, event in fixtures:
        print(provider, normalize_event(provider, event))
