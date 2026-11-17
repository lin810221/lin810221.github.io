# 循環與混合課：時鐘不等於劑量等效

算清站點、過渡和恢復，分開有氧、阻力與技能目的。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/32-circuit-rounds.svg" target="_blank" rel="noopener" aria-label="放大：循環站與反覆回合的時序"><img src="assets/figures/32-circuit-rounds.svg" alt="虛構站次與回合分出工作及轉換，沒有以總時鐘判有氧、肌力或專項劑量等效。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 32｜循環站與反覆回合的時序</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿每個站分工作與換站，寫負荷、動作與努力條件；即使總分鐘相同，也不能宣稱已得到相同有氧或阻力訓練劑量。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a> · <a href="https://www.who.int/publications/i/item/9789240015128">WHO：2020身體活動與久坐正式指南</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 一種結構多種用途

循環把多個站點或任務串起來，可為方便、綜合活動或特定訓練。名字本身不保證每肌群刺激、心肺強度或技能品質；需看站點內容、阻力、努力和休息。

## 時間計算

8站各40秒、站間20秒、末站後不另算恢復，工作320秒、間隔140秒；加暖身300與收尾180，總940秒。若還有器材調整、走動或多輪間休，要另外加，不能假裝總時長已含一切。

## 氣喘與力量刺激

全課很喘不表示每個動作都對最大力量或肌肥大最佳；高負荷也不一定整段都符合費力有氧定義。每一目標要有相應變數，不能用整堂感受取代所有單組資訊。

## 改課表時的查核

刪休息可能提高時效，卻也改變可完成阻力、技術和感受；不應說完全保留原介入。先寫固定與改變的條件，再觀察實際完成，避免只靠汗量評估成效。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 32_circuit_clock.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:32_circuit_clock.py -->

## 練習與解答

**先自己判斷：** 8站示例只計工作320秒，是否就是完整課長？

<details><summary>展開理由與驗算</summary>

不是。還有7個站間隔140秒、暖身300和收尾180，共940秒；額外過渡若存在還需另列。

</details>

## 官方來源與研究

- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [CDC：談話測試、絕對與相對強度](https://www.cdc.gov/physical-activity-basics/measuring/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
