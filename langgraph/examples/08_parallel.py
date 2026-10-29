"""Dynamic map-reduce with Send and stable, explicitly sorted output."""
import operator
from typing import Annotated, NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


class State(TypedDict):
    topics: list[str]
    results: Annotated[list[dict], operator.add]
    report: NotRequired[str]


class WorkerInput(TypedDict):
    index: int
    topic: str


def dispatch(state: State):
    if not state["topics"]:
        return "reduce"
    return [Send("worker", {"index": i, "topic": topic}) for i, topic in enumerate(state["topics"])]


def worker(state: WorkerInput) -> dict:
    return {"results": [{"index": state["index"], "text": f"已處理 {state['topic']}"}]}


def reduce_results(state: State) -> dict:
    ordered = sorted(state["results"], key=lambda item: item["index"])
    return {"report": "\n".join(item["text"] for item in ordered)}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("worker", worker)
    builder.add_node("reduce", reduce_results)
    builder.add_conditional_edges(START, dispatch, ["worker", "reduce"])
    builder.add_edge("worker", "reduce")
    builder.add_edge("reduce", END)
    return builder.compile()


if __name__ == "__main__":
    result = build_graph().invoke({"topics": ["State", "Reducer", "Send"], "results": []})
    print(result["report"])
