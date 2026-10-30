# 模型沒有學到：從第一個失敗的數值開始查

建立可重複的診斷順序，將資料、計算圖、最佳化與評估錯誤分開定位。

## 先界定失敗發生在哪裡

loss不降、訓練準確但驗證失敗，以及存檔後推論改變，是三種不同問題。先保留一個輸入批次、標籤、初始化與版本，縮短到CPU單步。若每次都換資料、seed和設定，修好後也難以知道原因。記錄第一次出現異常的張量，而非只留下最後的NaN。

## 用一個批次檢驗可學性

暫時關閉增強、Dropout與正則化，反覆訓練同一小批資料。對本課乾淨、可分且容量足夠的範例，loss應能明顯下降。這不是泛化評估，也不是任何資料都必然趨近零的定理：相同輸入若有矛盾標籤，就有不可消除的限制。成功後恢復獨立驗證資料，再逐項加回功能。

## 一次更新的四道檢查

先確認輸入有限、shape和類別範圍正確，再看logits、loss與梯度，最後比較參數更新前後。`grad is None`可能是未參與計算圖或被detach；全零梯度可能是飽和、mask或局部導數為零；有限但極小的梯度又是另一件事。optimizer持有舊模型參數、忘記step或在backward前清錯梯度，都可能讓參數不動。

```python
import torch
from torch import nn
torch.manual_seed(7)
model=nn.Linear(2,2)
optimizer=torch.optim.SGD(model.parameters(),lr=.1)
x=torch.tensor([[1.,-1.],[.5,2.]])
y=torch.tensor([0,1])
before=model.weight.detach().clone()
optimizer.zero_grad(set_to_none=True)
loss=nn.functional.cross_entropy(model(x),y)
assert torch.isfinite(loss)
loss.backward()
assert model.weight.grad is not None
assert torch.isfinite(model.weight.grad).all()
optimizer.step()
assert not torch.equal(before,model.weight)
```

## 第一個非有限值

除零、直接對零取log、過大的exp、無效的全遮罩Attention列，常比optimizer本身更早造成異常。用穩定的logsumexp與logits版loss；對小範例可開`torch.autograd.detect_anomaly()`定位backward來源，但它有額外成本，不當成日常效能設定。不要用任意clip或nan_to_num把根因藏起來。

## 訓練正常卻評估失敗

檢查eval模式、訓練統計前處理、標籤對應及padding語意是否一致。若單批可記住、全資料train正常但validation差，才往資料分布、容量、正則化與資料量調查。最後用同一輸入比對記憶體模型和重載模型的logits，確認交付邊界。

## 練習與解答

你看到loss有限、每個參數grad都有值，但weight完全沒變。下一步是什麼？答案：確認step執行、lr非零、optimizer的參數物件就是現在forward的模型，並以clone快照比較。僅印出兩次同一個Parameter參考，可能兩次都指向已更新的值而無法證明差異。

## 原始論文與官方來源

- [Autograd異常偵測](https://docs.pytorch.org/docs/2.15/autograd.html)
- [Module與訓練模式](https://docs.pytorch.org/docs/2.15/notes/modules.html)
