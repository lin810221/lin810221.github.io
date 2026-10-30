# Dropout：隨機遮蔽、期望與推論模式

用inverted scaling手算平均保持，了解它對學習訊號的擾動。

## 訓練期間隨機關閉部分值

Dropout以某機率將activation設零，降低模型對固定共適應模式的依賴。PyTorch的p是丟棄機率，不是保留機率。inverted dropout在train將保留下來的值除1-p，eval直接保持原值。

$$
\tilde h=\frac{m\odot h}{1-p},\quad m_j\sim\mathrm{Bernoulli}(1-p),\qquad
\mathbb E[\tilde h\mid h]=h
$$

期望保持不表示每筆／每個batch完全一樣，也不表示經過所有後續非線性後整個網路輸出期望恰等eval結果。

## 可執行觀察

p=.5、輸入10000個1，train輸出只會0或2，平均約1；eval全為1。第17例驗證這三項。固定seed讓實驗可重現，但不同隨機來源／呼叫次序也會改mask，不用某一批數字恰相等作通用保證。

## 與其他模組的互動

Dropout位置、機率與BatchNorm等一起影響學習。不是每個架構都需要很多Dropout，過大會讓小資料小模型欠擬合；對feature map可考慮channel型策略，語意與逐元素不同。先定方案再做validation比較。

## 推論與不確定性

標準推論用eval關掉隨機性；若研究MC Dropout，需要有意設計重複取樣、其他模組模式與校準，不能直接把幾次variance當完整epistemic uncertainty保證。模型仍可能在OOD自信錯誤。

## 練習與解答

只加no_grad後預測仍隨機，原因是Dropout還在train。解答：同時model.eval；反之eval並不自動關Autograd。若把p=.5理解為輸出乘.5，就漏掉隨機遮蔽與inverted scaling，不是同一演算法。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/17_dropout.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:17_dropout.py -->

## 原始論文與官方來源

- [Dropout原始論文](https://jmlr.org/papers/v15/srivastava14a.html)
- [Torch Dropout](https://docs.pytorch.org/docs/2.15/nn.html#dropout-layers)
