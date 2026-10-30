# 一個Transformer Block：Attention、FFN、Norm與Residual

實際組合pre-norm causal block，建立通往完整模型課程的橋梁。

## 兩個主要子層

Attention在位置間交換內容；逐位置FFN做非線性特徵轉換；residual保留直接路，norm調整指定feature統計。單一block不是完整語言模型，還缺輸入tokenization、embedding／位置策略、輸出head、訓練目標與生成流程。

$$
U=X+\mathrm{MHA}(\mathrm{LN}(X)),\qquad
Y=U+\mathrm{FFN}(\mathrm{LN}(U))
$$

本課採pre-norm；原論文post-norm與其他變體有不同路徑，不用此式代表所有Transformer。

## 小型實作

TinyBlock維度8、2head、FFN8→16→8加GELU，MHA dropout0、LayerNorm最後維度8。causal mask用MHA的True禁止上三角，need_weights=False。forward保持[N,T,8]，每個FFN獨立作用各位置。

## 整體causal測試

第32例改最後token輸入，前3位置輸出不變。這同時覆蓋norm、residual與FFN的正確軸；若誤用跨整個T的LayerNorm，可能透過其他路徑洩漏。能通過Attention函式測試，不等於所有外層操作都causal。

## 與RNN的差異

RNN以遞迴state串時間，Attention可在已知序列上平行建立內容關係，但一般有T²成本。生成逐步解碼時仍有自回歸與快取工程；不能因訓練可平行就說生成一次完成所有token。完整Transformer／LLM原理課將深入這些機制。

## 練習與解答

這個block輸出[2,4,8]，是否已能回答自然語言？答案：沒有；只是隨機參數的小運算模組。要分類可加pool/head並定資料／loss，要語言模型需詞表head與next-token目標。先明確任務，再判斷是否需要完整架構。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/32_transformer_block.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:32_transformer_block.py -->

## 原始論文與官方來源

- [Transformer研究](https://arxiv.org/abs/1706.03762)
- [MHA與mask](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)
