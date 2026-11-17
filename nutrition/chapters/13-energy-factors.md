# 食物能量與4／4／9：什麼時候可以用

用明示係數計算能量，分清可利用碳水、纖維與標示值。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/07-energy-factors.svg" target="_blank" rel="noopener" aria-label="放大：能量係數與支出不是同一張表"><img src="assets/figures/07-energy-factors.svg" alt="常用4、4、9係數估算三大營養素來源能量；不同成分、制度與人體支出有各自條件，不能直接當個人需要量。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 07｜能量係數與支出不是同一張表</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先讀清三欄共同單位，說出這些係數乘的是哪種克數，再指出纖維等成分或制度不同時為何需回查適用規則。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&amp;id=f639057139719594572">TFDA：食品營養標示指引手冊</a> · <a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=4248&amp;pid=12285">國健署：國人膳食營養素參考攝取量第八版</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 常用生理能量係數

蛋白質與一般可利用碳水常用4kcal/g，脂肪9，酒精7。它們是常用估算係數，不是所有食品分子測量值都完全一樣。纖維、糖醇與有機酸等還有其他處理方式，實際標示應依適用法規與資料。

$$
E=4C_{available}+4P+9F+k_{fiber}D+7A
$$

## 避免雙算

本式C已排除纖維，D另列；若某來源總碳水包含纖維，需先對齊再代入。飽和脂肪包含在F、糖包含在C，不另加一次。未知成分不硬補0，也不能拿此簡化式直接認證包裝能量合法。

## 算例

C=50g、P=20g、F=10g、D=5g，纖維係數選2、酒精0，得200+80+90+10=380kcal，約1589.92kJ。更換纖維係數會改數值，所以報告要保留採用方法，不能只留最終總熱量。

## 標示差異怎麼看

四捨五入、特定係數和成分計算可使標示能量不等於標示宏量值直接4/4/9。發現差異先核對單位、子項、方法和版本，不立即判廠商造假；也不能無限制把所有不符都歸於四捨五入。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 07_energy_factors.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:07_energy_factors.py -->

## 練習與解答

**請先判斷：** 脂肪10g含飽和3g，能否算9×(10+3)？

<details><summary>展開計算與理由</summary>

不行，飽和是脂肪子集合，總脂肪10g已包含3g；能量應按整體F計一次。相同原則適用糖和總碳水。

</details>

## 官方參考與跨課閱讀

- [TFDA：食品營養標示指引手冊](https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&id=f639057139719594572)
- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
