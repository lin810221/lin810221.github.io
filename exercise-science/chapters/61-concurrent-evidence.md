# 有氧與阻力並行：不是一定互相抵銷

用2026回顧理解共同訓練，保留目標、方法和族群差異。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/31-concurrent-order.svg" target="_blank" rel="noopener" aria-label="放大：並行訓練與順序的比較條件"><img src="assets/figures/31-concurrent-order.svg" alt="兩排顛倒順序的虛構安排呈現比較問題，間隔及區塊寬度不是通用建議，也不宣稱一定相互抵銷。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 31｜並行訓練與順序的比較條件</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先確認兩排除了順序外還缺少哪些比較條件，再說出並行效果不能只憑兩種運動同週出現就判互相抵銷；結果需對準目標。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a> · <a href="https://www.who.int/publications/i/item/9789240015128">WHO：2020身體活動與久坐正式指南</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 並行的定義

同一時期安排有氧與阻力，可同堂、同日或不同日。相對只做其中一項，訓練時間、總負荷與結果可能不同；不能以同時練兩種就認定力量必掉或肌肉長不出來。

## 2026證據更新

2026傘狀回顧支持並行對綜合適能的價值，但高度訓練與菁英資料仍有限；同年HIIT並行回顧也提醒方法與亞組研究量限制。不能把未顯著差異說成所有情況完全等效，或只挑一個亞組作全民規則。

## 優先與時程

若主要目標是某一任務，順序、恢復間隔與實際品質值得觀察；沒有固定數小時間隔能保證所有人無干擾。例子中的6小時是明示情境，不是最新指南規定。

## 實際審核

列每種活動的目的、量、強度、順序和反應，尤其總量是否增加。單次疲勞造成表現下降，與長期適應差異不同；先看時間尺度，再談所謂干擾。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 31_concurrent_schedule.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:31_concurrent_schedule.py -->

## 練習與解答

**先自己判斷：** 有氧和阻力同週出現，是否足以判定增肌一定受損？

<details><summary>展開理由與驗算</summary>

不是。需看總量、方法、時程、經驗與結果；最新回顧不支持這種無條件結論，也不保證所有安排完全等效。

</details>

## 官方來源與研究

- [2026並行訓練傘狀回顧](https://pubmed.ncbi.nlm.nih.gov/41762427/)
- [2026高強度間歇並行訓練統合分析](https://pubmed.ncbi.nlm.nih.gov/42759564/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
