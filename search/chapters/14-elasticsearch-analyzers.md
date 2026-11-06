# Elasticsearch Analyzer：索引分析與查詢分析

用 _analyze 驗證文字處理鏈，讓中文、代碼與自然語言各有清楚契約。

## 分析不是等到查不到才猜

建立索引前先整理實際詞彙：USB、ＡＸ－１００、繁體中文、英文縮寫、混合型號、帶重音字詞。每個測試包含原字串、使用的 analyzer 與預期 tokens。可在服務端呼叫 `_analyze` 觀察 offset、position、token type；不要只看表面命中數來推測斷詞行為。

```http
POST /_analyze
{"analyzer":"standard","text":"AX-100 USB hub"}
```

這段是服務操作配方，需要自行啟動服務，不是本課預設入口會發出的遠端請求。standard analyzer 的實際 token 規則應以指定版本輸出確認。

## Index analyzer 與 search analyzer

索引 analyzer 決定已保存的詞，search analyzer 決定查詢如何解讀。兩者可以有意不同，例如查詢時同義詞擴展；但必須維持可匹配的表示。改動 index analyzer 不會自動改寫舊 postings。保留原索引，建新版本並回填是較容易驗證的策略。

## 中文與多語策略

可評估服務版本支援的中文或 ICU 分析元件，也可在上游作受控斷詞，或採 n-gram。外掛需要確認版本相容、部署方式與授權；不能把一台本機可用等同所有雲服務都能安裝。繁簡對應也不是天然對稱，有些領域詞必須保留原始意義與多欄位查詢。

## 改善品質的對照實驗

固定相同資料與 qrels，以 A/B 索引比較 tokenizer、停用詞與同義詞，保存每次 analyzer 版本。除了 Recall 與 nDCG，也記錄索引 bytes、建置時間、詞典大小及查詢 p95。更多 tokens 可能提高召回，也可能增加誤召回與儲存成本，必須共同評估。

## 練習與解答

**請先嘗試：** 只改 search_analyzer，能否修復索引時已把型號切壞的問題？

<details><summary>展開解答與判斷依據</summary>

只能讓查詢更接近現有 token，不能還原索引未保存的原始結構。若需要精確型號，新增正規化 keyword 欄位並完整回填；本文分析則以新索引版本重建與比較。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch Mapping](https://www.elastic.co/docs/manage-data/data-store/mapping)
- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
