# 模型學不動時如何逐步定位

<figure class="cv-figure"><a href="assets/figures/08-training-state.svg" target="_blank" rel="noopener"><img src="assets/figures/08-training-state.svg" alt="影像經CNN產生logits，與真實標籤形成損失，反向傳播回模型；下方區分train與eval加inference_mode。" loading="lazy"></a><figcaption>從logits、損失到參數更新。分類CrossEntropyLoss接收logits，不要在前面重複套softmax。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>說出模型在此階段收到什麼、輸出什麼；用本單元算例核對shape、狀態或評估分母。 本頁主題：模型學不動時如何逐步定位。</p></div>

除錯要把「資料是否正確」「梯度是否更新」「模型是否能擬合」「是否泛化」拆成可觀察的問題。

## 先看圖與標籤

畫出真正送入模型的batch，還原Normalize時使用同一組mean與std；檢查RGB／BGR、方向、裁切、標籤索引與實際內容。檔名順序和標籤表順序不一致，仍然會得到合法shape和有限loss。記錄原始ID，才能追到標註來源。

分類labels應在0到C-1間且是整數。影像若仍為uint8，某些算子會直接報錯；若轉float卻未除255，數值尺度可能使訓練不穩。已除255後又除一次，則訊號過小。對每個管線階段印dtype、shape、min、max，而不是只印最後結果。

## 單一batch過擬合測試

先選少量固定樣本，關閉強增強與過強正則化，重複訓練到近乎全對。如果做不到，先檢查訓練迴圈、loss對應、可訓練參數及資料，不急著下載大模型。成功只表示有擬合能力，不能當泛化證據。

檢查optimizer是否真的持有新分類頭的參數；若換head後仍沿用舊optimizer，新的head可能完全沒更新。也要檢查是否在錯誤的inference_mode範圍中訓練，或先detach了logits。

## 從曲線分辨下一個實驗

訓練與驗證loss都很高，可能欠擬合、標籤雜訊或前處理問題；訓練低驗證高，可能過擬合、資料分布不同或開發切分失真。兩條線不是診斷的充分條件，需要資料與錯例證據。

NaN時先找第一個不有限的張量。檢查除0、log0、極端lr與半精度overflow；CPU float32能作簡化基準。梯度裁切可限制梯度大小，但無法把錯的標籤修成對的。不要用nan_to_num讓問題消失在日誌中。

## 一張除錯紀錄表

每次只改一項：原始假設、觀察、改動、期待結果與實際結果。先固定seed與資料，再比較學習率或增強。若換模型、切分、輸入尺寸與門檻四件事一起發生，就無法說改善來自哪個設定。

## 練習與解析

訓練準確率100%，驗證50%，能斷言模型太大嗎？不能。標籤對照表在兩個資料夾互換，也會出現這個結果。先檢查兩份class_to_idx，再看資料來源差異，最後才談容量與正則化。

如果BatchNorm在驗證階段仍更新running stats，結果會隨驗證順序改變。正確操作是eval()，並避免驗證資料改變模型狀態。對無法解釋的高分，也要做標籤打亂與背景遮蔽等負向檢查，找出捷徑學習或洩漏。

## 官方與原始資料

[Autograd異常偵測](https://docs.pytorch.org/docs/stable/autograd.html#debugging-and-anomaly-detection)；[eval模式](https://docs.pytorch.org/docs/stable/notes/autograd.html#evaluation-mode-nn-module-eval)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。
