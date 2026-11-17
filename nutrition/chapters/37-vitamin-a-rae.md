# 脂溶性維生素A、E、K與RAE

建立脂溶性維生素地圖，實作維生素A的形式限定換算。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/19-fat-soluble-vitamins.svg" target="_blank" rel="noopener" aria-label="放大：脂溶性維生素與吸收條件"><img src="assets/figures/19-fat-soluble-vitamins.svg" alt="脂質相關聚集體作吸收環境概念，維生素來源及原始單位仍需辨識，圖不計算個人可利用率或補充量。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 19｜脂溶性維生素與吸收條件</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先分清脂溶性維生素名稱和圖中的脂質環境，再說明RAE等單位為何需要保留特定來源，不能任意混同一個原始克數。</div>

<p class="health-figure-sources">圖解依據：<a href="https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/">NIH ODS：維生素A</a> · <a href="https://ods.od.nih.gov/factsheets/WYNTK-Consumer/">NIH ODS：補充品須知</a> · <a href="https://ods.od.nih.gov/factsheets/VitaminE-HealthProfessional/">NIH ODS：維生素E</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 功能與來源地圖

維生素A參與視覺和細胞分化，E具有抗氧化相關功能，K參與凝血等蛋白的活化。脂溶性描述溶解與運輸特性，不代表三者功能、儲存或毒性相同。D另有專節，不能把四種全都套同一上限。

## RAE不是單純重量改單位

依NIH資料，1μg RAE可對應1μg視網醇、2μg補充品β-胡蘿蔔素、12μg食物β-胡蘿蔔素，或24μg食物α-胡蘿蔔素／β-隱黃素。先指定形式與來源，再選係數，不能對所有IU使用固定通則。

$$
\mathrm{RAE}_{food\ beta}=\frac{\mu g\ \mathrm{beta\ carotene}}{12}
$$

## 手算一次

1200μg食物β-胡蘿蔔素換算100μg RAE；300μg視網醇為300μg RAE。兩者RAE可在同基準下討論，但美國成人上限中的預成形維生素A範圍不能直接換成所有類胡蘿蔔素總RAE。

## 使用限制

本課換算器把預成形A另存，避免把不同風險範圍混加。食品含量、吸收和個人狀況仍有差異；孕期及藥物背景尤其需專業評估。維生素K與抗凝藥的討論重點是穩定攝取與專業協調，不是自行停食蔬菜。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 19_vitamin_a.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:19_vitamin_a.py -->

## 練習與解答

**請先判斷：** 1200μg食物β-胡蘿蔔素是否等於1200μg視網醇？

<details><summary>展開計算與理由</summary>

不是。前者換算100μg RAE，後者1200μg RAE；形式與來源不能省略，且上限適用範圍仍需另外標記。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：維生素A](https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/)
- [NIH ODS：補充品須知](https://ods.od.nih.gov/factsheets/WYNTK-Consumer/)
- [NIH ODS：維生素E](https://ods.od.nih.gov/factsheets/VitaminE-HealthProfessional/)
- [NIH ODS：維生素K](https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
