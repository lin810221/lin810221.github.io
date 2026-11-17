# RNLE適用性：哪些情境不能直接套

算公式之前先確認任務，不讓未知變理想。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/30-applicability-redesign.svg" target="_blank" rel="noopener" aria-label="放大：公式有邊界，改善要回到任務"><img src="assets/figures/30-applicability-redesign.svg" alt="同一搬運流程包含不同工作段，方法適用、未知和改善需分開，不把任意倍率補成1完成報告。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 30｜公式有邊界，改善要回到任務</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>選出哪些情境不能直接套本課RNLE算術，說明不適用不是把上限截斷後繼續算；未知倍率也不補成1。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cdc.gov/niosh/ergonomics/about/rnle.html">NIOSH：RNLE入口與正式手冊</a> · <a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a> · <a href="https://www.hse.gov.uk/msd/pushpull/index.htm">HSE：推拉評估</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 任務類型

指定條件的雙手人工搬抬，和單手、坐跪姿、受限空間、不穩定負荷、抱搬人、推拉或大量其他非搬抬工作不同。不可只因有重量就使用RNLE。

## 其他條件

物件、地面、環境、工時、頻率和控制要求等需依手冊確認。本課不是完整適用性問卷，使用者選「已確認」僅代表教學假設，不構成真實現場認證。

## 未知與零分母

FM或CM未知時，RWL與LI保持未知；RWL若為0，LI不能輸出0。0會誤導成沒有負擔，真正意思是不能由該分母得到有限比值。

## 選其他方法

推拉、上肢重複、電腦與人員轉移各有不同評估途徑，必要時由適當受訓專業協助。程式提供範圍與資料整理，不產生個人可搬重量。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 30_rnle_applicability.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:30_rnle_applicability.py -->

## 練習與解答

**先想一想：** 不知道FM時填1，是否可先當作無影響算完再說？

<details><summary>展開驗算與理由</summary>

不應。1是具體假設，不是缺資料的代號；未知需保留，不可用理想值掩蓋資訊不足。

</details>

## 正式來源與進一步閱讀

- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [NIOSH：RNLE現行入口（2026頁面更新）](https://www.cdc.gov/niosh/ergonomics/about/rnle.html)
- [HSE RAPP：全身推拉工作](https://www.hse.gov.uk/msd/pushpull/index.htm)
- [HSE：ART為何不適合鍵鼠DSE](https://www.hse.gov.uk/msd/uld/art/faq.htm)
- [HSE MAC：指定人工搬運工作](https://www.hse.gov.uk/msd/mac/index.htm)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
