# ATP與三種供能路徑：一直共同工作

理解磷酸原、醣解與氧化供能，不用固定秒數切換開關。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/10-energy-overlap.svg" target="_blank" rel="noopener" aria-label="放大：三種供能路徑重疊參與"><img src="assets/figures/10-energy-overlap.svg" alt="三條曲線只表共同參與及相對角色可改變，不是各路徑的實測百分比，沒有固定秒數切換線。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 10｜三種供能路徑重疊參與</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>在同一時間位置指向三條曲線，說明它們可以共同參與；不要把交點當所有人固定切換秒數，並補上強度與持續時間條件。</div>

<p class="health-figure-sources">圖解依據：<a href="https://training.seer.cancer.gov/anatomy/muscular/structure.html">NCI：骨骼肌構造</a> · <a href="https://www.nhlbi.nih.gov/health/lungs/breathing-benefits">NHLBI：呼吸及氣體交換</a> · <a href="https://www.nhlbi.nih.gov/health/heart/blood-flow">NHLBI：心臟血流</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## ATP是直接能量媒介

肌肉活動和相關運輸需要ATP，身體透過多條路徑再合成。磷酸原提供快速支持，醣解與氧化路徑也參與；不是前十秒只有一條，再突然切換到另一條，比例受強度、時間、恢復與訓練等影響。

## 功率與容量

能快速供應多少與能維持多久是不同問題。短促高力、反覆間歇和長時間活動有不同需求，但任何一種運動都不能只用有氧或無氧兩字完整描述；間歇恢復也有生理活動。

## 乳酸的角色

乳酸不是訓練後好幾天痠痛的殘留垃圾；其產生、運輸與利用屬代謝的一部分。量到較高血乳酸不自動等於只有無氧工作，也不從一次採血直接給出所有訓練區域。

## 連到循環

供氧需肺、血液、循環和組織利用配合。範例以假設心率與每搏量算心輸出，讓單位清楚；它沒有量到個人的實際輸送、代謝比例或運動許可。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 10_cardiac_output.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:10_cardiac_output.py -->

## 練習與解答

**先自己判斷：** 跑到固定第30秒，是否所有供能突然由磷酸原改成醣解？

<details><summary>展開理由與驗算</summary>

不是。多路徑共同參與，比例依任務和條件變化；固定秒數圖是粗略示意，不能當個人能量系統開關。

</details>

## 官方來源與研究

- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [OpenStax：肌纖維類型](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-5-types-of-muscle-fibers)
- [OpenStax：運動與肌肉表現](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-6-exercise-and-muscle-performance)
- [Compendium：標準MET單位](https://pacompendium.com/unite-conversions/)
- [OpenStax：心臟生理與心輸出量](https://openstax.org/books/anatomy-and-physiology-2e/pages/19-4-cardiac-physiology)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
