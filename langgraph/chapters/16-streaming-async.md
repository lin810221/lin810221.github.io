## Streaming 不是只顯示 token

執行長流程時，前端需要知道正在檢索、等待工具或等待人審核。LangGraph 可以傳出不同層次的進度。先決定 UI 需要什麼，再選事件模式。

| stream_mode | 代表資料 | 常見用途 |
| --- | --- | --- |
| updates | 節點回傳的局部更新 | 哪一步完成、更新哪些欄位 |
| values | 合併後的完整狀態 | 除錯或狀態同步 |
| messages | 模型訊息 chunk 與 metadata | 顯示逐步生成的內容 |
| custom | 自訂事件 | 檢索進度、工作階段 |
| debug | 詳細的執行資訊 | 開發除錯，避免直接公開敏感資料 |

一般 Python 節點不會自然變成 LLM token 串流。你可以用 custom mode 回報進度，但要明確區分「模擬輸出」和真實模型 token。

## 可執行的 v2 範例

以下以 LangGraph 1.1+ 的 `stream(..., version="v2")` 統一格式示範。程式會先產生 custom 進度，再產生 answer 節點的 updates。

<!-- example:07_streaming.py -->

每筆事件都有 `type`、`ns` 和 `data`。`type` 是事件種類，`ns` 表示子圖命名空間，`data` 的內容依種類不同。

## 舊格式不要混著解析

沒有指定 v2 的 stream-mode API，單模式和多模式的回傳形狀可能不同：單模式可能直接得到 payload，多模式可能是 `(mode, payload)`。舊文章若寫 `for mode, chunk in ...`，不能直接拿來解析 v2 的 dict。

在服務邊界轉換成自己的事件契約，例如 `{"kind":"progress","node":"retrieve"}`，讓前端不必跟著內部 Python 物件格式變動。

## 真正的模型 token

對含有聊天模型節點的圖，可選 messages 模式：

```python
for part in graph.stream(inputs, stream_mode="messages", version="v2"):
    message_chunk, metadata = part["data"]
    if metadata.get("langgraph_node") == "chat":
        print(message_chunk.content, end="", flush=True)
```

這是模型圖的片段，不能用沒有 LLM 的本章範例期待得到 token。多模態或工具呼叫 chunk 也未必是文字；產品要依供應商內容型別處理，不要只用 `str(content)` 拼接所有資料。

## Async 版本

```python
async def run(graph, inputs):
    async for part in graph.astream(inputs, stream_mode="updates", version="v2"):
        print(part["data"])
```

非同步節點中，模型用 `await model.ainvoke(...)`，資料庫使用相對應的 async 用戶端。不要在 `async def` 裡直接放同步阻塞的網路請求；那仍可能卡住事件迴圈。

取消、用戶端斷線及執行停止是不同事件。前端不再讀串流，不一定代表後端任務已取消；需要依服務架構明確決定是否繼續、暫停或中止。

## 新版 1.2+ 的 Event Streaming

官方新版文件建議多數新應用考慮 typed-projection event streaming，例如 `graph.stream_events(..., version="v3")`，以 `stream.messages`、`stream.output` 等投影讀取。它屬於較新 API，**不在本課 1.1.9 實測範圍**；不要把 LangChain `astream_events(version="v2")` 的 runnable 事件協定視為同一件事。

選一種明確的版本與介面，固定依賴，再針對實際事件做契約測試，比混用不同年份的片段可靠。

**練習：**只把 custom 進度與最後公開答案送往前端，避免把完整 State 內的文件與審核資料都公開。

官方來源：[Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)、[Event streaming — 1.2+](https://docs.langchain.com/oss/python/langgraph/event-streaming)。
