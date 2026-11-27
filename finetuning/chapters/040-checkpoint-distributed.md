# Activation checkpoint與分散式訓練

節省哪種記憶體、增加哪種成本，要分清楚。

## Activation checkpoint的交換

一般反向需要保存中間activation；checkpoint捨棄其中部分，在反向時重新計算，以更多計算換取較低保存量。它不是把訓練狀態存成可續訓檔案，也不會讓基底權重消失。

需確認checkpoint模式、隨機狀態、dropout與模型支援，並核對是否與 `use_cache` 相容。先在小批次比較開關前後梯度與loss，再量測峰值和每步時間。不能只看到記憶體下降就假設數值與效能都合格。

## DDP與分片各自做什麼

DDP讓多個程序各持有模型副本並同步梯度，通常不靠增加GPU數來縮小單卡權重。FSDP或其他分片方案可分散參數、梯度與最佳化器狀態，但增加通訊、載入與checkpoint複雜度。量化adapter訓練還需核對所選組合是否支援。

從Accelerate設定啟動時，保存程序數、精度、累積與分片政策。檢查有效token的跨rank分母、資料是否重複、只有主程序寫檔等細節。本課實測為單程序CPU；分散式是工程指南，需在目標硬體另作驗收。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener"><img src="assets/figures/14.svg" alt="Activation checkpoint與分散式訓練：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Activation checkpoint與分散式訓練」讀圖：比較兩種保存內容，指出續訓與推論各自依賴的狀態。再回答：Activation checkpoint能不能代替保存optimizer的續訓checkpoint？</p></div>

## 自我檢查與解析

**題目：**Activation checkpoint能不能代替保存optimizer的續訓checkpoint？

<details><summary>展開解析</summary><p>不能。前者重算中間結果以省記憶體，後者保存訓練狀態以恢復進度，是不同功能。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/accelerate/usage_guides/gradient_accumulation)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
