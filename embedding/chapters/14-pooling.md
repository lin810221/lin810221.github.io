## Pooling 是一個有影響的選擇

Transformer 輸出每個位置的 hidden state，但許多任務需要每段只有一個向量。Pooling 把序列壓成固定形狀，可以取 CLS、平均、最大值、末個有效位置，或依模型使用特定模組。

方法不能脫離訓練 recipe。某個模型若以特定 pooling 學成，任意換成另一種可能破壞表示。載入完整 Sentence Transformer 通常會保留其模組設計，使用 backbone 則要自己確認。[SentenceTransformer 文件](https://sbert.net/docs/package_reference/sentence_transformer/model.html)

## Mask-aware 平均

令每個位置向量為 $h_i$，mask 為 $m_i\in\{0,1\}$，有效位置平均是：

$$
e=\frac{\sum_i m_i h_i}{\sum_i m_i}
$$

全為零的 mask 沒有有效內容，分母為零。應回報無效輸入，不要除以隨便加上的小數後假裝得到可靠表示。若實作使用 epsilon 防數值錯誤，也需另外保留無有效 token 狀態。

## 用數字看 PAD 的影響

有效位置為 `(1,0)`、`(0,1)`，PAD hidden state 是 `(2,-1)`。正確 mask 得 `(0.5,0.5)`；把 PAD 算入平均得 `(1,0)`，方向都變了。這些數字是手工示範，不是從某個 Transformer 抽出的結果。

<!-- example:06_pooling.py -->

如果 PAD 恰好是零向量，不 mask 只會改平均尺度，L2 正規化後方向相同；但真實 hidden states 不宜假設為零。清楚分辨這兩種情況，比一律說 padding 一定改 cosine 更精確。

## 特殊 token 與 prompt token

CLS、SEP、BOS、EOS 和任務前綴是否參與 pooling，應依模型定義。某些框架也能排除 prompt tokens。不能只根據 token 名稱自行刪除，否則和原本訓練的分布不同。

## 正規化的先後

平均 token 後再正規化，與先把每個 token 正規化再平均，一般不相同。前者保留不同 hidden state 長度對平均的影響，後者改變權重。部署時要保存這個順序，而非只寫一句「有做 normalization」。

## 練習與參考答案

**題目：**兩句內容相同，但 batch padding 長度不同，句向量應受到什麼影響？

**參考答案：**在正確 mask、推論模式及相同有效輸入下，理想上表示應一致到可接受數值誤差。若差異很大，檢查 mask、dropout、截斷、prompt 與 batch 處理；不先把變動歸因為語意。
