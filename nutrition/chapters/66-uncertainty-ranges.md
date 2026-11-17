# 份量與資料誤差：用範圍而非假精準

區分情境界限、量測誤差與統計信賴區間。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/33-diary-uncertainty.svg" target="_blank" rel="noopener" aria-label="放大：日誌完整性與不確定範圍"><img src="assets/figures/33-diary-uncertainty.svg" alt="日曆有紀錄與未知格，份量和資料來源誤差需另列；缺漏不是零，也不能以小數位消除未量到的資訊。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 33｜日誌完整性與不確定範圍</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>在有紀錄格旁畫份量上下範圍，指出它和未記錄是不同不確定來源，不能用補一個平均值宣稱全都量到了。</div>

<p class="health-figure-sources">圖解依據：<a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a> · <a href="https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&amp;pid=12285">國健署：國人膳食營養素參考攝取量第八版</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 不確定來自哪裡

份量估計、食物資料差異、準備方式、回憶漏記與營養素缺值是不同來源。把它們全部包成±10%沒有依據；應先記每一假設，再選能支持的方法。

## 簡單範圍計算

若某食物每100g能量116kcal、估計120至180g，能量情境為139.2至208.8kcal。另一項80kcal/100g、80至120g為64至96kcal，非負加總得203.2至304.8kcal。

## 界限不是機率

這個範圍只表示輸入上下界下的算術，不含95%涵蓋或中間值最可能的意思。若資料值本身也不確定，或份量誤差互相關聯，需要其他假設；不可把端點加總自動標成信賴區間。

## 未知仍是未知

沒有某營養素的值，不能靠份量上下界解出完整總量。工具回未知並列待查來源，避免把「有區間」當所有不確定已處理。報告應清楚寫是情境範圍與已忽略哪些誤差。

## 界限變寬代表什麼

同樣116kcal/100g食物，重量若已稱為150g，僅由這個模型算174kcal；若只估100至200g，界限就是116至232kcal。資訊較少使情境更寬，不表示真實值一定在中點，也不含資料庫本身誤差。若漏記一份醬料，擴大原食物份量界限不會自動補回那個系統性缺漏；應分開記錄漏項與估計誤差，再解釋分析仍缺什麼。

對兩項份量同時取下界或上界，還假設這些端點可共同發生；若有共同總重限制，需把限制寫入模型。若改用模擬，也要說明抽樣分布與相關，不能只因跑很多次就說結果為95%保證。

## 練習與解答

**請先判斷：** 203.2至304.8kcal能否直接稱95%信賴區間？

<details><summary>展開計算與理由</summary>

不能。它是指定輸入界限的情境加總，沒有抽樣分布或機率模型；要作統計區間需額外方法與假設。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [Cochrane：健康證據與白話摘要](https://www.cochrane.org/evidence)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
