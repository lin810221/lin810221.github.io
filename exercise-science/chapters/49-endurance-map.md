# 耐力訓練地圖：持續、間歇與任務需求

從目標、強度和可持續時間理解有氧安排，不只累積里程。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/25-endurance-modes.svg" target="_blank" rel="noopener" aria-label="放大：持續與間歇：方式和強度分開"><img src="assets/figures/25-endurance-modes.svg" alt="兩排虛構時鐘區分持續與交替安排，區塊長度不表示健康效益或實際生理劑量等效。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 25｜持續與間歇：方式和強度分開</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出有無恢復段，再說出圖中沒有給出的強度、模式與任務；不能只看交替色塊就認定是HIIT，也不能只看連續色塊判中等。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/publications/i/item/9789240015128">WHO：2020身體活動與久坐正式指南</a> · <a href="https://www.nhlbi.nih.gov/health/lungs/breathing-benefits">NHLBI：呼吸及氣體交換</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 耐力不是一種固定速度

支持日常活動、完成5km、長時間騎車與反覆球類回合，需求不同。有氧供能、經濟性、可維持強度、技能和策略共同影響結果，不能只用週里程或最大耗氧排名所有任務。

## 持續與間歇

持續活動便於累積某種任務時間，間歇將工作與恢復分段；兩者都可依強度與目標有不同用途。HIIT不等於所有間歇，更不代表每個工作段都必須全力。

## 配速作為外在量

5km用30min，平均10km/h、360秒/km；28min則約10.71km/h、336秒/km。這是同距離算術，仍需路線、氣候和計時一致才能較合理比較能力。

## 從可行性起步

先記目前活動、目標、可用時間與反應，再理解持續或間歇如何服務目標。教材不由一次配速開個人週跑量，也不將群體活動指南等同競賽課表；兩者可以互相參照但用途不同。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 25_running_pace.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:25_running_pace.py -->

## 練習與解答

**先自己判斷：** 平均速度一樣，是否持續跑和短間歇的生理需求一定一樣？

<details><summary>展開理由與驗算</summary>

不一定。工作、恢復、加速與總時長等不同，平均值可能掩蓋結構；需把實際任務寫清楚。

</details>

## 官方來源與研究

- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [CDC：談話測試、絕對與相對強度](https://www.cdc.gov/physical-activity-basics/measuring/)
- [2026並行訓練傘狀回顧](https://pubmed.ncbi.nlm.nih.gov/41762427/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
