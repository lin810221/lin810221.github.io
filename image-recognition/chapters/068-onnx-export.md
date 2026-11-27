# 使用現行ONNX路徑匯出模型

<figure class="cv-figure"><a href="assets/figures/23-pipeline-contract.svg" target="_blank" rel="noopener"><img src="assets/figures/23-pipeline-contract.svg" alt="前處理模型後處理三段依序串接，下方manifest包含輸入契約類別順序正規化座標版本校驗值測試樣本。" loading="lazy"></a><figcaption>部署契約：前處理、模型與後處理一起保存。遇到匯出前後結果不同，先比對輸入張量，再比對logits，最後比對後處理。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>從原始影像走到輸出，指出本單元必須保存或實測的契約，並標明量測範圍。 本頁主題：使用現行ONNX路徑匯出模型。</p></div>

ONNX把模型運算表示成可由其他runtime執行的圖；匯出成功只證明轉換可完成，還要驗證數值、形狀與完整前後處理。

## 現行PyTorch匯出方式

本課採torch.onnx.export的 `dynamo=True` 路徑，使用torch.export擷取模型，再轉換為ONNX。動態維度用dynamic_shapes描述；舊教材常見dynamic_axes主要對應不同匯出路徑，不直接拿來替代新API的設定。

匯出前model.eval()，輸入Tensor契約與正式推論一致。指定input_names與output_names有助於服務整合；opset_version依目標runtime支援選擇，不以數字最大為目的。本課小模型用opset18，單檔 `external_data=False` ；大型模型可能需要外部權重檔，交付時不能只複製主檔。

## 固定與動態維度

本課固定$C=3$、$H=W=24$，只讓batch在1到8間動態。匯出示例使用batch2，避免以1讓某些shape推導特化。dynamic_shapes描述可接受範圍，但服務仍要做明確輸入驗證；不能只依賴runtime報錯。

```python
dynamic_shapes = {'x': {0: torch.export.Dim('batch', min=1, max=8)}}
```

鍵x對應forward參數名稱，不是任意取的服務欄位。若改模型forward名稱或改成多個輸入，設定也需核對。動態寬高還會受到池化、patch與網路結構限制，不能只把四個軸都標dynamic就保證支援。

## 完整可執行驗證

21_export_onnx.py建立未訓練的小分類器，匯出並通過onnx.checker，再在ORT CPU以batch1、3、8比對logits。此範例刻意把數值一致性與辨識能力分開：未訓練模型也能驗證轉換，但沒有任務效能宣稱。

<!-- example:21_export_onnx.py -->

## 匯出已訓練模型

在examples資料夾執行`python 21_export_onnx.py --trained --output outputs/onnx`，會先完成本課合成分類訓練，再以同一個模型匯出與比對。資料夾包含classifier.onnx與contract.json；輸出紀錄另列訓練驗證結果和三種batch的數值誤差。自己的訓練程式可呼叫export_and_compare(folder, model)保留同一份參數，不需要為匯出重新訓練。

## 常見失敗

缺少onnxscript是環境問題；不支援的算子是匯出或runtime問題；把資料依賴的Python分支寫進forward則可能需要重構。不要為了讓圖輸出而默默刪掉NMS或某個重要運算，再稱為同一模型。

## 練習與解析

只比較argmax相同是否足夠？不夠。logits可能已有很大偏移，只是未跨過排名邊界；在門檻附近就可能改變決策。應同時比有限性、shape、絕對／相對誤差及代表性輸入，再比完整任務結果。套件鎖版和runtime提供者也要一起記錄。

## 官方與原始資料

[PyTorch ONNX現行API](https://docs.pytorch.org/docs/2.15/onnx.html)；[ONNX checker](https://onnx.ai/onnx/api/checker.html)；[ORT Python API](https://onnxruntime.ai/docs/api/python/api_summary.html)

來源查核：2026-11-23。合成資料的結果只驗證教學流程，不是自然影像效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 21_export_onnx.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

