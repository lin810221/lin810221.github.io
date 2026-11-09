# 整合案例：三天部分飲食紀錄報告

生成CSV、SVG與JSON，把資料身份、缺漏與解讀一起交付。

## 輸入有哪些

十筆虛構食物、三天部分日誌、明示來源的參考表與metadata，全部本機可讀。不下載個人健康資料，也不假裝是台灣飲食調查；每一列份量和單位都可追溯。

## 產出與檢查

CSV每營養素列完整量、已知小計與缺值項；SVG標題明示部分觀察，不加需要量線；JSON包含版本、情境、資料雜湊及檢查。第三天鈣的完整總量故意未知，以測試缺值能保留。

## 執行方式

可先跑47_case_report.py在暫存目錄觀察，再用48_complete_report.py --output my-nutrition-report交付新目錄。已存在目錄不覆寫，避免把舊報告混成新結果；報告和原始資料可一起比對。

## 解讀界線

圖表描述已記錄小計，不是建議熱量或完整菜單；NRV比較也不作缺乏或安全診斷。程式測試能驗證資料行為與算術，不能把虛構食物變成實測值，也不能證明個人飲食適當。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 47_case_report.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:47_case_report.py -->

## 練習與解答

**請先判斷：** 報告中空白鈣總量能否改0讓圖表順利？

<details><summary>展開計算與理由</summary>

不能。應保留未知和已知小計，並追查缺值食物；圖表應適應資料語意，不能反過來篡改資料。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)
- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
