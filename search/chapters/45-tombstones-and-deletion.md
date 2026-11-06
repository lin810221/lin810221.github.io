# Tombstone 與刪除傳播：查不到不等於清除完成

保留刪除版本以防舊事件復活，並區分可見性、索引回收與資料保留。

## 為什麼保留 Tombstone

若刪掉所有來源紀錄，延遲的 revision=1 upsert 可能被當新文件。active=False、revision=3 的 tombstone 表示這個 logical ID 已在更高版本失效；worker 與重建流程都以它為準。本例保留該狀態，但正式系統應依事件保留與資料政策決定何時可安全清理 tombstones。

## 刪除的不同階段

```text
source inactive → 查詢 hydration 立即隱藏
outbox → 向量庫刪除 ID → 候選不再占位
引擎 merge/回收 → 物理空間回收
備份/日誌保留 → 依政策到期或受控清除
```

搜尋結果不再出現，只驗證了查詢可見性；不代表舊 segment、WAL、快照、cache、日誌或外部複本已被清除。若有明確資料清除要求，需盤點所有衍生資料並另外驗收，不用單次 delete 回應作完整證明。

## 索引落後時的行為

來源先標 inactive，向量仍可能返回舊 point。專題回來源檢查 active 與 revision，拒絕展示；這保護最新資格，但可能讓結果不足 k。需要監控 discarded_stale、同步 lag 與查詢品質；來源檢查是過渡保護，不是可以永久不清索引的理由。

## 清理 Tombstone 的前提

確認沒有可能重播的舊事件、所有 generation/worker 已超過水位、備份恢復不會再灌入舊狀態，才討論清理。若來源 ID 允許重用，要定義新 incarnation 或更高版本，不讓新文件與已刪舊文件混淆。資料生命週期需超過單一引擎 API 的範圍。

## 驗收案例

新增v1→更新v2→刪除v3→重送v1/v2→重建新索引，文件都不應復活。接著檢查每租戶 ID、來源內容與 index count。部分服務的物理回收是非同步的，報告應分開列出功能刪除已確認、實體回收未驗證等狀態。

## 練習與解答

**請先嘗試：** 為了清理資料表，立刻刪掉 tombstone 與 outbox，會有什麼問題？

<details><summary>展開解答與判斷依據</summary>

失去拒絕舊事件與重建判斷的依據，也可能讓未完成 worker 跳過變更。應先定義可證明的水位、保留期與恢復協定，再清理。需要永久清除個資時，另以適當不可逆標識保存必要去重狀態。

</details>

## 官方文件與延伸閱讀

- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)
- [PostgreSQL 18 官方文件](https://www.postgresql.org/docs/18/)
- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
