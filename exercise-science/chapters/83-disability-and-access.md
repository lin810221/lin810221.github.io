# 身心障礙、可及性與不同資料體系

把活動形式、設備與支持納入課程，不以標準成人步行資料代替所有人。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/42-access-professional.svg" target="_blank" rel="noopener" aria-label="放大：可及性、慢性病與專業合作"><img src="assets/figures/42-access-professional.svg" alt="入口與任務間的箭頭表示需消除參與障礙，非評估通過；疾病和藥物等條件仍需適當專業。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 42｜可及性、慢性病與專業合作</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>從入口追到任務，逐項找設備、動線、資訊與協助可能阻擋的地方；不要以一個障礙名稱推定所有使用者有相同能力或需求。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/publications/i/item/9789240015128">WHO：2020身體活動與久坐正式指南</a> · <a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 可及性是實際條件

場地、設備、交通、溝通和支持影響參與；能力與障礙狀況不同，活動可有輪椅移動、水中、機械或其他合適形式。先問個人目標與條件，不以缺少某種形式推論不能受益。

## 資料體系不同

2024成人、長者與輪椅Compendium使用各自的資料和基準，不能因欄名都MET就套相同 $\frac{\frac{3.5mL}{kg}}{min}$ 。標準表也不是個人實測，未知時需保留，不能偷用成人步行值。

## 教學實驗

虛構輪椅活動有20分鐘，但個人限制、設備細節和相應MET未知；程式不補步行耗能，也不因時間已知就產生個人熱量或安全分數。可先補任務與資料來源。

## 專業與環境合作

依個人需要與醫療、物理治療或合格活動專業協調，調整設備和任務。一般原理提供共同語言，臨床限制和輔具使用不能由通用模板取代。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 42_accessible_record.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:42_accessible_record.py -->

## 練習與解答

**先自己判斷：** 輪椅活動20分鐘，可以直接套成人步行MET算精準耗能嗎？

<details><summary>展開理由與驗算</summary>

不可以。任務、資料體系、基準與個人條件不同，需相應來源並保留估計限制，不能用方便的值取代未知。

</details>

## 官方來源與研究

- [CDC：慢性健康狀況與身心障礙活動](https://www.cdc.gov/physical-activity-basics/guidelines/chronic-health-conditions-and-disabilities.html)
- [Compendium：輪椅活動資料體系](https://pacompendium.com/adult-wheelchair-users-compendium/)
- [Compendium：高齡者不同的MET基準](https://pacompendium.com/older-adult-compendium/)
- [2024成人身體活動Compendium與年齡範圍](https://pacompendium.com/adult-compendium/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
