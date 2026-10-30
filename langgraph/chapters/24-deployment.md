## 從腳本到服務，多了哪些責任？

腳本由你手動呼叫一次，服務則會同時面對多位使用者、重試、重啟、取消與長時間等待。部署的重點不只是開一個 port，而是讓執行、儲存和權限都有清楚的生命週期。

| 元件 | 應負責的事 |
| --- | --- |
| API | 驗證請求、確認身分、建立輸入與回應 |
| 圖 | 節點、路由、狀態轉移 |
| Checkpointer / Store | 執行進度與應用資料持久化 |
| Worker / Queue | 長工作、併發策略、重啟接手 |
| 觀測系統 | 日誌、trace、指標與警示 |

## 建議的專案結構

```text
knowledge-agent/
├── assistant/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   ├── tools.py
│   └── graph.py
├── tests/
├── pyproject.toml
├── langgraph.json
└── .env.example
```

`graph.py` 只組裝流程，模型與資料依賴在應用啟動時建立。需要測試時能替換依賴，不要在 import 時寄信、連線查詢或直接啟動圖執行。

## 路線一：Agent Server 與 LangGraph CLI

官方提供本機 Agent Server、Studio 及相關部署能力。最小設定可以指向已編譯的圖物件：

```json
{
  "dependencies": ["."],
  "graphs": {"assistant": "./assistant/graph.py:graph"},
  "env": ".env"
}
```

這裡假設專案已有可安裝的 `pyproject.toml`，且 `assistant/graph.py` 匯出 `graph`。`dependencies: ["."]` 不會替你憑空建立 Python 套件設定。

```powershell
python -m pip install "langgraph-cli[inmem]"
langgraph dev
```

CLI、Studio 和服務可能有額外環境及帳號需求，請依當前官方安裝文件操作。本課未在這個環境實際啟動 Agent Server；它是部署路線說明。

Agent Server 會管理 persistence 基礎設施，**不要直接把本課內建 InMemorySaver 的開發圖原封不動當成正式部署設定**。將建圖拆成 builder factory，依使用環境決定 compile 方式與儲存管理。

## 路線二：嵌入自己的 API 服務

如果已有 FastAPI 或其他服務，可在啟動階段建立圖，路由裡呼叫 `ainvoke` 或產生串流。以下是架構片段，`graph`、認證與存取檢查需要由你的應用提供：

```python
from langgraph.types import Command

async def ask(graph, body, user):
    # 必須先確認 user 能存取 body.thread_id。
    config = {"configurable": {"thread_id": body.thread_id}}
    result = await graph.ainvoke({"question": body.question}, config)
    if result.get("__interrupt__"):
        return {"status": "waiting_for_review",
                "review": result["__interrupt__"][0].value}
    return {"status": result["status"], "answer": result["answer"]}

async def resume_review(graph, thread_id, validated_decision):
    config = {"configurable": {"thread_id": thread_id}}
    result = await graph.ainvoke(Command(resume=validated_decision), config)
    return {"status": result["status"], "answer": result["answer"]}
```

這些是經過認證與驗證後的內部處理函式，不是完整 HTTP API。正式服務還要處理存取權、每個 thread 的併發、逾時、錯誤回應，以及資料庫連線池。

## 長時間執行與人工審核

對需等數小時審核的工作，第一次請求應回傳待審狀態與穩定 ID，不要保持 HTTP 連線等人點擊。之後由受權的審核端呼叫 resume，再取回結果。

對大量模型與工具步驟，可改由工作佇列處理，前端輪詢或訂閱事件。執行者崩潰時，需有機制讀取 checkpoint 接手；資料持久化不會自行啟動新的 worker。

## 版本、遷移與上線驗證

固定套件及模型設定，記錄圖版本和 State schema 版本。變更節點名稱、移除欄位或調整 interrupt 順序，可能影響仍在等待的舊 thread。保留相容路徑或完成資料遷移，再切換新流程。

上線驗證至少包含健康檢查、真實儲存讀寫、未授權 thread 存取、斷線重試、重啟後恢復，以及未核准不得發布。`langgraph dev` 的開發模式不能直接代表正式高可用部署。

官方來源：[Application structure](https://docs.langchain.com/oss/python/langgraph/application-structure)、[Run a local server](https://docs.langchain.com/oss/python/langgraph/local-server)、[Deployment options](https://docs.langchain.com/langsmith/deployment-options)。
