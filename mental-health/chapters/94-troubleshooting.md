# 排錯：環境、輸入、缺漏與錯誤結論

從資料條件找問題，不編造一個能通過的數字。

## 環境找不到模組

完整解壓examples、共用模組和data，從examples執行；不要只複製編號腳本。程式無第三方依賴，可指定已安裝3.15.2執行檔，不需要改全系統環境。

## 輸入被拒絕

NaN、無限值、布林冒充數字、負分鐘、錯時刻或零分母，都應核對原始意義。不要為了消錯把未知改成0；日期跨午夜需明示翌日，HH:MM採24小時格式。

## 完整摘要為未知

缺漏會傳播，這可能正是設計目的。可用平均不等於完整，三日移動平均需要完整窗口，計畫有未知任務就不能算精確餘量。不是換更多小數位就能補足資訊。

## 結果看起來顯著

先問結果、比較、期限與假設。相關不等於因果，d不等於臨床重要，低日記分不等於安全；工具成功也沒有完成診斷。

## 網頁修改與儲存

改Markdown後在根目錄建置本課；course-data.js與ZIP是生成檔。筆記與進度留在目前瀏覽器，不跨裝置同步；私人內容不需輸入，課程練習可用合成案例。

## 練習與解答

**先想一想：** 程式因缺漏輸出None，應把它改成0讓圖更完整嗎？

<details><summary>展開示範答案與理由</summary>

不應。None表示未知，0是實際數值，替換會改變資料與結論；應理解規則並保留缺漏。

</details>

## 來源與進一步閱讀

- [Python3.15.2官方正式發布](https://www.python.org/downloads/release/python-3152/)
- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [NIMH：心理治療](https://www.nimh.nih.gov/health/topics/psychotherapies)
- [NICE NG225：自傷照護及風險工具限制](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
