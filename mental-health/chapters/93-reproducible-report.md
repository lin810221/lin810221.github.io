# CSV、SVG與JSON：從資料到可重跑摘要

讓圖和算術可以回到原始輸入。

## 三種輸出

diary_observations.csv列日期、評分、狀態與尺度；SVG用點呈現14天觀察，缺漏明示且不跨缺漏接線；JSON含摘要、工作計畫、來源、雜湊和限制。

## 環境簡單

Python3.15.2只用標準函式庫，預設無連網、API或模型下載。相同資料與程式可重跑同一算術；完整ZIP也可獨立解壓執行，不需原專案目錄。

## 報告不覆寫

47入口在暫存目錄示範；48未給路徑也使用暫存，要保留結果需指定新資料夾。既有路徑拒絕覆寫，避免混入舊結果，不需刪除陌生資料解錯。

## 稽核要點

檢查14個排定日、12個有效觀察、兩天缺漏、完整平均未知、計畫B差額未知與五個資料雜湊。雜湊確認輸入身份，不證明因果、真實或臨床適用。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 47_report_preview.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:47_report_preview.py -->

## 練習與解答

**先想一想：** 報告圖有14個日期位置，就代表14筆有效評分嗎？

<details><summary>展開示範答案與理由</summary>

不代表。本例有兩天缺漏，所以有效12；需看狀態與摘要，圖的位置不是觀測數證明。

</details>

## 來源與進一步閱讀

- [Python3.15.2官方正式發布](https://www.python.org/downloads/release/python-3152/)
- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [NICE NG225：自傷照護及風險工具限制](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)
- [WHO：工作心理健康正式指南（2022）](https://www.who.int/publications/i/item/9789240053052)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
