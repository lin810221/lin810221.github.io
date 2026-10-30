# CUDA實務：非同步、OOM、allocated與reserved

讀懂GPU記憶體與計時，避免用錯誤量測做效能決策。

## 非同步如何影響觀察

GPU運算常以非同步方式提交，Python函式回傳不表示裝置已算完。只用perf_counter包一次forward，可能主要量到排程開銷。錯誤也可能在較晚同步點才浮現。除錯時可使用官方建議的同步設定縮小位置，但不應把除錯同步模式當正式效能結果。

## 一個基本量測片段

```python
# GPU片段：model與x需已在CUDA，且先完成暖機。
import time, torch
if torch.cuda.is_available():
    torch.cuda.synchronize()
    started = time.perf_counter()
    # output = model(x)
    torch.cuda.synchronize()
    print(time.perf_counter() - started)
```

這個空區塊本身不是模型benchmark，請放入你的實際運算並重複多次。分開量首次編譯、暖機與穩態；清楚記錄batch、shape、dtype、train/eval與是否包含搬移。也可用CUDA events量裝置時間，但同樣要理解同步。

## allocated與reserved

allocated描述Tensor等實際使用的記憶體，reserved含allocator保留區域。nvidia-smi還可能包含context與其他程序。empty_cache主要釋放未使用cache，不會把仍被引用的Tensor消掉，也不應每batch呼叫當萬用OOM解法。

## OOM的處理順序

先看batch／sequence長度與中間Tensor是否意外擴成N×N×D，清除history對圖的引用，驗證流程使用inference mode。再考慮小batch+正確累積、AMP、activation checkpointing。activation checkpointing以重新計算換記憶體，與訓練存檔checkpoint不同；Dropout／RNG與模組副作用需按API語意檢查。

## 多裝置生態

PyTorch也有MPS、XPU、ROCm等路徑，支援運算、profiler與dtype不同。本課CPU實測不代表其他硬體都相同；GPU部署應記build、driver與裝置，按官方平台文件驗證。最新2.15增加多種硬體能力，但本課不為沒有的硬體報效能數字。

## 練習與解答

每輪GPU記憶體持續上升，先查是否append未detach的loss或activation。若allocated穩定、reserved高，不一定是洩漏；可能是allocator保留。解答：先比較同shape多輪的趨勢與peak，再區分引用、cache與工作負載變動，不能只看一次nvidia-smi就下結論。

## 官方來源與延伸閱讀

- [CUDA與記憶體語意](https://docs.pytorch.org/docs/2.15/notes/cuda.html)
- [Activation checkpointing](https://docs.pytorch.org/docs/2.15/checkpoint.html)
