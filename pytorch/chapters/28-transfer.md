# 凍結與遷移學習：參數不更新，模組仍有模式

分清requires_grad、optimizer覆蓋範圍與BatchNorm／Dropout的狀態。

## 什麼叫凍結

把backbone參數requires_grad設False，代表它們不需計算參數梯度。只把head參數交給optimizer，確保更新範圍明確。這與eval不同：eval調整模組行為，不是鎖定weights；凍結weights也不一定阻止BatchNorm running statistics變化。

## 本課例子的界線

範例使用隨機初始化的Linear backbone，凍結後只訓練分類head，檢查backbone相等且head變化。它展示凍結機制，**沒有下載或使用預訓練權重**，因此不拿它宣稱遷移學習能提升準確率。真正transfer需另選適當預訓練模型、授權、前處理與相容套件。

## 凍結的執行順序

```python
import torch
from torch import nn
backbone = nn.Sequential(nn.Linear(4,6), nn.ReLU())
head = nn.Linear(6,3)
for parameter in backbone.parameters():
    parameter.requires_grad_(False)
optimizer = torch.optim.AdamW(head.parameters(), lr=.001)
with torch.no_grad():
    features = backbone(torch.randn(2,4))
logits = head(features)
print(logits.shape)
```

固定feature extractor時no_grad可減少圖；若你要讓前面的輸入或其他可訓練模組透過backbone反向，則不能直接把整段關掉。先畫出需要哪條梯度路徑。

## 分階段解凍

先訓練head，再解凍後幾層，使用較小backbone lr。重新建optimizer會失去原動量，add_param_group則需管理新增參數與scheduler相容性。每次改動都印可訓練參數數與group，確認沒有漏掉層或重複加入。若backbone需保持eval，外層model.train後要重新設定該子模組。

## 練習與解答

凍結參數後running_mean仍變動，原因是BatchNorm仍train mode。解答：明確決定是否凍結統計，再對backbone.eval；這不是所有transfer方案一律必做，而是要符合資料與策略。測試weights不變只驗證參數，還要另外檢查buffer，才能完整描述狀態是否保持。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/15_freezing.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:15_freezing.py -->

## 官方來源與延伸閱讀

- [Transfer learning](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [Module狀態](https://docs.pytorch.org/docs/2.15/notes/modules.html)
