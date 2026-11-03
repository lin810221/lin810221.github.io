# Header 參數與 _meta：路由資訊不等於身分

理解新版的參數標頭映射，並避免讓可偽造欄位決定租戶權限。

## 先區分三種資料

工具 arguments 是業務輸入；`_meta` 用於協定及擴充的中繼資料；HTTP headers 是傳輸層資料。它們可能彼此映射，但用途與可信度不同。某個欄位出現在 header 並不代表已經驗證，也不代表可以跳過 Schema。

在現代 MCP 中，版本與能力的主要事實仍來自請求本文。若標頭和本文不一致，服務應按協定拒絕，而不是選一個看起來比較可信的值。這能避免 gateway 與實際 handler 對同一請求做出不同判斷。

## x-mcp-header 解決什麼

某些 gateway 希望在不解析本文的情況下，依 region 等參數路由。工具 Schema 可以以 `x-mcp-header` 指定映射名稱，現代 HTTP Client 便將同一參數送到對應 `Mcp-Param-*` 標頭。Server 會檢查兩者一致性。

這仍然是模型或 Client 提供的參數，適合非敏感路由選項，不能直接當成已授權 tenant。若 region 影響資料權限，還要在驗證身分後檢查呼叫者是否能存取該區域。

## 型別與註冊限制

SDK 2.3.0 對映射參數做註冊檢查，支援簡單的 str、int、bool。float、複雜物件與沒有適當 Schema 的聯集不應被強行放進 header。Header 名稱也要合法且避免只差大小寫的重複，因為 HTTP 標頭不區分大小寫。

本例以 `WithJsonSchema` 明確宣告字串欄位。它只示範可合法註冊並列出 Schema，不宣稱已測試代理伺服器如何轉送標頭；實際部署仍要測試 Client、gateway 與 Server 三方一致。

## 真正身分從哪裡來

若使用者可以自行送出 `X-User: admin`，它就不能直接成為管理員身分。可信授權層應驗證 Token 或受保護的代理簽章，再產生 Server 內部 Principal。Header 傳遞的顯示語言與驗證後的 subject 可以同時存在，但不能互換。

## 練習與解答

檢查範例 Schema 中 region 的映射。再假設有人將本文 region=west、標頭 region=east，應拒絕不一致請求。最後思考：兩者都填 admin 是否能得到管理權限？不能，一致性只能證明兩份輸入相同，不能證明輸入者有權限。

## 可執行範例

在 `examples` 目錄執行 `python 13_header_parameters.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:13_header_parameters.py -->

## 官方閱讀

- [Header parameters](https://py.sdk.modelcontextprotocol.io/advanced/header-parameters/)
- [Context 的 headers](https://py.sdk.modelcontextprotocol.io/handlers/context/)
- [HTTP metadata](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
