## 常用 Import 與用途

| Import | 用途 |
| --- | --- |
| `from langgraph.graph import StateGraph, START, END` | 建圖與起終點 |
| `from langgraph.graph import MessagesState` | 內建 messages channel |
| `from langgraph.graph.message import add_messages` | 訊息 ID 合併規則 |
| `from langgraph.types import Command, Send, interrupt` | 跳轉、分發、暫停 |
| `from langgraph.types import RetryPolicy, CachePolicy` | 重試與節點快取政策 |
| `from langgraph.checkpoint.memory import InMemorySaver` | 程序內 checkpoint |
| `from langgraph.store.memory import InMemoryStore` | 程序內跨 thread 資料 |
| `from langgraph.runtime import Runtime` | 節點的 context 與 runtime 資源 |
| `from langgraph.prebuilt import ToolNode, tools_condition` | 工具協定執行與路由 |
| `from langgraph.func import entrypoint, task` | Functional API |

## 建圖的最短流程

```python
builder = StateGraph(State)
builder.add_node("work", work)
builder.add_edge(START, "work")
builder.add_edge("work", END)
graph = builder.compile()
result = graph.invoke(input_data)
```

State 和 work 必須先定義。這裡是語法速查，不是獨立程式。

## 常見操作對照

| 想做的事 | 使用方式 | 重要條件 |
| --- | --- | --- |
| 執行一次 | `graph.invoke(input, config)` | 回傳結果不是單純模型文字 |
| 非同步執行 | `await graph.ainvoke(...)` | 使用合適的 async 依賴 |
| 查看進度 | `graph.stream(..., version="v2")` | 解析對應格式 |
| 保留狀態 | `compile(checkpointer=saver)` | 每次提供正確 thread_id |
| 人工暫停 | `interrupt(payload)` | 有 checkpointer，payload 可序列化 |
| 回覆審核 | `invoke(Command(resume=value), config)` | 同一 thread 與可用持久資料 |
| 看狀態 | `graph.get_state(config)` | 查看 values 與 next |
| 看歷史 | `graph.get_state_history(config)` | 選對 checkpoint config |
| 更新快照 | `graph.update_state(config, update)` | 仍會使用 reducer |
| 動態多工作 | `Send("worker", task_input)` | 結果 channel 需正確聚合 |

## 錯誤訊息與排查方向

| 現象或錯誤 | 常見原因 | 優先檢查 |
| --- | --- | --- |
| `InvalidUpdateError` | 不合法節點回傳，或平行寫入衝突 | 回傳型別與 channel reducer |
| `GraphRecursionError` | 圖超出 super-step 上限 | 停止條件與實際路徑 |
| `KeyError` | 欄位尚未建立，或路由 mapping 無對應 | 前置節點及回傳值 |
| 對話一直重複 | 重送歷史，或累加回傳了舊列表 | 本輪增量與 message ID |
| 恢復後找不到待審 | 新 saver、新 thread、程序已重啟 | 儲存生命週期與 thread_id |
| 重跑多寄一封信 | interrupt 或 retry 重跑副作用 | task 邊界與外部冪等 key |
| 工具訊息被模型拒絕 | tool_call_id 缺失或歷史被截斷 | AI tool_calls 與 ToolMessage 配對 |
| 模型沒被呼叫卻有舊答案 | 快取或未清理的同 thread State | cache 和每輪初始化 |

## FAQ：我一定要用 LangChain 嗎？

不需要完整採用 LangChain 才能使用 LangGraph。節點可以呼叫任意 Python 函式或模型 SDK。本課使用部分 `langchain-core` 訊息和工具類別，是為了搭配現成協定。

## FAQ：一個 Node 就是一個 Agent 嗎？

不一定。Node 是執行單位；Agent 指包含模型決策與工具互動的行為組合。一個節點也可以包住另一張 Agent 子圖。

## FAQ：有 Checkpoint 就不會重複動作嗎？

不會自動保證。節點中途失敗、interrupt 恢復或 time travel 都可能重新執行後續程式。外部副作用仍需要穩定識別與去重機制。

## FAQ：為什麼傳空列表沒有清掉資料？

若 channel 使用串接 reducer，空列表只代表沒有新元素。清空需要明確覆寫機制、訊息刪除協定，或重新設計欄位的每輪範圍。

## FAQ：什麼時候應增加 recursion_limit？

先確認流程有合理的停止條件，且輸入確實需要更多節點步數，再適度增加。若只是模型一直來回呼叫工具，增加上限通常只會延後失敗並增加成本。

## FAQ：這份網站如何保存我的閱讀？

閱讀進度與每章筆記使用瀏覽器 localStorage。它不會同步到其他裝置；清除瀏覽器資料、換瀏覽器或移動本機路徑後可能需要重新記錄。重要筆記請自行備份。這和 Python 範例的 LangGraph checkpoint 是兩套不同功能。

官方來源：[LangGraph API reference](https://reference.langchain.com/python/langgraph/)、[LangGraph v1 migration](https://docs.langchain.com/oss/python/migrate/langgraph-v1)。
