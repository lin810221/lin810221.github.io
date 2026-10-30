## 如何使用這組練習？

先自己修改範例，再看參考做法。每題都有可觀察的通過條件，不要求程式碼和參考答案逐字相同。沒有涉及真模型的題目，都可以離線驗證。

## 練習一：拒絕空名字

修改第 4 章，在 normalize 後加入 validate。只有空白的名字應拋出 `ValueError`，正常名字仍產生問候。

參考節點：

```python
def validate(state: State) -> dict:
    if not state["name"]:
        raise ValueError("name 不得為空白")
    return {}

# 移除舊的 normalize → greet 連線，改為：
builder.add_node("validate", validate)
builder.add_edge("normalize", "validate")
builder.add_edge("validate", "greet")
```

**檢查：**`" 小林 "` 成功；`"   "` 失敗；不要在保留舊 edge 的同時又加新路徑，否則 greet 仍可能直接被啟動。

## 練習二：理解 Reducer 增量

將第 6 章的初始 events 改成 `["initial"]`，兩分支仍回傳 `["A"]` 與 `["B"]`。最後應恰好有三個項目。

```python
result = build_graph().invoke({"events": ["initial"]})
assert sorted(result["events"]) == ["A", "B", "initial"]
```

如果出現重複 initial，檢查節點是否回傳了整段 `state["events"]`。如果只剩 B，檢查該欄位是否真的設定 reducer。

## 練習三：兩個人的對話不要混在一起

延續第 12 章，A 說兩句、B 說一句。A 應有四則訊息，B 應有兩則。

```python
graph = build_graph()
a = {"configurable": {"thread_id": "A-chat"}}
b = {"configurable": {"thread_id": "B-chat"}}
graph.invoke({"messages": [("user", "A1")]}, a)
graph.invoke({"messages": [("user", "A2")]}, a)
graph.invoke({"messages": [("user", "B1")]}, b)
assert len(graph.get_state(a).values["messages"]) == 4
assert len(graph.get_state(b).values["messages"]) == 2
```

**思考：**若每個人各自有兩條 thread，要共享偏好應放在哪裡？參考答案是 Store，並由後端限制 namespace 範圍，不是把 thread_id 改成相同值。

## 練習四：審核可以修改，也可以拒絕

對完整專案先取得待審草稿，再提供 edited 字串。核准內容必須保留本輪的有效引用；拒絕時不得發布 edited。

```python
config = {"configurable": {"thread_id": "edited-review"}}
graph.invoke({"question": "記憶是什麼？"}, config)
result = graph.invoke(Command(resume={
    "approved": True,
    "edited": "Checkpointer 保存 thread 狀態。[D1]",
}), config)
assert result["answer"] == "Checkpointer 保存 thread 狀態。[D1]"
```

**檢查：**核准且引用有效才通過；改成 `[D99]` 或 `approved="true"` 應被拒絕；`approved=False` 應走 rejected。每個情境使用新 thread，以免前一個失敗狀態影響測試。

## 練習五：平行結果與空任務

把第 17 章的輸入改成 `["A", "A", "B"]`，結果應有三份並保持輸入索引順序。再用空 topics，結果應是空報告而非停在沒有輸出的狀態。

```python
graph = build_graph()
empty = graph.invoke({"topics": [], "results": []})
assert empty["report"] == ""

duplicate = graph.invoke({"topics": ["A", "A", "B"], "results": []})
assert duplicate["report"].splitlines() == ["已處理 A", "已處理 A", "已處理 B"]
```

如果要去重，應先決定業務是否將重複輸入視為同一工作，而不是隨手把列表轉成 set 丟失順序。

## 進階專題：替換一個邊界

在完整專案中只替換一項：真正的檢索器、模型草稿、SQLite 持久化或審核 API。先寫出介面和成功條件，再實作。至少保留無資料拒答、未核准不發布，以及重啟或下一輪不誤用舊狀態的驗證。

這些題目是教材原創練習；API 行為可查：[Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)、[Test](https://docs.langchain.com/oss/python/langgraph/test)。
