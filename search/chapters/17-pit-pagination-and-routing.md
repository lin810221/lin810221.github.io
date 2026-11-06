# PIT、search_after 與 Routing：穩定走過大量結果

用一致的排序與搜尋快照設計分頁，避免深層 OFFSET 與跨頁更新造成混亂。

## 為什麼 from + size 有代價

深層頁面要求各 shard 保留更多排序候選，協調節點再合併；越後面的頁面可能越昂貴。更新發生在翻頁期間，同一文件也可能移動名次。分頁不只是 UI 的頁碼，需要定義資料快照、排序鍵與游標有效期限。

## PIT 搭配 search_after

PIT 固定查詢時所看的索引狀態，search_after 使用上一頁最後一筆回傳的 sort values，而不是自行猜 score。排序需有可靠的 tie breaker；PIT 有其 _shard_doc 行為，實際 sort values 的結構以服務回應為準。後續請求沿用相同 query 與 sort，並使用最新回傳的 PIT ID，完成或逾時要關閉。

## 游標也是服務契約

對外 cursor 可包含 PIT ID、sort values、query hash 與主體範圍，再作簽署與期限檢查。不能讓換 tenant 的使用者拿同一 cursor 繼續翻頁，也不能接受任意修改排序值來查未授權範圍。頁面大小、總筆數上限與 PIT 存活時間應有限制，避免長時間保留資源。

## Routing 不等於授權

Routing 可讓已知租戶或分組的查詢只打相關 shards，但寫入與查詢需使用同一規則。它是定位與效能機制，不取代 tenant/ACL Filter；租戶大小不均也可能造成 hot shard。範例用固定 PIT 回應與明示假資料 sort tuple 觀察序列化，不宣稱已驗證實際跨 shard 順序。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 09_pagination.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:09_pagination.py -->

## 練習與解答

**請先嘗試：** 分頁第二頁可以直接改 query，但沿用第一頁 search_after 嗎？

<details><summary>展開解答與判斷依據</summary>

不應這樣做。游標描述的是相同查詢、排序與資料快照中的位置；改 query 應重新建立分頁流程。對外 cursor 應綁定查詢與身分，服務驗證不符就拒絕。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch 分頁與 PIT](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/paginate-search-results)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
