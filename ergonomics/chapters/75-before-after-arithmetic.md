# 改善前後的算術：距離變化不是傷害降幅

區分模型輸出、暴露改變與健康成效。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/38-before-after.svg" target="_blank" rel="noopener" aria-label="放大：改善前後：先看條件是不是同一個"><img src="assets/figures/38-before-after.svg" alt="兩個外力作用位置示意，改距離可能改模型結果，但不是傷害風險等比例下降；其他條件需列明。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 38｜改善前後：先看條件是不是同一個</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>在兩情境列出哪些條件宣告相同、哪些仍未知，說明LI或外力矩差異不能直接叫受傷風險減少同百分比。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a> · <a href="https://www.cdc.gov/niosh/ergonomics/about/rnle.html">NIOSH：RNLE入口與正式手冊</a> · <a href="https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=N0060009&amp;flno=324-1">台灣設施規則324-1條</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 同一問題的兩個設計

虛構搬抬在其他RNLE條件相同時，水平距離由50cm改為25cm。HM由0.5變1，因此算式中的建議重量限值提高一倍，同負重的LI減半。這是公式中的關係，不代表疾病減少一半。

## 哪些條件真的相同

需確認重量、位置、頻率、時段、抓握、目的端控制與適用條件。若改料箱位置同時改變重量和頻率，就不能把所有差異都歸給水平距離。未知條件寫未知，不能為了比較填1。

## 百分比的分母

由20降到10，絕對差是−10，相對原值下降50%；反向由10升20則增加100%。基準為0時相對變化未定義，不能顯示0%或無限改善。本課程式會把不適用的結論保留為未知。

## 多項結果要並列

模型算式、觀察時間、工作者功能、產品品質與新危害都值得記錄。單項改善不能代替整體驗收，平均值也不能掩蓋其中某人無法使用或某段資料遺漏。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 38_before_after_arithmetic.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:38_before_after_arithmetic.py -->

## 練習與解答

**先想一想：** LI減半可以直接寫成受傷風險減少50%嗎？

<details><summary>展開驗算與理由</summary>

不可以。LI是特定模型及適用條件下的設計指標，不是個人傷害機率。需分開呈現模型算術、實際暴露與健康結果。

</details>

## 正式來源與進一步閱讀

- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [NIOSH：2021修訂與短工時更正](https://stacks.cdc.gov/view/cdc/110725)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
