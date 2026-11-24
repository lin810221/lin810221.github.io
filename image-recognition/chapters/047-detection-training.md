# 偵測微調的實作契約

<figure class="cv-figure"><a href="assets/figures/14-detector-families.svg" target="_blank" rel="noopener"><img src="assets/figures/14-detector-families.svg" alt="三列並排流程分別展示候選區域兩階段、密集位置單階段與object queries集合預測，最後的重複處理方式不同。" loading="lazy"></a><figcaption>偵測器的設計家族。讀一個偵測器時，追蹤輸入、候選表示、匹配方式、損失與推論後處理。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>依排序追蹤TP／FP與分母變化，分開教學算例與正式COCO設定，說明一個重複或定位錯誤的影響。 本頁主題：偵測微調的實作契約。</p></div>

## 跑通介面與學會辨識是兩個里程碑

先以合成資料確認模型能接收images與targets、回傳有限loss、完成反向，再用固定驗證圖檢查推論輸出。這能驗證實作管線，但不能宣稱隨機初始化模型已具實用偵測能力。真正微調要有合適權重、標註資料、群組切分與足夠訓練，並報獨立評估。

Torchvision常見偵測器在`train()`且提供targets時回傳loss字典，在`eval()`推論時回傳每張圖的預測字典，包含boxes、labels與scores。不要用分類模型的`CrossEntropyLoss(model(batch), labels)`直接套在這裡；模型已依偵測架構建立多個訓練目標。

## 初始化要明確表達下載意圖

若需要完全不下載的介面示範，必須同時關閉模型與backbone預訓練權重；只寫`weights=None`不一定足以說明所有預設。以下為正式模型API的示意片段，正式完整實作仍須搭配資料載入、裝置及資源規劃，不把大型網路的訓練當作所有電腦都能立即完成的步驟。

```python
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn

model = fasterrcnn_resnet50_fpn(
    weights=None, weights_backbone=None, num_classes=3,
    min_size=128, max_size=128,
)
images = [torch.rand(3, 128, 128)]
targets = [{"boxes": torch.tensor([[15., 20., 75., 90.]]),
            "labels": torch.tensor([1], dtype=torch.int64)}]
model.train()
losses = model(images, targets)
total = sum(losses.values())
assert torch.isfinite(total)
```

這裡`num_classes=3`表示背景加兩個目標類，不是三個前景類。圖像浮點範圍與模型內部normalize要依該模型契約，不能先手動套另一分類模型的均值與標準差，造成重複正規化。

## 微調時更換預測頭

使用預訓練偵測權重是另一條明確選讀路線：確認模型與資料授權、權重版本、下載來源與雜湊，再載入對應weights enum。若目標類別數不同，要將分類／框頭換成符合自己標籤表的頭；實例分割還可能需更換mask頭。不能只改`labels`數值卻保留不相符的輸出語意。

先固定backbone小範圍訓練head，或以較小學習率解凍部分層，屬需要在驗證資料比較的策略。凍結梯度與BatchNorm的train/eval狀態分開處理，否則以為權重沒動，統計量仍可能改變。每個epoch保存loss各項、學習率、資料順序設定與評估口徑。

## 從最小樣本到正式實驗

先讓兩到八張人工確認的圖過擬合，檢查類別與框是否可學；再把augmentation逐項加回，觀察固定疊圖。回到完整資料後，按拍攝群組切分並保留空圖，避免資料管線只學到有物件場景。模型選擇用validation，test只用於最後確認。

推論使用`model.eval()`與`torch.inference_mode()`；它們用途不同，前者改變部分層行為，後者關閉梯度追蹤。把輸出移回CPU前先確認沒有把訓練loss當預測；保存原圖座標、類別對照、分數與模型版本，才能交給獨立評估器。

## 練習與解析

某程式把訓練loss字典當成`predictions[0]["boxes"]`，為何失敗？它混淆訓練與推論模式的輸出契約。先列印模式與回傳型別，將訓練步和推論步分開函式，並各用一個小樣本驗收。另一情境：模型可下載權重卻無法辨識自訂類別，不代表權重損壞；它的輸出類別語意可能根本沒有你要的類別，需微調與重新評估。

## 原始介面與執行界線

[Torchvision物件偵測微調教學](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html)提供標註與head替換的官方路徑；[Faster R-CNN模型文件](https://docs.pytorch.org/vision/stable/models/faster_rcnn.html)說明權重與模型輸入輸出。本文API查核2026-11-23，下載權重與大型資料微調是選讀路線，不能將本課離線玩具訓練結果當成其驗證。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 15_detector_contract.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:15_detector_contract.py -->

