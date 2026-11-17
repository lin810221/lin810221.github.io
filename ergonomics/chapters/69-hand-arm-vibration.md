# 手－手臂振動A(8)：加權、時間和單位

用已符合量測方法的輸入示範，不把手機數值當正式暴露。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/35-vibration-types.svg" target="_blank" rel="noopener" aria-label="放大：HAV與WBV：同單位也不是同方法"><img src="assets/figures/35-vibration-types.svg" alt="左側手工具接觸，右側乘坐設備接觸；輸入、軸向權重與時間方法不同，不能直接混算。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 35｜HAV與WBV：同單位也不是同方法</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指手工具接觸，再說HAV需已頻率加權三軸合成和實際觸發時間；多段依平方時間關係處理，不直接算術平均。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hse.gov.uk/vibration/hav/index.htm">HSE：手臂振動</a> · <a href="https://www.hse.gov.uk/vibration/wbv/regulations.htm">HSE：WBV</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 輸入先符合方法

a_hv是相應頻率加權的三軸合成振動值，單位m/s²；不是任意加速度或單軸未加權手機讀值。T為實際振動暴露時間，不直接用整個班表。

## 八小時參考算術

$$
A(8)=\sqrt{\frac{\sum_i a_{hv,i}^{2}T_i}{8\,h}}
$$

程式T用分鐘、分母480分鐘，需同一類暴露且時間不重疊。4m/s²暴露2小時得到2m/s² A(8)；再加2m/s²兩小時，合計√5約2.236。

## 不能直接算術平均

平方與時間權重很重要，多工具不把兩個A(8)直接相加。日資料不完整或某段未知，完整A(8)也未知；已知小計另列，不能稱全日。

## 不是疾病機率

HSE英國HAV行動值2.5、限值5m/s² A(8)有其法規背景，不是台灣統一標準，低於也非個人零風險。本課只做算術，不自動判合規或診斷。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 35_vibration_a8.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:35_vibration_a8.py -->

## 練習與解答

**先想一想：** 把兩個振動值直接平均，再乘整班8小時，就完成正式HAV評估嗎？

<details><summary>展開驗算與理由</summary>

沒有。需正確加權合成、實際觸發時間與多段平方時間關係，完整量測、方法和法規背景也要確認。

</details>

## 正式來源與進一步閱讀

- [HSE L140：手－手臂振動正式方法](https://www.hse.gov.uk/pubns/priced/l140.pdf)
- [HSE：英國HAV行動值與限值](https://www.hse.gov.uk/vibration/HAV/responsibilities.htm)
- [HSE：英國全身振動的不同方法](https://www.hse.gov.uk/vibration/wbv/regulations.htm)
- [台灣職安法：現行第6條](https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=N0060001&flno=6)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
