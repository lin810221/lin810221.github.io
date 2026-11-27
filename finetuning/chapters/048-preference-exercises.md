# 偏好學習驗收：符號與標註

讓手算、程式與訓練三者對得起來。

## 三個必做反例

先令policy與reference分數相同，確認loss為基準值；再只提高chosen相對分數，確認loss下降；最後將chosen與rejected對調，確認方向反轉。reference張量即使意外設為可求梯度，目標函式也應將它detach。

資料面檢查同提示、候選不相同、來源可追溯與標註規則一致。若較佳答案總比較長或總使用特定詞，請測試是否出現偏差；不能只用同來源配對的勝率當作獨立證據。

## 與SFT基準一起交付

報告SFT基準與DPO候選的格式、事實、偏好及保留能力。記錄解碼與judge設定；如果使用人工評分，對候選順序盲化並保留平手。結果不明確時，呈現分母與不確定性，不勉強宣告贏家。

本章交付一份配對稽核表、手算DPO、數值梯度測試、TRL最小訓練與保留評估提案。這些是之後擴大偏好訓練的起點；資料品質與評估仍是主要工作，而不是一個Trainer取代全部流程。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener"><img src="assets/figures/16.svg" alt="偏好學習驗收：符號與標註：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「偏好學習驗收：符號與標註」讀圖：指出固定reference與可更新policy，檢查相同配對如何進入兩者。再回答：reference也跟著policy更新，還是標準的固定reference DPO嗎？</p></div>

## 自我檢查與解析

**題目：**reference也跟著policy更新，還是標準的固定reference DPO嗎？

<details><summary>展開解析</summary><p>不是這裡定義的目標。同步reference是另一種明確設定的變體，不能在未記錄下改動。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/dpo_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
