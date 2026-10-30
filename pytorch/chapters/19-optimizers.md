# Optimizer：SGD、AdamW、param groups 與梯度清除

理解更新規則、optimizer 狀態與參數清單，而非只調 learning rate。

## optimizer 只管理交給它的參數

建立 optimizer 時傳入 model.parameters，之後 forward 新建立的層不會自動加入。凍結參數可以先 requires_grad_(False)，再用 filter 組清單。解凍後確認 optimizer 是否包含它，不能只改旗標就期待更新。

## SGD 與 AdamW 的起點

SGD 沿梯度下降，Momentum 加入歷史方向；AdamW 使用各參數的一階／二階估計並解耦 weight decay。這些狀態解釋了為何續訓不能只存模型。相同 lr 在不同 optimizer、loss 縮放與 batch 下，更新行為不同。AdamW 的 weight_decay 也不是任何情境都等同在 loss 手加 L2。

## 參數分組

```python
import torch
from torch import nn
model = nn.Sequential(nn.Linear(4,8), nn.ReLU(), nn.Linear(8,3))
optimizer = torch.optim.AdamW([
    {'params': model[0].parameters(), 'lr': 1e-4},
    {'params': model[2].parameters(), 'lr': 1e-3},
], weight_decay=.01)
for group in optimizer.param_groups:
    print(group['lr'], len(group['params']))
```

分組常用於 pretrained backbone 與新 head。不要把同一參數重複放入兩組；記錄規則與參數名稱，續訓時以相同結構建 optimizer，避免狀態錯配。bias、norm 是否 decay 應依模型與訓練方案決定，不是所有專案都一律排除。

## 梯度清除與 clipping

每次有效更新先 zero_grad，再 forward/backward。需要 clipping 時放 backward 之後、step 之前；AMP 則先 unscale。zero_grad(set_to_none=True) 不會把參數歸零，只清除梯度。optimizer.step 可能有動量與 decay，不能單憑本輪 grad 為零推定參數絕不變動。

## 練習與解答

模型參數有10個Tensor，optimizer只有2個，你預期所有層都訓練嗎？答案：不會；比對 `id(p)` 清單與 requires_grad，找出遺漏或刻意凍結的部分。另一題：續訓 loss 曲線突然轉折但weights相同，可能缺了什麼？optimizer 動量、scheduler、scaler、RNG與資料位置都要檢查，而非只懷疑存檔壞掉。

## 官方來源與延伸閱讀

- [Optimizer 與 scheduler](https://docs.pytorch.org/docs/2.15/optim.html)
