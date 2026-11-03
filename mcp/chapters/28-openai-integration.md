# OpenAI 整合：遠端 MCP 與自行管理工具

比較 Responses API 的 MCP 工具與自建 Client adapter，保留審核和結果控制。

## 兩條整合路線

第一條是你的應用管理 MCP Client，把工具轉為模型接受的函式定義，自己處理呼叫與結果。它適合本機 stdio、內網系統、特殊驗證，以及需要完全掌握工具路由的情況。第二條是使用 Responses API 的 MCP 工具，讓服務連接可用的遠端 Server。

官方也提供 Secure MCP Tunnel 等連接本機或私有服務的方式；這屬於供應商的連線能力，需要獨立設定與確認支援。本課的本機 HTTP Server 不會因為綁在 127.0.0.1，就自動能被雲端服務連到。

## 遠端工具設定的重點

遠端設定包含 `type: "mcp"`、server label、server URL、allowed tools 與審核政策。server label 是這次請求中的識別，URL 是能力服務位置；Token 與模型 API Key 則是不同祕密。工具清單應縮到任務必要範圍，避免一次開放全部寫入能力。

本課 payload 範例只建構 JSON，不發送 API。model 欄位故意留為需選擇的模型名稱，因為帳號可用模型與 MCP 支援可能不同。真正使用前，請依你的帳號與官方模型功能表選定並記錄版本。

## 審核是對話狀態的一部分

API 可能回傳 `mcp_approval_request`，應由應用呈現具體工具與參數，取得使用者決策後以對應 approval response 繼續。不能只在程式中看到待核准，就自動視為同意。設定 require_approval=always 是本課配置的預設，並非所有工具都可因此省略 Server 端審核。

Host 核准一次遠端工具呼叫，與業務上允許關閉某張工單，是兩種可疊加的控制。正式系統可要求 Server 同時驗證工單預覽、當前主體與核准紀錄，避免另一種 Client 繞過供應商 UI 直接寫入。

## 工具列表、上下文與成本

Responses 的輸出包含工具列舉、呼叫、結果與可能的核准項目。處理回應時應按型別分支，不要只假設第一個輸出區塊就是最終文字。工具 Schema 與結果也會使用模型上下文，因此縮小工具集合、限制結果大小及保留必要清單狀態都有實際價值。

## 練習與解答

檢查離線配置，確認只有 search_notes 開放，且沒有祕密字串。若要接本機 stdio，選自建 Client adapter，或先依官方支援流程建立受控連線；直接把 Windows 檔案路徑放進 server_url 不會變成遠端 MCP。模型 API 的端到端行為需實際帳號另測，不能以本課 JSON 驗證代替。

## 可執行範例

在 `examples` 目錄執行 `python 18_provider_configs.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:18_provider_configs.py -->

## 官方閱讀

- [OpenAI MCP servers](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)
- [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)
