"""Retry transient failures, inject immutable run context."""
from dataclasses import dataclass
from typing import NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime
from langgraph.types import RetryPolicy


@dataclass(frozen=True)
class Context:
    user_id: str


class State(TypedDict):
    question: str
    answer: NotRequired[str]


class TransientFailure(Exception):
    pass


def build_graph():
    attempts = {"count": 0}  # Only a test fixture; not a production retry counter.

    def call_service(state: State, runtime: Runtime[Context]) -> dict:
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise TransientFailure("模擬暫時性服務失敗")
        return {"answer": f"{runtime.context.user_id}: 已取得結果"}

    builder = StateGraph(State, context_schema=Context)
    builder.add_node("call_service", call_service, retry_policy=RetryPolicy(
        initial_interval=0.01, max_attempts=3, jitter=False, retry_on=TransientFailure
    ))
    builder.add_edge(START, "call_service")
    builder.add_edge("call_service", END)
    return builder.compile(), attempts


if __name__ == "__main__":
    graph, attempts = build_graph()
    result = graph.invoke({"question": "請查詢"}, context=Context(user_id="student-01"))
    print(result)
    print("attempts:", attempts["count"])
