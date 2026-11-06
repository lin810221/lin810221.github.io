# 去重、多樣性與 Reranking：前幾名不能只有同一份文件

區分候選召回與二階段排序，設計可替換且有預算的重排介面。

## 文件與 Chunk 的排名不同

一份長文件切成很多相近 chunks，可能占滿前十。搜尋商品時，十個同款不同片段通常不如多個有效商品。先定義顯示單位是 document、product、section 或 chunk，再決定 group key、每組上限與聚合分數。去重不能只看文字相同，還要保留來源版本與租戶。

## 二階段排序

第一階段以低成本召回候選，第二階段針對有限候選計算更昂貴特徵，例如 cross-encoder、規則或 learning-to-rank。重排只重排已召回資料，無法找回候選集合外的真值。本課專題提供清楚的候選/來源契約，沒有預設下載 reranker 或呼叫模型服務。

```text
rerank(query, scoped_current_documents, max_candidates, deadline)
  → ordered IDs + feature versions + mode
```

## 多樣性也有取捨

MMR 類方法在相關性與重複性之間平衡，可增加主題或來源多樣性，但過度多樣會把真正最相關的結果往後放。不要在沒有需要時，為了視覺「每筆不同」犧牲精確型號查詢。以查詢意圖與產品呈現單位決定策略。

## 預算與回退

限制重排候選數、本文長度與時間；超時時使用明確的原始融合順序，記錄 rerank-skipped。模型輸出任意 ID 時只能接受候選白名單內的 ID，不能讓生成文字變成未授權文件取回。無論排序方法如何，資格檢查與來源版本都不由模型評分覆寫。

## 評估

除 nDCG/MRR，記錄 unique_document_count、重複比例、每類覆蓋與延遲。準備「多片段同文件」、「同產品不同版本」、「精確代碼」的對照，確認分組不把不同租戶或新舊版本錯誤合併。若使用人工相關性標註，展示單位應與 qrels 一致。

## 練習與解答

**請先嘗試：** Reranker 覺得另一個未列入候選的 doc_id 很相關，可以直接抓嗎？

<details><summary>展開解答與判斷依據</summary>

不能。排序介面應只對已通過資格的候選操作；若要額外召回，必須走同樣的受控查詢與來源驗證流程。模型不能擴張租戶、索引或可查範圍。

</details>

## 官方文件與延伸閱讀

- [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/)
- [Elasticsearch RRF Retriever](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/rrf-retriever)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
