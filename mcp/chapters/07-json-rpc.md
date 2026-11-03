# JSON-RPC 與請求中繼資料

看懂線上的訊息，分清楚 request、response、notification 與內容型別。

## 一個請求由哪些欄位構成

MCP 使用 JSON-RPC 2.0。請求有 `jsonrpc`、`id`、`method` 和選用的 `params`。ID 用來配對回應，並不是登入 Token，也不是保證只執行一次的冪等鍵。在同一個送出者仍有未完成請求時，不應重用相同 ID；MCP 的請求 ID 也不能是 null。

以 `tools/list` 為例，method 表示操作，params 可以包含分頁 cursor 與 `_meta`。通知沒有 ID，也不預期一般請求回應；取消與進度等訊息必須依所用協定和傳輸規則處理。不要為所有 JSON 物件加一個 ID，就以為已經完成協定實作。

## 新版每次都自帶資訊

在 2026-07-28，`_meta` 裡的 `io.modelcontextprotocol/protocolVersion` 與 `io.modelcontextprotocol/clientCapabilities` 是每個請求的重要資料。Client 身分資訊則是選用。HTTP 還會把部分資料映射到標頭，供中介層處理，但本文內容仍是協定事實來源。

SDK 通常替你補齊這些欄位。手寫封包時若只照搬官方為了簡潔而省略 `_meta` 的片段，可能得到一個看似合理、實際不完整的請求。教學中的封包要分清楚「欄位說明」與「可以直接送出的完整請求」。

## 成功、失敗與工具失敗

JSON-RPC 回應的 ID 應對應原始請求，而且只能有 `result` 或 `error` 其中之一。新版正常結果包含 `resultType`，例如 `complete`。JSON-RPC error 則包含 code、message 和可能的 data，代表協定層無法正常完成這個請求。

工具找到合法輸入但無法完成業務時，也可能正常回傳 `CallToolResult`，其中 `isError=true`。這與 JSON-RPC error 不同：前者是工具執行結果，後者是請求層失敗。Host 應兩種都能處理，而不是看到 HTTP 200 就當成成功。

## Python 名稱與線上 JSON

Python SDK 使用 `input_schema`、`structured_content` 等欄位，線上則是 `inputSchema`、`structuredContent`。若要檢視序列化結果，使用 SDK 的 alias 輸出方式，而不是把 `__dict__` 直接丟進 JSON。讀取日誌時也要知道看到的是 Python 物件還是原始封包。

## 練習與解答

把範例回應 ID 改成 2，應拒絕配對；再同時加入 result 和 error，也應拒絕。最後思考：請求 ID 每次相同，是否能阻止重複扣款？不能；協定關聯 ID 不會替資料庫保存交易結果，寫入需要另行設計冪等契約與收據。

## 可執行範例

在 `examples` 目錄執行 `python 03_wire_messages.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:03_wire_messages.py -->

## 官方閱讀

- [基本訊息與 _meta](https://modelcontextprotocol.io/specification/2026-07-28/basic)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
