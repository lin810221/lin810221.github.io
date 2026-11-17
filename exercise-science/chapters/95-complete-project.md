# 完整專題：可重跑的訓練資料分析

把契約、計算、檢查和限制交給下一位閱讀者。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/48-project-map.svg" target="_blank" rel="noopener" aria-label="放大：完整專題：把任務、資料與限制連起來"><img src="assets/figures/48-project-map.svg" alt="四個專題面向互相核對：問題、資料、方法和交付；完成教學專題不等於個人訓練處方或醫療證明。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 48｜完整專題：把任務、資料與限制連起來</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿四張卡把一份虛構訓練資料專題的問題、資料、算術與限制串起來；能重跑只支持交付一致，不等於得到了個人最佳課表。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a> · <a href="https://www.who.int/publications/i/item/9789240015128">WHO：2020身體活動與久坐正式指南</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 專題任務

用隨課虛構資料產出獨立報告，不為真人設計最佳課表。驗收重點是同輸入可重現、未知保留、來源清楚、模型不越界；閱讀examples/README後執行48_complete_project.py。

## 交付內容

保留五個資料檔與SHA-256、Python版本、查核日期、模型假設、CSV、SVG、JSON和測試結果。雜湊只辨認檔案是否改變，不保證內容真實；重建後要比對資料與輸出是否相符。

## 必須通過的行為

未知日不補0、徒手負荷不造kg、量表不混用、零分母不亂算、ACWR無安全區、任意模型不預測準備度。輸出新目錄避免舊檔混入，ZIP解壓後不依賴原始專案路徑。

## 轉向真實資料

更換資料前確認來源、使用權、隱私、任務、單位、測法與缺值，重新驗證契約。真人健康與訓練決策還需適用方法與專業背景，不能只換CSV就把教學報告升級為處方工具。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 48_complete_project.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:48_complete_project.py -->

## 練習與解答

**先自己判斷：** 把metadata的synthetic改false，就能把示例當真實訓練研究嗎？

<details><summary>展開理由與驗算</summary>

不能。必須以真實可追溯資料重建，核對使用權和方法；標籤改字不會改變數字的來源或證據等級。

</details>

## 官方來源與研究

- [Python 3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Impellizzeri等：ACWR概念與方法陷阱](https://pubmed.ncbi.nlm.nih.gov/32502973/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
