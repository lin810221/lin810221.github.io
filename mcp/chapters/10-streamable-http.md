# Streamable HTTP：把工具提供給遠端 Client

理解單一端點、JSON／SSE 回應、Origin 與舊版傳輸的差異。

## 先看現代版的單一請求

Server 提供一個 MCP endpoint，例如 `/mcp`。Client 對它送出 POST，回應可以是 JSON，也可以是這個請求專用的 SSE 串流。SSE 可以承載進度等訊息，最後回傳完成結果；使用串流不代表它是另一個 HTTP API，更不表示一定有持久 Session。

2026-07-28 移除了協定層 Session 與舊式 GET 背景串流。長期變更通知改走 `subscriptions/listen` 的回應串流。若 Host 使用較舊協定，伺服器仍可能為相容性保留舊流程，必須查看實際協定模式。

## 啟動與呼叫

在安裝好的 `examples` 環境開兩個終端機。第一個保持 Server 執行，第二個執行 Client：

```powershell
python 05_http_server.py --serve --port 8765
```

```powershell
python 06_http_client.py --url http://127.0.0.1:8765/mcp
```

只執行 `05_http_server.py` 不會開埠，只會顯示準備好的 ASGI 路由。這個設計讓全部範例可以安全地自動檢查。Client 沒給 `--url` 時也是程序內測試，不能把那種成功當成 HTTP 已驗證。

## 接受內容與中繼資料

Client 要能處理 `application/json` 與 `text/event-stream`，並在請求送出所需的版本和能力標頭。若你用 curl 只送一個 JSON、卻漏掉 Accept 或版本欄位，Server 拒絕不代表工具故障。初學階段先用 SDK 產生正確傳輸，再用 Inspector 觀察封包。

## 為什麼只綁定 loopback

本課本機服務綁在 `127.0.0.1`，沒有刻意開放區域網路。正式對外服務要另外加入 TLS、授權、Origin 驗證、主機名稱允許清單、請求大小與速率上限。允許瀏覽器跨來源的 CORS 設定，也不能代替 MCP 所需的 Origin 檢查或 Token 驗證。

`stateless_http=True` 與 `json_response=True` 是此範例的傳輸設定。前者也影響 SDK 對舊版 Client 的 HTTP Session 行為，不應拿這個旗標推論所有業務狀態都可放在記憶體：審核與收據仍需保存到持久儲存。

## 練習與解答

先啟動 Server 再呼叫一次，停止 Server 後重試。第二次預期是連線失敗，並非 `matches=[]`。如果路徑寫成 `/sse` 卻用 Streamable HTTP Client，也可能是路由錯誤；請先核對端點及傳輸，再改模型提示詞。

## 可執行範例

在 `examples` 目錄執行 `python 05_http_server.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:05_http_server.py -->

## 官方閱讀

- [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [Server 部署](https://py.sdk.modelcontextprotocol.io/run/deploy/)
