"""A bounded conditional loop. No model involved."""
from typing import Literal, NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    count: int
    target: int
    answer: NotRequired[str]


def advance(state: State) -> dict:
    return {"count": state["count"] + 1}


def choose(state: State) -> Literal["again", "done"]:
    return "again" if state["count"] < state["target"] else "done"


def finish(state: State) -> dict:
    return {"answer": f"完成 {state['count']} 次"}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("advance", advance)
    builder.add_node("finish", finish)
    builder.add_edge(START, "advance")
    builder.add_conditional_edges("advance", choose, {"again": "advance", "done": "finish"})
    builder.add_edge("finish", END)
    return builder.compile()


if __name__ == "__main__":
    print(build_graph().invoke({"count": 0, "target": 3}, {"recursion_limit": 20}))
