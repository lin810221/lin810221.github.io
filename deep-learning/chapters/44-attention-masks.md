# Self、Cross與Causal Mask：防止未來資訊滲漏

用擾動未來value的實驗，驗證能看見的位置是否符合任務。

## 來源與可見範圍

self-attention的Q/K/V來自同一序列，cross-attention的Q來自一段、K/V來自另一來源。能否看未來由任務決定：整句分類可全可見，下一token預測通常限制key位置j<=query位置i。名稱本身不會替你加mask。

## bool語意最容易相反

PyTorch F.scaled_dot_product_attention的bool True表示允許；nn.MultiheadAttention的bool attn_mask True表示禁止。兩者API契約相反，本課明確分開。padding mask、causal mask與float additive mask也有各自shape／組合規則，不能看到bool就直接搬用。

## 正規化與全mask

手工實作通常將不可見logit設-inf後softmax，正常非空集合被遮項為0；若整row全-inf，普通softmax會有NaN，需處理無有效key政策。現成算子的邊界實作也需看版本，不把任意mask當一定有定義。

## 直接測未來不變性

第31例用lower-triangular allowed mask，將最後位置V加100，前3個輸出應完全不變；另比is_causal=True結果。這個測試比只看mask矩陣長得像三角更有力。若倒置True／False，可能仍產生有限值卻偷看未來。

## dropout與eval

functional SDPA的dropout_p由你明確提供，不能以為外部model.eval會替任意functional呼叫自動改成0。驗證固定0；模組版本則依其契約管理。mask、dropout、shape與快取在真實語言模型互相影響，完整生成／KV cache由Transformer課深入。

## 練習與解答

L4的query第1個只能看key0；query最後可看0..3。解答：把每個query能看的索引寫出，再做擾動測試。若Q/K也改未來，前面的合法可見值依舊不該改；多層網路還需norm／其他運算不跨未來位置，第46章測完整小block。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/31_causal_mask.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:31_causal_mask.py -->

## 原始論文與官方來源

- [SDPA mask與dropout](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [MHA mask語意](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)
