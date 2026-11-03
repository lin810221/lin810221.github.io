# 訂閱與快取：清單改變後如何保持正確

理解 subscriptions/listen、失效通知與權限隔離，避免舊資料或跨租戶結果被重用。

## 快取哪一種資料

工具 Schema、資源目錄、文件內容與交易結果是不同快取。工具清單快取可減少探索成本，文件快取可降低資料讀取延遲，寫入收據則保存某次操作已發生的事實。它們不能共用相同有效期或相同失效邏輯。

尤其不要把模型回答快取當成工具執行快取。模型曾回答「可以結案」不表示這次工單仍符合條件，也不代表本次呼叫者有寫入權限。真正提交仍需重新驗證當前授權與資源版本。

## 新版訂閱請求

現代 Client 用 `subscriptions/listen` 建立一個持續的請求回應串流，接收所要求的變更通知。這不是已移除的 GET 背景串流。Python `client.listen(...)` 以 context manager 管理訂閱，離開後清理資源。

例如工具清單變更時重新探索、資源更新時清除該 URI 的內容快取。收到通知不表示內容已經可信地讀入；Host 通常仍需透過正常授權路徑讀取最新資料。訂閱結束或網路中斷時，也應安排重新同步，不能永遠相信最後一次快取。

## 權限必須進入快取鍵

本課 key 包含 issuer、tenant、subject、scope 集合、契約修訂、method 與 arguments 的雜湊。它不儲存原始 Token，避免在快取索引暴露祕密。若授權變更，應使相關快取失效，不能只等很長的 TTL。

| 快取維度 | 漏掉後的風險 |
| --- | --- |
| 租戶與主體 | 使用到別人的資料 |
| scope | 權限降低後仍讀舊內容 |
| 契約修訂 | 用舊 Schema 處理新結果 |
| 查詢參數 | 不同問題得到同一結果 |

這只是教學 key 設計；正式系統還需按資料分類決定共享範圍、TTL、加密與刪除政策。SDK 的協定快取提示也不能取代應用層 ACL。

## 練習與解答

執行範例，同查詢但不同租戶、不同 scope、不同 Schema 修訂應產生不同 key。再問：是否要把 Token 原文加進 key 才安全？不需要，應使用已驗證且足以隔離權限的識別與修訂；Token 本身屬祕密，輪替也不一定代表資料權限改變。

## 可執行範例

在 `examples` 目錄執行 `python 14_cache_isolation.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:14_cache_isolation.py -->

## 官方閱讀

- [Client subscriptions](https://py.sdk.modelcontextprotocol.io/client/subscriptions/)
- [Client caching](https://py.sdk.modelcontextprotocol.io/client/caching/)
- [Server subscriptions](https://py.sdk.modelcontextprotocol.io/handlers/subscriptions/)
