# 專題：可訓練的像素分割

<figure class="cv-figure"><a href="assets/figures/25-project-pipelines.svg" target="_blank" rel="noopener"><img src="assets/figures/25-project-pipelines.svg" alt="商品分類使用整張類別和混淆矩陣，偵測使用框類別和AP，表面分割使用像素類別和IoU Dice。" loading="lazy"></a><figcaption>把分類、偵測與分割各做成一個專題。改變任務時，連標註成本、評估單位與失敗成本一起改變。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>沿專題資料流逐步對照命令與成品，指出真值、保留集、指標及版本紀錄的位置。 本頁主題：專題：可訓練的像素分割。</p></div>

分割專題把每個像素變成分類目標，特別重視幾何對齊、類別ID與分母政策。

## 任務與資料

本課合成圖以mask0表示背景、1表示前景。make_shapes同時產生影像、類別、mask與box，這些是同一個生成物件的不同標註。分割模型只用影像和mask，不需要從分類標籤猜像素位置。

輸入[N,3,24,24]，輸出logits[N,2,24,24]；target為long[N,24,24]。CrossEntropy沿類別軸比較每個像素，target不做one-hot，也不跟影像一起除255。如果真實資料使用255忽略區，要用ignore_index並在指標中排除相同區域。

## 從最小模型開始

17_train_segmenter.py使用 $3\times 3$ 卷積、ReLU與 $1\times 1$ 輸出head，訓練35步。這不是完整U-Net，但能驗證像素loss、梯度與驗證流程；當資料需要更大上下文或多尺度時，再換用U-Net等架構並保持相同評估契約。

<!-- example:17_train_segmenter.py -->

本課驗證以前景的全體像素交集與聯集計算IoU和Dice，這是micro式聚合；如果改成逐影像先算再平均，結果可能不同。背景不列入前景IoU，但仍影響FP及FN；報告應把政策說清楚。

## 儲存圖像與模型

在examples資料夾執行`python 17_train_segmenter.py --output outputs/segmentation`。preview.png每列由左至右為原影像、真值mask、預測mask；report.json保存數值，segmenter.pt保存state_dict。這讓你能同時觀察分數與邊界，不把全體平均當成每張都正確。分類與定位範例也有相同的--output選項，具體圖例見包內README。

## 圖像驗收

隨機抽查影像、真值與預測疊圖，檢查是否有一格偏移、邊界膨脹或小物件消失。mask resize採最近鄰避免製造虛構類別；logits resize則可使用適當連續插值，再argmax。兩種處理不是相同函數，要依模型輸出定義操作。

真實專題可加入ignore區域、不同前景大小與不規則形狀，使用群組切分。只在同一生成器得高分，不能聲稱能分割照片、器官或工業瑕疵。需要新的標註與獨立外部資料，確認類別及邊界定義。

## 練習與解析

真值只有100個前景，預測全背景，pixel accuracy可能仍很高，但前景IoU為0。這揭露了背景不平衡；應看每類IoU、支持像素與物件尺度切片。若真值和預測都完全沒有前景，本課將該類IoU列未定義，不能未說明就視為100%。

對小物件，邊界錯1像素可能影響很大。若任務重視邊界，可另加適當邊界指標與標註一致性評估，但不把不同像素解析度的距離直接混在一起。

交付包括模型、mask類別表、ignore政策、插值與還原方法、聚合方式、錯例圖及來源版本。這些設定與權重一樣影響最終結果。

## 官方與原始資料

[CrossEntropy像素分類](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)；[U-Net原始論文](https://arxiv.org/abs/1505.04597)

來源查核：2026-11-23。合成資料的結果只驗證教學流程，不是自然影像效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 17_train_segmenter.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

