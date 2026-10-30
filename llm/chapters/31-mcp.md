## MCP 解決的整合問題

Model Context Protocol 提供應用與外部能力之間的協定。它可以讓不同 Host 以共同方式發現並呼叫工具或使用資源，減少每個整合都另寫一套介面。

MCP 不是模型本身，也不會自動產生一個 Agent；是否讓模型使用工具、如何顯示結果與授權，仍由 Host 應用決定。

## Host、Client、Server

| 元件 | 角色 |
| --- | --- |
| Host | 面向使用者或任務的應用，管理模型與整合 |
| Client | 在 Host 中負責與特定 Server 的協定連線 |
| Server | 提供工具、資源或其他支援能力 |

例如知識助理是 Host，其中的 Client 連到文件 Server。Server 描述可用的搜尋工具；Host 再依規則把適合的工具交給模型。

## Tools、Resources 與 Prompts

Tools 表達可呼叫能力；Resources 提供可讀資料或內容參照；Prompts 提供可使用的提示模板。不同型別的發現和使用方式不同，不必全部都轉成同一種工具。

工具描述通常包含名稱、說明與 input schema。Host 發現後，仍要確認能力範圍和可信程度，不能因為 schema 合法就授予所有使用者存取。

## 一次整合的概念流程

```text
建立連線 → 協商支援能力 → 發現工具 / 資源
    → Host 選擇可提供給模型的能力
    → 模型提出請求 → Host 授權 → 呼叫 Server → 回傳結果
```

協定版本與傳輸方式需依目前官方規格。常見本機與遠端整合在啟動、認證、session 和錯誤處理上並不相同。

## MCP 和 Function Calling 的關係

Function calling 描述模型提出工具請求的方式；MCP 描述 Host 與外部能力服務之間的通訊。Host 可以把 MCP 工具映射成模型可見工具，再把結果送回模型。

供應商的 remote MCP 整合可能替你處理部分連線與呼叫，但仍要管理可用 server、授權、資料範圍及必要核准。外部 Server 也可能傳回不可信內容。

## 和 Agent SDK、Skills 有何不同？

Agent SDK 提供執行抽象，MCP 提供整合協定，skills / 提示套件通常提供任務指引或資源。它們可以一起使用，但不是同一層。

MCP 也不等於所有 Agent 彼此協作的標準。多 Agent 的任務委派、狀態和責任交接，需要另外設計。

## 上線前的整合驗證

測試工具發現、錯誤參數、超時、認證到期、資源權限與重連。不要在 log 中保留 bearer token，也不要讓任意外部描述自動成為高權限指令。

**練習：**把「文件搜尋 Server」的 read-only 工具與「發布報告 Server」的寫入工具分開，說明 Host 應如何對待兩者的授權與核准。

官方來源：[MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)、[OpenAI MCP integration](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)、[Claude tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。
