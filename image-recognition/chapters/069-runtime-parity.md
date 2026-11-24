# 數值一致性與部署驗收

<figure class="cv-figure"><a href="assets/figures/23-pipeline-contract.svg" target="_blank" rel="noopener"><img src="assets/figures/23-pipeline-contract.svg" alt="前處理模型後處理三段依序串接，下方manifest包含輸入契約類別順序正規化座標版本校驗值測試樣本。" loading="lazy"></a><figcaption>部署契約：前處理、模型與後處理一起保存。遇到匯出前後結果不同，先比對輸入張量，再比對logits，最後比對後處理。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>從原始影像走到輸出，指出本單元必須保存或實測的契約，並標明量測範圍。 本頁主題：數值一致性與部署驗收。</p></div>

部署驗收要比較同一個函數、同一份輸入與同一個後處理政策，才知道差異發生在哪裡。

## 分層比較

第一層比較輸入像素與tensor；第二層比較模型logits或原始預測；第三層比較softmax、框反轉、NMS、mask還原等後處理；最後比較任務指標及使用者可見結果。只比較畫面上同一類名稱，會漏掉大量接近門檻的差異。

float32不同kernel的計算順序可能造成小誤差。常用判準是abs(a-b)≤atol+rtol×abs(reference)。本課先用atol1e-5、rtol1e-4檢查小模型；這是驗證設定，不是所有任務適用的通用標準。低精度及不同硬體要重新選定有意義的容許範圍。

$$
|y_{runtime}-y_{ref}|\le a_{tol}+r_{tol}|y_{ref}|
$$

## 門檻附近的風險

兩個runtime輸出0.49999與0.50001，數值非常接近，卻會在threshold=.5分到不同類。應另外統計決策翻轉、信心邊界、框NMS排序及IoU是否跨過評估門檻。相同分數或極相近框的排序可能有tie差異，報告要說明規則。

偵測不能只比輸出列表第i個框，因為排序與數量可能改；需先按類別及IoU做合理匹配，分開比座標、分數及新增／遺失框。分割則要注意ignore區域與像素對齊，不能將resize後的mask直接與原尺寸標註混算。

## 固定測試組

保留標準、極端尺寸、低亮度、小物件、透明圖、空目標與非法格式案例。固定原始檔雜湊和期待的處理規則，不能每次重新隨機產生卻稱同一回歸測試。合成資料適合測shape、幾何和邊界，真實代表性資料才能驗證實務品質。

本課ONNX範例會比batch1、3、8，覆蓋動態batch的幾個位置；並未聲稱所有尺寸、GPU、手機、TensorRT或INT8都測過。若部署目標不同，保留同一驗收方法，重新執行並寫入實際證據。

## 練習與解析

某次匯出Top1一致率100%，但少數類recall下降，可能嗎？若這兩個數字真的對同一批輸入及相同label定義計算，就互相矛盾；應檢查取樣、label map、門檻或版本是否不同。先解決報告契約，再推論模型原因。

另問：外接框只差1像素是否可忽略？對200像素物件可能影響小，對2像素物件很大。驗收應連結任務尺度，而不是只用全體平均座標誤差。

## 官方與原始資料

[NumPy assert_allclose](https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html)；[ORT相容性](https://onnxruntime.ai/docs/reference/compatibility.html)

來源查核：2026-11-23。合成資料的結果只驗證教學流程，不是自然影像效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 21_export_onnx.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

<!-- example:21_export_onnx.py -->

