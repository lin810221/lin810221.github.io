# Attention：Query、Key、Value與縮放內積

用一個小矩陣手算權重，理解內容相依的資訊聚合。

## 從固定摘要到選擇性讀取

Query表示目前想找的條件，Key提供可比對特徵，Value是要被聚合的內容。它們可以由相同或不同資料透過可學投影取得。Attention是加權讀取機制，不等於神經模型的完整推理或人類注意力。

$$
S=\frac{QK^T}{\sqrt{d_k}},\qquad A=\mathrm{softmax}_{keys}(S),\qquad O=AV
$$

Q[L,d_k]、K[S,d_k]、V[S,d_v]，權重[L,S]，輸出[L,d_v]。每個query row沿keys正規化，不跨batch或任意feature軸。

## 為什麼除sqrt(d_k)

在部分獨立尺度近似下，內積隨維度的變異增加，可能讓softmax過於尖銳、梯度不利。縮放是一種控制logits尺度的設計，仍受表示分布與norm影響；不能把它當所有attention都必用相同公式的定理。

## 真正數值對照

第30例生成double Q/K/V、算softmax與AV，再比F.scaled_dot_product_attention(dropout_p=0)。每row sum為1，輸出誤差接近精度。CPU驗證只保證這個數學契約，沒有報FlashAttention或GPU速度。

## 權重如何解讀

大權重表示此層此head在當下混合較多某value，不自動是因果重要性。還有投影、其他head、FFN與residual路徑。若要解釋整個預測，不能只畫一張attention熱圖就說找到了唯一理由。

## 練習與解答

QK logits全相同，權重均勻，輸出是values平均。若某key被mask則需先排除再正規化，不是在softmax後隨意設零而忘記重新歸一。空可見集合需明確政策，下一章用future invariance測causal實作。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/30_attention.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:30_attention.py -->

## 原始論文與官方來源

- [Attention原始Transformer研究](https://arxiv.org/abs/1706.03762)
- [Scaled dot-product API](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [早期encoder-decoder attention](https://arxiv.org/abs/1409.0473)
