# 排錯：環境、輸入、缺漏與錯誤結論

從資料條件找問題，不編造一個能通過的數字。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/47-report-reading.svg" target="_blank" rel="noopener" aria-label="放大：圖表與來源：可核對，不代替理解"><img src="assets/figures/47-report-reading.svg" alt="同一份虛構資料連到表格、圖與說明，缺漏與來源仍需保留；檔案格式不是療效證據。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 47｜圖表與來源：可核對，不代替理解</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>遇到出乎預期的結果，依目的、輸入、缺漏、單位和來源逐項排查；不要為了讓圖完整而補0或改成理想值。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/questions-and-answers/item/stress">WHO：壓力問答</a> · <a href="https://www.nimh.nih.gov/health/topics/caring-for-your-mental-health">NIMH：照顧心理健康</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

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
