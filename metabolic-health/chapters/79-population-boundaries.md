# 兒少、成人與特殊族群：不要外推同一界線

先確認指南在談誰，再理解數字。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/40-life-stage-boundaries.svg" target="_blank" rel="noopener" aria-label="放大：生命階段與適用族群"><img src="assets/figures/40-life-stage-boundaries.svg" alt="人物大小只為辨識情境，不是兒少、成人或長者的能力比例，界線不得直接外推。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 40｜生命階段與適用族群</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出各人物代表不同情境，再列原資料需要哪些族群與方法條件；說明成人界線不能直接縮小套兒少。</div>

<p class="health-figure-sources">圖解依據：<a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a> · <a href="https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance">NIDDK：胰島素阻抗與正常調節</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 成人規則不是全齡規則

台灣一般成人BMI界線、成人血壓或PREVENT年齡範圍，都有明確族群。兒童成長、青春期、孕哺和其他特殊情境需要不同評估；不能只因公式能輸入就認為適用。

## 成長與營養

兒少需要支持生長、發展與家庭環境，體位評估常涉及年齡、性別與成長圖。成人減重百分比不可直接套用，公開排名或限制飲食也可能造成傷害。本課不產生兒童體位診斷或熱量處方。

## 同一指標不同解釋

血紅素狀態、懷孕、肌肉量、衰弱與急性疾病等，可能改變檢驗和模型適用性。確認已知與未知比把所有欄位塞進成人計算器重要。程式只檢查情境標籤是否提供，不將其變成疾病預測。

## 課程如何劃範圍

主線以一般成人健康教育為主；特殊族群章說明為何需另尋正式評估，不建立家庭自行診療表。若想深入兒科、孕產或老年醫學，可作未來獨立課程，但目前不建立尚未完成的課程連結。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 40_life_stage_context.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:40_life_stage_context.py -->

## 練習與解答

**先自己判斷：** 成人BMI公式可以算兒童的數值，所以能用成人界線判讀嗎？

<details><summary>展開驗算與理由</summary>

不能。算術可得比值不代表成人分類適用；兒少需成長與年齡等背景，營養和評估目的也不同。

</details>

## 官方來源與研究

- [國健署：台灣成人體位標準](https://www.hpa.gov.tw/542/9737/n)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [2025 Lancet Commission：臨床肥胖定義框架](https://pmc.ncbi.nlm.nih.gov/articles/PMC11870235/)
- [2026台灣高齡高血壓正式指南](https://pubmed.ncbi.nlm.nih.gov/42926177/)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
