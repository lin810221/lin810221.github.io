"""Offline, testable RAG-style assistant. No model, vector DB, or outbound side effects."""
import re
from typing import Literal, NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

DOCUMENTS = [
    {"id": "D1", "keys": ["記憶", "memory", "checkpoint", "checkpointer"],
     "text": "Checkpointer 保存單一 thread 的圖狀態；InMemorySaver 在程序結束後不會保留資料。"},
    {"id": "D2", "keys": ["記憶", "memory", "store", "長期"],
     "text": "Store 儲存應用定義的資料，可跨 thread 使用；資料的 namespace 與權限由應用負責。"},
    {"id": "D3", "keys": ["審核", "interrupt", "恢復"],
     "text": "interrupt 暫停節點；以相同 thread_id 及 Command(resume=...) 提供外部決策。"},
]


class State(TypedDict):
    question: str
    query: NotRequired[str]
    docs: NotRequired[list[dict]]
    draft: NotRequired[str]
    approved: NotRequired[bool]
    answer: NotRequired[str]
    status: NotRequired[str]


def normalize(state: State) -> dict:
    # Reset transient fields because the same thread can receive another question.
    return {"query": state["question"].strip().lower(), "docs": [], "draft": "",
            "approved": False, "answer": "", "status": "searching"}


def retrieve(state: State) -> dict:
    hits = [dict(doc) for doc in DOCUMENTS if any(key in state["query"] for key in doc["keys"])]
    return {"docs": hits}


def after_retrieve(state: State) -> Literal["draft", "refuse"]:
    return "draft" if state["docs"] else "refuse"


def draft_answer(state: State) -> dict:
    # Extractive fixed template: deliberately not an LLM or semantic retriever.
    text = "\n".join(f"{doc['text']} [{doc['id']}]" for doc in state["docs"])
    return {"draft": text, "status": "waiting_for_review"}


def review(state: State) -> dict:
    decision = interrupt({"question": state["question"], "draft": state["draft"],
                          "sources": [d["id"] for d in state["docs"]],
                          "expected": {"approved": "boolean", "edited": "optional string"}})
    if not isinstance(decision, dict) or type(decision.get("approved")) is not bool:
        raise ValueError("Decision must contain an approved boolean")
    edited = decision.get("edited", state["draft"])
    if not isinstance(edited, str):
        raise ValueError("edited must be a string")
    if decision["approved"]:
        allowed = {doc["id"] for doc in state["docs"]}
        cited = set(re.findall(r"\[(D\d+)\]", edited))
        if not edited.strip() or not cited or not cited.issubset(allowed):
            raise ValueError("Approved draft must cite retrieved document IDs")
    return {"approved": decision["approved"], "draft": edited}


def finalize(state: State) -> dict:
    if not state["approved"]:
        return {"answer": "審核未通過，未發布答案。", "status": "rejected"}
    return {"answer": state["draft"], "status": "done"}


def refuse(state: State) -> dict:
    return {"answer": "目前文件沒有足夠依據，請補充資料或換一個問題。", "status": "insufficient_evidence"}


def build_graph(checkpointer=None):
    builder = StateGraph(State)
    for name, node in [("normalize", normalize), ("retrieve", retrieve), ("draft", draft_answer),
                       ("review", review), ("finalize", finalize), ("refuse", refuse)]:
        builder.add_node(name, node)
    builder.add_edge(START, "normalize")
    builder.add_edge("normalize", "retrieve")
    builder.add_conditional_edges("retrieve", after_retrieve)
    builder.add_edge("draft", "review")
    builder.add_edge("review", "finalize")
    builder.add_edge("finalize", END)
    builder.add_edge("refuse", END)
    return builder.compile(checkpointer=checkpointer if checkpointer is not None else InMemorySaver())


if __name__ == "__main__":
    graph = build_graph()
    config = {"configurable": {"thread_id": "knowledge-demo"}}
    paused = graph.invoke({"question": "LangGraph 的記憶怎麼運作？"}, config)
    print("待審草稿:", paused["__interrupt__"][0].value["draft"])
    done = graph.invoke(Command(resume={"approved": True}), config)
    print("\n核准後:", done["status"], "\n", done["answer"])
