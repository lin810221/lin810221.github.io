# 版本基準：新版無狀態請求與舊版握手

以 2026-11-03 查核的 MCP 2026-07-28、Python SDK 2.3.0 為主線。

## 三種版本必須分開看

協定版本使用日期，例如 `2026-07-28`；Python SDK 使用套件版本，例如 `mcp==2.3.0`；你的工單服務也應有自己的應用版本。SDK 更新不表示每個 Host 立即支援全部新協定功能；服務版本增加，也不一定代表協定格式有變。

本課查核日期為 **2026-11-03**，主線使用當日官方 current 協定與正式穩定版 Python SDK。實測環境是 Python 3.11.6。套件鎖版是重現基準；日後更新教材時需重新查核、安裝與測試，不能只修改頁首日期。

## 2026-07-28 的核心差異

新版請求各自帶有版本與 Client 能力等 `_meta`，不再依賴協定層連線 Session 保存這些事實。Client 可以先用 `server/discover` 探索支援版本與能力，也可以依已知版本直接送出請求並處理不相容錯誤。探索本身不授權後續操作。

較舊的 `2025-11-25` 及之前協定，先進行 `initialize`，再以 initialized 通知完成連線準備。你仍然會在既有 Host 或舊教材看到這條流程，因此本課會解釋它，但不把它當成新版請求的必要前置步驟。

## Python SDK 的寫法也變了

| 舊寫法或習慣 | 本課主線 |
| --- | --- |
| `mcp.server.fastmcp.FastMCP` | `mcp.server.MCPServer` |
| 手動組合 Session 並 initialize | 高階 `Client` context manager |
| Python 欄位 `structuredContent` | `structured_content` |
| 假設 Server 主動向 Client 發出請求 | 新版採 MRTR 把輸入需求放入結果 |
| 把 GET 背景 SSE 串流當成現代 HTTP 必備 | 請求內 SSE 與訂閱請求各有生命週期 |

Python 欄位使用 snake_case，線上 JSON 仍依規範使用 camelCase，通常由 SDK 序列化處理。另有獨立的第三方 `fastmcp` 套件，不應把它的版本和 API 與官方 SDK 的歷史類別混用。

## 相容模式是有意識的選擇

本課預設 `Client(..., mode="auto")`，它會探索並在必要時退回舊握手。`mode="legacy"` 明確走舊版；固定現代版本則代表呼叫者已知對方支援，不能拿來證明探索成功。偵錯時記錄實際 `client.protocol_version`，不要從本機套件號猜線上協定。

## 練習與解答

看見舊教程要求 `await session.initialize()`，是否應直接刪除？先確認它使用哪個 SDK 與協定介面。高階 v2 Client 已管理連線，但低階舊版 Session 範例的生命週期不同。升級要連同 import、欄位、錯誤、傳輸及雙端測試一起做，不能只換一行類別名稱。

## 官方閱讀

- [Current 協定版本](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning)
- [SDK 2.3.0 發布](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0)
- [v2 變更](https://py.sdk.modelcontextprotocol.io/whats-new/)
