# Inspector 與第一輪整合除錯

用可觀察的請求和回應定位問題，建立不依賴模型猜測的驗證流程。

## Inspector 放在哪個位置

Inspector 是 MCP 的開發檢查工具，可以列出工具、檢視 Schema、填參數、讀資源與觀察協定訊息。它扮演 Client／Host 的測試介面，不會替你證明業務權限正確，也不會讓未支援新版本的產品自動升級。

當某個工具在桌面助理中失敗時，先用 Inspector 或本課 Client 單獨呼叫。如果獨立呼叫也失敗，優先檢查 Server 與傳輸；若獨立成功，才回頭檢查 Host 的允許清單、參數轉換、協定模式及上下文處理。

## 使用方式與版本注意

官方 Inspector 提供 Web、CLI 與 TUI 介面。使用前查看官方目前的 Node 要求與 release；不要把舊教材的 Node 最低版本當成永久保證。範例命令會透過 npx 取得套件，屬於開發者明確執行的下載，教材網頁本身不會啟動它。

```powershell
npx @modelcontextprotocol/inspector --cli python 01_first_server.py --serve --method tools/list
```

若你的 Inspector 版本對子程序旗標的解析不同，可先啟動 Web UI，將 command 填為虛擬環境 Python 的絕對路徑，再將腳本與 `--serve` 分別放入 args。不要把 Server 額外參數誤放成 Inspector 自己的旗標。

## 一次只測一條假設

建議順序是：確認程序能啟動、探索版本、取得工具清單、呼叫一個最小合法輸入、呼叫一個應失敗的輸入，最後才讀完整資源和寫入流程。這樣可以為每個問題保留明確的前提，而不是一次修改五個設定後只知道「現在似乎能用了」。

觀察時記錄 endpoint、transport、實際 protocol version、工具名稱與錯誤類型。請求裡若有 Token、文件或使用者資料，不應直接貼進公開 issue；先產生不含敏感內容的最小重現。

## 三層測試各自證明什麼

| 測試 | 可證明的事 | 不能取代 |
| --- | --- | --- |
| 純函式測試 | 查詢、權限與交易規則 | 協定序列化 |
| 程序內 SDK 測試 | 工具契約與 SDK 行為 | 真實埠與程序邊界 |
| stdio／HTTP 整合 | 封包、啟動、串流與清理 | 真實供應商帳號支援 |

## 練習與解答

用不存在的工具名呼叫一次，保存錯誤結果；再用已存在工具但錯誤參數呼叫。兩次都可能呈現失敗，但根因不同。解答應指出工具是否被探索到，以及請求是否抵達業務邏輯，不能只用「模型沒接好」當作所有問題的總結。

## 官方閱讀

- [Inspector](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector)
- [SDK Testing](https://py.sdk.modelcontextprotocol.io/get-started/testing/)
- [除錯](https://py.sdk.modelcontextprotocol.io/troubleshooting/)
