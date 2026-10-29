"""Parent and child use different contracts; wrapper maps them explicitly."""
from typing import NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END


class ChildState(TypedDict):
    text: str
    normalized: NotRequired[str]


def clean(state: ChildState) -> dict:
    return {"normalized": state["text"].strip().lower()}


child_builder = StateGraph(ChildState)
child_builder.add_node("clean", clean)
child_builder.add_edge(START, "clean")
child_builder.add_edge("clean", END)
child = child_builder.compile()


class ParentState(TypedDict):
    question: str
    query: NotRequired[str]


def adapt(state: ParentState) -> dict:
    result = child.invoke({"text": state["question"]})
    return {"query": result["normalized"]}


def build_graph():
    builder = StateGraph(ParentState)
    builder.add_node("prepare", adapt)
    builder.add_edge(START, "prepare")
    builder.add_edge("prepare", END)
    return builder.compile()


if __name__ == "__main__":
    print(build_graph().invoke({"question": "  What Is State?  "}))
