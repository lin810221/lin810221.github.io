"""Same thread retains messages; a different thread starts a new conversation."""
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END


def respond(state: MessagesState) -> dict:
    user_turns = sum(message.type == "human" for message in state["messages"])
    return {"messages": [AIMessage(content=f"這是第 {user_turns} 個問題。") ]}


def build_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("respond", respond)
    builder.add_edge(START, "respond")
    builder.add_edge("respond", END)
    return builder.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":
    graph = build_graph()
    config = {"configurable": {"thread_id": "lesson-12"}}
    graph.invoke({"messages": [("user", "你好")]}, config)
    result = graph.invoke({"messages": [("user", "接著聊")]}, config)
    print(result["messages"][-1].content)
    snapshot = graph.get_state(config)
    print("next:", snapshot.next)
    print("messages:", len(snapshot.values["messages"]))
