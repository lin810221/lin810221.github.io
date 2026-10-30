# 混合精度AMP：autocast、GradScaler與clipping順序

使用目前API，先保留float32基準，再選配CUDA混合精度。

## 不把整個模型盲目half

autocast依運算選擇合適精度，搭配float32參數與必要的高精度運算。float16可能發生梯度underflow，GradScaler將loss放大後反向，再還原梯度供更新。bfloat16的動態範圍不同，是否需要scaler與裝置支援要依實際配置決定，不把所有低精度混為一談。

## 目前的API與正確順序

本課使用torch.autocast與torch.amp.GradScaler，不以舊的torch.cuda.amp命名空間作主線。scaler在完整訓練中應建立一次並跨step沿用，續訓保存scaler.state_dict。core中的amp_step是一個獨立更新的教學函式，不把每次新建scaler當長期訓練建議。

```python
# CUDA訓練片段：model、x、y、optimizer需先準備好。
import torch
scaler = torch.amp.GradScaler('cuda')
# for x, y in loader:
#     optimizer.zero_grad(set_to_none=True)
#     with torch.autocast('cuda', dtype=torch.float16):
#         loss = criterion(model(x), y)
#     scaler.scale(loss).backward()
#     scaler.unscale_(optimizer)
#     torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
#     scaler.step(optimizer)
#     scaler.update()
```

先unscale再clip，才是在真實梯度尺度裁切。累積多批時，同一有效群組完成後才unscale／step／update；不可中途改scale後把不同縮放梯度混在一起。

## 本章預設與選配

`20_amp.py`預設在CPU做AMP停用的float32更新，測試比對普通step；它不是CPU AMP加速成績。明確加`--cuda-amp`才要求CUDA，不可用時直接錯誤。GPU路徑需在你的硬體檢查finite loss、梯度、數值差異、吞吐與記憶體，不能從CPU fallback推定已通過。

## 練習與解答

若clipping在unscale前，閾值相當於被scale改變，可能把梯度裁得過小。解答：先還原，再檢查／裁切。若AMP後NaN，回到FP32定位、檢查不穩定算子與輸入，必要時局部停用autocast；不能靠scaler修正原本就除零或錯誤標籤的問題。

## 完整可執行範例

從專案根目錄執行 `python pytorch/examples/20_amp.py`。下載包內另含共用模組、資料與測試，請一起保留。

<!-- example:20_amp.py -->

## 官方來源與延伸閱讀

- [AMP examples](https://docs.pytorch.org/docs/2.15/notes/amp_examples.html)
- [AMP API](https://docs.pytorch.org/docs/2.15/amp.html)
