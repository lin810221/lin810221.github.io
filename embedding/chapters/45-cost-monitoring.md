## 建置與查詢分開看

匯入要處理大量文件，關心每秒片段、tokens、失敗與重試；query 關心每題延遲、尾端時間與併發。一次把全部文件重算會增加費用，未變文件應按內容與設定跳過。

費用還包含索引、原文儲存、備份與硬體閒置。API 單價會變，記錄實驗當時的價格與計費單位，不把某次估價寫成永遠成立的模型成本。

## 延遲拆解

```text
query latency = auth + preprocessing + tokenization + encoding + search + postprocess
```

若 encoding 只占 10%，換更快 encoder 的總改善有限。先看分段 trace，再選壓縮、batch、cache 或資料庫方案。網路、冷啟動與排隊也可能主導 p95。

## 本機效能

固定硬體、dtype、batch、長度與預熱，再比較 throughput。batch 越大可能增加單題等待；文件長度排序可減 padding，但要還原輸出身分。量化後的速度也依 CPU/GPU 與後端支援，不只依 bit 數。

框架的效率文件可作優化入口，但應在自己的硬體和題集驗證。[Sentence Transformers efficiency](https://sbert.net/docs/sentence_transformer/usage/efficiency.html)

## 需要監控的資料契約

維度不符、NaN、零向量率、範數分布、未知詞率、輸入截斷、batch 成功率與 manifest mismatch，都可能在 API 可用時悄悄傷害品質。為每次匯入與查詢保存 request/job ID 和設定版本。

相似度分布變動也要有上下文：資料來源、query 類型或模型改版都可能導致。不要只設一條平均值警報，沒有可追查樣本。

## 品質回饋

使用者覺得無幫助，可能是檢索、條件、版本或呈現問題。把回饋對回原文和當時模型設定，審核後加入回歸集。不要直接把回饋文字當正式知識或訓練正例。

## 預算與停止

批次重試和多模型路由都設定上限。cache 命中需確認同一空間與授權，不能為了省費用跨 scope 共用結果。先提供可觀察且可靠的基線，再逐步優化。

## 練習與參考答案

**題目：**吞吐提高兩倍，但使用者等更久，可能為什麼？

**參考答案：**大 batch 可能增加排隊等待；吞吐與單題延遲是不同指標。看 p50/p95、batch 集合時間和併發，依服務目標選設定，而非只追最大每秒數。
