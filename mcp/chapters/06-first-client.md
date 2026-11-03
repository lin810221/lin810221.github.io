# 第一個 Client：探索、呼叫與檢查結果

不依賴 LLM，先證明工具、資源與提示模板可以正常互通。

## Client 不是模型

MCP Client 負責協定通訊，它不會自動理解自然語言，也不會自行選工具。本單元直接以 Python 決定要執行的操作，讓每個步驟都有固定輸入與預期輸出。後面在 Host 加入模型時，替換的是決策來源，而不是已驗證的工具契約。

`async with Client(server)` 建立測試用的程序內連線；給 URL 則使用 HTTP；給 `StdioServerParameters` 則由 Client 啟動子程序。這些方式共用相近的方法介面，但只有後兩者會驗證真實傳輸與程序邊界，測試報告必須清楚區分。

## 先探索再呼叫

`list_tools()` 回傳的不是裸陣列，而是包含 `.tools` 的結果。每個 Tool 有 `name`、`description`、`input_schema` 等欄位。不要把列舉順序當成名稱，也不要把人類可讀 title 當成路由識別。工具名稱應透過穩定映射交給呼叫流程。

連線後也可以查看 `protocol_version`、`server_capabilities`、`server_info` 與 instructions。新版允許伺服器不回傳身分，因此處理一般第三方 Server 時，要考慮 `server_info` 為 `None`，而不是立即存取 `.name`。

## 呼叫之後一定讀錯誤旗標

`call_tool()` 回傳 `CallToolResult`。先判斷 `is_error`，成功後才使用 `structured_content`。`content` 是不同內容區塊的聯集，文字、圖片、音訊與資源連結不能全部當成 `.text` 讀取。當你的應用只支援文字時，應明確處理其餘型別，不能默默宣稱內容完整。

本課的 `SearchResult` 有穩定欄位，因此可以做結構驗證。若工具只回傳自然語言，應用程式無法可靠地靠字串中包含「成功」來判斷業務狀態；需要交付的機器資料應透過 Schema 表達。

## 資源和 Prompt 走不同方法

`list_resource_templates()` 列出參數化 URI，`read_resource()` 才取得內容。`get_prompt()` 則渲染訊息模板。這些方法完成後不會替你生成一段模型回答；Host 仍需決定哪些內容進入模型上下文，以及是否符合使用者的資料授權。

## 練習與解答

在範例中列出每個工具的名稱，再讀取 `notes://guide/mcp`。解答的關鍵是使用 `.tools`、`.resource_templates`、`.contents` 與 `.messages` 這些不同結果容器。若只複製一個「萬用 result[0]」寫法，會在工具能用而資源不能用時產生難以解讀的型別錯誤。

## 可執行範例

在 `examples` 目錄執行 `python 02_first_client.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:02_first_client.py -->

## 官方閱讀

- [Client API 與結果](https://py.sdk.modelcontextprotocol.io/client/)
- [Client transports](https://py.sdk.modelcontextprotocol.io/client/transports/)
