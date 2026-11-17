# 間歇訓練：工作、恢復與總時鐘

把結構寫清楚，不用HIIT標籤取代強度與恢復資訊。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/27-interval-review.svg" target="_blank" rel="noopener" aria-label="放大：間歇總時鐘與整週核對"><img src="assets/figures/27-interval-review.svg" alt="上排分工作恢復，下排分計畫完成未知；圖只整理時序，未將所有段落自動歸為同一強度。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 27｜間歇總時鐘與整週核對</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿上排分別加總工作和恢復，再說出總時鐘能回答與不能回答什麼；恢復時心率仍高不等於整段都能算指定費力活動。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/publications/i/item/9789240015128">WHO：2020身體活動與久坐正式指南</a> · <a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 每個段落要有定義

工作時間、強度來源、恢復形式與時間、重複數、暖身與收尾都是條件。衝刺、較長高強度間歇和一般交替步行不同，不能因都分段就套同一生理結論。

## 時鐘驗算

6次工作60秒、次間恢復90秒，末次後不另計恢復，工作360秒、恢復450秒；加暖身600與收尾300，總1710秒即28.5分鐘。若末次另有90秒恢復則30分鐘，必須在計畫中明說。

## 強度不由名字保證

工作段強度要用合適任務與參考描述，恢復可能很輕也可能是活動恢復。不能把總28.5分鐘全自動當費力活動，心率還高也不證明每段有相同成本。

## 實際完成與耐受

記每段完成、速度或功率、感受和恢復，未完成不補成計畫值。若目標品質無法維持，需檢查結構而非只鼓勵硬撐；個人適用需看健康、經驗和監督等背景。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 27_interval_clock.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:27_interval_clock.py -->

## 練習與解答

**先自己判斷：** 上述6次示例為何不是6個恢復段？

<details><summary>展開理由與驗算</summary>

因定義是只在工作段之間恢復，6次有5個間隔；若另計末次恢復，總時間會不同，不能默默混入。

</details>

## 官方來源與研究

- [CDC：談話測試、絕對與相對強度](https://www.cdc.gov/physical-activity-basics/measuring/)
- [2026高強度間歇並行訓練統合分析](https://pubmed.ncbi.nlm.nih.gov/42759564/)
- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
