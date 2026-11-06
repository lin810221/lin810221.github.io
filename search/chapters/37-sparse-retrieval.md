# Sparse Retrieval：BM25、詞頻與學習式稀疏表示

辨識 sparse vector 的不同來源，不把所有稀疏查詢都叫 BM25。

## 稀疏描述的是儲存形狀

一個極大維度向量只保存少數非零項，就稱 sparse；其權重可以是 TF、TF-IDF、BM25 變形或模型學得的值。形狀相同不代表分數公式相同。本課 Qdrant 範例只用固定詞表與 TF，以便直接觀察 indices/values；它不是 production BM25，也沒有訓練 SPLADE 類模型。

## 語彙維度與詞彙版本

詞項 ID 必須穩定，query 和 document encoder 的規則也要一致。若用 hash trick，需要接受碰撞並固定 hash seed；若用詞表，要保存 vocab 版本、未知詞行為與停止詞規則。IDF 依文件集合變動時，重新計算與更新範圍也需要明確策略。

## 學習式 Sparse 的額外成本

模型可能替原文未出現的詞分配權重，以增加語意召回；這需要推論、模型下載、版本與評估。稀疏程度影響倒排 posting 數與查詢成本，並非只看 embedding 維度就能估算容量。以模型標籤聲稱「自動理解」不能代替真實多語資料上的品質測量。

## 與 Dense 的互補

代碼、罕見專有名詞與精確詞可由 lexical/sparse 保留，較自由表達可由 dense 補召回。兩路仍會有共同盲點，例如來源根本沒有答案、錯誤 metadata 或不同版本表示。先檢查來源與資格，再評估各路對 Recall、排序與延遲的邊際貢獻。

## 實驗設計

建立 lexical-only、dense-only 與 hybrid 三組，以同一 qrels 比較；固定每路候選預算，另做等成本比較。記錄未知詞、語言、詞長與代碼切片。只比較「hybrid 每路100」與「single10」不公平，因為改善可能只是用了更多候選與計算。

## 練習與解答

**請先嘗試：** 看見 sparse.indices 與 values，就能知道使用 BM25 嗎？

<details><summary>展開解答與判斷依據</summary>

不能。要追查權重如何產生、是否使用文件頻率與長度正規化、詞表如何對齊。本課明示 TF sparse 只是查詢機制教具，BM25 另用手算與 FTS 路線驗證。

</details>

## 官方文件與延伸閱讀

- [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/)
- [Elasticsearch Similarity](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
