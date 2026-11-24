# 部署驗收練習與解析

<figure class="cv-figure"><a href="assets/figures/23-pipeline-contract.svg" target="_blank" rel="noopener"><img src="assets/figures/23-pipeline-contract.svg" alt="前處理模型後處理三段依序串接，下方manifest包含輸入契約類別順序正規化座標版本校驗值測試樣本。" loading="lazy"></a><figcaption>部署契約：前處理、模型與後處理一起保存。遇到匯出前後結果不同，先比對輸入張量，再比對logits，最後比對後處理。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>從原始影像走到輸出，指出本單元必須保存或實測的契約，並標明量測範圍。 本頁主題：部署驗收練習與解析。</p></div>

本章把前處理、匯出、速度與監測放在同一份交付中，目標是另一個人可以重現並判斷限制。

## 題目：模型檔相同卻結果不同

兩個服務載入完全相同ONNX，A採RGB，B採BGR；A把letterbox補邊去掉再反算框，B直接除單一scale。哪個需要重訓？

解析：先不用重訓。兩個服務計算的是不同輸入及後處理函數，應回到訓練契約統一。對偵測框，先減dx／dy再除實際sx／sy，並保存原圖尺寸；整數取整可能讓sx與sy略不同。

## 題目：動態batch的證據

匯出時指定dynamic_shapes，只用batch2驗證，可以宣稱batch1到8都正確嗎？解析：不能。至少挑範圍邊界與中間值，還要測非法輸入是否符合服務規則。動態宣告是圖的契約，執行測試是額外證據；兩者不能互相替代。

## 題目：計算整體加速

原流程解碼15ms、模型10ms、後處理5ms，模型加速到2ms。總時間由30變22ms，加速約1.364倍。若只報模型5倍加速，不能拿它回答整體服務有沒有達標。

## 題目：沒有真實標註的監測

上線後confidence平均提高，是否表示品質提升？解析：不代表。模型可能遇到更容易資料，也可能變得過度自信。必須配合獨立抽樣標註、類別與設備切片、錯例與版本，才能估計品質。

## 實作任務

執行21_export_onnx.py，確認ONNX checker與三種batch的logit比對都完成；讀取輸出的contract，指出它固定哪些軸、哪些軸動態。再跑22_benchmark.py，在記錄中填入實際CPU、Python、套件、執行緒、輸入大小、warmup及樣本數。

不要把本機速度貼成其他硬體的保證。若只能用CPU，明確記錄CPU；沒有跑CUDA、INT8或手機，就列為未驗證路線。這種界線能讓下一位接手者知道該補哪一個測試，而不是猜測。

## 交付檢查表

- 原始檔到模型輸入的每一步皆有設定與固定樣本。
- 模型、標籤、前後處理與需求檔有相同版本記錄。
- 數值誤差與任務評估分開，空目標及非法輸入有明確政策。
- 速度報告寫出量測範圍，監測含抽樣複核與回退條件。

完成後可以進入專題。專題不是額外列出模型名稱，而是把資料、訓練、評估與成品連成一條能執行的路徑。

## 官方與原始資料

[ONNX Runtime Python](https://onnxruntime.ai/docs/api/python/api_summary.html)；[PyTorch匯出教學](https://docs.pytorch.org/tutorials/beginner/onnx/export_simple_model_to_onnx_tutorial.html)

來源查核：2026-11-23。合成資料的結果只驗證教學流程，不是自然影像效能基準。
