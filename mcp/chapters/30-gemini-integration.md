# Gemini 整合：CLI 設定與模型 Adapter

使用明確的工具允許清單，區分 Gemini CLI 與 API 的工具執行責任。

## CLI 和 API 是兩條不同路線

Gemini CLI 是已提供 Host 功能的工具，可管理 MCP Server、工具清單與確認流程。使用 Gemini API 自建應用時，則需要知道由哪一層管理 Client、函式轉換與呼叫結果。不能因 CLI 能讀資源，就假設任何 API 呼叫都會自動讀取 MCP Resource。

對初學者，先使用本課 stdio 範例與 CLI 配置理解現成 Host；需要自製網頁、特殊租戶權限或完整審核時，再建立自己的 adapter。這兩條路都能重用相同 Server，不必重新寫一份搜尋業務邏輯。

## CLI 的重要配置

設定檔中的 `mcpServers` 可以指定 command、args、cwd、env。遠端連線則需使用該版本要求的 HTTP 設定欄位。`trust: false` 保留工具確認流程，`includeTools` 限定可見工具。它們屬於 Host 政策，不會代替 Server 的資料權限。

```json
{
  "mcpServers": {
    "course_notes": {
      "command": "ABSOLUTE_PYTHON_PATH",
      "args": ["ABSOLUTE_EXAMPLE_PATH/01_first_server.py", "--serve"],
      "trust": false,
      "includeTools": ["search_notes"]
    }
  }
}
```

路徑應換成你的實際環境。不要把帳號密碼或 Token 直接寫入會推送到 Git 的 JSON；需要的祕密以產品支援的受控方式注入，並只傳給必要 Server。

## API 自動呼叫也要有邊界

官方 Python 範例中可能看到 ClientSession 的自動函式呼叫整合。那屬於特定 SDK 的支援介面，使用前需核對它與 MCP v2 的相容性，不要把舊 Session 建立方式直接貼進本課的高階 Client 程式。

保守且可控的做法是自行把已允許 MCP 工具轉為模型函式定義，檢查模型輸出後再透過 Client 呼叫。這需要處理名稱限制、Schema 支援範圍、呼叫 ID、結果型別和對話歷史，不能只做一個工具名稱字串替換。

## 練習與解答

檢查 provider 配置範例，CLI 應保持 trust=false 並只開放 search_notes。將寫入工具加入清單之前，應先完成 Server 的核准與冪等流程。若 CLI 顯示未連線，先查 command、args、信任目錄與 Server stderr；不要先調 temperature，因為那不會修正程序啟動問題。

## 官方閱讀

- [Gemini CLI MCP](https://geminicli.com/docs/tools/mcp-server/)
- [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)
