# 運動營養：強度、時間與飲食背景

先建立活動情境，再理解能量、醣、蛋白質、水分與電解質。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/36-activity-recovery.svg" target="_blank" rel="noopener" aria-label="放大：活動、飲食供應與恢復支持"><img src="assets/figures/36-activity-recovery.svg" alt="食物供應與活動需求、恢復及生活支持相連，圖不計算個人低能量可用性或用單一症狀判定病況。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 36｜活動、飲食供應與恢復支持</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先說活動強度、時間與背景可能改變哪些需求，再指出食物來源圖不能直接給每個人的運動營養劑量或補充方案。</div>

<p class="health-figure-sources">圖解依據：<a href="https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/">NIH ODS：運動表現與補充品</a> · <a href="https://ods.od.nih.gov/factsheets/WYNTK-Consumer/">NIH ODS：補充品須知</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 運動不是一種固定情境

散步、短時間阻力訓練、長時間耐力或高溫活動，需求與限制不同。一般成人、競技運動者與有疾病者不能套同一補給表；研究對象與訓練型態要先標清楚。

## 優先記錄的資訊

活動種類、開始時間、持續時間、強度、環境、進食與飲水、腸胃耐受及恢復感受。範例回傳這些欄位與缺項，不由一個運動分鐘數產生精確能量消耗或自動補充劑量。

## 食物基礎與產品

足夠能量、合適醣類與蛋白來源、液體及微量營養是基本條件。運動飲料、蛋白粉與一般飲料用途不同，不因有sport字樣就人人需要。補充品研究常限特定訓練族群，不能全面外推。

## 實務決策

先看是否有足夠的普通食物與可行時程，再討論便利產品；若長時間、高溫、反覆賽程或有健康背景，查適用指南與專業支持。競賽者還需確認禁用物質和產品污染風險，品質驗證也不等於保證成效。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 36_sports_record.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:36_sports_record.py -->

## 練習與解答

**請先判斷：** 一般短時間活動能否直接照搬菁英耐力賽補給計畫？

<details><summary>展開計算與理由</summary>

不應。活動時間、強度、環境、訓練和健康背景不同，需先確認情境與實際需要。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：運動表現與補充品](https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/)
- [NIH ODS：補充品須知](https://ods.od.nih.gov/factsheets/WYNTK-Consumer/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
