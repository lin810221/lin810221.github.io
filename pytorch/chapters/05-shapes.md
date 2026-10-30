# Shape 與軸：索引、切片、維度變換與 reduction

在每一步寫下維度，避免數字可以計算但意義已經錯位。

## 每個軸都要有名字

`[N,F]` 表示 N 筆樣本與 F 個特徵；`[N,C,H,W]` 表示影像 batch、channel、高、寬；`[N,T,D]` 表示序列位置與表示維度。相同數量的元素可以有不同意義。`reshape` 不會理解哪一軸是時間，更不會自動把 HWC 圖片變成 CHW。

## 索引會不會消掉維度

```python
import torch
x = torch.arange(12, dtype=torch.float32).reshape(3, 4)
print(x[0].shape)       # [4]，第一個軸消失
print(x[0:1].shape)     # [1,4]，保留 batch
print(x[:, 1].shape)    # [3]
print(x[:, 1:2].shape)  # [3,1]
print(x.sum(dim=1).shape)                 # [3]
print(x.mean(dim=1, keepdim=True).shape)   # [3,1]
```

`dim=1` 是消去／聚合第 1 軸，並不是「取第一列」。keepdim 保留長度 1 的軸，便於後續廣播。讀程式時以軸名稱代替純數字，例如「對每筆樣本的 feature 平均」。

## unsqueeze、squeeze、permute

`unsqueeze(1)` 將 `[N]` 變 `[N,1]`；`squeeze(1)` 只移除指定長度為 1 的軸。無參數 squeeze 可能把 batch_size=1 的 batch 軸也刪掉，造成訓練時正常、單筆推論失敗。影像 HWC→CHW 使用 permute(2,0,1)，因為它是調換軸，不是單純重排形狀。

## 最容易漏掉的回歸錯誤

預測 `[4,1]` 減答案 `[4]`，得到 `[4,4]`，每一筆預測竟與四個答案比較。程式不一定報錯，loss 甚至會下降。先明確決定回歸契約是兩者 `[N,1]` 或兩者 `[N]`，並在 loss 前 assert 相等。第 6 章解釋這是廣播規則的結果。

## 練習與解答

`x[2,3,4]` 對 dim=1 求和，keepdim=False 輸出 `[2,4]`；True 為 `[2,1,4]`。若每個樣本要有一個分數，需再決定聚合哪一軸。不要用 `view(-1)` 抹平所有維度來消除錯誤，因為那同時抹去了 batch 的意義。執行範例，親眼核對錯誤與修正後的差值形狀。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/02_shapes.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:02_shapes.py -->

## 官方來源與延伸閱讀

- [Tensor 維度操作](https://docs.pytorch.org/docs/2.15/tensors.html)
- [Broadcasting](https://docs.pytorch.org/docs/2.15/notes/broadcasting.html)
