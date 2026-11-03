# 驗收交付：產生可核對的報告與資料

讓專案成果包含執行證據、版本與限制，而不只是一張聊天截圖。

## 驗收應交付哪些東西

完整專案應有可重現環境、啟動與測試命令、資料契約、成功及拒絕案例，以及實際執行結果。對有副作用操作，報告還需要核對狀態、版本與收據，而不是只記錄模型回答「已完成」。

本課交付腳本在新目錄建立 SQLite 與 acceptance.json。報告保存 SDK 版本、測試 transport、模型 API 呼叫數、跨租戶查詢結果、另一租戶工單狀態和交易收據。它是本機驗收資料，不是正式服務的合規認證。

## 執行方式

```powershell
python 30_delivery_report.py
python 30_delivery_report.py --output .qa/run-001
python -m unittest discover -s . -p test_examples.py -v
```

第一條使用臨時目錄，結束後清除；第二條保留在你選定的目錄供檢查。每次交付用新目錄，因為腳本不會把已結案 T1 偷偷重置成 open。若重用舊資料庫而失敗，先確認資料狀態，不應用刪資料當作一般恢復策略。

## 報告要支持哪些結論

本課流程應顯示 alpha T1 已 closed、version=2，beta T1 仍 open，committed audit_count=1，provider_api_calls=0。跨租戶 notes 查詢不會取得 beta 私有文字。這些欄位各自對應一個可觀察不變量。

若要宣稱真實 HTTP 互通，需另執行本課 transport tests；若要宣稱某個模型產品可以使用，需在實際帳號完成產品整合。程序內成功、HTTP 成功和供應商成功，是不同層次的證據。

## 交付前清點敏感資訊

SQLite、Token、使用者文件與除錯日誌不應直接發布到 GitHub Pages。教材只打包虛構資料與程式；個人測試輸出請留在忽略目錄。若你把專題換成公司資料，更要先決定資料保存和存取政策，不能沿用公開教材的分享方式。

## 練習與解答

刪掉報告中的 transport 欄位，會失去什麼？你無法判斷成功來自程序內還是真實網路。再刪掉 beta_ticket，會少掉跨租戶未變更的證據。好的驗收報告不是越長越好，而是每個關鍵結論都有對應、可重跑的檢查。

## 可執行範例

在 `examples` 目錄執行 `python 30_delivery_report.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:30_delivery_report.py -->

## 官方閱讀

- [SDK 測試範圍](https://py.sdk.modelcontextprotocol.io/get-started/testing/)
- [Inspector CI 工具](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector/cli)
