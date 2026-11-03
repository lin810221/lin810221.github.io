# 把 MCP 接進 Agent 控制迴圈

讓模型提出呼叫，讓 Host 執行政策，讓 Server 維護事實。

## Agent 多了哪一段

前面的 Client 都由程式決定工具名稱與參數。加入模型後，模型成為呼叫提案的來源：Host 提供工具定義，模型回傳一個或多個呼叫，再由 Host 決定哪些可以執行。MCP Server 仍然保持相同契約，不需要知道模型品牌。

一個完整迴圈至少包含：取得允許工具、呼叫模型、解析工具提案、驗證允許清單與預算、執行、把真實結果送回模型，以及判斷是否結束。只把工具清單丟給模型，還不算完成可運作的 Agent。

## 用測試替身先驗證路由

本課的 proposals 是固定資料，代表模型可能產生的呼叫。這能測試未知工具是否被阻止、超出預算是否停止，以及失敗結果會不會被包裝成成功。沒有 API 費用，也不會因模型隨機性讓每次測試結果不同。

真實供應商 adapter 應保留 call_id 或 tool_use_id，使工具結果對應原始提案。不同 API 對多工具、串流和對話歷史的格式不同，應分別處理，不能把 JSON 欄位名稱全部視為通用標準。

## 三道檢查各自獨立

| 位置 | 要檢查的事情 |
| --- | --- |
| Host | 工具是否開放、是否需審核、呼叫數與時間預算 |
| Server | 已驗證主體、輸入與業務條件 |
| 結果處理 | is_error、輸出 Schema、資料大小與來源 |

Host 的允許清單可以改善使用範圍，但無法取代 Server 的資料權限。Server 的權限正確，也不代表 Host 可以無限制呼叫同一工具；仍需避免無限迴圈與高成本搜尋。

## 何時應停止

模型輸出最終回答、使用者取消、預算耗盡、缺少權限或不可恢復錯誤，都可能終止迴圈。停止後要清理連線與待處理工作。工具結果有資料不足時，模型應保留不確定性，而不是為了結束流程編造一個成功狀態。

## 練習與解答

把提案改成 close_ticket，本例 Host 應拒絕，因為只允許 search_notes。再送三次搜尋、max_calls=2，第三次應被預算阻止。這兩個測試驗證的是程式可強制的控制，不是模型是否願意遵守一句「不要亂用工具」。需要更完整編排可接 [LangGraph](../langgraph/index.html)。

## 可執行範例

在 `examples` 目錄執行 `python 17_agent_loop.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:17_agent_loop.py -->

## 官方閱讀

- [Build a Client](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-client)
- [Client best practices](https://modelcontextprotocol.io/docs/2026-07-28/develop/clients/client-best-practices)
