# 必要線性代數：shape、內積與批次矩陣

把每個符號對到實際維度，讓之後的forward與backward有清楚契約。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![神經元把輸入轉成可學表示；參數透過loss梯度更新；輸入、目標與輸出shape先對齊。](assets/figures/review-01-foundations.svg)

> **圖解｜神經元把輸入轉成可學表示**：參數透過loss梯度更新；輸入、目標與輸出shape先對齊。

**本單元讀圖任務**：讀完「必要線性代數：shape、內積與批次矩陣」後，在圖上指出「非線性」的位置或對應關係；用本單元的一個例子說明它與「預測」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 樣本與特徵軸

每列代表一筆樣本，採用列向量的排列方式：

$$
X\in\mathbb{R}^{N\times d},\quad
W\in\mathbb{R}^{d\times h},\quad
b\in\mathbb{R}^{h},\qquad Z=XW+b\in\mathbb{R}^{N\times h}.
$$

偏置 $b$ 沿著樣本軸廣播。PyTorch `nn.Linear` 的權重儲存形狀為 $h\times d$，計算時使用轉置；本課手算使用 $d\times h$，對照實作時要分清兩種排列。

$$
Z_{i,j}=\sum_{k=1}^{d}X_{i,k}W_{k,j}+b_j.
$$

若 $N=3,d=2,h=4$，輸出 $Z$ 有 12 個數，權重 $W$ 有 8 個參數，偏置 $b$ 有 4 個。改變 batch 大小不應改變參數數量，因為同一組規則套用到每筆樣本。

## 逐元素與矩陣運算

`*`常表示逐元素，`@`是矩陣乘積；ReLU對每個值作用，softmax則需指定哪個軸正規化。若把分類dim設成batch軸，就讓不同樣本互相競爭。assert shape只能查結構，也要為每個軸寫名字，確定數值含義。

## Jacobian與向量積

向量輸出對向量輸入的導數是Jacobian。反向傳播通常不完整建立大Jacobian，而計算上游梯度與局部Jacobian的乘積。這能以與forward相近的運算結構傳導導數，也是大模型可訓練的關鍵。

$$
J_{j,k}=\frac{\partial f_j}{\partial x_k},\qquad
\nabla_x L=J^T\nabla_f L
$$

## 廣播的危險

回歸pred[N,1]與target[N]相減，可能擴成[N,N]。程式能算不表示逐樣本配對正確。mean、sum與keepdim也會影響之後廣播與梯度縮放。先列每步shape，loss前明確要求一致；類別索引[N]則有不同契約。

## 練習與解答

輸入 $X\in\mathbb{R}^{4\times3}$、權重 $W\in\mathbb{R}^{3\times2}$、偏置 $b\in\mathbb{R}^{2}$ 時，輸出與參數各有多少個數？

**解答：**輸出形狀為 $4\times2$，共 8 個數；權重有 $3\times2=6$ 個參數，偏置有 2 個，共 8 個參數。若只把 batch 改成 10，輸出改成 $10\times2$，參數數量仍為 8。兩者在原例恰好相等，不代表輸出數量與參數數量是一回事。

## 原始論文與官方來源

- [Linear與張量](https://docs.pytorch.org/docs/2.15/nn.html)
- [Broadcasting](https://docs.pytorch.org/docs/2.15/notes/broadcasting.html)
- [數學基礎](https://www.deeplearningbook.org/contents/linear_algebra.html)
