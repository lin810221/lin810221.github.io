# 混合精度、BF16與梯度裁剪

精度配置涵蓋多種張量，不只是模型載入參數。

## 不同dtype的角色

FP16與BF16都是較小的浮點格式，但指數範圍與尾數精度不同。適合的格式依硬體與運算而定，不能把它們視為相同的開關。模型權重、activation、累積梯度、最佳化器狀態與部分敏感運算可能使用不同dtype。

Autocast為支援的運算選擇dtype；某些FP16流程需要gradient scaler。進行梯度裁剪前需先unscale，否則裁剪到的不是原梯度尺度。BF16常不需要同樣的scaling，但仍需檢查非有限值與硬體支援。

## 先建立數值基準

本課CPU主線使用FP32，便於比較loss、梯度與合併結果。移到GPU時，以固定批次比較FP32或較高精度基準，記錄loss、梯度範數、輸出差異與容許誤差。不同kernel與硬體可能改變浮點結果，不能承諾跨平台bitwise一致。

出現NaN時保存第一個異常步驟的資料ID、長度、dtype與梯度，再降低到單批次重現。盲目調小學習率可能掩蓋無效mask或非法輸入；必須先確認資料與目標正確。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener"><img src="assets/figures/13.svg" alt="混合精度、BF16與梯度裁剪：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「混合精度、BF16與梯度裁剪」讀圖：數出microbatch與更新的邊界，說明有效target不同時如何加權。再回答：使用autocast後，所有模型張量是否都變成同一dtype？</p></div>

## 自我檢查與解析

**題目：**使用autocast後，所有模型張量是否都變成同一dtype？

<details><summary>展開解析</summary><p>不是。不同運算與狀態可能採不同精度，應分項檢查；量化權重的儲存格式也另算。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://docs.pytorch.org/docs/stable/notes/amp_examples.html)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
