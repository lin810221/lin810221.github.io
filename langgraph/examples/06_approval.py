"""Resume a human decision with the same graph and thread."""
from typing import NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class State(TypedDict):
    draft: str
    approved: NotRequired[bool]
    answer: NotRequired[str]


def review(state: State) -> dict:
    decision = interrupt({"question": "是否核准這份草稿？", "draft": state["draft"]})
    if not isinstance(decision, dict) or type(decision.get("approved")) is not bool:
        raise ValueError("Expected {'approved': bool}")
    return {"approved": decision["approved"]}


def finalize(state: State) -> dict:
    return {"answer": state["draft"] if state["approved"] else "草稿未核准。"}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("review", review)
    builder.add_node("finalize", finalize)
    builder.add_edge(START, "review")
    builder.add_edge("review", "finalize")
    builder.add_edge("finalize", END)
    return builder.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":
    graph = build_graph()
    config = {"configurable": {"thread_id": "review-demo"}}
    paused = graph.invoke({"draft": "這是待審核的答案。"}, config)
    print("等待審核:", paused["__interrupt__"][0].value)
    result = graph.invoke(Command(resume={"approved": True}), config)
    print("最終答案:", result["answer"])
