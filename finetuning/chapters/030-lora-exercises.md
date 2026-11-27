# LoRA驗收與多adapter管理

用可重現的檢查確認只改了你打算改的部分。

## 必要的數值檢查

檢查初始adapter輸出是否與基底一致、第一次梯度是否符合初始化、訓練後基底是否保持不變，以及保存再載入後logits是否相符。比較需在eval模式與相同dtype下，並清楚設定浮點誤差容許範圍。

故意將target改成不存在的名稱、使用不同基底、漏掉額外輸出頭，再觀察哪些檢查能及早發現。只有「檔案存在」的測試不足以驗證模型成品。

## 多個adapter是部署契約

同一基底可以保存多個任務adapter，但切換、合併或加權組合需要模型與服務支援。請求路由必須記錄adapter版本，避免使用者A的任務意外套到B的設定。不要假設任意兩個adapter相加仍有原本各自的品質。

交付表應包含基底revision、tokenizer、adapter名稱、rank、alpha、target與額外層。若服務將adapter合併，保留原始可回復成品與數值比較；合併後的檔案大小增加，不代表訓練失敗，而是保存形式改變。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener"><img src="assets/figures/10.svg" alt="LoRA驗收與多adapter管理：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「LoRA驗收與多adapter管理」讀圖：從B為零推回初始輸出，說明第一步A與B的梯度差異。再回答：兩個adapter都能單獨運行，是否代表加權混合後不用再評估？</p></div>

## 自我檢查與解析

**題目：**兩個adapter都能單獨運行，是否代表加權混合後不用再評估？

<details><summary>展開解析</summary><p>不代表。權重組合會形成新行為，需要重新檢查格式、品質、遺忘與路由。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/developer_guides/checkpoint)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
