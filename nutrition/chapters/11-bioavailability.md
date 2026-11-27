# 生物可利用率與食物基質

分清含量、吸收和利用，理解同餐、加工與個體差異。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/06-food-matrix.svg" target="_blank" rel="noopener" aria-label="放大：食物基質與腸道條件"><img src="assets/figures/06-food-matrix.svg" alt="營養成分被包在食物結構中，加工搭配及腸道條件影響釋出與利用；不把所有吸收效率設成固定比例。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 06｜食物基質與腸道條件</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出基質內的成分與外層結構，再列兩項可能改變釋出或吸收的條件，說明圖不能直接給個人利用率百分比。</div>

<p class="health-figure-sources">圖解依據：<a href="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/">NIH ODS：鐵</a> · <a href="https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works">NIDDK：消化系統如何運作</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 含量不是唯一資訊

食物基質包括結構、纖維、其他成分與加工狀態，會影響消化和可得性。某營養素含量高，不代表個人實際吸收一定同比高；反過來也不能因吸收率較低就將整種食物判成沒有價值。

## 交互作用的例子

維生素C可促進非血基質鐵吸收，某些食物成分與同餐條件也會影響；脂溶性維生素處理與脂肪/消化系統有關。這些方向不等於可用一個固定百分比對每個人預測。研究條件和是否缺乏都重要。

## 不濫用吸收係數

範例假設10mg、吸收比例.1–.3，只得到模型範圍1–3mg，比例明示虛構。DRIs的攝取參考通常已含體系的相關假設，不能先把攝取乘吸收率，再直接和攝取RDA比而重複調整。

## 機制與飲食決策

加工有時增加可利用、有時造成損失，也可能改善安全、便利與可得性。不要把生食、天然、未加工一律當較好；需要看食品、營養素和族群。課程使用具體案例與來源，而不是給所有食物同一個折損係數。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 06_absorption_uncertainty.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:06_absorption_uncertainty.py -->

## 練習與解答

**請先判斷：** 食物鐵含量10mg、假設吸收2mg，能否直接和標示每日參考15mg比 $\frac{2}{15}$ ？

<details><summary>展開計算與理由</summary>

這混合吸收量與攝取參考的分母，通常不適當。先確認參考值是攝取還是生理需求、採何種生物可利用假設；不能未對齊就算不足比例。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：鐵](https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/)
- [NIDDK：消化系統如何運作](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
