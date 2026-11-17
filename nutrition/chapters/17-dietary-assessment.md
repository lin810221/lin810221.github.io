# 飲食評估：回憶、日誌與重複觀察

比較觀察工具的用途，分清部分記錄與習慣攝取。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/09-assessment-reference.svg" target="_blank" rel="noopener" aria-label="放大：飲食觀察與參考值用途"><img src="assets/figures/09-assessment-reference.svg" alt="日曆的已知與未知觀察對照不同參考值用途，未記錄不是零；需要量評估、規劃及上限不可共用同一門檻。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 09｜飲食觀察與參考值用途</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先找日曆中的問號，說明回憶、日誌與重複觀察各可能漏掉什麼，再指出未填不能直接變成零攝取。</div>

<p class="health-figure-sources">圖解依據：<a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a> · <a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/">NIH ODS：鈣</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 常用方法

24小時回憶、食物日誌、秤重紀錄與頻率問卷捕捉不同資訊。回憶有遺漏，記錄可能改變原行為，頻率問卷依賴食品清單與份量假設。沒有一種工具在所有目的都完美，應依個人討論、研究群體或長期模式選擇。

## 重複天的重要性

一天可能不是平常，平日、週末、季節和活動也不同。多日平均減少某些日間波動，卻不自動修正系統漏報或食品配錯。均數、標準差和習慣攝取分布不是同一概念，不能由三天樣本直接得缺乏機率。

## 本課資料

diary.csv是三天虛構部分紀錄，不提供個人熱量目標，也沒有保證餐點完整。加總只代表已記食物；缺測微量營養素保留None，漏記食物無法靠軟體猜回。報告標示這個範圍，避免低小計被解讀為需要更少攝取。

## 與參考值比較

先對齊營養素型態、單位、生命階段、來源範圍與參考種類。NRV用於標示，RDA/AI等有不同評估意義；單日總量與檢驗也不是同一件事。能算百分比不表示已完成個人營養評估。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 09_diary_variation.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:09_diary_variation.py -->

## 練習與解答

**請先判斷：** 紀錄三天平均鈣低於RDA，能否確診缺鈣？

<details><summary>展開計算與理由</summary>

不能。需看資料完整、習慣攝取、適用參考與臨床情況，RDA以下不等於診斷。資料可協助提問與改善紀錄，但不替代完整評估。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)
- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [NIH ODS：鈣](https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
