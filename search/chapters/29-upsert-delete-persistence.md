# Upsert、刪除與 Local 持久化：不把成功回應當版本保護

觀察同 ID 覆寫、刪除與重新開啟資料，再補上來源版本與重送語意。

## Upsert 的基本語意

相同 point ID upsert 會更新資料，並不天然知道你的業務 revision 是否較新。本課 raw VectorStore.upsert 沒有分散式 CAS 保證；只允許受控的來源同步 worker 呼叫。若直接把舊事件寫回向量庫，仍可能覆蓋新內容，所以版本判斷不能只寫在教材描述裡。

## 刪除與 Tombstone

向量庫可按 ID 刪除，但來源保留 active=False 與較新的 revision，才能拒絕延遲的舊 upsert。只刪向量卻忘記來源，重建會把文件加回；只改來源卻不清索引，候選仍占用預算。服務 hydration 可先隱藏失效候選，同步 worker 再清除索引。

## Local 保存與重新開啟

`19_qdrant_persistence.py` 使用臨時目錄，寫入後 close，再以同一路徑重新開啟並查詢。不要同時用兩個 Local client 打開同一目錄；它不是多程序伺服器。使用 TemporaryDirectory 的範例在結束後會清理自己的臨時資料，不會修改你的遠端叢集。

## 可靠寫入需要更多條件

wait=True 對操作完成有特定語意，但不代表跨 source/vector 交易、全副本一致或可災難復原。正式 server 的 ordering、consistency、replication 設定需按版本驗收。完整恢復也要考慮來源、worker checkpoint、recipe 與是否存在重建中的 generation。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 18_qdrant_updates.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:18_qdrant_updates.py -->

## 練習與解答

**請先嘗試：** 已成功刪除 point，舊 outbox 事件晚到時如何避免復活？

<details><summary>展開解答與判斷依據</summary>

先讀權威來源的最新版本與 tombstone。只有與現行版本一致的事件才更新；最新狀態是 inactive 就刪除。分散多寫者還需有序分區或 CAS 等更強機制，本課單一有序 worker 不宣稱涵蓋所有並行情況。

</details>

## 官方文件與延伸閱讀

- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)
- [Qdrant Filtering](https://qdrant.tech/documentation/search/filtering/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
