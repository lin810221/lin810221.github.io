# Claude 整合：API Connector、桌面與開發工具

辨識產品層差異，使用當前 MCP toolset 配置，而非混用舊版 beta 範例。

## 先問使用的是哪個產品

Claude Messages API 的遠端 MCP Connector、桌面 Host 與開發工具的本機配置，是不同整合面。前者由雲端服務連遠端工具，後者可由本機程序啟動 stdio。即使使用相同模型，也不能把一個產品的設定檔直接當成另一個 API 的參數。

本課先用自己的 Client 驗證 Server，再依產品選配置，這樣連線問題不會與模型選擇混在一起。你不需要先購買任何模型服務，才能完成 Server、工具契約與工單專題。

## Messages API 的當前配置

查核時遠端 Connector 仍以 beta 形式提供。使用 `mcp_servers` 定義 URL 與 Server 名稱，再以 `mcp_toolset` 在 tools 中配置工具。新 beta header `mcp-client-2026-09-15` 支援記錄／固定工具清單；部分雲端平台的支援 header 仍不同，需按實際平台確認。

```json
{
  "mcp_servers": [{"type": "url", "name": "course_notes", "url": "https://mcp.example.invalid/mcp"}],
  "tools": [{"type": "mcp_toolset", "mcp_server_name": "course_notes", "default_config": {"enabled": false}, "configs": {"search_notes": {"enabled": true}}}]
}
```

這是配置片段，不含模型、訊息、認證與 beta header，不應當成可直接送出的完整 HTTP 請求。完整離線結構可參考下載包的 provider 配置範例。

## 工具清單變更與支援範圍

遠端 Connector 主要處理工具呼叫；不能假設 Resource、Prompt 或每個新協定互動都會自動進入模型。固定工具清單能降低對話中契約漂移，但 Server 仍須在每次呼叫檢查權限與輸入，不能把 pinned list 當成授權證明。

處理模型回傳內容時要識別工具相關區塊。採新 beta 的對話狀態應保留必要 listing 資訊，不能只取 content[0] 當最終文字而丟掉其他狀態。帳號功能、資料政策與模型支援需在正式環境另外確認。

## 本機 Host 的配置思路

本機通常需要 command、args、cwd 和必要 env。command 應指向確定的 Python 環境，args 分開保存腳本與 --serve。桌面 Host 不一定繼承你終端機的虛擬環境，因此「終端機可以跑」並不足以證明產品內可以啟動。

## 練習與解答

舊文章將 tool_configuration 放在 Server 定義，為何新配置可能不同？因為工具政策已移到 toolset，需按所選 beta 的當前格式遷移。再問本機 stdio 能否直接放進遠端 mcp_servers？不能，必須選產品支援的連線面，並獨立處理授權與網路可達性。

## 官方閱讀

- [Claude MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
- [MCP 本機連線](https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers)
