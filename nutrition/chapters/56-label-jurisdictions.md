# 台灣與其他地區標示：規則不能混用

對照現行台灣規範與國際名稱，標示生效日和適用食品。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/28-label-serving.svg" target="_blank" rel="noopener" aria-label="放大：一份、一包與每100的關係"><img src="assets/figures/28-label-serving.svg" alt="包裝與標示並列，先找每份大小與包裝份數，再核對每100基準及地區規則，不把不同制度視為相同門檻。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 28｜一份、一包與每100的關係</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>在標示頁上標出地區規則的位置，解釋為何看到相同單位仍須核對修整、欄位及制度，不能任意混套台灣和其他地區。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.mohw.gov.tw/cp-5269-70142-1.html">衛福部：現行包裝食品營養標示修正</a> · <a href="https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&amp;id=f639057139719594572">TFDA：食品營養標示指引手冊</a> · <a href="https://www.fda.gov.tw/TC/includes/GetFile.ashx?id=f639251744443617765">TFDA：四歲以上每日參考值</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 本課台灣基線

一般包裝食品營養標示採2022-06-23修正、2024-07-01施行的規範作查核基線；不是網站更新到2026就把生效日改成2026。2026-11-09重新查核後仍應保留原始公告與適用範圍。

## 必要欄位與格式

一般欄位包含能量、蛋白質、脂肪、飽和脂肪、反式脂肪、碳水化合物、糖與鈉。格式有每份搭配每100g／mL，或搭配每日參考值百分比等條件；特定產品另有要求，不能一張示意圖覆蓋所有食品。

## 國際名稱不完全同義

美國DV、台灣每日參考值、DRIs中的RDA等，在用途、分母與欄位上可能不同。美國添加糖欄也不能直接當台灣總糖；遇到海外產品，先標地區和規則，再比較相同概念。

## 課堂審核表

列食品種類、地區、規範版本、生效日、每份量與比較基準；若來源是預告草案，清楚寫草案並不取代正式規範。教材不以美國熱量計算或修整規則裁定台灣產品是否合法。

## 地區欄位的資料設計

可將一筆標示記為jurisdiction、rule_version、effective_date、food_category、serving_size和nutrient_definition。若讀入美國添加糖，不把欄名改台灣總糖直接接入；先建立定義對照並保留原欄。相同數字、不同定義仍是不同資料，清楚的欄位可防止跨國比較時無聲換概念。

## 練習與解答

**請先判斷：** 一篇2026新聞介紹草案，能否直接改寫成所有產品已適用？

<details><summary>展開計算與理由</summary>

不能。要核對是否正式公告、生效日與食品範圍；較新新聞不等於較新有效法規。

</details>

## 官方參考與跨課閱讀

- [衛福部：現行包裝食品營養標示修正](https://www.mohw.gov.tw/cp-5269-70142-1.html)
- [TFDA：食品營養標示指引手冊](https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&id=f639057139719594572)
- [TFDA：四歲以上每日參考值](https://www.fda.gov.tw/TC/includes/GetFile.ashx?id=f639251744443617765)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
