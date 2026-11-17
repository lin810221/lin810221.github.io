# 營養證據：機制、相關與因果

理解研究能回答什麼，為之後保健宣稱與飲食型態建立判讀方法。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/02-evidence-structure.svg" target="_blank" rel="noopener" aria-label="放大：觀察到關係，還要找替代解釋"><img src="assets/figures/02-evidence-structure.svg" alt="飲食和結果之間有觀察關係，其他因素可能同時影響兩者；箭頭表示待檢驗的可能路徑，不宣告因果。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 02｜觀察到關係，還要找替代解釋</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先找飲食與結果，再沿紫色箭頭說一個可能的共同原因；解釋為何同時出現還不能直接證明飲食造成全部差異。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cochrane.org/evidence">Cochrane：健康證據與白話摘要</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a> · <a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 不同證據的用途

機制研究說明可能如何作用，觀察研究探索長期關係，隨機試驗比較特定介入。每種設計有優勢與限制，不能因有細胞機制就宣稱食用某劑量能降低人體疾病；也不能因觀察相關不完美就忽略所有長期證據。

## 營養研究的特殊問題

食物互相替代，增加某來源常減少另一來源；總能量、社經、活動與其他習慣可能混淆。攝取量有回憶、份量與資料庫誤差，長期依從性也難。必須問「相對什麼替代」與實際量測，而不是只看某成分的單一係數。

## 結果與研究對象

血中指標改善與疾病/生活品質結果不同；健康成人、運動員、孕婦與病人不可任意外推。效果大小、追蹤時間、不良事件與不確定性都應列。p值不等於效果重要，也不證明沒有偏誤。

## 可查證紀錄

為每項數字保留來源、日期、地區、族群、單位與用途。範例將標示NRV和食物觀測分開，避免更新一張表卻無聲改掉整份分析。完整統計推論可跨讀[應用統計](../applied-statistics/index.html)，這裡先學必要判讀。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 02_source_and_reference.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:02_source_and_reference.py -->

## 練習與解答

**請先判斷：** 一篇研究顯示吃某食物的人較健康，能否證明食物本身造成效果？

<details><summary>展開計算與理由</summary>

不一定。還需處理其他習慣、選擇、測量與反向因果；看設計、替代品、劑量和族群，再與整體證據比較。單篇相關不能直接升格全民處方。

</details>

## 官方參考與跨課閱讀

- [Cochrane：健康證據與白話摘要](https://www.cochrane.org/evidence)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
