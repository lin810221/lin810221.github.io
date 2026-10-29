"""Behavioral checks for the offline tutorial, never calls a provider model."""
import importlib.util
import sys
from pathlib import Path
import pytest
from langgraph.types import Command

HERE = Path(__file__).parent


def load(name):
    module_name = "tutorial_" + name
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def config(name):
    return {"configurable": {"thread_id": name}}


def test_first_graph_normalizes_before_greeting():
    graph = load("01_hello").build_graph()
    result = graph.invoke({"name": "  小林  "})
    assert result == {"name": "小林", "greeting": "你好，小林！"}


def test_parallel_reducer_preserves_each_contribution_once():
    graph = load("02_reducers").build_graph()
    result = graph.invoke({"events": ["initial"]})
    assert sorted(result["events"]) == ["A", "B", "initial"]
    assert result["summary"] == "A,B,initial"


@pytest.mark.parametrize("target", [1, 3, 5])
def test_loop_terminates_at_target(target):
    graph = load("03_routing").build_graph()
    result = graph.invoke({"count": 0, "target": target}, {"recursion_limit": 20})
    assert result["count"] == target
    assert result["answer"] == f"完成 {target} 次"


def test_tool_request_and_result_ids_match():
    graph = load("04_tools_agent").build_graph()
    result = graph.invoke({"messages": [("user", "6 * 7")]})
    messages = result["messages"]
    assert [m.type for m in messages] == ["human", "ai", "tool", "ai"]
    assert messages[2].tool_call_id == messages[1].tool_calls[0]["id"]
    assert str(messages[2].content) == "42"
    assert "42" in messages[-1].content


def test_threads_keep_separate_histories():
    graph = load("05_checkpoints").build_graph()
    a, b = config("a"), config("b")
    graph.invoke({"messages": [("user", "A1")]}, a)
    graph.invoke({"messages": [("user", "A2")]}, a)
    graph.invoke({"messages": [("user", "B1")]}, b)
    assert len(graph.get_state(a).values["messages"]) == 4
    assert len(graph.get_state(b).values["messages"]) == 2
    assert graph.get_state(a).next == ()


@pytest.mark.parametrize("approved", [True, False])
def test_review_requires_explicit_decision(approved):
    graph = load("06_approval").build_graph()
    cfg = config("review")
    paused = graph.invoke({"draft": "draft text"}, cfg)
    assert "__interrupt__" in paused
    assert "answer" not in paused
    result = graph.invoke(Command(resume={"approved": approved}), cfg)
    assert result["approved"] is approved
    assert result["answer"] == ("draft text" if approved else "草稿未核准。")


def test_v2_stream_has_custom_progress_and_update():
    graph = load("07_streaming").build_graph()
    parts = list(graph.stream({"question": "graph?"}, stream_mode=["updates", "custom"], version="v2"))
    assert [p["type"] for p in parts] == ["custom", "updates"]
    assert parts[0]["data"]["progress"] == 0.5
    assert "answer" in parts[1]["data"]["answer"]
    assert all("ns" in p for p in parts)


@pytest.mark.parametrize("topics", [[], ["A", "A", "B"], ["State", "Send"]])
def test_send_handles_empty_input_and_preserves_input_order(topics):
    graph = load("08_parallel").build_graph()
    result = graph.invoke({"topics": topics, "results": []})
    assert result["report"] == "\n".join(f"已處理 {topic}" for topic in topics)
    assert len(result["results"]) == len(topics)


def test_subgraph_adapts_contract_without_leaking_private_keys():
    result = load("09_subgraph").build_graph().invoke({"question": "  Hello Graph  "})
    assert result == {"question": "  Hello Graph  ", "query": "hello graph"}


def test_functional_workflow_resumes():
    workflow = load("10_functional").workflow
    cfg = config("functional-test")
    paused = workflow.invoke("State", cfg)
    assert paused["__interrupt__"]
    result = workflow.invoke(Command(resume=True), cfg)
    assert result == {"answer": "關於 State 的學習摘要。"}


def test_transient_error_retries_and_context_is_available():
    module = load("11_retry_context")
    graph, attempts = module.build_graph()
    result = graph.invoke({"question": "test"}, context=module.Context(user_id="student"))
    assert attempts["count"] == 2
    assert result["answer"] == "student: 已取得結果"


def test_capstone_refuses_unknown_question_without_review():
    graph = load("12_knowledge_assistant").build_graph()
    result = graph.invoke({"question": "推薦午餐"}, config("unknown"))
    assert result["status"] == "insufficient_evidence"
    assert "__interrupt__" not in result


def test_capstone_publishes_only_approved_edited_answer():
    graph = load("12_knowledge_assistant").build_graph()
    cfg = config("edited")
    paused = graph.invoke({"question": "記憶如何運作？"}, cfg)
    assert paused["answer"] == ""
    assert paused["__interrupt__"][0].value["sources"] == ["D1", "D2"]
    edited = "Checkpointer 保存 thread 狀態。[D1]"
    done = graph.invoke(Command(resume={"approved": True, "edited": edited}), cfg)
    assert done["answer"] == edited
    assert done["status"] == "done"


def test_capstone_rejection_does_not_publish_draft():
    graph = load("12_knowledge_assistant").build_graph()
    cfg = config("rejected")
    graph.invoke({"question": "記憶？"}, cfg)
    result = graph.invoke(Command(resume={"approved": False}), cfg)
    assert result["status"] == "rejected"
    assert "D1" not in result["answer"]


@pytest.mark.parametrize("decision", [
    {"approved": "true"},
    {"approved": True, "edited": "無引用"},
    {"approved": True, "edited": "錯誤引用 [D99]"},
    {"approved": True, "edited": 123},
])
def test_capstone_rejects_invalid_decisions(decision):
    graph = load("12_knowledge_assistant").build_graph()
    cfg = config("invalid")
    graph.invoke({"question": "記憶？"}, cfg)
    with pytest.raises(ValueError):
        graph.invoke(Command(resume=decision), cfg)


def test_next_question_resets_transient_fields_in_same_thread():
    graph = load("12_knowledge_assistant").build_graph()
    cfg = config("repeat")
    graph.invoke({"question": "記憶？"}, cfg)
    graph.invoke(Command(resume={"approved": True}), cfg)
    result = graph.invoke({"question": "推薦午餐"}, cfg)
    assert result["approved"] is False
    assert result["docs"] == []
    assert result["draft"] == ""
    assert result["status"] == "insufficient_evidence"
