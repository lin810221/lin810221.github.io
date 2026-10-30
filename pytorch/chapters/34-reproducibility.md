# 隨機種子與可重現性：seed能保證什麼

辨認不同隨機來源、運算非決定性與跨版本差異。

## seed控制的是序列起點

同一RNG、相同狀態與相同呼叫次序，才會得到同一序列。先抽一組亂數再初始化模型，與先初始化模型再抽亂數，可能得到不同weights，即使最初manual_seed相同。獨立Generator可隔離資料切分、shuffle與其他隨機操作。

## 範例中的獨立來源

第18例使用獨立Generator做randperm，再插入global torch.rand，確認不影響該Generator的序列。這不是說所有隨機性都被隔離；Dropout仍使用其裝置的RNG。Python random、NumPy、外部augmentation套件及worker都可能另有狀態。

## 決定性演算法

```python
import random, torch
random.seed(7)
torch.manual_seed(7)
torch.use_deterministic_algorithms(True)
```

這個選項會選擇決定性路徑或在無可用路徑時報錯，可能有速度代價。某些CUDA運算還需依官方說明設定額外環境。cuDNN benchmark控制演算法搜尋，與deterministic不是同一件事。不要只貼上幾行設定就保證跨所有硬體bitwise一致。

## 重現與穩健性要分開

固定一個seed可協助除錯，但模型是否穩健要看多個seed、split與合理擾動。比較方案時使用配對seed與相同資料，回報平均與變異；只挑最好的seed會使成績偏樂觀。精確續訓與統計上可重現也有不同要求，第32章只測前者的受控CPU案例。

## 練習與解答

先設seed，再多呼叫一次torch.randn，模型初始化可能改變；為資料shuffle傳獨立Generator後，global呼叫不再影響它。解答：存seed只是記錄起點，resume要保存目前RNG state；從epoch2接續時重設最初seed會回到錯誤位置。正式產物還要記版本、OS、device與決定性設定，才能解釋相同seed卻不同的結果。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/18_seeds.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:18_seeds.py -->

## 官方來源與延伸閱讀

- [Reproducibility](https://docs.pytorch.org/docs/2.15/notes/randomness.html)
