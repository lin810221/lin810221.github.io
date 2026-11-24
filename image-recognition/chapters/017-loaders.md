# DataLoader批次與可重現性

<figure class="cv-figure"><a href="assets/figures/05-group-splits.svg" target="_blank" rel="noopener"><img src="assets/figures/05-group-splits.svg" alt="三個來源群組各有三張近似影像，分別完整進入訓練驗證測試，紅色虛線指出同來源跨組的洩漏。" loading="lazy"></a><figcaption>影像資料的切分邊界。逐張隨機分割不能保證獨立；先選正確的來源群組，再檢查重複影像。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>沿影像和標註的路徑讀圖，指出必須共同改變的欄位，以及需要隔離的來源群組。 本頁主題：DataLoader批次與可重現性。</p></div>

將樣本組成適合任務的批次，先在單進程跑對，再逐步處理 worker、隨機狀態與效能。

## 從一筆樣本走到一個批次

Dataset 回傳一筆資料，DataLoader 決定索引順序、批次大小、載入進程與如何組合樣本。分類若每張圖都是同 shape 的 CHW，通常可堆疊為 NCHW；若尺寸不同，先有固定縮放／補邊政策，或使用自訂 collate。框數量各異的偵測資料不能直接當成固定長度矩陣堆疊。

例如兩張圖分別有 1 與 3 個物體，boxes shape 為 `(1,4)` 和 `(3,4)`。為了讓它們進同一批而胡亂補零，會把不存在的框送入訓練，除非模型介面明確接受 padding 和 valid mask。TorchVision 偵測常用影像 list 與目標字典 list，保留每張的變長結構。

## 先採容易除錯的設定

本課 CPU 入門先用 `num_workers=0`，在主進程載入資料，錯誤堆疊較直接。訓練通常 shuffle=True，驗證／測試通常 shuffle=False，且 drop_last=False，確保最後不足一批的樣本仍被評估。驗證不打亂是方便追蹤與固定順序，不代表只有這個設定才有合法數學結果；重點是所有樣本與身分對應都正確。

batch_size 是每次組成幾筆；更大會增加輸入與活化記憶體，也可能改變最佳化行為。num_workers 是載入端並行數，不是模型計算執行緒數，也不會憑空增加 GPU。先量測資料等待與計算時間，再比較 0、1、2 等有限設定，避免把能跑的流程調成大量進程競爭。

## 隨機來源不只一個

抽樣順序、影像增強、模型初始化、Python random、NumPy 與 torch 都可能影響結果。設定其中一個 seed 不會自動控制其他來源。以下為 DataLoader 設定示意，假設已建立合法的 `train_dataset`；實際訓練仍需另設定模型初始化與記錄環境。

```python
import random
import numpy as np
import torch
from torch.utils.data import DataLoader

def seed_worker(worker_id):
    seed = torch.initial_seed() % 2**32
    random.seed(seed)
    np.random.seed(seed)

def make_loader(train_dataset):
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)
    gen = torch.Generator().manual_seed(42)
    return DataLoader(train_dataset, batch_size=8, shuffle=True,
        num_workers=0, generator=gen, worker_init_fn=seed_worker,
        drop_last=False, pin_memory=False)
```

num_workers=0 時不會呼叫 worker_init_fn，主進程的 seed 因此前面另設。若程式使用 `np.random.default_rng` 的獨立 Generator，`np.random.seed` 不會改變它，應明確建立並傳遞該 Generator。記錄 seed 只是重現條件的一部分，不保證不同硬體、套件版號與後端的每個浮點位元都相同。

## Windows 多進程的必要結構

Windows worker 通常透過 spawn 啟動新解譯器，會重新匯入模組。把訓練與 DataLoader 啟動放進 `main()`，並用 `if __name__ == '__main__': main()` 保護；Dataset 類別、collate_fn、worker_init_fn 放在模組頂層，避免無法序列化的區域函式或 lambda。先確認單進程正確，再增加 worker。

以下偵測 collate 的示意保留變長內容，沒有替框補零。是否需要 list 或 tuple 再由模型介面決定。

```python
def collate_detection(batch):
    images, targets = zip(*batch)
    return list(images), list(targets)
```

persistent_workers 可減少重啟成本，但 worker 的隨機狀態與資料物件也會持續存在；不能假定每個 epoch 都回到同一狀態。預取增加同時在記憶體中的批次，影像較大時可能是明顯成本。這些選項應由實際效能量測支撐，而不是一律打開。

## 驗收可重現性要比較什麼

在同一環境與資料版本，從全新程式執行兩次，記錄前幾批 sample_id、label、增強參數及 loss 趨勢。只檢查「最後準確率差不多」可能漏掉順序不一致；只要求完全相同又可能把跨硬體浮點差異誤認為資料洩漏。依目的設定精確相等或數值容許誤差，並保留執行環境。

## 練習與解析

**題目：** 驗證集 19 張、batch size 8，drop_last=True 會評估幾張？為何固定 seed 後每次按第二次訓練仍可能不同？

**解析：** 只評估 16 張，最後 3 張被丟掉，可能讓結果偏向特定順序。Notebook 或同一進程的隨機狀態已被前次訓練消耗，模型與 loader 也可能未重新初始化；要重新建立完整狀態或從新程式執行。再核對其他 RNG、worker 與非確定性操作。

## 官方來源

[PyTorch 資料載入文件](https://docs.pytorch.org/docs/2.15/data.html) 可核對批次與 Windows spawn；[可重現性說明](https://docs.pytorch.org/docs/2.15/notes/randomness.html) 可核對 seed 與跨環境限制。示意設定為本課 CPU 起點，並非所有硬體的效能最佳值。
