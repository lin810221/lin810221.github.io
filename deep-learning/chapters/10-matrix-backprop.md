# 矩陣反向傳播：一個batch如何一起求梯度

由softmax CE的輸出梯度，推回兩層MLP並核對shape。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![Forward與Backward的對應；反向傳播沿既有計算圖套鏈式法則；梯度檢查用有限差分提供數值參考。](assets/figures/review-02-networks.svg)

> **圖解｜Forward與Backward的對應**：反向傳播沿既有計算圖套鏈式法則；梯度檢查用有限差分提供數值參考。

**本單元讀圖任務**：讀完「矩陣反向傳播：一個batch如何一起求梯度」後，在圖上指出「Loss」的位置或對應關係；用本單元的一個例子說明它與「鏈式梯度」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 固定 row-vector 記號

每列是一筆樣本。輸入與兩層權重的形狀如下：

$$
X\in\mathbb{R}^{N\times d},\quad
W_1\in\mathbb{R}^{d\times h},\quad
W_2\in\mathbb{R}^{h\times C}.
$$

前向計算沿著同一套記號進行：

$$
A_1=XW_1+b_1,\quad H=\operatorname{ReLU}(A_1),\quad Z=HW_2+b_2.
$$

交叉熵對 $N$ 筆樣本取平均。PyTorch `Linear` 儲存轉置排列的權重；核對梯度時，要先對齊參數與手算矩陣的形狀。

## 輸出層的簡潔梯度

CE把softmax與log合併後，對logits梯度為 $\frac{P-Y}{N}$ ，其中Y為one-hot。這只對此處未加權、每筆一個類別的mean契約成立；若有class weights或有效token mask，分母要重新推導。

$$
D_Z=\frac{P-Y}{N},\quad
D_{W_2}=H^TD_Z,\quad D_{b_2}=\sum_iD_{Z,i}
$$

## 經過ReLU再回第一層

先傳 $D_H=D_ZW_2^\top$，再逐元素乘上 $A_1>0$ 的指示函數。weights梯度是輸入轉置乘local delta，bias是batch加總。這些式子的shape本身提供檢查，若需要隨意reshape才能相乘，多半記號已錯位。

$$
D_{A_1}=(D_ZW_2^T)\odot1[A_1>0],\quad
D_{W_1}=X^TD_{A_1},\quad D_{b_1}=\sum_iD_{A_1,i}
$$

## 實驗與驗收

第4例使用N3、d2、h3、C2與double，計算全部manual矩陣再與Autograd.grad比。不是建立龐大完整Jacobian，而是直接用相同的向量積結構。ReLU在0處不可微，本例選非邊界值，PyTorch對0的約定會在activation章說明。

## 練習與解答

若loss使用sum，D_Z不除N；其他推導相同。若W2有共享分支，對它的貢獻需相加。解答：反向傳播的核心是局部Jacobian乘上游訊號與共享節點累加，不是每種新架構都重寫完整微積分。新層仍需知道局部運算與數值穩定性。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/04_matrix_backprop.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:04_matrix_backprop.py -->

## 原始論文與官方來源

- [Autograd](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [CrossEntropyLoss](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
