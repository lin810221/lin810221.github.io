# Elasticsearch Mapping：text、keyword 與向量欄位

把文件契約轉成可檢查的 Mapping，避免動態型別猜測累積成遷移問題。

## Index 是查詢結構也是管理單位

Elasticsearch index 包含 mapping、設定與 shards。欄位用 text 才能經過分析，用 keyword 保留精確值供 Filter、排序與聚合。數字、日期與 bool 應使用明確型別。本課設定 dynamic=strict，未宣告欄位會失敗，讓 schema 變更在匯入時被看見，而不是默默生成不一致資料。

## 定義必要欄位

title/body 使用 text；tenant、doc_id、recipe、category 使用 keyword；revision 與 point_id 為 long；active 為 boolean。dense_vector 固定八維、cosine 相似度。這八維只屬於教學 fixture；換模型後應依實際維度建立新欄位或新索引，不能截斷向量硬塞進原 mapping。

## 欄位變更多半不是原地改型別

把既有 keyword 改成 text 或改維度，通常需要新索引、回填與切換。新增 multi-field 後，舊文件也需要重新處理才會有新索引值。建立 index_v2、記錄來源水位、跑品質與資格驗收，再切換讀取 alias，保留可用的回復路線。

## 範例驗證了什麼

入口透過真正 Elasticsearch Python SDK 的 indices.create 產生序列化請求，記錄節點回傳固定成功訊息，沒有啟動伺服器。因此能驗證參數結構與 JSON，不能證明 mapping 在實際服務一定建立成功、授權已設定或 ANN 資料已建好。服務路線需再將同一 mapping 送入受控測試叢集驗收。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 06_elastic_mapping.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:06_elastic_mapping.py -->

## 練習與解答

**請先嘗試：** dynamic=strict 是否能代替文件的業務驗證？

<details><summary>展開解答與判斷依據</summary>

不能。它限制未宣告欄位與引擎型別，仍需檢查租戶來源、ID 穩定性、revision 順序與 recipe。引擎接受文件不等於文件符合跨系統資料契約。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch Mapping](https://www.elastic.co/docs/manage-data/data-store/mapping)
- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
