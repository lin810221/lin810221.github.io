# 偵測資料與共同轉換

<figure class="cv-figure"><a href="assets/figures/06-paired-transforms.svg" target="_blank" rel="noopener"><img src="assets/figures/06-paired-transforms.svg" alt="兩個十乘六方格展示左側三乘三遮罩與框，水平翻轉後移到右側，框由1,2,4,5變成6,2,9,5。" loading="lazy"></a><figcaption>幾何增強要同步變換標註。先驗證轉換後框和mask仍覆蓋同一物件，再開始長時間訓練。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>核對框、類別與分數的意義；區分框邊界、模型輸出、抑制規則與真值匹配。 本頁主題：偵測資料與共同轉換。</p></div>

## 偵測批次不是一張固定長度的標籤表

一張照片有三隻貓，另一張沒有任何貓，偵測模型仍應接受兩張圖。分類的單一整數標籤無法描述這種答案；常見偵測資料集回傳`image, target`，其中target是字典。Torchvision偵測器的images通常是影像Tensor的list，各圖可以不同尺寸；targets是對應字典的list。不要把不同數量的框硬堆成普通`[N,K,4]`再假裝K固定。

本課的目標物類別從1開始，0保留給Torchvision常見偵測器的背景。這是本課偵測介面約定，不是全世界資料集的共通類別編碼；語意分割的0可以是正常的背景類。從外部資料轉入時保存雙向對照表，輸出時也要還原原始category_id。

## 最小target與型別

`boxes`是`float32 [K,4]`、`labels`是`int64 [K]`，每列代表同一個物件。分割任務另有`masks [K,H,W]`。`image_id`辨識原圖而非批次位置；供評估使用的`area`、`iscrowd`要依資料與評估契約保存，不可把真實群聚標註一律改成0。

```python
import torch
from torchvision import tv_tensors
from torchvision.transforms import v2

image = tv_tensors.Image(torch.zeros((3, 80, 120), dtype=torch.uint8))
target = {
    "boxes": tv_tensors.BoundingBoxes(
        [[10., 20., 40., 60.]], format="XYXY", canvas_size=(80, 120)
    ),
    "labels": torch.tensor([1], dtype=torch.int64),
}
flip = v2.RandomHorizontalFlip(p=1.0)
flipped_image, flipped_target = flip(image, target)
assert torch.equal(flipped_target["boxes"], torch.tensor([[80., 20., 110., 60.]]))
```

這段只驗證成對轉換，不宣稱零影像可以訓練出辨識能力。`canvas_size`順序是H,W；boxes列的順序是x,y。`tv_tensors.Image`、`BoundingBoxes`、`Mask`告訴v2物件的語意，避免把框當作一般矩陣處理。

## 一次抽樣幾何參數，再共同變換

如果分別對影像與框呼叫兩次隨機翻轉，即使機率都是0.5，兩者仍可能只翻到其中一個。應把整份樣本一起傳給同一組轉換。裁切後移除框，必須同步移除labels與相應的instance masks；顏色擾動通常只作用於影像，不能改變類別遮罩的ID。

例如原來三個物件的labels是`[1,2,1]`，裁切僅保留第0與第2個框，labels應成為`[1,1]`。若只把框刪成兩列，labels仍三列，便失去一對一對應。使用清理轉換時仍要用小樣本畫圖驗證，不把「函式沒有報錯」當成標註正確。

## 空圖與資料載入

真正沒有目標物的圖應表示為`boxes.shape == (0,4)`、`labels.shape == (0,)`。不要造一個零面積的背景框；那是無效幾何。`collate_fn`可回傳`tuple(zip(*batch))`或明確建構兩個list，避免預設collation嘗試堆疊不同尺寸影像與框數。訓練前檢查資料ID無重複、框位於畫布、標籤在對照表範圍內。

切分仍以病人、相機、拍攝批次、影片等獨立群組為單位。同一物件的相鄰幀出現在train與test，可能讓分數看起來很好，卻無法驗證陌生場景的能力。augmentation只在train隨機使用；validation的幾何與輸出還原政策固定保存。

## 練習與解析

假設一張圖寬100，框`[5,10,25,30]`和一個對應二值遮罩。水平翻轉時只改框，遮罩沒變，會發生什麼？框移到`[75,10,95,30]`，遮罩仍在左側，兩種監督互相矛盾。驗收時疊上半透明遮罩與矩形框，並檢查遮罩非零範圍是否落在框政策容許的範圍。

再試一張空圖、一張一物件、一張多物件，確認DataLoader都能回傳；每次隨機轉換後列數與畫布尺寸維持一致，才進入長時間訓練。

## 原始資料與API

[Torchvision成對轉換範例](https://docs.pytorch.org/vision/stable/auto_examples/transforms/plot_transforms_e2e.html)說明TVTensor的用途；[偵測微調教學](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html)提供模型資料介面。此處以本課小型原創樣本推導檢查方式，查核2026-11-23。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 07_joint_transforms.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:07_joint_transforms.py -->

