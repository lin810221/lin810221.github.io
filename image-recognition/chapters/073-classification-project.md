# 專題：從影像到分類報告

<figure class="cv-figure"><a href="assets/figures/25-project-pipelines.svg" target="_blank" rel="noopener"><img src="assets/figures/25-project-pipelines.svg" alt="商品分類使用整張類別和混淆矩陣，偵測使用框類別和AP，表面分割使用像素類別和IoU Dice。" loading="lazy"></a><figcaption>把分類、偵測與分割各做成一個專題。改變任務時，連標註成本、評估單位與失敗成本一起改變。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>沿專題資料流逐步對照命令與成品，指出真值、保留集、指標及版本紀錄的位置。 本頁主題：專題：從影像到分類報告。</p></div>

本專題以可從零執行的小型分類器，完成資料生成、訓練、獨立驗證、錯誤切片與成品契約。

## 任務與輸出

辨識24×24影像中的正方形或細長矩形。標籤0為square、1為bar，背景有小幅隨機雜訊，前景位置改變。這是明確控制因素的教學資料，沒有攝影機或自然影像泛化宣稱；它能讓你確認管線確實更新參數。

make_shapes以seed23產生96張訓練影像、seed41產生48張驗證影像。不同種子避免完全相同生成樣本，但仍共享同一生成機制，因此不把它等同跨設備的真實外部驗證。真實專題要用工件、個體或拍攝場次分組切分。

## 依序執行

先跑01_image_io.py與06_group_split.py建立輸入及切分直覺，再執行09_train_classifier.py。追讀vision_core.py中的模型：兩層卷積、池化、3×3適應池化及2類head。每次更新使用AdamW與CrossEntropy，驗證時eval和inference_mode。

接著跑10_classification_metrics.py核對手算矩陣，再跑20_shift_slices.py比較原生成條件與刻意反轉亮度。最後用21_export_onnx.py理解獨立的匯出一致性測試；預設是未訓練模型，加入`--trained --output outputs/onnx`則先訓練本課分類器，再匯出並驗證同一個模型。也可在自己的程式把已訓練model傳入export_and_compare，避免將不同成品混在一起。

## 保存實驗紀錄

至少記錄資料生成版本、seed、樣本數、shape、dtype、range、模型結構、lr、步數及loss。輸出每類recall、混淆矩陣與錯例ID。選擇最佳checkpoint時使用驗證資料，不因測試結果不好而重新挑選。

可將model.state_dict()及class map保存到自己指定目錄。檔名附版本有助辨識，但真正內容應寫入manifest及雜湊；只用「final_final2.pth」無法說明來源。讀取時重建相同架構，再載入可信的state_dict。

## 改動一個因素

把訓練影像數減少、增大雜訊、改變前景大小或增加旋轉，每次只動一項。先預測哪個指標會變，再驗證。若新增圓形當第三類，需要一起改資料、head、loss目標及label map，不是只把num_classes改3。

## 練習與解析

模型在原生成資料滿分、反轉亮度後大幅降低，是程式失敗嗎？不一定。這是刻意域改變造成的可觀察失效，說明模型依賴的特徵未涵蓋新條件。若要支援反轉，需要合理的訓練資料或策略，並保留新的獨立驗證，而不是修改報告分母。

驗收要求可以從乾淨環境執行、loss下降、保留資料指標與固定錯例可追溯。分數只是其中一項，資料邊界與完整交付同樣需要成立。

## 官方與原始資料

[PyTorch資料與訓練流程](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)；[保存模型](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)

來源查核：2026-11-23。合成資料的結果只驗證教學流程，不是自然影像效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 09_train_classifier.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:09_train_classifier.py -->

