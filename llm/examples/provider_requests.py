"""Minimal REST adapters. No outbound request until call_live() is explicitly used."""
import argparse
import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass

PROVIDERS = {
    "openai": ("https://api.openai.com/v1/responses", "OPENAI_API_KEY", "OPENAI_MODEL"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/interactions", "GEMINI_API_KEY", "GEMINI_MODEL"),
    "claude": ("https://api.anthropic.com/v1/messages", "ANTHROPIC_API_KEY", "ANTHROPIC_MODEL"),
}


@dataclass(frozen=True)
class Reply:
    text: str
    status: str
    usage: dict
    request_id: str | None = None


def request_for(provider: str, model: str, prompt: str, max_tokens: int = 2048) -> dict:
    if provider not in PROVIDERS:
        raise ValueError("Unknown provider")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("A model ID is required")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("A nonempty prompt is required")
    if type(max_tokens) is not int or max_tokens < 1:
        raise ValueError("max_tokens must be a positive integer")
    instruction = "請以繁體中文清楚回答。"
    if provider == "openai":
        return {"model": model, "instructions": instruction, "input": prompt,
                "max_output_tokens": max_tokens, "store": False}
    if provider == "gemini":
        return {"model": model, "system_instruction": instruction, "input": prompt,
                "generation_config": {"max_output_tokens": max_tokens}, "store": False}
    return {"model": model, "system": instruction, "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]}


def with_schema(provider: str, body: dict, schema: dict) -> dict:
    """Only use with a model supporting this provider's structured-output mode."""
    result = json.loads(json.dumps(body))
    if provider == "openai":
        result["text"] = {"format": {"type": "json_schema", "name": "answer", "schema": schema, "strict": True}}
    elif provider == "gemini":
        result["response_format"] = {"type": "text", "mime_type": "application/json", "schema": schema}
    elif provider == "claude":
        result["output_config"] = {"format": {"type": "json_schema", "schema": schema}}
    else:
        raise ValueError("Unknown provider")
    return result


def parse_reply(provider: str, data: dict) -> Reply:
    """Normalize visible text only; never treat thinking or tool arguments as an answer."""
    if provider == "openai":
        items = data.get("output", [])
        blocks = [block for item in items if item.get("type") == "message" for block in item.get("content", [])]
        text = "".join(block.get("text", "") for block in blocks if block.get("type") == "output_text")
        status = data.get("status", "unknown")
        if status == "completed" and any(item.get("type") == "function_call" for item in items):
            status = "requires_tools"
        if any(block.get("type") == "refusal" for block in blocks):
            status = "refused"
    elif provider == "gemini":
        steps = data.get("steps", [])
        text = "".join(block.get("text", "") for step in steps if step.get("type") == "model_output"
                       for block in step.get("content", []) if block.get("type") == "text")
        status = data.get("status", "unknown")
        if status not in ("incomplete", "failed", "cancelled") and any(step.get("type") == "function_call" for step in steps):
            status = "requires_tools"
    elif provider == "claude":
        blocks = data.get("content", [])
        text = "".join(block.get("text", "") for block in blocks if block.get("type") == "text")
        stop = data.get("stop_reason", "unknown")
        status = {"end_turn": "completed", "stop_sequence": "completed", "max_tokens": "incomplete",
                  "tool_use": "requires_tools", "refusal": "refused", "pause_turn": "paused"}.get(stop, stop)
        if (data.get("stop_details") or {}).get("type") == "refusal":
            status = "refused"
    else:
        raise ValueError("Unknown provider")
    return Reply(text=text, status=status, usage=data.get("usage") or {}, request_id=data.get("id"))


def call_raw(provider: str, body: dict, timeout: float = 45) -> dict:
    url, key_name, _ = PROVIDERS[provider]
    key = os.environ.get(key_name)
    if not key:
        raise ValueError(f"Set {key_name} in the environment before using --live")
    headers = {"Content-Type": "application/json"}
    if provider == "gemini":
        headers["x-goog-api-key"] = key
    else:
        headers["Authorization"] = f"Bearer {key}"
    if provider == "claude":
        headers["anthropic-version"] = os.environ.get("ANTHROPIC_VERSION", "2026-10-21")
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        # Intentionally omit the response body and request headers from logs.
        raise RuntimeError(f"Provider HTTP {error.code}; inspect request ID and official error docs") from None
    return data


def call_live(provider: str, body: dict, timeout: float = 45) -> Reply:
    return parse_reply(provider, call_raw(provider, body, timeout))


def run_cli(provider: str):
    parser = argparse.ArgumentParser(description="Dry run by default; --live sends one billable API request")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--prompt", default="請用一個例子解釋 AI Agent。")
    parser.add_argument("--max-output-tokens", type=int, default=2048)
    args = parser.parse_args()
    _, _, model_name = PROVIDERS[provider]
    model = os.environ.get(model_name)
    if args.live and not model:
        parser.error(f"Set {model_name} to a model available to your account")
    body = request_for(provider, model or f"YOUR_{provider.upper()}_MODEL", args.prompt, args.max_output_tokens)
    if args.live:
        print(json.dumps(asdict(call_live(provider, body)), ensure_ascii=False, indent=2))
    else:
        print("DRY RUN: no network request, no API key required")
        print(PROVIDERS[provider][0])
        print(json.dumps(body, ensure_ascii=False, indent=2))
