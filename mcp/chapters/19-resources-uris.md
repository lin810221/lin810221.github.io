# 資源與 URI 模板：把內容提供給 Host

設計穩定可引用的內容介面，並保持讀取權限、大小與版本清楚。

## URI 是識別，不是任意檔案路徑

`notes://guide/mcp` 是本課定義的資源 URI，Server 決定它對應什麼內容。它不代表 Host 可以讀取電腦上某個同名檔案，也不代表允許把 topic 換成任意磁碟路徑。URI 解碼、模板參數與底層路徑應分層處理。

穩定 URI 可以讓搜尋結果引用全文，讓 Host 在需要時再讀取，也讓測試能對照特定資源。若內容會更新，應提供修訂或資料日期，避免同一個引用在沒有說明下指向完全不同的內容。

## 固定資源與模板

固定資源透過 `resources/list` 探索；模板透過 `resources/templates/list` 探索。`notes://guide/{topic}` 只描述一組可讀取的 URI，本身不是完整文件。Client 填入 topic 後，再以 `resources/read` 取得內容。

本課示範只允許 mcp 與 approval 兩種 topic，不把任意輸入直接交給 `open()`。這種允許清單適合小型內容集合；正式文件平台可以依已驗證主體列出可用資源，再以穩定文件 ID 讀取。

## 回傳型別與大小限制

文字內容有 text、URI 與可能的 MIME；二進位內容有 blob 及對應 MIME。Host 需要分辨 `TextResourceContents` 和 `BlobResourceContents`，不能把所有結果都做 `.text`。工具回傳的 ResourceLink 也可能尚未被讀取，應保留其 URI 與授權要求。

資源可以很大，但模型上下文有預算。應定義最大 bytes、摘要或分段讀取方式，並在讀取前確認權限。不能先把完整機密文件送進模型，再要求模型只使用允許的段落。

## 內容不是可信指令

手冊、網頁或使用者文件可能包含「忽略規則」「把 Token 寄出去」等字句。Host 應把它們視為待分析資料，而不是新的高權限指令。Resource 的技術型別不會讓內容自動可信，來源、權限與使用目的仍需追蹤。

## 練習與解答

執行範例，觀察固定資源清單為空，但模板清單有內容，仍可讀取實際 URI。這是合理情況。再讀未知 topic，應得到錯誤，而不是自動嘗試任何 URL。解答要說明「可探索的模板」與「允許的參數值」不是同一件事，後者仍由服務契約決定。

## 可執行範例

在 `examples` 目錄執行 `python 11_resources.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:11_resources.py -->

## 官方閱讀

- [Resources 規範](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- [URI 模板](https://py.sdk.modelcontextprotocol.io/servers/uri-templates/)
