# 平衡、穩定與感覺控制

理解任務如何改變需求，不把更晃當所有目標都更好。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/35-balance-control.svg" target="_blank" rel="noopener" aria-label="放大：支持面、感覺訊息與軀幹控制"><img src="assets/figures/35-balance-control.svg" alt="簡化人形與支持面強調感覺、肢體和軀幹協調，虛線不是個人實測重心或平衡風險界線。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 35｜支持面、感覺訊息與軀幹控制</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出支持面，再列視覺、前庭與本體感覺的線索，說明平衡是多系統整合；不用閉眼或單腳挑戰來替圖中的箭頭證明。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.nidcd.nih.gov/health/balance-disorders">NIDCD：平衡的正常功能</a> · <a href="https://training.seer.cancer.gov/anatomy/nervous/tissue.html">NCI：神經組織</a> · <a href="https://training.seer.cancer.gov/anatomy/muscular/structure.html">NCI：骨骼肌構造</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 多個系統共同工作

視覺、前庭、體感、肌力與控制共同支持姿勢和動態任務。單腳站、移動、轉身和搬物有不同需求；一個靜態成績不直接表示所有生活場景能力。

## 穩定與訓練目標

不穩定環境可能適合某些控制練習，卻可能限制可施加外力；若目標是最大力量或功率，不是越晃越好。先說要練哪種能力，再選條件，而非以困難感排名品質。

## 測試的重複性

腳位、視線、輔助、表面、計時與終止規則都會影響結果。範例用虛構重複測量看差值分布，不把它轉成跌倒風險或個人安全判定。

## 日常和生命階段

長者指南包含平衡與功能活動，但具體形式需看能力、環境和支持。安排需避免在沒有適當保護下刻意製造失衡；有眩暈、跌倒或疾病背景時尋求相應評估。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 35_balance_repeatability.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:35_balance_repeatability.py -->

## 練習與解答

**先自己判斷：** 站在更不穩平台舉重，是否對最大力量一定更有效？

<details><summary>展開理由與驗算</summary>

不一定。任務可能更偏控制並限制外力輸出；需看目標與證據，困難感不是效果的充分指標。

</details>

## 官方來源與研究

- [CDC：長者有氧、肌力與平衡](https://www.cdc.gov/physical-activity-basics/guidelines/older-adults.html)
- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Weir：重測信度、ICC與SEM方法](https://pubmed.ncbi.nlm.nih.gov/15705040/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
