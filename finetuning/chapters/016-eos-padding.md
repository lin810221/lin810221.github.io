# EOS、padding與停止條件

相同token ID可能扮演不同位置角色。

## 何時結束與何處補齊

EOS或回合結束符教模型結束回答；padding則用來把批次補成相同長度。若把所有EOS都從labels移除，模型可能失去學習停止的訊號。若將padding當target，模型又可能因大量容易預測的空位而得到好看的loss。

有些模型把 `pad_token_id` 設成EOS。此時不能只依token值判斷哪些位置要忽略，必須根據真正的 `attention_mask` 與assistant spans。右側padding常用於訓練，批次生成則需依模型要求處理左側padding與位置資訊。

## 以一個短批次核對

取兩筆長短不同的回答，列出 `input_ids`、`attention_mask`、`labels`，逐格確認有效EOS仍受監督，新增padding為忽略值。課程collator用專用pad token，避免示例把兩種概念混在一起；換模型後仍需重做同樣測試。

推論應保存停止token、最大新token數與模板。若答案一直重複角色標頭，先查訓練是否缺結束符、推論是否加錯標頭，及decode是否隱藏了特殊token。不能只靠縮短生成長度掩蓋模板錯誤。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener"><img src="assets/figures/06.svg" alt="EOS、padding與停止條件：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「EOS、padding與停止條件」讀圖：沿文件邊界檢查可見前文與有效labels，說明截斷會刪去哪部分。再回答：PAD與EOS共用ID時，直接把該ID的所有labels設為忽略值會怎樣？</p></div>

## 自我檢查與解析

**題目：**PAD與EOS共用ID時，直接把該ID的所有labels設為忽略值會怎樣？

<details><summary>展開解析</summary><p>會連真正的結束訊號一起刪掉。應以位置遮罩區分有效EOS與批次補齊位置。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/chat_templating)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
