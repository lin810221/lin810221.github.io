# 飲食日誌：紀錄完整性比小數位更重要

辨認部分紀錄、缺值與日間變異，避免偽造完整一天。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/33-diary-uncertainty.svg" target="_blank" rel="noopener" aria-label="放大：日誌完整性與不確定範圍"><img src="assets/figures/33-diary-uncertainty.svg" alt="日曆有紀錄與未知格，份量和資料來源誤差需另列；缺漏不是零，也不能以小數位消除未量到的資訊。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 33｜日誌完整性與不確定範圍</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>找出問號格，分開「確定沒吃」與「沒有紀錄」，再說明有效天數和排定天數為何不能在平均中任意互換。</div>

<p class="health-figure-sources">圖解依據：<a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a> · <a href="https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&amp;pid=12285">國健署：國人膳食營養素參考攝取量第八版</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 本課日誌的範圍

diary.csv是三天的部分食物觀察，不是完整菜單、減重方案或能量目標。標題、報告和圖都會重複標明partial observations；不能把這些小計當讀者應達成的日量。

## 需要記的欄位

日期、時段、食物ID、實際量、單位、準備狀態、估計方法和未記項目。隱藏油、醬料、飲料與補充品可能造成系統性漏記，計算到小數第二位也不會消除這種偏誤。

## 每項營養有自己的完整性

某天能量已知不代表鈣或D也完整。範例第三天加入某些微量營養未知的飲料，因此完整總量為未知並保留已知小計。這是刻意安排的資料行為測試，不是說飲料真實沒有這些營養素。

## 平均值的限制

三個部分日量的平均不是習慣攝取，不能對照RDA就判不足率；日間變異、季節、週末與記錄方式都影響估計。先描述觀察範圍和品質，再決定是否需更多資料。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 33_diary_missingness.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:33_diary_missingness.py -->

## 練習與解答

**請先判斷：** 日誌圖有三根柱，是否代表三天完整能量需要？

<details><summary>展開計算與理由</summary>

不是。它是已記錄部分食物的小計；柱高既不等於需要量，也未證明完整攝取。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)
- [國健署：國人膳食營養素參考攝取量第八版](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&pid=12285)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
