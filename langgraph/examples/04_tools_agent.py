"""Real tool protocol, deterministic simulated model. No provider API call."""
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


def simulated_model(state: MessagesState) -> dict:
    last = state["messages"][-1]
    if isinstance(last, ToolMessage):
        return {"messages": [AIMessage(content=f"計算結果是 {last.content}。") ]}
    # Fixed request for teaching the protocol; this is not natural-language parsing.
    return {"messages": [AIMessage(content="", tool_calls=[{
        "name": "multiply", "args": {"a": 6, "b": 7}, "id": "call-demo-1", "type": "tool_call"
    }])]}


def build_graph(model_node=simulated_model):
    builder = StateGraph(MessagesState)
    builder.add_node("agent", model_node)
    builder.add_node("tools", ToolNode([multiply]))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    return builder.compile()


if __name__ == "__main__":
    result = build_graph().invoke({"messages": [("user", "6 乘 7 是多少？")]}, {"recursion_limit": 12})
    for message in result["messages"]:
        print(message.type, repr(message.content), getattr(message, "tool_calls", None))
