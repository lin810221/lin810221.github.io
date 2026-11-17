# 重複、峰值與工作循環：平均之外的資訊

把頻率、施力與時序一起描述。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/31-repetition-time.svg" target="_blank" rel="noopener" aria-label="放大：重複、施力與持續的共同觀察"><img src="assets/figures/31-repetition-time.svg" alt="同一總次數可分散或集中，需記定義、力與姿勢等條件；時間區塊無疾病與安全色帶。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 31｜重複、施力與持續的共同觀察</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>用不同集中方式標記相同次數，指出平均之外還缺峰值、順序和恢復；圖不能直接轉成正式重複作業分數。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hse.gov.uk/msd/uld/art/faq.htm">HSE：ART用途限制</a> · <a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 定義動作和循環

一件產品可需要多個抓握，一個循環可包含左右不同活動。正式工具有定義，原創觀察也需明示，不能用容易取得的產量直接代替手部頻率。

## 同平均不同形狀

60次/10分鐘與120次/20分鐘都為6次/分鐘，但集中、均勻、力、姿勢與等待可能不同。平均不會自動保留高峰或局部持續。

## 恢復和工作輪換

是否改變需求要看實際內容，不是只換崗位名稱。訓練、速度要求、人力和流程也影響暴露，不能讓輪換變成更多人承擔相同高需求。

## 原創實驗

程式只比較明示窗口率和活動比例，沒有ART分數或傷害預測。取樣和其他資料應服務真正問題，必要時使用正式工具與受訓評估。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 31_repetition_blocks.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:31_repetition_blocks.py -->

## 練習與解答

**先想一想：** 兩段平均都是6次/分鐘，就可合併當作所有作業條件相同嗎？

<details><summary>展開驗算與理由</summary>

不能。力、姿勢、節奏、工作與恢復可能不同，平均只是一部分資訊。

</details>

## 正式來源與進一步閱讀

- [HSE ART：上肢重複作業工具](https://www.hse.gov.uk/msd/uld/art/index.htm)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
