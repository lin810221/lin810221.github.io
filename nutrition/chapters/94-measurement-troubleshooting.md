# 常見錯誤排查：數字合理不代表問題定義正確

依單位、基準、形式、來源與時間逐步找到錯誤。

## 第一層：輸入

檢查g／mg／μg、g／mL、每份／每100、生／熟、可食部／購買重與乾粉／沖泡後。千倍錯誤、份數錯位與密度假設，是比小數修整更優先的問題；負值、非有限數與零分母應拒絕。

## 第二層：語意

總糖不是自由糖，可利用碳水不含本課另列纖維，鈉不是食鹽，DFE不是原始folic acid，IU不能泛用換質量。即使每行算術都正確，錯誤欄位對應仍會產生錯誤結論。

## 第三層：參考

NRV、RDA、AI、UL、CDRR的用途與族群不同；草案、正式公告與施行日期分開。限定來源與化學形式不相符時，不勉強計算百分比。缺資料應顯示未知，不是0。

## 第四層：解讀與技術

部分日誌不能稱全日攝取，情境界限不能稱95%區間，程式成功不能稱健康已驗證。若本機import失敗，先從examples目錄執行並核對Python；離線網站的課文變更要重跑build，不直接修改生成JS。

## 練習與解答

**請先判斷：** 程式沒有報錯且數字都正，是否已證明分析適用？

<details><summary>展開計算與理由</summary>

沒有。還要核對語意、基準、來源、族群與解讀；程式成功只是其中一層，不能取代問題定義與資料查核。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)
- [TFDA：食品營養標示指引手冊](https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&id=f639057139719594572)
- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
