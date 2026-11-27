# 選擇target modules與可訓練層

目標名稱依架構而變，不能複製一組通用縮寫。

## 從實際模型列出模組

本課小Llama以 `q_proj` 與 `v_proj` 作為清楚的最小示例。其他模型可能使用合併QKV、不同命名或MoE參數；先列出 `named_modules()` 與權重形狀，再決定target。某個設定能在一種架構載入，不代表適用全部模型。

只改attention與同時修改MLP具有不同容量與資源成本。`target_modules='all-linear'` 也應核對版本對輸出頭等特殊層的處理。不要在不知情下把輸出頭、embedding或不相容量化層一起改動。

## 附加參數也要交付

新增token或分類頭時，可能需要訓練並保存額外層，例如 `modules_to_save`；這些權重會增加成品與最佳化器狀態。若只儲存LoRA矩陣而漏掉新頭，重新載入後的行為就不完整。

列出可訓練參數總數、各類模組數與adapter名稱，加入實驗manifest。若找不到任何target，應中止並顯示模組清單，而非靜默改成完整微調。以固定批次比較初始logits，也能發現意外更動。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener"><img src="assets/figures/09.svg" alt="選擇target modules與可訓練層：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「選擇target modules與可訓練層」讀圖：逐一核對A、B與基底形狀，數出哪些格子可以更新。再回答：別人的模型使用c_attn，本模型找不到，應怎麼辦？</p></div>

## 自我檢查與解析

**題目：**別人的模型使用c_attn，本模型找不到，應怎麼辦？

<details><summary>展開解析</summary><p>檢查本模型的實際模組與形狀，重新選target並驗證參數數量；不能只改名字直到程式不報錯。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/package_reference/lora)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
