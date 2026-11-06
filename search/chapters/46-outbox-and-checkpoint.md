# Outbox、Checkpoint 與當機重播

真的在索引寫入後、保存水位前注入故障，觀察 at-least-once 如何恢復。

## 正確提交順序

Worker 讀 checkpoint 後的有序事件，回來源取得當前狀態，符合現行 revision 才 upsert 或 delete。索引寫入完成後再保存 checkpoint。若反過來先保存水位，當機後可能永遠跳過尚未成功的寫入；水位不應代表「已讀取」，而應代表契約要求的效果已完成或明確跳過。

## 注入故障

入口故意在向量庫寫入後拋出錯誤，尚未 acknowledge。第二次 replay 再次處理同一事件，穩定 ID 避免重複點。若來源已更新或刪除，舊事件會被最新 revision/tombstone 取代，而不是按事件內舊本文覆蓋現在資料。

## 順序假設

這是單一有序 worker。平行 consumer、跨 partition 或查完來源後又有更新，都需要更強的每 key 順序、租約、CAS 或版本保護。僅在應用端先 get revision 再呼叫外部 upsert，不能解決所有並行競態。教材會保留這個限制，不宣稱具備分散式 exactly-once。

## Checkpoint 與新索引

舊 checkpoint 只證明舊 consumer 曾完成到那裡，不證明全新空 collection 也有資料。災難復原時從來源快照重建新索引，再依水位補事件；若直接沿用舊 checkpoint，可能產生「沒有待辦事件但整個向量庫是空的」的錯誤。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 27_outbox_replay.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:27_outbox_replay.py -->

## 練習與解答

**請先嘗試：** 某事件版本太舊被跳過，能否推進 checkpoint？

<details><summary>展開解答與判斷依據</summary>

在本課單一有序流程中，已確認權威來源有更新狀態、後續事件也在同一序列時可明確跳過並前進；一般分散式系統還需驗證順序與重建協定。跳過原因應可觀察，不能把未知錯誤當過期事件吞掉。

</details>

## 官方文件與延伸閱讀

- [PostgreSQL 18 官方文件](https://www.postgresql.org/docs/18/)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
