# 模型成品與前後處理契約

<figure class="cv-figure"><a href="assets/figures/23-pipeline-contract.svg" target="_blank" rel="noopener"><img src="assets/figures/23-pipeline-contract.svg" alt="前處理模型後處理三段依序串接，下方manifest包含輸入契約類別順序正規化座標版本校驗值測試樣本。" loading="lazy"></a><figcaption>部署契約：前處理、模型與後處理一起保存。遇到匯出前後結果不同，先比對輸入張量，再比對logits，最後比對後處理。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>從原始影像走到輸出，指出本單元必須保存或實測的契約，並標明量測範圍。 本頁主題：模型成品與前後處理契約。</p></div>

可部署成品不是只有一份權重；還必須讓另一個人知道如何把原始影像轉成模型輸入，再把輸出轉成正確結果。

## 輸入契約

保存layout、dtype、range、色彩順序、尺寸策略、EXIF及透明度處理、Normalize與允許的輸入格式。對本課分類器而言，輸入為float32 NCHW、3通道RGB、 $24\times 24$ 、0到1，沒有ImageNet Normalize。部署時額外加Normalize會改變函數，即使模型檔完全相同。

偵測常需要記錄resize及letterbox的實際比例、offset和原圖大小，輸出框才能反轉回原圖；分割則需要把logits或mask還原，並清楚定義插值、argmax順序與ignore區域。硬裁切掉的資訊不能靠座標反轉恢復。

## 輸出契約

分類保存label map及logits／機率定義；偵測保存框格式、座標單位、是否已做NMS、score threshold和max detections；分割保存每個class ID、背景及ignore_index。0在偵測target通常保留背景，在語意分割卻可以是有效類別，不能全站共用一條硬規則。

模型輸出[N,C]不等於服務必須回傳全部logits；可以回傳top-k與門檻判斷，但要能追溯模型與處理版本。低信心或不合法輸入的回應要事先定義，避免用一個正常類別假裝處理成功。

## 成品清單與校驗

建議包括模型檔、contract.json、labels.json、版本需求、資料與權重來源、指標報告、固定測試影像及預期輸出。模型與設定用SHA-256記錄完整性；雜湊只是內容識別，不代表安全或準確。只有可信來源的checkpoint才可載入，state_dict載入仍應注意型別與來源。

21_export_onnx.py會在暫存資料夾產生單檔ONNX與contract.json，驗證完自動清理。需要永久交付時可在自己的指定輸出目錄呼叫export_and_compare；不要把暫存路徑誤當部署成品位置。

## 一個版本改動算例

模型權重不變，label map從['良品','瑕疵']變成['瑕疵','良品']，所有語意都翻轉；前處理RGB變BGR也可能大幅改變結果。因此應將模型、前處理、標籤與後處理視為同一交付版本，而不是只看pth修改時間。

## 練習與解析

同一張圖在Python與網頁服務預測不同，先查哪裡？先固定原始檔雜湊，再逐步比較解碼後像素、EXIF方向、resize、通道、range及模型輸入，最後才比logits與後處理。若第一個張量就不同，先修資料流；重訓模型通常無法解決部署前處理錯誤。

驗收時至少保留一張普通、一張邊界尺寸、一張透明影像與一個無效檔案案例；回應應符合已定義的輸入契約。

## 官方與原始資料

[PyTorch模型保存](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)；[ONNX模型結構](https://onnx.ai/onnx/intro/concepts.html)

來源查核：2026-11-23。合成資料的結果只驗證教學流程，不是自然影像效能基準。
