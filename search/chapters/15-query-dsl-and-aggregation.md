# Query DSL、Filter 與 Aggregation：查詢也要有邊界

建立受控的 multi_match 與精確 Filter，理解查詢、聚合與資料資格的作用範圍。

## 把相關性與資格寫在正確位置

bool.must 可放 multi_match，title^2 提升標題；bool.filter 放 tenant、active 與 recipe 的精確條件。模型或使用者不能直接提供整份 DSL，否則可繞過欄位限制與資源預算。本課服務只接受 query、k，由可信主體產生租戶，再組出固定形狀的請求。

## Aggregation 的作用域

聚合可建立分類計數、日期直方圖與數值統計，但要確認它在什麼範圍計算。若只把租戶限制放在 post_filter，聚合可能涵蓋更大的集合而洩漏計數。身分與必要權限必須限制所有資料讀取，包括聚合、suggest、高亮與第二段取文件操作。

## Timeout、size 與候選預算

限制 size、查詢長度、欄位清單與可用操作。向量 k 與 num_candidates 不同，且過濾需放在向量召回的適當位置；僅在最終 hits 再丟棄，可能造成不足 k。逾時回應還需檢查 timed_out 與 shard failures，不從 HTTP 200 推論結果完整。

## 離線與 live

預設入口用真實 SDK 記錄請求；`--live` 只對你指定的既有索引發出搜尋。透過環境變數提供 URL、索引、API key 與 CA，不將憑證寫進教材。官方 TLS 與憑證驗證應保持啟用；不要以 verify_certs=false 當通用排錯方式。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 07_elastic_query.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:07_elastic_query.py -->

## 練習與解答

**請先嘗試：** 租戶 Filter 放在 post_filter，頁面分類計數看起來正常，為何仍有風險？

<details><summary>展開解答與判斷依據</summary>

post_filter 與 aggregations 的作用時機不同，分類計數可能包含未授權資料。應讓必要租戶與 ACL 條件限制所有讀取路徑，並以兩租戶同分類資料驗證計數與 hits 都隔離。

</details>

## 官方文件與延伸閱讀

- [Query 與 Filter Context](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-filter-context)
- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
