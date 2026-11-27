# 專題：比較完整微調、LoRA與DPO

建立可歸因的比較，不只收集三條loss曲線。

## 定義三種不同問題

完整微調與LoRA比較的是參數適應方式；SFT與DPO比較的是學習訊號與目標，不能把三者當成完全平行的開關。先建立SFT基準，再選擇是否以LoRA訓練policy及是否加入偏好階段。

同一資料版本與模板下，記錄有效token、更新步數、超參數搜尋預算及可訓練參數。若候選使用不同資料量，明確描述為資料與方法共同變更，不能只歸因於演算法名稱。

## 一份比較報告的結構

先列任務與基準，再列資料、模型身分與設定，最後報保留品質、切片、成本與成品回讀。偏好階段另附配對品質、reference身分與DPO符號檢查；量化支線另附硬體、精度與峰值實測。

進階挑戰是設計rank與target模組消融，以及新任務和保留能力的取捨。結論可以是某個方法在限定成本與資料下較合適，不需要宣稱一種方法對所有LLM都更好。將失敗結果也保存，才能真正累積可用知識。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener"><img src="assets/figures/23.svg" alt="專題：比較完整微調、LoRA與DPO：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「專題：比較完整微調、LoRA與DPO」讀圖：沿完整交付鏈指出每個步驟產出的證據，再找出尚未測試的能力。再回答：LoRA SFT與完整參數DPO結果不同，能直接說是LoRA造成嗎？</p></div>

## 自我檢查與解析

**題目：**LoRA SFT與完整參數DPO結果不同，能直接說是LoRA造成嗎？

<details><summary>展開解析</summary><p>不能。參數化與學習目標都改變，需控制其中一項或建立更完整的實驗矩陣。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/dpo_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
