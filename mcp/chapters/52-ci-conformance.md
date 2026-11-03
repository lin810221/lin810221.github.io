# CI 與協定驗收：每次更新都能重跑

把教材、範例、工具契約與真實傳輸檢查放入可維護的更新流程。

## 鎖版與更新是兩件事

requirements 鎖住這次已測的 MCP 2.3.0 與相依套件，讓讀者重現。下一次課程更新則重新查核正式版本、建立新環境、執行測試與記錄差異。自動安裝 latest 不能代替升級驗證，永遠停在舊環境也不是更新策略。

本課額外建立獨立 MCP CI job，避免新 SDK 的 HTTP 相依與既有 LangGraph 課程互相影響。教材編譯只需 Markdown 工具；執行 MCP 範例則在自己的隔離環境進行。

## 最小 CI 流程

```text
checkout → 安裝指定 Python → 安裝鎖版依賴
         → 純領域與安全測試 → SDK 契約測試
         → stdio／HTTP／Origin 測試 → 產生結果
```

網站另執行 Markdown 編譯、內部連結、公式與離線字型檢查。讀者不需要安裝 Python 才能看網頁，但修改原稿後必須重新編譯生成資料，才能讓網站呈現最新內容。

## Conformance 不等於完整業務驗收

協定 conformance 關注訊息、方法、版本與傳輸是否符合規範；業務驗收則確認跨租戶、審核、交易與收據是否正確。即使 Inspector 能成功列工具，仍可能存在 SQL 越權或重複寫入，兩者必須分別測試。

正式導入官方 conformance tooling 時，先查其當前版本、支援修訂與執行需求。本課不把自行寫的 unittest 冒稱官方認證，也不因某次工具列舉成功就宣稱整個 MCP 規範已完整實作。

## 讓失敗可以被診斷

CI 應保留測試名稱、版本、OS 與安全的失敗上下文。Transport 測試需要能開啟本機埠與子程序；受限環境可能拒絕這些動作，報告應區分環境限制與程式錯誤。測試服務必須在 finally 關閉，避免後續工作被占用的埠干擾。

## 練習與解答

故意刪掉輸出模型的一個必要欄位，契約測試應失敗；再移除 ACL，跨租戶測試應失敗。若 CI 仍綠燈，代表驗證沒有保護這些要求。只測試腳本能啟動，無法支持「此專案可以安全讓 Agent 操作工單」的結論。

## 官方閱讀

- [SDK Testing](https://py.sdk.modelcontextprotocol.io/get-started/testing/)
- [Inspector CLI](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector/cli)
- [官方規範來源](https://github.com/modelcontextprotocol/modelcontextprotocol)
