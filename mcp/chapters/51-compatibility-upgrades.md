# 相容性與升級：從 v1 到 v2 的檢查路線

將 import、型別、協定模式與 Host 差異整理成可驗證矩陣。

## 不只改一個版本號

SDK v2 的主要入口、欄位與低階 Server 引擎都有變更。升級時先固定既有基準與測試，再分別遷移工具宣告、Client、輸出型別、錯誤處理與傳輸設定。若同時改掉資料庫和模型，很難把行為差異歸因到正確來源。

本課使用 MCPServer 與高階 Client，避免讓新學習路線依賴已移除的 import。仍維護舊系統時，可以保留受測的維護分支，並讓兩種協定模式的相容測試證明服務能互通。

## 一份實用的升級表

| 檢查 | 要核對的行為 |
| --- | --- |
| import | FastMCP 舊路徑與 MCPServer 新路徑 |
| Python 型別 | snake_case、mcp-types 與 alias 序列化 |
| Client lifecycle | 高階 Client、低階 Session 與關閉責任 |
| 錯誤 | ToolError、MCPError、unexpected exception |
| HTTP | 現代 POST、SSE、舊 Session 相容性 |
| 互動 | 舊 callback 與現代 MRTR |
| 擴充 | 核心能力、版本與雙端支援 |

不要從 README 的最小例子推論所有低階 handler 都有自動驗證。v2 的低階介面需要你更明確維護輸入檢查與完整結果，詳細遷移應以官方 guide 對照實際使用的功能。

## 相容性矩陣至少有四個維度

協定版本、SDK 版本、傳輸、Host 產品與版本，都可能改變結果。你可以用新 SDK 服務舊 Host，也可以用同一高階 Client 測現代與 legacy，但應記錄實際連線結果，不能只看已安裝套件。

本課會驗證程序內現代模式與 legacy 模式，還有真實 stdio／HTTP。沒有執行的供應商帳號與容器環境則保留限制。這比一張全部打勾、卻沒有對應測試的支援表更有用。

## Schema 與工具語意也要版本化

新增選用欄位可能相容，刪除必填欄位、改名或改變 total 語意則可能破壞呼叫者。若結果仍是相同 JSON 形狀，卻由全部命中數改成當頁筆數，也需要注意下游解讀。版本管理不只是讓程式能 import。

## 練習與解答

把測試 Client 切為 legacy，觀察協定版本成為 2025-11-25，而工具業務結果仍相同。這證明的是該工具在這兩種模式可用，不代表所有擴充與互動都相容。升級紀錄應列出實測功能，避免過度延伸結論。

## 官方閱讀

- [Migration Guide](https://py.sdk.modelcontextprotocol.io/migration/)
- [Protocol versions](https://py.sdk.modelcontextprotocol.io/protocol-versions/)
- [SDK v2 變更](https://py.sdk.modelcontextprotocol.io/whats-new/)
