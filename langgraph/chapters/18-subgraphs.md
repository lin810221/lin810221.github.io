## 什麼時候需要子圖？

當檢索、文件評估與草稿產生已形成可重用的流程，把它們組成 subgraph，可以讓主圖只關心輸入與輸出。子圖本身仍是一張圖，能有分支、模型及工具。

不要因為檔案變長就盲目拆圖。先確認邊界：輸入是什麼、輸出是什麼、哪些資料只能留在內部。

## 方式一：共享欄位，直接當節點

```python
# parent 和 child 都有同名且相容的 question / answer 欄位。
# child 是已 compile 的子圖。
parent_builder.add_node("answer_pipeline", child)
```

這適合共享明確 channel 的父子圖。子圖內部可以有父圖不關心的欄位，但共享欄位的型別與合併規則必須一致。不要因為同名就假設用途相同。

## 方式二：不同契約，用包裝節點轉換

完整範例中的父圖使用 `question` 與 `query`，子圖使用 `text` 與 `normalized`。`adapt` 明確負責映射。

<!-- example:09_subgraph.py -->

執行後父圖結果包含 `question` 和 `query`，query 是 `what is state?`。子圖的 `text`、`normalized` 不會因為名稱不同而自動流入父圖。

## 為什麼明確轉換很重要？

多個 Agent 若各有私有訊息歷史，直接共享一個巨大的 messages 列表，可能讓不相關的工具協定或內部推論互相污染。包裝節點只傳入任務，取回結構化結果，更容易控制上下文。

另外，子圖回傳了整段父層已存在的訊息，再經父圖 add_messages 合併，可能造成意外更新。每個介面都應說清楚回傳的是新增訊息、最終答案，還是完整歷史。

## 持久化與觀察

父圖設定 checkpointer 後，可依子圖編譯方式與需求繼承持久化能力。子圖的 checkpoint namespace 協助區分執行位置。要區分每次呼叫各自獨立，還是子 Agent 跨輪保留歷史，不要假設兩者是同一種預設。

觀察巢狀執行時，可使用支援子圖的 stream 設定，以及 `get_state(config, subgraphs=True)` 查看可用資訊。子圖如果藏在框架無法辨識的動態封裝裡，可觀察性可能受限。

## 子圖內的 interrupt

若父節點呼叫子圖，而子圖中發生 interrupt，恢復時不只要理解子節點的重跑邊界，也要留意包裝父節點可能重新執行。因此父節點呼叫子圖前，不要放無法安全重跑的副作用。

需要子圖向父圖路由時，`Command(graph=Command.PARENT, goto=...)` 可以表達向上一層移交；這種耦合應有清楚契約，不能把任意內部節點名稱當公開 API。

**練習：**將本章 child 改成兩個步驟：strip 再 lower。父圖應不需要知道內部新增了節點，只維持相同輸入輸出。

官方來源：[Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)、[Command reference](https://reference.langchain.com/python/langgraph/types/Command)。
