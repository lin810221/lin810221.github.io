# 第一次全文搜尋：建立、寫入與查詢

用真正的 SQLite FTS5 建立商品索引，觀察一個查詢如何返回資料。

## 從一小份資料開始

範例資料是虛構商品與文件，包含 alpha、beta 兩個租戶。先執行入口，查詢 `USB hub`；預期只能看到 alpha 的有效商品。沒有命中時先檢查文件內容與 token，不要立刻更換向量模型。

## 看懂三張表

`docs` 是權威來源，`docs_fts` 是 external-content FTS5 虛擬表，`outbox` 保存待同步的變更。觸發器讓來源新增、修改、刪除與 FTS 更新發生在同一資料庫交易。外部內容模式不會替你自動同步；少了觸發器或正確的 rebuild，MATCH 與來源內容可能不一致。

## 查詢的方向

`MATCH ?` 使用綁定參數；我們再將每個 token 轉成字面詞，避免把使用者輸入當成 FTS 查詢語法。SQL 的 tenant、active 與 LIMIT 也透過綁定參數傳入。SQLite `bm25()` 的較好結果數值較小，排序用 ASC；展示時取負數只是方便閱讀，不能與其他引擎的分數互比。

## 第一個驗收

比較 `USB hub`、`AX-100`、不存在的詞與 beta 身分下的同查詢。結果應能回到來源的穩定 ID。再讀 `source_store.py` 的三個 trigger，追蹤更新前的詞如何先刪除、再新增。這裡的成功條件是查詢、來源與 Filter 一致，並非每個詞都必須回傳 k 筆。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 01_first_fts.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:01_first_fts.py -->

## 練習與解答

**請先嘗試：** 將文件中的 hub 改成 docking，再查原詞與新詞，應檢查什麼？

<details><summary>展開解答與判斷依據</summary>

來源 revision 要增加；舊 hub 不應再命中被修改的那筆，新 docking 應命中。檢查是同一 doc_id 與 point_id，而非新增重複文件；再確認 outbox 多出一筆新版本事件。

</details>

## 官方文件與延伸閱讀

- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)
- [APSW 官方導覽](https://rogerbinns.github.io/apsw/example.html)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
