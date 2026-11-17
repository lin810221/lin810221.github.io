# 學習路線、指南版本與範例環境

從零安排閱讀，明確標示本課的正式基線、虛構資料與可驗證範圍。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/03-units-food-record.svg" target="_blank" rel="noopener" aria-label="放大：先把食物與分母連起來"><img src="assets/figures/03-units-food-record.svg" alt="可食重量接到帶有每100克或每份定義的食品資料，單位與版本需要同時保存，圖不預測吸收或需要量。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 03｜先把食物與分母連起來</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿圖從實際食物到資料版本，列出開始學習時先要確認的兩項條件，說明更新日期不能代替食品與數據定義。</div>

<p class="health-figure-sources">圖解依據：<a href="https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/">NIH ODS：維生素D</a> · <a href="https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/">NIH ODS：維生素A</a> · <a href="https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&amp;id=f639057139719594572">TFDA：食品營養標示指引手冊</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 三條入口

完整路線依十六章順序；想先看生活應用，可讀食物類別、標示與外食，再回補消化和營養素；偏資料者可先跑單位、份量、缺值與報告。每章六單元，章內編號重新從01開始，穩定網址與筆記獨立保存。

## 本次查核基線

2026-11-09：台灣DRIs以官方仍列的第八版；一般包裝食品標示以2022修正、2024-07-01生效版為主，營養宣稱另有2024修正及部分2026生效條款。WHO2026健康飲食頁和其正式專題指南，NIH單位/補充品資料作補充，來源地區不混用。

## 執行方式

主要實測Python3.15.2，標準函式庫不需pip套件或API金鑰。網頁可離線讀，資料檔的食物與三天紀錄均為虛構、且非完整菜單。實作只驗算術與資料契約，不將指南比較產生為個人診斷、補充量或標示合法性認證。

```powershell
cd nutrition/examples
py -3.15 01_first_food_record.py
py -3.15 -m unittest discover -s . -p test_examples.py -v
py -3.15 48_complete_report.py --output my-nutrition-report
```

## 更新不是換日期

新增指南先確認正式發布與生效，草案另標；網站更新日不必等於規範生效日。更新來源、範例、測試與ZIP後重新編譯，舊課日期只代表當時查核狀態。這種版本習慣對健康資訊尤其重要。

## 練習與解答

**請先判斷：** 第九版草案較新，是否應直接取代正式第八版所有表？

<details><summary>展開計算與理由</summary>

不能只因草案年份新就當有效標準。先查正式發布、適用範圍和生效，草案可介紹變更方向，但主線及計算參考仍標明當次實際採用的正式版本。

</details>

## 官方參考與跨課閱讀

- [國健署：國人膳食營養素參考攝取量第八版](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&pid=12285)
- [衛福部：現行包裝食品營養標示修正](https://www.mohw.gov.tw/cp-5269-70142-1.html)
- [衛福部：營養宣稱修正](https://www.mohw.gov.tw/cp-2704-77719-1.html)
- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
