"""Functional API workflow with a resumable human review."""
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


@task
def prepare(topic: str) -> str:
    return f"關於 {topic} 的學習摘要。"


@entrypoint(checkpointer=InMemorySaver())
def workflow(topic: str) -> dict:
    draft = prepare(topic).result()
    approved = interrupt({"draft": draft, "question": "是否保留這份摘要？"})
    if type(approved) is not bool:
        raise ValueError("Expected a boolean decision")
    return {"answer": draft if approved else "已取消"}


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "functional-demo"}}
    print(workflow.invoke("LangGraph", config))
    print(workflow.invoke(Command(resume=True), config))
