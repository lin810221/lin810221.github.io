# 延遲吞吐記憶體與量化

<figure class="cv-figure"><a href="assets/figures/24-latency.svg" target="_blank" rel="noopener"><img src="assets/figures/24-latency.svg" alt="時間條按7毫秒讀取11毫秒前處理18毫秒模型6毫秒後處理8毫秒傳輸拆分，端到端共50毫秒。" loading="lazy"></a><figcaption>延遲的分母與計時邊界。寫下從哪個事件開始到哪個事件結束，再比較不同部署方案。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>從原始影像走到輸出，指出本單元必須保存或實測的契約，並標明量測範圍。 本頁主題：延遲吞吐記憶體與量化。</p></div>

速度需要先定義量測範圍與條件，才能把數字轉成部署決策。

## 分開每個階段

端到端延遲包含排隊、讀檔／解碼、前處理、CPU到GPU傳輸、模型、後處理與回傳。只量model(x)通常比實際服務快很多。批次大小增加可能提升吞吐，卻增加等待湊批的時間與單筆延遲，因此不能只報每秒張數。

例如解碼8ms、前處理4ms、模型10ms、後處理3ms，單筆串行約25ms，不是10ms。若模型加速兩倍，總時間變20ms，整體只快1.25倍。想改善哪個部分，應從實測瓶頸決定。

## 正確量測

先warmup，固定裝置、執行緒、batch、尺寸與dtype，重複量測並報median與p95。CPU同步執行可以用perf_counter；CUDA多為非同步，需要正確同步或CUDA events，否則量到的只是排程時間。不要把第一次載入權重和穩定期forward混成一個平均。

22_benchmark.py只量CPU小模型forward，排除解碼、排隊與傳輸。數字依硬體與背景負載變動，不在課文寫成保證速度。這個小範例的用途是正確建立量測邊界。

<!-- example:22_benchmark.py -->

## 壓縮與量化

減少通道、輸入尺寸、蒸餾、FP16／BF16及INT8是不同策略。量化需處理scale、zero point、支援算子與校準資料；權重變小不保證裝置有更快kernel。校準資料須代表部署，不能用測試標籤反覆最佳化後再報未受影響的分數。

量化後重跑數值及任務驗收，觀察小物件、少數類、低對比等切片。目標runtime與CPU／GPU不同，應參考當前官方支援路徑，不直接複製過時的量化API。課內介紹原理及ORT工具，沒有把未執行的INT8效能寫成實測。

## 練習與解析

batch8每批40ms，吞吐約200張／秒；但若只在湊滿8張才處理，低流量下單筆可能等很久。應配合最大等待時間與排隊策略。若服務要求p95低於50ms，只有平均20ms仍不足以驗收。

把尺寸長寬減半，輸入像素四分之一，但端到端不一定快四倍，因為解碼、排隊及固定成本仍存在。必須同時檢查辨識品質，尤其細小瑕疵是否被縮掉。

## 官方與原始資料

[PyTorch benchmark](https://docs.pytorch.org/docs/stable/benchmark_utils.html)；[ORT量化](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)；[CUDA同步](https://docs.pytorch.org/docs/stable/generated/torch.cuda.synchronize.html)

來源查核：2026-11-23。合成資料的結果只驗證教學流程，不是自然影像效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 22_benchmark.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

