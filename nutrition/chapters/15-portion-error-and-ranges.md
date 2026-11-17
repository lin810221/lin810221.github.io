# 份量誤差與範圍估計

把不確定寫進結果，理解上下界、可信區間和缺值的差別。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/08-portion-range.svg" target="_blank" rel="noopener" aria-label="放大：份量的範圍，比假精準更有用"><img src="assets/figures/08-portion-range.svg" alt="三個不同碗量代表估計的不確定範圍，不是測得的熱量或體重預測；長時間變化還有身體調節及資料條件。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 08｜份量的範圍，比假精準更有用</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>看三個碗的大小，列出秤重與目測各能減少和保留哪種不確定，說明為何小數很多不代表份量已經準確。</div>

<p class="health-figure-sources">圖解依據：<a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&amp;id=f639057139719594572">TFDA：食品營養標示指引手冊</a> · <a href="https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&amp;pid=12285">國健署：國人膳食營養素參考攝取量第八版</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 誤差來自多個環節

秤重、容器估量、可食部、醬料、烹調吸油和資料庫食品配對都會影響結果。看似精確的總熱量可能只是多個粗估相加。先說你實際量到什麼，不用多位小數掩蓋來源不確定。

## 確定上下界

已知每100g含量x，份量可能a到b，營養素範圍為xa/100到xb/100。多項非負成分可加各界限，但這只是指定範圍的算術，不含機率；相關誤差與未記錄項目也沒有自動被涵蓋。

## 範例

兩食物能量116、80kcal/100g，份量分別120–180、80–120g，範圍203.2–304.8kcal。若另一成分熱量未知，完整總量仍未知，不能只取已知部分叫整餐。程式會保留原因，避免不明缺值變成低熱量假象。

## 解讀方式

一個區間重疊不代表兩餐沒有差異，也不代表有統計顯著；這裡沒有抽樣推論。若真要比較，需要更好的測量、重複資料與適當設計。生活上可先針對最影響估量的大項改善紀錄，而不是追每個微小誤差。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 08_estimation_ranges.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:08_estimation_ranges.py -->

## 練習與解答

**請先判斷：** 把份量範圍算成203–305，能寫成95%信賴區間嗎？

<details><summary>展開計算與理由</summary>

不能，除非另有支持機率意義的資料與統計模型。這是明示假設的確定上下界；不涵蓋未知食品、漏記或參考需要量的不確定。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [TFDA：食品營養標示指引手冊](https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&id=f639057139719594572)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
