# Generation、切換與回復：新索引先驗收再上線

將索引版本與 query recipe 成套切換，以交易內比較避免覆蓋別人的操作。

## 一份可檢查的 Generation

manifest 包含來源快照、水位、schema、analyzer、vector recipe、metric、筆數與驗收報告。新索引可以建好但未核准服務查詢；只有契約、資格、品質與同步水位都通過，才標記 verified。模型或單純 count 相等不能替代這些證據。

## 原子指標與 Query Recipe

本課 IndexRegistry 在 SQLite 交易中比較 expected_current，再同步更新 active generation 和 query recipe。避免新 query encoder 打舊向量，或另一操作者已切換卻被覆蓋。它是應用指標範例，不是 Elasticsearch alias 或 Qdrant distributed alias 的實作。

## 真實服務切換

Elasticsearch 可評估 alias 切換，Qdrant 可評估 collection aliases；各產品的 API、原子範圍與 client caching 行為需確認。多服務配置還要考慮 encoder、filter schema 與快取版本。將 generation 納入快取 key 與 response，才能定位切換中的混用。

## 回復不是改回名字就結束

舊 generation 若已落後來源，回復後可能漏新資料。保留可追趕事件、版本相容的 query encoder 與足夠磁碟空間。先影子比較，再小流量切換，設品質/錯誤/延遲回復門檻；回復也必須維持 tenant、active 與刪除語意。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 28_generation_cutover.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:28_generation_cutover.py -->

## 練習與解答

**請先嘗試：** 新索引品質較好，但 checkpoint 還落後，能否先標 verified？

<details><summary>展開解答與判斷依據</summary>

不能隱藏必要驗收失敗。可依產品契約另外定義允許 lag 的門檻與證據，但本例 required checkpoint 必須通過。切換前應補齊並對帳，避免把相關性提升換成缺資料。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)
- [Qdrant 官方快速入門](https://qdrant.tech/documentation/quickstart/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
