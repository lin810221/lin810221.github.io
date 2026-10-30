"""Native, stateless tool loops. Only multiply is allowed; no network until live=True."""
import json
import os
from agent_core import multiply
from provider_requests import PROVIDERS, request_for, parse_reply, call_raw

PARAMETERS = {"type":"object", "properties":{"a":{"type":"integer"},"b":{"type":"integer"}},
              "required":["a","b"], "additionalProperties":False}


def tool_definition(provider):
    if provider == "claude":
        return {"name":"multiply","description":"Multiply two bounded integers.","input_schema":PARAMETERS}
    tool = {"type":"function","name":"multiply","description":"Multiply two bounded integers.","parameters":PARAMETERS}
    if provider == "openai":
        tool["strict"] = True
    return tool


def native_agent(provider: str, question: str, live: bool = False, max_turns: int = 6, max_calls: int = 4) -> dict:
    _, _, model_env = PROVIDERS[provider]
    model = os.environ.get(model_env)
    if live and not model:
        raise ValueError(f"Set {model_env}")
    base = request_for(provider, model or "YOUR_MODEL", question, 4096)
    base["tools"] = [tool_definition(provider)]
    if not live:
        return {"status":"dry_run", "request":base}
    if max_turns < 1 or max_calls < 0:
        raise ValueError("Invalid execution budget")
    if provider == "gemini":
        history = [{"type":"user_input","content":[{"type":"text","text":question}]}]
    else:
        history = [{"role":"user","content":question}]
    used, seen, usages = 0, {}, []
    for _ in range(max_turns):
        body = json.loads(json.dumps(base))
        body["messages" if provider == "claude" else "input"] = history
        raw = call_raw(provider,body)
        reply = parse_reply(provider,raw)
        usages.append(reply.usage)
        if reply.status == "completed":
            return {"status":"completed","answer":reply.text,"usage_by_turn":usages}
        if reply.status != "requires_tools":
            return {"status":reply.status,"answer":"","usage_by_turn":usages}
        if provider == "openai":
            history.extend(raw["output"])
            calls = [(item["call_id"],item["name"],item["arguments"]) for item in raw["output"] if item.get("type") == "function_call"]
        elif provider == "gemini":
            history.extend(raw["steps"])
            calls = [(step["id"],step["name"],step["arguments"]) for step in raw["steps"] if step.get("type") == "function_call"]
        else:
            history.append({"role":"assistant","content":raw["content"]})
            calls = [(block["id"],block["name"],block["input"]) for block in raw["content"] if block.get("type") == "tool_use"]
        results = []
        for call_id, name, arguments in calls:
            if not isinstance(call_id,str) or not call_id:
                raise ValueError("A native tool call ID is required")
            if isinstance(arguments,str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = None
            fingerprint = json.dumps({"name":name,"args":arguments},sort_keys=True)
            if call_id in seen:
                prior, result = seen[call_id]
                if fingerprint != prior:
                    raise ValueError("Tool ID reused with different arguments")
            else:
                if used >= max_calls:
                    return {"status":"budget_exceeded","answer":"","usage_by_turn":usages}
                used += 1
                if name != "multiply":
                    result = {"error":"unknown_tool"}
                elif not isinstance(arguments,dict):
                    result = {"error":"invalid_arguments"}
                else:
                    try:
                        result = {"value":multiply(arguments)}
                    except (TypeError,ValueError):
                        result = {"error":"invalid_arguments"}
                seen[call_id] = (fingerprint,result)
            text = json.dumps(result)
            if provider == "openai":
                results.append({"type":"function_call_output","call_id":call_id,"output":text})
            elif provider == "gemini":
                results.append({"type":"function_result","name":name,"call_id":call_id,"result":[{"type":"text","text":text}]})
            else:
                results.append({"type":"tool_result","tool_use_id":call_id,"content":text,"is_error":"error" in result})
        if provider == "claude":
            history.append({"role":"user","content":results})
        else:
            history.extend(results)
    return {"status":"budget_exceeded","answer":"","usage_by_turn":usages}
