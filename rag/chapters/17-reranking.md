## 第一階段先找得到，第二階段再看得細

大型索引需要快速縮小範圍，第一階段檢索通常不能讓每份文件都與問題進行完整聯合推論。重排器只處理較小的候選集合，對每組 query/document 評估相關性，再把更適合回答的片段放前面。

bi-encoder 可預先計算文件表示；cross-encoder 同時讀取問題與候選，通常需要每次查詢重新計算，不能像文件向量一樣對任意問題重用分數。這是常見 retrieve-and-rerank 設計的計算分工。[Sentence Transformers 官方教學](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

## 三種重排方式

| 方式 | 優點 | 限制 |
| --- | --- | --- |
| 詞元覆蓋、規則 | 透明、便宜、離線 | 沒有完整語意理解 |
| Cross-encoder | 聯合分析問題與文件 | 多個候選帶來額外推論 |
| LLM 判定或排序 | 可處理複雜規準 | 費用、延遲、偏誤與格式檢查 |

cross-encoder 輸出可能是 logits、相關性分數或經激活後的值，並非永遠是已校準機率。不同模型的分數不能任意互換門檻。若使用 LLM 排序，還要防止候選文字中的指令干擾判定。

## 跑一個透明的基線

<!-- example:08_reranking.py -->

這裡計算查詢詞元在片段中的覆蓋比例，只是可解釋的教學重排器。它能展示「候選和重排結果分開保存」，不能證明神經 reranker 的品質。你可以先比較 BM25 排名與覆蓋排名，檢查哪些問題受益、哪些問題變差。

## 真正 cross-encoder 的接點

選配環境可安裝 Sentence Transformers，按模型文件選定多語或領域模型，再執行類似流程：

```python
# 選配示意：先自行安裝相依套件、下載並固定模型版本。
from sentence_transformers import CrossEncoder
import os
model = CrossEncoder(os.environ["RERANK_MODEL"])
pairs = [(query, chunk.text) for chunk, _ in hits]
scores = model.predict(pairs)
ranked = sorted(zip([c for c, _ in hits], scores), key=lambda row: -float(row[1]))
```

這段不屬於預設離線範例，初次使用會涉及模型下載。記錄輸入截斷長度與模型版本，避免關鍵例外條款恰好被截掉。

## 重排不能救回什麼

沒有進候選的相關文件，重排器看不到。若第一階段只回傳錯誤兩段，換更大的重排模型未必有用。先檢查候選 recall，再看重排後 top-k 的 precision、nDCG 與最終答案支持度。

## 練習與參考答案

**題目：**重排前候選含正確條款，重排後消失，如何除錯？

**參考答案：**保存問題、候選文字、截斷後輸入、每筆分數與前後排名。確認語言相容、模型方向是否搞反、排序是高分還是低分優先，再檢查候選是否包含標題與適用條件。不要只用新 top-1 的外觀判斷。
