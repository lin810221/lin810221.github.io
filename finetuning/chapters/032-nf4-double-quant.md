# NF4、double quantization與QLoRA

理解論文中的三個節省來源，不把它們混成同一件事。

## NF4不是均勻四位元整數

NF4使用針對近似常態權重分布設計的非均勻碼本，搭配分塊縮放。四位元能表示十六個碼，但重建數值的間距不必相同。若分布有強烈離群值或不同形狀，其效果仍需測試，不能把設計假設當作品質保證。

Double quantization再壓縮量化常數，減少metadata成本；它不表示把每個權重簡單量化兩次就等同論文方法。Paged optimizer則處理記憶體壓力的另一部分，與NF4碼本是不同機制。

## QLoRA的訓練路徑

QLoRA保留量化且凍結的基底，透過浮點計算訓練低秩adapter。梯度更新adapter，並非直接把四位元整數權重當成一般可微參數更新。基底解量化與adapter運算仍有暫存及activation成本。

課程的量化入口只用均勻玩具量化說明誤差，明確不冒稱NF4或GPU QLoRA實測。真正支線使用bitsandbytes設定與PEFT的k-bit準備步驟；需要相容GPU時才執行，並量測實際峰值而非引用論文硬體當成本機結果。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener"><img src="assets/figures/11.svg" alt="NF4、double quantization與QLoRA：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「NF4、double quantization與QLoRA」讀圖：比較兩排碼本間距，說明本單元涉及哪種量化與哪些假設。再回答：使用四位元權重並完整更新所有權重，就能稱為本課所說的QLoRA嗎？</p></div>

## 自我檢查與解析

**題目：**使用四位元權重並完整更新所有權重，就能稱為本課所說的QLoRA嗎？

<details><summary>展開解析</summary><p>不能。此處的QLoRA指凍結量化基底並訓練低秩adapter的路徑，需同時確認量化、凍結與可訓練參數。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/2305.14314)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
