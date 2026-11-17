# 功能、活動度與結果方向

用適當任務觀察能力，先弄清是越高越好還是越低越好。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/15-baseline-change.svg" target="_blank" rel="noopener" aria-label="放大：基線、方向與未知觀察"><img src="assets/figures/15-baseline-change.svg" alt="時間線含一段缺漏並以虛線提示連接是假想，不當作實測；數值升降需依測試方向解讀。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 15｜基線、方向與未知觀察</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先替「完成時間」與「可用活動範圍」各寫改善方向，再看這條任意曲線；上升不一定都代表進步，必須保留原測試定義與條件。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 功能測試的任務性

起身、步行、搬物、平衡等可描述特定能力，測試條件與人群很重要。一項測試不涵蓋所有生活功能；時間、支撐和輔具等若改變，結果也可能不再直接可比。

## 活動度與控制

角度需記關節、主動被動、負重與方法。角度增加不直接代表疼痛改善或特定運動表現提高；平衡時間也不能單獨診斷跌倒風險，需要相應驗證與背景。

## 差值與百分比

30秒變28秒原始變化-2秒、約-6.67%；若任務以時間越低越好，方向可能有利。20cm變22cm為+10%，但要看誤差與實務重要性。基準0時不能用一般百分比定義，程式保留未知。

## 寫清楚觀察結論

用「在這個協定下觀察到」開頭，附單位、方向、測試品質和限制。若需醫療或跌倒評估，由合格專業人員處理；教材的數字方向不是診斷。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 15_change_direction.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:15_change_direction.py -->

## 練習與解答

**先自己判斷：** 時間從30變28，百分比是負，是否一定表示變差？

<details><summary>展開理由與驗算</summary>

不一定。需先知道任務方向，完成時間可能越低越好；仍需看誤差、條件和結果意義，不能只看正負號。

</details>

## 官方來源與研究

- [CDC：長者有氧、肌力與平衡](https://www.cdc.gov/physical-activity-basics/guidelines/older-adults.html)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [2024靜態伸展劑量與柔軟度統合分析](https://pubmed.ncbi.nlm.nih.gov/39614059/)
- [Weir：重測信度、ICC與SEM方法](https://pubmed.ncbi.nlm.nih.gov/15705040/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
