# HTTP 上游 Adapter：限時、限量與結果驗證

把外部 API 的不穩定性隔離在明確契約內，避免直接透傳不可信回應。

## MCP Server 常常也是 HTTP Client

一個天氣、工單或資料搜尋工具，背後可能呼叫既有 REST API。MCP 只標準化 Host 到 Server 的互通；Server 到上游的驗證、逾時、重試、版本與憑證仍需自己管理。這是一個獨立的授權與錯誤邊界。

若上游需要服務憑證，Server 應依正式政策取得，不應將 incoming MCP Token 原樣轉送。兩者 audience 與權限目的不同。使用者委派情況也需明確的授權流程，而不是把任何 Bearer 字串往下一站傳。

## 固定端點與可注入 Client

本課 adapter 只呼叫固定 `/status`，HTTP client 的 base URL 由受信任配置提供。模型沒有任意 URL 參數。Client 由 lifespan 管理，可重用連線，也方便測試時注入 MockTransport，不需要對外服務才能檢查錯誤行為。

你仍需對實際 base URL、DNS、TLS 與重新導向建立政策。MockTransport 測試不會證明網路出口安全，因此測試報告要區分資料處理與真實網路環境。

## 先限制讀取，再解析資料

檢查成功狀態、content type，透過串流累計 bytes 並在超限時停止，最後才解析 JSON 和 Pydantic 模型。若先把無界 response 全部下載完，再檢查 len，記憶體上限就已經失效。

本課 `ServiceStatus` 只接受已定義的 service 和 status 欄位，未知 status 或額外結構不會被悄悄當成成功。對上游 429／5xx 等失敗，不在這個 parser 中自動重試，而交由外層明確的預算政策判斷。

## 來源與錯誤要保留

工具可以回傳資料時間與上游來源，讓模型區分最新值與快取值。上游 HTML 錯誤頁不應原樣送進模型當作業務內容；內部錯誤也不應包含 API Token 或完整 Authorization header。

## 練習與解答

測試有效 JSON、錯誤 MIME、未知狀態、429 與超大回應。成功案例產生型別化結果，其餘皆應拒絕。這些測試已以受控回應執行，沒有連到任何公開服務。正式串接後，還需另測 TLS、真實認證與上游限流。

## 共用 Adapter 原始碼

此模組與完整測試一起包含在下載包中，不需模型 API Key。

<!-- example:upstream_adapter.py -->

## 官方閱讀

- [SDK Lifespan](https://py.sdk.modelcontextprotocol.io/handlers/lifespan/)
- [SDK HTTP transports](https://py.sdk.modelcontextprotocol.io/client/transports/)
- [MCP 安全最佳實務](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
