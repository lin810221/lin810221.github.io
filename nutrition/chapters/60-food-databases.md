# 食物成分資料庫：來源、狀態與版本

理解檢驗、標示與調查資料的差異，建立可更新的查詢紀錄。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/30-energy-provenance.svg" target="_blank" rel="noopener" aria-label="放大：從食品狀態到能量重建"><img src="assets/figures/30-energy-provenance.svg" alt="食物資料的生熟與版本連到能量重建，係數、其他成分和修整可影響差異，圖不將差異直接判成錯誤。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 30｜從食品狀態到能量重建</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>指出原始食品的生熟狀態和資料版本，說明同名食物可能需要哪些匹配資訊，才能避免把資料庫數字當固定不變真值。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.mohw.gov.tw/cp-5269-70142-1.html">衛福部：現行包裝食品營養標示修正</a> · <a href="https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&amp;id=f639057139719594572">TFDA：食品營養標示指引手冊</a> · <a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 相同名稱不保證同一筆食物

品種、產地、可食部、生熟、含水量、烹調和品牌都可能改變組成。搜尋到米飯或豆腐後，先核對描述與基準，不因名稱最像就直接取第一筆。產品配方更新也可能使舊標示失去適用性。

## USDA資料類型

FoodData Central的Foundation、FNDDS、Branded與SR Legacy等有不同目的與來源；品牌資料可能來自產品標示，不能一概當目前每包產品的獨立實驗室測值。跨資料類型比較需保留來源和時間。

## 缺值與真實零

數值0、缺資料、低於界限與不適用需要區分。匯出時可用空白加狀態欄，而非CSV空格默認0。本課虛構食物明示synthetic，避免讓同學誤以為是國健署或USDA的真實資料。

## 可重現查核紀錄

保留資料ID、版本、取得日期、描述、基準、單位和處理方法；改值要能追溯。完整專題用SHA-256記錄資料檔案身份，雜湊證明檔案是否改變，不保證內容的營養真實性或臨床適用性。

## 選兩筆看似相同資料

甲資料是生豆每100g，乙是水煮豆每100g；若直接比較，水分和準備差異會影響濃度。丙資料又是品牌罐頭含鹽版本，不能只因名稱同豆類就混當同一食品。先保留原描述和資料類型，再決定是否可換算、需哪些產率或配方；資料不相容時，清楚說無法直接比較比強行平均更有意義。

更新同一資料ID時仍要比對版本；來源保留舊ID不保證內容未改，雜湊與取得日期可輔助追溯差異。

## 練習與解答

**請先判斷：** Branded資料是否一定是本日獨立實測，空值是否可補0？

<details><summary>展開計算與理由</summary>

兩者都不是。先看來源及更新，空值保留未知；資料類型與缺值規則需要明示。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [國健署：國人膳食營養素參考攝取量第八版](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&pid=12285)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
