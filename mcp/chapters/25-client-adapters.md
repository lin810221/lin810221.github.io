# 建立自己的 Client Adapter

把協定連線封裝成應用介面，同時保留錯誤、型別與生命週期資訊。

## Adapter 要隱藏什麼，保留什麼

應用程式不需要到處知道 stdio 或 HTTP 的建立細節，但需要知道呼叫是否成功、資料是否完整、以及操作是否可能有副作用。Adapter 可以集中連線、列舉與內容轉換，不能把所有錯誤吞掉後回傳同一個空字典。

可將公開介面設成 `discover()`、`call(name, arguments)` 與 `read(uri)`，內部管理真正的 SDK Client。若介面會在 context 結束後被重用，應重新建立 Client，而不是保留已關閉的連線物件。建立與清理責任要由同一層掌握。

## 四種連線輸入

本課已使用程序內 Server、stdio 參數與 URL。第四種是自行管理的 transport context manager，例如要提供特定 HTTP client、headers 或認證流程。這時你也必須確認 HTTP library 版本；目前 SDK 使用 httpx2，不能直接把舊版 httpx 的物件視為相容。

初學者先用高階 Client 的 URL 模式，讓 SDK 管理必要標頭與版本。等確定需要自訂 TLS、連線池、代理或 OAuth，再閱讀對應 transport API，避免為一個預設連線重寫半個 SDK。

## 將錯誤保留成穩定分類

Adapter 可以把連線失敗轉為 `TransportFailure`、把 `is_error` 轉為受控 ToolFailure、把輸出違約轉為 ContractFailure。保留 request_id 和原始分類供內部追查，但傳給模型的訊息應經過安全處理。這樣 Agent 才能按類別安排恢復，而不是猜錯誤字串。

讀取 content 時，也應明確回報不支援的型別。若只支援文字，不能悄悄丟棄圖片後說「這是完整結果」；可以保留可用摘要，並清楚說明還有哪些內容未處理。

## 網址不是可信設定

讓使用者填 Server URL 的 Host，必須考慮 SSRF、重新導向與資料傳送目的。對公司內部服務，可以由管理者提供允許清單與憑證綁定，而不是讓模型任意指定要連哪一台。Adapter 也不應把登入某個 Server 的 Token 轉送到另一個 origin。

## 練習與解答

先在本機啟動 HTTP Server，再給本範例 `--url`。拿掉 URL 後成功，是否表示 HTTP 還在服務？不表示，因為它明確切回程序內測試。好的 adapter 測試與日誌應保留實際 transport，避免把不同測試面的成功混為一談。

## 可執行範例

在 `examples` 目錄執行 `python 06_http_client.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:06_http_client.py -->

## 官方閱讀

- [Client transports](https://py.sdk.modelcontextprotocol.io/client/transports/)
- [OAuth client](https://py.sdk.modelcontextprotocol.io/client/oauth/)
