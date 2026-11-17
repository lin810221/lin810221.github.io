# 完整專題：可重現的飲食資料分析交付

串起資料契約、計算、測試、圖表與限制，完成獨立專題。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/48-project-review.svg" target="_blank" rel="noopener" aria-label="放大：資料、圖與解釋一起交付"><img src="assets/figures/48-project-review.svg" alt="資料表、觀察圖和說明來源三份成果相互核對，保留假設與未知；圖柱為任意示意，不表示真實營養量或疾病機率。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 48｜資料、圖與解釋一起交付</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>將完整專題的資料、圖和說明各配到一個核對問題，指出來源或缺漏不一致時應先查哪裡，不把成功產出當健康認證。</div>

<p class="health-figure-sources">圖解依據：<a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://www.python.org/downloads/release/python-3152/">Python3.15.2正式發布</a> · <a href="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx">NIH ODS：營養參考值的不同用途</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 專題任務

使用隨課虛構食物與部分日誌，交付可重跑報告；評量重點是來源、單位、缺值、參考範圍與可重現，不是為真人開菜單。先讀examples/README與模型限制，再執行48_complete_report.py。

## 交付清單

保留輸入檔與SHA-256、Python版本、日期、每項計算假設、CSV、SVG、JSON、測試結果與限制。日期與雜湊幫助追溯，不保證內容正確；更新資料後需重跑並比對差異。

## 必須通過的行為

糖無一般NRV不產生百分比；未知微量營養不補0；維生素換算要求形式；限定來源的UL不亂加；圖表不加個人目標線；輸出目錄已存在時不覆寫。這些直接影響分析含義，比只測函式有回傳值更重要。

## 從專題到真實資料

替換資料前先保留資料契約、出處、使用權與版本，重新確認食品描述、準備狀態及缺值；真實產品不能沿用虛構數值。若涉及真人健康評估，資料分析還需專業背景與適用方法，不能只換檔名就升級為診斷工具。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 48_complete_report.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:48_complete_report.py -->

## 練習與解答

**請先判斷：** 真實分析只要把synthetic改false就完成嗎？

<details><summary>展開計算與理由</summary>

不行。須以真實可追溯來源重建資料、驗證契約與方法，並確認使用範圍；標籤改字不會使虛構數字成為真實證據。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
