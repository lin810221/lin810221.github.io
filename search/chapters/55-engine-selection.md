# 引擎選型：從需求矩陣決定，不從排行榜決定

比較嵌入式全文、向量函式庫、向量服務與關聯整合的責任分配。

## 能力矩陣

| 選項 | 適合起點 | 需要你補上的責任 |
|---|---|---|
| SQLite FTS5 | 本機工具、小型全文資料 | 中文分析、服務化、共享與維運策略 |
| Faiss CPU | ANN 演算法實驗、程序內向量索引 | metadata/ACL、交易、同步、服務與備份 |
| Qdrant Server | 以向量與 Filter 為核心的查詢服務 | 來源契約、同步、部署與品質評估 |
| Elasticsearch | 複雜全文分析、欄位查詢與聚合 | mapping、分片、更新與服務維護 |
| PostgreSQL＋pgvector | 關聯資料、交易與搜尋靠近來源 | SQL 計畫、索引維護、共享資源管理 |

這是責任分工，不是絕對功能邊界；各產品仍可能支援其他模式，必須依版本、部署與方案查核。OpenSearch 等替代產品應另建能力驗收，不直接視為同一服務。

## 先寫工作負載

列出 N、d、本文大小、更新/刪除率、QPS、p95、tenant 分布、Filter selectivity、資料時效、備份RPO/RTO與維運人力。是否需要複雜聚合、精確 join、多語分析與近即時更新，通常比單一向量數更有決策價值。

## 用同一評估集比較

先確認每個候選方案都通過硬條件與資料資格，再比較品質、成本與延遲。微基準需同硬體、資料、metric、Filter、候選深度與執行緒；服務端到端測試還要包含網路與來源取回。不把 Local 與遠端叢集或不同壓縮品質的數字硬放同一速度排行。

## 保持退出路線

來源資料與 recipe 可重建，ID 與 ingestion 契約獨立，query/rerank 介面有界，會讓日後換引擎較容易。過早抽象所有 DSL 會隱藏差異，但把業務權限寫死在某個非標準查詢中也增加遷移成本。先抽象共同責任，保留可觀察的引擎特有行為。

## 練習與解答

**請先嘗試：** 本機十萬筆資料，是否一定要啟動分散式向量資料庫？

<details><summary>展開解答與判斷依據</summary>

不一定。依維度、查詢率、Filter、更新與可用性需求，Flat、FTS 或單庫整合可能已足夠。先用簡單方案建立正確基線並量測，再因具體能力或規模瓶頸增加系統。

</details>

## 官方文件與延伸閱讀

- [SQLite FTS5 官方文件](https://www.sqlite.org/fts5.html)
- [Faiss Indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)
- [pgvector 官方使用文件](https://github.com/pgvector/pgvector)
- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
