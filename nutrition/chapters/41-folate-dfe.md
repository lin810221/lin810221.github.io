# 葉酸、DFE與來源限定的上限

實作食物葉酸與folic acid換算，避免把DFE當所有上限的分子。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/21-vitamin-sources.svg" target="_blank" rel="noopener" aria-label="放大：維生素來源、當量與評估"><img src="assets/figures/21-vitamin-sources.svg" alt="天然食物、強化和補充來源並列，提醒當量換算與上限的來源範圍不同；食物處理及狀態評估需另有資料。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 21｜維生素來源、當量與評估</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先用三個來源分清原始葉酸形式與DFE，再說明比較指定來源的上限時，為何不能把當量值直接當原始folic acid量。</div>

<p class="health-figure-sources">圖解依據：<a href="https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/">NIH ODS：葉酸與DFE</a> · <a href="https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/">NIH ODS：維生素B12</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 先標化學形式

食物天然folate與強化或補充品中的folic acid有不同利用背景。DFE是膳食葉酸當量，不是所有葉酸型態的原始重量；先記形式、來源和是否隨餐，再談換算。

## 三個換算條件

1μg DFE對應1μg食物葉酸、0.6μg隨餐folic acid，或0.5μg空腹folic acid。因此240μg隨餐folic acid約為400μg DFE；課程不替未建立通用轉換的5-MTHF自行發明係數。

$$
\mathrm{DFE}_{with\ food}=\frac{\mu g\ \mathrm{folic\ acid}}{0.6}
$$

## 上限分子不同

美國19歲以上的1000μg UL針對補充與強化來源的folic acid，不是所有天然食物葉酸，也不是把DFE直接相加後對照1000。範例保留原始folic acid重量與來源限定，防止換算後失去風險判讀的範圍。

## 生命階段的應用

備孕與孕期的規劃涉及時間、適用指南、疾病與藥物背景。此單元教會讀形式和計算；特殊高風險情況不從一般參考值自動推導補充劑量。另一個重要問題是葉酸與B12狀態的臨床評估，不能用單一補充品掩蓋原因。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 21_folate.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:21_folate.py -->

## 練習與解答

**請先判斷：** 240μg隨餐folic acid為400μg DFE，做上述美國UL比較時應用哪個數字？

<details><summary>展開計算與理由</summary>

用適用來源的原始folic acid 240μg，不把400μg DFE直接當同一分子；還要確認年齡與其他強化／補充來源。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：葉酸與DFE](https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/)
- [NIH ODS：維生素B12](https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
