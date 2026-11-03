# Prompt 與補全：提供可重用的使用流程

將訊息模板、參數建議與模型生成分開，避免混淆三種不同操作。

## Prompt 是準備訊息

例如使用者選擇「整理工單摘要」，填入工單主題，Host 取得一組訊息後再決定如何交給模型。MCP Prompt 的工作是渲染這些訊息，不會因為叫做 prompt 就直接呼叫模型，更不應在渲染時執行寫入。

Prompt 有名稱、描述與參數清單。它的參數是字串值，不等同 Tool 的任意 JSON Schema 參數。若需要複雜驗證或資料查詢，可以在合適的工具與領域層處理，不要把所有結構藏在一個難以驗證的字串中。

## 一個模板可以產生多則訊息

模板可以回傳單則文字，也可以安排多則訊息與資源內容，依 SDK 支援的型別構成。Host 必須知道其支援的角色和內容區塊，並決定如何與目前對話合併。不能把來自外部 Server 的模板無條件升級為全域系統政策。

本課 `explain(topic)` 輸出一則教學指示。你可以把它改成包含目標、格式與引用要求的模板，但仍需保留資料來源與不確定性；「請務必正確」不會代替事實查核。

## 補全是參數建議

MCP completions 用於在填入 Prompt 或 URI 模板參數時提供候選值。例如輸入 `ap`，回傳 `approval`。這不是語言模型的文字 completion，也不是自動補出缺少權限的資料。

補全請求包含要補哪個參照、哪個 argument，以及目前已輸入的值。有些情況還會帶其他已填參數作 context，讓候選更精確。候選清單應遵守同樣權限邊界，不能透過自動完成洩漏其他租戶的機密文件名稱。

## 設計可維護的模板

讓模板參數名稱穩定，避免突然改名導致 Host 表單失效。常用流程可以加入版本說明，但不必把全部內部 prompt-engineering 實驗暴露給每個使用者。對正式輸出，仍需透過 Schema 或驗收測試確認必要欄位。

## 練習與解答

執行範例，確認補全回傳 approval，而取得 Prompt 只回傳訊息。把輸入改為未知前綴，合理結果是空候選，不能假裝找到了近似文件。接著思考哪一層要呼叫模型：答案是 Host 或明確的應用流程，並非 `prompts/get` 本身。

## 可執行範例

在 `examples` 目錄執行 `python 12_prompts_completion.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:12_prompts_completion.py -->

## 官方閱讀

- [Prompts](https://py.sdk.modelcontextprotocol.io/servers/prompts/)
- [Completions](https://py.sdk.modelcontextprotocol.io/servers/completions/)
- [Prompt 規範](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
