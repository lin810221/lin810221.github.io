# 一餐的營養加總：已知小計與未知

建立可靠的食物向量加總，同一餐的各營養素可能有不同完整性。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/31-meal-observation.svg" target="_blank" rel="noopener" aria-label="放大：一餐的可見來源與未知項目"><img src="assets/figures/31-meal-observation.svg" alt="餐盤旁列食品重量、醬料油飲料及外食資料，已知小計與完整總量不同；視覺盤子不保證觀察完整。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 31｜一餐的可見來源與未知項目</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指盤上看得到的食物，再列盤外可能缺的成分，說明加總已知項為何不能自動叫做整餐完整營養量。</div>

<p class="health-figure-sources">圖解依據：<a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://www.mohw.gov.tw/cp-2704-41108-1.html">衛福部：我的餐盤</a> · <a href="https://www.mohw.gov.tw/cp-5269-70142-1.html">衛福部：現行包裝食品營養標示修正</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 從單項到一餐

每個食物先依實際量換算，再按相同營養素和單位相加。示例穀物150g蛋白3.9g、豆腐150g蛋白12g，加蔬菜150g蛋白3g，已知總量18.9g；不能把食物重量直接當營養素重量。

## 缺一項如何輸出

如果豆腐D未知，即使其餘兩項D都有值，整餐D也不能叫完整已知總量。輸出 `amount=None` 、known_subtotal和missing_foods，讓人看見可用線索與缺口；未知不是營養不存在。

## 零份量的特殊情況

完全沒吃某食物時，該項貢獻是0，無需因未食用食物某欄未知污染整餐。反過來只要吃了正量，未知就需傳播。這個邊界是資料邏輯，不是生理吸收模型。

## 防止重複計算

混合菜若已用成品資料，不再把同一份油和原料全加一次；若用食譜拆解，就不要另加整道菜。資料記錄保留方法欄，讓查核者知道分量如何分配和哪些成分未能觀察。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 31_meal_aggregation.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:31_meal_aggregation.py -->

## 練習與解答

**請先判斷：** 一項食物維生素D未知，能否以其他食物D小計當完整總量？

<details><summary>展開計算與理由</summary>

不能。應標完整總量未知，另提供已知小計和缺值食物；只有未食用的零份量不造成貢獻未知。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [衛福部：我的餐盤](https://www.mohw.gov.tw/cp-2704-41108-1.html)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
