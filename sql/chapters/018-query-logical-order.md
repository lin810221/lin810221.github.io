# SQL的邏輯順序與查詢除錯

用分階段結果定位錯誤，再用執行計畫理解實際運算。

## 先掌握邏輯層次

一個常見查詢可按FROM與JOIN、WHERE、GROUP BY、HAVING、視窗計算、輸出與排序等層次理解。這是語意上的解讀方式，不等於底層一定按這個物理順序執行；最佳化器可以重排符合語意的操作。

當結果不對，先把查詢拆成CTE，逐段看筆數與鍵。先確認來源有沒有漏資料，再確認JOIN是否擴大粒度，接著確認分組與空值，最後才看排序及LIMIT。一次調整很多條件，即使結果碰巧正確，也很難知道原因。

## 常見症狀與最小反例

總額突然翻倍，先檢查一對多JOIN；原本要保留的客戶消失，檢查LEFT JOIN後的WHERE；前幾筆每次不同，檢查完整排序。這些診斷都是假設，仍要用可重現的小資料證明，不靠症狀直接判定唯一原因。

## 為每一層留下證據

可以記錄輸入列數、輸出列數、鍵的唯一性、空值數與金額總和。資訊要能說明語意，不只是把整張表印進log。真實環境還需避免輸出私人資料與憑證；本課使用合成資料，因此可完整比對。

本章完成後，你應能先手算四筆付款訂單，再用SQL重現結果。接下來的JOIN與視窗不是全新的黑盒，而是建立在這些已確認的資料粒度與條件之上。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener" aria-label="放大SQL的邏輯順序與查詢除錯圖解"><img src="assets/figures/06.svg" alt="SQL的邏輯順序與查詢除錯：獨立教學算例中兩組大小不同，使用總和與筆數重建整體平均，說明不可讓組別取得相同權重。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SQL的邏輯順序與查詢除錯」讀圖：獨立教學算例中兩組大小不同，使用總和與筆數重建整體平均，說明不可讓組別取得相同權重。請用圖回答：總額翻倍時，應先把SUM改成SUM(DISTINCT amount_cents)嗎？</p></div>

## 自我檢查與解析

**題目：**總額翻倍時，應先把SUM改成SUM(DISTINCT amount_cents)嗎？

<details><summary>展開解析</summary><p>不應如此修補。不同訂單可能剛好有相同金額，DISTINCT會刪掉合法值；應先找到造成重複的JOIN粒度並修正。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab05.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab05.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
