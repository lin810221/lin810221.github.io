# 驗收與交付：產出能重建的搜尋專案

將功能、隔離、故障重送與備份重建轉成可檢查報告。

## 交付不只是一張搜尋截圖

一份可維護專案應包含來源 fixture、schema、recipe、依賴版本、可執行入口、測試、設定範例與限制。本課壓縮檔可獨立解壓使用，網站只負責閱讀；不依賴網頁打開時執行 Python，也不會從瀏覽器存取你的本機資料庫。

## 實際執行的驗收

32_delivery_report 在新目錄建立來源與 Qdrant Local，測兩租戶查詢、保存來源備份，接著從備份重建另一個全新索引，比較查詢 ID，輸出 acceptance.json。目的地必須不存在，避免覆蓋既有專案；未指定時使用臨時目錄並在離開時清理。

## 讀懂報告

報告中的 SDK 版本、mode、來源資料、alpha/beta hits 與 restore IDs 都來自當次執行。它不宣稱遠端服務已啟動、RLS 已驗證或備份可跨任意服務版本恢復。無模型 API 呼叫表示主線不需要金鑰，但首次安裝依賴仍需要取得套件。

## 完整驗收清單

文字 token/排名、向量 Exact/ANN、每路 Filter、權威 hydration、版本拒絕、outbox 回滾、寫後當機重送、刪除不復活、Local 重開、索引檔檢查碼、generation 門檻與來源重建都有測試。服務路線另需真實引擎的 DSL/SQL、RLS、ANN 計畫、快照與負載驗收；這些不應被離線報告勾成已完成。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 32_delivery_report.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:32_delivery_report.py -->

## 練習與解答

**請先嘗試：** 交付測試通過，可否直接寫 production-ready？

<details><summary>展開解答與判斷依據</summary>

應具體寫已通過哪些範圍。這是完整可學習與本機驗收的專題，尚需依部署環境補認證、資源、監控、服務整合與負載故障測試。避免用模糊標籤蓋過未驗證項目。

</details>

## 官方文件與延伸閱讀

- [APSW 官方導覽](https://rogerbinns.github.io/apsw/example.html)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)
- [Qdrant Snapshots](https://qdrant.tech/documentation/operations/snapshots/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
