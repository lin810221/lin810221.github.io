"""Two parallel nodes contribute updates to a reducer channel."""
import operator
from typing import Annotated, NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    events: Annotated[list[str], operator.add]
    summary: NotRequired[str]


def collect_left(state: State) -> dict:
    return {"events": ["A"]}


def collect_right(state: State) -> dict:
    return {"events": ["B"]}


def summarize(state: State) -> dict:
    return {"summary": ",".join(sorted(state["events"]))}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("left", collect_left)
    builder.add_node("right", collect_right)
    builder.add_node("join", summarize)
    builder.add_edge(START, "left")
    builder.add_edge(START, "right")
    builder.add_edge(["left", "right"], "join")
    builder.add_edge("join", END)
    return builder.compile()


if __name__ == "__main__":
    print(build_graph().invoke({"events": []}))
