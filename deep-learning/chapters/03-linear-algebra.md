# 必要線性代數：shape、內積與批次矩陣

把每個符號對到實際維度，讓之後的forward與backward有清楚契約。

## 樣本與特徵軸

X[N,d]每列是一筆，W[d,h]將d個輸入映射h個輸出，b[h]沿batch廣播。Z=XW+b得到[N,h]。PyTorch nn.Linear的weight儲存[h,d]，forward用其轉置；本課手算採W[d,h]，對照實作時明確分別，不混用兩種記號。

$$
Z_{i,j}=\sum_{k=1}^{d}X_{i,k}W_{k,j}+b_j
$$

若N=3,d=2,h=4，Z有12個數，W有8個參數，b有4個。batch大小改變不應改參數數量，因為相同規則套到每筆樣本。

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

X[5,4]→W1[4,6]→ReLU→W2[6,2]得到[5,2]；參數含bias為4×6+6+6×2+2=44。若X乘上一個不相容[5,6]矩陣，不能靠reshape掩蓋。解答：重新確認樣本軸與feature軸，保持相同數量元素不等於保持資料意義。

## 原始論文與官方來源

- [Linear與張量](https://docs.pytorch.org/docs/2.15/nn.html)
- [Broadcasting](https://docs.pytorch.org/docs/2.15/notes/broadcasting.html)
- [數學基礎](https://www.deeplearningbook.org/contents/linear_algebra.html)
