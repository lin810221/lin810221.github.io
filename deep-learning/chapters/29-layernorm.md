# LayerNorm、GroupNorm與RMSNorm：正規化軸的選擇

比較批次相依性、affine參數與保存狀態，避免只背名稱。

## LayerNorm依指定尾部維度

對X[N,T,D]使用LayerNorm(D)，每個樣本每個token沿D算mean與variance。其他batch樣本改變不應影響此筆正規化，因此常見於序列架構；它不像BN需要running mean供eval使用。gamma／beta仍可學。

$$
\mu_{n,t}=\frac1D\sum_d x_{n,t,d},\qquad
\hat x_{n,t,d}=\frac{x_{n,t,d}-\mu_{n,t}}{\sqrt{\sigma_{n,t}^2+\epsilon}}
$$

## GroupNorm與Instance概念

對NCHW，GroupNorm將channel分組並沿組內channel與空間正規化，批次大小不直接參與；組數與channel需相容。InstanceNorm等另有軸與狀態設定。不能因都回傳同shape就視為相同統計操作。

## RMSNorm的差別

RMSNorm按均方根縮放，一般不減mean；它與LayerNorm不是只改名稱。具體affine、epsilon與實作支援看目前API及模型設定。某些架構常用不代表所有任務都需替換既有norm，先維持可比實驗。

## 現成數值檢查

第19例在[2,3,4]上做LayerNorm(4)，列最後一軸mean接近0，單獨處理第一筆與原batch第一筆相同；另列GroupNorm形狀。這直接驗證軸與batch相依性，而非只說它「讓模型穩定」。

## Norm與residual位置

pre-norm先規範化再經子層與加回，post-norm在加總後正規化，影響梯度路徑與訓練行為。第46章TinyBlock用pre-norm並實測causal invariant；完整Transformer各種變體由獨立課深入，不把一個小block等同所有LLM。

## 練習與解答

LayerNorm((T,D))與LayerNorm(D)是否一樣？答案：前者同時跨時間與feature，改變每個token含義且affine形狀不同。對causal模型尤其需小心未來資訊是否透過不當軸混入。先寫norm沿哪些軸，再看輸出與梯度。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/19_layernorm.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:19_layernorm.py -->

## 原始論文與官方來源

- [LayerNorm原始論文](https://arxiv.org/abs/1607.06450)
- [Torch normalization](https://docs.pytorch.org/docs/2.15/nn.html#normalization-layers)
