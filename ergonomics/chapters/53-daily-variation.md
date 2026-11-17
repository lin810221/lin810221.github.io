# 活動變化與恢復：看實際需求是否不同

用排程與缺漏資料理解安排的限制。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/27-changes-and-care.svg" target="_blank" rel="noopener" aria-label="放大：活動變化與照顧任務的差異"><img src="assets/figures/27-changes-and-care.svg" alt="任務名稱不同不保證充分恢復，搬物與搬人的可變性也不同；需合適設備、協作與方法。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 27｜活動變化與照顧任務的差異</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>比較兩個工作段是否真的改變同一部位的需求，說明變換名稱不等於充分恢復；排程算術不能當個人休息處方。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a> · <a href="https://www.hse.gov.uk/msd/pushpull/index.htm">HSE：推拉評估</a> · <a href="https://www.cdc.gov/niosh/ergonomics/about/rnle.html">NIOSH：RNLE入口與正式手冊</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 變化可以有不同目的

減少持續姿勢、改變肌群需求、處理視覺或注意負擔，可能需要不同安排。不是所有任務切換都算同一恢復，也不是所有等待都沒有負荷。

## 指定時間只是算術

40分鐘某任務加5分鐘其他安排，三輪共135分鐘。這沒有建立法定額度、醫療處方或每個人的最佳間隔，需放回工作內容與需求。

## 資料缺漏要保留

兩段已知加一段未知，完整總量未知。不能把未記錄時段當休息，或用已知小計推全日暴露。

## 和一般活動分工

WHO公共衛生建議有年齡和背景，不等於工作復健課表。訓練主線可回運動科學，本課關注工作是否提供變化與可用資源。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 27_daily_variation.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:27_daily_variation.py -->

## 練習與解答

**先想一想：** 工作換名稱但仍相同緊握和伸取，就一定達成恢復嗎？

<details><summary>展開驗算與理由</summary>

不一定。需看實際力、部位、時間和工作方式，名稱與排程不是恢復生理證明。

</details>

## 正式來源與進一步閱讀

- [HSE：工作安排與休息的適用條件](https://www.hse.gov.uk/msd/dse/work-routine.htm)
- [OSHA：多種工作參考姿勢與變化](https://www.osha.gov/etools/computer-workstations/positions)
- [WHO：2026活動說明及2020正式指南入口](https://www.who.int/news-room/fact-sheets/detail/physical-activity)
- [NIOSH：2021修訂與短工時更正](https://stacks.cdc.gov/view/cdc/110725)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
