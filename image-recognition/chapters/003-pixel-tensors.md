# 像素張量與數值範圍

<figure class="cv-figure"><a href="assets/figures/02-tensor-layout.svg" target="_blank" rel="noopener"><img src="assets/figures/02-tensor-layout.svg" alt="三色通道由HWC影像陣列重排成CHW三個平面，並分開標註uint8和float32範圍，批次後為NCHW。" loading="lazy"></a><figcaption>HWC 與 CHW：軸順序和數值範圍是兩件事。重排軸不等於除以255；使用前同時核對shape、dtype、值域。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>先指出圖中的輸入與輸出，再用本單元的術語描述它們；檢查尺寸、軸順序與座標是否一致。 本頁主題：像素張量與數值範圍。</p></div>

同一張影像可以有多種張量表示；形狀、dtype、範圍與通道順序必須一起寫進契約。

## 像素、通道與張量

灰階影像在每個位置存一個強度值，RGB 在同一位置存三個通道。張量是多維數值陣列：形狀告訴你每個維度有多長，dtype 告訴你可儲存的數值型別，語意則由資料契約決定。形狀是 `(3,32,32)`，還不能知道它是三張灰階圖，或一張三通道圖；要搭配維度名稱才完整。

本課圖片陣列採 HWC，即高、寬、通道；單張模型輸入採 CHW，批次為 NCHW。RGB uint8 像素通常是 0 到 255，模型前可轉 float32 的 0 到 1，再依指定均值與標準差做通道標準化。標準化後超出 0 到 1 是正常現象，不能再盲目截斷。

## 手算一個像素的轉換

假設紅通道原值為 128，縮放後是 $\frac{128}{255}\approx0.50196$。若採教學用均值 0.5、標準差 0.25，標準化結果約 0.00784。這兩步不同：先把數值單位換到 0–1，再相對於指定分布平移及縮放。直接把 uint8 改成 float32，128 仍是 128，不會自動變成 0.50196。

$$
x_{01}=\frac{x_{8}}{255},\qquad z_c=\frac{x_{01,c}-\mu_c}{\sigma_c},\qquad \sigma_c>0
$$

`mu`、`sigma` 必須與輸入縮放規則一致。若從資料估計，只能使用訓練集；若使用預訓練權重指定的前處理，應遵循該權重契約並在實驗中記錄。不能拿整份資料的統計量悄悄把測試分布帶進訓練。

## 維度換序不是重新解讀記憶體

下列獨立片段以人工指定的一個像素示意，重點在 `permute` 交換維度與明確縮放。

```python
import numpy as np
import torch

hwc = np.zeros((2, 4, 3), dtype=np.uint8)
hwc[1, 2] = [128, 64, 255]
x = torch.from_numpy(hwc).permute(2, 0, 1).float() / 255
batch = x.unsqueeze(0)
assert tuple(batch.shape) == (1, 3, 2, 4)
assert torch.isclose(batch[0, 2, 1, 2], torch.tensor(1.0))
```

`reshape(3,2,4)` 只改形狀解讀，不會把原本相鄰的 RGB 值正確搬到三個通道平面，因此不能取代 `permute`。`torch.from_numpy` 通常共享原陣列記憶體；若之後仍修改 NumPy 來源，需理解共享關係，必要時複製。`permute` 後可能不連續，只有在後續操作需要時才使用 `contiguous()`。

## 影像、類別與遮罩有不同規則

| 資料 | 例子 | dtype／範圍 |
| --- | --- | --- |
| 模型影像 | N×3×H×W | float32；依前處理契約 |
| 分類答案 | N | int64 類別 ID，0 可以是第一類 |
| 語意分割答案 | N×H×W | int64；本課 0 是合法背景類，255 為忽略 |
| 偵測答案 | 每張的 N 個框 | float32 XYXY；前景 label 從 1 起，0 保留給背景 |

語意 mask 的 255 是「不計入損失／評估」的標記，不是最白的物體。不要除以 255，也不要套影像均值標準化；resize 使用最近鄰保留離散 ID。偵測類別 0 的保留是本課對應偵測 API 的契約，不能推論所有分類或所有套件都禁止 0。

## 記憶體與失敗診斷

一個 $8\times3\times224\times224$ float32 批次僅輸入就需要 $8\times3\times224\times224\times4=4{,}816{,}896$ bytes，約 4.59 MiB；訓練還有活化、梯度與最佳化狀態。把 batch 加倍可能使多個部位一起增長。若顏色顛倒，檢查 RGB／BGR；若輸出總是相近，檢查範圍、通道、模型模式與標籤，不要立刻增加網路深度。

## 練習與解析

**題目：** mask 原本只有 `{0,1,255}`，經前處理後出現 0.0039；哪裡出錯？影像標準化後出現負數又是否同樣錯誤？

**解析：** mask 很可能被當影像除以 255，類別 1 被改成約 0.0039，應保留整數標籤與 ignore 規則。影像的負數可能只是低於均值的合法標準化值，兩者不能用同一範圍判準。

## 官方來源

[TorchVision ToDtype](https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.v2.ToDtype.html) 說明 dtype 與縮放選項；[Tensor.permute](https://docs.pytorch.org/docs/2.15/generated/torch.Tensor.permute.html) 可核對維度換序。數值與記憶體算例為本課自行設定。
