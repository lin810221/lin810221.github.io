# 遮罩格式與ignore_index

<figure class="cv-figure"><a href="assets/figures/17-segmentation-tasks.svg" target="_blank" rel="noopener"><img src="assets/figures/17-segmentation-tasks.svg" alt="三個相同雙人物場景分別顯示同類同色語意分割、人物各色實例分割和帶背景區域的全景分割。" loading="lazy"></a><figcaption>像素標籤與物件身分。先判斷需要「類別」或「個體身分」；不要直接把彩色調色盤當成連續迴歸目標。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>指出每個像素的類別及忽略區，追蹤空間對齊，並核對損失或指標的分母政策。 本頁主題：遮罩格式與ignore_index。</p></div>

## 看起來一樣的PNG，數值可能不同

標註工具可能輸出整數索引PNG、RGB顏色圖、每物件一張二值mask，或多邊形／RLE。這些格式不能直接互換。顏色圖中的`[0,255,0]`可能代表葉片，不代表類別255；索引PNG的顏色盤只是顯示方式，真正像素值可能是1。匯入前先檢查影像mode、唯一值與標註工具格式。

建立明確的label map，例如背景0、葉片1、花朵2、無法判定255。255是本課選用的ignore_index，不是固定的第256類。不能把未標註區一律改成背景：背景是「確定不是目標類」，未標註是「沒有可靠答案」，兩者的監督意義不同。

## 遮罩不走照片的正規化

照片可以轉float再除255，類別mask不可如此處理。原本類別1除255變成0.0039，再轉long會變0，於是幾乎所有前景被洗成背景。RGB顏色mask也應先依精確色表映射成類別ID，遇到未知顏色應拒絕或記錄明確政策，不用「最接近色」默默掩蓋壓縮或標註錯誤。

```python
import torch

target = torch.tensor([[[0, 1], [2, 255]]], dtype=torch.long)
valid = target != 255
allowed = torch.tensor([0, 1, 2, 255])
assert torch.isin(target, allowed).all()
assert int(valid.sum()) == 3
```

這裡最後一格不參與訓練與評估的有效像素分母；不應先把它轉成背景再計算。若整個batch都沒有有效像素，要按實驗政策跳過或回傳明確狀態，不能把NaN loss當成正常數字繼續更新。

## 成對幾何與離散插值

對照片做resize可以採bilinear等連續插值，mask則應使用保留類別ID的方式，例如nearest。`tv_tensors.Mask`讓v2依型別選擇相應行為；仍要檢查新mask的唯一值是否為原類別集合的子集，因為自己寫的轉換或錯誤型別包裝可能繞過預期政策。

```python
from torchvision import tv_tensors
from torchvision.transforms import v2

image = tv_tensors.Image(torch.zeros((3, 2, 2), dtype=torch.uint8))
mask = tv_tensors.Mask(target[0])
out_image, out_mask = v2.Resize((8, 8))(image, mask)
assert set(out_mask.unique().tolist()) <= {0, 1, 2, 255}
assert out_image.shape[-2:] == out_mask.shape[-2:]
```

裁切、旋轉與翻轉都必須使用同一組幾何參數。填補新區域時應明定填背景還是ignore，取決於是否真的知道那裡屬背景。對遮罩做ColorJitter、JPEG壓縮或照片的Normalize，則會破壞其語意。

## 損失與評估共同遵守ignore

多類別交叉熵可設定`ignore_index=255`；自訂Dice、IoU與confusion matrix也必須先用相同valid mask排除。若訓練忽略卻評估當背景，分母就不一致。二元BCE常需先以`reduction="none"`取得逐像素loss，再以valid mask選取或加權平均，不應假定所有loss都有相同ignore參數。

資料清單應保存來源標註ID、畫布尺寸、label map版本、邊界模糊區政策與標註品質。若同一病人或同一原圖被切成許多patch，先按原始群組切分再切patch，避免相鄰像素跨到train/test。

## 練習與解析

mask唯一值原為`{0,1,255}`，resize後出現`{0,1,32,64,128,255}`，可能是哪裡錯？最先檢查是否把mask當一般影像做bilinear；不能直接round後宣稱已恢復，因為邊界插值已混合背景、前景與ignore。應從原始離散mask重做轉換。

交付時附原圖、離散mask、疊圖與唯一值統計各一份；檢查一張全背景、一張含ignore、一張多類與一張空有效區。型別介面見[torchvision Mask](https://docs.pytorch.org/vision/stable/generated/torchvision.tv_tensors.Mask.html)，縮放見[Resize](https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.v2.Resize.html)。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 16_mask_pipeline.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:16_mask_pipeline.py -->

