"""LangGraph 1.1+ unified v2 stream envelope; no LLM token calls."""
from typing import NotRequired, TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    question: str
    answer: NotRequired[str]


def answer(state: State) -> dict:
    writer = get_stream_writer()
    writer({"stage": "reading", "progress": 0.5})
    return {"answer": "LangGraph 使用圖來編排有狀態的流程。"}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("answer", answer)
    builder.add_edge(START, "answer")
    builder.add_edge("answer", END)
    return builder.compile()


if __name__ == "__main__":
    for part in build_graph().stream(
        {"question": "什麼是 LangGraph？"}, stream_mode=["updates", "custom"], version="v2"
    ):
        print(part["type"], part["data"])
