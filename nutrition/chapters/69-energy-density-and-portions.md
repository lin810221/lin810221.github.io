# 等能量份量與能量密度：一個維度的控制

觀察不同食物的份量差，不把等能量當成等飽足或等健康。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/35-density-habit.svg" target="_blank" rel="noopener" aria-label="放大：等能量份量與日常選擇情境"><img src="assets/figures/35-density-habit.svg" alt="大小不同的食物作能量密度概念，不提供真實等量換算；等能量只固定一個維度，習慣還受環境與機會影響。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 35｜等能量份量與日常選擇情境</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出圖是假想等能量條件，再列體積、營養及飽足中仍可能不同的部分，不把一個維度的控制當完整健康判斷。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/fact-sheets/detail/healthy-diet">WHO健康飲食：2026更新</a> · <a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://www.mohw.gov.tw/cp-2704-41108-1.html">衛福部：我的餐盤</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 同能量不同重量

水分、纖維、脂肪與其他成分影響能量密度。90kcal可能對應示例油10g或堅果約15.25g，另一種含水食物則需不同重量。這描述算術，不是說誰必然讓每位讀者更飽。

## 如何求份量

指定參考能量E和食物每100基準e，以E÷e×100求所需g或mL。e必須正，不能以零能量食品求正能量等值，也不能缺密度就混合g與mL。

## 組合食物的比較

若換掉的不只是單一食物，需把整份組合的營養與份量重新算。等能量控制了總量一項，蛋白質、纖維、微量營養、口感與價格仍不同；不應把算出的克數包裝成每日建議。

## 行為與生理不直接外推

研究食物體積或密度時，要看實驗條件、自由攝取與持續時間。短期飽足評分與長期攝取或健康結果並不相同。本課工具只協助把比較條件表達清楚。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 35_isoenergy_portion.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:35_isoenergy_portion.py -->

## 練習與解答

**請先判斷：** 兩份等能量食物是否保證同樣飽足？

<details><summary>展開計算與理由</summary>

不保證。食物基質、組成、體積、情境和個體差異都影響；等能量只固定一個比較條件。

</details>

## 官方參考與跨課閱讀

- [WHO健康飲食：2026更新](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)
- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
