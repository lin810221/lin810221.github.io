# 備份、還原與重建：真正測一次才能知道能否恢復

以來源快照重建全新索引，區分舊 checkpoint 與新索引的資料水位。

## 定義 RPO 與 RTO

RPO 描述可接受遺失多少時間的資料，RTO 描述可接受恢復多久。來源每日備份但 outbox 沒保留，不一定能恢復到剛才；索引可重建但要花十小時，也可能超過產品容許時間。先定目標，再決定快照頻率、日誌保留與預先準備資源。

## 本課的可執行還原

完整交付入口使用 SQLite backup API 保存來源，關閉 Local 後保留其資料，另以來源備份建立全新空 Qdrant Local，重新匯入 active 文件，查詢並比對恢復前後 ID。這是離線穩定快照重建，不是複製活躍資料目錄，也不宣稱驗證 server snapshot。

## 不能照搬舊 Checkpoint

備份中的 checkpoint 可能顯示舊索引已處理到 seq=10；新 collection 卻一筆也沒有。若只 replay seq>10，就會得到空索引。新 generation 必須從來源快照完整建置，再依自己的快照水位追事件。checkpoint 應與 consumer/generation 及資料狀態綁定。

## 線上重建需更強協定

離線實驗暫停 producers，因而來源快照穩定。線上要取得一致快照與水位，保留之後的變更，處理 encode 期間更新/刪除，追到可切換門檻後驗收。若沒有 snapshot+CDC 協定，不能把遍歷一次來源後設定最新水位稱為無漏資料重建。

## 還原報告的內容

記錄來源版本、備份位置/檢查碼、recipe、active ID 集合、每租戶計數、代表性查詢、失效文件不復活、耗時與未驗證項目。備份檔存在只證明有檔案；真正可恢復要靠隔離環境還原與語意驗收。保管憑證與備份存取另依你的服務環境配置。

## 練習與解答

**請先嘗試：** 備份還原後所有 count 相同，還需要查詢驗收嗎？

<details><summary>展開解答與判斷依據</summary>

需要，ID、內容、版本或詞表可能對錯；還要測租戶 Filter、刪除、recipe 與代表性排名。計數是必要觀察之一，不能單獨證明搜尋語意與資料資格恢復。

</details>

## 官方文件與延伸閱讀

- [APSW 官方導覽](https://rogerbinns.github.io/apsw/example.html)
- [Qdrant Snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [PostgreSQL 18 官方文件](https://www.postgresql.org/docs/18/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
