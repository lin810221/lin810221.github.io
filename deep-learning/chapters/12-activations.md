# Activation：Sigmoid、Tanh、ReLU、GELU與梯度

比較函數值、飽和區與導數，理解選擇對表示及最佳化的影響。

## 非線性也改變梯度

Sigmoid輸出0..1、導數最高.25；Tanh輸出-1..1、中心附近導數較大；兩者大絕對值區都可能飽和。ReLU保留正值，負區輸出0且局部導數0。它們沒有哪個在所有任務都最佳，要配合初始化、深度與架構。

$$
\sigma'(x)=\sigma(x)(1-\sigma(x)),\qquad
\tanh'(x)=1-\tanh^2(x)
$$

## ReLU邊界與dead unit

0點不可微，框架採某個subgradient約定；PyTorch在0給0。若某單元長期在負區，這條路可能沒有梯度，稱dead ReLU的常見現象。LeakyReLU保留負斜率是候選解法，但也改函數族與尺度，不保證修復資料或步長問題。

## 平滑選項

GELU為xΦ(x)，SiLU為xσ(x)，負區仍可能有平滑反應。GELU可有近似實作，本課預設F.gelu的確切設定。模型中間activation與最後輸出activation要分清：分類CE接受raw logits，不在最後再加GELU或softmax當固定模板。

## 觀察值與導數

第6例在[-3,-1,0,1,3]比較四種函數與Autograd導數。sigmoid在0為.25、GELU在0為.5、ReLU在0為0，可直接核對。不要只看曲線範圍，還要看多層連乘後梯度如何傳。

## 練習與解答

連續20層sigmoid是否必然梯度等於.25²⁰？答案：不是，還乘weights與不同activation導數；這只是局部導數上界的一部分直覺。第23章會用精確標量鏈展示乘積，再說明不能直接代替所有矩陣網路定律。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/06_activations.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:06_activations.py -->

## 原始論文與官方來源

- [Activation functions](https://docs.pytorch.org/docs/2.15/nn.html#non-linear-activations-weighted-sum-nonlinearity)
- [Functional activation](https://docs.pytorch.org/docs/2.15/nn.functional.html)
