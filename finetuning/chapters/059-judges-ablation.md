# 模型judge、人工複核與消融

讓評分器的偏差也成為檢查對象。

## Judge不是自動真相

LLM judge可能受回答長度、位置、文風與自身家族偏好影響。使用固定rubric，盲化模型名稱，交換候選順序並保留平手；對重要或高分歧案例做人工複核。保存judge模型revision、提示與解析規則。

若judge與訓練教師相同，更需獨立檢查是否只是偏好一致。事實問題應核對可靠來源，格式問題用程式驗證，不能把所有可檢查事項都交給一句「請評分」。

## 消融需要控制比較條件

比較完整微調、LoRA與QLoRA時，列出模型、資料、模板、曝光token、可訓練參數、搜尋預算及硬體。rank、alpha、target與學習率一起變動，無法只歸因於rank。資源不等時可做成本限制下比較，但明確命名問題。

先保存合理提示基準，再比較候選，報告多個種子與關鍵切片。若差異小於評分不確定性，結論可以是尚無足夠證據；這比只挑最好一次結果更有用。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/20.svg" target="_blank" rel="noopener"><img src="assets/figures/20.svg" alt="模型judge、人工複核與消融：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「模型judge、人工複核與消融」讀圖：比較總體與重要切片，指出哪些分母與錯誤類型不能省略。再回答：judge偏愛較長回答，如何發現與處理？</p></div>

## 自我檢查與解析

**題目：**judge偏愛較長回答，如何發現與處理？

<details><summary>展開解析</summary><p>建立內容相近但長度不同的控制案例、交換順序、分長度切片並人工複核；修改rubric後重跑基準與候選。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
