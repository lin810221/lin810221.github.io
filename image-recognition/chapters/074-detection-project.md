# 專題：單物件定位到多物件偵測

<figure class="cv-figure"><a href="assets/figures/25-project-pipelines.svg" target="_blank" rel="noopener"><img src="assets/figures/25-project-pipelines.svg" alt="商品分類使用整張類別和混淆矩陣，偵測使用框類別和AP，表面分割使用像素類別和IoU Dice。" loading="lazy"></a><figcaption>把分類、偵測與分割各做成一個專題。改變任務時，連標註成本、評估單位與失敗成本一起改變。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>沿專題資料流逐步對照命令與成品，指出真值、保留集、指標及版本紀錄的位置。 本頁主題：專題：單物件定位到多物件偵測。</p></div>

先完成受限制的單物件定位，再理解一般偵測器多出的物件數、類別、背景與匹配問題。

## 小專題的明確假設

23_train_locator.py假設每張合成圖恰好一個前景，輸出四個正規化框邊界，以SmoothL1訓練。它沒有處理沒有物件、多個物件或多類別，因此不能稱為完整通用偵測器。這個限制讓座標、loss與評估先變得可檢查。

原圖24×24，真值框以除24正規化；輸出經sigmoid落在0到1。推論時乘24，並排序左右及上下邊界，再算每張圖與該張真值的IoU。排序是輸出契約的一部分；一般偵測器可能使用中心寬高或其他參數化，要依模型解碼方式核對。

## 可以直接跑的定位訓練

<!-- example:23_train_locator.py -->

驗證用不同seed的32張圖，報平均IoU與樣本數。平均會掩蓋最差案例，可以再列IoU低於.5的比例及錯框圖。因為每張圖都一定一個物件，沒有FP／FN的完整問題，不計通用mAP。

## 接到真正偵測器

一般偵測target是每張影像的boxes[N,4]與labels[N]，不同影像N可不同，也可為0。TorchVision模型接收影像list與target list；num_classes包含背景。訓練回傳loss字典，eval回傳boxes、scores及labels，兩種模式的回傳契約不同。

15_detector_contract.py先驗證合成資料契約，明確加--heavy可建立未訓練FasterRCNN骨幹與偵測頭並跑CPU前向，不下載權重。這是API煙霧測試；真正微調需選擇具名預訓練權重、核對條款、替換head及使用代表性標註資料。

## 評估與交付

用13_iou_nms.py了解框重疊與類別內抑制，再用14_detection_ap.py手算一對一匹配與重複FP。正式資料使用COCO格式及官方評估時，保存類別ID映射、ignore／crowd、area、maxDets與IoU設定，不把toy AP當成COCO mAP。

## 練習與解析

把一張完全空白圖輸入單物件定位器，它仍會吐一個框，為何？因為架構沒有「沒有物件」的輸出與訓練資料。低IoU無法完整表示這個失敗，下一步需要物件存在性、背景負例或一般偵測器。先修改任務契約，再選適合架構。

完整偵測專題的驗收除了分數，還要看空目標、重複框、小物件、遮擋、來源切分與原圖座標還原。所有預處理和門檻都保存，才有可重現結果。

## 官方與原始資料

[官方物件偵測微調](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html)；[COCOeval原始碼](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)

來源查核：2026-11-23。合成資料的結果只驗證教學流程，不是自然影像效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 23_train_locator.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

