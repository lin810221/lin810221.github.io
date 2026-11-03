# 工具、資源、提示模板：選對暴露介面

從行為、內容與互動目的，區分 MCP 的三種主要伺服器能力。

## 工具是可以要求執行的能力

Tool 有名稱、描述與輸入 Schema，可能還有輸出 Schema。`search_notes(query, limit)` 代表一項可執行查詢，`close_ticket(preview_id, idempotency_key)` 則代表有副作用的操作。工具可以唯讀，也可以寫入；是否寫入取決於實作與業務契約，而不是名稱看起來像不像查詢。

模型通常根據工具描述選擇呼叫，但 MCP 並未要求每個呼叫都由模型決定。一般 UI、測試程式或腳本同樣能透過 Client 呼叫工具，這也是本課先用確定性測試建立信心的原因。

## 資源是可識別的內容

Resource 以 URI 辨識，例如 `notes://guide/mcp`。它可以是文字、圖片或其他資料，但應有明確的型別與大小邊界。固定 URI 的資源與帶參數的資源模板分開列舉；模板 `notes://guide/{topic}` 並不是可以原樣讀取的文件，必須先填入允許的 topic。

Resource 是否會被模型讀到，取決於 Host 如何加入上下文。有些 Host 提供選取器，有些會主動讀取，有些整合介面只支援工具。因此你不能因為成功註冊 Resource，就假設所有模型都已取得內容。

## Prompt 是可以取得的訊息模板

Prompt 將常用流程或角色訊息做成可探索的模板，例如「根據工單記錄整理結案摘要」。取得 Prompt 只代表渲染訊息，並不等於呼叫模型，也不應在渲染階段寫入工單。模板參數、工具參數與使用者身分是不同資料，不要混成一個任意字典。

| 需求 | 適合的介面 | 不應假設的事情 |
| --- | --- | --- |
| 對關鍵字執行搜尋 | Tool | 搜尋結果必然可信 |
| 讀取已知操作手冊 | Resource | URI 等同檔案系統路徑 |
| 載入報告撰寫流程 | Prompt | 模板能提高資料權限 |
| 核准工單結案 | 受控審核流程 | 一句提示就能代替授權 |

## 可以重疊，但要有穩定語意

文件搜尋可以回傳 ResourceLink，再由 Host 決定是否讀取全文；也可以回傳摘要與穩定引用。這種組合能把「探索候選」與「讀取內容」拆開，控制上下文大小。若一個工具同時查詢、上傳文件、寫入與發信，就很難描述權限與重試規則，應按業務交易邊界拆分。

## 練習與解答

「提供部門手冊、列出待辦工單、產生報告模板」依序適合 Resource、Tool、Prompt。若部門手冊有不同權限，Resource 讀取仍需驗證主體；把敏感內容改成 Resource 不會繞過 ACL。實作時先為每種介面各做一個最小例子，再測試目標 Host 是否真的支援。

## 官方閱讀

- [伺服器能力](https://modelcontextprotocol.io/docs/2026-07-28/learn/server-concepts)
- [Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- [Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
