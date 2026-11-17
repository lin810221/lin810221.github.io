# 保存期限、開封與紀錄的不確定

把包裝日期放回實際保存條件，不把期限當獨立保證。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/45-cold-chain-history.svg" target="_blank" rel="noopener" aria-label="放大：保存日期與冷鏈歷史"><img src="assets/figures/45-cold-chain-history.svg" alt="從製備運送保存到食用的時間軸，任何未取得條件都保留未知；日期、開封及特定族群情境不可互相代替。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 45｜保存日期與冷鏈歷史</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿時間軸標出開封、保存及離開冷藏的可能未知段，說明保存日期為何不能自動保證任何處理條件下都安全。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/publications/i/item/9789241594639">WHO：食品安全五要點手冊</a> · <a href="https://www.cdc.gov/food-safety/prevention/index.html">CDC：預防食物中毒</a> · <a href="https://www.who.int/news-room/fact-sheets/detail/food-safety">WHO：食品安全</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 期限有前提

產品期限依指定包裝、保存和使用條件建立；開封、溫度失控或污染可能改變情況。日期名稱與法律意義也隨地區與產品不同，不能把國外best before字義一律套到台灣所有標示。

## 開封後重新記錄

記開封時間、保存方式、器具接觸與產品說明；若標示要求冷藏或限時使用，不能只看外盒未開封期限。冰箱設定溫度與實際各位置溫度也可能不同，需適當觀察。

## 缺漏資料怎麼辦

不知道曾在室溫放多久，不能填0分鐘；不知溫度也不填理想冷藏值。範例用unknown顯示缺項，拒絕輸出「可安全保存X天」；模型沒有食物種類與完整微生物參數，不能假裝有預測能力。

## 採買到食用的可行安排

按實際使用量分裝、避免反覆開封和交叉接觸、先使用較早開封的合適產品。這些安排還要符合食品與保存條件；若有召回或明顯異常，按官方處理而非嘗試用計算器證明可以食用。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 45_storage_uncertainty.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:45_storage_uncertainty.py -->

## 練習與解答

**請先判斷：** 不知室溫時間，為了完成表格填0是否合理？

<details><summary>展開計算與理由</summary>

不合理。0表示沒有暴露，與未知不同；應保留缺項並查實際條件，不以假設資料提供安全保證。

</details>

## 官方參考與跨課閱讀

- [WHO：食品安全五要點手冊](https://www.who.int/publications/i/item/9789241594639)
- [CDC：預防食物中毒](https://www.cdc.gov/food-safety/prevention/index.html)
- [WHO：食品安全](https://www.who.int/news-room/fact-sheets/detail/food-safety)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
