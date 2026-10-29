"""Run: python 01_hello.py. No API key required."""
from typing import NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    greeting: NotRequired[str]


def normalize(state: State) -> dict:
    return {"name": state["name"].strip()}


def greet(state: State) -> dict:
    return {"greeting": f"你好，{state['name']}！"}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("normalize", normalize)
    builder.add_node("greet", greet)
    builder.add_edge(START, "normalize")
    builder.add_edge("normalize", "greet")
    builder.add_edge("greet", END)
    return builder.compile()


if __name__ == "__main__":
    result = build_graph().invoke({"name": "  小林  "})
    print(result)
