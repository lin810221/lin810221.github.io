# Revision 與冪等 Upsert：相同重送，過期拒絕

將版本規則寫進來源模組，讓舊事件無法覆蓋新文件。

## 三個分支

新 revision 大於舊版：接受更新；相等且內容相同：不產生新效果；相等但內容不同或小於舊版：拒絕。穩定 point_id 不能在更新中改變，否則向量庫可能留下舊 ID。這些是業務資料契約，應在權威寫入層驗證，而不是寄望資料庫 upsert 自動知道時間先後。

## Outbox 必須一起提交

SourceStore.upsert 在同一 SQLite 交易寫來源、由 trigger 更新 FTS、再寫唯一事件。事件 ID 由 tenant/doc_id/revision 的無歧義編碼組成。測試會注入 outbox 寫入失敗，驗證來源與全文索引一同回滾，避免資料已改但同步事件不存在。

## 單寫者與多寫者

本課版本產生與更新使用受控單一流程。若有多寫者，讀舊版、判斷版本、寫入必須在相同鎖定或條件更新邊界內，不能將交易外的 get 當 CAS。可使用 revision WHERE、SELECT FOR UPDATE 或資料庫產生版本；失敗時回明確 conflict，不默默覆蓋。

## 重送不是全域 Exactly-once

來源拒絕重複版本、索引穩定 ID 與單一有序 worker，共同讓本例可安全重送。它不保證跨任意多節點與網路分區 exactly-once。報告應寫出實際故障模型、順序假設與已驗證案例，避免把局部冪等誇成分散式原子交易。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 26_versioned_ingest.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:26_versioned_ingest.py -->

## 練習與解答

**請先嘗試：** 同版本內容不同，但後到的時間比較晚，是否應接受？

<details><summary>展開解答與判斷依據</summary>

不應把到達時間當來源真相。相同版本應描述相同狀態，衝突需拒絕並回到來源釐清；正確更新應取得更高 revision。時鐘、重送與網路延遲都會讓到達順序不可靠。

</details>

## 官方文件與延伸閱讀

- [PostgreSQL 18 官方文件](https://www.postgresql.org/docs/18/)
- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
