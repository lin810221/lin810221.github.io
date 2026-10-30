# 運算與 Broadcasting：從逐元素到矩陣乘法

用具體形狀推算廣播，理解向量化何時正確、何時會意外放大資料。

## 逐元素與線性代數

`a*b` 是逐元素乘法，`a@b` 是矩陣乘法。輸入 `[N,F]` 與權重 `[F,C]` 矩陣乘積為 `[N,C]`，每一項是 F 個特徵的加權和。若兩邊同為 `[N,F]`，逐元素相乘不會幫你聚合 feature；你還需要決定 sum 的軸。

$$
Z_{n,c}=\sum_{f=1}^{F} X_{n,f}W_{f,c}+b_c
$$

## 廣播的檢查方法

從最右邊對齊各軸，缺少的軸視為 1。兩邊相同或其中一邊是 1 才相容。`[3,4] + [4] → [3,4]`；`[3,4] + [3,1] → [3,4]`；`[3,4] + [3]` 則不相容。這是運算規則，不代表語意正確。

```python
import torch
x = torch.arange(12.).reshape(3,4)
column_bias = torch.tensor([1.,2.,3.,4.])
row_mean = x.mean(dim=1, keepdim=True)
print((x + column_bias).shape)
print((x - row_mean).mean(dim=1))
try:
    print(x + torch.ones(3))
except RuntimeError as error:
    print(type(error).__name__)
```

## 向量化的好處與代價

以批次 Tensor 取代 Python 每筆迴圈，通常減少解譯器與裝置呼叫開銷。但 `[N,1,D] - [1,M,D]` 會產生 `[N,M,D]` 中間結果；N、M 都很大時，記憶體可能先爆掉。可以分塊或改用矩陣恆等式。廣播讀取本身常以 stride 表示，後續運算輸出仍可能很大。

## batch 矩陣乘法

`[B,N,F] @ [B,F,C] → [B,N,C]`，最後兩軸做矩陣乘法，前面的 batch 軸依規則對齊。先從二維推演，再擴充高維，不要依賴試到沒有報錯。`nn.Linear(F,C)` 的儲存權重為 `[C,F]`，forward 會使用合適的轉置，與自己寫 `[F,C]` 的數學記號要分清楚。

## 練習與解答

`[8,1] - [8]` 為何變成 `[8,8]`？答案：右邊補成 `[1,8]`，兩個軸分別擴張。若想逐樣本比較，將標籤 unsqueeze(1)，或只對預測 squeeze(1)。若把 pairwise 距離當逐筆 loss，即使沒有 runtime error，學習目標也已改變。

## 官方來源與延伸閱讀

- [廣播規則](https://docs.pytorch.org/docs/2.15/notes/broadcasting.html)
- [torch.matmul](https://docs.pytorch.org/docs/2.15/torch.html#blas-and-lapack-operations)
