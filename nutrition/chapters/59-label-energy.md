# 從營養素重建熱量：為何不一定完全相等

檢查醣類、纖維與係數，不用簡化算式作合規認證。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/30-energy-provenance.svg" target="_blank" rel="noopener" aria-label="放大：從食品狀態到能量重建"><img src="assets/figures/30-energy-provenance.svg" alt="食物資料的生熟與版本連到能量重建，係數、其他成分和修整可影響差異，圖不將差異直接判成錯誤。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 30｜從食品狀態到能量重建</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>由左側原始成分追到能量重建，列兩個可能影響差異的條件，說明不能只用4／4／9算出的數字強迫完全等於標示。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.mohw.gov.tw/cp-5269-70142-1.html">衛福部：現行包裝食品營養標示修正</a> · <a href="https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&amp;id=f639057139719594572">TFDA：食品營養標示指引手冊</a> · <a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 4／4／9的條件

蛋白質4、可利用碳水4、脂肪9是常用教學係數；纖維、糖醇、酒精、有機酸等可能需要另外處理。若資料中的碳水已含纖維，又將纖維能量再加一次，就會重複計算。

## 本課欄位的定義

available_carb_g明示為排除纖維的可利用碳水；fiber_g另列，纖維係數是示範選項而非每一產品實際值。原始標示若只寫碳水，需先確認定義和地區規則，不能直接改欄名接進函式。

## 差值如何處理

示例豆飲每100mL標示能量42kcal，而選定係數重建38.2kcal；差3.8不是證明違法，也不能全都說一定是四捨五入。要檢查資料定義、成分、方法與修整；虛構資料本就沒有真實產品合規主張。

## 合理的結論

報原值、重建值、差值和係數假設，列待查欄位。這能發現單位、份量或重複計算問題；法律容許誤差與判定程序則查適用規範，不能由本課簡化模型自動給綠燈。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 30_label_energy_check.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:30_label_energy_check.py -->

## 練習與解答

**請先判斷：** 重建熱量差一點，是否足以認定廠商錯標？

<details><summary>展開計算與理由</summary>

不足。需查定義、係數、成分、修整及適用法規與檢測；本課算式只用於資料一致性探索。

</details>

## 官方參考與跨課閱讀

- [衛福部：現行包裝食品營養標示修正](https://www.mohw.gov.tw/cp-5269-70142-1.html)
- [TFDA：食品營養標示指引手冊](https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&id=f639057139719594572)
- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
