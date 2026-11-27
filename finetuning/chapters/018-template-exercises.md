# 模板稽核練習：逐格追蹤token

把監督位置變成可看的表格與可重跑的測試。

## 建立四筆最小測試

準備單輪、多輪、長回答及特殊符號四筆對話。每筆印出模板文字、token、角色mask、attention mask與最終labels，標示哪個logit對應哪個target。答案不只填一個loss數字，而是能解釋每個有效位置的來源。

故意移除模板的 `generation` 區塊，確認assistant-only檢查能發現空監督；再把長度上限縮到只剩user，確認會中止。若工具靜默退回全序列監督，也應由測試發現，而非當作正常結果接受。

## 在修改前後比較契約

更換tokenizer、template或特殊token都算資料處理變更。保存一份固定樣本的期望token及mask，更新後比較差異，再決定是否需要新資料版本與重新訓練。不要因為能載入checkpoint就假設輸入格式沒有變。

本章完成後，你應能解釋訓練為何需要assistant答案、推論為何停在回答起點，以及停止token為何需要監督。這些檢查適用完整微調、LoRA與DPO，不因只訓練少量參數而省略。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener"><img src="assets/figures/06.svg" alt="模板稽核練習：逐格追蹤token：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「模板稽核練習：逐格追蹤token」讀圖：沿文件邊界檢查可見前文與有效labels，說明截斷會刪去哪部分。再回答：把模型loss與手寫loss比對相同，是否已證明模板正確？</p></div>

## 自我檢查與解析

**題目：**把模型loss與手寫loss比對相同，是否已證明模板正確？

<details><summary>展開解析</summary><p>尚未。兩者可能共用同一組錯標籤；還需人工核對角色、答案範圍、EOS與截斷邊界。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/chat_templating)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
