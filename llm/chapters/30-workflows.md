## 先從固定流程開始

如果任務明確是「檢索、草稿、審核、發布」，用固定路徑可以直接驗證每個步驟。只有其中某一步需要依中間結果決定工具時，才加入 Agent 迴圈。

這能讓 AI 自由度集中在有價值的位置，同時保留可預測的資料處理和授權規則。

## 三種常見組合

| 架構 | 資料流 | 適合情境 |
| --- | --- | --- |
| 固定 Workflow | 程式決定下一站 | 清楚的業務順序 |
| Workflow 中的一個 Agent | 固定外框、局部模型選工具 | 部分任務需要彈性 |
| 多 Agent 協作 | 專家各自處理、再整合 | 明確的上下文或工具分工 |

多 Agent 並不保證更準，也可能增加訊息傳遞、重複工具與費用。先用單一 Agent 的基線比較，再決定是否拆分。

## Router、Supervisor 與 Handoff

Router 根據問題交給特定專家；Supervisor 安排多個任務再整合；Handoff 將對話或控制責任交給另一個角色。這些模式可以用一般函式或圖表達，不一定需要新的套件。

交接時明確定義任務、允許資料、工具範圍與結果 schema。不要把所有專家的完整原生歷史任意串在一起，尤其可能破壞工具配對或帶入不相關指令。

## 和 LangGraph 串接

在已定義 State 的圖中，可以把模型服務當成一個節點：

```python
from provider_requests import request_for, call_live

def draft_node(state):
    body = request_for("openai", model_id, state["prompt"], 4096)
    reply = call_live("openai", body)
    if reply.status != "completed":
        raise ValueError(f"Generation not completed: {reply.status}")
    return {"draft": reply.text}
```

這是連線節點片段，model_id 需由設定提供。實際圖還要有 State、路由、儲存與錯誤策略。若節點中有長工具迴圈，也要確認取消與恢復邊界。

## 狀態應該保留什麼？

保存問題、必要原生歷史或其持久引用、檢索 ID、草稿、審核版本與工作狀態。模型物件、資料庫連線和憑證應作為執行依賴，不必全部寫進 checkpoint。

圖的 checkpoint 和供應商的 response ID 解決不同問題。前者描述應用流程進度，後者描述服務內的資源；兩者的保存期限和可用性需要一起設計。

## 平行、重試與副作用

只有互相獨立的工作才適合平行。重試可重跑模型或工具，但不能假設外部動作沒收到回覆就是沒成功。每一個發布或交易邊界都應有明確去重。

**練習：**將第 36 章的知識助理畫成圖，指出哪些節點可以替換供應商，哪些應保持固定規則。接著閱讀 [LangGraph 完整課程](../langgraph/index.html) 的 checkpoint 與人工審核章節。

官方來源：[LangGraph thinking](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)、[LangGraph workflows](https://docs.langchain.com/oss/python/langgraph/workflows-agents)、[Google ADK](https://adk.dev/)。
