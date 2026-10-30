"""A provider-neutral tool loop for teaching. History here is not a native API wire format."""
import json
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict


@dataclass(frozen=True)
class Decision:
    text: str | None = None
    calls: tuple[ToolCall, ...] = ()


def multiply(arguments: dict):
    if set(arguments) != {"a", "b"} or any(type(arguments[key]) is not int for key in ("a", "b")):
        raise ValueError("multiply requires exactly two integer arguments")
    if any(abs(arguments[key]) > 1_000_000 for key in ("a", "b")):
        raise ValueError("Demo integer limit exceeded")
    return arguments["a"] * arguments["b"]


def run_agent(model: Callable, question: str, tools: dict[str, Callable], max_turns: int = 6, max_calls: int = 4) -> dict:
    if not isinstance(question, str) or not question.strip():
        raise ValueError("A question is required")
    if max_turns < 1 or max_calls < 0:
        raise ValueError("Invalid execution budget")
    history = [{"role": "user", "text": question}]
    seen, call_count = {}, 0
    for _ in range(max_turns):
        decision = model(history)
        if not isinstance(decision, Decision) or bool(decision.text) == bool(decision.calls):
            raise ValueError("Model must return either final text or tool calls")
        if decision.text:
            if not isinstance(decision.text, str) or not decision.text.strip():
                raise ValueError("Final text must be a nonempty string")
            return {"status": "completed", "answer": decision.text, "history": history}
        history.append({"role": "assistant", "calls": decision.calls})
        for call in decision.calls:
            if not isinstance(call, ToolCall) or not call.id or not isinstance(call.arguments, dict):
                raise ValueError("Invalid tool call")
            fingerprint = json.dumps({"name": call.name, "arguments": call.arguments}, sort_keys=True)
            if call.id in seen:
                old_fingerprint, result = seen[call.id]
                if old_fingerprint != fingerprint:
                    raise ValueError("A tool call ID was reused with different arguments")
            else:
                if call_count >= max_calls:
                    return {"status": "budget_exceeded", "answer": "", "history": history}
                call_count += 1
                if call.name not in tools:
                    result = {"error": "unknown_tool"}
                else:
                    try:
                        result = {"value": tools[call.name](call.arguments)}
                    except (TypeError, ValueError):
                        result = {"error": "invalid_arguments"}
                seen[call.id] = (fingerprint, result)
            history.append({"role": "tool", "call_id": call.id, "result": result})
    return {"status": "budget_exceeded", "answer": "", "history": history}


def simulated_model(history: list[dict]) -> Decision:
    if history[-1]["role"] == "tool":
        result = history[-1]["result"]
        return Decision(text=f"計算結果是 {result['value']}。" if "value" in result else "工具未能完成。")
    return Decision(calls=(ToolCall("demo-1", "multiply", {"a": 6, "b": 7}),))
