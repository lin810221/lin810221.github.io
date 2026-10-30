# 儲存與載入：state_dict、map_location 與信任來源

把模型、前處理與設定一起交付，區分推論權重與續訓狀態。

## 保存什麼才足夠

state_dict保存參數與persistent buffers，並不保存你任意寫的Python前處理或欄位意義。推論包至少要有模型設定、weights、train scaler、label mapping與版本。續訓另需optimizer、scheduler、scaler、RNG與進度。本課payload同時保存current model與best_model，兩者用途分開。

## 載入與重建模型

先用相同結構建立Module，再load_state_dict。map_location='cpu'讓GPU存檔能先在CPU讀取，之後按需求移device。strict預設檢查key；若故意只載backbone，需讀missing/unexpected keys，不能一律strict=False把結構錯誤藏起來。

```python
import torch
from course_core import TinyMLP
model = TinyMLP()
# 教學片段：路徑需為你自己產生且信任的檔案。
# state = torch.load('weights.pt', map_location='cpu', weights_only=True)
# model.load_state_dict(state)
model.eval()
```

本章完整例子使用temporary directory真正寫入、載入與比對，不會覆蓋你的檔案。

## weights_only 的用途與限制

本課明確指定weights_only=True，payload僅含Tensor、字串、數字與一般容器。這限制unpickling可做的事情，但仍只載入可信來源，不視為任意檔案的安全沙盒。不要為了解決不相容就直接改False；先理解檔案格式、必要類別與來源。

## 保存瞬間要獨立

CPU Tensor若只detach可能仍共享儲存；best快照逐值clone。新run使用新路徑，本課save_checkpoint若檔案已存在會拒絕，避免不小心改掉上一次。正式長時間訓練可設計暫存檔與原子替換，還需考慮同檔案系統與失敗恢復，不要把教材小例當完整儲存服務。

## 練習與解答

重新啟動Python載入檔案，對相同raw feature做預測，應與保存前一致。若只保存normalized輸入卻未保存mean/scale，真實新資料就無法按訓練方式轉換。解答：weights之外的資料契約也是模型產物，應一起版本化。不要以「檔案能打開」代替輸出一致性測試。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/16_checkpoints.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:16_checkpoints.py -->

## 官方來源與延伸閱讀

- [Serialization](https://docs.pytorch.org/docs/2.15/notes/serialization.html)
- [存取模型](https://docs.pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html)
