# 指南與最新版本：WHO和ACSM各回答什麼

以2026查核基線建立主線，分清發布年、查核日和研究截止日。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/02-evidence-dates.svg" target="_blank" rel="noopener" aria-label="放大：指南日期與證據範圍"><img src="assets/figures/02-evidence-dates.svg" alt="時間線標正式指南發布年份，查核日不把舊指南改名；不同來源回答不同族群與任務問題。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 02｜指南日期與證據範圍</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿時間線分別找到WHO2020與ACSM2026，說出發布日期和今天查核不是同一件事，並在原課文確認各自的適用族群。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/publications/i/item/9789240015128">WHO：2020身體活動與久坐正式指南</a> · <a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 健康活動與訓練最佳化

WHO2020正式指南處理不同族群的活動與久坐，2026更新說明頁不代表整套指南改名2026。一般成人有氧方向為每週150–300分鐘中等或75–150分鐘費力活動，或相當組合，另有肌力要求；一些活動比完全沒有好。

成人肌肉強化另建議每週至少兩天，涵蓋主要肌群；有氧分鐘不能自動替代這一面向。這是一般健康活動框架，不是每位讀者第一週必完成的固定課表。

## 2026阻力訓練立場

ACSM2026立場聲明於3月線上發布，刊於4月期刊，更新2009版本，對象主要是健康成人。它綜合到2024年10月的回顧搜尋；新發布不代表已涵蓋之後所有研究。主要建議與特定運動員或疾病處方不可混同。

## 原則與必要條件不同

進步可以來自多種阻力方式，不必每組都力竭、限定某種器材或先懂複雜週期化。不同目標的負荷與總量證據會逐章介紹；不能把傘狀回顧中的群體比較，變成每位讀者必須立刻達成的門檻。

## 成人分鐘換算

純教學把90分鐘中等與30分鐘費力合成150分鐘中等活動等效。這只處理成人有氧加權，不自動涵蓋肌力、平衡、久坐與個人背景，休息段也不能只因心率尚高就全算費力。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 02_guideline_context.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:02_guideline_context.py -->

## 練習與解答

**先自己判斷：** 查核日是2026-11-09，是否應把WHO2020指南和ACSM2009全部改名2026？

<details><summary>展開理由與驗算</summary>

不能。查核、原始發布與正式更新分開；WHO正式基線仍標2020，ACSM則採2026更新，舊文只有在比較歷史時明示使用。

</details>

## 官方來源與研究

- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [WHO：2026更新的身體活動說明](https://www.who.int/news-room/fact-sheets/detail/physical-activity)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
