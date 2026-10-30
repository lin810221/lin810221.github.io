# 驗證與推論：eval、no_grad、inference_mode

兩種獨立開關：模組行為與Autograd記錄，必須各自設定。

## eval 不是關閉梯度

model.eval() 相當於將模組切到train(False)，使Dropout、BatchNorm等使用推論行為。一般Linear仍可建立計算圖，所以eval後output.requires_grad仍可能True。相反地，no_grad只改Autograd記錄，不會幫你關Dropout。正式驗證通常需要兩者。

## 選擇 no_grad 或 inference_mode

no_grad適合不需要記錄該段運算；inference_mode有額外限制與優化，適合輸出不會再投入需梯度記錄的推論路徑。不能把inference mode建立的Tensor任意帶回訓練並假設一切相同。兩者都不是參數凍結旗標，也不會替你改model.training。

```python
import torch
from torch import nn
model = nn.Sequential(nn.Linear(4,3), nn.Dropout(.5))
x = torch.ones(2,4)
model.eval()
print(model(x).requires_grad)  # True
with torch.inference_mode():
    output = model(x)
print(output.requires_grad)    # False
```

## 模式還原與驗證資料

本課evaluate在進入時記錄原training旗標，以finally還原；若模型原本eval，結束仍eval。這個小型模型各層模式一致；若你刻意把部分backbone設eval，需逐模組管理混合模式，不可假設一次model.train(previous)能還原各子層差異。

驗證不shuffle、不做隨機train增強，不用驗證答案反向更新參數。仍可依驗證結果選超參數／best checkpoint，因此最後需要獨立test衡量選擇後的結果。

## 練習與解答

Dropout模型重複預測不同，只有包no_grad仍不同，原因是它還在train mode。加入eval後核對同一輸入輸出一致。若在驗證後忘記切回train，Dropout可能整個後半訓練都被關閉。解答：明確在train_epoch開始呼叫train，evaluate使用try/finally，並加入模式與grad行為測試。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/10_evaluation.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:10_evaluation.py -->

## 官方來源與延伸閱讀

- [Evaluation mode 與 grad modes](https://docs.pytorch.org/docs/2.15/notes/autograd.html#evaluation-mode-nn-module-eval)
