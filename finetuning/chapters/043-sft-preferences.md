# SFT、DPO與RLHF的資料差異

示範學習與偏好比較回答不同的問題。

## SFT給示範，偏好給比較

SFT告訴模型一個合適回答長什麼樣；偏好資料比較同提示下的兩個候選。偏好學習可補充風格與品質排序，但不能憑空提供沒有出現在資料中的可靠事實。SFT後再做DPO是一種常見路線，並非所有任務的固定必經順序。

傳統RLHF流程可能包含偏好標註、reward model與policy最佳化；DPO以特定目標直接利用配對，省去明確訓練reward model的那條主線。它們不是相同API的不同名稱。

## 先固定比較對象

保留SFT checkpoint作為基準，定義偏好評估、事實指標與能力保留集。模型若更討喜卻更容易編造，不能以偏好勝率單獨宣布成功。偏好規則、候選來源與標註品質需與權重一起記錄。

本課先手算序列分數，再拆DPO公式，最後使用真實TRL跑最小步驟。讀者應能解釋chosen與rejected的監督範圍，以及reference為什麼固定；不應只看到一個較低的loss就認為對齊已完成。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener"><img src="assets/figures/15.svg" alt="SFT、DPO與RLHF的資料差異：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SFT、DPO與RLHF的資料差異」讀圖：重算差中之差與DPO logit，指出四個序列分數的角色。再回答：DPO不需顯式reward model，是否代表不需偏好規則？</p></div>

## 自我檢查與解析

**題目：**DPO不需顯式reward model，是否代表不需偏好規則？

<details><summary>展開解析</summary><p>仍需要。偏好配對與標註規則定義了學習訊號；省去一個模型不會省去資料品質與評估。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/2305.18290)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
