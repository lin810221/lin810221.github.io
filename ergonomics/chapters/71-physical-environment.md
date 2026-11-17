# 物理環境：照明、溫度、地面與設備

把身體周圍條件納入任務，不只盯關節。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/36-environment-route.svg" target="_blank" rel="noopener" aria-label="放大：物理環境與流程：把任務走完"><img src="assets/figures/36-environment-route.svg" alt="工作流程可能跨取料、組裝和運送，照明、地面、維護及空間都需確認，不能由新設備名字推適配。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 36｜物理環境與流程：把任務走完</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>從圖中選一個環境條件補到任務，說明看不清、地面或輪具問題也會改變操作；不把它們全部歸給姿勢不標準。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a> · <a href="https://www.hse.gov.uk/msd/pushpull/index.htm">HSE：推拉評估</a> · <a href="https://www.hse.gov.uk/msd/uld/art/faq.htm">HSE：ART用途限制</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 條件會改變操作

看不清、太冷、通道窄、輪具卡住或桌面不穩，都可能改變用力與姿勢。這些不應全歸成個人動作不標準，改善可從來源和維護開始。

## 照明與視覺

精細工作與螢幕有不同需求，反光、陰影、對比和個人視覺都重要。不把單一亮度百分比或一個數字套所有工作，也不以無反光宣告全部風險已處理。

## 地面和裝備

摩擦、坡度、障礙、鞋具與手套等可能影響可行性。需要實際任務與相關規範，不能只因設備新或標示符合某名稱就省略評估。

## 程式中的未知

範例列照明、地面、輪具和溫度是否已知，沒資料不填良好。它協助提出下一步，不測環境、不作正式法規符合結論。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 36_environment_context.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:36_environment_context.py -->

## 練習與解答

**先想一想：** 更換一個新工具後，就能假設所有環境與維護問題消失嗎？

<details><summary>展開驗算與理由</summary>

不能。新設備仍需和路徑、空間、維護、使用者及工作流程一起評估，其他條件不會自動變已知。

</details>

## 正式來源與進一步閱讀

- [HSE：DSE工作站專用檢核表](https://www.hse.gov.uk/pubns/ck1.pdf)
- [HSE RAPP：全身推拉工作](https://www.hse.gov.uk/msd/pushpull/index.htm)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [台灣職安法：現行第6條](https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=N0060001&flno=6)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
