# 完整專題：可重現的飲食資料分析交付

串起資料契約、計算、測試、圖表與限制，完成獨立專題。

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
