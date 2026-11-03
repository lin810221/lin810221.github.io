# 總練習、詳解與版本速查

用設計題和故障情境檢查理解，並整理日常開發最常查的路線。

## 基礎題與解答

**題一：MCP Client 是否等於 Agent？** 不是。Client 處理協定；Agent 還需要決策、工具政策、結果回饋與停止條件。沒有模型的測試程式也能當 Client。

**題二：新協定是否一定先 initialize？** 不需要。2026-07-28 採每請求 metadata，可先 server/discover；舊模式才使用握手。高階 Client 的 async with 管理的是 SDK 生命週期，不能將它等同於舊線上握手。

**題三：HTTP 200 是否代表工具成功？** 不一定。回應可能含工具失敗或協定資訊，必須檢查對應型別與 is_error。真正業務效果還需以狀態與收據核對。

## 契約題與解答

**題四：工具輸入合法就能執行嗎？** 仍需身分、scope、ACL 和狀態條件。有效 ticket_id 不表示屬於當前租戶。

**題五：為什麼成功結果沒有 structured content？** 可能工具沒有宣告可結構化的回傳型別、刻意關閉，或只回傳非結構內容。不要僅根據函式實際 return dict 就假設 SDK 一定產生 output schema；應檢查宣告與列舉結果。

**題六：Tool annotations 能保證唯讀嗎？** 不能，它是提示。實際資料權限與副作用由程式、資料庫及外部系統控制。

## 安全與交易題解答

**題七：模型填 tenant=admin 能切換租戶嗎？** 不應。主體來自可信驗證層，模型參數不能修改它。

**題八：核准後資料版本變更怎麼辦？** 拒絕舊預覽，建立新預覽並重新審核；不能無條件覆寫。

**題九：寫入 timeout 後直接重試？** 先辨識結果未知，透過收據或相同冪等鍵確認。不同 key 可能成為不同操作。

**題十：兩個 worker 各有本機去重字典是否足夠？** 不足，需共享且可協調的持久交易或上游等價保證。

## 版本與實測矩陣

| 項目 | 本課基準／實測範圍 |
| --- | --- |
| 查核日 | 2026-11-03 |
| 主要協定 | MCP 2026-07-28 |
| 官方 Python SDK | mcp 2.3.0，mcp-types 2.3.0 |
| Python | 本機 3.11.6；課程採 3.11+ 路線 |
| 傳輸 | 程序內、真實 stdio、loopback Streamable HTTP |
| 相容性 | 另測 legacy 2025-11-25 |
| 認證 | 離線 JWT fixture 與受保護 ASGI 請求；非正式 IdP 登入 |
| 供應商整合 | 配置與契約教學；未執行付費模型 API |
| 部署 | ASGI 與維運教學；未替你發布容器或雲端服務 |

PyPI metadata 與官方文件對 Python 最低版本的文字可能不同；本課以實際 3.11 環境與鎖版測試為依據，不宣稱已測每一個 Python 版本。正式更新應重新執行完整測試矩陣。

## 日常速查路線

先查 [SDK Client](https://py.sdk.modelcontextprotocol.io/client/) 的結果型別，再查 [Tools](https://py.sdk.modelcontextprotocol.io/servers/tools/) 與 [Structured Output](https://py.sdk.modelcontextprotocol.io/servers/structured-output/)。連線看 transports，登入看 authorization，升級看 migration。遇到舊文章時，先確認版本，避免把不同 API 世代混在一起。

完成本課後，可以把自己的唯讀系統包成工具，逐步加入受控寫入。開始前先寫下輸入、輸出、身分來源與成功證據，再寫程式；這些契約能讓 MCP 從展示連線變成可維護的工程整合。

## 官方閱讀

- [SDK 2.3.0](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0)
- [Current 協定](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning)
- [Migration](https://py.sdk.modelcontextprotocol.io/migration/)
