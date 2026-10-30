# nn.Module：參數、buffer、子模組與 state_dict

讓 optimizer、device 搬移與存檔都能找到真正需要管理的狀態。

## Module 管理的不只是 forward

繼承 nn.Module 並呼叫 super().__init__，再將層指定為 self 的屬性。透過 `model(x)` 呼叫 forward，讓 hooks 與框架機制正常運作。不要平常直接用 model.forward(x) 來繞過這層入口。

## 三種狀態

Parameter 會出現在 model.parameters，optimizer 才能取得它；buffer 不需要梯度，但可能需要保存與跟隨 device，例如正規化統計；一般 Python 屬性是你的程式狀態，不能假設自動存檔。本章 center 是 register_buffer，所以會出現在 state_dict，也會隨 model.to 移動。

## 容器的差別

`self.layers=[nn.Linear(...)]` 是普通 list，內部 Module 不會按這個寫法被註冊。用 ModuleList 保留可自行迭代的註冊子模組；Sequential 適合依序串接單一輸入輸出。ModuleList 本身不替你定義 forward，需自行寫迴圈。

```python
from course_core import TinyMLP
model = TinyMLP()
print(sum(p.numel() for p in model.parameters()))
for name, tensor in model.state_dict().items():
    print(name, tuple(tensor.shape))
```

預設 MLP 的參數數量為 4×12+12+12×3+3=99。Dropout 與 ReLU 無可訓練參數，不代表它們在 forward 沒有效果。透過參數計數可以快速發現忘記註冊的層。

## forward 應保持介面清楚

輸入 x[N,4]，回傳 logits[N,3]，loss 在外部計算，方便訓練與推論共用。不要每次 forward 重新建立 Linear，那會使權重反覆初始化且不在既有 optimizer 內。資料尺寸變動也應明確驗證，不依靠隱藏的 reshape 消除錯誤。

## 練習與解答

執行範例，比較正確模型的 named_parameters、named_buffers、state_keys 與錯誤容器的參數數。解答：plain list 中的 Linear 雖然可以做矩陣運算，optimizer 卻可能完全不知道它存在。修正為 ModuleList，再確認參數計數與 state_dict 都增加，而不是只看 forward 有沒有輸出。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/07_modules.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:07_modules.py -->

## 官方來源與延伸閱讀

- [Modules](https://docs.pytorch.org/docs/2.15/notes/modules.html)
- [神經網路元件](https://docs.pytorch.org/docs/2.15/nn.html)
